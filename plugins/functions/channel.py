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
from json import dumps
from typing import List, Union

from pyrogram import Client

from .. import glovar
from .etc import code, code_block, lang, thread
from .telegram import send_message

# Enable logging
logger = logging.getLogger(__name__)


def exchange_to_hide(client: Client) -> bool:
    # Let other bots exchange data in the hide channel instead
    try:
        glovar.should_hide = True
        share_data(
            client=client,
            receivers=["EMERGENCY"],
            action="backup",
            action_type="hide",
            data=True
        )

        # Send debug message
        text = (f"{lang('project')}{lang('colon')}{code(glovar.sender)}\n"
                f"{lang('issue')}{lang('colon')}{code(lang('exchange_invalid'))}\n"
                f"{lang('auto_fix')}{lang('colon')}{code(lang('protocol_1'))}\n")
        thread(send_message, (client, glovar.critical_channel_id, text))

        return True
    except Exception as e:
        logger.warning(f"Exchange to hide error: {e}", exc_info=True)

    return False


def format_data(sender: str, receivers: List[str], action: str, action_type: str,
                data: Union[bool, dict, int, str] = None) -> str:
    # See https://scp-079.org/exchange/
    text = ""
    try:
        data = {
            "from": sender,
            "to": receivers,
            "action": action,
            "type": action_type,
            "data": data
        }
        text = code_block(dumps(data, indent=4))
    except Exception as e:
        logger.warning(f"Format data error: {e}", exc_info=True)

    return text


def share_data(client: Client, receivers: List[str], action: str, action_type: str,
               data: Union[bool, dict, int, str] = None) -> bool:
    # Use this function to share data in the channel
    try:
        thread(
            target=share_data_thread,
            args=(client, receivers, action, action_type, data)
        )

        return True
    except Exception as e:
        logger.warning(f"Share data error: {e}", exc_info=True)

    return False


def share_data_thread(client: Client, receivers: List[str], action: str, action_type: str,
                      data: Union[bool, dict, int, str] = None) -> bool:
    # Share data thread
    try:
        if glovar.sender in receivers:
            receivers.remove(glovar.sender)

        if not receivers:
            return True

        if glovar.should_hide:
            channel_id = glovar.hide_channel_id
        else:
            channel_id = glovar.exchange_channel_id

        text = format_data(
            sender=glovar.sender,
            receivers=receivers,
            action=action,
            action_type=action_type,
            data=data
        )
        result = send_message(client, channel_id, text)

        # Sending failed due to channel issue
        if result is False and not glovar.should_hide:
            # Use hide channel instead
            exchange_to_hide(client)
            thread(share_data, (client, receivers, action, action_type, data))

        return True
    except Exception as e:
        logger.warning(f"Share data thread error: {e}", exc_info=True)

    return False
