from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "interns.csv"
ARTIFACT_DIR = Path(__file__).resolve().parent / "artifacts"
MODEL_PATH = ARTIFACT_DIR / "performance_model.joblib"
METRICS_PATH = ARTIFACT_DIR / "training_metrics.json"

RAW_FEATURE_COLUMNS = [
    "task_completion_time_hours",
    "feedback_rating",
    "attendance_percentage",
]
ENGINEERED_FEATURE_COLUMNS = [
    "task_completion_time_hours",
    "feedback_rating",
    "attendance_percentage",
    "efficiency_index",
    "attendance_strength",
    "feedback_attendance_interaction",
]
TARGET_COLUMN = "performance_score"


def ensure_artifact_dir() -> Path:
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    return ARTIFACT_DIR


def clamp_score(score: float) -> float:
    return float(np.clip(score, 0.0, 100.0))


def score_to_label(score: float) -> str:
    if score >= 80:
        return "Excellent"
    if score >= 50:
        return "Average"
    return "Struggling"


def clean_dataframe(frame: pd.DataFrame) -> pd.DataFrame:
    cleaned = frame.copy()
    cleaned.columns = [column.strip().lower() for column in cleaned.columns]

    expected_columns = set(RAW_FEATURE_COLUMNS + [TARGET_COLUMN])
    missing_columns = expected_columns - set(cleaned.columns)
    if missing_columns:
        raise ValueError(f"Dataset is missing required columns: {sorted(missing_columns)}")

    numeric_columns = RAW_FEATURE_COLUMNS + [TARGET_COLUMN]
    for column in numeric_columns:
        cleaned[column] = pd.to_numeric(cleaned[column], errors="coerce")

    cleaned = cleaned.drop_duplicates(subset=RAW_FEATURE_COLUMNS, keep="last")
    cleaned["task_completion_time_hours"] = cleaned["task_completion_time_hours"].clip(lower=0.5, upper=168)
    cleaned["feedback_rating"] = cleaned["feedback_rating"].clip(lower=1, upper=5)
    cleaned["attendance_percentage"] = cleaned["attendance_percentage"].clip(lower=0, upper=100)
    cleaned[TARGET_COLUMN] = cleaned[TARGET_COLUMN].clip(lower=0, upper=100)

    feature_medians = cleaned[RAW_FEATURE_COLUMNS].median(numeric_only=True)
    cleaned[RAW_FEATURE_COLUMNS] = cleaned[RAW_FEATURE_COLUMNS].fillna(feature_medians)
    cleaned[TARGET_COLUMN] = cleaned[TARGET_COLUMN].fillna(cleaned[TARGET_COLUMN].median())

    return cleaned.reset_index(drop=True)


def engineer_features(frame: pd.DataFrame) -> pd.DataFrame:
    engineered = frame.copy()
    hours = engineered["task_completion_time_hours"].clip(lower=0.5)
    rating = engineered["feedback_rating"].clip(lower=1)
    attendance = engineered["attendance_percentage"].clip(lower=0)

    engineered["efficiency_index"] = (rating * attendance) / hours
    engineered["attendance_strength"] = attendance / 100.0
    engineered["feedback_attendance_interaction"] = rating * attendance / 5.0
    return engineered[ENGINEERED_FEATURE_COLUMNS]


def build_input_frame(task_completion_time_hours: float, feedback_rating: float, attendance_percentage: float) -> pd.DataFrame:
    frame = pd.DataFrame(
        [
            {
                "task_completion_time_hours": task_completion_time_hours,
                "feedback_rating": feedback_rating,
                "attendance_percentage": attendance_percentage,
            }
        ]
    )
    return engineer_features(frame)
