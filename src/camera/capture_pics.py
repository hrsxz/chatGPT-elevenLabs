import base64
import logging
import os
import time
from pathlib import Path

import cv2  # pip install opencv-python
import numpy as np
from PIL import Image  # pip install Pillow

# Calculate the project root path directly
project_root_path = Path(__file__).resolve().parent.parent.parent
filename = project_root_path / "logs/camera.log"
logging.basicConfig(level=logging.DEBUG, filename=filename)


class Capture_Pics:
    """This class use for capturing pics from webcam"""

    def __init__(self, folder=project_root_path / "artifacts/frames"):
        # Folder
        self.folder = project_root_path / "artifacts/frames"

        # Create the frames folder if it doesn't exist
        frames_dir = os.path.join(os.getcwd(), folder)
        os.makedirs(frames_dir, exist_ok=True)

        # Initialize the webcam
        self.cap = cv2.VideoCapture(0)

        # Check if the webcam is opened correctly
        if not self.cap.isOpened():
            raise IOError("Cannot open webcam")

    def capture_one_pic(self, frame_name: str):
        if frame_name != "live":
            # Countdown to capture the image.
            logging.info("📸 Smile for the camera! Capturing 2...")
            time.sleep(1)
            logging.info("📸 Smile for the camera! Capturing 1...")
            time.sleep(0.5)
        ret, frame = self.cap.read()
        if ret:
            # Convert the frame to a PIL image
            pil_img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

            # Resize the image
            max_size = 600
            ratio = max_size / max(pil_img.size)
            new_size = tuple(int(x * ratio) for x in pil_img.size)
            resized_img = pil_img.resize(new_size, Image.LANCZOS)

            # Convert the PIL image back to an OpenCV image
            frame = cv2.cvtColor(np.array(resized_img), cv2.COLOR_RGB2BGR)

            # Save the frame as an image file
            path = f"{self.folder}/{frame_name}.jpg"
            cv2.imwrite(path, frame)

            # Release the camera and close all windows
            self.cap.release()
            cv2.destroyAllWindows()
        else:
            frame = None
            logging.error("Failed to capture image")

        logging.info("📸 Picture saved.")

        return frame

    def frame_to_base64(self, frame):
        # convert the frame to JPEG format
        retval, buffer = cv2.imencode(".jpg", frame)
        if retval:
            # convert the image to bytes and base64 encode it
            jpg_as_text = base64.b64encode(buffer.tobytes()).decode()
            return jpg_as_text
        raise ValueError("Could not convert the frame to JPEG")
