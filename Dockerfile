FROM python:3.9

# Create a folder /app if it doesn't exist,
# the /app folder is the current working directory
WORKDIR /app


COPY ./requirements.txt /app

COPY ./models /app/models

# Copy necessary files to our app
COPY ./src/main.py /app

ENV MODEL_PATH /app/models/model.pkl
ENV SCALER_PATH /app/models/scaler.gz

LABEL maintainer="tiennk"

EXPOSE 30000

# Disable pip cache to shrink the image size a little bit,
# since it does not need to be re-installed
RUN pip install -r requirements.txt --no-cache-dir

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "30000"]
