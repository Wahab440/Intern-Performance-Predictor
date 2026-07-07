from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

from .model import save_artifact
from .utils import (
    DATA_PATH,
    METRICS_PATH,
    TARGET_COLUMN,
    clean_dataframe,
    engineer_features,
    ensure_artifact_dir,
    score_to_label,
)


def generate_synthetic_dataset(n_samples: int = 240, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    task_completion_time = np.clip(rng.gamma(shape=2.2, scale=4.0, size=n_samples) + 1.0, 0.5, 24.0)
    feedback_rating = np.clip(rng.normal(loc=3.4, scale=0.85, size=n_samples), 1.0, 5.0)
    attendance_percentage = np.clip(rng.normal(loc=84.0, scale=10.0, size=n_samples), 45.0, 100.0)

    base_score = (
        34.0
        + (feedback_rating * 15.0)
        + (attendance_percentage * 0.34)
        - (task_completion_time * 2.6)
        + ((feedback_rating - 3.0) * (attendance_percentage - 75.0) * 0.08)
    )
    noise = rng.normal(loc=0.0, scale=4.5, size=n_samples)
    performance_score = np.clip(base_score + noise, 0.0, 100.0)

    frame = pd.DataFrame(
        {
            "intern_id": [f"INT-{index:04d}" for index in range(1, n_samples + 1)],
            "task_completion_time_hours": task_completion_time.round(2),
            "feedback_rating": feedback_rating.round(1),
            "attendance_percentage": attendance_percentage.round(1),
            "performance_score": performance_score.round(2),
        }
    )

    return frame


def load_training_data() -> pd.DataFrame:
    if DATA_PATH.exists():
        loaded_frame = pd.read_csv(DATA_PATH)
        if len(loaded_frame) >= 100:
            return loaded_frame

    synthetic_frame = generate_synthetic_dataset()
    ensure_artifact_dir()
    synthetic_frame.to_csv(DATA_PATH, index=False)
    return synthetic_frame


def train_model(random_state: int = 42) -> dict:
    raw_frame = load_training_data()
    cleaned_frame = clean_dataframe(raw_frame)
    feature_frame = engineer_features(cleaned_frame)
    target = cleaned_frame[TARGET_COLUMN]

    x_train, x_test, y_train, y_test = train_test_split(
        feature_frame,
        target,
        test_size=0.2,
        random_state=random_state,
    )

    model = RandomForestRegressor(
        n_estimators=300,
        random_state=random_state,
        min_samples_leaf=2,
        n_jobs=-1,
    )
    model.fit(x_train, y_train)

    predictions = model.predict(x_test)
    # Some sklearn versions do not support the `squared` keyword; compute RMSE directly
    rmse = float(mean_squared_error(y_test, predictions) ** 0.5)
    feature_importances = [
        {"feature": name, "importance": float(score)}
        for name, score in sorted(
            zip(feature_frame.columns, model.feature_importances_),
            key=lambda item: item[1],
            reverse=True,
        )
    ]

    artifact = {
        "model": model,
        "feature_names": list(feature_frame.columns),
        "rmse": rmse,
        "feature_importances": feature_importances,
        "trained_at": datetime.now(timezone.utc).isoformat(),
        "label_thresholds": {"excellent": 80, "average": 50},
    }

    save_artifact(artifact)
    ensure_artifact_dir()
    metrics = {
        "rmse": rmse,
        "n_train": int(len(x_train)),
        "n_test": int(len(x_test)),
        "feature_importances": feature_importances,
        "sample_labels": {
            "excellent": score_to_label(90),
            "average": score_to_label(65),
            "struggling": score_to_label(35),
        },
    }
    METRICS_PATH.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    return metrics


if __name__ == "__main__":
    metrics = train_model()
    print(json.dumps(metrics, indent=2))
