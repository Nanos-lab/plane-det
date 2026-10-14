# -*- coding: utf-8 -*-
"""level1_size 模块的配置加载逻辑。"""

from __future__ import annotations

from pathlib import Path

import yaml

CONFIG_PATH = Path(__file__).resolve().parent / "config.yaml"


def load_config(path: Path = CONFIG_PATH) -> dict:
    """读取 config.yaml，返回配置字典。"""
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)
