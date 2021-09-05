from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import UserAlreadyParticipant
from lib.driver.stream import app as USER
from lib.config import USERNAME_BOT


@Client.on_message(filters.command(["join", "join@{USERNAME_BOT}"]))
async def join(client, message):
    chat_id = message.chat.id
    try:
        link = await client.export_chat_invite_link(chat_id)
    except BaseException:
        await message.reply("**Error:**\nAdd me as admin of your group!")
        return
    try:
        await USER.join_chat(link)
    except UserAlreadyParticipant:
        pass
