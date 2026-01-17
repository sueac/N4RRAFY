import tkinter as tk
from tkinter import filedialog
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
import threading
import pygame
import os

# ---------- Setup ----------
load_dotenv()
client = ElevenLabs(api_key=os.getenv("API_KEY"))

pygame.mixer.init()

# ---------- UI logic ----------
def upload_file():
    global words, word_index

    file_path = filedialog.askopenfilename(
        title="Select a file",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )

    if file_path:
        status_label.config(text="AI is thinking...")
        root.update_idletasks()

        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()

        words = text.split()
        word_index = 0
        text_box.delete("1.0", tk.END)

        threading.Thread(target=generate_and_play_audio, args=(text,)).start()
        root.after(500, speak_words)


def generate_and_play_audio(text):
    audio = client.text_to_speech.convert(
        text=text,
        voice_id="JBFqnCBsd6RMkjVDRZzb",
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128",
    )

    with open("output.mp3", "wb") as f:
        for chunk in audio:
            f.write(chunk)

    pygame.mixer.music.load("output.mp3")
    pygame.mixer.music.play()

    status_label.config(text="AI is speaking 🎧")


def speak_words():
    global word_index

    if word_index < len(words):
        text_box.insert(tk.END, words[word_index] + " ")
        text_box.see(tk.END)
        word_index += 1

        root.after(120, speak_words)
    else:
        status_label.config(text="AI finished speaking ✔️")


# ---------- Controls ----------
def stop_audio():
    pygame.mixer.music.stop()
    status_label.config(text="Stopped ⏹️")


# ---------- Tkinter UI ----------
root = tk.Tk()
root.title("AI Reader")
root.geometry("1200x1200")

upload_btn = tk.Button(root, text="Upload File", command=upload_file)
upload_btn.pack(pady=10)

stop_btn = tk.Button(root, text="Stop", command=stop_audio)
stop_btn.pack(pady=5)

status_label = tk.Label(root, text="No file selected")
status_label.pack()

text_box = tk.Text(root, wrap="word", height=20)
text_box.pack(padx=10, pady=10, fill="both", expand=True)

words = []
word_index = 0

root.mainloop()
