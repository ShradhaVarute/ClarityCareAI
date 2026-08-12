import pandas as pd
from pipeline.train import train_disease_model

DATA_URL = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv"

COLUMNS = [
    "pregnancies", "glucose", "blood_pressure", "skin_thickness",
    "insulin", "bmi", "diabetes_pedigree", "age", "target"
]


def run():
    df = pd.read_csv(DATA_URL, names=COLUMNS)

    X = df.drop(columns=["target"])
    y = df["target"]

    train_disease_model("diabetes", X, y, balance_classes=True)


if __name__ == "__main__":
    run()