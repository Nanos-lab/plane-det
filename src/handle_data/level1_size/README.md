# level1_size 层级模块

## 用途

第一层级分类任务：将航迹对应的机型划分为大型机（1）/小型机（0）二分类。

## 目录结构

```
level1_size/
├── __init__.py
├── config/
│   ├── __init__.py
│   ├── config.yaml   # 该层级专属配置
│   └── config.py
├── features.py          # 调用 feature_extract 公共函数，构建该层级特征表
├── dataset.py            # 机型->大类映射 + 数据集划分（分层抽样）
└── README.md              # 本文件
```

## features.py

- `extract_track_features(df)`：单条航迹 -> 一行特征 Series（aircraft_type + 9 个特征）
- `extract_features_from_tracks(df)`：批量提取多条航迹特征，跳过点数不足的航迹并打印跳过数量
- `save_features(features_df, output_path=...)` / `load_features(input_path=...)`：特征表保存与读取，默认路径由 `paths.output_dir` + `paths.features_filename` 组合而成

提取的特征：max_speed、cruise_speed、max_height、cruise_height、max_acceleration、max_deceleration、max_climb_rate、max_descent_rate、max_heading_rate

## dataset.py

- `map_to_category(aircraft_type)`：机型 -> 1（大型机）/ 0（小型机），未配置的机型抛 `ValueError`
- `split_dataset(features_df)`：生成 `category` 列、丢弃 `aircraft_type` 列、按 `category` 分层抽样划分训练/测试集
- `save_split(train_df, test_df, output_dir=...)`：保存为 `train.csv` / `test.csv`，默认目录为配置中的 `paths.split_dir`

## 配置说明

`config/config.yaml` 包含：

| 字段 | 说明 |
| --- | --- |
| `track_features.min_points` | 航迹最少点数，低于此值跳过该航迹 |
| `track_features.round_digits` | 特征数值保留的小数位数 |
| `track_features.output_columns` | 特征提取输出列顺序 |
| `category_mapping.large` / `.small` | 机型到大类的映射列表 |
| `split.test_size` | 测试集比例 |
| `split.random_seed` | 划分随机种子 |
| `columns.aircraft_type` / `.category` | 该层级用到的列名 |
| `paths.output_dir` | 该层级所有产物（特征表、train/test）的统一输出目录，默认 `data/processed/level1_size` |
| `paths.features_filename` | 特征表文件名，默认 `features.csv` |

## 当前状态

- 已验证：用 `data/raw/prepared.csv`（250 条模拟航迹）跑通特征提取 + 保存 + 划分全流程
  - 特征表：250 行，9 特征列
  - 划分结果：train 200 行 / test 50 行（8:2），分层抽样后两者大型机占比一致（均为 0.4）
