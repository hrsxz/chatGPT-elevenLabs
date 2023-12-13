import os
import base64

from elevenlabs import generate, play


class client_elevenlabs():
    """_summary_

    Args:
        play (_type_): _description_
    """
    def __init__(self, voice_id="DPsqCHWEBVTyO9962K8u"):
        self.api_key = os.getenv('ELEVEN_API_KEY')
        if self.api_key is None:
            raise Exception("Missing ELEVEN_API_KEY environment variable")
        self.headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": self.api_key
        }

        self.url = "https://api.elevenlabs.io/v1/text-to-speech/" + voice_id

    def play_audio(self, text):
        audio = generate(text, voice="DPsqCHWEBVTyO9962K8u")

        unique_id = base64.urlsafe_b64encode(os.urandom(30)).decode("utf-8").rstrip("=")
        dir_path = os.path.join("artifacts/audio", unique_id)
        os.makedirs(dir_path, exist_ok=True)
        file_path = os.path.join(dir_path, "audio.wav")

        with open(file_path, "wb") as f:
            f.write(audio)

        play(audio)


if __name__ == "__main__":
    client = client_elevenlabs()
    client.play_audio("Born and raised in the charming south,\n"
                      "I can add a touch of sweet southern hospitality\n"
                      "to your audiobooks and podcasts")
