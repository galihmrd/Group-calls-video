import database.database_banned_sql as db

from pyrogram.types import Message
from pyrogram import Client, filters
from pyrogram.errors import BadRequest
from pyrogram.types.messages_and_media import message

from lib.helpers.text_helper import get_arg
from lib.helpers.decorators import sudo_users


@Client.on_message(filters.command("gbl"))
@sudo_users
async def blacklist(client: Client, message: Message):
    arg = message.text.split(None, 2)[1:]
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        try:
           reason = arg[0]
        except:
           reason = "No reason"
    else:
        if arg[0].startswith("@"):
            try:
                user = await client.get_users(arg[0])
                user_id = user.id
                try:
                   reason = arg[1]
                except:
                   reason = "No reason"
            except BadRequest as ex:
                await message.reply("not a valid user")
                print(ex)
                return ""
        else:
            user_id = int(arg[0])
            try:
               reason = arg[1]
            except:
               reason = "No reason"
        db.banned_user(int(user_id))
        await message.reply(f"**User:** [blacklisted](tg://user?id={user_id})\n**Reason:** {reason}")


@Client.on_message(filters.command("ungbl"))
@sudo_users
async def unblacklist(client: Client, message: Message):
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user["id"]
    else:
        arg = " ".join(message.command[1:])
        if arg.startswith("@"):
            try:
                user = await client.get_users(arg)
                user_id = user.id
            except BadRequest:
                await message.reply("not a valid user")
                return ""
        else:
            user_id = int(arg)
        db.unban_user(int(user_id))
        await message.reply(f"[unblacklisted](tg://user?id={user_id})")
