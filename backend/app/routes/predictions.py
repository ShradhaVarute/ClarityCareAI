from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.core.model_registry import SUPPORTED_DISEASES
from app.core.prediction_service import run_prediction
from app.models.user import User
from app.models.prediction import Prediction
from app.models.explanation import Explanation
from app.schemas.prediction import PredictionRequest, PredictionResponse

router = APIRouter(prefix="/predictions", tags=["predictions"])


@router.post("/{disease_name}", response_model=PredictionResponse)
def create_prediction(
    disease_name: str,
    payload: PredictionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if disease_name not in SUPPORTED_DISEASES:
        raise HTTPException(status_code=404, detail=f"Unknown disease: {disease_name}")

    try:
        result = run_prediction(disease_name, payload.features)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

    db_prediction = Prediction(
        patient_id=payload.patient_id,
        input_features=payload.features,
        predicted_disease=disease_name,
        confidence_score=str(result["confidence"]),
        model_version="v1",
    )
    db.add(db_prediction)
    db.commit()
    db.refresh(db_prediction)

    db_explanation = Explanation(
        prediction_id=db_prediction.id,
        shap_values=result["explanation"],
    )
    db.add(db_explanation)
    db.commit()

    return PredictionResponse(
        prediction=result["prediction"],
        confidence=result["confidence"],
        disease=disease_name,
        explanation=result["explanation"],
    )