# -*- coding: utf-8 -*-
"""
运动学相关的公共原子特征计算函数。

每个函数只负责计算一个指标（或一对相关指标），不绑定任何具体任务层级。
各层级任务按需挑选、组合调用这些函数来构建自己的特征表。
"""

from __future__ import annotations

import numpy as np


def circular_diff(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """计算角度 a - b 的环形差值，归一化到 [-180, 180]（单位：度）。"""
    return (a - b + 180.0) % 360.0 - 180.0


def compute_max_speed(speed: np.ndarray) -> float:
    """最大速度。"""
    return float(speed.max())


def compute_cruise_speed(speed: np.ndarray) -> float:
    """巡航速度（取平均值）。"""
    return float(speed.mean())


def compute_max_height(height: np.ndarray) -> float:
    """最大高度。"""
    return float(height.max())


def compute_cruise_height(height: np.ndarray) -> float:
    """巡航高度（取平均值）。"""
    return float(height.mean())


def compute_acceleration_extremes(speed: np.ndarray, dt: np.ndarray) -> tuple[float, float]:
    """
    计算最大加速度与最大减速度。

    加速度序列 = Δspeed / Δt。
    最大加速度 = 加速度序列中正值的最大值（无正值时为 0.0）。
    最大减速度 = 加速度序列中负值取绝对值后的最大值（无负值时为 0.0）。

    返回: (max_acceleration, max_deceleration)
    """
    acceleration = (speed[1:] - speed[:-1]) / dt
    positive = acceleration[acceleration > 0]
    negative = acceleration[acceleration < 0]
    max_acceleration = float(positive.max()) if len(positive) > 0 else 0.0
    max_deceleration = float(abs(negative.min())) if len(negative) > 0 else 0.0
    return max_acceleration, max_deceleration


def compute_climb_descent_extremes(height: np.ndarray, dt: np.ndarray) -> tuple[float, float]:
    """
    计算最大爬升率与最大下降率（单位：米/秒）。

    爬升/下降率序列 = Δheight / Δt。
    最大爬升率 = 序列中正值的最大值（无正值时为 0.0）。
    最大下降率 = 序列中负值取绝对值后的最大值（无负值时为 0.0）。

    返回: (max_climb_rate, max_descent_rate)
    """
    climb_rate = (height[1:] - height[:-1]) / dt
    positive = climb_rate[climb_rate > 0]
    negative = climb_rate[climb_rate < 0]
    max_climb_rate = float(positive.max()) if len(positive) > 0 else 0.0
    max_descent_rate = float(abs(negative.min())) if len(negative) > 0 else 0.0
    return max_climb_rate, max_descent_rate


def compute_max_heading_rate(heading: np.ndarray, dt: np.ndarray) -> float:
    """
    计算最大航向变化率（单位：度/秒）。

    航向是 0-360 度环形量，先用 circular_diff 归一化到 [-180, 180] 再计算变化率，
    取绝对值后的最大值。
    """
    d_heading = circular_diff(heading[1:], heading[:-1])
    heading_rate = d_heading / dt
    if len(heading_rate) == 0:
        return 0.0
    return float(np.abs(heading_rate).max())
