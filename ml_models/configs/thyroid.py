import pandas as pd
from pipeline.train import train_disease_model

DATA_URL = "https://raw.githubusercontent.com/00pratapsingh/Thyroid-Prediction-System/main/hypothyroid.csv"

NUMERIC_COLUMNS = ["age", "TSH", "T3", "TT4", "T4U", "FTI"]


def run():
    df = pd.read_csv(DATA_URL)
    df = df.replace("?", pd.NA)

    for col in NUMERIC_COLUMNS:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    missing_fraction = df.isna().mean()
    columns_to_drop = missing_fraction[missing_fraction > 0.5].index.tolist()
    df = df.drop(columns=columns_to_drop)

    df = df.dropna()

    df["target"] = (df["Class"].str.lower() != "negative").astype(int)
    df = df.drop(columns=["Class"])

    df = pd.get_dummies(df, drop_first=True)

    X = df.drop(columns=["target"])
    y = df["target"]

    print("Shape after cleaning:", df.shape)
    print("Feature count:", X.shape[1])
    print("Target distribution:", y.value_counts().to_dict())

    return train_disease_model("thyroid", X, y, balance_classes=False, threshold=0.2)


if __name__ == "__main__":
    run()