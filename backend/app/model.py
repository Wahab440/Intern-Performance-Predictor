from __future__ import annotations

from pathlib import Path
from typing import Any

import joblib
import pandas as pd

from .utils import MODEL_PATH, ensure_artifact_dir, score_to_label


Artifact = dict[str, Any]


def save_artifact(artifact: Artifact, path: Path | None = None) -> Path:
    target_path = path or MODEL_PATH
    ensure_artifact_dir()
    joblib.dump(artifact, target_path)
    return target_path


def load_artifact(path: Path | None = None) -> Artifact:
    target_path = path or MODEL_PATH
    if not target_path.exists():
        raise FileNotFoundError(f"Model artifact not found at {target_path}")

    loaded_artifact = joblib.load(target_path)
    if not isinstance(loaded_artifact, dict):
        raise ValueError("Invalid model artifact format")
    return loaded_artifact


def predict_from_artifact(artifact: Artifact, feature_frame: pd.DataFrame) -> float:
    model = artifact["model"]
    raw_prediction = float(model.predict(feature_frame)[0])
    return raw_prediction


def format_prediction(raw_score: float) -> tuple[float, str]:
    rounded_score = round(raw_score, 2)
    return rounded_score, score_to_label(rounded_score)
