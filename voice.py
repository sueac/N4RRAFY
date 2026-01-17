from dotenv import load_dotenv

from elevenlabs.client import ElevenLabs

from elevenlabs.play import play

import os

load_dotenv()

elevenlabs = ElevenLabs(

  api_key=os.getenv("API_KEY"),

)

audio = elevenlabs.text_to_speech.convert(

    text="We are failing this hackathon.",

    voice_id="JBFqnCBsd6RMkjVDRZzb",

    model_id="eleven_multilingual_v2",

    output_format="mp3_44100_128",

)

with open("output.mp3", "wb") as f:
    for chunk in audio:
        f.write(chunk)

os.system("output.mp3") 