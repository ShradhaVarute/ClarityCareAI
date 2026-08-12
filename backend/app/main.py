from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth, predictions
from app import models
from app.routes import auth, predictions, doctor
from app.routes import auth, predictions, doctor, admin

app = FastAPI(
    title="Clarity Care AI",
    description="Explainable Disease Prediction API",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(predictions.router)
app.include_router(doctor.router)
app.include_router(admin.router)

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "Clarity Care AI backend"}