import os
import math
import wget
import requests
from yt_dlp import YoutubeDL
from pyrogram.types import Message
from pyrogram import Client, filters
from youtube_search import YoutubeSearch

ydl_opts = {
        'format':'best',
        'keepvideo':True,
        'prefer_ffmpeg':False,
        'geo_bypass':True,
        'outtmpl':'%(title)s.%(ext)s',
        'quite':True
}

@Client.on_message(filters.command("video"))
async def video(client, message):
    query = " ".join(message.command[1:])
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        title = results[0]["title"][:40]
        thumbnail = results[0]["thumbnails"][0]
        duration = results[0]["duration"]
        results[0]["url_suffix"]
    except Exception as e:
        print(e)
    try:
        msg = await message.reply("```Downloading...```")
        with YoutubeDL(ydl_opts) as ytdl:
            ytdl_data = ytdl.extract_info(link, download=True)
            file_name = ytdl.prepare_filename(ytdl_data)
    except Exception as e:
        return await msg.edit(f'**Error:** {e}')
    preview = wget.download(thumbnail)
    await msg.edit("```Uploading to telegram server...```")
    await message.reply_video(
        file_name,
        duration=int(ytdl_data["duration"]),
        thumb=preview,
        caption=ytdl_data['title'])
    try:
        os.remove(file_name)
        os.remove(preview)
        await msg.delete()
    except Exception as e:
        print(e)

@Client.on_message(filters.command("music"))
async def music(client, message):
    input = " ".join(message.command[1:])
    try:
        ydl_opts = {"format": "bestaudio[ext=m4a]"}
        results = YoutubeSearch(input, max_results=1).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        title = results[0]["title"][:40]
        thumbnail = results[0]["thumbnails"][0]
        duration = results[0]["duration"]
        results[0]["url_suffix"]
    except Exception as e:
        await message.reply("{str(e)}")
    msg = await message.reply("```Downloading...```")
    preview = wget.download(thumbnail)
    with YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(link, download=False)
        audio_file = ydl.prepare_filename(info_dict)
        ydl.process_info(info_dict)
    await msg.edit("```Uploading to telegram server...```")
    await message.reply_audio(
        audio_file,
        duration=int(info_dict["duration"]),
        thumb=preview,
        caption=info_dict['title'])
    try:
        os.remove(audio_file)
        os.remove(preview)
        await msg.delete()
    except Exception as e:
        print(e)
