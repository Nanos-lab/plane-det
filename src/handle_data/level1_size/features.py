# -*- coding: utf-8 -*-
"""
level1_size 层级的特征提取逻辑：组合调用 handle_data.feature_extract 中的公共原子函数，
构建该层级（大型机/小型机二分类）所需的航迹特征表。
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from ..config.config import load_config as load_root_config
from ..feature_extract import io_utils, kinematics, time_utils
from .config.config import load_config as load_level_config

_ROOT_CONFIG = load_root_config()
_LEVEL_CONFIG = load_level_config()

_COLUMNS = _ROOT_CONFIG["columns"]
_TIME_FORMAT = _ROOT_CONFIG["time"]["format"]

_MIN_POINTS = _LEVEL_CONFIG["track_features"]["min_points"]
_ROUND_DIGITS = _LEVEL_CONFIG["track_features"]["round_digits"]
_OUTPUT_COLUMNS = _LEVEL_CONFIG["track_features"]["output_columns"]

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
_OUTPUT_DIR = _PROJECT_ROOT / _LEVEL_CONFIG["paths"]["output_dir"]
_FEATURES_FILE_PATH = _OUTPUT_DIR / _LEVEL_CONFIG["paths"]["features_filename"]


def extract_track_features(df: pd.DataFrame) -> pd.Series:
    """
    从单条航迹的点迹序列中提取 level1_size 层级所需的特征。

    参数：
        df: 单条航迹的 DataFrame，包含 handle_data 顶层 columns 定义的字段。

    返回：
        pd.Series，索引为 aircraft_type 及 track_features.output_columns 中定义的特征名。

    异常：
        ValueError: 当航迹点数少于配置中的 track_features.min_points 时抛出。
    """
    time_col = _COLUMNS["time"]
    height_col = _COLUMNS["height"]
    speed_col = _COLUMNS["speed"]
    heading_col = _COLUMNS["heading"]
    aircraft_type_col = _COLUMNS["aircraft_type"]

    if len(df) < _MIN_POINTS:
        raise ValueError(f"航迹点数不足：{len(df)} < min_points({_MIN_POINTS})")

    df = df.copy()
    df[time_col] = time_utils.ensure_datetime(df[time_col], _TIME_FORMAT)
    df = df.sort_values(time_col).reset_index(drop=True)

    speed = df[speed_col].to_numpy(dtype=float)
    height = df[height_col].to_numpy(dtype=float)
    heading = df[heading_col].to_numpy(dtype=float)
    dt = time_utils.compute_dt_seconds(df[time_col])

    max_acceleration, max_deceleration = kinematics.compute_acceleration_extremes(speed, dt)
    max_climb_rate, max_descent_rate = kinematics.compute_climb_descent_extremes(height, dt)

    features = {
        "max_speed": kinematics.compute_max_speed(speed),
        "cruise_speed": kinematics.compute_cruise_speed(speed),
        "max_height": kinematics.compute_max_height(height),
        "cruise_height": kinematics.compute_cruise_height(height),
        "max_acceleration": max_acceleration,
        "max_deceleration": max_deceleration,
        "max_climb_rate": max_climb_rate,
        "max_descent_rate": max_descent_rate,
        "max_heading_rate": kinematics.compute_max_heading_rate(heading, dt),
    }

    result = {aircraft_type_col: df[aircraft_type_col].iloc[0]}
    for col in _OUTPUT_COLUMNS:
        result[col] = round(float(features[col]), _ROUND_DIGITS)

    return pd.Series(result)


def extract_features_from_tracks(df: pd.DataFrame) -> pd.DataFrame:
    """
    对包含多条航迹的原始数据批量提取 level1_size 层级特征。

    参数：
        df: 包含多条航迹（多个 id）的原始数据 DataFrame。

    返回：
        pd.DataFrame，每行对应一条有效航迹的特征，点数不足的航迹会被跳过。
    """
    id_col = _COLUMNS["id"]

    rows = []
    skipped = 0

    for _, track_df in df.groupby(id_col, sort=False):
        try:
            rows.append(extract_track_features(track_df))
        except ValueError:
            skipped += 1

    if skipped > 0:
        print(f"共跳过 {skipped} 条航迹（点数不足 {_MIN_POINTS} 点）")

    return pd.DataFrame(rows).reset_index(drop=True)


def save_features(features_df: pd.DataFrame, output_path: Path = _FEATURES_FILE_PATH) -> Path:
    """保存 level1_size 特征表，默认路径由配置中的 paths.output_dir + paths.features_filename 决定。"""
    return io_utils.save_dataframe(features_df, output_path)


def load_features(input_path: Path = _FEATURES_FILE_PATH) -> pd.DataFrame:
    """读取已保存的 level1_size 特征表，默认路径由配置中的 paths.output_dir + paths.features_filename 决定。"""
    return io_utils.load_dataframe(input_path)
