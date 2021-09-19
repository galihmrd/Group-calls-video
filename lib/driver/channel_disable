import os
import asyncio
import subprocess
from pytgcalls import idle
from pytgcalls import PyTgCalls
from pytgcalls import StreamType
from pytgcalls.types.input_stream import (
                        AudioParameters,
                        InputAudioStream,
                        InputVideoStream,
                        VideoParameters,

)
from pyrogram import Client, filters
from pyrogram.types import Message
from lib.config import USERNAME_BOT
from yt_dlp import YoutubeDL
from yt_dlp.utils import ExtractorError
from lib.tg_stream import call_py, app

SIGINT: int = 2
FFMPEG_PROCESS = {}

def raw_converter(dl, song, video):
    return subprocess.Popen(
        ['ffmpeg', '-i', dl, '-f', 's16le', '-ac', '1', '-ar', '48000', song, '-y', '-f', 'rawvideo', '-r', '20', '-pix_fmt', 'yuv420p', '-vf', 'scale=854:480', video, '-y'],
        stdin=None,
        stdout=None,
        stderr=None,
        cwd=None,
    )

def youtube(url: str):
    try:
        params = {"format": "best[height=?480]/best", "noplaylist": True}
        yt = YoutubeDL(params)
        info = yt.extract_info(url, download=False)
        return info['url']
    except ExtractorError: # do whatever
        return 
    except Exception:
        return


@Client.on_message(filters.command(["cplay", "cplay@{USERNAME_BOT}"]) & filters.group & ~filters.edited)
async def cstartvideo(client, m: Message):
    replied = m.reply_to_message
    if not replied:
        if len(m.command) < 2:
            await m.reply("💡 reply to video or provide youtube/live video url to start video streaming")
        else:
            livelink = m.text.split(None, 1)[1]
            chat_id = m.chat.title
            try:
                livelink = await asyncio.wait_for(
                    app.loop.run_in_executor(
                        None,
                        lambda : youtube(livelink)
                    ),
                    timeout=None # Add timeout (recommended)
                )
            except asyncio.TimeoutError:
                await m.reply("TimeoutError: process is taking unexpected time")
                return
            if not livelink:
                await m.reply("failed to get video data")
                return
            process = raw_converter(livelink, f'audio{chat_id}.raw', f'video{chat_id}.raw')
            FFMPEG_PROCESS[chat_id] = process
            msg = await m.reply("🔁 **Starting video streaming...**")
            await asyncio.sleep(10)
            try:
                audio_file = f'audio{chat_id}.raw'
                video_file = f'video{chat_id}.raw'
                while not os.path.exists(audio_file) or \
                        not os.path.exists(video_file):
                    await asyncio.sleep(2)
                await call_py.join_group_call(
                    int(chat_id),
                    InputAudioStream(
                        audio_file,
                        AudioParameters(
                            bitrate=48000,
                        ),
                    ),
                    InputVideoStream(
                        video_file,
                        VideoParameters(
                            width=854,
                            height=480,
                            frame_rate=20,
                        ),
                    ),
                    stream_type=StreamType().live_stream,
                )
                await msg.edit("💡 **Video streaming started!**\n\n» **join to video chat on the top to watch the video.**")
                await idle()
            except Exception as e:
                await msg.edit(f"🚫 **error** | `{e}`")
   
    elif replied.video or replied.document:
        msg = await m.reply("📥 Downloading video...")
        video = await client.download_media(m.reply_to_message)
        chat_id = m.chat.title
        await msg.edit("🔁 **Preparing...**")
        os.system(f"ffmpeg -i '{video}' -f s16le -ac 1 -ar 48000 'audio{chat_id}.raw' -y -f rawvideo -r 20 -pix_fmt yuv420p -vf scale=640:360 'video{chat_id}.raw' -y")
        try:
            audio_file = f'audio{chat_id}.raw'
            video_file = f'video{chat_id}.raw'
            while not os.path.exists(audio_file) or \
                    not os.path.exists(video_file):
                await asyncio.sleep(2)
            await call_py.join_group_call(
                int(chat_id),
                InputAudioStream(
                    audio_file,
                    AudioParameters(
                        bitrate=48000,
                    ),
                ),
                InputVideoStream(
                    video_file,
                    VideoParameters(
                        width=640,
                        height=360,
                        frame_rate=20,
                    ),
                ),
                stream_type=StreamType().local_stream,
            )
            await msg.edit("💡 **Video streaming started!**\n\n» **join to video chat on the top to watch the video.**")
        except Exception as e:
            await msg.edit(f"🚫 **Error** | `{e}`")
            await idle()
    else:
        await m.reply("💭 Please reply to video or video file to stream")


@Client.on_message(filters.command(["cstop", "cstop@{USERNAME_BOT}"]) & filters.group & ~filters.edited)
async def cstopvideo(client, m: Message):
    chat_id = m.chat.title
    try:
        process = FFMPEG_PROCESS.get(chat_id)
        if process:
            try:
                process.send_signal(SIGINT)
                await asyncio.sleep(3)
            except Exception as e:
                print(e)
        await call_py.leave_group_call(int(chat_id))
        await m.reply("✅ **Disconnected from vc !**")
    except Exception as e:
        await m.reply(f"🚫 **Error** | `{e}`")
