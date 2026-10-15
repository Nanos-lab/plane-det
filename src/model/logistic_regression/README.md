# logistic_regression 模型

## 用途

用逻辑回归（StandardScaler + LogisticRegression 的 Pipeline）解决二分类任务。当前配置指向 level1_size 的训练/测试数据（大型机/小型机分类），但代码本身不感知数据来源的具体层级，仅通过配置路径读取。

## 目录结构

```
logistic_regression/
├── __init__.py
├── config/
│   ├── __init__.py
│   ├── config.yaml   # 数据路径、超参数、输出路径
│   └── config.py
├── train.py             # 训练并保存模型
├── evaluate.py            # 评估并保存结果
└── README.md               # 本文件
```

## train.py

- `load_train_data(train_path=None)`：读取训练数据，拆分为特征 X（除 label_column 外的所有列）和标签 y
- `train_model(X, y)`：构建 `Pipeline(StandardScaler + LogisticRegression)` 并训练
- `save_model(pipeline, output_path=...)`：用 `joblib.dump` 保存，默认路径为 `paths.output_dir / paths.model_filename`
- `main()`：串联以上三步，可直接 `python -m src.model.logistic_regression.train` 运行

## evaluate.py

- `load_test_data(test_path=None)`：读取测试数据，拆分方式与训练数据一致
- `load_model(model_path=...)`：读取已保存模型
- `evaluate(pipeline, X, y)`：计算 accuracy、precision、recall、f1、confusion_matrix，返回可直接序列化为 json 的 dict
- `save_evaluation(result, output_path=...)`：保存为 json 文件，默认路径为 `paths.output_dir / paths.evaluation_filename`
- `main()`：串联以上四步，可直接 `python -m src.model.logistic_regression.evaluate` 运行

## 配置说明

`config/config.yaml` 包含：

| 字段 | 说明 |
| --- | --- |
| `data.train_path` / `data.test_path` | 训练/测试数据路径 |
| `data.label_column` | 标签列名，其余列均视为特征 |
| `model.C` | 逻辑回归正则化强度 |
| `model.max_iter` | 最大迭代次数 |
| `model.random_seed` | 随机种子 |
| `paths.output_dir` | 模型与评估结果的统一输出目录，默认 `outputs/logistic_regression` |
| `paths.model_filename` | 模型文件名，默认 `model.joblib` |
| `paths.evaluation_filename` | 评估结果文件名，默认 `evaluation.json` |

## 当前状态

- 已验证训练+评估全流程可跑通（用 level1_size 的 train/test 数据）
- 当前模拟数据未刻意让大型机/小型机在特征上有系统性差异，评估指标偏低（accuracy 约 0.58）符合预期，待后续替换为更有区分度的数据或真实数据后复查
