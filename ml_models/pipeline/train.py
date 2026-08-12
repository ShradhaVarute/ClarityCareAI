import json
import joblib
import shap
from imblearn.over_sampling import SMOTE
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score


def train_disease_model(disease_name: str, X, y, output_dir: str = "saved_models", balance_classes: bool = False, threshold: float = 0.5):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    if balance_classes:
        smote = SMOTE(random_state=42)
        X_train_scaled, y_train = smote.fit_resample(X_train_scaled, y_train)

    model = RandomForestClassifier(n_estimators=200, random_state=42)
    model.fit(X_train_scaled, y_train)

    y_proba = model.predict_proba(X_test_scaled)[:, 1]
    y_pred = (y_proba >= threshold).astype(int)

    metrics = {
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred, zero_division=0),
        "recall": recall_score(y_test, y_pred, zero_division=0),
        "f1_score": f1_score(y_test, y_pred, zero_division=0),
        "roc_auc": roc_auc_score(y_test, y_proba),
        "threshold_used": threshold,
        "n_train": len(X_train_scaled),
        "n_test": len(X_test),
    }

    explainer = shap.TreeExplainer(model)

    disease_dir = Path(output_dir) / disease_name
    disease_dir.mkdir(parents=True, exist_ok=True)

    joblib.dump(model, disease_dir / "model.joblib")
    joblib.dump(scaler, disease_dir / "scaler.joblib")
    joblib.dump(explainer, disease_dir / "explainer.joblib")
    joblib.dump(list(X.columns), disease_dir / "feature_names.joblib")

    with open(disease_dir / "metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)

    print(f"[{disease_name}] Training complete.")
    print(json.dumps(metrics, indent=2))

    return model, metrics