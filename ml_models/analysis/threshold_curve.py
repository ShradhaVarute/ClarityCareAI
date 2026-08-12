import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import joblib
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import precision_recall_curve


def plot_threshold_curve(disease_name: str, X_test_scaled, y_test):
    base_dir = Path(__file__).resolve().parent.parent
    model = joblib.load(base_dir / "saved_models" / disease_name / "model.joblib")
    y_proba = model.predict_proba(X_test_scaled)[:, 1]

    precisions, recalls, thresholds = precision_recall_curve(y_test, y_proba)

    plt.figure(figsize=(8, 5))
    plt.plot(thresholds, precisions[:-1], label="Precision")
    plt.plot(thresholds, recalls[:-1], label="Recall")
    plt.xlabel("Decision Threshold")
    plt.ylabel("Score")
    plt.title(f"{disease_name}: Precision & Recall vs Threshold")
    plt.legend()
    plt.grid(True)

    output_path = base_dir / "saved_models" / disease_name / "threshold_curve.png"
    plt.savefig(output_path)
    print(f"Saved chart to {output_path}")