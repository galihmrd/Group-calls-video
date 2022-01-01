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

from pyrogram import Client, filters
from pyrogram.types import Message

from lib.config import USERNAME_BOT
from lib.helpers.decorators import blacklist_users, sudo_users
from lib.tg_stream import app as USER


@Client.on_message(filters.command(["ping", "ping@{USERNAME_BOT}"]))
@blacklist_users
async def ping_(client: Client, message: Message):
    start = datetime.now()
    msg = await message.reply_text('`Latensi`')
    end = datetime.now()
    latency = (end - start).microseconds / 1000
    await msg.edit(f"**Latency:** `{latency} ms`")


@Client.on_message(filters.command(["repo", "repo@{USERNAME_BOT}"]))
@blacklist_users
async def repo(client, message):
    repo = "https://github.com/galihmrd/Group-calls-video"
    license = "https://github.com/galihmrd/Group-calls-video/blob/stream/beta/LICENSE"
    await message.reply(f"**Source code:** [Here]({repo})\n**License:** [GPL-3.0 License]({license})")


@Client.on_message(filters.command(["logs", "log"]))
@sudo_users
async def logfile(client, message):
    await client.send_document(document="log.txt", chat_id=message.from_user.id)
    await message.reply("I've send the log on PM's")


# PMpermit #
@USER.on_message(filters.text & filters.private & ~filters.me & ~filters.bot)
async def pmPermit(client: USER, message: Message):
    await USER.send_message(
        message.chat.id,
        f"Hello {message.from_user.mention} How are you?"
    )
