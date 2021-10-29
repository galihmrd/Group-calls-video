import database.blacklist as db

from pyrogram.types import Message
from pyrogram import Client, filters
from pyrogram.errors import BadRequest
from pyrogram.types.messages_and_media import message

from lib.helpers.decorators import sudo_users


@Client.on_message(filters.command("gbl"))
@sudo_users
async def blacklist(client: Client, message: Message):
    arg = message.text.split(None, 2)[1:]
    replied = message.reply_to_message
    if replied:
        user_id = replied.from_user.id
        user = await client.get_users(user_id)
        mention = user.mention
        try:
            reason = " ".join(arg[0:])
        except:
            reason = "No reason"
    elif arg[0].startswith("@"):
        try:
            user = await client.get_users(arg[0])
            user_id = user.id
            mention = user.mention
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
        user = await client.get_users(arg[0])
        mention = user.mention
        try:
            reason = arg[1]
        except:
            reason = "No reason"
    bl_check = db.is_bl(int(user_id))
    if bl_check:
        await message.reply(f"{mention} has been blacklisted")
    else:
        db.blacklist(int(user_id))
        await message.reply(f"**NewBlacklist access**\n**User:** {mention} | {user_id}\n**Reason:** {reason}")


@Client.on_message(filters.command("ungbl"))
@sudo_users
async def unblacklist(client: Client, message: Message):
    replied = message.reply_to_message
    if replied:
        user_id = replied.from_user.id
        user = await client.get_users(user_id)
        mention = user.mention
    else:
        arg = " ".join(message.command[1:])
        if arg.startswith("@"):
            try:
                user = await client.get_users(arg)
                user_id = user.id
                mention = user.mention
            except BadRequest:
                await message.reply("not a valid user")
                return ""
        else:
            user_id = int(arg)
            user = await client.get_users(arg)
            mention = user.mention
    check_bl = db.is_bl(int(user_id))
    if not check_bl:
        await message.reply(f"{mention} is not blacklisted")
    else:
        db.unblacklist(int(user_id))
        await message.reply(f"**Unblacklist access**\n**User:** {mention} | {user_id}")
