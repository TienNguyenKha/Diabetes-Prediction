import joblib
import numpy as np
import os
from typing import List
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel

# import mlflow

# MLFLOW_TRACKING_URI="http://localhost:5000"

# # Load the ML model
# mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
# model_uri = os.path.join("models:/", 'exp3_cleaned_standard-xgb',"1" )
# model = mlflow.pyfunc.load_model(model_uri)

model = joblib.load(
    os.environ.get('MODEL_PATH', "models/model.pkl")
)

# app = FastAPI(
#     root_path='/diabetes'
# )
app = FastAPI()

class request_body(BaseModel):
    data: List[float]
    
example_input = {
    "data": [-1.15332192, -0.05564105,  0.12035144, -1.25882277, -1.08285125,
        -0.28446352, -0.49468374, -0.52559768]
}

@app.get("/")
def home():
    return "API is working as expected."

@app.post("/preloaded_xgb")
async def diabetes_predict(input : request_body):
    x= np.array(input.data).reshape(-1, 8)
    pred=model.predict(x)[0]
    result={}
    if pred == 0:
        result['diabetes result']= 'No diabetes'
    else:
        result['diabetes result']= 'Diabetes'
    return result

