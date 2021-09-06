import pafy
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from lib.driver.misc import CHANNEL_VIDEO, VIDEO_CALL
from lib.driver.stream import group_call_factory


@Client.on_message(filters.command("ytstream"))
async def ytstream(client, message):
    query = message.command[1]
    rby = message.from_user.mention
    chat_id = message.chat.id
    txt = await message.reply(f"```Converting url...```\nUrl: ```{query}```")
    try:
        video = pafy.new(query)
        final_source = video.getbest().url
    except Exception as e:
        await message.reply(f'**Error:** {e}')
    if len(message.command) < 2:
        await message.reply("Give some youtube video url")
    else:
        group_call = group_call_factory.get_group_call()
        await group_call.join(chat_id)
        await group_call.start_video(final_source)
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
            caption=f"**Streaming via [youtube url]({query})**\n**Requested by:** {rby}\n**To stop:** /stop",
            photo="./etc/banner.png",
            reply_markup=keyboard,
        )


@Client.on_message(filters.command("ytcstream"))
async def cstream(client, message):
    query = message.command[1]
    rby = message.from_user.mention
    chat_id = message.chat.title
    text = await message.reply(f"```Converting url...```\nUrl: ```{query}```")
    try:
        video = pafy.new(query)
        source = video.getbest().url
    except Exception as e:
        await message.reply(f'**Error:** {e}')
    if len(message.command) < 2:
        await message.reply("Give some youtube url")
    else:
        group_call = group_call_factory.get_group_call()
        await group_call.join(int(chat_id))
        await group_call.start_video(source)
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
            caption=f"**Streaming via [youtube url]({query})**\n**Requested by:** {rby}\n**To stop:** /cstop",
            photo="./etc/banner.png",
            reply_markup=keyboard,
        )
