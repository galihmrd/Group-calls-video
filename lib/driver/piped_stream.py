import pafy
from pyrogram import Client, filters
from pytgcalls.exceptions import NoActiveGroupCall, NotInGroupCallError
from youtube_search import YoutubeSearch

from lib.helpers.database.chat_sql import add_chat
from lib.helpers.decorators import blacklist_users
from lib.helpers.filters import public_filters
from lib.helpers.pstream import pstream
from lib.helpers.ffmpeg_audio import time_stamp
from lib.tg_stream import call_py

from .join import opengc


@Client.on_message(filters.command(["play", "stream"]) & public_filters)
@blacklist_users
async def play_video(client, message):
    flags = " ".join(message.command[1:])
    replied = message.reply_to_message
    text = message.text.split(None, 2)[1:]
    user = message.from_user.mention
    try:
        if text[0] == "-channel":
            chat_id = int(message.chat.title)
            try:
                input = " ".join(text[1:])
            except Exception:
                pass
        else:
            chat_id = message.chat.id
            input = " ".join(message.command[1:])
    except Exception:
        pass
    if not replied:
        try:
            add_chat(str(chat_id))
        except BaseException:
            pass
        try:
            msg = await message.reply("`Searching...`")
            results = YoutubeSearch(input, max_results=1).to_dict()
            vUrl = f"https://youtube.com{results[0]['url_suffix']}"
            await msg.edit("`Processing...`")
            video = pafy.new(vUrl)
            file_source = video.getbest().url
            title = video.title
        except Exception as e:
            await msg.edit(f"**Error:** {e}")
            return False
        try:
            await pstream(chat_id, file_source)
        except NoActiveGroupCall:
            await msg.edit("**No active call!**\n`Starting Group call...`")
            await opengc(client, message)
            await pstream(chat_id, file_source)
        await msg.edit(f"**Played by {user}**\n**Target {chat_id}**\n`{title}`")
    elif replied.video or replied.document:
        outName = f"{message.from_user.id}_video.mp4}"
        flags = " ".join(message.command[1:])
        chat_id = int(message.chat.title) if flags == "-channel" else message.chat.id
        msg = await message.reply("`Downloading from telegram...`")
        file_source = await client.download_media(replied)
        await msg.edit("Ffmpeg process...")
        time_stamp(file_source, outName)
        try:
            add_chat(str(chat_id))
        except BaseException:
            pass
        try:
            await pstream(chat_id, outName)
        except NoActiveGroupCall:
            await msg.edit("**No active call!**\n`Starting Group call...`")
            await opengc(client, message)
            await pstream(chat_id, outName)
        await msg.edit(f"**Played by {user}**\n**Target {chat_id}**")
    elif replied.audio:
        flags = " ".join(message.command[1:])
        chat_id = int(message.chat.title) if flags == "-channel" else message.chat.id
        msg = await message.reply("`Downloading from telegram...`")
        input_file = await client.download_media(replied)
        try:
            add_chat(str(chat_id))
        except BaseException:
            pass
        try:
            await pstream(chat_id, input_file, True)
        except NoActiveGroupCall:
            await msg.edit("**No active call!**\n`Starting Group call...`")
            await opengc(client, message)
            await pstream(chat_id, input_file, True)
        await msg.edit(f"**Played by {user}**\n**Target {chat_id}**")
    else:
        await message.reply("Error!")


@call_py.on_stream_end()
async def end(cl, update):
    print("stream ended in " + str(update.chat_id))
    try:
        await call_py.leave_group_call(update.chat_id)
    except NotInGroupCallError:
        pass
