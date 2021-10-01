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

from random import randint
from pyrogram.types import Message
from pyrogram import Client, filters
from pyrogram.raw.types import InputGroupCall
from pyrogram.errors import UserAlreadyParticipant
from pyrogram.raw.functions.phone import CreateGroupCall

from lib.config import USERNAME_BOT
from lib.tg_stream import app as USER
from lib.helpers.filters import private_filters, public_filters


@Client.on_message(filters.command(["join",
                                    "join@{USERNAME_BOT}"]) & public_filters)
async def join(client, message):
    chat_id = message.chat.id
    try:
        link = await client.export_chat_invite_link(chat_id)
    except BaseException:
        await message.reply("**Error:**\nAdd me as admin of your group!")
        return
    try:
        await USER.join_chat(link)
        await message.reply("**Userbot Joined**")
    except UserAlreadyParticipant:
        await message.reply("**Userbot Already Participant**")

@Client.on_message(filters.command(["opengc",
                                    "opengc@{USERNAME_BOT"]) & public_filters)
async def opengc(client, message):
    flags = " ".join(message.command[1:])
    channel_id = message.chat.title
    chat_id = message.chat.id
    try:
        if flags == "channel":
             await USER.send(CreateGroupCall(
                   peer=(await USER.resolve_peer(int(channel_id))),
                        random_id=randint(10000, 999999999)
                   )
             )
             await message.reply("**Voice chat started!**")
        else:
             await USER.send(CreateGroupCall(
                   peer=(await USER.resolve_peer(chat_id)),
                        random_id=randint(10000, 999999999)
                   )
             )
             await message.reply("**Voice chat channel started!**")
    except Exception:
        await message.reply(
           "**Error:** Add userbot as admin of your group/channel with permission **Can manage voice chat**"
        )
