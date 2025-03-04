import base64
from typing import Iterator
import numpy as np
import numpy.typing as npt
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
import cv2
import time


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

frame_header = b"--frame\r\nContent-Type: image/jpeg\r\n\r\n"
frame_footer = b"\r\n"

# Load your images (ensure these paths are correct)
img1 = cv2.imread("img1.bmp")
img2 = cv2.imread("img2.bmp")


@app.get("/stream")
async def stream():
    """
    Stream video frames over HTTP as MJPEG.
    """
    def encode_frame(frame: npt.NDArray[np.uint8]) -> bytes:
        """Encode a frame to JPEG format."""
        success, buffer = cv2.imencode(".jpg", frame)
        if not success:
            raise ValueError("Failed to encode frame")
        return buffer.tobytes()

    def get_streaming_frame(frame: npt.NDArray[np.uint8]) -> bytes:
        """Prepare a complete MJPEG frame."""
        return frame_header + encode_frame(frame) + frame_footer

    def frame_generator() -> Iterator[bytes]:
        """Yield frames in an infinite loop."""
        index = 0
        while True:
            frame = img1 if index % 2 == 0 else img2
            index += 1
            # Slow down the stream for demonstration purposes
            time.sleep(0.5)
            if frame is None:
                continue
            try:
                yield get_streaming_frame(frame)
            except Exception as e:
                # Optionally log the exception
                continue

    return StreamingResponse(
        frame_generator(),
        media_type="multipart/x-mixed-replace; boundary=frame",
    )
    
@app.get("/capture")
def capture():
    """
    Capture a single frame and return it as JPEG along with its HSV conversion.
    """
    frame = img1
    if frame is None:
        return JSONResponse(content={"error": "No image found."}, status_code=404)
    
    # Convert the frame to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Resize image to 640x480
    frame = cv2.resize(frame, (640, 480))
    hsv = cv2.resize(hsv, (640, 480))
    
    # Encode images as JPEG
    success_img, img_buffer = cv2.imencode(".jpg", frame)
    success_hsv, hsv_buffer = cv2.imencode(".jpg", hsv)
    
    if not (success_img and success_hsv):
        return JSONResponse(content={"error": "Failed to encode image."}, status_code=500)
    
    # Convert binary JPEG data to base64 strings for JSON serialization
    img_base64 = base64.b64encode(img_buffer).decode('utf-8')
    hsv_base64 = base64.b64encode(hsv_buffer).decode('utf-8')
    
    body = {
        "image": f"data:image/jpeg;base64,{img_base64}",
        "heatmap": f"data:image/jpeg;base64,{hsv_base64}",
        "processingTime": 1.0,
        "isDetected": False
    }
    
    return JSONResponse(content=body)
