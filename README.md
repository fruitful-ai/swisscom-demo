# Image Streaming Demo

# Getting Started

```sh
pip install -r requirements.txt
```

# Endpoints

Image stream: `http://localhost:8012/stream`
Response: byte stream


Capture image: `http://localhost:8012/capture`
Response: 

```json
{
    "image": "data:image/jpeg;base64,img...",
    "heatmap": "data:image/jpeg;base64,img...",
    "processingTime": 1.0,
    "isDetected": false
}
```

# Run locally
```bash
./server.sh
```

# Build the container

```sh
docker build -t vision-demo:vX .
```

# Run the container

```sh
docker run --rm -p 8012:8012 vision-demo:vX
```