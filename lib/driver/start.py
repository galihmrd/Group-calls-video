from pyrogram.types import Message
from pyrogram import Client, filters

from lib.config import USERNAME_BOT


HELP_TEXT = """**List Command:**

**/stream** -> [reply to file/put streaming url]
**/cstream** -> [stream in channel]

**/ytstream** -> [put youtube url]
**/ytcstream** -> [stream in channel]

**/stop** -> [for group]
**/cstop** -> [for channel]

**/schedule** {value} -> [stop scheduler]
"""

@Client.on_message(filters.command(["start", "start@{USERNAME_BOT}"]))
async def start(client, message):
    await message.reply("**👋 I'm alive**")

@Client.on_message(filters.command(["help", "help@{USERNAME_BOT}"]))
async def help(client, message):
    await message.reply(HELP_TEXT)
