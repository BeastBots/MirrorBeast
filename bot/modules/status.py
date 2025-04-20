from psutil import cpu_percent, virtual_memory, disk_usage
from time import time
from asyncio import gather, iscoroutinefunction
from random import choice, random

from pyrogram.errors import QueryIdInvalid

from .. import (
    task_dict_lock,
    status_dict,
    task_dict,
    bot_start_time,
    intervals,
    sabnzbd_client,
    DOWNLOAD_DIR,
    OWNER_ID,
)
from ..core.torrent_manager import TorrentManager
from ..core.jdownloader_booter import jdownloader
from ..helper.ext_utils.bot_utils import new_task
from ..helper.ext_utils.status_utils import (
    EngineStatus,
    MirrorStatus,
    get_readable_file_size,
    get_readable_time,
    speed_string_to_bytes,
)
from ..helper.telegram_helper.bot_commands import BotCommands
from ..helper.telegram_helper.message_utils import (
    send_message,
    delete_message,
    auto_delete_message,
    send_status_message,
    update_status_message,
    edit_message,
)
from ..helper.telegram_helper.button_build import ButtonMaker


# Fun Easter egg messages for owner
owner_responses = [
    "🧠 <q><b><i>Mission Control is idle, sir. Ready for your next command.</i></b></q>",
    "🦁 <q><b><i>The Beast is resting. What shall we hunt next?</i></b></q>",
    "💤 <q><b><i>System dormant. Your digital kingdom awaits orders.</i></b></q>",
    "🔍 <q><b><i>Scanning complete! No active tasks detected. What's the next mission?</i></b></q>",
    "🛌 <q><b><i>All systems cleared. Beast is taking a power nap.</i></b></q>",
    "🦾 <q><b><i>Battle stations clear, commander. The Beast stands ready.</i></b></q>",
    "🧙‍♂️ <q><b><i>The digital realm is quiet. What magic shall we work next?</i></b></q>",
    "🌟 <q><b><i>Mirror Beast awaits your brilliance! No current operations.</i></b></q>",
    "🎮 <q><b><i>Game over for now. Press START to begin a new mission!</i></b></q>",
    "🏆 <q><b><i>Achievement unlocked: Clear Task Queue! What's next on your agenda?</i></b></q>",
    "✨ <q><b><i>Dear Master, there are no tasks currently running.</i></b></q>",
    "🙏 <q><b><i>My deepest respects, but nothing is in progress right now.</i></b></q>",
    "💎 <q><b><i>Everything's clear at the moment, Boss.</i></b></q>",
    "🫡 <q><b><i>No active tasks, Sir. Standing by.</i></b></q>",
    "👑 <q><b><i>Nothing in queue, My Liege.</i></b></q>",
    "🎩 <q><b><i>At your service, Master. The task list is empty.</i></b></q>",
    "⚙️ <q><b><i>No active processes, as you command.</i></b></q>",
    "🖥️ <q><b><i>The system is idle and awaiting your orders.</i></b></q>",
    "📊 <q><b><i>All clear, Captain. No current operations.</i></b></q>",
    "📭 <q><b><i>The taskbox is empty, Boss.</i></b></q>"
]

# Fun Easter egg messages for regular users
easter_eggs = [
    "🐾 <q><b><i>The Beast is currently hibernating. No active tasks.</i></b></q>",
    "🧩 <q><b><i>All systems operational, waiting for your next puzzle.</i></b></q>",
    "🔮 <q><b><i>The crystal ball shows... no active downloads!</i></b></q>",
    "🎯 <q><b><i>Target acquired: Nothing! No downloads in progress.</i></b></q>",
    "🛸 <q><b><i>The mothership reports all tasks complete.</i></b></q>",
    "🤖 <q><b><i>Beep boop! No tasks found in my circuits.</i></b></q>",
    "🌈 <q><b><i>Clear skies ahead! No downloads in progress.</i></b></q>",
    "🖥️ <q><b><i>The system is idle and awaiting your orders.</i></b></q>",
    "📊 <q><b><i>All clear, Captain. No current operations.</i></b></q>",
    "📭 <q><b><i>The taskbox is empty, Boss.</i></b></q>",
    "💀 <q><b><i>Stop it, Get Some Help!</i></b></q>",
    "☠️ <q><b><i>Bro… there's nothing here.</i></b></q>",
    "🧠 <q><b><i>Empty. Just like your head.</i></b></q>",
    "👻 <q><b><i>Ghost town, pal. No tasks here.</i></b></q>",
    "🎈 <q><b><i>All air, no substance. Zero tasks.</i></b></q>",
    "📭 <q><b><i>The taskbox is emptier than your DMs.</i></b></q>",
    "🥶 <q><b><i>Cold, dead silence. No action here.</i></b></q>",
    "🕳️ <q><b><i>A black hole of nothingness.</i></b></q>",
    "🫥 <q><b><i>Disappeared… like your crush did.</i></b></q>",
    "🪦 <q><b><i>Buried in inactivity. Nothing running.</i></b></q>",
    "😴 <q><b><i>Asleep on the job? Nope — nothing started.</i></b></q>",
    "🧍 <q><b><i>Standing still. Nothing's moving.</i></b></q>",
    "🕸️ <q><b><i>Covered in cobwebs. No tasks alive.</i></b></q>",
    "🔍 <q><b><i>Searched everywhere — found nothing.</i></b></q>",
    "🫠 <q><b><i>Nothing but silence…</i></b></q>",
    "🐍 <q><b><i>No scripts hissing here.</i></b></q>",
    "📉 <q><b><i>Task levels: Rock bottom.</i></b></q>",
    "🎭 <q><b><i>An empty stage. No acts playing.</i></b></q>",
    "🎮 <q><b><i>No game. No players. Just you.</i></b></q>",
    "🚪 <q><b><i>Closed shop. Nothing's running.</i></b></q>",
    "📺 <q><b><i>No broadcast found.</i></b></q>",
    "📝 <q><b><i>Blank slate. Zero tasks.</i></b></q>",
    "🦴 <q><b><i>Bone dry.</i></b></q>",
    "💨 <q><b><i>Gone with the wind. No processes.</i></b></q>",
    "🛸 <q><b><i>Abducted by aliens, maybe?</i></b></q>",
    "🕯️ <q><b><i>Lit a candle… still no tasks.</i></b></q>",
    "🦗 <q><b><i>Crickets…</i></b></q>",
    "🚫 <q><b><i>No entries, no fun.</i></b></q>",
    "🖥️ <q><b><i>System idle. Nada.</i></b></q>",
    "🌑 <q><b><i>Dark and empty.</i></b></q>",
    "🥲 <q><b><i>This hurts. No tasks yet.</i></b></q>",
    "📡 <q><b><i>Signal lost. No task detected.</i></b></q>",
    "🎶 <q><b><i>No song playing.</i></b></q>",
    "📂 <q><b><i>Folder's empty too.</i></b></q>",
    "🥀 <q><b><i>Withered away. No work here.</i></b></q>",
    "🌫️ <q><b><i>Lost in the mist of nothingness.</i></b></q>",
    "🛌 <q><b><i>Taking a nap. No activity.</i></b></q>",
    "🚷 <q><b><i>Nothing allowed. No tasks here.</i></b></q>",
    "🥸 <q><b><i>You pretending there's a task?</i></b></q>",
    "🎲 <q><b><i>Rolled a zero.</i></b></q>",
    "🗿 <q><b><i>Stone-cold nothing.</i></b></q>",
    "🧤 <q><b><i>Handled… except there's nothing to handle.</i></b></q>",
    "📢 <q><b><i>Loud silence detected.</i></b></q>",
    "🔕 <q><b><i>No notifications. No jobs.</i></b></q>",
    "🥁 <q><b><i>Drumroll… for nothing.</i></b></q>",
    "🪑 <q><b><i>Empty chair vibes.</i></b></q>",
    "📸 <q><b><i>Snapshot of… absolutely nothing.</i></b></q>",
    "🐚 <q><b><i>Echoes of nothing.</i></b></q>",
    "🌪️ <q><b><i>A whirlwind of inactivity.</i></b></q>"
]


@new_task
async def task_status(_, message):
    async with task_dict_lock:
        count = len(task_dict)

    if count == 0:
        currentTime = get_readable_time(time() - bot_start_time)
        free = get_readable_file_size(disk_usage(DOWNLOAD_DIR).free)
        free_percent = round(100 - disk_usage(DOWNLOAD_DIR).percent, 1)
        
        # Check if owner or normal user using imported OWNER_ID
        if message.from_user.id == OWNER_ID:
            response = choice(owner_responses)
        else:
            response = choice(easter_eggs)
            
        # Add a small chance (10%) for an ultra-rare Easter egg for everyone
        if random() < 0.1:
            response = "✨👑 <q><b>Time itself paused... The UNSEEN RESPONSE has revealed itself to YOU — a moment rarer than stardust in a black hole.</b></q>"

        msg = f"""{response}

⌬ <b><u>Bot Stats</u></b>
╭ <b>CPU</b> → {cpu_percent()}%
├ <b>RAM</b> → {virtual_memory().percent}%
├ <b>Free</b> → {free} [{free_percent}%]
╰ <b>UP</b> → {currentTime}
"""
        reply_message = await send_message(message, msg)
        await auto_delete_message(message, reply_message)
    else:
        text = message.text.split()
        if len(text) > 1:
            user_id = message.from_user.id if text[1] == "me" else int(text[1])
        else:
            user_id = 0
            sid = message.chat.id
            if obj := intervals["status"].get(sid):
                obj.cancel()
                del intervals["status"][sid]
        await send_status_message(message, user_id)
        await delete_message(message)


async def get_download_status(download):
    eng = download.engine
    speed = (
        download.speed()
        if eng.startswith(("Pyro", "yt-dlp", "RClone", "Google-API"))
        else 0
    )
    return (
        (
            await download.status()
            if iscoroutinefunction(download.status)
            else download.status()
        ),
        speed,
        eng,
    )


@new_task
async def status_pages(_, query):
    data = query.data.split()
    key = int(data[1])
    if data[2] == "ref":
        await update_status_message(key, force=True)
    elif data[2] in ["nex", "pre"]:
        async with task_dict_lock:
            if key in status_dict:
                if data[2] == "nex":
                    status_dict[key]["page_no"] += status_dict[key]["page_step"]
                else:
                    status_dict[key]["page_no"] -= status_dict[key]["page_step"]
    elif data[2] == "ps":
        async with task_dict_lock:
            if key in status_dict:
                status_dict[key]["page_step"] = int(data[3])
    elif data[2] == "st":
        async with task_dict_lock:
            if key in status_dict:
                status_dict[key]["status"] = data[3]
        await update_status_message(key, force=True)
    elif data[2] == "ov":
        message = query.message
        tasks = {
            "Download": 0,
            "Upload": 0,
            "Seed": 0,
            "Archive": 0,
            "Extract": 0,
            "Split": 0,
            "QueueDl": 0,
            "QueueUp": 0,
            "Clone": 0,
            "CheckUp": 0,
            "Pause": 0,
            "SamVid": 0,
            "ConvertMedia": 0,
            "FFmpeg": 0,
        }
        dl_speed = 0
        up_speed = 0
        seed_speed = 0

        async with task_dict_lock:
            status_results = await gather(
                *(get_download_status(download) for download in task_dict.values())
            )

        eng_status = EngineStatus()
        if any(
            eng in (eng_status.STATUS_ARIA2, eng_status.STATUS_QBIT)
            for _, __, eng in status_results
        ):
            dl_speed, seed_speed = await TorrentManager.overall_speed()

        if any(eng == eng_status.STATUS_SABNZBD for _, __, eng in status_results):
            if sabnzbd_client.LOGGED_IN:
                dl_speed += (
                    int(
                        float(
                            (await sabnzbd_client.get_downloads())["queue"].get(
                                "kbpersec", "0"
                            )
                        )
                    )
                    * 1024
                )

        if any(eng == eng_status.STATUS_JD for _, __, eng in status_results):
            if jdownloader.is_connected:
                dl_speed += (
                    await jdownloader.device.downloadcontroller.get_speed_in_bytes()
                )

        for status, speed, _ in status_results:
            match status:
                case MirrorStatus.STATUS_DOWNLOAD:
                    tasks["Download"] += 1
                    if speed:
                        dl_speed += speed_string_to_bytes(speed)
                case MirrorStatus.STATUS_UPLOAD:
                    tasks["Upload"] += 1
                    up_speed += speed_string_to_bytes(speed)
                case MirrorStatus.STATUS_SEED:
                    tasks["Seed"] += 1
                case MirrorStatus.STATUS_ARCHIVE:
                    tasks["Archive"] += 1
                case MirrorStatus.STATUS_EXTRACT:
                    tasks["Extract"] += 1
                case MirrorStatus.STATUS_SPLIT:
                    tasks["Split"] += 1
                case MirrorStatus.STATUS_QUEUEDL:
                    tasks["QueueDl"] += 1
                case MirrorStatus.STATUS_QUEUEUP:
                    tasks["QueueUp"] += 1
                case MirrorStatus.STATUS_CLONE:
                    tasks["Clone"] += 1
                case MirrorStatus.STATUS_CHECK:
                    tasks["CheckUp"] += 1
                case MirrorStatus.STATUS_PAUSED:
                    tasks["Pause"] += 1
                case MirrorStatus.STATUS_SAMVID:
                    tasks["SamVid"] += 1
                case MirrorStatus.STATUS_CONVERT:
                    tasks["ConvertMedia"] += 1
                case MirrorStatus.STATUS_FFMPEG:
                    tasks["FFmpeg"] += 1
                case _:
                    tasks["Download"] += 1

        msg = f"""㊂ <b>Tasks Overview</b> :

╭ <b>Download:</b> {tasks["Download"]} | <b>Upload:</b> {tasks["Upload"]}
├ <b>Seed:</b> {tasks["Seed"]} | <b>Archive:</b> {tasks["Archive"]}
├ <b>Extract:</b> {tasks["Extract"]} | <b>Split:</b> {tasks["Split"]}
├ <b>QueueDL:</b> {tasks["QueueDl"]} | <b>QueueUP:</b> {tasks["QueueUp"]}
├ <b>Clone:</b> {tasks["Clone"]} | <b>CheckUp:</b> {tasks["CheckUp"]}
├ <b>Paused:</b> {tasks["Pause"]} | <b>SamVideo:</b> {tasks["SamVid"]}
╰ <b>Convert:</b> {tasks["ConvertMedia"]} | <b>FFmpeg:</b> {tasks["FFmpeg"]}

╭ <b>Total Download Speed:</b> {get_readable_file_size(dl_speed)}/s
├ <b>Total Upload Speed:</b> {get_readable_file_size(up_speed)}/s
╰ <b>Total Seeding Speed:</b> {get_readable_file_size(seed_speed)}/s
"""
        button = ButtonMaker()
        button.data_button("Back", f"status {data[1]} ref")
        await edit_message(message, msg, button.build_menu())

    try:
        await query.answer()
    except QueryIdInvalid:
        pass
