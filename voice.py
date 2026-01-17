import requests

API_KEY = "YOUR_API_KEY"
VOICE_ID = "21m00Tcm4TlvDq8ikWAM"

url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

headers = {
    "xi-api-key": API_KEY,
    "Content-Type": "application/json"
}

data = {
    "text": "Hello! This is ElevenLabs text to speech.",
    "voice_settings": {
        "stability": 0.5,
        "similarity_boost": 0.75
    }
}

response = requests.post(url, json=data, headers=headers)

with open("output.mp3", "wb") as f:
    f.write(response.content)

print("Saved output.mp3")
