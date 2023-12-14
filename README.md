# StemSplitter: Audio Separation Server

StemSplitter is a powerful and efficient server designed for separating audio tracks into their individual components, such as vocals, drums, and instruments. Leveraging the capabilities of the Demucs deep learning model within a Flask-based framework, this server provides an API endpoint for processing audio files.

## Features

- **Advanced Audio Separation**: Utilizes the state-of-the-art Demucs model for accurate and efficient audio track separation.
- **Secure API**: The server offers a secure API endpoint for uploading audio files and receiving the processed output.
- **Docker Integration**: Containerized with Docker for easy setup, deployment, and scalability.
- **Customizable**: Easy to modify and extend based on individual project requirements.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

What you need to install the software:

- Docker
- Python 3.8+
- pip (Python package manager)

### Installation

1. **Clone the Repository**

    ```bash
    git clone https://github.com/jinoAlgon/StemSplitter-Audio-Separation-Server.git
    cd StemSplitter
    ```

2. **Build and Run the Docker Container**

    ```bash
    docker build -t audio-server .
    docker run -p 5000:5000 audio-server
    ```

The server will start running on `localhost` at port `5000`.

## Usage

To separate an audio file into stems:

1. Send a `POST` request to `http://localhost:5000/separate` with the audio file.
2. Receive the processed file as a zip containing the separated tracks.

Example using `curl`:

```bash
curl -X POST -F "file=@path_to_your_audio_file.mp3" http://localhost:5000/separate -o separated.zip
