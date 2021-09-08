from pyrogram import filters
from typing import List, Union
from lib.config import COMMAND_PREFIXES

def command(commands: Union[str, List[str]]):
    return filters.command(commands, COMMAND_PREFIXES)

private_filters = filters.private & ~ filters.edited \
    & ~ filters.via_bot & ~ filters.forwarded
public_filters = filters.group & ~ filters.edited & \
    ~ filters.via_bot & ~ filters.forwarded
