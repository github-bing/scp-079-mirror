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
from typing import Dict, List, Union

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.WARNING,
    filename='log',
    filemode='w'
)
logger = logging.getLogger(__name__)

# Read data from config.ini

# [basic]
prefix: List[str] = []
prefix_str: str = "/!"

# [bots]
github_id: int = 0

# [channels]
critical_channel_id: int = 0
debug_channel_id: int = 0
exchange_channel_id: int = 0
github_channel_id: int = 0
hide_channel_id: int = 0
test_group_id: int = 0

# [custom]
backup: Union[bool, str] = ""
project_link: str = ""
project_name: str = ""
zh_cn: Union[bool, str] = ""

try:
    config = RawConfigParser()
    config.read("config.ini")
    # [basic]
    prefix = list(config["basic"].get("prefix", prefix_str))
    # [bots]
    github_id = int(config["bots"].get("github_id", github_id))
    # [channels]
    critical_channel_id = int(config["channels"].get("critical_channel_id", critical_channel_id))
    debug_channel_id = int(config["channels"].get("debug_channel_id", debug_channel_id))
    exchange_channel_id = int(config["channels"].get("exchange_channel_id", exchange_channel_id))
    github_channel_id = int(config["channels"].get("github_channel_id", github_channel_id))
    hide_channel_id = int(config["channels"].get("hide_channel_id", hide_channel_id))
    test_group_id = int(config["channels"].get("test_group_id", test_group_id))
    # [custom]
    backup = config["custom"].get("backup", backup)
    backup = eval(backup)
    project_link = config["custom"].get("project_link", project_link)
    project_name = config["custom"].get("project_name", project_name)
    zh_cn = config["custom"].get("zh_cn", zh_cn)
    zh_cn = eval(zh_cn)
except Exception as e:
    logger.warning(f"Read data from config.ini error: {e}", exc_info=True)

# Check
if (prefix == []
        or github_id == 0
        or github_channel_id == 0
        or backup not in {False, True}
        or zh_cn not in {False, True}):
    logger.critical("No proper settings")
    raise SystemExit("No proper settings")

# Languages
lang: Dict[str, str] = {
    # Admin
    "admin": (zh_cn and "管理员") or "Admin",
    # Basic
    "colon": (zh_cn and "：") or ": ",
    "version": (zh_cn and "版本") or "Version",
    # Emergency
    "issue": (zh_cn and "发现状况") or "Issue",
    "exchange_invalid": (zh_cn and "数据交换频道失效") or "Exchange Channel Invalid",
    "auto_fix": (zh_cn and "自动处理") or "Auto Fix",
    "protocol_1": (zh_cn and "启动 1 号协议") or "Initiate Protocol 1",
    "transfer_channel": (zh_cn and "频道转移") or "Transfer Channel",
    "emergency_channel": (zh_cn and "应急频道") or "Emergency Channel",
    # Special
    "update_repo": (zh_cn and "更新项目") or "Repo",
    "update_branch": (zh_cn and "项目分支") or "Branch",
    "commit_count": (zh_cn and "提交数量") or "Commit"
}

# Init

all_commands: List[str] = [
    "version"
]

sender: str = "MIRROR"

should_hide: bool = False

version: str = "0.0.5"

# Start program
copyright_text = (f"SCP-079-{sender} v{version}, Copyright (C) 2019 SCP-079 <https://scp-079.org>\n"
                  "Licensed under the terms of the GNU General Public License v3 or later (GPLv3+)\n")
print(copyright_text)
