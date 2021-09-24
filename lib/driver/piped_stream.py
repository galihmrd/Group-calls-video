import asyncio

from pyrogram import Client, filters
from lib.tg_stream import call_py
from youtube_search import YoutubeSearch

from pytgcalls import idle
from pytgcalls import StreamType
from pytgcalls.types.input_stream import AudioVideoPiped
from pytgcalls.types.input_stream.quality import MediumQualityAudio
from pytgcalls.types.input_stream.quality import MediumQualityVideo



async def get_youtube_stream(input: str):
    proc = await asyncio.create_subprocess_exec(
        'yt-dlp',
        '-g',
        '-f',
        # CHANGE THIS BASED ON WHAT YOU WANT
        'best[height<=?480][width<=?854]',
        f"https://youtube.com{YoutubeSearch(input, 1).to_dict()[0]['url_suffix']}",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    return stdout.decode().split('\n')[0]

@Client.on_message(filters.command("play"))
async def play_video(client, message):
    replied = message.reply_to_message
    if not replied:
        msg = await message.reply("```Processing...```")
        chat_id = message.chat.id
        input = " ".join(message.command[1:])
        file = await get_youtube_stream(input)
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
        msg = await message.reply("```Downloading from telegram...```")
        chat_id = message.chat.id
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

