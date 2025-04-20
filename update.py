from sys import exit
from importlib import import_module
from logging import (
    FileHandler,
    StreamHandler,
    INFO,
    basicConfig,
    error as log_error,
    info as log_info,
    warning as log_warning,
    getLogger,
    ERROR,
)
from os import path, remove, environ, makedirs
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from subprocess import run as srun, call as scall, PIPE, STDOUT
from shutil import rmtree
from time import time

getLogger("pymongo").setLevel(ERROR)

var_list = [
    "BOT_TOKEN",
    "TELEGRAM_API",
    "TELEGRAM_HASH",
    "OWNER_ID",
    "DATABASE_URL",
    "BASE_URL",
    "UPSTREAM_REPO",
    "UPSTREAM_BRANCH",
    "UPDATE_PKGS",
]

# Clean up log files
if path.exists("log.txt"):
    with open("log.txt", "r+") as f:
        f.truncate(0)

if path.exists("rlog.txt"):
    remove("rlog.txt")

# Ensure backup directory exists
backup_dir = "update_backup"
if not path.exists(backup_dir):
    makedirs(backup_dir, exist_ok=True)

basicConfig(
    format="[%(asctime)s] [%(levelname)s] - %(message)s",
    datefmt="%d-%b-%y %I:%M:%S %p",
    handlers=[FileHandler("log.txt"), StreamHandler()],
    level=INFO,
)

# Function for secure command execution with output capture
def execute_command(command, shell=True):
    try:
        result = srun(command, shell=shell, stdout=PIPE, stderr=STDOUT, text=True)
        if result.returncode != 0:
            log_error(f"Command failed with code {result.returncode}: {result.stdout}")
            return False, result.stdout
        return True, result.stdout
    except Exception as e:
        log_error(f"Command execution error: {str(e)}")
        return False, str(e)

# Function to check current version against repository
def check_for_updates(repo, branch):
    try:
        # Create a temporary directory for version checking
        temp_dir = f"temp_check_{int(time())}"
        makedirs(temp_dir, exist_ok=True)
        
        # Clone only the latest commit to check version
        success, output = execute_command(
            f"git clone --depth 1 --branch {branch} {repo} {temp_dir}"
        )
        if not success:
            rmtree(temp_dir, ignore_errors=True)
            return True  # Assume update needed if check fails
            
        # Check for version differences
        from bot.version import get_version as current_version
        version_file = path.join(temp_dir, "bot", "version.py")
        
        if path.exists(version_file):
            spec = {}
            with open(version_file) as f:
                exec(f.read(), spec)
            repo_version = spec.get("get_version", lambda: "v0.0.0")()
            
            if current_version() == repo_version:
                log_info(f"Already up to date with version {repo_version}")
                rmtree(temp_dir, ignore_errors=True)
                return False
            else:
                log_info(f"Update available: {current_version()} → {repo_version}")
        
        rmtree(temp_dir, ignore_errors=True)
        return True
    except Exception as e:
        log_error(f"Version check failed: {str(e)}")
        return True  # Assume update needed if check fails

try:
    settings = import_module("config")
    config_file = {
        key: value.strip() if isinstance(value, str) else value
        for key, value in vars(settings).items()
        if not key.startswith("__")
    }
except ModuleNotFoundError:
    log_info("Config.py file is not Added! Checking ENVs..")
    config_file = {}

env_updates = {
    key: value.strip() if isinstance(value, str) else value
    for key, value in environ.items()
    if key in var_list
}
if env_updates:
    log_info("Config data is updated with ENVs!")
    config_file.update(env_updates)

BOT_TOKEN = config_file.get("BOT_TOKEN", "")
if not BOT_TOKEN:
    log_error("BOT_TOKEN variable is missing! Exiting now")
    exit(1)

BOT_ID = BOT_TOKEN.split(":", 1)[0]

if DATABASE_URL := config_file.get("DATABASE_URL", "").strip():
    try:
        conn = MongoClient(DATABASE_URL, server_api=ServerApi("1"))
        db = conn.wzmlx
        old_config = db.settings.deployConfig.find_one({"_id": BOT_ID}, {"_id": 0})
        config_dict = db.settings.config.find_one({"_id": BOT_ID})
        if (
            old_config is not None and old_config == config_file or old_config is None
        ) and config_dict is not None:
            config_file["UPSTREAM_REPO"] = config_dict["UPSTREAM_REPO"]
            config_file["UPSTREAM_BRANCH"] = config_dict.get("UPSTREAM_BRANCH", "master")
            config_file["UPDATE_PKGS"] = config_dict.get("UPDATE_PKGS", "True")
        conn.close()
    except Exception as e:
        log_error(f"Database ERROR: {e}")

UPSTREAM_REPO = config_file.get("UPSTREAM_REPO", "").strip()
UPSTREAM_BRANCH = config_file.get("UPSTREAM_BRANCH", "").strip() or "master"

if UPSTREAM_REPO:
    # Create backup of current code
    timestamp = int(time())
    backup_name = f"{backup_dir}/backup_{timestamp}"
    success, _ = execute_command(f"cp -r . {backup_name} 2>/dev/null || mkdir -p {backup_name}")
    if success:
        log_info(f"Created backup at {backup_name}")
    
    # Check if update is needed
    if not check_for_updates(UPSTREAM_REPO, UPSTREAM_BRANCH):
        log_info("No updates available. Skipping update process.")
    else:
        log_info(f"Updating from: {UPSTREAM_REPO} | Branch: {UPSTREAM_BRANCH}")
        
        if path.exists(".git"):
            log_info("Removing existing git repository...")
            rmtree(".git", ignore_errors=True)
            
        # Clone with proper Git identity for Mirror Beast
        update_command = f"""
            git init -q \
            && git config --global user.email 131198906+ThePrateekBhatia@users.noreply.github.com \
            && git config --global user.name Prateek Bhatia \
            && git add . \
            && git commit -sm "pre-update snapshot" -q \
            && git remote add origin {UPSTREAM_REPO} \
            && git fetch origin -q \
            && git reset --hard origin/{UPSTREAM_BRANCH} -q
        """
        
        success, output = execute_command(update_command)
        
        if success:
            log_info("Successfully updated with latest changes!")
        else:
            log_error(f"Update failed! Error: {output}")
            log_warning("Attempting to rollback to previous version...")
            
            # Rollback from backup
            rollback_cmd = f"rsync -a --delete {backup_name}/ . --exclude {backup_dir}/"
            success, output = execute_command(rollback_cmd)
            
            if success:
                log_info("Rollback successful. Your bot is back to the previous state.")
            else:
                log_error(f"Rollback failed! You may need to reinstall. Error: {output}")
                log_info(f"Your backup is available at: {backup_name}")

    repo = UPSTREAM_REPO.split("/")
    if len(repo) >= 2:
        UPSTREAM_REPO = f"https://github.com/{repo[-2]}/{repo[-1]}"
        log_info(f"Using repository: {UPSTREAM_REPO} | Branch: {UPSTREAM_BRANCH}")
    else:
        log_warning(f"Unable to parse repository format: {UPSTREAM_REPO}")


UPDATE_PKGS = config_file.get("UPDATE_PKGS", "True")
if (isinstance(UPDATE_PKGS, str) and UPDATE_PKGS.lower() == "true") or UPDATE_PKGS:
    log_info("Updating packages...")
    try:
        # Try using uv first (faster)
        success, output = execute_command("command -v uv")
        if success:
            success, output = execute_command("uv pip install -U -r requirements.txt")
        else:
            # Fall back to pip if uv is not available
            success, output = execute_command("pip install -U -r requirements.txt")
        
        if success:
            log_info("Successfully updated all packages!")
        else:
            log_error(f"Package update failed! Error: {output}")
    except Exception as e:
        log_error(f"Package installation error: {str(e)}")
