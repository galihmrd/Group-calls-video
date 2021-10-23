
import pafy
from pyrogram import Client, filters
from pytgcalls import StreamType
from pytgcalls.exceptions import NoActiveGroupCall
from pytgcalls.types.input_stream import AudioImagePiped, AudioVideoPiped
from pytgcalls.types.input_stream.quality import MediumQualityVideo

from database.database_chat_sql import add_chat_to_db
from lib.helpers.filters import public_filters
from lib.tg_stream import call_py

from .join import opengc


@Client.on_message(filters.command("play") & public_filters)
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
            add_chat_to_db(str(chat_id))
            msg = await message.reply("```Processing...```")
            video = pafy.new(input)
            file_source = video.getbest().url
            title = video.title
        except Exception as e:
            await msg.edit(f"**Error:** {e}")
            return False
        await msg.edit(f"**Streamed by: {user}**\n**Title:** ```{title}```")
        try:
            await call_py.join_group_call(
                chat_id,
                AudioVideoPiped(
                    file_source
                ),
                stream_type=StreamType().live_stream
            )
        except NoActiveGroupCall:
            await opengc(client, message)
    elif replied.video or replied.document:
        flags = " ".join(message.command[1:])
        chat_id = int(
            message.chat.title) if flags == "channel" else message.chat.id
        msg = await message.reply("```Downloading from telegram...```")
        file_source = await client.download_media(replied)
        await msg.edit(f"**Streamed by: {user}**")
        try:
            add_chat_to_db(str(chat_id))
            await call_py.join_group_call(
                chat_id,
                AudioVideoPiped(
                    file_source
                ),
                stream_type=StreamType().live_stream
            )
        except NoActiveGroupCall:
            await opengc(client, message)
    elif replied.audio:
        flags = " ".join(message.command[1:])
        chat_id = int(
            message.chat.title) if flags == "channel" else message.chat.id
        msg = await message.reply("```Downloading from telegram...```")
        input_file = await client.download_media(replied)
        await msg.edit(f"**Streamed by: {user}**")
        try:
            add_chat_to_db(str(chat_id))
            await call_py.join_group_call(
                chat_id,
                AudioImagePiped(
                    input_file,
                    './etc/banner.png',
                    video_parameters=MediumQualityVideo(),
                ),
                stream_type=StreamType().pulse_stream,
            )
        except NoActiveGroupCall:
            await opengc(client, message)
    else:
        await message.reply("Error!")


@call_py.on_stream_end()
async def end(cl, update):
    print("stream ended in " + str(update.chat_id))
    await call_py.leave_group_call(update.chat_id)
