from pyrogram.types import Message
from pyrogram import Client, filters
from youtube_search import YoutubeSearch
from lib.helpers.decorators import blacklist_users


@Client.on_message(filters.command("search"))
@blacklist_users
async def ytsearch(client, mesaage):
    try:
       if len(message.command) <2:
           await message.reply("Give me some title")
           return
       input = " ".join(message.command[1:])
       msg = await message.reply("`searching...`")
       results = YoutubeSearch(input, max_results=4).to_dict()
       i = 0
       text = " "
       while i < 4:
           text += f"**Title:** {results[i]['title']}\n"
           text += f"**Duration:** {results[i]['duration']}\n"
           text += f"**Views:** {results[i]['views']}\n"
           text += f"**Channel:** {results[i]['channel']}\n"
           text += f"**Url:** [Klik disini](https://youtube.com{results[i]['url_suffix']})\n\n"
           i += 1
       await msg.edit(text, disable_web_page_preview=True)
    except BaseException:
       pass
