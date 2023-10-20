from time import sleep

import requests
from utils.logging import logger


def predict():
    logger.info("Sending POST requests!")
    input = {
        "data": [0.0, 120.0, 74.0, 18.0, 63.0, 30.5, 0.285, 26.0],
    }
    response = requests.post(
        "http://tiennkapp.org.m1/preloaded_xgb",
        headers={
            "accept": "application/json",
        },
        json=input,
    )


if __name__ == "__main__":
    while True:
        predict()
        sleep(0.5)
