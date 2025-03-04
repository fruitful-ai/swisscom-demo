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
    "image": f"data:image/jpeg;base64,{img_base64}",
    "heatmap": f"data:image/jpeg;base64,{hsv_base64}",
    "processingTime": 1.0,
    "isDetected": False
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