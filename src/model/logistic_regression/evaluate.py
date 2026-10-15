# -*- coding: utf-8 -*-
"""
评估逻辑回归模型：读取测试数据和已保存的模型，计算评估指标并保存为 json 文件。
"""

from __future__ import annotations

import json
from pathlib import Path

import joblib
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)

from .config.config import load_config

_CONFIG = load_config()

_LABEL_COLUMN = _CONFIG["data"]["label_column"]
_TEST_PATH = _CONFIG["data"]["test_path"]

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
_OUTPUT_DIR = _PROJECT_ROOT / _CONFIG["paths"]["output_dir"]
_MODEL_PATH = _OUTPUT_DIR / _CONFIG["paths"]["model_filename"]
_EVALUATION_PATH = _OUTPUT_DIR / _CONFIG["paths"]["evaluation_filename"]


def load_test_data(test_path: Path | str = None) -> tuple[pd.DataFrame, pd.Series]:
    """读取测试数据，拆分为特征 X 和标签 y，拆分方式与训练数据一致。"""
    path = _PROJECT_ROOT / test_path if test_path else _PROJECT_ROOT / _TEST_PATH
    df = pd.read_csv(path, encoding="utf-8-sig")
    X = df.drop(columns=[_LABEL_COLUMN])
    y = df[_LABEL_COLUMN]
    return X, y


def load_model(model_path: Path = _MODEL_PATH):
    """读取已保存的模型 Pipeline。"""
    return joblib.load(model_path)


def evaluate(pipeline, X: pd.DataFrame, y: pd.Series) -> dict:
    """
    计算评估指标：accuracy、precision、recall、f1、confusion_matrix。

    返回的 dict 可直接序列化为 json（confusion_matrix 存成列表的列表）。
    """
    y_pred = pipeline.predict(X)
    return {
        "accuracy": accuracy_score(y, y_pred),
        "precision": precision_score(y, y_pred),
        "recall": recall_score(y, y_pred),
        "f1": f1_score(y, y_pred),
        "confusion_matrix": confusion_matrix(y, y_pred).tolist(),
    }


def save_evaluation(result: dict, output_path: Path = _EVALUATION_PATH) -> Path:
    """将评估结果保存为 json 文件。"""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    return output_path


def main() -> None:
    X, y = load_test_data()
    pipeline = load_model()
    result = evaluate(pipeline, X, y)
    saved_path = save_evaluation(result)
    print(f"评估结果已保存至: {saved_path}")
    print(result)


if __name__ == "__main__":
    main()
