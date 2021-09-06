from pyrogram import Client, filters
from pyrogram.types import Message

from lib.config import USERNAME_BOT

VIDEO_CALL = {}
CHANNEL_VIDEO = {}


@Client.on_message(filters.command(["stop", "stop@{USERNAME_BOT}"]))
async def stopvideo(client, m: Message):
    chat_id = m.chat.id
    user = m.from_user.mention
    try:
        await VIDEO_CALL[chat_id].stop()
        await m.reply(f"**Stopped by {user}!**")
    except Exception as e:
        await m.reply(f"**Error** - `{e}`")


@Client.on_message(filters.command(["cstop", "cstop@{USERNAME_BOT"]))
async def cstop(client, message):
    chat_id = message.chat.title
    user = message.from_user.mention
    try:
        await CHANNEL_VIDEO[chat_id].stop()
        await message.reply(f"**Stopped by {user}!**")
    except Exception as e:
        await message.reply(f"**Error:** `{e}`")
