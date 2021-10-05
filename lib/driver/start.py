'''
tg-stream-video, An Telegram Bot Project
Copyright (c) 2021 GalihMrd <https://github.com/Imszy17>
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.
You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>
'''

from pyrogram.types import Message
from pyrogram.types import InlineKeyboardMarkup
from pyrogram.types import InlineKeyboardButton
from pyrogram import Client, filters

from lib.config import USERNAME_BOT


HELP_PLAY = """**[HELP MESSAGE]**
**>> Description:** ```to streaming video in video chat group/channel```

**[GUIDE]**
**>> Group:** ```/play [reply to video/audio/give youtube url]```
**>> Channel:** ```/play [channel] [reply to video/audio/give youtube url]```

**>> Note:** ```To stream in channel stream you must replace chat title to Channel ID```
"""

HELP_PAUSE = """**[HELP MESSAGE]**
**>> Description:** ```To pause stream in video chat grouo/channel```

**[GUIDE]**
**>> Group:** ```/pause```
**>> Channel:** ```/pause [channel]```

**>> Note:** ```Replace chat title to pause channel stream```
"""

HELP_RESUME = """**[HELP MESSAGE]**
**>> Description:** ```To resume stream in video chat grouo/channel```

**[GUIDE]**
**>> Group:** ```/resume```
**>> Channel:** ```/resume [channel]```

**>> Note:** ```Replace chat title to resume channel stream```
"""

HELP_STOP = """**[HELP MESSAGE]**
**>> Description:** ```To stop stream in video chat grouo/channel```

**[GUIDE]**
**>> Group:** ```/stop```
**>> Channel:** ```/stop [channel]```

**>> Note:** ```Replace chat title to stop channel stream```
"""

START_MESSAGE = """ **I'M ALIVE**
"""


@Client.on_callback_query(filters.regex(pattern=r"^(play|pause|resume|stop)$"))
async def callback(b, cb):
    help_type = cb.matches[0].group(1)
    if help_type == "play":
        await cb.message.edit(HELP_PLAY)
    elif help_type == "pause":
        await cb.message.edit(HELP_PAUSE)
    elif help_type == "resume":
        await cb.message.edit(HELP_RESUME)
    elif help_type == "stop":
        await cb.message.edit(HELP_STOP)


@Client.on_message(filters.command("help"))
async def help(client, message):
    marr = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("PLAY HELP", "play"),
                InlineKeyboardButton("PAUSE HELP", "pause"),
                InlineKeyboardButton("RESUME HELP", "resume"),
            ],
            [InlineKeyboardButton("STOP HELP", "stop")],
        ]
    )
    await message.reply(
        "**Command help with description**",
        reply_markup=marr
    )


@Client.on_message(filters.command("start"))
async def start(client, message):
    await message.reply(START_MESSAGE)
