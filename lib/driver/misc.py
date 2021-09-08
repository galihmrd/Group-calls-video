import asyncio
from datetime import datetime
from pyrogram.types import Message
from pyrogram import Client, filters

from lib.config import USERNAME_BOT
from lib.helpers.filters import private_filters, public_filters

VIDEO_CALL = {}
CHANNEL_VIDEO = {}


@Client.on_message(filters.command(["stop",
                                    "stop@{USERNAME_BOT}"]) & public_filters)
async def stopvideo(client, m: Message):
    chat_id = m.chat.id
    user = m.from_user.mention
    try:
        await VIDEO_CALL[chat_id].stop()
        await m.reply(f"**Stopped by {user}!**")
    except Exception as e:
        await m.reply(f"**Error:** {str(e)}")

@Client.on_message(filters.command(["cstop",
                                    "cstop@{USERNAME_BOT"]) & public_filters)
async def cstop(client, message):
    chat_id = message.chat.title
    user = message.from_user.mention
    try:
        await CHANNEL_VIDEO[chat_id].stop()
        await message.reply(f"**Stopped by {user}!**")
    except Exception as e:
        await message.reply(f"**Error:** {str(e)}")

@Client.on_message(filters.command(["ping", "ping@{USERNAME_BOT}"]))
async def ping_(client: Client, message: Message):
    start = datetime.now()
    msg = await message.reply_text('`Latensi`')
    end = datetime.now()
    latency = (end - start).microseconds / 1000
    await msg.edit(f"**Latency:** `{latency} ms`")

@Client.on_message(filters.command(["repo", "repo@{USERNAME_BOT}"]))
async def repo(client, message):
    repo = "https://github.com/Imszy17/tg-stream-video"
    await message.reply(f"**Source code:** [Here]({repo})")

@Client.on_message(filters.command(["schedule",
                                    "schedule@{USERNAME_BOT}"]) & public_filters)
async def sch(client, message):
    chat_id = message.chat.id
    chid = message.chat.title
    user = message.from_user.mention
    input = message.command[1]
    txt = await message.reply(f"**Stopped in** `{input}s`")
    await asyncio.sleep(int(input))
    try:
        await txt.edit(f"**Stopped by {user}!**")
        await VIDEO_CALL[chat_id].stop()
        await CHANNEL_VIDEO[chid].stop()
    except Exception as e:
        pass
