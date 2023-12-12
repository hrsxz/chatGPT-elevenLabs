from src.chatGPT import gpt_utils
from src.elevenLabs import elevenLabs_utils

client_channel = gpt_utils.client_chatGPT()

# client_channel.test_connection(model_name="gpt-4-vision-preview")

base64_image = client_channel.load_image(path="./artifacts/frames/frame.jpg")
response_text = client_channel.analyze_image_with_GPT(base64_image, [])
print(response_text)

client = elevenLabs_utils.client_elevenlabs()
client.play_audio(response_text)
