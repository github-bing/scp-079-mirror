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

from pyrogram import Filters, Message

from .. import glovar

# Enable logging
logger = logging.getLogger(__name__)


def is_exchange_channel(_, message: Message) -> bool:
    # Check if the message is sent from the exchange channel
    try:
        if message.chat:
            cid = message.chat.id
            if glovar.should_hide:
                if cid == glovar.hide_channel_id:
                    return True
            elif cid == glovar.exchange_channel_id:
                return True
    except Exception as e:
        logger.warning(f"Is exchange channel error: {e}", exc_info=True)

    return False


def is_from_user(_, message: Message) -> bool:
    # Check if the message is sent from a user
    try:
        if message.from_user:
            return True
    except Exception as e:
        logger.warning(f"Is from user error: {e}", exc_info=True)

    return False


def is_github_bot(_, message: Message) -> bool:
    # Check if the message is sent from the github bot
    try:
        if message.from_user:
            uid = message.from_user.id
            if uid == glovar.github_id:
                return True
    except Exception as e:
        logger.warning(f"Is github bot error: {e}", exc_info=True)

    return False


def is_hide_channel(_, message: Message) -> bool:
    # Check if the message is sent from the hide channel
    try:
        if message.chat:
            cid = message.chat.id
            if cid == glovar.hide_channel_id:
                return True
    except Exception as e:
        logger.warning(f"Is hide channel error: {e}", exc_info=True)

    return False


def is_test_group(_, message: Message) -> bool:
    # Check if the message is sent from the test group
    try:
        if message.chat:
            cid = message.chat.id
            if cid == glovar.test_group_id:
                return True
    except Exception as e:
        logger.warning(f"Is test group error: {e}", exc_info=True)

    return False


exchange_channel = Filters.create(
    func=is_exchange_channel,
    name="Exchange Channel"
)

from_user = Filters.create(
    func=is_from_user,
    name="From User"
)

github_bot = Filters.create(
    func=is_github_bot,
    name="GitHub Bot"
)

hide_channel = Filters.create(
    func=is_hide_channel,
    name="Hide Channel"
)

test_group = Filters.create(
    func=is_test_group,
    name="Test Group"
)
