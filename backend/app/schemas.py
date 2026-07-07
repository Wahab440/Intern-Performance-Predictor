from pydantic import BaseModel, Field


class PerformanceInput(BaseModel):
    task_completion_time_hours: float = Field(
        ..., gt=0, le=168, description="Time taken to complete the task in hours"
    )
    feedback_rating: float = Field(
        ..., ge=1, le=5, description="Manager or mentor feedback rating from 1 to 5"
    )
    attendance_percentage: float = Field(
        ..., ge=0, le=100, description="Attendance percentage over the review window"
    )


class PredictionResponse(BaseModel):
    predicted_score: float = Field(..., description="Predicted performance score from 0 to 100")
    performance_label: str = Field(..., description="Excellent, Average, or Struggling")


class HealthResponse(BaseModel):
    status: str
    model_ready: bool
