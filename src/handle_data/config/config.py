# -*- coding: utf-8 -*-
"""
handle_data 模块的配置加载逻辑。

负责读取 config.yaml 并提供给模块内其他代码使用，具体加载/校验逻辑随模块实现逐步补充。
"""

from __future__ import annotations

from pathlib import Path

import yaml

CONFIG_PATH = Path(__file__).resolve().parent / "config.yaml"


def load_config(path: Path = CONFIG_PATH) -> dict:
    """读取 config.yaml，返回配置字典。"""
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)
