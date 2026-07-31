from fastapi import FastAPI

app = FastAPI(
    title="Clarity Care AI",
    description="Explainable Disease Prediction API",
    version="0.1.0",
)

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "Clarity Care AI backend"}