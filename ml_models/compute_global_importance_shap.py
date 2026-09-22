import json
import joblib
import numpy as np
from pathlib import Path
from compute_feature_bounds import LOADERS

for disease, loader in LOADERS.items():
    print(f"Computing SHAP-based global importance for {disease}...")

    model_dir = Path("saved_models") / disease
    model = joblib.load(model_dir / "model.joblib")
    scaler = joblib.load(model_dir / "scaler.joblib")
    explainer = joblib.load(model_dir / "explainer.joblib")
    feature_names = joblib.load(model_dir / "feature_names.joblib")

    X = loader()
    X = X[feature_names]  # ensure exact column order matches training

    # Use a sample for speed on larger datasets (SHAP can be slow row-by-row)
    sample = X.sample(n=min(200, len(X)), random_state=42)
    scaled = scaler.transform(sample)

    shap_values = explainer.shap_values(scaled)
    if isinstance(shap_values, list):
        values = np.array(shap_values[1])
    elif shap_values.ndim == 3:
        values = shap_values[:, :, 1]
    else:
        values = shap_values

    mean_abs_shap = np.abs(values).mean(axis=0)

    if disease == "breast_cancer":
        # same inversion logic as prediction_service.py, for consistency
        pass  # mean(|x|) is already direction-agnostic, no inversion needed here

    ranked = sorted(zip(feature_names, mean_abs_shap), key=lambda x: x[1], reverse=True)
    output = [{"feature": f, "importance": float(v)} for f, v in ranked[:10]]

    with open(model_dir / "global_importance.json", "w") as f:
        json.dump(output, f, indent=2)

    print(f"  -> saved, top feature: {output[0]['feature']}")