# -*- coding: utf-8 -*-
"""
文件 IO 公共函数：特征表的保存与读取。路径由调用方传入，不假设固定目录结构。
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


def save_dataframe(df: pd.DataFrame, output_path: Path) -> Path:
    """将 DataFrame 保存为 CSV 文件（utf-8-sig 编码），自动创建父目录。"""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False, encoding="utf-8-sig")
    return output_path


def load_dataframe(input_path: Path) -> pd.DataFrame:
    """从 CSV 文件读取 DataFrame（utf-8-sig 编码）。"""
    return pd.read_csv(Path(input_path), encoding="utf-8-sig")
