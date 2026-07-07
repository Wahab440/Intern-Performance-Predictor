from __future__ import annotations

from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .db import get_predictions_collection
from .model import load_artifact
from .predict import predict_performance
from .schemas import HealthResponse, PerformanceInput, PredictionResponse


app = FastAPI(
    title="Intern Performance Predictor",
    description="Predicts intern performance score and category from operational signals.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL_ARTIFACT = None


def log_prediction(payload: PerformanceInput, prediction: PredictionResponse) -> None:
    collection = get_predictions_collection()
    if collection is None:
        return

    try:
        collection.insert_one(
            {
                "input": payload.model_dump(),
                "output": prediction.model_dump(),
                "created_at": datetime.now(timezone.utc),
                "source": "api",
            }
        )
    except Exception:
        return


def get_model_artifact() -> dict:
    global MODEL_ARTIFACT
    if MODEL_ARTIFACT is None:
        try:
            MODEL_ARTIFACT = load_artifact()
        except FileNotFoundError:
            from .train import train_model

            train_model()
            MODEL_ARTIFACT = load_artifact()
    return MODEL_ARTIFACT


@app.on_event("startup")
def warm_model() -> None:
    get_model_artifact()


@app.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    artifact_ready = True
    try:
        get_model_artifact()
    except Exception:
        artifact_ready = False
    return HealthResponse(status="ok", model_ready=artifact_ready)


@app.post("/predict", response_model=PredictionResponse)
def predict(payload: PerformanceInput) -> PredictionResponse:
    try:
        artifact = get_model_artifact()
        prediction = predict_performance(payload, artifact)
        log_prediction(payload, prediction)
        return prediction
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {exc}") from exc
