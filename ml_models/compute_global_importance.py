import json
import joblib
import numpy as np
from pathlib import Path

DISEASES = [
    "heart_disease", "diabetes", "breast_cancer", "kidney_disease",
    "liver_disease", "parkinsons", "stroke", "lung_cancer", "thyroid", "hepatitis",
]

for disease in DISEASES:
    model_dir = Path("saved_models") / disease
    explainer = joblib.load(model_dir / "explainer.joblib")
    feature_names = joblib.load(model_dir / "feature_names.joblib")
    model = joblib.load(model_dir / "model.joblib")

    # Use the model's built-in feature_importances_ (fast, no need to re-run SHAP on a full dataset)
    importances = model.feature_importances_
    ranked = sorted(zip(feature_names, importances), key=lambda x: x[1], reverse=True)

    output = [{"feature": f, "importance": float(i)} for f, i in ranked[:10]]

    with open(model_dir / "global_importance.json", "w") as f:
        json.dump(output, f, indent=2)

    print(f"[{disease}] saved global importance ({len(output)} features)")