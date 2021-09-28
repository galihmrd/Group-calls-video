import asyncio
import pafy

from pyrogram import Client, filters
from youtube_search import YoutubeSearch
from lib.tg_stream import call_py
from lib.helpers.filters import private_filters, public_filters

from pytgcalls import idle
from pytgcalls import StreamType
from pytgcalls.types.input_stream import AudioVideoPiped
from pytgcalls.types.input_stream.quality import MediumQualityAudio
from pytgcalls.types.input_stream.quality import MediumQualityVideo



@Client.on_message(filters.command("play") & public_filters)
async def play_video(client, message):
    flags = " ".join(message.command[1:])
    replied = message.reply_to_message
    if not replied:
        try:
            msg = await message.reply("```Processing...```")
            chat_id = message.chat.id
            input = " ".join(message.command[1:])
            video = pafy.new(input)
            file = video.getbest().url
        except Exception as e:
            await msg.edit(f"**Error:** {e}")
            return False
        await msg.edit("```Streamed```")
        await call_py.join_group_call(
            chat_id,
            AudioVideoPiped(
                file,
                MediumQualityAudio(),
                MediumQualityVideo()
            ),
            stream_type=StreamType().live_stream
        )
    elif replied.video or replied.document:
        if flags == "channel":
             chat_id = int(message.chat.title)
        else:
             chat_id = message.chat.id
        msg = await message.reply("```Downloading from telegram...```")
        file = await client.download_media(replied)
        await msg.edit("```Streamed```")
        await call_py.join_group_call(
            chat_id,
            AudioVideoPiped(
                file,
                MediumQualityAudio(),
                MediumQualityVideo()
            ),
            stream_type=StreamType().live_stream
        )
    else:
        await message.reply("```Please reply to video or video file to stream```")

@call_py.on_stream_end()
async def end(cl, update):
    print("stream ended in " + str(update.chat_id))
    await call_py.leave_group_call(update.chat_id)
