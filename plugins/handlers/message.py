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
import re

from pyrogram import Client, Filters, Message

from .. import glovar
from ..functions.etc import code, code_block, general_link, get_entity_text, get_text, lang, thread
from ..functions.filters import from_user, github_bot, hide_channel
from ..functions.receive import receive_text_data
from ..functions.telegram import read_history, read_mention, send_message

# Enable logging
logger = logging.getLogger(__name__)


@Client.on_message(Filters.incoming & Filters.channel & ~Filters.command(glovar.all_commands, glovar.prefix)
                   & hide_channel, group=-1)
def exchange_emergency(client: Client, message: Message) -> bool:
    # Sent emergency channel transfer request
    try:
        # Read basic information
        data = receive_text_data(message)

        if not data:
            return True

        sender = data["from"]
        receivers = data["to"]
        action = data["action"]
        action_type = data["type"]
        data = data["data"]

        if "EMERGENCY" not in receivers:
            return True

        if action != "backup":
            return True

        if action_type != "hide":
            return True

        if data is True:
            glovar.should_hide = data
        elif data is False and sender == "MANAGE":
            glovar.should_hide = data

        project_text = general_link(glovar.project_name, glovar.project_link)
        hide_text = (lambda x: lang("enabled") if x else "disabled")(glovar.should_hide)
        text = (f"{lang('project')}{lang('colon')}{project_text}\n"
                f"{lang('action')}{lang('colon')}{code(lang('transfer_channel'))}\n"
                f"{lang('emergency_channel')}{lang('colon')}{code(hide_text)}\n")
        thread(send_message, (client, glovar.debug_channel_id, text))

        return True
    except Exception as e:
        logger.warning(f"Exchange emergency error: {e}", exc_info=True)

    return False


@Client.on_message(Filters.incoming & Filters.bot
                   & from_user & github_bot)
def forward(client: Client, message: Message) -> bool:
    # Forward messages from GitHub bot to the channel
    try:
        origin_text = get_text(message)

        if not re.search("new commit.? to .*:.*:", origin_text):
            return True

        link_list = []

        for en in message.entities:
            if en.url:
                the_text = get_entity_text(message, en)
                the_link = en.url
                link_list.append((the_text, the_link))

        if len(link_list) <= 1:
            return True

        commit_unit = link_list[0]
        commit_unit_text = commit_unit[0]
        compare_link = commit_unit[1]
        commit_count = commit_unit_text.split(" new ")[0]
        commit_line = origin_text.split("\n\n")[0]
        commit_project_branch = commit_line.split(" to ")[1].split(":")
        commit_project = commit_project_branch[0]
        commit_branch = commit_project_branch[1]

        text = (f"{lang('update_repo')}{lang('colon')}{code(commit_project)}\n"
                f"{lang('update_branch')}{lang('colon')}{code(commit_branch)}\n"
                f"{lang('commit_count')}{lang('colon')}{general_link(commit_count, compare_link)}\n")

        link_list = link_list[1:]
        origin_text = origin_text.split("\n\n")[1]
        origin_text = re.sub(
            pattern=" by .*$",
            repl="#######",
            string=origin_text,
            flags=re.M
        )
        origin_text_list = origin_text.split("#######")
        i = 0
        for link_unit in link_list:
            commit_hash = link_unit[0]
            commit_link = link_unit[1]
            commit_message = origin_text_list[i].strip().split(": ")[1]
            text += (f"{general_link(commit_hash, commit_link)}：" + "-" * 24 + "\n\n"
                     f"{code_block(commit_message)}\n\n")
            i += 1

        thread(send_message, (client, glovar.github_channel_id, text))

        return True
    except Exception as e:
        logger.warning(f"Forward error: {e}", exc_info=True)

    return False


@Client.on_message(Filters.incoming & ~Filters.private & Filters.mentioned, group=1)
def mark_mention(client: Client, message: Message) -> bool:
    # Mark mention as read
    try:
        if not message.chat:
            return True

        cid = message.chat.id
        thread(read_mention, (client, cid))

        return True
    except Exception as e:
        logger.warning(f"Mark mention error: {e}", exc_info=True)

    return False


@Client.on_message(Filters.incoming & (~Filters.private | Filters.bot), group=2)
def mark_message(client: Client, message: Message) -> bool:
    # Mark messages as read
    try:
        if not message.chat:
            return True

        cid = message.chat.id
        thread(read_history, (client, cid))

        return True
    except Exception as e:
        logger.warning(f"Mark message error: {e}", exc_info=True)

    return False
