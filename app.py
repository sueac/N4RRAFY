import tkinter as tk
from tkinter import filedialog

def upload_file():
    global words, word_index

    file_path = filedialog.askopenfilename(
        title="Select a file",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )

    if file_path:
        status_label.config(text="AI is thinking...")
        root.update_idletasks()

        with open(file_path, 'r') as file:
            text = file.read()

        words = text.split()
        word_index = 0

        root.after(2000, speak_words)  # wait 2 seconds before speaking

def speak_words():
    global word_index

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
root.geometry("500x300")

upload_btn = tk.Button(root, text="Upload File", command=upload_file)
upload_btn.pack(pady=10)

status_label = tk.Label(root, text="No file selected")
status_label.pack()

text_box = tk.Text(root, wrap="word", height=10)
text_box.pack(padx=10, pady=10, fill="both", expand=True)

words = []
word_index = 0

root.mainloop()
