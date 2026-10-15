# -*- coding: utf-8 -*-
"""
level1_size 层级的数据集划分逻辑：将具体机型映射为大型机/小型机二分类标签，
并按分层抽样划分为训练集和测试集。
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split

from ..feature_extract import io_utils
from .config.config import load_config

_CONFIG = load_config()

_AIRCRAFT_TYPE_COL = _CONFIG["columns"]["aircraft_type"]
_CATEGORY_COL = _CONFIG["columns"]["category"]
_LARGE_TYPES = set(_CONFIG["category_mapping"]["large"])
_SMALL_TYPES = set(_CONFIG["category_mapping"]["small"])

_TEST_SIZE = _CONFIG["split"]["test_size"]
_RANDOM_SEED = _CONFIG["split"]["random_seed"]

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
_OUTPUT_DIR = _PROJECT_ROOT / _CONFIG["paths"]["output_dir"]


def map_to_category(aircraft_type: str) -> int:
    """
    将具体机型映射为大类标签：1=大型机，0=小型机。

    异常：
        ValueError: 当机型不在配置的 category_mapping 中时抛出。
    """
    if aircraft_type in _LARGE_TYPES:
        return 1
    if aircraft_type in _SMALL_TYPES:
        return 0
    raise ValueError(f"未知机型，未在 category_mapping 中配置: {aircraft_type!r}")


def split_dataset(features_df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    将特征表划分为训练集和测试集（分层抽样，按 category 分层）。

    参数：
        features_df: 包含 aircraft_type 列及若干特征列的 DataFrame。

    返回：
        (train_df, test_df)，均不含 aircraft_type 列，只保留特征列 + category 列。
    """
    df = features_df.copy()
    df[_CATEGORY_COL] = df[_AIRCRAFT_TYPE_COL].apply(map_to_category)
    df = df.drop(columns=[_AIRCRAFT_TYPE_COL])

    train_df, test_df = train_test_split(
        df,
        test_size=_TEST_SIZE,
        random_state=_RANDOM_SEED,
        stratify=df[_CATEGORY_COL],
    )

    return train_df.reset_index(drop=True), test_df.reset_index(drop=True)


def save_split(
    train_df: pd.DataFrame,
    test_df: pd.DataFrame,
    output_dir: Path = _OUTPUT_DIR,
) -> tuple[Path, Path]:
    """
    保存划分后的训练集和测试集，默认目录由配置中的 paths.output_dir 决定。

    返回：
        (train_path, test_path)
    """
    output_dir = Path(output_dir)
    train_path = io_utils.save_dataframe(train_df, output_dir / "train.csv")
    test_path = io_utils.save_dataframe(test_df, output_dir / "test.csv")
    return train_path, test_path
