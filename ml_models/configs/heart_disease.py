from ucimlrepo import fetch_ucirepo
from pipeline.train import train_disease_model


def run():
    heart_disease = fetch_ucirepo(id=45)
    X = heart_disease.data.features.copy()
    y = heart_disease.data.targets.copy()

    # Target in this dataset is 0-4 (severity); we binarize to 0 = no disease, 1 = disease present
    y = (y.iloc[:, 0] > 0).astype(int)

    # Drop rows with missing values for this first pass (documented limitation, refine later if needed)
    combined = X.copy()
    combined["target"] = y
    combined = combined.dropna()

    X_clean = combined.drop(columns=["target"])
    y_clean = combined["target"]

    return train_disease_model("heart_disease", X_clean, y_clean)


if __name__ == "__main__":
    run()