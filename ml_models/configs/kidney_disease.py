import pandas as pd
from ucimlrepo import fetch_ucirepo
from pipeline.train import train_disease_model


def run():
    kidney = fetch_ucirepo(id=336)
    X = kidney.data.features.copy()
    y = kidney.data.targets.copy()

    combined = X.copy()
    combined["target"] = y.iloc[:, 0].map({"ckd": 1, "notckd": 0})

    # This dataset has categorical columns mixed with numeric — encode categoricals
    combined = pd.get_dummies(combined, drop_first=True)
    combined = combined.dropna()

    print(combined.columns.tolist())
    print(combined.shape)

    X_clean = combined.drop(columns=["target"])
    y_clean = combined["target"]

    return train_disease_model("kidney_disease", X_clean, y_clean)


if __name__ == "__main__":
    run()
