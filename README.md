<p align="center">
    <a href="https://github.com/BeastBots/MirrorBeast">
        <kbd>
            <img width="250" src="https://i.imgur.com/1QEBdAB.png" alt="Mirror Beast Logo">
        </kbd>
    </a>

<i>Mirror Beast is a powerful, feature-rich Telegram bot for downloading, mirroring, and managing various types of content. Based on WZML-X by SilentDemonSD with significant enhancements and optimizations.</i>

</p>

<div align=center>

[![](https://img.shields.io/badge/Mirror%20Beast-v1.0.0--beast-blue?style=flat&labelColor=292c3b)](#) [![](https://img.shields.io/badge/License-MIT-important?style=flat&labelColor=292c3b)](https://github.com/BeastBots/MirrorBeast/blob/master/LICENSE) [![](https://img.shields.io/badge/Telegram-Channel-9cf?style=flat&logo=telegram&logoColor=blue&labelColor=292c3b)](https://t.me/MirrorBeast) [![](https://img.shields.io/badge/Support-Group-9cf?style=flat&logo=telegram&logoColor=blue&labelColor=292c3b)](https://t.me/MirrorBeastSupport)

</div>

---

# ✨ Mirror Beast Features

- **Multi-source Downloads**: Torrents, direct links, Google Drive, Mega.nz, Telegram files, and more
- **Multi-destination Uploads**: Google Drive, Telegram, and Rclone-supported clouds
- **Customizable Processing**: Extract, compress, sample videos, take screenshots, and more 
- **Powerful Media Tools**: Media info, IMDb data, custom thumbnails, subtitles
- **Advanced Leech Options**: Split files, upload as document/media, custom captions
- **User Management**: Authorization system, usage limits, queuing system
- **Elegant UI**: Clean status display, progress tracking, and user-friendly commands
- **Extended Search**: Torrent search, IMDb lookups, and media information retrieval
- **Automation**: RSS feed monitoring and automatic downloads

---

# 🚀 Deployment Guide

<details>
<summary><b>🖥️ VPS Deployment</b></summary>

### Prerequisites
- A VPS with Ubuntu/Debian
- Docker and Docker Compose installed
- Git installed

### Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/BeastBots/MirrorBeast && cd MirrorBeast
   ```

2. **Create your config file**
   ```bash
   cp config_sample.py config.py
   ```
   
3. **Edit the config file with your settings**
   ```bash
   nano config.py
   ```

4. **Build and run with Docker Compose (recommended)**
   ```bash
   sudo docker-compose up -d
   ```

5. **View logs**
   ```bash
   sudo docker-compose logs -f
   ```

</details>

<details>
<summary><b>☁️ Heroku Deployment</b></summary>

1. Fork this repository
2. Go to your Heroku account and create a new app
3. Connect the app to your GitHub repository
4. Add the following buildpacks:
   - heroku/python
   - https://github.com/jonathanong/heroku-buildpack-ffmpeg-latest
   - https://github.com/HasibulKabir/heroku-buildpack-rclone
5. Add the required environment variables from config_sample.py
6. Deploy the app

</details>

---

# 📝 Configuration

All configuration options are documented in the `config_sample.py` file. You can create your own `config.py` file based on this template.

Key configuration sections:
- Telegram API credentials
- Bot behavior settings
- Download/Upload preferences
- Service integrations (Google Drive, Rclone, JDownloader, etc.)
- User access control
- Media processing options

New features:
- `SHOW_CLOUD_LINKS`: Toggle visibility of cloud storage links (Drive/Rclone) in task completion messages

---

# 🤖 Bot Commands

<details>
<summary><b>View Command List</b></summary>

### General Commands
- `/start` - Start the bot
- `/help` - Get detailed help
- `/stats` - Bot usage statistics
- `/status` - Check ongoing tasks

### Mirror Commands
- `/mirror` - Mirror to cloud
- `/qbmirror` - Mirror using qBittorrent
- `/jdmirror` - Mirror using JDownloader
- `/nzbmirror` - Mirror using Usenet

### Leech Commands
- `/leech` - Leech to Telegram
- `/qbleech` - Leech using qBittorrent
- `/jdleech` - Leech using JDownloader
- `/nzbleech` - Leech using Usenet

### Other Commands
- `/clone` - Clone Google Drive files
- `/count` - Count files in Drive
- `/search` - Search torrents or Drive
- `/cancel` - Cancel a task
- `/ytdl` - Download YouTube videos
- `/imdb` - Search IMDb for media info

</details>

---

# 🌟 Public Leech Group

For users who want to use our free public Mirror Beast bots, join our [leech group](https://t.me/MirrorBeastGroup).

For additional services and links, check our [Beast Gateways](https://t.me/MirrorBeastGateways/8).

---

# 👥 Credits

- Original base: [WZML-X](https://github.com/SilentDemonSD/WZML-X) by SilentDemonSD
- Enormous thanks to all the contributors of the original projects

---

# ⚖️ License

This project is licensed under the [MIT License](LICENSE).

