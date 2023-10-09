import joblib
import numpy as np

# Define path to our model
MODEL_DIR = "models"


def test_model_correctness():
    clf = joblib.load(f"{MODEL_DIR}/model.pkl")
    scaler = joblib.load(f"{MODEL_DIR}/scaler.gz")
    data = [0.0, 120.0, 74.0, 18.0, 63.0, 30.5, 0.285, 26.0]
    x = np.array(data).reshape(-1, 8)
    x_scaled = scaler.transform(x)
    pred = clf.predict(x_scaled)[0]
    assert pred == 0
