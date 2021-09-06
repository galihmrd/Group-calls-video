import os
import asyncio
from pytgcalls import GroupCallFactory
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from lib.config import API_ID, API_HASH, SESSION_NAME, USERNAME_BOT

app = Client(SESSION_NAME, API_ID, API_HASH)
group_call_factory = GroupCallFactory(app, GroupCallFactory.MTPROTO_CLIENT_TYPE.PYROGRAM)
VIDEO_CALL = {}
CHANNEL_VIDEO = {}

@Client.on_message(filters.command(["stream", "stop@{USERNAME_BOT}"]))
async def stream(client, m: Message):
    replied = m.reply_to_message
    if not replied:
        if len(m.command) < 2:
            await m.reply("`Reply to some Video or Give Some Live Stream Url!`")
        else:
            livelink = m.text.split(None, 1)[1]
            msg = await m.reply("`Starting Live Stream...`")
            chat_id = m.chat.id
            await asyncio.sleep(1)
            try:
                group_call = group_call_factory.get_group_call()
                await group_call.join(chat_id)
                await group_call.start_video(livelink)
                VIDEO_CALL[chat_id] = group_call
                await msg.delete()
                keyboard = InlineKeyboardMarkup(

                    [
                        [
                            InlineKeyboardButton(
                                '📣 Channel support', url='https://t.me/feyystatus',
                            ),
                        ],
                    ],
                )
                await m.reply_photo(
                    photo="./etc/banner.png",
                    caption=f"**Started [Live Streaming](livelink) !**",
                    reply_markup=keyboard,
                )

            except Exception as e:
                await msg.edit(f"**Error** -- `{e}`")
    elif replied.video or replied.document:
        msg = await m.reply("`Downloading...`")
        video = await client.download_media(m.reply_to_message)
        chat_id = m.chat.id
        await asyncio.sleep(2)
        try:
            group_call = group_call_factory.get_group_call()
            await group_call.join(chat_id)
            await group_call.start_video(video)
            VIDEO_CALL[chat_id] = group_call
            await msg.delete()
            keyboard = InlineKeyboardMarkup(

                [
                    [
                        InlineKeyboardButton(
                            '📣 Channel support', url='https://t.me/feyystatus',
                        ),
                    ],
                 ],
             )
            await m.reply_photo(
                photo="./etc/banner.png",
                caption=f"**Streamed video from telegram files**",
                reply_markup=keyboard,
            )
        except Exception as e:
            await msg.edit(f"**Error** -- `{e}`")
    else:
        await m.reply("`Reply to some Video!`")

@Client.on_message(filters.command(["stop", "stop@{USERNAME_BOT}"]))
async def stopvideo(client, m: Message):
    chat_id = m.chat.id
    user = m.from_user.mention
    try:
        await VIDEO_CALL[chat_id].stop()
        await m.reply(f"**Stopped by {user}!**")
    except Exception as e:
        await m.reply(f"**🚫 Error** - `{e}`")

@Client.on_message(filters.command(["cstop", "cstop@{USERNAME_BOT"]))
async def cstop(client, message):
    chat_id = message.chat.title
    user = message.from_user.mention
    try:
        await CHANNEL_VIDEO[chat_id].stop()
        await message.reply(f"**Stopped by {user}!**")
    except Exception as e:
        await message.reply(f"**Error:** `{e}`")
