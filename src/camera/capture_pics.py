import os
import cv2  # pip install opencv-python
import numpy as np

from PIL import Image  # pip install Pillow


class Capture_Pics():
    """This class use for capturing pics from webcam
    """
    def __init__(self, folder="artifacts/frames"):
        # Folder
        self.folder = "artifacts/frames"

        # Create the frames folder if it doesn't exist
        frames_dir = os.path.join(os.getcwd(), folder)
        os.makedirs(frames_dir, exist_ok=True)

        # Initialize the webcam
        self.cap = cv2.VideoCapture(0)

        # Check if the webcam is opened correctly
        if not self.cap.isOpened():
            raise IOError("Cannot open webcam")

    def capture_one_pic(self):
        ret, frame = self.cap.read()
        if ret:
            # Convert the frame to a PIL image
            pil_img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

            # Resize the image
            max_size = 800
            ratio = max_size / max(pil_img.size)
            new_size = tuple([int(x*ratio) for x in pil_img.size])
            resized_img = pil_img.resize(new_size, Image.LANCZOS)

            # Convert the PIL image back to an OpenCV image
            frame = cv2.cvtColor(np.array(resized_img), cv2.COLOR_RGB2BGR)

            # Save the frame as an image file
            print("📸 Smile for the camera! Capturing and saving the image.")
            path = f"{self.folder}/frame.jpg"
            cv2.imwrite(path, frame)
        else:
            print("Failed to capture image")
