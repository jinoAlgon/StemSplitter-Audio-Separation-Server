# Python 3.8 image
FROM python:3.8-slim

# working directory inside the container
WORKDIR /app

# requirements file into the container
COPY requirements.txt .

# Installing system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libsndfile1 \
        ffmpeg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Installing Python dependencies
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copying the application code into the container
COPY audio_api.py audio_processing.py ./
COPY cert.pem .
COPY key.pem .

# Setting the Flask app environment variable
ENV FLASK_APP=audio_api.py

# Expose the port the app will run on
EXPOSE 5000

CMD ["python", "audio_api.py"]
