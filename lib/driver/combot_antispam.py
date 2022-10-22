import asyncio

import requests
from pyrogram import Client, filters
from pyrogram.types import ChatPermissions, InlineKeyboardButton, InlineKeyboardMarkup


@Client.on_message(filters.all)
async def checker(client, message):
    id_ = message.from_user.id
    chat_ = message.chat.id
    api = f"https://api.cas.chat/check?user_id={id_}"
    session = requests.Session()
    req = session.request("get", api)
    status = req.json()["ok"]
    # Check
    get = await client.get_users(id_)
    username = get.username
    mention = get.mention
    if username == None:
        msg = await message.reply(
            f"{mention} multed!\nReason: no username!",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            ">> Tap to Unmute <<",
                            callback_data="unmute",
                        ),
                    ],
                ],
            ),
        )
        try:
            await client.restrict_chat_member(chat_, id_, ChatPermissions())
            await asyncio.sleep(240)
            await client.ban_chat_member(chat_, id_)
            await asyncio.sleep(35)
            await client.unban_chat_member(chat_, id_)
        except:
            await msg.edit(f"{mention} user without username")
        if status == True:
            try:
                result = req.json()["result"]
                reason = f"https://cas.chat/query?u={id_}"
                offenses = result["offenses"]
                time_added = result["time_added"]
                await msg.edit(
                    f"**COMBOT ANTI SPAM**\n\n**User:** {mention} banned!\n**ID:** `{id_}`\n**Reason:** [Link]({reason})\n**Time added:** {time_added}"
                )
                await client.ban_chat_member(chat_, id_)
            except Exception as e:
                await message.reply(e)
    else:
        print(username)
        if status == True:
            try:
                result = req.json()["result"]
                reason = f"https://cas.chat/query?u={id_}"
                offenses = result["offenses"]
                time_added = result["time_added"]
                await message.reply(
                    f"**COMBOT ANTI SPAM**\n\n**User:** {mention} banned!\n**ID:** `{id_}`\n**Reason:** [Link]({reason})\n**Time added:** {time_added}"
                )
                await client.ban_chat_member(chat_, id_)
            except:
                pass
        else:
            await message.reply(f"{mention} Joined!\nCombot & username check passed")


@Client.on_callback_query(filters.regex(pattern=r"^(unmute)$"))
async def inline_unmute(client, callback):
    ids = callback.message.from_user.id
    chats = callback.message.chat.id
    get = await client.get_users(ids)
    username = get.username
    if username == None:
        await callback.answer("Set your username first!")
    else:
        await client.restrict_chat_member(
            chats,
            ids,
            ChatPermissions(
                can_send_messages=True,
                can_send_media_messages=True,
                can_send_other_messages=True,
            ),
        )
