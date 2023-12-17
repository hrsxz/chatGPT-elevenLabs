"""Run this file, and you will connect to the ElevenLabs server to convert the given text
into voice and save it under artifacts/audio.
"""
import requests


CHUNK_SIZE = 1024
# url = "https://api.elevenlabs.io/v1/text-to-speech/DPsqCHWEBVTyO9962K8u"  # 3uKAXEQt3XkLH6uWDheu

url = "https://api.elevenlabs.io/v1/text-to-speech/Fq5OJJwxtdJafNydKC4i"  # GH Fq5OJJwxtdJafNydKC4i
headers = {
    "Accept": "audio/mpeg",
    "Content-Type": "application/json",
    "xi-api-key": "08f82e1c5aa822594c7c96103652060b"
}

data = {
    "text": "感觉不太像？",
    "model_id": "eleven_multilingual_v2",
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
