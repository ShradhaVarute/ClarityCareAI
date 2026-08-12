import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent  # points to ml_models/

sys.path.append(str(BASE_DIR))

import pandas as pd
import joblib
from sklearn.model_selection import train_test_split

DATA_URL = "https://raw.githubusercontent.com/YuvrazError/Healthcare-Dataset-Analysis/main/healthcare-dataset-stroke-data.csv"

df = pd.read_csv(DATA_URL)
df = df.drop(columns=["id"])
df = df.dropna()
df = pd.get_dummies(df, drop_first=True)

X = df.drop(columns=["stroke"])
y = df["stroke"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

scaler = joblib.load(BASE_DIR / "saved_models" / "stroke" / "scaler.joblib")
X_test_scaled = scaler.transform(X_test)

from threshold_curve import plot_threshold_curve
plot_threshold_curve("stroke", X_test_scaled, y_test)