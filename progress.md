# 会话进度记录

## 项目说明

本项目（plane-det-2）基于飞机航迹（点迹序列）的特征进行机型识别，不涉及图像/视觉模型。

## 当前状态

**最后更新：** 2026-10-14
**运行环境：** conda 环境 `imgforge`，Python 解释器固定为 `E:\anaconda3\envs\imgforge\python.exe`（不使用 `conda run` / `conda activate`）

## 本次会话做了什么

- 梳理仓库现状：确认是全新仓库（无 commit），已有 `agents.md`、`feature-list.json`、`init.sh`、`progress.md`、`requirements.txt` 等脚手架占位文件
- 明确项目方向：根据航迹点迹特征做机型识别（时序/轨迹特征分类问题），不是图像识别
- 将 `init.sh`（bash 脚本，在当前 Windows + PowerShell 环境下不适用）替换为 `init.ps1`：
  - 固定调用 `E:\anaconda3\envs\imgforge\python.exe`
  - 检查 `requirements.txt` 并执行 `pip install -r requirements.txt`
  - 若存在 `tests` 目录则运行 `pytest`，否则跳过
- 验证 `init.ps1` 可正常运行：Python 版本确认通过，依赖全部已满足，当前无 `tests` 目录故跳过测试，脚本以 exit code 0 结束

## 当前依赖（requirements.txt）

pandas, numpy, duckdb, pyyaml, scikit-learn, joblib, pydantic, fastapi, uvicorn

## 遗留事项

- `agents.md`、`feature-list.json` 仍是通用模板占位内容，尚未针对本项目改写（按用户要求，不预先拆解 feature，后续做了什么再记录）
- 尚无源代码、无数据、无 tests 目录

## 下次会话可参考

- 验证命令：`powershell -ExecutionPolicy Bypass -File .\init.ps1`
- 继续开发时，根据实际写的代码再决定目录结构（如 `src/`、`tests/`、`data/` 等）

## 2026-10-14 补充：目录结构搭建

- 创建 `data/`、`src/`、`outputs/` 三个基础目录，用于模块化开发：
  - `data/`：存放原始及处理后的航迹点迹数据
  - `src/`：存放核心源代码（特征工程、模型、训练/推理逻辑等），已加 `__init__.py` 使其可作为 Python 包导入
  - `outputs/`：存放运行产出物（模型权重、日志、评估报告、预测结果等）
- 新增 `.gitignore`：忽略 `__pycache__/`、`*.pyc`、`.pytest_cache/`；并将 `outputs/` 内容排除出版本控制（仅保留目录结构，用 `.gitkeep` 占位）

## 2026-10-14 补充：handle_data 模块与特征提取功能

- 确立模块初始化规范（`__init__.py` + `config/config.yaml` + `config/config.py` + `README.md`），记录在 `architecture.md`
- 搭建 `src/handle_data/` 模块骨架，并新增 `track_features.py` 实现航迹统计特征提取：
  - `extract_track_features(df)`：单条航迹 -> 一行特征 Series
  - `extract_features_from_tracks(df)`：多条航迹批量提取，跳过点数不足的航迹
  - 特征：max_speed、cruise_speed、max_height、cruise_height、max_acceleration、max_deceleration、max_climb_rate、max_descent_rate、max_heading_rate
- 用 `data/raw/prepared.csv`（250 条模拟航迹）验证通过，数值范围合理
- 修复 pandas 3.0 datetime64 精度（us 非 ns）导致的时间差计算错误，详见 `issues-log.md`

## 2026-10-14 补充：特征文件保存与读取

- `track_features.py` 新增 `save_features(features_df)` / `load_features()`，将特征表保存/读取为 `data/processed/features.csv`（固定文件名，覆盖式更新）
- `config.yaml` 补充 `paths.processed_dir`、`features_file.filename`
- `data/processed/` 加入 `.gitignore`（可由 raw 数据重新生成，不入库）
- 验证：保存后读回的数据与原特征表数值一致

## 2026-10-14 补充：按分层模型重构模块结构 + level1_size 功能

- 重新设计模块组织方式：不再按"处理阶段"（特征提取/数据划分）划分模块，改为按"任务层级"划分，`handle_data` 作为所有层级任务的主目录
- 新增 `handle_data/feature_extract/`：公共、与任务无关的原子特征计算函数
  - `kinematics.py`：compute_max_speed、compute_cruise_speed、compute_max_height、compute_cruise_height、compute_acceleration_extremes、compute_climb_descent_extremes、compute_max_heading_rate
  - `time_utils.py`：ensure_datetime、compute_dt_seconds
  - `io_utils.py`：save_dataframe、load_dataframe（路径参数化，不假设固定目录结构）
- `handle_data/config/config.yaml` 精简为只保留原始数据公共信息（columns、time、paths.raw_dir）
- 新增 `handle_data/level1_size/`：第一层级（大型机/小型机二分类）任务模块
  - `features.py`：组合调用 feature_extract 公共函数，构建该层级特征表
  - `dataset.py`：`map_to_category`（机型->大类，未知机型抛异常）+ `split_dataset`（分层抽样）+ `save_split`
  - 专属 `config/config.yaml`：track_features 参数、category_mapping（large/small 机型列表）、split（test_size=0.2, random_seed=42）、路径配置
- 删除旧的 `track_features.py` 及旧产物 `data/processed/features.csv`
- 新产物路径：`data/processed/level1_size/features.csv`、`data/splits/level1_size/{train,test}.csv`，均加入 `.gitignore`
- 端到端验证通过：250 条航迹 -> 250 行特征 -> 按 8:2 分层抽样划分为 train(200)/test(50)，train/test 大型机占比均为 0.4（分层抽样生效）；未知机型正确抛 ValueError
- `architecture.md` 模块列表更新为 handle_data / feature_extract / level1_size 三行

## 2026-10-14 补充：level1_size 产物目录合并

- `level1_size` 的训练/测试集划分结果不再单独放 `data/splits/level1_size/`，改为与 `features.csv` 同目录，统一输出到 `data/processed/level1_size/`（该层级所有产物集中管理）
- 修改 `config/config.yaml` 中 `paths.split_dir`，删除不再使用的 `data/splits/` 目录，`.gitignore` 同步移除相关规则
- 重新验证：`features.csv`、`train.csv`、`test.csv` 均正确输出到 `data/processed/level1_size/`
