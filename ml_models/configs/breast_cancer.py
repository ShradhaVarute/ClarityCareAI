import pandas as pd
from sklearn.datasets import load_breast_cancer
from pipeline.train import train_disease_model


def run():
    data = load_breast_cancer(as_frame=True)
    X = data.data
    y = data.target  # already 0/1: 0 = malignant, 1 = benign in sklearn's encoding

    return train_disease_model("breast_cancer", X, y)


if __name__ == "__main__":
    run()