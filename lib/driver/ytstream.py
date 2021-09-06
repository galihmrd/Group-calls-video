import pafy
from pyrogram import Client, filters
from pyrogram.types import Message
from lib.driver.stream import VIDEO_CALL, CHANNEL_VIDEO, group_call_factory


@Client.on_message(filters.command("ytstream"))
async def ytstream(client, message):
    query = message.command[1]
    rby = message.from_user.mention
    chat_id = message.chat.id
    video = pafy.new(query)
    txt = await message.reply(f"```Converting url...```\nUrl: ```{query}```")
    final_source = video.getbest().url
    if len(message.command) < 2:
        await message.reply("Give some youtube video url")
    else:
        group_call = group_call_factory.get_group_call()
        await group_call.join(chat_id)
        await group_call.start_video(final_source)
        VIDEO_CALL[chat_id] = group_call
        await message.reply(f"**Streaming via youtube url**\n**Requested by:** {rby}\n**To stop:** /stop")
        await txt.delete()

@Client.on_message(filters.command("ytcstream"))
async def cstream(client, message):
    query = message.command[1]
    rby = message.from_user.mention
    chat_id = message.chat.title
    video = pafy.new(query)
    text = await message.reply(f"```Converting url...```\nUrl: ```{query}```")
    source = video.getbest().url
    if len(message.command) < 2:
        await message.reply("Give some youtube url")
    else:
        group_call = group_call_factory.get_group_call()
        await group_call.join(int(chat_id))
        await group_call.start_video(source)
        CHANNEL_VIDEO[chat_id] = group_call
        await text.edit(f"**Streaming via youtube url**\n**Requested by:** {rby}\n**To stop:** /stop")
