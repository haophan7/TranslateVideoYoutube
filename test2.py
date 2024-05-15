import tkinter as tk
from tkinter import filedialog
import os
import moviepy.editor as mp
import speech_recognition as sr
from pydub import AudioSegment
from pydub.silence import split_on_silence

def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("MP4 files", "*.mp4")])
    entry.delete(0, tk.END)
    entry.insert(tk.END, file_path)

def convert_audio_to_text(language_code):
    recognizer = sr.Recognizer()
    file_path = entry.get()

    # Extract audio from MP4
    video = mp.VideoFileClip(file_path)
    audio_file_path = file_path.replace(".mp4", ".wav")
    video.audio.write_audiofile(audio_file_path)

    # Load audio file using pydub
    audio = AudioSegment.from_wav(audio_file_path)

    # Define duration of each chunk (in milliseconds)
    chunk_duration = 30 * 1000  # 30 seconds

    # Process each chunk separately
    full_text = ""
    for i, start_time in enumerate(range(0, len(audio), chunk_duration)):
        # Extract chunk
        chunk = audio[start_time:start_time+chunk_duration]

        # Export chunk as WAV file
        chunk.export(f"chunk_{i}.wav", format="wav")

        with sr.AudioFile(f"chunk_{i}.wav") as source:
            chunk_audio_data = recognizer.record(source, duration=len(chunk)/1000)  # Adjusted to process the whole chunk
            try:
                # Recognize using Google Speech Recognition with specified language
                text = recognizer.recognize_google(chunk_audio_data, language=language_code)
                full_text += text + " "
            except sr.UnknownValueError:
                pass
            except sr.RequestError as e:
                print(f"Error: {e}")

        # Clean up - delete temporary WAV file
        os.remove(f"chunk_{i}.wav")

    # Save the full text to a TXT file
    save_file_path = file_path.replace(".mp4", ".txt")
    with open(save_file_path, "w", encoding="utf-8") as f:  # Ensure UTF-8 encoding for non-English characters
        f.write(full_text)
        text_output.config(state=tk.NORMAL)
        text_output.delete("1.0", tk.END)
        text_output.insert(tk.END, "Text saved to: " + save_file_path)
        text_output.config(state=tk.DISABLED)

    # Clean up - delete temporary WAV file
    os.remove(audio_file_path)


# Create the main window
root = tk.Tk()
root.title("Audio to Text Converter")

# Create widgets
label = tk.Label(root, text="Select an MP4 audio file:")
label.pack()

entry = tk.Entry(root, width=50)
entry.pack()

browse_button = tk.Button(root, text="Browse", command=browse_file)
browse_button.pack()

language_label = tk.Label(root, text="Select language code (e.musics., en for English, fr for French):")
language_label.pack()

language_entry = tk.Entry(root, width=10)
language_entry.pack()

convert_button = tk.Button(root, text="Convert", command=lambda: convert_audio_to_text(language_entry.get()))
convert_button.pack()

text_output = tk.Text(root, height=10, width=50)
text_output.config(state=tk.DISABLED)
text_output.pack()

# Start the GUI
root.mainloop()
