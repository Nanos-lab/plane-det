# model 模块

## 用途

模型训练与评估主目录。按模型类型（而非数据层级）组织子模块，比如 `logistic_regression`。

## 设计原则

- 每个模型子模块通过自己的 `config.yaml` 指定要用的训练/测试数据路径（`data.train_path` / `data.test_path`）和标签列名（`data.label_column`），与数据处理模块（`handle_data`）完全解耦，不感知其内部层级结构
- 只要目标 csv 的列结构符合"若干特征列 + 一个 label 列"的约定，`model` 下的任何模型都可以直接拿来训练，不需要改代码
- 公共的训练/评估工具函数（如指标计算、模型保存通用逻辑），若发现多个模型都需要，再抽到 `model/config/` 旁边新建公共模块

## 目录结构

```
model/
├── __init__.py
├── config/            # 公共配置（当前为空占位）
└── logistic_regression/   # 逻辑回归模型
    └── README.md
```

## 新增模型时如何扩展

1. 在 `model/` 下新建 `<model_name>/` 目录，按统一模块初始化结构搭建（见 `architecture.md`）
2. 在该模型的 `config/config.yaml` 中配置数据来源、超参数、输出路径
3. 实现 `train.py`（训练+保存模型）和 `evaluate.py`（评估+保存结果）
4. 在 `architecture.md` 的模块列表中补充一行
