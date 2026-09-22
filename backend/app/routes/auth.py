from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.core.database import get_db
from app.core.security import hash_password, verify_password, create_access_token
from app.models.user import User
from app.models.patient import Patient
from app.schemas.auth import UserRegister, UserLogin, Token
from app.core.deps import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])
limiter = Limiter(key_func=get_remote_address)


@router.post("/register", response_model=Token)
@limiter.limit("10/hour")
def register(request: Request, payload: UserRegister, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Public self-registration always creates a patient account. Doctor and
    # admin accounts can only be created by an existing admin (see
    # POST /admin/users) — they are never chosen by the registrant.
    new_user = User(
        email=payload.email,
        hashed_password=hash_password(payload.password),
        role="patient",
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    db.add(Patient(user_id=new_user.id, full_name=payload.full_name))
    db.commit()

    token = create_access_token({"sub": str(new_user.id), "role": new_user.role})
    return Token(access_token=token)


@router.post("/login", response_model=Token)
@limiter.limit("5/minute")
def login(request: Request, payload: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token({"sub": str(user.id), "role": user.role})
    return Token(access_token=token)


@router.get("/me")
def get_me(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    response = {
        "id": current_user.id,
        "email": current_user.email,
        "role": current_user.role,
    }

    if current_user.role == "patient":
        patient = db.query(Patient).filter(Patient.user_id == current_user.id).first()
        if patient:
            response["patient_id"] = patient.id
            response["full_name"] = patient.full_name

    return response