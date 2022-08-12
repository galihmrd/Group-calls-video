import requests
from pyrogram import Client, filters


@Client.on_message(filters.command("check_spam"))
async def antispam(client, message):
    id = " ".join(message.command[1:])
    api = f"https://api.cas.chat/check?user_id={id}"
    session = requests.Session()
    req = session.request("get", api)
    status = req.json()["ok"]
    if status == True:
        try:
            result = req.json()["result"]
            reason = f"https://cas.chat/query?u={id}"
            offenses = result["offenses"]
            time_added = result["time_added"]
            await message.reply(
                f"**COMBOT ANTI SPAM**\n\n**User:** `{id}`\n**Is banned:** {offenses}\n**Reason:** [Link]({reason})\n**Time added:** {time_added}"
            )
        except Exception as e:
            await message.reply(e)
    else:
        await message.reply("Combot: This user is safe!")
