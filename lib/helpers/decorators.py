from pyrogram import Client
from typing import Callable
from pyrogram.types import Message
from lib.config import SUDO_USERS


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
