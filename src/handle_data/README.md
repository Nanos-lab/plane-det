# handle_data 模块

## 用途

数据处理主目录。所有分层模型任务（level1_size、后续的 level2 等）都放在该模块下。

## 目录结构

```
handle_data/
├── __init__.py
├── config/
│   ├── __init__.py
│   ├── config.yaml     # 公共配置：原始数据列名、时间格式、原始数据路径（所有层级共用）
│   └── config.py
├── feature_extract/      # 公共特征计算原子函数（与具体任务层级无关）
│   ├── time_utils.py
│   ├── kinematics.py
│   ├── io_utils.py
│   └── README.md
├── level1_size/           # 第一层级：大型机/小型机二分类任务
│   └── README.md
└── README.md               # 本文件
```

## 设计原则

- `config/config.yaml`：只放描述"原始数据长什么样"的公共信息，所有层级任务共用
- `feature_extract/`：原子特征计算函数（如最大速度、爬升率），不绑定具体任务，各层级按需组合调用
- `<level>/`：每个层级任务有自己的 `features.py`（组合调用公共函数构建特征表）、`dataset.py`（数据集划分逻辑）、`config/config.yaml`（该层级专属配置）

## 新增层级任务时如何扩展

1. 在 `handle_data/` 下新建 `<level_name>/` 目录，按统一模块初始化结构搭建（见 `architecture.md`）
2. 若需要新的原子特征，先在 `feature_extract/` 里补充公共函数，再在该层级的 `features.py` 中组合调用
3. 在该层级的 `config/config.yaml` 中配置该层级专属的参数（机型映射、划分比例、路径等）
4. 在 `architecture.md` 的模块列表中补充一行
