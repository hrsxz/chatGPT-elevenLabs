"""Run this file, and you will connect to the ElevenLabs server to convert the given text
into voice and save it under artifacts/audio.
"""
import requests


CHUNK_SIZE = 1024
url = "https://api.elevenlabs.io/v1/text-to-speech/DPsqCHWEBVTyO9962K8u"  # 3uKAXEQt3XkLH6uWDheu

headers = {
    "Accept": "audio/mpeg",
    "Content-Type": "application/json",
    "xi-api-key": "08f82e1c5aa822594c7c96103652060b"
}

data = {
    "text": "Born and raised in the charming south,\n"
            "I can add a touch of sweet southern hospitality\n"
            "to your audiobooks and podcasts",
    "model_id": "eleven_monolingual_v1",
    "voice_settings": {
        "stability": 0.5,
        "similarity_boost": 0.5
    }
}

response = requests.post(url, json=data, headers=headers)
with open('./artifacts/audio/output.mp3', 'wb') as f:
    for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
        if chunk:
            f.write(chunk)
