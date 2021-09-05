import pafy
from pyrogram import Client, filters
from pyrogram.types import Message
from lib.driver.stream import group_call_factory


VIDEO_CALL = {}

@Client.on_message(filters.command("ytstream"))
async def ytstream(client, message):
    query = message.command[1]
    chat_id = message.chat.id
    video = pafy.new(query)
    final_source = video.getbest().url
    txt = await message.reply("```Download and converting...```")
    if len(message.command) < 2:
        await message.reply("Give some youtube video url")
    else:
        group_call = group_call_factory.get_group_call()
        await group_call.join(chat_id)
        await group_call.start_video(final_source)
        VIDEO_CALL[chat_id] = group_call
        await message.reply("**Streamed!**")
        await txt.delete()
