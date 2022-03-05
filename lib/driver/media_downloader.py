import asyncio
import json
import os
from urllib import request

import wget
from pyrogram import Client, filters
from pytgcalls.exceptions import NoActiveGroupCall
from youtube_search import YoutubeSearch
from yt_dlp import YoutubeDL

from lib.config import REST_API
from lib.helpers.cover_generator import generate_cover
from lib.helpers.decorators import blacklist_users
from lib.helpers.pstream import pstream_audio
from lib.helpers.time_converter import cvt_time

from .join import opengc

ydl_opts = {
    "format": "best",
    "keepvideo": True,
    "prefer_ffmpeg": False,
    "geo_bypass": True,
    "outtmpl": "%(title)s.%(ext)s",
    "quite": True,
}


@Client.on_message(filters.command(["video", "vid"]))
@blacklist_users
async def video(client, message):
    query = " ".join(message.command[1:])
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        title = results[0]["title"][:40]
        duration = results[0]["duration"]
        thumbnail = results[0]["thumbnails"][0]
        results[0]["url_suffix"]
    except Exception as e:
        print(e)
    try:
        msg = await message.reply("`Downloading...`")
        with YoutubeDL(ydl_opts) as ytdl:
            ytdl_data = ytdl.extract_info(link, download=True)
            video_file = ytdl.prepare_filename(ytdl_data)
    except Exception as e:
        return await msg.edit(f"**Error:** {e}")
    try:
        preview = wget.download(thumbnail)
    except BaseException:
        pass
    try:
        await msg.edit("`Uploading to telegram server...`")
        await message.reply_video(
            video_file,
            thumb=preview,
            duration=int(ytdl_data["duration"]),
            caption=f"**Title:** {title}\n**Duration:** {duration}\n**Source:** [YouTube]({link})\n**Requested by:** {message.from_user.mention}",
        )
    except Exception as e:
        await msg.edit(f"**Error:** {e}")
    try:
        os.remove(video_file)
        os.remove(preview)
        await msg.delete()
    except Exception as e:
        print(e)


@Client.on_message(filters.command(["music", "song"]))
@blacklist_users
async def music(client, message):
    prequest = message.from_user.first_name
    user_mention = message.from_user.mention
    input = message.text.split(None, 2)[1:]
    msg = await message.reply("`Downloading...`")
    try:
        if input[0] == "stream":
            query = input[1]
        else:
            try:
                query = " ".join(message.command[1:])
            except BaseException:
                pass
    except BaseException:
        pass
    try:
        ydl_opts = {"format": "bestaudio[ext=m4a]"}
        results = YoutubeSearch(query, max_results=1).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        title = results[0]["title"][:40]
        thumbnail = results[0]["thumbnails"][0]
        duration = results[0]["duration"]
        views = results[0]["views"]
        results[0]["url_suffix"]
    except Exception as e:
        await msg.edit(f"**Error:** ```{e}```")
    try:
        preview = wget.download(thumbnail)
    except BaseException:
        pass
    with YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(link, download=False)
        audio_file = ydl.prepare_filename(info_dict)
        ydl.process_info(info_dict)
    if input[0] == "stream":
        await msg.edit("`Generating cover...`")
        await generate_cover(prequest, title, views, duration, thumbnail)
        photo = "final.png"
        try:
            await pstream_audio(message.chat.id, audio_file, photo)
        except NoActiveGroupCall:
            await msg.edit("**No active call!**\n`Starting Group call...`")
            await opengc(client, message)
            await pstream_audio(message.chat.id, audio_file, photo)
        await msg.edit(f"**Streamed by: {user_mention}**\n**Title:** `{title}`")
        await asyncio.sleep(int(cvt_time(duration)))
        try:
            os.remove(audio_file)
            os.remove(preview)
        except BaseException:
            pass
    else:
        await msg.edit("`Uploading to telegram server...`")
        await message.reply_audio(
            audio_file,
            thumb=preview,
            duration=int(info_dict["duration"]),
            title=str(info_dict["title"]),
            caption=f"**Title:** {title}\n**Duration:** {duration}\n**Source:** [YouTube]({link})\n**Requested by:** {message.from_user.mention}",
        )
        try:
            os.remove(audio_file)
            os.remove(preview)
            await msg.delete()
        except Exception as e:
            print(e)


@Client.on_message(filters.command(["tiktok", "ttdl"]))
@blacklist_users
async def tiktokdl(client, message):
    nameFile = f"tiktok_{message.from_user.id}"
    tiktokUrl = message.command[1]
    tiktokApi = f"{REST_API}/tiktok_nowm?url={tiktokUrl}"
    try:
        msg = await message.reply("`Processing...`")
        response = request.urlopen(tiktokApi)
        data = json.loads(response.read())
        await msg.edit("`Downloading to local server...`")
        videoFile = wget.download(data["download"], nameFile)
        await msg.edit("`Uploading to telegram server...`")
        await message.reply_video(
            videoFile,
            caption=f"**Video by:** {data['from']}\n\n {data['caption']}",
        )
        try:
            os.remove(videoFile)
            await msg.delete()
        except BaseException:
            pass
    except BaseException:
        await msg.edit("Api Error!")


@Client.on_message(filters.command(["fb", "facebook"]))
async def fb_download(client, message):
    nameFile = f"fb_{message.from_user.id}"
    postUrl = message.command[1]
    fbApi = f"{REST_API}/fb?url={postUrl}"
    try:
        msg = await message.reply("`Processing...`")
        response = request.urlopen(fbApi)
        data = json.loads(response.read())
        await msg.edit("`Downloading to local server...`")
        videoFile = wget.download(data["result"][0]["download"], nameFile)
        await msg.edit("`Uploading to telegram server...`")
        await message.reply_video(
            videoFile,
            caption=f"**Url:** {postUrl}",
        )
        try:
            os.remove(videoFile)
            await msg.delete()
        except BaseException:
            pass
    except BaseException:
        await msg.edit(f"Api error!")
