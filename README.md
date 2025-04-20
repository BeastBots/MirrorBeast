<p align="center">
    <a href="https://github.com/BeastBots/MirrorBeast">
        <kbd>
            <img width="250" src="https://imgur.com/dX6GoKH.png" alt="MirrorBeast Logo">
        </kbd>
    </a>

<i>MirrorBeast is a powerful extended fork of <a href="https://github.com/SilentDemonSD/WZML-X">WZML-X</a>, enhancing the traditional mirror-leech Telegram bot with advanced features, improved architecture, and seamless integration capabilities. Powered by Beast, this version offers a comprehensive solution for all your mirroring, leeching, and file management needs.</i>

</p>

<div align=center>

[![](https://img.shields.io/github/repo-size/BeastBots/MirrorBeast?color=green&label=Repo%20Size&labelColor=292c3b)](#) [![](https://img.shields.io/github/commit-activity/m/BeastBots/MirrorBeast?logo=github&labelColor=292c3b&label=Github%20Commits)](#) [![](https://img.shields.io/github/license/BeastBots/MirrorBeast?style=flat&label=License&labelColor=292c3b)](#)|[![](https://img.shields.io/github/issues-raw/BeastBots/MirrorBeast?style=flat&label=Open%20Issues&labelColor=292c3b)](#) [![](https://img.shields.io/github/issues-closed-raw/BeastBots/MirrorBeast?style=flat&label=Closed%20Issues&labelColor=292c3b)](#) [![](https://img.shields.io/github/issues-pr-raw/BeastBots/MirrorBeast?style=flat&label=Open%20Pull%20Requests&labelColor=292c3b)](#) [![](https://img.shields.io/github/issues-pr-closed-raw/BeastBots/MirrorBeast?style=flat&label=Closed%20Pull%20Requests&labelColor=292c3b)](#)
:---:|:---:|
[![](https://img.shields.io/github/languages/count/BeastBots/MirrorBeast?style=flat&label=Total%20Languages&labelColor=292c3b&color=blueviolet)](#) [![](https://img.shields.io/github/languages/top/BeastBots/MirrorBeast?style=flat&logo=python&labelColor=292c3b)](#) [![](https://img.shields.io/github/last-commit/BeastBots/MirrorBeast?style=flat&label=Last%20Commit&labelColor=292c3b&color=important)](#) [![](https://badgen.net/github/branches/BeastBots/MirrorBeast?label=Total%20Branches&labelColor=292c3b)](#)|[![](https://img.shields.io/github/forks/BeastBots/MirrorBeast?style=flat&logo=github&label=Forks&labelColor=292c3b&color=critical)](#) [![](https://img.shields.io/github/stars/BeastBots/MirrorBeast?style=flat&logo=github&label=Stars&labelColor=292c3b&color=yellow)](#)
[![](https://img.shields.io/badge/Telegram%20Channel-Join-9cf?style=for-the-badge&logo=telegram&logoColor=blue&style=flat&labelColor=292c3b)](https://t.me/MirrorBeast) |[![](https://img.shields.io/badge/Support%20Group-Join-9cf?style=for-the-badge&logo=telegram&logoColor=blue&style=flat&labelColor=292c3b)](https://t.me/MirrorBeastSupport) | [![](https://img.shields.io/badge/Mirror%20Group-Join-9cf?style=for-the-badge&logo=telegram&logoColor=blue&style=flat&labelColor=292c3b)](https://t.me/MirrorBeastGroup)

</div>

<div align="center">
    <img src="https://imgur.com/DK02Qhr.png" alt="MirrorBeast Banner" width="100%">
</div>

---

# 🔥 What's New in MirrorBeast

MirrorBeast builds upon the foundations of WZML-X with significant enhancements:

- **Enhanced Architecture**: Completely restructured codebase for better performance and scalability
- **Advanced JDownloader Integration**: Superior JDownloader support with improved API integration
- **SABnzbd Support**: Full integration with SABnzbd for Usenet downloads
- **Improved Web UI**: Sleek, responsive web interface for easy management
- **Hybrid Leech System**: Optimized leech operations with advanced control mechanisms
- **Multi-Cloud Support**: Expanded cloud service integrations beyond the basics
- **Optimized Performance**: Reduced resource utilization and faster processing
- **Enhanced Queue Management**: Smart queue system with priority handling
- **Expanded Media Processing**: Better media handling, metadata extraction, and formatting
- **Powerful Search Capabilities**: Improved search algorithms across multiple sources

---

# 🚀 Deployment Guide

<details>
  <summary><strong>VPS Deployment <kbd>Click Here</kbd></strong></summary>

## 1. Installing Requirements

Clone this repository:

```bash
git clone https://github.com/BeastBots/MirrorBeast mirrorbot/ && cd mirrorbot
```

## 2. Build and Run with Docker

There are two methods to build and run the Docker image:

### Method 1: Using Official Docker Commands

- **Start Docker daemon** (skip if already running):

  ```bash
  sudo dockerd
  ```

- **Build the Docker image:**

  ```bash
  sudo docker build . -t mirrorbeast
  ```

- **Run the image:**

  ```bash
  sudo docker run -p 80:80 -p 8080:8080 mirrorbeast
  ```

- **To stop the running image:**

  ```bash
  sudo docker ps
  sudo docker stop <container_id>
  ```

### Method 2: Using docker-compose (Recommended)

- **Install docker-compose:**

  ```bash
  sudo apt install docker-compose
  ```

- **Build and run the Docker image:**

  ```bash
  sudo docker-compose up
  ```

- **After editing files, rebuild:**

  ```bash
  sudo docker-compose up --build
  ```

- **To stop the running image:**

  ```bash
  sudo docker-compose stop
  ```

- **To restart the image:**

  ```bash
  sudo docker-compose start
  ```

#### Important Docker Notes

1. Set `BASE_URL_PORT` and `RCLONE_SERVE_PORT` variables to any port you want to use. Default is `80` and `8080` respectively.
2. You should stop the running image before deleting the container and you should delete the container before the image.
3. To delete the container:

```bash
sudo docker container prune
```

4. To delete images:

```bash
sudo docker image prune -a
```

5. Check the number of processing units of your machine with `nproc` cmd and multiply by 4, then edit `AsyncIOThreadsCount` in qBittorrent.conf.
    
</details>

<details>
  <summary><strong>Heroku Deployment <kbd>Click Here</kbd></strong></summary>

## Setup on Heroku

1. Fork this repository
2. Go to your forked repository settings -> secrets
3. Add the following secrets:
   - `HEROKU_API_KEY`: Your Heroku API key
   - `HEROKU_APP_NAME`: Your Heroku app name
   - `HEROKU_EMAIL`: Your Heroku email
4. Go to Actions tab and run the workflow

For more detailed instructions, check the [deployment guide](https://github.com/BeastBots/MirrorBeast/wiki/Heroku-Deployment).

</details>

---

# 📋 Features

<details>
  <summary><strong>Core Features</strong></summary>
  
- **Mirror and Leech**: Mirror to Google Drive or leech to Telegram
- **Multi-Protocol Support**: Torrent, Direct links, Mega.nz, and more
- **Usenet Support**: Full integration with SABnzbd
- **JDownloader Support**: Enhanced integration with JDownloader
- **Telegram File Operations**: Upload, download, and manage files directly via Telegram
- **Customizable Upload**: Configure upload destinations with ease
- **Media Conversion**: Convert media to different formats
- **Metadata Management**: Extract and modify metadata from files
- **Cloud Integration**: Google Drive, OneDrive, and other cloud services
- **Queue Management**: Sophisticated queue system with priority handling
- **Automated Tasks**: Schedule tasks with built-in cron functionality
- **Web Interface**: Feature-rich web UI for remote management

</details>

<details>
  <summary><strong>Additional Features</strong></summary>
  
- **User Authentication**: Multi-tier user access control
- **Webhook Integration**: Connect with external services via webhooks
- **Customizable UI**: Personalize bot interface and responses
- **Multi-language Support**: Bot supports multiple languages
- **Status Updates**: Real-time status updates for ongoing tasks
- **Log Management**: Advanced logging with configurable levels
- **Performance Monitoring**: Resource usage and performance metrics
- **Proxy Support**: Route traffic through proxies for privacy
- **Rate Limiting**: Prevent abuse with intelligent rate limiting
- **Extensible Architecture**: Easy to extend with new functionality
- **Plugin System**: Add new features via plugins

</details>

---

# 🔧 Configuration

Copy `config_sample.py` to `config.py` and edit the required variables:

<details>
  <summary><strong>Essential Configuration</strong></summary>

```python
# REQUIRED CONFIG
BOT_TOKEN = "Telegram Bot Token"
OWNER_ID = 123456789  # Your Telegram User ID
TELEGRAM_API = 123456  # Your Telegram API ID
TELEGRAM_HASH = "abcdef123456"  # Your Telegram API Hash
DATABASE_URL = "MongoDB URL"
```

</details>

<details>
  <summary><strong>Advanced Configuration</strong></summary>

See `config_sample.py` for all available configuration options. Key sections include:

- Task Limits
- Media Search
- Bot Settings
- GDrive Tools
- Rclone Configuration
- JDownloader Setup
- SABnzbd Setup
- Leech Options
- Search Configuration

</details>

---

# 📱 Connect with Us

- **Channel**: [MirrorBeast](https://t.me/MirrorBeast)
- **Support Group**: [MirrorBeastSupport](https://t.me/MirrorBeastSupport)
- **Mirror Group**: [MirrorBeastGroup](https://t.me/MirrorBeastGroup)

---

# 👨‍💻 Contributors

<details>
  <summary><strong>Click Here For Contributors</strong></summary>

|<img width="80" src="https://github.com/BeastBots.png">|
|:---:|
|[`Beast`](https://github.com/BeastBots)|
|Project Lead & Developer|

</details>

---

# 📝 License

MirrorBeast is licensed under the [MIT License](LICENSE).

