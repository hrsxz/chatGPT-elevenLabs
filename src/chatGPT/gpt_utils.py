import os
import base64
import errno
import time

from openai import OpenAI


class client_chatGPT:
    """This class summarize the utility methods for chatGPT
    Raises:
        Exception: _description_

    Returns:
        _type_: _description_
    """

    def __init__(self):
        api_key = os.getenv('OPENAI_API_KEY')
        if api_key is None:
            raise Exception("Missing OPENAI_API_KEY environment variable")
        self.client = OpenAI(api_key=api_key)

    def test_connection(self, model_name):
        stream = self.client.chat.completions.create(
            # model="gpt-3.5-turbo-1106" "gpt-4-vision-preview",
            model=model_name,
            messages=[{"role": "user", "content": "who are you? GPT4 or GPT3?"}],
            stream=True,
        )
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                print(chunk.choices[0].delta.content, end="")

    def generate_new_line(self, base64_image):
        return [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Describe this image"},
                    {
                        "type": "image_url",
                        "image_url": f"data:image/jpeg;base64,{base64_image}",
                    },
                    {"type": "text", "text": "用英文和中文双语来回答这个问题"}
                ],
            },
        ]

    def analyze_image_with_GPT(self, base64_image, script):
        response = self.client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "system",
                    "content": """
                    You are Sir David Attenborough.
                    Narrate the picture of the human as if it is a nature documentary.
                    Make it snarky and funny. Don't repeat yourself. Make it short.
                    If I do anything remotely interesting, make a big deal about it!
                    """,
                },
            ]
            + script
            + self.generate_new_line(base64_image),
            max_tokens=500,
        )
        response_text = response.choices[0].message.content
        return response_text

    def encode_image(self, image_path):
        while True:
            try:
                with open(image_path, "rb") as image_file:
                    return base64.b64encode(image_file.read()).decode("utf-8")
            except IOError as e:
                if e.errno != errno.EACCES:
                    # Not a "file in use" error, re-raise
                    raise
                # File is being written to, wait a bit and retry
                time.sleep(0.1)

    def load_image(self, path="./artifacts/frames/frame.jpg"):
        # path to your image
        image_path = os.path.join(os.getcwd(), path)

        # getting the base64 encoding
        base64_image = self.encode_image(image_path)

        return base64_image
