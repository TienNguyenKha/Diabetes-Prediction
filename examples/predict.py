import sys

import requests

sys.path.append("..")
from app.utils.logging import logger

API_ENDPOINT = "http://localhost:30001/preloaded_xgb"


def main():
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
    }

    json_data = {
        "data":[0.0, 120.0, 74.0, 18.0,
                        63.0, 30.5, 0.285, 26.0]
    }

    # Post request to prediction endpoint.
    response = requests.post(API_ENDPOINT, headers=headers, json=json_data)
    if response.status_code == 200:
        logger.info("Successful!")
        logger.info(response.json())
    else:
        logger.info("Failed to get prediction!")


if __name__ == "__main__":
    main()