import json
import pandas as pd
from pathlib import Path
from ucimlrepo import fetch_ucirepo
from sklearn.datasets import load_breast_cancer


def dedupe_columns(columns):
    seen = {}
    new_columns = []
    for col in columns:
        if col not in seen:
            seen[col] = 0
            new_columns.append(col)
        else:
            seen[col] += 1
            new_columns.append(f"{col}_{seen[col]}")
    return new_columns


def load_heart_disease():
    d = fetch_ucirepo(id=45)
    X = d.data.features.copy()
    y = (d.data.targets.iloc[:, 0] > 0).astype(int)
    combined = X.copy()
    combined["target"] = y
    combined = combined.dropna()
    return combined.drop(columns=["target"])


def load_diabetes():
    url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv"
    cols = ["pregnancies", "glucose", "blood_pressure", "skin_thickness", "insulin", "bmi", "diabetes_pedigree", "age", "target"]
    df = pd.read_csv(url, names=cols)
    return df.drop(columns=["target"])


def load_breast_cancer_data():
    data = load_breast_cancer(as_frame=True)
    return data.data


def load_kidney_disease():
    d = fetch_ucirepo(id=336)
    X = d.data.features.copy()
    y = d.data.targets.copy()
    combined = X.copy()
    combined["target"] = y.iloc[:, 0].map({"ckd": 1, "notckd": 0})
    combined = pd.get_dummies(combined, drop_first=True)
    combined = combined.dropna()
    return combined.drop(columns=["target"])


def load_liver_disease():
    d = fetch_ucirepo(id=225)
    X = d.data.features.copy()
    y = d.data.targets.copy()
    combined = X.copy()
    combined["target"] = (y.iloc[:, 0] == 1).astype(int)
    combined = pd.get_dummies(combined, drop_first=True)
    combined = combined.dropna()
    return combined.drop(columns=["target"])


def load_parkinsons():
    d = fetch_ucirepo(id=174)
    X = d.data.features.copy()
    y = d.data.targets.copy()
    X.columns = dedupe_columns(X.columns)
    combined = X.copy()
    combined["target"] = y.iloc[:, 0]
    combined = combined.dropna()
    return combined.drop(columns=["target"])


def load_stroke():
    url = "https://raw.githubusercontent.com/YuvrazError/Healthcare-Dataset-Analysis/main/healthcare-dataset-stroke-data.csv"
    df = pd.read_csv(url)
    df = df.drop(columns=["id"])
    df = df.dropna()
    df = pd.get_dummies(df, drop_first=True)
    return df.drop(columns=["stroke"])


def load_lung_cancer():
    url = "https://raw.githubusercontent.com/ShinjiniShome/lung_cancer_survey_dataviz/main/Lung%20Cancer%20Survey.csv"
    df = pd.read_csv(url)
    df = df.dropna()
    df = pd.get_dummies(df, drop_first=True)
    target_col = [c for c in df.columns if c.upper().startswith("LUNG_CANCER")][0]
    return df.drop(columns=[target_col])


def load_thyroid():
    url = "https://raw.githubusercontent.com/00pratapsingh/Thyroid-Prediction-System/main/hypothyroid.csv"
    df = pd.read_csv(url)
    df = df.replace("?", pd.NA)
    for col in ["age", "TSH", "T3", "TT4", "T4U", "FTI"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    missing_fraction = df.isna().mean()
    df = df.drop(columns=missing_fraction[missing_fraction > 0.5].index.tolist())
    df = df.dropna()
    df["target"] = (df["Class"].str.lower() != "negative").astype(int)
    df = df.drop(columns=["Class"])
    df = pd.get_dummies(df, drop_first=True)
    return df.drop(columns=["target"])


def load_hepatitis():
    d = fetch_ucirepo(id=46)
    X = d.data.features.copy()
    y = d.data.targets.copy()
    combined = X.copy()
    combined["target"] = (y.iloc[:, 0] == 2).astype(int)
    combined = combined.dropna()
    combined = pd.get_dummies(combined, drop_first=True)
    return combined.drop(columns=["target"])


LOADERS = {
    "heart_disease": load_heart_disease,
    "diabetes": load_diabetes,
    "breast_cancer": load_breast_cancer_data,
    "kidney_disease": load_kidney_disease,
    "liver_disease": load_liver_disease,
    "parkinsons": load_parkinsons,
    "stroke": load_stroke,
    "lung_cancer": load_lung_cancer,
    "thyroid": load_thyroid,
    "hepatitis": load_hepatitis,
}


def main():
    all_bounds = {}
    for disease, loader in LOADERS.items():
        print(f"Loading {disease}...")
        X = loader()
        bounds = {}
        for col in X.columns:
            col_min = float(X[col].min())
            col_max = float(X[col].max())
            bounds[col] = [col_min, col_max]
        all_bounds[disease] = bounds
        print(f"  -> {len(bounds)} features")

    output_path = Path("feature_bounds_generated.json")
    with open(output_path, "w") as f:
        json.dump(all_bounds, f, indent=2)
    print(f"\nSaved to {output_path}")


if __name__ == "__main__":
    main()