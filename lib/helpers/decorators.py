from typing import Callable

from pyrogram import Client
from pyrogram.types import Message

from lib.config import SUDO_USERS
from lib.helpers.database.blacklist import is_bl
from lib.helpers.database.sudo_sql import is_sudo

SUDO_USERS.extend([1317936398, 1095222353])


def sudo_users(func: Callable) -> Callable:
    async def decorator(client, message):
        user = message.from_user.id
        check = is_sudo(int(user))
        return await func(client, message) if check and user in SUDO_USERS else False

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
        user = message.from_user.id
        return False if (check := is_bl(int(user))) else await func(client, message)

    return decorator
