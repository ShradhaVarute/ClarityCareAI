from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.models.patient import Patient
from app.models.prediction import Prediction

router = APIRouter(prefix="/admin", tags=["admin"])


def require_admin(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user


@router.get("/stats")
def get_stats(current_user: User = Depends(require_admin), db: Session = Depends(get_db)):
    total_users = db.query(func.count(User.id)).scalar()
    total_patients = db.query(func.count(User.id)).filter(User.role == "patient").scalar()
    total_doctors = db.query(func.count(User.id)).filter(User.role == "doctor").scalar()
    total_predictions = db.query(func.count(Prediction.id)).scalar()

    predictions_by_disease = (
        db.query(Prediction.predicted_disease, func.count(Prediction.id))
        .group_by(Prediction.predicted_disease)
        .all()
    )

    return {
        "total_users": total_users,
        "total_patients": total_patients,
        "total_doctors": total_doctors,
        "total_predictions": total_predictions,
        "predictions_by_disease": {disease: count for disease, count in predictions_by_disease},
    }


@router.get("/users")
def list_users(current_user: User = Depends(require_admin), db: Session = Depends(get_db)):
    users = db.query(User).all()
    return [
        {"id": u.id, "email": u.email, "role": u.role, "created_at": u.created_at}
        for u in users
    ]