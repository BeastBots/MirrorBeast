#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Configuration file for Beast - Mirror/Leech Telegram Bot
Based on WZML-X by SilentDemonSD, further enhanced and customized
"""

#----------------------------------------------------------#
#                     REQUIRED CONFIG                       #
#----------------------------------------------------------#
BOT_TOKEN = ""                         # Your Telegram Bot API token from @BotFather
OWNER_ID = 0                           # Your Telegram User ID (not username) as an integer
TELEGRAM_API = 0                       # Your Telegram API ID from my.telegram.org
TELEGRAM_HASH = ""                     # Your Telegram API Hash from my.telegram.org
DATABASE_URL = ""                      # MongoDB connection string

#----------------------------------------------------------#
#                   BOT BASIC SETTINGS                      #
#----------------------------------------------------------#
DEFAULT_LANG = "en"                    # Default language code (en, hi, fr, etc)
CMD_SUFFIX = ""                        # Command suffix (e.g., "1" would make commands like /mirror1)
STATUS_LIMIT = 10                      # Number of tasks shown in status message
STATUS_UPDATE_INTERVAL = 15            # Time in seconds between status updates
SET_COMMANDS = True                    # Set bot commands in Telegram client
BOT_PM = False                         # Enable/disable private messaging with bot
TIMEZONE = "Asia/Kolkata"              # Timezone for displaying times correctly

# Bot appearance and behavior
CUSTOM_BOT_HEADER = "Mirror Beast"     # Custom header for status page
CUSTOM_BOT_HEADER_LINK = "https://t.me/MirrorBeast"  # Link for the header
EXCLUDED_EXTENSIONS = ""               # File extensions to exclude, comma-separated (e.g., "exe,zip")
INCOMPLETE_TASK_NOTIFIER = False       # Notify about incomplete tasks
NAME_SWAP = ""                         # Swap words in filenames, format: "word1:word2,word3:word4"
FFMPEG_CMDS = {}                       # Custom FFMPEG commands
UPLOAD_PATHS = {}                      # Custom upload paths for different filetypes
CLEAN_LOG_MSG = False                  # Auto-delete log messages
SHOW_CLOUD_LINKS = True                # Show cloud storage links in task completion messages

# Telegram connection
TG_PROXY = (
    {}
)  # {"scheme": "socks5", "hostname": "", "port": 1234, "username": "user", "password": "pass"}
USER_SESSION_STRING = ""               # Pyrogram session string for user account
HELPER_TOKENS = ""                     # Extra bot tokens for parallel operations

#----------------------------------------------------------#
#                   ACCESS CONTROL                          #
#----------------------------------------------------------#
AUTHORIZED_CHATS = ""                  # Chat IDs where bot is usable (comma-separated)
SUDO_USERS = ""                        # User IDs with sudo access (comma-separated)
FORCE_SUB_IDS = ""                     # Chat IDs where subscription is required
LOGIN_PASS = ""                        # Password for accessing the bot
VERIFY_TIMEOUT = 0                     # Time for user verification in seconds

# Task limits
BOT_MAX_TASKS = 0                      # Maximum simultaneous tasks for the bot (0 = unlimited)
USER_MAX_TASKS = 0                     # Maximum simultaneous tasks per user (0 = unlimited)
USER_TIME_INTERVAL = 0                 # Cooldown between user tasks in seconds

#----------------------------------------------------------#
#                   DOWNLOAD SETTINGS                       #
#----------------------------------------------------------#
DEFAULT_UPLOAD = "rc"                  # Default upload type: 'gd' (Google Drive) or 'rc' (Rclone)
YT_DLP_OPTIONS = ""                    # youtube-dl options as a JSON string

# API Keys for various services
FILELION_API = ""                      # API key for FileLion
STREAMWISH_API = ""                    # API key for StreamWish
INSTADL_API = ""                       # API for Instagram downloads

# MegaAPI credentials
MEGA_EMAIL = ""                        # Mega.nz account email
MEGA_PASSWORD = ""                     # Mega.nz account password

# JDownloader
JD_EMAIL = ""                          # JDownloader email
JD_PASS = ""                           # JDownloader password

#----------------------------------------------------------#
#                      TASK LIMITS                          #
#----------------------------------------------------------#
# Set to 0 for unlimited
DIRECT_LIMIT = 0                       # Max size for direct links in GB
MEGA_LIMIT = 0                         # Max size for Mega.nz links in GB
TORRENT_LIMIT = 0                      # Max size for torrents in GB
GD_DL_LIMIT = 0                        # Max size for Google Drive downloads in GB
RC_DL_LIMIT = 0                        # Max size for Rclone downloads in GB
CLONE_LIMIT = 0                        # Max size for cloning in GB
JD_LIMIT = 0                           # Max size for JDownloader downloads in GB
NZB_LIMIT = 0                          # Max size for NZB files in GB
YTDLP_LIMIT = 0                        # Max size for YT-DLP downloads in GB
PLAYLIST_LIMIT = 0                     # Max videos in a playlist
LEECH_LIMIT = 0                        # Max size for leeching in GB
EXTRACT_LIMIT = 0                      # Max size for extraction in GB
ARCHIVE_LIMIT = 0                      # Max size for archiving in GB
STORAGE_LIMIT = 0                      # Max bot storage usage in GB

#----------------------------------------------------------#
#                    GOOGLE DRIVE TOOLS                     #
#----------------------------------------------------------#
GDRIVE_ID = ""                         # Default Google Drive folder ID
GD_DESP = "Uploaded with Beast"         # Description for uploads
IS_TEAM_DRIVE = False                  # Set to True if using Team Drive
STOP_DUPLICATE = False                 # Check for duplicates on Google Drive
INDEX_URL = ""                         # Index URL for direct links

#----------------------------------------------------------#
#                    RCLONE CONFIG                          #
#----------------------------------------------------------#
RCLONE_PATH = ""                       # Path to rclone.conf file
RCLONE_FLAGS = ""                      # Custom rclone flags
RCLONE_SERVE_URL = ""                  # Rclone serve URL
RCLONE_SERVE_PORT = 0                  # Rclone serve port
RCLONE_SERVE_USER = ""                 # Rclone serve username
RCLONE_SERVE_PASS = ""                 # Rclone serve password

#----------------------------------------------------------#
#                  LEECH SETTINGS                           #
#----------------------------------------------------------#
LEECH_SPLIT_SIZE = 0                   # Split files larger than this size in bytes (default: 2GB)
AS_DOCUMENT = False                    # Upload files as document instead of media
EQUAL_SPLITS = False                   # Create equal-sized parts
MEDIA_GROUP = False                    # Send media as a group
USER_TRANSMISSION = True               # Let users decide transmission type
HYBRID_LEECH = True                    # Both media and document based on type
LEECH_PREFIX = ""                      # Add prefix to leeched files
LEECH_SUFFIX = ""                      # Add suffix to leeched files
LEECH_FONT = ""                        # Font for custom filenames
LEECH_CAPTION = ""                     # Caption for leeched files
LEECH_DUMP_CHAT = ""                   # Chat ID where to dump leeched files
THUMBNAIL_LAYOUT = ""                  # Caption for thumbnail layout

#----------------------------------------------------------#
#             TORRENT / DIRECT DOWNLOAD SETTINGS            #
#----------------------------------------------------------#
# qBittorrent/Aria2c
TORRENT_TIMEOUT = 0                    # Timeout for torrents in seconds (0 = no timeout)
BASE_URL = ""                          # Web server base URL
BASE_URL_PORT = 0                      # Web server port
WEB_PINCODE = True                     # Use pincode for web server

# Queue system
QUEUE_ALL = 0                          # Number of parallel tasks in queue (0 = disable queue)
QUEUE_DOWNLOAD = 0                     # Number of parallel downloads
QUEUE_UPLOAD = 0                       # Number of parallel uploads

#----------------------------------------------------------#
#                    MEDIA SETTINGS                         #
#----------------------------------------------------------#
# IMDb template for movie/series info
IMDB_TEMPLATE = """<b>🎬 Title:</b> <a href="{url}">{title}</a> [{year}]
<b>🌟 Rating:</b> <code>{rating}/10</code> ({votes} votes)
<b>🎭 Genre:</b> {genres}
<b>📅 Released:</b> <a href="{url_releaseinfo}">{release_date}</a>
<b>🎙️ Language:</b> {languages}
<b>🌍 Country:</b> {countries}
<b>🎬 Also Known As:</b> {aka}

<b>📝 Storyline:</b>
<blockquote>{plot}</blockquote>

<b>🎭 Cast:</b> <a href="{url_cast}">View on IMDb</a>
<b>⏱️ Runtime:</b> {runtime} minutes
<b>🏆 Awards:</b> {awards}
<b>🎞️ Director:</b> {director}

<b>💾 Downloaded by:</b> <a href="https://t.me/MirrorBeast">Beast</a>"""

# Media tools settings
MEDIA_STORE = True                     # Store media in personal database for users

#----------------------------------------------------------#
#                     RSS SETTINGS                          #
#----------------------------------------------------------#
RSS_DELAY = 600                        # Time in seconds between RSS checks
RSS_CHAT = ""                          # Chat ID where to send RSS feeds
RSS_SIZE_LIMIT = 0                     # Maximum size for RSS downloads in GB

#----------------------------------------------------------#
#                  TORRENT SEARCH                           #
#----------------------------------------------------------#
SEARCH_API_LINK = ""                   # Torrent search API URL
SEARCH_LIMIT = 0                       # Maximum number of search results (0 = unlimited)
SEARCH_PLUGINS = [
    "https://raw.githubusercontent.com/qbittorrent/search-plugins/master/nova3/engines/piratebay.py",
    "https://raw.githubusercontent.com/qbittorrent/search-plugins/master/nova3/engines/limetorrents.py",
    "https://raw.githubusercontent.com/qbittorrent/search-plugins/master/nova3/engines/torlock.py",
    "https://raw.githubusercontent.com/qbittorrent/search-plugins/master/nova3/engines/torrentscsv.py",
    "https://raw.githubusercontent.com/qbittorrent/search-plugins/master/nova3/engines/eztv.py",
    "https://raw.githubusercontent.com/qbittorrent/search-plugins/master/nova3/engines/torrentproject.py",
    "https://raw.githubusercontent.com/MaurizioRicci/qBittorrent_search_engines/master/kickass_torrent.py",
    "https://raw.githubusercontent.com/MaurizioRicci/qBittorrent_search_engines/master/yts_am.py",
    "https://raw.githubusercontent.com/MadeOfMagicAndWires/qBit-plugins/master/engines/linuxtracker.py",
    "https://raw.githubusercontent.com/MadeOfMagicAndWires/qBit-plugins/master/engines/nyaasi.py",
    "https://raw.githubusercontent.com/LightDestory/qBittorrent-Search-Plugins/master/src/engines/ettv.py",
    "https://raw.githubusercontent.com/LightDestory/qBittorrent-Search-Plugins/master/src/engines/glotorrents.py",
    "https://raw.githubusercontent.com/LightDestory/qBittorrent-Search-Plugins/master/src/engines/thepiratebay.py",
    "https://raw.githubusercontent.com/v1k45/1337x-qBittorrent-search-plugin/master/leetx.py",
    "https://raw.githubusercontent.com/nindogo/qbtSearchScripts/master/magnetdl.py",
    "https://raw.githubusercontent.com/msagca/qbittorrent_plugins/main/uniondht.py",
    "https://raw.githubusercontent.com/khensolomon/leyts/master/yts.py",
]

#----------------------------------------------------------#
#                   USENET SERVERS                          #
#----------------------------------------------------------#
# Sabnzbd
USENET_SERVERS = [
    {
        "name": "main",                # Server name
        "host": "",                    # Server hostname
        "port": 563,                   # Server port
        "timeout": 60,                 # Connection timeout
        "username": "",                # Username
        "password": "",                # Password
        "connections": 8,              # Maximum connections
        "ssl": 1,                      # Use SSL (0=no, 1=yes)
        "ssl_verify": 2,               # SSL verification level
        "ssl_ciphers": "",             # SSL ciphers
        "enable": 1,                   # Enable server (0=no, 1=yes)
        "required": 0,                 # Required server (0=no, 1=yes)
        "optional": 0,                 # Optional server (0=no, 1=yes)
        "retention": 0,                # Retention days
        "send_group": 0,               # Send group (0=no, 1=yes)
        "priority": 0,                 # Server priority (0=highest)
    }
]

#----------------------------------------------------------#
#                     UPDATE SETTINGS                       #
#----------------------------------------------------------#
UPSTREAM_REPO = ""                     # Git repository URL for updates
UPSTREAM_BRANCH = "master"             # Git branch for updates
UPDATE_PKGS = False                    # Update pip packages on startup
