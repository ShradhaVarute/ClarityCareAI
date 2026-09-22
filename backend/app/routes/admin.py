from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.core.database import get_db
from app.core.deps import get_current_user
from app.core.security import hash_password, create_access_token
from app.models.user import User
from app.models.patient import Patient
from app.models.prediction import Prediction
from app.schemas.auth import StaffCreate, Token

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


@router.post("/users", response_model=Token)
def create_staff_user(
    payload: StaffCreate,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Create a doctor or admin account. Only an existing admin can do this —
    these roles are never self-assignable via public registration."""
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        email=payload.email,
        hashed_password=hash_password(payload.password),
        role=payload.role,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = create_access_token({"sub": str(new_user.id), "role": new_user.role})
    return Token(access_token=token)