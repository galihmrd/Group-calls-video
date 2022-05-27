"""
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
"""

from typing import List, Union

from pyrogram import filters

from lib.config import COMMAND_PREFIXES


def command(commands: Union[str, List[str]]):
    return filters.command(commands, COMMAND_PREFIXES)


private_filters = (
    filters.private & ~filters.via_bot & ~filters.forwarded
)
public_filters = filters.group & ~filters.via_bot & ~filters.forwarded
