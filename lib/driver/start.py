'''
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
'''

from pyrogram.types import Message
from pyrogram import Client, filters

from lib.config import USERNAME_BOT


HELP_TEXT = """**List Command:**

**• /stream** -> [reply to file/put streaming url]
**• /cstream** -> [stream in channel]

**• /ytstream** -> [put youtube url]
**• /ytcstream** -> [stream in channel]

**• /pause** -> [pause group stream]
**• /pause channel** -> [pause channel stream]

**• /resume** -> [resume group stream]
**• /resume channel** -> [resume channel stream]

**• /stop** -> [for group]
**• /stop channel** -> [for channel]

**• /schedule** {value} -> [stop scheduler]
"""

@Client.on_message(filters.command(["start", "start@{USERNAME_BOT}"]))
async def start(client, message):
    await message.reply("**👋 I'm alive**")

@Client.on_message(filters.command(["help", "help@{USERNAME_BOT}"]))
async def help(client, message):
    await message.reply(HELP_TEXT)
