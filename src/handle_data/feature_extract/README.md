# feature_extract 公共特征计算函数

公共、与具体任务层级无关的原子函数，供各层级任务（如 `level1_size`）组合调用，构建自己需要的特征表。

## time_utils.py

- `ensure_datetime(series, time_format)`：防御性时间转换，若已是 datetime 类型则不转换
- `compute_dt_seconds(time_series)`：计算已排序时间序列中相邻点的时间差（秒），使用 `Timedelta.total_seconds()`，不依赖 datetime64 底层精度

## kinematics.py

运动学原子特征计算，每个函数只负责一个（或一对相关）指标：

| 函数 | 说明 |
| --- | --- |
| `compute_max_speed(speed)` | 最大速度 |
| `compute_cruise_speed(speed)` | 巡航速度（均值） |
| `compute_max_height(height)` | 最大高度 |
| `compute_cruise_height(height)` | 巡航高度（均值） |
| `compute_acceleration_extremes(speed, dt)` | 返回 (最大加速度, 最大减速度) |
| `compute_climb_descent_extremes(height, dt)` | 返回 (最大爬升率, 最大下降率)，单位米/秒 |
| `compute_max_heading_rate(heading, dt)` | 最大航向变化率，单位度/秒，内部做环形角度修正 |

无正值/负值时，对应的极值返回 `0.0`。

## io_utils.py

- `save_dataframe(df, output_path)`：保存为 CSV（utf-8-sig），自动创建父目录
- `load_dataframe(input_path)`：从 CSV 读取（utf-8-sig）

路径均由调用方传入，不假设固定目录结构。

## 新增特征时如何扩展

在 `kinematics.py`（或新建同类文件）里添加一个新的原子函数即可，各层级的 `features.py` 按需调用。
