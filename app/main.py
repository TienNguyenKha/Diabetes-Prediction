import os
from time import time
from typing import List

import joblib
import numpy as np
from fastapi import FastAPI, File, UploadFile
from opentelemetry import metrics
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from opentelemetry.metrics import set_meter_provider
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from prometheus_client import start_http_server
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

# Start Prometheus client
start_http_server(port=8099, addr="0.0.0.0")
# Service name is required for most backends
resource = Resource(attributes={SERVICE_NAME: "diabetes-prediction-service"})

# Exporter to export metrics to Prometheus
reader = PrometheusMetricReader()

# Meter is responsible for creating and recording metrics
provider = MeterProvider(resource=resource, metric_readers=[reader])
set_meter_provider(provider)
meter = metrics.get_meter("diabetespred", "0.1.1")

# Create your first counter
counter = meter.create_counter(
    name="diabetespred_request_counter", description="Number of diabetespred requests"
)

histogram = meter.create_histogram(
    name="diabetespred_response_histogram",
    description="diabetespred response histogram",
    unit="seconds",
)
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
    # Mark the starting point for the response
    starting_time = time()

    x = np.array(input.data).reshape(-1, 8)
    x_scaled = scaler.transform(x)
    logger.info("Make predictions...")
    pred = model.predict(x_scaled)[0]
    result = {}
    if pred == 0:
        result["diabetes result"] = "No diabetes"
    else:
        result["diabetes result"] = "Diabetes"

    label = {"api": "/diabetespred"}

    # Increase the counter
    counter.add(10, label)

    # Mark the end of the response
    ending_time = time()
    elapsed_time = ending_time - starting_time

    # Add histogram
    logger.info(elapsed_time)
    histogram.record(elapsed_time, label)

    return result
