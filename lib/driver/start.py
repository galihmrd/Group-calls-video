from pyrogram import Message
from pyrogram import Client, filters
from lib.helpers.decorators import blacklist_users


@Client.on_message(filters.command("start"))
@blacklist_users
async def start(client, message):
    await message.reply(f"Hello {message.from_user.name} how are you?")
