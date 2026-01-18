import tkinter as tk
from tkinter import filedialog
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
import threading
import pygame
import os
from mutagen.mp3 import MP3

is_paused = False
audio_started = threading.Event()
word_delay_ms = 180
current_highlight = None



# ---------- Setup ----------
load_dotenv()
client = ElevenLabs(api_key=os.getenv("API_KEY"))

pygame.mixer.init()

def generate_and_play_audio(text):
    global word_delay_ms

    audio = client.text_to_speech.convert(
        text=text,
        voice_id="JBFqnCBsd6RMkjVDRZzb",
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128",
    )

    with open("output.mp3", "wb") as f:
        for chunk in audio:
            f.write(chunk)

    mp3 = MP3("output.mp3")
    duration = mp3.info.length  # seconds

    word_delay_ms = int((duration / len(words)) * 1000)

    pygame.mixer.music.load("output.mp3")
    pygame.mixer.music.play()
    audio_started.set()


def upload_file():
    global words, word_index, is_paused
    audio_started.clear()
    is_paused = False

    file_path = filedialog.askopenfilename(
        title="Select a text file",
        filetypes=[("Text files", "*.txt")]
    )

    

    if not file_path:
        return
    

        with open(file_path, 'r') as file:
            text = file.read()

        words = text.split()
        word_index = 0

        root.after(2000, speak_words)  # wait 2 seconds before speaking

def speak_words():
    global word_index, current_highlight

    if is_paused:
        return  # ⛔ stop advancing text while paused

    if word_index < len(words):
        text_box.insert(tk.END, words[word_index] + " ")
        text_box.see(tk.END)  # auto-scroll
        word_index += 1

        # control speaking speed (milliseconds)
        root.after(200, speak_words)
    else:
        status_label.config(text="AI finished speaking ✔️")

# Create window
root = tk.Tk()
root.title("AI Reader")
root.geometry("1200x1200")

# ---------------- BACKGROUND (JPEG WORKS) ----------------
bg_image = Image.open("images/bruh.jpg")# JPEG is OK
bg_image = bg_image.resize((700, 500))
bg_photo = ImageTk.PhotoImage(bg_image)

background_label = tk.Label(root, image=bg_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)
background_label.lower()  # send to back

# ---------------- UI ----------------
upload_btn = tk.Button(root, text="Upload File", command=upload_file)
upload_btn.pack(pady=10)

controls = tk.Frame(root)
controls.pack(pady=10)

start_btn = tk.Button(controls, text="▶️ Start / Resume", command=start_audio)
start_btn.pack(side="left", padx=5)

pause_btn = tk.Button(controls, text="⏸️ Pause", command=pause_audio)
pause_btn.pack(side="left", padx=5)


status_label = tk.Label(
    root,
    text="No file selected",
    fg="white",
    bg="black"
)
status_label.pack()

text_box = tk.Text(root, wrap="word", height=10)
text_box.pack(padx=10, pady=10, fill="both", expand=True)

# ---------------- STATE ----------------
words = []
word_index = 0

root.mainloop()
