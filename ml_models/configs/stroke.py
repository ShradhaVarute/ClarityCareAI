import pandas as pd
from pipeline.train import train_disease_model

DATA_URL = "https://raw.githubusercontent.com/YuvrazError/Healthcare-Dataset-Analysis/main/healthcare-dataset-stroke-data.csv"


def run():
    df = pd.read_csv(DATA_URL)

    df = df.drop(columns=["id"])  # patient id column — must be dropped, classic leakage risk
    df = df.dropna()

    df = pd.get_dummies(df, drop_first=True)  # gender, work_type, smoking_status, etc. are categorical

    X = df.drop(columns=["stroke"])
    y = df["stroke"]

    return train_disease_model("stroke", X, y, balance_classes=True, threshold=0.15)

if __name__ == "__main__":
    run()