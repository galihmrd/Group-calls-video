import os
import asyncio
from pytgcalls import GroupCallFactory
from pyrogram import Client, filters
from pyrogram.types import Message
from config import API_ID, API_HASH, SESSION_NAME

app = Client(SESSION_NAME, API_ID, API_HASH)
group_call_factory = GroupCallFactory(app, GroupCallFactory.MTPROTO_CLIENT_TYPE.PYROGRAM)
VIDEO_CALL = {}


@Client.on_message(filters.command("stream"))
async def stream(client, m: Message):
    replied = m.reply_to_message
    if not replied:
        await m.reply("`Reply to some Video!`")
    elif replied.video or replied.document:
        msg = await m.reply("`Downloading...`")
        chat_id = m.chat.id
        await asyncio.sleep(2)
        try:
            group_call = group_call_factory.get_group_call()
            await group_call.join(chat_id)
            await group_call.start_video(video)
            VIDEO_CALL[chat_id] = group_call
            await msg.edit("**▶️ Started Streaming!**")
        except Exception as e:
            await msg.edit(f"**Error** -- `{e}`")
    else:
        await m.reply("`Reply to some Video!`")

@Client.on_message(filters.command("stop"))
async def stopvideo(client, m: Message):
    chat_id = m.chat.id
    try:
        await VIDEO_CALL[chat_id].stop()
        await m.reply("**⏹️ Stopped Streaming!**")
    except Exception as e:
        await m.reply(f"**🚫 Error** - `{e}`")
