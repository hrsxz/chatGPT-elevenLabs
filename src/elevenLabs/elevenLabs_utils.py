# import base64
import logging
import os
from pathlib import Path

from elevenlabs import generate, play

# Calculate the project root path directly
project_root_path = Path(__file__).resolve().parent.parent.parent
filename = project_root_path / "logs/elevenlabs.log"

logging.basicConfig(level=logging.DEBUG, filename=filename)


class client_elevenlabs:
    """_summary_

    Args:
        play (_type_): _description_
    """

    def __init__(
        self, voice_id="Fq5OJJwxtdJafNydKC4i"
    ):  # default: DPsqCHWEBVTyO9962K8u
        self.api_key = os.getenv("ELEVEN_API_KEY")
        if self.api_key is None:
            # raise Exception("Missing ELEVEN_API_KEY environment variable")
            # W0719: Raising too general exception (broad-exception-raised)
            raise ValueError("Missing ELEVEN_API_KEY environment variable")
        self.headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": self.api_key,
        }

        self.url = "https://api.elevenlabs.io/v1/text-to-speech/" + voice_id

    def play_audio(self, text) -> None:
        """Play audio from the given file path."""
        audio = generate(
            text, voice="DPsqCHWEBVTyO9962K8u", model="eleven_multilingual_v2"
        )

        # random_bytes = os.urandom(30)  # 生成随机字节
        # encoded_bytes = base64.urlsafe_b64encode(random_bytes)  # Base64 编码
        # unique_id = encoded_bytes.decode("utf-8").rstrip("=")  # 解码并去除填充符
        dir_path = project_root_path / "artifacts/audio"  # , unique_id)
        os.makedirs(dir_path, exist_ok=True)
        file_path = os.path.join(dir_path, "audio.wav")

        with open(file_path, "wb") as f:
            f.write(audio)

        play(audio)

    def run(self, response_text: str):
        try:
            logging.info("Elevenlabs process started")
            self.play_audio(response_text)
        # except Exception as e:
        # W0718: Catching too general exception Exception (broad-exception-caught)
        except (ValueError, KeyError) as e:
            logging.exception("Error in the child process: %s", e)


# if __name__ == "__main__":
#     client = client_elevenlabs()
#     client.play_audio("Born and raised in the charming south,\n"
#                       "I can add a touch of sweet southern hospitality\n"
#                       "to your audiobooks and podcasts")
