# 项目架构说明

各模块详细信息见对应 README。

## 模块初始化结构

```
<module_name>/
├── __init__.py
├── config/
│   ├── __init__.py
│   ├── config.yaml   # 配置项
│   └── config.py      # 配置加载逻辑
└── README.md           # 模块架构说明
```

## 模块列表

| 模块 | 路径 | 说明 | 详细文档 |
| --- | --- | --- | --- |
| handle_data | `src/handle_data/` | 数据处理主目录，所有分层任务都放在其下 | [src/handle_data/README.md](src/handle_data/README.md) |
| feature_extract | `src/handle_data/feature_extract/` | 公共特征计算原子函数，供各层级任务组合调用 | [src/handle_data/feature_extract/README.md](src/handle_data/feature_extract/README.md) |
| level1_size | `src/handle_data/level1_size/` | 第一层级：大型机/小型机二分类（特征提取 + 数据集划分） | [src/handle_data/level1_size/README.md](src/handle_data/level1_size/README.md) |
| model | `src/model/` | 模型训练与评估主目录，按模型类型组织子模块 | [src/model/README.md](src/model/README.md) |
| logistic_regression | `src/model/logistic_regression/` | 逻辑回归模型：训练 + 评估 | [src/model/logistic_regression/README.md](src/model/logistic_regression/README.md) |

新增模块后在此表格补充一行。
