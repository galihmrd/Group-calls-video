import asyncio
from datetime import datetime
from pyrogram.types import Message
from pyrogram import Client, filters

from lib.config import USERNAME_BOT

VIDEO_CALL = {}
CHANNEL_VIDEO = {}


@Client.on_message(filters.command(["stop", "stop@{USERNAME_BOT"]))
async def cstop(client, message):
    chat_id = message.chat.title
    chid = message.chat.id
    user = message.from_user.mention
    try:
        await message.reply(f"**Stopped by {user}!**")
        await VIDEO_CALL[chid].stop()
        await CHANNEL_VIDEO[chat_id].stop()
    except Exception as e:
        pass

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

@Client.on_message(filters.command("schedule"))
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
