from asyncio import gather, sleep
from html import escape
from time import time
from mimetypes import guess_type
from contextlib import suppress
from os import path as ospath

from aiofiles.os import listdir, remove, path as aiopath
from requests import utils as rutils

from ... import (
    intervals,
    task_dict,
    task_dict_lock,
    LOGGER,
    non_queued_up,
    non_queued_dl,
    queued_up,
    queued_dl,
    queue_dict_lock,
    same_directory_lock,
    DOWNLOAD_DIR,
)
from ..common import TaskConfig
from ...core.tg_client import TgClient
from ...core.config_manager import Config
from ...core.torrent_manager import TorrentManager
from ..ext_utils.bot_utils import encode_slink, sync_to_async
from ..ext_utils.db_handler import database
from ..ext_utils.files_utils import (
    clean_download,
    clean_target,
    create_recursive_symlink,
    get_path_size,
    join_files,
    remove_excluded_files,
    move_and_merge,
)
from ..ext_utils.links_utils import is_gdrive_id
from ..ext_utils.status_utils import get_readable_file_size, get_readable_time
from ..ext_utils.task_manager import check_running_tasks, start_from_queued
from ..mirror_leech_utils.gdrive_utils.upload import GoogleDriveUpload
from ..mirror_leech_utils.rclone_utils.transfer import RcloneTransferHelper
from ..mirror_leech_utils.status_utils.gdrive_status import GoogleDriveStatus
from ..mirror_leech_utils.status_utils.queue_status import QueueStatus
from ..mirror_leech_utils.status_utils.rclone_status import RcloneStatus
from ..mirror_leech_utils.status_utils.telegram_status import TelegramStatus
from ..mirror_leech_utils.upload_utils.telegram_uploader import TelegramUploader
from ..telegram_helper.button_build import ButtonMaker
from ..telegram_helper.message_utils import (
    delete_message,
    delete_status,
    send_message,
    update_status_message,
)


class TaskListener(TaskConfig):
    def __init__(self):
        super().__init__()

    async def clean(self):
        with suppress(Exception):
            if st := intervals["status"]:
                for intvl in list(st.values()):
                    intvl.cancel()
            intervals["status"].clear()
            await gather(TorrentManager.aria2.purgeDownloadResult(), delete_status())

    def clear(self):
        self.subname = ""
        self.subsize = 0
        self.files_to_proceed = []
        self.proceed_count = 0
        self.progress = True

    async def remove_from_same_dir(self):
        async with task_dict_lock:
            if (
                self.folder_name
                and self.same_dir
                and self.mid in self.same_dir[self.folder_name]["tasks"]
            ):
                self.same_dir[self.folder_name]["tasks"].remove(self.mid)
                self.same_dir[self.folder_name]["total"] -= 1

    async def on_download_start(self):
        if self.bot_pm and self.is_super_chat:
            self.pm_msg = await send_message(
                self.user_id,
                f"""➲ <b><u>Task Started :</u></b>
┃
┖ <b>Link:</b> <a href='{self.source_url}'>Click Here</a>
""",
            )
        if (
            self.is_super_chat
            and Config.INCOMPLETE_TASK_NOTIFIER
            and Config.DATABASE_URL
        ):
            await database.add_incomplete_task(
                self.message.chat.id, self.message.link, self.tag
            )

    async def on_download_complete(self):
        await sleep(2)
        if self.is_cancelled:
            return
        multi_links = False
        if (
            self.folder_name
            and self.same_dir
            and self.mid in self.same_dir[self.folder_name]["tasks"]
        ):
            async with same_directory_lock:
                while True:
                    async with task_dict_lock:
                        if self.mid not in self.same_dir[self.folder_name]["tasks"]:
                            return
                        if (
                            self.same_dir[self.folder_name]["total"] <= 1
                            or len(self.same_dir[self.folder_name]["tasks"]) > 1
                        ):
                            if self.same_dir[self.folder_name]["total"] > 1:
                                self.same_dir[self.folder_name]["tasks"].remove(
                                    self.mid
                                )
                                self.same_dir[self.folder_name]["total"] -= 1
                                spath = f"{self.dir}{self.folder_name}"
                                des_id = list(self.same_dir[self.folder_name]["tasks"])[
                                    0
                                ]
                                des_path = f"{DOWNLOAD_DIR}{des_id}{self.folder_name}"
                                LOGGER.info(f"Moving files from {self.mid} to {des_id}")
                                await move_and_merge(spath, des_path, self.mid)
                                multi_links = True
                            break
                    await sleep(1)
        async with task_dict_lock:
            if self.is_cancelled:
                return
            if self.mid not in task_dict:
                return
            download = task_dict[self.mid]
            self.name = download.name()
            gid = download.gid()
        LOGGER.info(f"Download completed: {self.name}")

        if not (self.is_torrent or self.is_qbit):
            self.seed = False

        if multi_links:
            self.seed = False
            await self.on_upload_error(
                f"{self.name} Downloaded!\n\nWaiting for other tasks to finish..."
            )
            return
        elif self.same_dir:
            self.seed = False

        if self.folder_name:
            self.name = self.folder_name.strip("/").split("/", 1)[0]

        if not await aiopath.exists(f"{self.dir}/{self.name}"):
            try:
                files = await listdir(self.dir)
                self.name = files[-1]
                if self.name == "yt-dlp-thumb":
                    self.name = files[0]
            except Exception as e:
                await self.on_upload_error(str(e))
                return

        dl_path = f"{self.dir}/{self.name}"
        self.size = await get_path_size(dl_path)
        self.is_file = await aiopath.isfile(dl_path)

        if self.seed:
            up_dir = self.up_dir = f"{self.dir}10000"
            up_path = f"{self.up_dir}/{self.name}"
            await create_recursive_symlink(self.dir, self.up_dir)
            LOGGER.info(f"Shortcut created: {dl_path} -> {up_path}")
        else:
            up_dir = self.dir
            up_path = dl_path

        await remove_excluded_files(self.up_dir or self.dir, self.excluded_extensions)

        if not Config.QUEUE_ALL:
            async with queue_dict_lock:
                if self.mid in non_queued_dl:
                    non_queued_dl.remove(self.mid)
            await start_from_queued()

        if self.join and not self.is_file:
            await join_files(up_path)

        if self.extract and not self.is_nzb:
            up_path = await self.proceed_extract(up_path, gid)
            if self.is_cancelled:
                return
            self.is_file = await aiopath.isfile(up_path)
            self.name = up_path.replace(f"{up_dir}/", "").split("/", 1)[0]
            self.size = await get_path_size(up_dir)
            self.clear()
            await remove_excluded_files(up_dir, self.excluded_extensions)

        if self.ffmpeg_cmds:
            up_path = await self.proceed_ffmpeg(
                up_path,
                gid,
            )
            if self.is_cancelled:
                return
            self.is_file = await aiopath.isfile(up_path)
            self.name = up_path.replace(f"{up_dir}/", "").split("/", 1)[0]
            self.size = await get_path_size(up_dir)
            self.clear()

        if self.is_leech and self.is_file:
            fname = ospath.basename(up_path)
            self.file_details["filename"] = fname
            self.file_details["mime_type"] = (guess_type(fname))[
                0
            ] or "application/octet-stream"

        if self.name_swap:
            up_path = await self.substitute(up_path)
            if self.is_cancelled:
                return
            self.is_file = await aiopath.isfile(up_path)
            self.name = up_path.replace(f"{up_dir}/", "").split("/", 1)[0]

        if self.screen_shots:
            up_path = await self.generate_screenshots(up_path)
            if self.is_cancelled:
                return
            self.is_file = await aiopath.isfile(up_path)
            self.name = up_path.replace(f"{up_dir}/", "").split("/", 1)[0]
            self.size = await get_path_size(up_dir)

        if self.convert_audio or self.convert_video:
            up_path = await self.convert_media(
                up_path,
                gid,
            )
            if self.is_cancelled:
                return
            self.is_file = await aiopath.isfile(up_path)
            self.name = up_path.replace(f"{up_dir}/", "").split("/", 1)[0]
            self.size = await get_path_size(up_dir)
            self.clear()

        if self.sample_video:
            up_path = await self.generate_sample_video(up_path, gid)
            if self.is_cancelled:
                return
            self.is_file = await aiopath.isfile(up_path)
            self.name = up_path.replace(f"{up_dir}/", "").split("/", 1)[0]
            self.size = await get_path_size(up_dir)
            self.clear()

        if self.compress:
            up_path = await self.proceed_compress(
                up_path,
                gid,
            )
            self.is_file = await aiopath.isfile(up_path)
            if self.is_cancelled:
                return
            self.clear()

        self.name = up_path.replace(f"{up_dir}/", "").split("/", 1)[0]
        self.size = await get_path_size(up_dir)

        if self.is_leech and not self.compress:
            await self.proceed_split(up_path, gid)
            if self.is_cancelled:
                return
            self.clear()

        self.subproc = None

        add_to_queue, event = await check_running_tasks(self, "up")
        await start_from_queued()
        if add_to_queue:
            LOGGER.info(f"Added to Queue/Upload: {self.name}")
            async with task_dict_lock:
                task_dict[self.mid] = QueueStatus(self, gid, "Up")
            await event.wait()
            if self.is_cancelled:
                return
            LOGGER.info(f"Start from Queued/Upload: {self.name}")

        self.size = await get_path_size(up_dir)

        if self.is_leech:
            LOGGER.info(f"Leech Name: {self.name}")
            tg = TelegramUploader(self, up_dir)
            async with task_dict_lock:
                task_dict[self.mid] = TelegramStatus(self, tg, gid, "up")
            await gather(
                update_status_message(self.message.chat.id),
                tg.upload(),
            )
            del tg
        elif is_gdrive_id(self.up_dest):
            LOGGER.info(f"Gdrive Upload Name: {self.name}")
            drive = GoogleDriveUpload(self, up_path)
            async with task_dict_lock:
                task_dict[self.mid] = GoogleDriveStatus(self, drive, gid, "up")
            await gather(
                update_status_message(self.message.chat.id),
                sync_to_async(drive.upload),
            )
            del drive
        else:
            LOGGER.info(f"Rclone Upload Name: {self.name}")
            RCTransfer = RcloneTransferHelper(self)
            async with task_dict_lock:
                task_dict[self.mid] = RcloneStatus(self, RCTransfer, gid, "up")
            await gather(
                update_status_message(self.message.chat.id),
                RCTransfer.upload(up_path),
            )
            del RCTransfer
        return

    async def on_upload_complete(
        self, link, files, folders, mime_type, rclone_path="", dir_id=""
    ):
        if (
            self.is_super_chat
            and Config.INCOMPLETE_TASK_NOTIFIER
            and Config.DATABASE_URL
        ):
            await database.rm_complete_task(self.message.link)
        
        # Add save message prefix to use in callback data
        save_prefix = f"save_{self.mid}"
        
        msg = (
            f"<b><i>{escape(self.name)}</i></b>\n│"
            f"\n┟ <b>Task Size</b> → {get_readable_file_size(self.size)}"
            f"\n┠ <b>Time Taken</b> → {get_readable_time(time() - self.message.date.timestamp())}"
            f"\n┠ <b>In Mode</b> → {self.mode[0]}"
            f"\n┠ <b>Out Mode</b> → {self.mode[1]}"
        )
        LOGGER.info(f"Task Done: {self.name}")
        if self.is_leech:
            msg += f"\n┠ <b>Total Files</b> → {folders}"
            if mime_type != 0:
                msg += f"\n┠ <b>Corrupted Files</b> → {mime_type}"
            msg += f"\n┖ <b>Task By</b> → {self.tag}\n\n"

            # Always send to PM if it's a leech task
            try:
                # Ensure we have a valid user_id
                user_id = self.user_id
                LOGGER.info(f"Attempting to send leech results to user PM: {user_id}")
                
                # Full message prepared for PM
                full_msg = msg
                full_msg += "〶 <b><u>Files List :</u></b>\n"
                fmsg = ""
                for index, (link, name) in enumerate(files.items(), start=1):
                    chat_id, msg_id = link.split("/")[-2:]
                    # Add direct link to the file in PM message
                    fmsg += f"{index}. <a href='{link}'>{name}</a>"
                    if Config.MEDIA_STORE and (
                        self.is_super_chat or Config.LEECH_DUMP_CHAT
                    ):
                        if chat_id.isdigit():
                            chat_id = f"-100{chat_id}"
                        flink = f"https://t.me/{TgClient.BNAME}?start={encode_slink('file' + chat_id + '&&' + msg_id)}"
                        fmsg += f"\n┖ <b>Get Media</b> → <a href='{flink}'>Store Link</a> | <a href='https://t.me/share/url?url={flink}'>Share Link</a>"
                    fmsg += "\n"
                    
                # Send notification to group
                group_msg = f"<b><i>{escape(self.name)}</i></b>\n│"
                group_msg += f"\n┠ <b>Task Size</b> → {get_readable_file_size(self.size)}"
                group_msg += f"\n┠ <b>Status</b> → Completed and sent to your PM"
                group_msg += f"\n┖ <b>Task By</b> → {self.tag}"
                
                # Send full message with links to PM - Using direct API method
                if fmsg:
                    if len(fmsg.encode() + full_msg.encode()) <= 4000:
                        await send_message(
                            user_id, 
                            full_msg + fmsg
                        )
                        LOGGER.info(f"Successfully sent complete message to user PM: {user_id}")
                    else:
                        # Split into multiple messages if too long
                        await send_message(
                            user_id, 
                            full_msg
                        )
                        
                        chunks = []
                        current_chunk = ""
                        for line in fmsg.splitlines(True):
                            if len(current_chunk.encode() + line.encode()) > 4000:
                                chunks.append(current_chunk)
                                current_chunk = line
                            else:
                                current_chunk += line
                        if current_chunk:
                            chunks.append(current_chunk)
                            
                        for chunk in chunks:
                            await sleep(1)  # Avoid rate limiting
                            await send_message(
                                user_id, 
                                chunk
                            )
                        LOGGER.info(f"Successfully sent chunked messages to user PM: {user_id}")
                else:
                    # No files to list, just send the message
                    await send_message(
                        user_id, 
                        full_msg
                    )
                    LOGGER.info(f"Successfully sent message to user PM: {user_id}")
                
                # Send notification to group
                await send_message(self.message, group_msg)
                
                # Send to MIRROR_LOG_ID chat/channel if configured
                mirror_log_id = Config.MIRROR_LOG_ID
                if mirror_log_id:
                    try:
                        mirror_log_id = int(mirror_log_id)
                        if files and self.is_super_chat:
                            full_log_msg = msg + "\n〶 <b><u>Files List :</u></b>\n" + fmsg
                            if len(full_log_msg.encode()) > 4000:
                                # Split into chunks if message is too long
                                log_chunks = []
                                log_current_chunk = msg + "\n〶 <b><u>Files List :</u></b>\n"
                                for line in fmsg.splitlines(True):
                                    if len(log_current_chunk.encode() + line.encode()) > 4000:
                                        log_chunks.append(log_current_chunk)
                                        log_current_chunk = line
                                    else:
                                        log_current_chunk += line
                                if log_current_chunk:
                                    log_chunks.append(log_current_chunk)
                                    
                                for chunk in log_chunks:
                                    await sleep(1)  # Avoid rate limiting
                                    await send_message(mirror_log_id, chunk)
                            else:
                                await send_message(mirror_log_id, full_log_msg)
                        else:
                            # For simple messages without file lists
                            await send_message(mirror_log_id, full_msg or msg)
                        LOGGER.info(f"Successfully forwarded task completion message to MIRROR_LOG_ID: {mirror_log_id}")
                    except Exception as e:
                        LOGGER.error(f"Failed to send message to MIRROR_LOG_ID: {str(e)}")
            except Exception as e:
                # If sending to PM fails, fall back to sending in group
                LOGGER.error(f"Failed to send message to PM: {str(e)}")
                
                # Create buttons for group message
                save_button = ButtonMaker()
                save_button.callback_button("📥 Save", save_prefix)
                save_markup = save_button.build_menu(1)
                
                if not files and not self.is_super_chat:
                    await send_message(self.message, msg, save_markup)
                else:
                    log_chat = self.message
                    msg += "〶 <b><u>Files List :</u></b>\n"
                    fmsg = ""
                    for index, (link, name) in enumerate(files.items(), start=1):
                        chat_id, msg_id = link.split("/")[-2:]
                        fmsg += f"{index}. <a href='{link}'>{name}</a>"
                        if Config.MEDIA_STORE and (
                            self.is_super_chat or Config.LEECH_DUMP_CHAT
                        ):
                            if chat_id.isdigit():
                                chat_id = f"-100{chat_id}"
                            flink = f"https://t.me/{TgClient.BNAME}?start={encode_slink('file' + chat_id + '&&' + msg_id)}"
                            fmsg += f"\n┖ <b>Get Media</b> → <a href='{flink}'>Store Link</a> | <a href='https://t.me/share/url?url={flink}'>Share Link</a>"
                        fmsg += "\n"
                        if len(fmsg.encode() + msg.encode()) > 4000:
                            await send_message(log_chat, msg + fmsg, save_markup)
                            await sleep(1)
                            fmsg = ""
                    if fmsg != "":
                        await send_message(log_chat, msg + fmsg, save_markup)
        else:
            msg += f"\n│\n┟ <b>Type</b> → {mime_type}"
            if mime_type == "Folder":
                msg += f"\n┠ <b>SubFolders</b> → {folders}"
                msg += f"\n┠ <b>Files</b> → {files}"
            if (
                link
                or (rclone_path and Config.RCLONE_SERVE_URL and not self.private_link)
            ):
                buttons = ButtonMaker()
                if (link and Config.SHOW_CLOUD_LINK):
                    buttons.url_button("☁️ Cloud Link", link)
                else:
                    msg += f"\n\nPath: <code>{rclone_path}</code>"
                if rclone_path and Config.RCLONE_SERVE_URL and not self.private_link:
                    remote, rpath = rclone_path.split(":", 1)
                    url_path = rutils.quote(f"{rpath}")
                    share_url = f"{Config.RCLONE_SERVE_URL}/{url_path}"
                     # Redirect to index page instead of direct download
                    if mime_type == "Folder" or not share_url.endswith("/"):
                        share_url = share_url.rstrip("/")
                    buttons.url_button("🔗 Rclone Link", share_url)
                if not rclone_path and dir_id:
                    INDEX_URL = ""
                    if self.private_link:
                        INDEX_URL = self.user_dict.get("INDEX_URL", "") or ""
                    elif Config.INDEX_URL:
                        INDEX_URL = Config.INDEX_URL
                    if INDEX_URL:
                        share_url = f"{INDEX_URL}findpath?id={dir_id}"
                        buttons.url_button("⚡ Index Link", share_url)
                        if mime_type.startswith(("image", "video", "audio")):
                            share_urls = f"{INDEX_URL}findpath?id={dir_id}&view=true"
                            buttons.url_button("🌐 View Link", share_urls)
                
                # Add Save to Saved Messages button
                buttons.callback_button("📥 Save", save_prefix)
                button = buttons.build_menu(2)
            else:
                msg += f"\n┃\n┠ Path: <code>{rclone_path}</code>"
                
                # Create buttons if none exist
                buttons = ButtonMaker()
                buttons.callback_button("📥 Save", save_prefix)
                button = buttons.build_menu(1)
            
            msg += f"\n┃\n┖ <b>Task By</b> → {self.tag}"
            await send_message(self.message, msg, button)
            
            # Send to MIRROR_LOG_ID chat/channel if configured
            mirror_log_id = Config.MIRROR_LOG_ID
            if mirror_log_id:
                try:
                    mirror_log_id = int(mirror_log_id)
                    await send_message(mirror_log_id, msg, button)
                    LOGGER.info(f"Successfully forwarded non-leech task completion message to MIRROR_LOG_ID: {mirror_log_id}")
                except Exception as e:
                    LOGGER.error(f"Failed to send message to MIRROR_LOG_ID: {str(e)}")
                    
        if self.seed:
            await clean_target(self.up_dir)
            async with queue_dict_lock:
                if self.mid in non_queued_up:
                    non_queued_up.remove(self.mid)
            await start_from_queued()
            return

        if self.pm_msg and (not Config.DELETE_LINKS or Config.CLEAN_LOG_MSG):
            await delete_message(self.pm_msg)

        await clean_download(self.dir)
        async with task_dict_lock:
            if self.mid in task_dict:
                del task_dict[self.mid]
            count = len(task_dict)
        if count == 0:
            await self.clean()
        else:
            await update_status_message(self.message.chat.id)

        async with queue_dict_lock:
            if self.mid in non_queued_up:
                non_queued_up.remove(self.mid)

        await start_from_queued()

    async def on_download_error(self, error, button=None, is_limit=False):
        async with task_dict_lock:
            if self.mid in task_dict:
                del task_dict[self.mid]
            count = len(task_dict)
        await self.remove_from_same_dir()
        msg = (
            f"""〶 <b><i><u>Limit Breached:</u></i></b>
│
┟ <b>Task Size</b> → {get_readable_file_size(self.size)}
┠ <b>In Mode</b> → {self.mode[0]}
┠ <b>Out Mode</b> → {self.mode[1]}
{error}"""
            if is_limit
            else f"""<i><b>〶 Download Stopped!</b></i>
│
┟ <b>Due To</b> → {escape(str(error))}
┠ <b>Task Size</b> → {get_readable_file_size(self.size)}
┠ <b>Time Taken</b> → {get_readable_time(time() - self.message.date.timestamp())}
┠ <b>In Mode</b> → {self.mode[0]}
┠ <b>Out Mode</b> → {self.mode[1]}
┖ <b>Task By</b> → {self.tag}"""
        )

        await send_message(self.message, msg, button)
        if count == 0:
            await self.clean()
        else:
            await update_status_message(self.message.chat.id)

        if (
            self.is_super_chat
            and Config.INCOMPLETE_TASK_NOTIFIER
            and Config.DATABASE_URL
        ):
            await database.rm_complete_task(self.message.link)

        async with queue_dict_lock:
            if self.mid in queued_dl:
                queued_dl[self.mid].set()
                del queued_dl[self.mid]
            if self.mid in queued_up:
                queued_up[self.mid].set()
                del queued_up[self.mid]
            if self.mid in non_queued_dl:
                non_queued_dl.remove(self.mid)
            if self.mid in non_queued_up:
                non_queued_up.remove(self.mid)

        await start_from_queued()
        await sleep(3)
        await clean_download(self.dir)
        if self.up_dir:
            await clean_download(self.up_dir)
        if self.thumb and await aiopath.exists(self.thumb):
            await remove(self.thumb)

    async def on_upload_error(self, error):
        async with task_dict_lock:
            if self.mid in task_dict:
                del task_dict[self.mid]
            count = len(task_dict)
        await send_message(self.message, f"{self.tag} {escape(str(error))}")
        if count == 0:
            await self.clean()
        else:
            await update_status_message(self.message.chat.id)

        if (
            self.is_super_chat
            and Config.INCOMPLETE_TASK_NOTIFIER
            and Config.DATABASE_URL
        ):
            await database.rm_complete_task(self.message.link)

        async with queue_dict_lock:
            if self.mid in queued_dl:
                queued_dl[self.mid].set()
                del queued_dl[self.mid]
            if self.mid in queued_up:
                queued_up[self.mid].set()
                del queued_up[self.mid]
            if self.mid in non_queued_dl:
                non_queued_dl.remove(self.mid)
            if self.mid in non_queued_up:
                non_queued_up.remove(self.mid)

        await start_from_queued()
        await sleep(3)
        await clean_download(self.dir)
        if self.up_dir:
            await clean_download(self.up_dir)
        if self.thumb and await aiopath.exists(self.thumb):
            await remove(self.thumb)