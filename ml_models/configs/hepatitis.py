from ucimlrepo import fetch_ucirepo
import pandas as pd
from pipeline.train import train_disease_model


def run():
    hepatitis = fetch_ucirepo(id=46)
    X = hepatitis.data.features.copy()
    y = hepatitis.data.targets.copy()

    combined = X.copy()
    combined["target"] = (y.iloc[:, 0] == 2).astype(int)  # 2 = LIVE -> 1, 1 = DIE -> 0
    combined = combined.dropna()

    combined = pd.get_dummies(combined, drop_first=True)

    X_clean = combined.drop(columns=["target"])
    y_clean = combined["target"]

    print("Shape after cleaning:", combined.shape)
    print("Target distribution:", y_clean.value_counts().to_dict())

    return train_disease_model("hepatitis", X_clean, y_clean)


if __name__ == "__main__":
    run()