from pathlib import Path

# Points to the ml_models/saved_models folder at the project root
ML_MODELS_DIR = Path(__file__).resolve().parent.parent.parent.parent / "ml_models" / "saved_models"

SUPPORTED_DISEASES = [
    "heart_disease", "diabetes", "breast_cancer", "kidney_disease",
    "liver_disease", "parkinsons", "stroke", "lung_cancer",
    "thyroid", "hepatitis",
]


def get_model_paths(disease_name: str) -> dict:
    if disease_name not in SUPPORTED_DISEASES:
        raise ValueError(f"Unsupported disease: {disease_name}")

    disease_dir = ML_MODELS_DIR / disease_name
    return {
        "model": disease_dir / "model.joblib",
        "scaler": disease_dir / "scaler.joblib",
        "explainer": disease_dir / "explainer.joblib",
        "feature_names": disease_dir / "feature_names.joblib",
    }