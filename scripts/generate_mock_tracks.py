# -*- coding: utf-8 -*-
"""
生成模拟航迹点迹数据，用于在没有真实数据时跑通项目流程。

规则（与用户确认过）：
- 每个机型生成 10 条航迹，每条航迹 20 个点
- 采样时间间隔随机（每条航迹内，点与点之间的间隔在合理范围内随机）
- id 仅用于区分不同航迹，没有其他含义
- 单条航迹内部运动学要连贯（经纬度/高度/速度/航向逐点平滑演化，不乱跳）
- 航迹之间互不关联，起始位置/时间/状态不做跨航迹的统一限制
- 数据本身不追求对应真实机型性能，仅用于验证流程

输出：data/raw/prepared.csv，列为 id,time,lon,lat,height,speed,heading,aircraft_type
"""

from __future__ import annotations

import csv
import math
import random
from datetime import datetime, timedelta
from pathlib import Path

AIRCRAFT_TYPES = [
    "B-1B", "B-52H", "C-130", "E-2D", "E-3", "EA-18G",
    "F-15", "F-16", "F-22", "F-35A", "F-35B", "F-35C", "F/A-18",
    "KC-130", "KC-135", "KC-46", "MQ-4C", "P-8A",
    "RC-135S", "RC-135UVW", "RQ-4", "U-2",
    "庞巴迪60X", "庞巴迪6500", "雅典娜RS",
]

TRACKS_PER_TYPE = 10
POINTS_PER_TRACK = 20

OUTPUT_PATH = Path(__file__).resolve().parent.parent / "data" / "raw" / "prepared.csv"

EARTH_RADIUS_KM = 6371.0


def random_start_time() -> datetime:
    """起始时间不做跨航迹限制，在一个宽泛的时间窗口内随机取值。"""
    base = datetime(2020, 1, 1)
    offset_days = random.uniform(0, 365 * 5)
    offset_seconds = random.uniform(0, 86400)
    return base + timedelta(days=offset_days, seconds=offset_seconds)


def move_point(lon: float, lat: float, heading_deg: float, distance_km: float) -> tuple[float, float]:
    """沿给定航向、给定距离（km）从当前经纬度推进一步，返回新的经纬度。"""
    heading_rad = math.radians(heading_deg)
    lat_rad = math.radians(lat)

    delta_lat = (distance_km * math.cos(heading_rad)) / EARTH_RADIUS_KM
    delta_lon = (distance_km * math.sin(heading_rad)) / (EARTH_RADIUS_KM * math.cos(lat_rad) + 1e-9)

    new_lat = lat + math.degrees(delta_lat)
    new_lon = lon + math.degrees(delta_lon)
    return new_lon, new_lat


def generate_track(track_id: str, aircraft_type: str) -> list[dict]:
    """生成单条航迹的 20 个点，保证运动学连贯（不乱跳）。"""
    lon = random.uniform(-180.0, 180.0)
    lat = random.uniform(-60.0, 60.0)
    height = random.uniform(500.0, 15000.0)
    speed = random.uniform(150.0, 1200.0)
    heading = random.uniform(0.0, 360.0)

    current_time = random_start_time()
    rows = []

    for _ in range(POINTS_PER_TRACK):
        rows.append({
            "id": track_id,
            "time": current_time.strftime("%Y-%m-%d %H:%M:%S"),
            "lon": round(lon, 6),
            "lat": round(lat, 6),
            "height": round(height, 1),
            "speed": round(speed, 1),
            "heading": round(heading % 360.0, 2),
            "aircraft_type": aircraft_type,
        })

        # 采样间隔随机，但在合理范围内（雷达/数据链常见量级）
        interval_seconds = random.uniform(2.0, 10.0)
        current_time += timedelta(seconds=interval_seconds)

        # 航向小幅随机漂移，避免剧烈转向造成的"乱跳"
        heading += random.uniform(-8.0, 8.0)
        heading %= 360.0

        # 速度小幅随机漂移
        speed += random.uniform(-15.0, 15.0)
        speed = max(50.0, min(1300.0, speed))

        # 高度小幅随机漂移
        height += random.uniform(-80.0, 80.0)
        height = max(0.0, min(20000.0, height))

        # 按当前速度与时间间隔推进位置（速度假设单位为节，换算为 km）
        distance_km = (speed * 0.514444) * interval_seconds / 1000.0
        lon, lat = move_point(lon, lat, heading, distance_km)
        lat = max(-85.0, min(85.0, lat))

    return rows


def main() -> None:
    random.seed(42)
    all_rows: list[dict] = []
    track_counter = 1

    for aircraft_type in AIRCRAFT_TYPES:
        for _ in range(TRACKS_PER_TYPE):
            track_id = f"{track_counter:04d}"
            all_rows.extend(generate_track(track_id, aircraft_type))
            track_counter += 1

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_PATH.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["id", "time", "lon", "lat", "height", "speed", "heading", "aircraft_type"],
        )
        writer.writeheader()
        writer.writerows(all_rows)

    print(f"已生成 {len(all_rows)} 行模拟数据，共 {track_counter - 1} 条航迹，输出至: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
