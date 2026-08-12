from pydantic import BaseModel
from typing import Any


class PredictionRequest(BaseModel):
    patient_id: int
    features: dict[str, Any]


class ExplanationItem(BaseModel):
    feature: str
    shap_value: float
    input_value: Any


class PredictionResponse(BaseModel):
    prediction: int
    confidence: float
    disease: str
    explanation: list[ExplanationItem]