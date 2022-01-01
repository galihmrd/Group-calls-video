import pafy
import asyncio
from pyrogram import Client, filters

from lib.helpers.pstream import pstream
from lib.helpers.database.chat_sql import add_chat
from lib.helpers.decorators import blacklist_users
from lib.helpers.filters import public_filters
from lib.tg_stream import group_call_factory


group_call = group_call_factory.get_group_call()

@Client.on_message(filters.command(["play", "stream"]) & public_filters)
@blacklist_users
async def play_video(client, message):
    flags = " ".join(message.command[1:])
    replied = message.reply_to_message
    text = message.text.split(None, 2)[1:]
    user = message.from_user.mention
    try:
        if text[0] == "channel":
            chat_id = int(message.chat.title)
            try:
                input = text[1]
            except Exception:
                pass
        else:
            chat_id = message.chat.id
            input = text[0]
    except Exception:
        pass
    if not replied:
        try:
            add_chat(str(chat_id))
        except BaseException:
            pass
        try:
            msg = await message.reply("`Processing...`")
            video = pafy.new(input)
            file_source = video.getbest().url
            title = video.title
        except Exception as e:
            await msg.edit(f"**Error:** {e}")
            return False
        if not group_call.is_connected:
            await pstream(chat_id, file_source)
        else
            await group_call.stop()
            await asyncio.sleep(3)
            await pstream(chat_id, file_source)
        await msg.edit(f"**Streamed by: {user}**\n**Title:** `{title}`")
    elif replied.video or replied.document:
        flags = " ".join(message.command[1:])
        chat_id = int(
            message.chat.title) if flags == "channel" else message.chat.id
        msg = await message.reply("`Downloading from telegram...`")
        file_source = await client.download_media(replied)
        try:
            add_chat(str(chat_id))
        except BaseException:
            pass
        if not group_call.is_connected:
            await pstream(chat_id, file_source)
        else:
            await group_call.stop()
            await asyncio.sleep(3)
            await pstream(chat_id, file_source)
        await msg.edit(f"**Streamed by: {user}**")
    elif replied.audio:
        flags = " ".join(message.command[1:])
        chat_id = int(
            message.chat.title) if flags == "channel" else message.chat.id
        msg = await message.reply("`Downloading from telegram...`")
        input_file = await client.download_media(replied)
        try:
            add_chat(str(chat_id))
        except BaseException:
            pass
        if not group_call.is_connected:
            await pstream(chat_id, input_file, True)
        else:
            await group_call.stop()
            await asyncio.sleep(3)
            await pstream(chat_id, input_file, True)
        await msg.edit(f"**Streamed by: {user}**")
    else:
        await message.reply("Error!")
