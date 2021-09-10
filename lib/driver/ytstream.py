import pafy
from pyrogram import Client, filters
from pyrogram.types import (
     InlineKeyboardButton,
     InlineKeyboardMarkup,
     Message,
)
from lib.config import USERNAME_BOT
from lib.driver.stream import group_call_factory
from lib.driver.misc import CHANNEL_VIDEO, VIDEO_CALL
from lib.helpers.filters import private_filters, public_filters


@Client.on_message(filters.command(["ytstream",
                                    "ytstream@{USERNAME_BOT}"]) & public_filters)
async def ytstream(client, message):
    query = message.command[1]
    rby = message.from_user.mention
    chat_id = message.chat.id
    txt = await message.reply(f"```Converting url...```\nUrl: ```{query}```")
    try:
        video = pafy.new(query)
        title = video.title
        duration = video.duration
        final_source = video.getbest().url
    except Exception as e:
        await message.reply(f'**Error:** {e}')
    if len(message.command) < 2:
        await message.reply("Give some youtube video url")
    else:
        group_call = group_call_factory.get_group_call()
        await group_call.join(chat_id)
        await group_call.start_video(final_source, enable_experimental_lip_sync=True)
        VIDEO_CALL[chat_id] = group_call
        await txt.delete()
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        '📣 Channel support', url='https://t.me/feyystatus',
                    ),
                ],
            ],
        )
        await message.reply_photo(
            caption=f"**Streaming [{title}]({query})**\n**Duration:** {duration}\n**Requested by:** {rby}\n**To stop:** /stop",
            photo="./etc/banner.png",
            reply_markup=keyboard,
        )

@Client.on_message(filters.command(["ytcstream",
                                    "ytstream@{USERNAME_BOT}"]) & public_filters)
async def cstream(client, message):
    query = message.command[1]
    rby = message.from_user.mention
    chat_id = message.chat.title
    text = await message.reply(f"```Converting url...```\nUrl: ```{query}```")
    try:
        video = pafy.new(query)
        title = video.title
        duration = video.duration
        source = video.getbest().url
    except Exception as e:
        await message.reply(f'**Error:** {e}')
    if len(message.command) < 2:
        await message.reply("Give some youtube url")
    else:
        group_call = group_call_factory.get_group_call()
        await group_call.join(int(chat_id))
        await group_call.start_video(source, enable_experimental_lip_sync=True)
        CHANNEL_VIDEO[chat_id] = group_call
        await text.delete()
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        '📣 Channel support', url='https://t.me/feyystatus',
                    ),
                ],
            ],
        )
        await message.reply_photo(
            caption=f"**Streaming [{title}]({query})**\n**Duration:** {duration}\n**Requested by:** {rby}\n**To stop:** /cstop",
            photo="./etc/banner.png",
            reply_markup=keyboard,
        )
