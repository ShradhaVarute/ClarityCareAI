import json
from app.core.model_registry import ML_MODELS_DIR, SUPPORTED_DISEASES
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
from app.models.patient import Patient
from fastapi.responses import Response
from app.core.report_generator import generate_prediction_report


router = APIRouter(prefix="/predictions", tags=["predictions"])


@router.get("/history")
def get_my_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if current_user.role != "patient":
        raise HTTPException(status_code=403, detail="Patient access only")

    patient = db.query(Patient).filter(Patient.user_id == current_user.id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient record not found")

    predictions = (
        db.query(Prediction)
        .filter(Prediction.patient_id == patient.id)
        .order_by(Prediction.created_at.desc())
        .all()
    )

    results = []
    for pred in predictions:
        explanation = db.query(Explanation).filter(Explanation.prediction_id == pred.id).first()
        results.append({
            "id": pred.id,
            "predicted_disease": pred.predicted_disease,
            "confidence_score": pred.confidence_score,
            "created_at": pred.created_at,
            "shap_values": explanation.shap_values if explanation else None,
        })

    return results

@router.get("/history/{prediction_id}")
def get_prediction_detail(
    prediction_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    patient = db.query(Patient).filter(Patient.user_id == current_user.id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient record not found")

    prediction = (
        db.query(Prediction)
        .filter(Prediction.id == prediction_id, Prediction.patient_id == patient.id)
        .first()
    )
    if not prediction:
        raise HTTPException(status_code=404, detail="Prediction not found")

    explanation = db.query(Explanation).filter(Explanation.prediction_id == prediction.id).first()

    return {
        "id": prediction.id,
        "predicted_disease": prediction.predicted_disease,
        "confidence_score": prediction.confidence_score,
        "created_at": prediction.created_at,
        "input_features": prediction.input_features,
        "explanation": explanation.shap_values if explanation else [],
        "prediction": 1 if float(prediction.confidence_score) >= 0.5 else 0,
    }

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

@router.get("/history/{prediction_id}/report")
def download_prediction_report(
    prediction_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    patient = db.query(Patient).filter(Patient.user_id == current_user.id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient record not found")

    prediction = (
        db.query(Prediction)
        .filter(Prediction.id == prediction_id, Prediction.patient_id == patient.id)
        .first()
    )
    if not prediction:
        raise HTTPException(status_code=404, detail="Prediction not found")

    explanation = db.query(Explanation).filter(Explanation.prediction_id == prediction.id).first()

    pdf_bytes = generate_prediction_report({
        "patient_name": patient.full_name,
        "predicted_disease": prediction.predicted_disease,
        "confidence_score": prediction.confidence_score,
        "created_at": prediction.created_at.strftime("%B %d, %Y at %I:%M %p"),
        "prediction": 1 if float(prediction.confidence_score) >= 0.5 else 0,
        "explanation": explanation.shap_values if explanation else [],
    })

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=assessment_{prediction_id}.pdf"},
    )

@router.get("/insights/{disease_name}")
def get_global_importance(disease_name: str, current_user: User = Depends(get_current_user)):
    if disease_name not in SUPPORTED_DISEASES:
        raise HTTPException(status_code=404, detail="Unknown disease")

    path = ML_MODELS_DIR / disease_name / "global_importance.json"
    if not path.exists():
        raise HTTPException(status_code=404, detail="Insights not available for this disease")

    with open(path) as f:
        return json.load(f)