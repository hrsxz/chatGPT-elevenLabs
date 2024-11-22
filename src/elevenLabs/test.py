import os

from elevenlabs import play

dir_path = os.path.join("artifacts/audio")  # , unique_id)
os.makedirs(dir_path, exist_ok=True)
file_path = os.path.join(dir_path, "audio.wav")

with open(file_path, "rb") as f:
    audio = f.read()

play(audio)

print("done")
