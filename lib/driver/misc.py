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

from datetime import datetime
from pyrogram.types import Message
from pyrogram import Client, filters
from lib.tg_stream import call_py
from lib.config import USERNAME_BOT, SUDO_USERS
from lib.helpers.decorators import sudo_users
from pytgcalls.exceptions import GroupCallNotFound


@Client.on_message(filters.command(["ping", "ping@{USERNAME_BOT}"]))
async def ping_(client: Client, message: Message):
    start = datetime.now()
    msg = await message.reply_text('`Latensi`')
    end = datetime.now()
    latency = (end - start).microseconds / 1000
    await msg.edit(f"**Latency:** `{latency} ms`")


@Client.on_message(filters.command(["repo", "repo@{USERNAME_BOT}"]))
async def repo(client, message):
    repo = "https://github.com/galihmrd/Group-calls-video"
    license = "https://github.com/galihmrd/Group-calls-video/blob/stream/beta/LICENSE"
    await message.reply(f"**Source code:** [Here]({repo})\n**License:** [GPL-3.0 License]({license})")


@Client.on_message(filters.command("pause"))
async def pause(client, message):
    query = " ".join(message.command[1:])
    if query == "channel":
        chat_id = int(message.chat.title)
        type = "Channel"
    else:
        chat_id = message.chat.id
        type = "Group"
    try:
        await call_py.pause_stream(chat_id)
        await message.reply(f"**{type} stream paused!**")
    except GroupCallNotFound:
        await message.reply('**Error:** GroupCall not found!')


@Client.on_message(filters.command("resume"))
async def resume(client, message):
    query = " ".join(message.command[1:])
    if query == "channel":
        chat_id = int(message.chat.title)
        type = "Channel"
    else:
        chat_id = message.chat.id
        type = "Group"
    try:
        await call_py.resume_stream(chat_id)
        await message.reply(f"**{type} stream resumed!**")
    except GroupCallNotFound:
        await message.reply("**Error:** GroupCall not found!")


@Client.on_message(filters.command("stop"))
@sudo_users
async def stopped(client, message):
    query = " ".join(message.command[1:])
    user_id = message.from_user.id
    if query == "channel":
        chat_id = int(message.chat.title)
        type = "Channel"
    else:
        chat_id = message.chat.id
        type = "Group"
    try:
        await call_py.leave_group_call(chat_id)
        await message.reply(f"**{type} stream stopped!**")
    except GroupCallNotFound:
        await message.reply("**Error:** GroupCall not found")


@Client.on_message(filters.command("volume"))
@sudo_users
async def change_volume(client, message):
    range = " ".join(message.command[1])
    chat_id = message.chat.id
    try:
       await call_py.change_volume_call(chat_id, range)
       await message.reply(f"**Volume changed to:** ```{range}```")
    except Exception as e:
       await message.reply(f"**Error:** {e}")
