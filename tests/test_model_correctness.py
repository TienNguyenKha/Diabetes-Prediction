import joblib
import pandas as pd
import numpy as np

# Define path to our model
MODEL_DIR = "models"

def test_model_correctness():
    clf = joblib.load(f"{MODEL_DIR}/model.pkl")
    data = [-1.15332192, -0.05564105,  0.12035144, -1.25882277, -1.08285125,
        -0.28446352, -0.49468374, -0.52559768]
    x= np.array(data).reshape(-1, 8)
    pred=clf.predict(x)[0]
    assert pred == 0