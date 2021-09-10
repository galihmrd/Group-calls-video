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

import time
import asyncio
from datetime import datetime
from pyrogram.types import Message
from pyrogram import Client, filters

from lib.config import USERNAME_BOT
from lib.helpers.filters import private_filters, public_filters

VIDEO_CALL = {}
CHANNEL_VIDEO = {}


# Convert seconds to mm:ss
def convert_seconds(seconds):
    seconds = seconds % (24 * 3600)
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%02d:%02d" % (minutes, seconds)

# Convert hh:mm:ss to seconds
def time_to_seconds(time):
    stringt = str(time)
    return sum(
        int(x) * 60 ** i for i,
        x in enumerate(
            reversed(
                stringt.split(":"))))


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
    if len(message.command) >= 2:
        pass
    else:
        await message.reply("Please enter value in seconds")
        return
    chat_id = message.chat.id
    chid = message.chat.title
    user = message.from_user.mention
    input = message.command[1]
    txt = await message.reply(f"**Stopped in** `{input}s`")
    await asyncio.sleep(int(input))
    try:
        await txt.edit(f"**Stopped by {user}!**")
        await VIDEO_CALL[chat_id].stop()
    except Exception:
        return
    try:
        await CHANNEL_VIDEO[chid].stop()
    except Exception:
        pass
