from pyrogram import Client, idle
from config import API_ID, API_HASH, BOT_TOKEN
from player.videoplayer import app

bot = Client(
    ":memory:",
    API_ID,
    API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="player"),
)

bot.start()
app.start()
idle()
