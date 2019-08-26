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
from configparser import RawConfigParser
from typing import List

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.WARNING,
    filename='log',
    filemode='w'
)
logger = logging.getLogger(__name__)

# Init
all_commands: List[str] = [
    "version"
]

sender: str = "MIRROR"

should_hide: bool = False

version: str = "0.0.1"

# Read data from config.ini

# [basic]
prefix: List[str] = []
prefix_str: str = "/!"

# [bots]
github_id: int = 0

# [channels]
critical_channel_id: int = 0
exchange_channel_id: int = 0
github_channel_id: int = 0
hide_channel_id: int = 0
test_group_id: int = 0

try:
    config = RawConfigParser()
    config.read("config.ini")
    # [basic]
    prefix = list(config["basic"].get("prefix", prefix_str))
    # [bots]
    github_id = int(config["bots"].get("github_id", github_id))

    # [channels]
    critical_channel_id = int(config["channels"].get("critical_channel_id", critical_channel_id))
    exchange_channel_id = int(config["channels"].get("exchange_channel_id", exchange_channel_id))
    github_channel_id = int(config["channels"].get("github_channel_id", github_channel_id))
    hide_channel_id = int(config["channels"].get("hide_channel_id", hide_channel_id))
    test_group_id = int(config["channels"].get("test_group_id", test_group_id))
except Exception as e:
    logger.warning(f"Read data from config.ini error: {e}", exc_info=True)

# Check
if (prefix == []
        or github_id == 0
        or critical_channel_id == 0
        or exchange_channel_id == 0
        or github_channel_id == 0
        or hide_channel_id == 0
        or test_group_id == 0):
    logger.critical("No proper settings")
    raise SystemExit("No proper settings")

# Start program
copyright_text = (f"SCP-079-{sender} v{version}, Copyright (C) 2019 SCP-079 <https://scp-079.org>\n"
                  "Licensed under the terms of the GNU General Public License v3 or later (GPLv3+)\n")
print(copyright_text)
