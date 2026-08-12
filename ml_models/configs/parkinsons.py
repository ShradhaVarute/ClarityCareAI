import pandas as pd
from ucimlrepo import fetch_ucirepo
from pipeline.train import train_disease_model


def deduplicate_columns(columns):
    """Appends a numeric suffix to any repeated column name so every name is unique."""
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


def run():
    parkinsons = fetch_ucirepo(id=174)
    X = parkinsons.data.features.copy()
    y = parkinsons.data.targets.copy()

    X.columns = deduplicate_columns(X.columns)
    X.columns = deduplicate_columns(X.columns)
    print(X.columns.tolist())

    combined = X.copy()
    combined["target"] = y.iloc[:, 0]
    combined = combined.dropna()

    X_clean = combined.drop(columns=["target"])
    y_clean = combined["target"]

    return train_disease_model("parkinsons", X_clean, y_clean)


if __name__ == "__main__":
    run()