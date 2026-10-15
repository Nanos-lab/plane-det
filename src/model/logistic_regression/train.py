# -*- coding: utf-8 -*-
"""
训练逻辑回归模型：读取训练数据，构建"标准化 + 逻辑回归"的 Pipeline 并训练，保存模型。

数据来源、超参数、输出路径均由 config.yaml 配置，与具体的数据处理模块（如 handle_data）解耦，
只要目标 csv 的列结构（若干特征列 + 一个 label 列）符合约定即可。
"""

from __future__ import annotations

from pathlib import Path

import joblib
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from .config.config import load_config

_CONFIG = load_config()

_LABEL_COLUMN = _CONFIG["data"]["label_column"]
_TRAIN_PATH = _CONFIG["data"]["train_path"]

_MODEL_PARAMS = _CONFIG["model"]

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
_OUTPUT_DIR = _PROJECT_ROOT / _CONFIG["paths"]["output_dir"]
_MODEL_PATH = _OUTPUT_DIR / _CONFIG["paths"]["model_filename"]


def load_train_data(train_path: Path | str = None) -> tuple[pd.DataFrame, pd.Series]:
    """
    读取训练数据，拆分为特征 X 和标签 y。

    除 label_column 外的所有列均作为特征，不硬编码特征列名列表，
    以便数据处理那边新增特征列时模型侧不需要改代码。
    """
    path = _PROJECT_ROOT / train_path if train_path else _PROJECT_ROOT / _TRAIN_PATH
    df = pd.read_csv(path, encoding="utf-8-sig")
    X = df.drop(columns=[_LABEL_COLUMN])
    y = df[_LABEL_COLUMN]
    return X, y


def train_model(X: pd.DataFrame, y: pd.Series) -> Pipeline:
    """构建并训练 StandardScaler + LogisticRegression 的 Pipeline。"""
    pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("classifier", LogisticRegression(
            C=_MODEL_PARAMS["C"],
            max_iter=_MODEL_PARAMS["max_iter"],
            random_state=_MODEL_PARAMS["random_seed"],
        )),
    ])
    pipeline.fit(X, y)
    return pipeline


def save_model(pipeline: Pipeline, output_path: Path = _MODEL_PATH) -> Path:
    """保存训练好的 Pipeline（含标准化器和分类器）。"""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, output_path)
    return output_path


def main() -> None:
    X, y = load_train_data()
    pipeline = train_model(X, y)
    saved_path = save_model(pipeline)
    print(f"模型已保存至: {saved_path}")


if __name__ == "__main__":
    main()
