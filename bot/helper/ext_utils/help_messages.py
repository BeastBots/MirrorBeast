from ..telegram_helper.bot_commands import BotCommands

# Define constants for repeated strings
NOTE = "<b>NOTE:</b>"
CMD = "/cmd"

# Helper function to format commands
def format_command(description, *examples):
    return f"<b>{description}</b>:\n" + "\n".join(examples)

# Mirror Help Messages
mirror = f"""<b>Send link along with command line or </b>\n\n{CMD} link\n\n<b>By replying to link/file</b>:\n\n{CMD} -n new name -e -up upload destination\n\n{NOTE}:\n1. Commands that start with <b>qb</b> are ONLY for torrents."""

# YouTube Help Messages
yt = f"""<b>Send link along with command line</b>:\n\n{CMD} link\n<b>By replying to link</b>:\n{CMD} -n new name -z password -opt x:y|x1:y1\n\nCheck here all supported <a href='https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md'>SITES</a>\nCheck all yt-dlp api options from this <a href='https://github.com/yt-dlp/yt-dlp/blob/master/yt_dlp/YoutubeDL.py#L212'>FILE</a> or use this <a href='https://t.me/mltb_official_channel/177'>script</a> to convert cli arguments to api options."""

# Clone Help Messages
clone = f"""Send Gdrive|Gdot|Filepress|Filebee|Appdrive|Gdflix link or rclone path along with command or by replying to the link/rc_path by command.\nUse -sync to use sync method in rclone. Example: {CMD} rcl/rclone_path -up rcl/rclone_path/rc -sync"""

# Reintroduce missing variables from the original file
new_name = """<b>New Name</b>: -n\n\n/cmd link -n new name\nNote: Doesn't work with torrents"""
extract_zip = """<b>Extract/Zip</b>: -e -z\n\n/cmd link -e password (extract password protected)\n/cmd link -z password (zip password protected)\n/cmd link -z password -e (extract and zip password protected)\nNote: When both extract and zip added with cmd it will extract first and then zip, so always extract first"""
seed = """<b>Bittorrent seed</b>: -d\n\n/cmd link -d ratio:seed_time or by replying to file/link\nTo specify ratio and seed time add -d ratio:time.\nExample: -d 0.7:10 (ratio and time) or -d 0.7 (only ratio) or -d :10 (only time) where time in minutes"""
multi_link = """<b>Multi links only by replying to first link/file</b>: -i\n\n/cmd -i 10(number of links/files)"""
same_dir = """<b>Move file(s)/folder(s) to new folder</b>: -m\n\nYou can use this arg also to move multiple links/torrents contents to the same directory, so all links will be uploaded together as one task\n\n/cmd link -m new folder (only one link inside new folder)\n/cmd -i 10(number of links/files) -m folder name (all links contents in one folder)\n/cmd -b -m folder name (reply to batch of message/file(each link on new line))"""
thumb = """<b>Thumbnail for current task</b>: -t\n\n/cmd link -t tg-message-link (doc or photo) or none (file without thumb)"""
split_size = """<b>Split size for current task</b>: -sp\n\n/cmd link -sp (500mb or 2gb or 4000000000)\nNote: Only mb and gb are supported or write in bytes without unit!"""
upload = """<b>Upload Destination</b>: -up\n\n/cmd link -up rcl/gdl (rcl: to select rclone config, remote & path | gdl: To select token.pickle, gdrive id) using buttons"""
rcf = """<b>Rclone Flags</b>: -rcf\n\n/cmd link|path|rcl -up path|rcl -rcf --buffer-size:8M|--drive-starred-only|key|key:value\nThis will override all other flags except --exclude\nCheck here all <a href='https://rclone.org/flags/'>RcloneFlags</a>."""
bulk = """<b>Bulk Download</b>: -b\n\nBulk can be used only by replying to text message or text file contains links separated by new line."""
join = """<b>Join Splitted Files</b>: -j\n\nThis option will only work before extract and zip, so mostly it will be used with -m argument (samedir)\nBy Reply:\n/cmd -i 3 -j -m folder name\n/cmd -b -j -m folder name\nif u have link(folder) have splitted files:\n/cmd link -j"""
rlone_dl = """<b>Rclone Download</b>:\n\nTreat rclone paths exactly like links\n/cmd main:dump/ubuntu.iso or rcl(To select config, remote and path)\nUsers can add their own rclone from user settings"""
tg_links = """<b>TG Links</b>:\n\nTreat links like any direct link\nSome links need user access so you must add USER_SESSION_STRING for it."""
sample_video = """<b>Sample Video</b>: -sv\n\nCreate sample video for one video or folder of videos."""
screenshot = """<b>ScreenShots</b>: -ss\n\nCreate screenshots for one video or folder of videos."""
convert_media = """<b>Convert Media</b>: -ca -cv\n\n/cmd link -ca mp3 -cv mp4 (convert all audios to mp3 and all videos to mp4)"""
force_start = """<b>Force Start</b>: -f -fd -fu\n\n/cmd link -f (force download and upload)"""
user_download = """<b>User Download</b>: link\n\n/cmd tp:link to download using owner token.pickle incase service account enabled."""
name_swap = """<b>Name Substitution</b>: -ns\n\n/cmd link -ns script/code/s | mirror/leech"""
transmission = """<b>Tg transmission</b>: -hl -ut -bt\n\n/cmd link -hl (leech by user and bot session with respect to size) (Hybrid Leech)"""
thumbnail_layout = """Thumbnail Layout: -tl\n\n/cmd link -tl 3x3 (widthxheight) 3 photos in row and 3 photos in column"""
leech_as = """<b>Leech as</b>: -doc -med\n\n/cmd link -doc (Leech as document)"""
ffmpeg_cmds = """<b>FFmpeg Commands</b>: -ff\n\nlist of lists of ffmpeg commands. You can set multiple ffmpeg commands for all files before upload.\n\nNotes:\n1. Add <code>-del</code> to the list(s) which you want from the bot to delete the original files after command run complete!\n2. FFmpeg Variables in the last cmd such as metadata ({title}, {title2}, etc...) can be edited in user settings (usetting).\n3. To execute one of pre-added lists in bot like: (\"subtitle\": [\"-i mltb.mkv -c copy -c:s srt mltb.mkv\"]), you must use -ff subtitle (list key).\n4. You can add Telegram link for small size inputs like photo to set watermark.\n\nExamples:\n[\"-i mltb.mkv -c copy -c:s srt mltb.mkv\", \"-i mltb.video -c copy -c:s srt mltb\", \"-i mltb.m4a -c:a libmp3lame -q:a 2 mltb.mp3\", \"-i mltb.audio -c:a libmp3lame -q:a 2 mltb.mp3\", \"-i mltb -map 0:a -c copy mltb.mka -map 0:s -c copy mltb.srt\"], \"metadata\": [\"-i mltb.mkv -map 0 -map -0:v:1 -map -0:s -map 0:s:0 -map -0:v:m:attachment -c copy -metadata:s:v:0 title={title} -metadata:s:a:0 title={title} -metadata:s:a:1 title={title2} -metadata:s:a:2 title={title2} -c:s srt -metadata:s:s:0 title={title3} mltb -y -del\", \"-i mltb -i tg://openmessage?user_id=5272663208&message_id=322801 -filter_complex 'overlay=W-w-10:H-h-10' -c:a copy mltb\", \"watermark\": [\"-i mltb -i tg://openmessage?user_id=5272663208&message_id=322801 -filter_complex 'overlay=W-w-10:H-h-10' -c:a copy mltb\"]}"""

# Reintroduce the missing variables
gdrive = """<b>Gdrive</b>: link\nIf DEFAULT_UPLOAD is `rc` then you can pass up: `gd` to upload using gdrive tools to GDRIVE_ID.\n/cmd gdriveLink or gdl or gdriveId -up gdl or gdriveId or gd"""
rclone_cl = """<b>Rclone</b>: path\nIf DEFAULT_UPLOAD is `gd` then you can pass up: `rc` to upload to RCLONE_PATH.\n/cmd rcl/rclone_path -up rcl/rclone_path/rc -rcf flagkey:flagvalue|flagkey|flagkey:flagvalue"""

# Define dictionaries for help messages
YT_HELP_DICT = {
    "main": yt,
    "New-Name": f"<b>New Name</b>: -n\n\n{CMD} link -n new name\nNote: Doesn't work with torrents",
    "Zip": "<b>Zip</b>: -z password\n\n{CMD} link -z (zip)\n{CMD} link -z password (zip password protected)",
    "Quality": "<b>Quality Buttons</b>: -s\n\nIn case default quality added from yt-dlp options using format option and you need to select quality for specific link or links with multi links feature.\n{CMD} link -s",
    "Options": "<b>Options</b>: -opt\n\n{CMD} link -opt {\"format\": \"bv*+mergeall[vcodec=none]\", \"nocheckcertificate\": True, \"playliststart\": 10, \"fragment_retries\": float(\"inf\"), \"matchtitle\": \"S13\", \"writesubtitles\": True, \"live_from_start\": True, \"postprocessor_args\": {\"ffmpeg\": [\"-threads\", \"4\"]}, \"wait_for_video\": (5, 100), \"download_ranges\": [{\"start_time\": 0, \"end_time\": 10}]}",
    "Multi-Link": "<b>Multi links only by replying to first link/file</b>: -i\n\n{CMD} -i 10(number of links/files)",
    "Same-Directory": "<b>Move file(s)/folder(s) to new folder</b>: -m\n\nYou can use this arg also to move multiple links/torrents contents to the same directory, so all links will be uploaded together as one task\n\n{CMD} link -m new folder (only one link inside new folder)\n{CMD} -i 10(number of links/files) -m folder name (all links contents in one folder)\n{CMD} -b -m folder name (reply to batch of message/file(each link on new line))",
    "Thumb": "<b>Thumbnail for current task</b>: -t\n\n{CMD} link -t tg-message-link (doc or photo) or none (file without thumb)",
    "Split-Size": "<b>Split size for current task</b>: -sp\n\n{CMD} link -sp (500mb or 2gb or 4000000000)\nNote: Only mb and gb are supported or write in bytes without unit!",
    "Upload-Destination": "<b>Upload Destination</b>: -up\n\n{CMD} link -up rcl/gdl (rcl: to select rclone config, remote & path | gdl: To select token.pickle, gdrive id) using buttons",
    "Rclone-Flags": "<b>Rclone Flags</b>: -rcf\n\n{CMD} link|path|rcl -up path|rcl -rcf --buffer-size:8M|--drive-starred-only|key|key:value\nThis will override all other flags except --exclude\nCheck here all <a href='https://rclone.org/flags/'>RcloneFlags</a>.",
    "Bulk": "<b>Bulk Download</b>: -b\n\nBulk can be used only by replying to text message or text file contains links separated by new line.",
    "Sample-Video": "<b>Sample Video</b>: -sv\n\nCreate sample video for one video or folder of videos.",
    "Screenshot": "<b>ScreenShots</b>: -ss\n\nCreate screenshots for one video or folder of videos.",
    "Convert-Media": "<b>Convert Media</b>: -ca -cv\n\n{CMD} link -ca mp3 -cv mp4 (convert all audios to mp3 and all videos to mp4)",
    "Force-Start": "<b>Force Start</b>: -f -fd -fu\n\n{CMD} link -f (force download and upload)",
    "Name-Swap": "<b>Name Substitution</b>: -ns\n\n{CMD} link -ns script/code/s | mirror/leech",
    "TG-Transmission": "<b>Tg transmission</b>: -hl -ut -bt\n\n{CMD} link -hl (leech by user and bot session with respect to size) (Hybrid Leech)",
    "Thumb-Layout": "Thumbnail Layout: -tl\n\n{CMD} link -tl 3x3 (widthxheight) 3 photos in row and 3 photos in column",
    "Leech-Type": "<b>Leech as</b>: -doc -med\n\n{CMD} link -doc (Leech as document)",
    "FFmpeg-Cmds": "<b>FFmpeg Commands</b>: -ff\n\nlist of lists of ffmpeg commands. You can set multiple ffmpeg commands for all files before upload."
}

MIRROR_HELP_DICT = {
    "main": mirror,
    "New-Name": new_name,
    "DL-Auth": "<b>Direct link authorization</b>: -au -ap\n\n/cmd link -au username -ap password",
    "Headers": "<b>Direct link custom headers</b>: -h\n\n/cmd link -h key: value key1: value1",
    "Extract/Zip": extract_zip,
    "Select-Files": "<b>Bittorrent/JDownloader/Sabnzbd File Selection</b>: -s\n\n/cmd link -s or by replying to file/link",
    "Torrent-Seed": seed,
    "Multi-Link": multi_link,
    "Same-Directory": same_dir,
    "Thumb": thumb,
    "Split-Size": split_size,
    "Upload-Destination": upload,
    "Rclone-Flags": rcf,
    "Bulk": bulk,
    "Join": join,
    "Rclone-DL": rlone_dl,
    "Tg-Links": tg_links,
    "Sample-Video": sample_video,
    "Screenshot": screenshot,
    "Convert-Media": convert_media,
    "Force-Start": force_start,
    "User-Download": user_download,
    "Name-Swap": name_swap,
    "TG-Transmission": transmission,
    "Thumb-Layout": thumbnail_layout,
    "Leech-Type": leech_as,
    "FFmpeg-Cmds": ffmpeg_cmds,
}

CLONE_HELP_DICT = {
    "main": clone,
    "Multi-Link": multi_link,
    "Bulk": bulk,
    "Gdrive": gdrive,
    "Rclone": rclone_cl,
}

RSS_HELP_MESSAGE = """
Use this format to add feed url:
Title1 link (required)
Title2 link -c cmd -inf xx -exf xx
Title3 link -c cmd -d ratio:time -z password

-c command -up mrcc:remote:path/subdir -rcf --buffer-size:8M|key|key:value
-inf For included words filter.
-exf For excluded words filter.
-stv true or false (sensitive filter)

Example: Title https://www.rss-url.com -inf 1080 or 720 or 144p|mkv or mp4|hevc -exf flv or web|xxx
This filter will parse links that its titles contain `(1080 or 720 or 144p) and (mkv or mp4) and hevc` and doesn't contain (flv or web) and xxx words. You can add whatever you want.

Another example: -inf  1080  or 720p|.web. or .webrip.|hvec or x264. This will parse titles that contain ( 1080  or 720p) and (.web. or .webrip.) and (hvec or x264). I have added space before and after 1080 to avoid wrong matching. If this `10805695` number in title it will match 1080 if added 1080 without spaces after it.

Filter Notes:
1. | means and.
2. Add `or` between similar keys, you can add it between qualities or between extensions, so don't add filter like this f: 1080|mp4 or 720|web because this will parse 1080 and (mp4 or 720) and web ... not (1080 and mp4) or (720 and web).
3. You can add `or` and `|` as much as you want.
4. Take a look at the title if it has a static special character after or before the qualities or extensions or whatever and use them in the filter to avoid wrong match.
Timeout: 60 sec.
"""

PASSWORD_ERROR_MESSAGE = """
<b>This link requires a password!</b>
- Insert <b>::</b> after the link and write the password after the sign.

<b>Example:</b> link::my password
"""


help_string = f"""
NOTE: Try each command without any argument to see more detalis.
/{BotCommands.MirrorCommand[0]} or /{BotCommands.MirrorCommand[1]}: Start mirroring to cloud.
/{BotCommands.QbMirrorCommand[0]} or /{BotCommands.QbMirrorCommand[1]}: Start Mirroring to cloud using qBittorrent.
/{BotCommands.JdMirrorCommand[0]} or /{BotCommands.JdMirrorCommand[1]}: Start Mirroring to cloud using JDownloader.
/{BotCommands.NzbMirrorCommand[0]} or /{BotCommands.NzbMirrorCommand[1]}: Start Mirroring to cloud using Sabnzbd.
/{BotCommands.YtdlCommand[0]} or /{BotCommands.YtdlCommand[1]}: Mirror yt-dlp supported link.
/{BotCommands.LeechCommand[0]} or /{BotCommands.LeechCommand[1]}: Start leeching to Telegram.
/{BotCommands.QbLeechCommand[0]} or /{BotCommands.QbLeechCommand[1]}: Start leeching using qBittorrent.
/{BotCommands.JdLeechCommand[0]} or /{BotCommands.JdLeechCommand[1]}: Start leeching using JDownloader.
/{BotCommands.NzbLeechCommand[0]} or /{BotCommands.NzbLeechCommand[1]}: Start leeching using Sabnzbd.
/{BotCommands.YtdlLeechCommand[0]} or /{BotCommands.YtdlLeechCommand[1]}: Leech yt-dlp supported link.
/{BotCommands.CloneCommand} [drive_url]: Copy file/folder to Google Drive.
/{BotCommands.CountCommand} [drive_url]: Count file/folder of Google Drive.
/{BotCommands.DeleteCommand} [drive_url]: Delete file/folder from Google Drive (Only Owner & Sudo).
/{BotCommands.UserSetCommand[0]} or /{BotCommands.UserSetCommand[1]} [query]: Users settings.
/{BotCommands.BotSetCommand[0]} or /{BotCommands.BotSetCommand[1]} [query]: Bot settings.
/{BotCommands.SelectCommand}: Select files from torrents or nzb by gid or reply.
/{BotCommands.CancelTaskCommand[0]} or /{BotCommands.CancelTaskCommand[1]} [gid]: Cancel task by gid or reply.
/{BotCommands.ForceStartCommand[0]} or /{BotCommands.ForceStartCommand[1]} [gid]: Force start task by gid or reply.
/{BotCommands.CancelAllCommand} [query]: Cancel all [status] tasks.
/{BotCommands.ListCommand} [query]: Search in Google Drive(s).
/{BotCommands.SearchCommand} [query]: Search for torrents with API.
/{BotCommands.MediaInfoCommand[0]} or /{BotCommands.MediaInfoCommand[1]} [query]: Get media info.
/{BotCommands.StatusCommand}: Shows a status of all the downloads.
/{BotCommands.StatsCommand}: Show stats of the machine where the bot is hosted in.
/{BotCommands.PingCommand}: Check how long it takes to Ping the Bot (Only Owner & Sudo).
/{BotCommands.AuthorizeCommand}: Authorize a chat or a user to use the bot (Only Owner & Sudo).
/{BotCommands.UnAuthorizeCommand}: Unauthorize a chat or a user to use the bot (Only Owner & Sudo).
/{BotCommands.UsersCommand}: show users settings (Only Owner & Sudo).
/{BotCommands.AddSudoCommand}: Add sudo user (Only Owner).
/{BotCommands.RmSudoCommand}: Remove sudo users (Only Owner).
/{BotCommands.RestartCommand}: Restart and update the bot (Only Owner & Sudo).
/{BotCommands.LogCommand}: Get a log file of the bot. Handy for getting crash reports (Only Owner & Sudo).
/{BotCommands.ShellCommand}: Run shell commands (Only Owner).
/{BotCommands.AExecCommand}: Exec async functions (Only Owner).
/{BotCommands.ExecCommand}: Exec sync functions (Only Owner).
/{BotCommands.ClearLocalsCommand}: Clear {BotCommands.AExecCommand} or {BotCommands.ExecCommand} locals (Only Owner).
/{BotCommands.RssCommand}: RSS Menu.
"""

BOT_COMMANDS = {
    "Mirror": "[link/file] Mirror to Upload Destination",
    "QbMirror": "[magnet/torrent] Mirror to Upload Destination using qBit",
    "Ytdl": "[link] Mirror YouTube, m3u8, Social Media and yt-dlp supported urls",
    "Leech": "[link/file] Leech files to Upload to Telegram",
    "QbLeech": "[magnet/torrent] Leech files to Upload to Telegram using qBit",
    "YtdlLeech": "[link] Leech YouTube, m3u8, Social Media and yt-dlp supported urls",
    "Clone": "[link] Clone files/folders to GDrive",
    "UserSet": "User personal settings",
    "ForceStart": "[gid/reply] Force start from queued task",
    "Count": "[link] Count no. of files/folders in GDrive",
    "List": "[query] Search any Text which is available in GDrive",
    "Search": "[query] Search torrents via Qbit Plugins",
    "MediaInfo": "[reply/link] Get MediaInfo of the Target Media",
    "SpeedTest": "Check Bot Speed using Speedtest.com",
    "Select": "[gid/reply] Select files for NZB, Aria2, Qbit Tasks",
    "Ping": "Ping Bot to test Response Speed",
    "Status": "[id/me] Tasks Status of Bot",
    "Stats": "Bot, OS, Repo & System full Statistics",
    "Rss": "User RSS Management Settings",
    "IMDB": "[query] or ttxxxxxx Get IMDB info",
    "CancelAll": "Cancel all Tasks on the Bot",
    "Help": "Detailed help usage of the WZ Bot",
    "BotSet": "[SUDO] Bot Management Settings",
    "Log": "[SUDO] Get Bot Logs for Internal Working",
    "Restart": "[SUDO] Reboot bot",
    "RestartSessions": "[SUDO] Reboot User Sessions",
}
