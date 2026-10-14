# -*- coding: utf-8 -*-
"""
时间相关的公共工具函数：时间列的防御性转换、排序、逐点时间差计算。
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def ensure_datetime(series: pd.Series, time_format: str) -> pd.Series:
    """若 series 不是 datetime 类型，则按 time_format 转换为 datetime。"""
    if pd.api.types.is_datetime64_any_dtype(series):
        return series
    return pd.to_datetime(series, format=time_format)


def compute_dt_seconds(time_series: pd.Series) -> np.ndarray:
    """
    计算已排序时间序列中相邻点的时间差（秒）。

    使用 Timedelta.total_seconds()，不依赖 datetime64 的底层精度（ns/us/ms 等）。

    返回长度为 len(time_series) - 1 的数组。
    """
    t1 = time_series.iloc[1:].reset_index(drop=True)
    t2 = time_series.iloc[:-1].reset_index(drop=True)
    return (t1 - t2).dt.total_seconds().to_numpy()
