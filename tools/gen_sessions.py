# pylint: disable=invalid-name, missing-module-docstring
#
# Copyright (C) 2020-2021 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/UsergeTeam/Userge/blob/master/LICENSE >
#
# All rights reserved.

import asyncio

from pyrogram import Client
from pyrogram.errors import UserIsBot

from lib.config import API_HASH, API_ID


async def genStrSession() -> None:  # pylint: disable=missing-function-docstring
    async with Client(
        "Userge",
        api_id=int(API_ID) or input("Enter Telegram APP ID: "),
        api_hash=API_HASH or input("Enter Telegram API HASH: "),
    ) as userge:
        print("\nprocessing...")
        doneStr = "sent to saved messages!"
        try:
            await userge.send_message(
                "me", f"#STRING_SESSION\n\n```{await userge.export_session_string()}```"
            )
        except UserIsBot:
            doneStr = "successfully printed!"
            print(await userge.export_session_string())
        print(f"Done !, session string has been {doneStr}")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(genStrSession())
