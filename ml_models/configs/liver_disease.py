import pandas as pd
from ucimlrepo import fetch_ucirepo
from pipeline.train import train_disease_model


def run():
    liver = fetch_ucirepo(id=225)
    X = liver.data.features.copy()
    y = liver.data.targets.copy()

    combined = X.copy()
    combined["target"] = (y.iloc[:, 0] == 1).astype(int)  # 1 = liver patient, 2 = not

    combined = pd.get_dummies(combined, drop_first=True)  # handles the "Gender" column
    combined = combined.dropna()

    X_clean = combined.drop(columns=["target"])
    y_clean = combined["target"]

    return train_disease_model("liver_disease", X_clean, y_clean)


if __name__ == "__main__":
    run()