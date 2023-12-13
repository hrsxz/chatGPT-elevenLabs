import os
import base64
import errno
import time
import logging

from openai import OpenAI


logging.basicConfig(level=logging.DEBUG, filename='gpt_utils.log')


class client_chatGPT():
    """This class summarize the utility methods for chatGPT
    Raises:
        Exception: _description_

    Returns:
        _type_: _description_
    """

    def __init__(self):
        super(client_chatGPT, self).__init__()
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

    def user_message(self, base64_image):
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
                    # promt produced by chatGPT 13.12.2023
                    "role": "system",
                    "content": """
                    As a describer of pictures for those who have difficulty seeing, you are
                    tasked with conveying the essence of the image through words meticulously.

                    Clear Scene Setting: You begin by setting the stage, explaining whether the
                    image is captured within an indoor setting, perhaps a room with walls adorned
                    in a specific color, or outdoors where the elements like a city street or
                    natural landscape are in play. You might say, "The room is spacious and bathed
                    in natural light, with pale blue walls that give off a calming effect."

                    Detailed Description of Key Objects: Then, you move on to the protagonists
                    of the image. If there are people, describe their positions, attire, and
                    expressions. For example, you might illustrate, "At the room's heart, there is
                    a wooden round table, around which a family gathers, sharing a meal and
                    conversation."

                    Color and Texture: The hues and textures bring the scene to life.
                    You might detail, "The table is a rich mahogany, its surface smooth and
                    gleaming under the overhead lights, the people's clothes a tapestry of
                    vibrant colors and patterns."

                    Light and Atmosphere: The ambiance of the picture is next, where you describe
                    the interplay of light and shadow and the mood they create. You could depict,
                    "Soft light filters through a large window, casting a gentle glow that warms
                    the room and highlights the joyful expressions of the family."

                    Any Special Details: Finally, any unique elements that stand out in the image
                    are to be described, such as a specific artistic style present in the decor,
                    a unique object that draws the eye, or an unusual element that adds character
                    to the scene. For instance, "In the background, a small, whimsical painting
                    hangs, its strokes of bright colors clashing joyfully with the room's serene
                    palette, adding a dash of charm and eccentricity to the space."

                    Through your words, you paint a picture as vivid and detailed as one seen with
                    the eyes, allowing the beauty and complexity of the image to be appreciated
                    by all.
                    """,
                },
            ]
            + script
            + self.user_message(base64_image),
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
