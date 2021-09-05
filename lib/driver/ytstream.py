import pafy
from pyrogram import Client, filters
from pyrogram.types import Message
from lib.driver.stream import group_call_factory


VIDEO_CALL = {}

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
        await message.reply(f"**Streaming via youtube url**\n**Requested by:** {rby}\n**To stop:** /ytstop")
        await txt.delete()

@Client.on_message(filters.command(["ytstop", "ytstop@{USERNAME_BOT}"]))
async def ytstop(client, message):
    chat_id = message.chat.id
    try:
        await VIDEO_CALL[chat_id].stop()
        await message.reply("**Stopped!**")
    except Exception as e:
        await message.reply("error")
