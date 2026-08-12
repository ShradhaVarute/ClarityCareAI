import pandas as pd
from pipeline.train import train_disease_model

DATA_URL = "https://raw.githubusercontent.com/ShinjiniShome/lung_cancer_survey_dataviz/main/Lung%20Cancer%20Survey.csv"


def run():
    df = pd.read_csv(DATA_URL)
    df = df.dropna()

    df = pd.get_dummies(df, drop_first=True)  # GENDER, and all the YES/NO symptom columns

    # After get_dummies, the target column becomes something like "LUNG_CANCER_YES"
    target_col = [c for c in df.columns if c.upper().startswith("LUNG_CANCER")][0]

    X = df.drop(columns=[target_col])
    y = df[target_col].astype(int)

    return train_disease_model("lung_cancer", X, y)


if __name__ == "__main__":
    run()