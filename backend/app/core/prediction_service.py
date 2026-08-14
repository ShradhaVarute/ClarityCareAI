import joblib
import numpy as np
import pandas as pd
from functools import lru_cache
from app.core.model_registry import get_model_paths


@lru_cache(maxsize=None)
def load_disease_artifacts(disease_name: str):
    """Loads and caches a disease's model/scaler/explainer/features — loaded once, reused across requests."""
    paths = get_model_paths(disease_name)
    return {
        "model": joblib.load(paths["model"]),
        "scaler": joblib.load(paths["scaler"]),
        "explainer": joblib.load(paths["explainer"]),
        "feature_names": joblib.load(paths["feature_names"]),
    }


def run_prediction(disease_name: str, input_features: dict) -> dict:
    artifacts = load_disease_artifacts(disease_name)
    feature_names = artifacts["feature_names"]

    missing = [f for f in feature_names if f not in input_features]
    if missing:
        raise ValueError(f"Missing required features: {missing}")

    ordered_values = pd.DataFrame([[input_features[f] for f in feature_names]], columns=feature_names)
    scaled = artifacts["scaler"].transform(ordered_values)

    raw_proba = artifacts["model"].predict_proba(scaled)[0][1]

    shap_values = artifacts["explainer"].shap_values(scaled)
    if isinstance(shap_values, list):
        values_for_positive_class = np.array(shap_values[1][0]).flatten()
    elif shap_values.ndim == 3:
        values_for_positive_class = shap_values[0, :, 1]
    else:
        values_for_positive_class = shap_values[0]
    values_for_positive_class = np.asarray(values_for_positive_class).flatten()

    if disease_name == "breast_cancer":
        # sklearn encodes class 1 = benign here — invert everything so
        # "1" consistently means "condition present" across all diseases
        prediction = int(raw_proba < 0.5)
        confidence = 1 - raw_proba
        values_for_positive_class = -values_for_positive_class
    else:
        prediction = int(raw_proba >= 0.5)
        confidence = raw_proba

    explanation = sorted(
        [
            {"feature": f, "shap_value": float(v), "input_value": input_features[f]}
            for f, v in zip(feature_names, values_for_positive_class)
        ],
        key=lambda x: abs(x["shap_value"]),
        reverse=True,
    )

    return {
        "prediction": prediction,
        "confidence": float(confidence),
        "explanation": explanation,
    }