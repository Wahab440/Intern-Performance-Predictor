from __future__ import annotations

from .model import format_prediction, predict_from_artifact
from .schemas import PerformanceInput, PredictionResponse
from .utils import build_input_frame


def predict_performance(input_payload: PerformanceInput, artifact: dict) -> PredictionResponse:
    feature_frame = build_input_frame(
        task_completion_time_hours=input_payload.task_completion_time_hours,
        feedback_rating=input_payload.feedback_rating,
        attendance_percentage=input_payload.attendance_percentage,
    )
    raw_score = predict_from_artifact(artifact, feature_frame)
    predicted_score, performance_label = format_prediction(raw_score)
    return PredictionResponse(predicted_score=predicted_score, performance_label=performance_label)
