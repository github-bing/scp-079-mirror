# SCP-079-MIRROR - What will I see
# Copyright (C) 2019 SCP-079 <https://scp-079.org>
#
# This file is part of SCP-079-MIRROR.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging
from html import escape
from random import uniform
from threading import Thread
from time import sleep
from typing import Any, Callable, Union

from pyrogram import Message, MessageEntity
from pyrogram.errors import FloodWait

from .. import glovar

# Enable logging
logger = logging.getLogger(__name__)


def bold(text: Any) -> str:
    # Get a bold text
    try:
        text = str(text).strip()
        if text:
            return f"<b>{escape(text)}</b>"
    except Exception as e:
        logger.warning(f"Bold error: {e}", exc_info=True)

    return ""


def code(text: Any) -> str:
    # Get a code text
    try:
        text = str(text).strip()
        if text:
            return f"<code>{escape(text)}</code>"
    except Exception as e:
        logger.warning(f"Code error: {e}", exc_info=True)

    return ""


def code_block(text: Any) -> str:
    # Get a code block text
    try:
        text = str(text).rstrip()
        if text:
            return f"<pre>{escape(text)}</pre>"
    except Exception as e:
        logger.warning(f"Code block error: {e}", exc_info=True)

    return ""


def general_link(text: Union[int, str], link: str) -> str:
    # Get a general link
    result = ""
    try:
        text = str(text).strip()
        link = link.strip()
        if text and link:
            result = f'<a href="{link}">{escape(text)}</a>'
    except Exception as e:
        logger.warning(f"General link error: {e}", exc_info=True)

    return result


def get_entity_text(message: Message, entity: MessageEntity) -> str:
    # Get a message's entity text
    result = ""
    try:
        text = get_text(message)

        if not text or not entity:
            return ""

        offset = entity.offset
        length = entity.length
        text = text.encode("utf-16-le")
        result = text[offset * 2:(offset + length) * 2].decode("utf-16-le")
    except Exception as e:
        logger.warning(f"Get entity text error: {e}", exc_info=True)

    return result


def get_text(message: Message) -> str:
    # Get message's text
    text = ""
    try:
        the_text = message.text or message.caption
        if the_text:
            text += the_text
    except Exception as e:
        logger.warning(f"Get text error: {e}", exc_info=True)

    return text


def lang(text: str) -> str:
    # Get the text
    result = ""
    try:
        result = glovar.lang.get(text, text)
    except Exception as e:
        logger.warning(f"Lang error: {e}", exc_info=True)

    return result


def mention_id(uid: int) -> str:
    # Get a ID mention string
    result = ""
    try:
        result = general_link(f"{uid}", f"tg://user?id={uid}")
    except Exception as e:
        logger.warning(f"Mention id error: {e}", exc_info=True)

    return result


def thread(target: Callable, args: tuple) -> bool:
    # Call a function using thread
    try:
        t = Thread(target=target, args=args)
        t.daemon = True
        t.start()

        return True
    except Exception as e:
        logger.warning(f"Thread error: {e}", exc_info=True)

    return False


def wait_flood(e: FloodWait) -> bool:
    # Wait flood secs
    try:
        sleep(e.x + uniform(0.5, 1.0))
        return True
    except Exception as e:
        logger.warning(f"Wait flood error: {e}", exc_info=True)

    return False
