#!/usr/bin/env python3
from datetime import datetime

from sys import version_info
from pkg_resources import get_distribution

from bot import (
    __version__,
)

def get_version():
    return {
        "bot_version": __version__,
        "bot_name": "MirrorBeast",
        "fork_name": "MirrorBeast",
        "fork_url": "https://github.com/BeastBots/MirrorBeast",
        "python_version": f"{version_info[0]}.{version_info[1]}.{version_info[2]}",
        "os_arch": "Server",
    }


if __name__ == "__main__":
    print(get_version())
