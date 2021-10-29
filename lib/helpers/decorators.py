from typing import Callable

from pyrogram import Client
from pyrogram.types import Message

from lib.config import SUDO_USERS
from database.blacklist import is_bl


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
    async def decorator(client, message):
        check = is_bl(message)
        if check is not None:
            return await func(client, message)

    return decorator
