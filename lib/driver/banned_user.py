from pyrogram import Client, filters
from pyrogram.errors import BadRequest
from pyrogram.types import Message

import lib.helpers.database.blacklist as db
from lib.helpers.database.sudo_sql import is_sudo
from lib.helpers.decorators import sudo_users


@Client.on_message(filters.command(["gbl", "bl"]))
@sudo_users
async def blacklist(client: Client, message: Message):
    arg = message.text.split(None, 2)[1:]
    if replied := message.reply_to_message:
        try:
            user_id = replied.from_user.id
            user = await client.get_users(user_id)
            mention = user.mention
            try:
                reason = " ".join(arg[:])
            except BaseException:
                reason = "None"
        except BadRequest:
            return await message.reply("Failed: Invalid id")
    elif arg[0].startswith("@"):
        try:
            user = await client.get_users(arg[0])
            user_id = user.id
            mention = user.mention
            try:
                reason = arg[1]
            except BaseException:
                reason = "None"
        except BadRequest:
            return await message.reply("Failed: Invalid username")
    else:
        try:
            user_id = int(arg[0])
            user = await client.get_users(arg[0])
            mention = user.mention
            try:
                reason = arg[1]
            except BaseException:
                reason = "None"
        except BadRequest:
            return await message.reply("Failed: Invalid id")
    if check_sudo := is_sudo(int(user_id)):
        return await message.reply("Can't blacklist my sudo!")
    if db.is_bl(user_id):
        await message.reply(f"{mention} already blacklisted!")
    else:
        db.blacklist(int(user_id))
        await message.reply(
            f"**Blacklisted**\n**User:** {mention} | `{user_id}`\n**Reason:** {reason}"
        )


@Client.on_message(filters.command(["ungbl", "unbl"]))
@sudo_users
async def unblacklist(client: Client, message: Message):
    if replied := message.reply_to_message:
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
                return await message.reply("not a valid user")
        else:
            user_id = int(arg)
            user = await client.get_users(arg)
            mention = user.mention
    if check_bl := db.is_bl(int(user_id)):
        db.unblacklist(int(user_id))
        await message.reply(f"**Unblacklisted** {mention} | `{user_id}`")
    else:
        await message.reply(f"{mention} is not blacklisted")
