from io import BytesIO

from pyrogram import Client, filters
from pyrogram.types import Message

from lib.helpers.database.chat_sql import chatlists, rm_chat
from lib.helpers.decorators import sudo_users
from lib.helpers.text_helper import get_arg


@Client.on_message(filters.command("broadcast"))
@sudo_users
async def broadcast(client: Client, message: Message):
    to_send = get_arg(message)
    success = 0
    failed = 0
    for chat in chatlists()():
        try:
            await client.send_message(
                str(chat),
                to_send
            )
            success += 1
        except BaseException:
            failed += 1
            rm_chat(str(chat))
    await message.reply(
        f"Message sent to {success} chat(s). {failed} chat(s) failed recieve message"
    )


@Client.on_message(filters.command("chatlist"))
@sudo_users
async def chatlist(client, message):
    all_chats = chatlists()
    chats = [i for i in all_chats if str(i).startswith("-")]
    chatfile = "Daftar chat.\n0. ID grup | Jumlah anggota | tautan undangan\n"
    P = 1
    for chat in chats:
        try:
            link = await client.export_chat_invite_link(int(chat))
        except BaseException:
            link = "Null"
        try:
            members = await client.get_chat_members_count(int(chat))
        except BaseException:
            members = "Null"
        try:
            chatfile += f"{P}. {chat} | {members} | {link}\n"
            P += 1
        except BaseException:
            pass
    with BytesIO(str.encode(chatfile)) as output:
        output.name = "chatlist.txt"
        await message.reply_document(document=output, disable_notification=True)
