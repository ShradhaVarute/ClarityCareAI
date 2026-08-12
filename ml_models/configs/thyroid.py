import pandas as pd
from pipeline.train import train_disease_model

DATA_URL = "https://raw.githubusercontent.com/00pratapsingh/Thyroid-Prediction-System/main/hypothyroid.csv"


def run():
    df = pd.read_csv(DATA_URL)
    df = df.replace("?", pd.NA)

    print("Missing values per column:")
    print(df.isna().sum().sort_values(ascending=False))

    # Drop columns that are missing in most rows (e.g. TBG is rarely tested)
    missing_fraction = df.isna().mean()
    columns_to_drop = missing_fraction[missing_fraction > 0.5].index.tolist()
    print("Dropping high-missingness columns:", columns_to_drop)
    df = df.drop(columns=columns_to_drop)

    df = df.dropna()
    print("Shape after cleaning:", df.shape)

    df["target"] = (df["Class"].str.lower() != "negative").astype(int)
    df = df.drop(columns=["Class"])

    df = pd.get_dummies(df, drop_first=True)

    X = df.drop(columns=["target"])
    y = df["target"]

    print("Target distribution:", y.value_counts().to_dict())

    return train_disease_model("thyroid", X, y, balance_classes=False, threshold=0.2)


if __name__ == "__main__":
    run()