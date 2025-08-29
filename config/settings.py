from __future__ import annotations

import os
from pathlib import Path

PKG_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DATASET_PATH = PKG_ROOT / "data" / "static" / "ac_data_only_top_5.csv"
DATASET_PATH = Path(os.getenv("SHOPASSIST_DATASET_PATH", DEFAULT_DATASET_PATH))

STAGE0_SYSTEM_MESSAGE = PKG_ROOT / "src" / "prompts" / "stage0" / "system_message.md"
STAGE1_TOOLS = PKG_ROOT / "src" / "prompts" / "stage0" / "tools.md"
STAGE1_TOOLS_CHOICE = PKG_ROOT / "src" / "prompts" / "stage0" / "tools_choice.md"

STAGE1_SYSTEM_MESSAGE = PKG_ROOT / "src" / "prompts" / "stage1" / "system_message.md"
EXTRACT_DICT_SYS_MSG = (
    PKG_ROOT / "src" / "prompts" / "stage1" / "extract_dictionary_system_message.md"
)
STAGE2_SYSTEM_MESSAGE = PKG_ROOT / "src" / "prompts" / "stage2" / "system_message.md"

STAGE3_SYSTEM_MESSAGE = PKG_ROOT / "src" / "prompts" / "stage3" / "system_message.md"
