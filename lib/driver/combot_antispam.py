import requests
import lib.helpers.database.blacklist as db
from pyrogram import Client, filters


@Client.on_message(filters.new_chat_members)
async def antispam(client, message):
    id = message.from_user.id
    mention = message.from_user.mention
    chid = message.chat.id
    api = f"https://api.cas.chat/check?user_id={id}"
    session = requests.Session()
    req = session.request("get", api)
    status = req.json()["ok"]
    await message.delete()
    if status == True:
        try:
            result = req.json()["result"]
            reason = f"https://cas.chat/query?u={id}"
            offenses = result["offenses"]
            time_added = result["time_added"]
            await message.reply(
                f"**COMBOT ANTI SPAM**\n\n**User:** {mention}\n**ID:** `{id}`\n**Reason:** [Link]({reason})\n**Time added:** {time_added}"
            )
            try:
                await client.ban_chat_member(chid, id)
                if db.is_bl(id):
                    return None
                else:
                    db.blacklist(int(id))
            except BaseException:
                pass
        except Exception as e:
            await message.reply(e)
    else:
        await message.reply(f"**Combot Check:** {mention} This user is safe!")
