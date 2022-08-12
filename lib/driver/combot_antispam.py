import requests

from pyrogram import Client, filters
from pyrogram.types import Message



@Client.on_message(filters.command("check_spam"))
async def antispam(client, message):
    id = " ".join(message.command[1:])
    api = f"https://api.cas.chat/check?user_id={id}"
    session = requests.Session()
    req = session.request('get', api)
    status = req.json()['ok']
    if status == "True":
        try:
            result = req.json()['result']
            reason = result['messages']
            offenses = result['offenses']
            time_added = result['time_added']
            await message.reply(f"**User:** `{id}`\n**Is banned:** {offenses}\n**Reason:** `{reason}`\n**Time added:** {time_added}")
        except Exception as e:
            await message.reply(e)
    else:
        await message.reply("This user is safe!")
