import logging

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from slowapi import Limiter

from app.core.database import get_db
from app.core.security import hash_password, verify_password, create_access_token
from app.models.user import User
from app.models.patient import Patient
from app.schemas.auth import UserRegister, UserLogin, Token
from app.core.deps import get_current_user

logger = logging.getLogger("uvicorn.error")

router = APIRouter(prefix="/auth", tags=["auth"])


def get_client_ip(request: Request) -> str:
    """Real client IP, for rate limiting behind Render's proxy chain.

    Render appends exactly two hops of its own after whatever a client sends:
    a Cloudflare edge address, then Render's internal proxy address. Those two
    are controlled by the platform and can be trusted; everything a client
    puts before them is attacker-editable, so we always drop exactly the last
    two entries and take what's left over as the real client IP.
    """
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        hops = [h.strip() for h in forwarded.split(",") if h.strip()]
        if len(hops) > 2:
            return hops[-3]
    return request.client.host if request.client else "unknown"


limiter = Limiter(key_func=get_client_ip)


@router.post("/register", response_model=Token)
@limiter.limit("10/hour")
def register(request: Request, payload: UserRegister, db: Session = Depends(get_db)):
    email = payload.email.lower()
    existing = db.query(User).filter(User.email == email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        email=email,
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
    # TEMPORARY diagnostic: remove after verifying the fix
    logger.info(
        f"LOGIN DIAG key={get_client_ip(request)} "
        f"xff={request.headers.get('x-forwarded-for')}"
    )

    email = payload.email.lower()
    user = db.query(User).filter(User.email == email).first()
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