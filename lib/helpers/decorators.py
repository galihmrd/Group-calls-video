from typing import Callable

from pyrogram import Client
from pyrogram.types import Message

from lib.config import SUDO_USERS
from database.database_banned_sql import check_banned


def sudo_users(func: Callable) -> Callable:
    async def decorator(client, message):
        if message.from_user.id in SUDO_USERS:
            return await func(client, message)

    return decorator


def errors(func: Callable) -> Callable:
    async def decorator(client: Client, message: Message):
        try:
            return await func(client, message)
        except Exception as e:
            await message.reply(f"{type(e).__name__}: {e}")

    return decorator


def blacklist_users(func: Callable) -> Callable:
    async def decorator(filter, client, message):
        check = check_banned(message)
        if check:
            return False
        else:
            return await func(filter, client, message)

    return decorator
