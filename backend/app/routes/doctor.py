from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.models.patient import Patient
from app.models.prediction import Prediction
from app.models.explanation import Explanation

router = APIRouter(prefix="/doctor", tags=["doctor"])


def require_doctor(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role not in ("doctor", "admin"):
        raise HTTPException(status_code=403, detail="Doctor or admin access required")
    return current_user


@router.get("/patients")
def list_patients(current_user: User = Depends(require_doctor), db: Session = Depends(get_db)):
    patients = db.query(Patient).all()
    return [
        {"id": p.id, "full_name": p.full_name, "date_of_birth": p.date_of_birth}
        for p in patients
    ]
@router.get("/predictions/{prediction_id}")
def get_prediction_detail(
    prediction_id: int,
    current_user: User = Depends(require_doctor),
    db: Session = Depends(get_db),
):
    prediction = db.query(Prediction).filter(Prediction.id == prediction_id).first()
    if not prediction:
        raise HTTPException(status_code=404, detail="Prediction not found")

    patient = db.query(Patient).filter(Patient.id == prediction.patient_id).first()
    explanation = db.query(Explanation).filter(Explanation.prediction_id == prediction.id).first()

    return {
        "id": prediction.id,
        "patient_name": patient.full_name if patient else "Unknown",
        "predicted_disease": prediction.predicted_disease,
        "confidence_score": prediction.confidence_score,
        "created_at": prediction.created_at,
        "input_features": prediction.input_features,
        "explanation": explanation.shap_values if explanation else [],
        "prediction": 1 if float(prediction.confidence_score) >= 0.5 else 0,
    }


@router.get("/patients/{patient_id}/predictions")
def get_patient_predictions(
    patient_id: int,
    current_user: User = Depends(require_doctor),
    db: Session = Depends(get_db),
):
    predictions = db.query(Prediction).filter(Prediction.patient_id == patient_id).all()

    results = []
    for pred in predictions:
        explanation = db.query(Explanation).filter(Explanation.prediction_id == pred.id).first()
        results.append({
            "id": pred.id,
            "predicted_disease": pred.predicted_disease,
            "confidence_score": pred.confidence_score,
            "created_at": pred.created_at,
            "input_features": pred.input_features,
            "shap_values": explanation.shap_values if explanation else None,
        })

    return results