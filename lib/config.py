import os

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
SESSION_NAME = os.getenv("SESSION_NAME")
COMMAND_PREFIXES = os.getenv("COMMAND_PREFIXES", "!")
BOTLOG_CHATID = os.getenv("BOTLOG_CHATID")
DATABASE_URL = os.getenv("DATABASE_URL")
TIKTOK_API = os.getenv("TIKTOK_API", "https://yourapi.tiktok")
SUDO_USERS = list(map(int, os.getenv("SUDO_USERS").split()))
