import os
from typing import List

import joblib
import numpy as np
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from sklearn.preprocessing import StandardScaler
from utils.logging import logger

# import mlflow

# MLFLOW_TRACKING_URI="http://localhost:5000"

# # Load the ML model
# mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
# model_uri = os.path.join("models:/", 'exp3_cleaned_standard-xgb',"1" )
# model = mlflow.pyfunc.load_model(model_uri)

model = joblib.load(os.environ.get("MODEL_PATH", "models/model.pkl"))
scaler = joblib.load(os.environ.get("SCALER_PATH", "models/scaler.gz"))

# app = FastAPI(
#     root_path='/diabetes'
# )
app = FastAPI()


class request_body(BaseModel):
    data: List[float]

    class Config:
        schema_extra = {"example": [0.0, 120.0, 74.0, 18.0, 63.0, 30.5, 0.285, 26.0]}


# example_input = {
#     "data": [0.0, 120.0, 74.0, 18.0, 63.0, 30.5, 0.285, 26.0]
# }


@app.get("/")
def home():
    return "API is working."


@app.post("/preloaded_xgb")
async def diabetes_predict(input: request_body):
    x = np.array(input.data).reshape(-1, 8)
    x_scaled = scaler.transform(x)
    logger.info("Make predictions...")
    pred = model.predict(x_scaled)[0]
    result = {}
    if pred == 0:
        result["diabetes result"] = "No diabetes"
    else:
        result["diabetes result"] = "Diabetes"
    return result
