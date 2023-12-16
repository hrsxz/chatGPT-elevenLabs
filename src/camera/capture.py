import time
import os

from capture_pics import Capture_Pics

# Folder
folder = "artifacts/frames"

# Create the frames folder if it doesn't exist
frames_dir = os.path.join(os.getcwd(), folder)
os.makedirs(frames_dir, exist_ok=True)

# Wait for the camera to initialize and adjust light levels
time.sleep(2)

while True:
    capture_image = Capture_Pics()
    # capture one picture
    frame = capture_image.capture_one_pic("live")

    # Wait for 1 seconds
    time.sleep(0.1)
