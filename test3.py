from youtube_transcript_api import YouTubeTranscriptApi
from googletrans import Translator
from pytube import YouTube
import os
import tkinter as tk
from tkinter import messagebox
import tkinter.filedialog
from moviepy.editor import VideoFileClip
import moviepy.editor as mp
import speech_recognition as sr
from pydub import AudioSegment
import time
import webbrowser

translator = Translator()


# Function to translate text
def translate_text():
    # Clear the text widget
    output_text.delete(1.0, tk.END)

    # Get the YouTube video URL from the entry widget
    video_url = url_entry.get()

    # Get selected language code from the option menu
    selected_language_code = language_options.get()

    # Get transcript of the video
    try:
        tx = YouTubeTranscriptApi.get_transcript(video_url, languages=[selected_language_code])
    except Exception as e:
        messagebox.showerror("Error", f"Could not retrieve transcript: {str(e)}")
        return

    original_text = ""  # Variable to store original text
    translated_text = ""  # Variable to store translated text

    for i in tx:
        outtxt = i['text']
        original_text += outtxt + "\n"  # Concatenate original text

        try:
            # Translate text to Vietnamese
            translated_text += translator.translate(outtxt, src='auto', dest='vi').text + "\n"  # Concatenate translated text
        except Exception as e:
            output_text.insert(tk.END, f"Error occurred: {str(e)}\n")
            time.sleep(1)  # Wait for 1 second before retrying

    # Display original text and translated text in the text widget
    output_text.insert(tk.END,
                       f"Original Text:\n{original_text}\nTranslated Text:\n{translated_text}\n\n")

    # Show success message in a dialog box
    messagebox.showinfo("Translation Complete",
                        "Đã dịch video sang tiếng Việt thành công.")


# Function to clear text widget
def clear_text():
    url_entry.delete(0, tk.END)  # Xóa nội dung trong url_entry
    output_text.config(state=tk.NORMAL)  # Cho phép chỉnh sửa nội dung trong output_text
    output_text.delete(1.0, tk.END)  # Xóa nội dung trong output_text
    output_text.config(state=tk.DISABLED)  # Không cho phép chỉnh sửa nội dung trong output_text sau khi xóa


# Function to download video
def download_video():
    # Get the YouTube video URL from the entry widget
    video_url = url_entry.get()

    try:
        # Create a YouTube object with the provided URL
        yt = YouTube(video_url)

        # Select the highest resolution stream for downloading
        video = yt.streams.get_highest_resolution()

        # Define the directory to save the video
        save_path = "downloads"

        # Check if the directory exists, if not, create it
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        # Download the video to the selected directory
        video_file = video.download(save_path)

        # Convert the downloaded video to MP4 format
        mp4_file = os.path.join(save_path, os.path.splitext(os.path.basename(video_file))[0] + ".mp4")

        # Show success message in a dialog box
        messagebox.showinfo("Download Complete", "Video đã được tải về và chuyển đổi sang MP4 thành công!")
    except Exception as e:
        # Show error message if there is an error during download
        messagebox.showerror("Error", f"Lỗi khi tải video: {str(e)}")


# Function to show downloaded videos
def show_downloaded_videos():
    # Create a new window for showing downloaded videos
    videos_window = tk.Toplevel(root)
    videos_window.title("Downloaded Videos")

    # Create a frame to contain video list and scrollbar
    video_frame = tk.Frame(videos_window)
    video_frame.pack(fill=tk.BOTH, expand=True)

    # Create a listbox to display downloaded videos
    video_listbox = tk.Listbox(video_frame, selectmode=tk.SINGLE)
    video_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Create a scrollbar for the listbox
    scrollbar = tk.Scrollbar(video_frame, orient=tk.VERTICAL, command=video_listbox.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Configure the listbox to use the scrollbar
    video_listbox.config(yscrollcommand=scrollbar.set)

    # Get list of files in the "downloads" directory
    download_dir = "downloads"
    if os.path.exists(download_dir):
        files = os.listdir(download_dir)
        mp4_files = [file for file in files if file.endswith(".mp4")]

        # Populate the listbox with mp4 files
        for mp4_file in mp4_files:
            video_listbox.insert(tk.END, mp4_file)

    # Function to play selected video
    def play_video():
        selected_index = video_listbox.curselection()
        if selected_index:
            selected_video = video_listbox.get(selected_index)
            selected_video_path = os.path.join(download_dir, selected_video)
            os.startfile(selected_video_path)  # Open the video file with default application

    # Button to play selected video
    play_button = tk.Button(videos_window, text="Play", command=play_video)
    play_button.pack(pady=5)

def convert_audio_to_text(language_code):
    recognizer = sr.Recognizer()
    file_path = url_entry.get()

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
                # Update the text_output widget with recognized text
                output_text.config(state=tk.NORMAL)
                # Check if "Translated MP4 File Text:" has been inserted
                if not output_text.get(1.0, tk.END).startswith("Translated MP4 File Text:"):
                    output_text.insert(tk.END, "Translated MP4 File Text: \n")
                output_text.insert(tk.END, f"{text}")
                output_text.config(state=tk.DISABLED)
            except sr.UnknownValueError:
                pass
            except sr.RequestError as e:
                print(f"Error: {e}")

        # Clean up - delete temporary WAV file
        os.remove(f"chunk_{i}.wav")

    # Clean up - delete temporary WAV file
    os.remove(audio_file_path)


# Function to select file
def select_file():
    file_path = tk.filedialog.askopenfilename(filetypes=[("MP4 files", "*.mp4")])
    url_entry.delete(0, tk.END)
    url_entry.insert(tk.END, file_path)


# Function to open YouTube homepage
def open_youtube():
    webbrowser.open("https://www.youtube.com")


# Create main window
root = tk.Tk()
root.title("YouTube Transcript Translation")

# Label for URL entry
url_label = tk.Label(root, text="Enter YouTube Video URL or Choose MP4 File:")
url_label.pack()

# Entry widget for URL input
url_entry = tk.Entry(root, width=50)
url_entry.pack()

# Button to select file
select_file_button = tk.Button(root, text="Choose File", command=select_file)
select_file_button.pack(pady=5)

# Get all language codes and their names
all_languages = ["af", "ak", "sq", "am", "ar", "hy", "as", "ay", "az", "bn", "eu", "be", "bho", "bs", "bg", "my",
                 "ca", "ceb", "zh-Hans", "zh-Hant", "co", "hr", "cs", "da", "dv", "nl", "en", "eo", "et", "ee",
                 "fil", "fi", "fr", "gl", "lg", "ka", "de", "el", "gn", "gu", "ht", "ha", "haw", "iw", "hi", "hmn",
                 "hu", "is", "ig", "id", "ga", "it", "ja", "jv", "kn", "kk", "km", "rw", "ko", "kri", "ku", "ky",
                 "lo", "la", "lv", "ln", "lt", "lb", "mk", "mg", "ms", "ml", "mt", "mi", "mr", "mn", "ne", "nso",
                 "no", "ny", "or", "om", "ps", "fa", "pl", "pt", "pa", "qu", "ro", "ru", "sm", "sa", "gd", "sr",
                 "sn", "sd", "si", "sk", "sl", "so", "st", "es", "su", "sw", "sv", "tg", "ta", "tt", "te", "th",
                 "ti", "ts", "tr", "tk", "uk", "ur", "ug", "uz", "vi", "cy", "fy", "xh", "yi", "yo", "zu"]

# Option menu for selecting language
language_options = tk.StringVar(root)
language_options.set("en")  # Default language is English
language_label = tk.Label(root, text="Select Language:")
language_label.pack()
language_menu = tk.OptionMenu(root, language_options, *all_languages)
language_menu.pack()

# Create text widget to display translated text
output_text = tk.Text(root, wrap="word", height=20, width=80)
output_text.pack()

# Create a frame to contain buttons
button_frame = tk.Frame(root)
button_frame.pack()

# Button to trigger translation
translate_button = tk.Button(button_frame, text="Translate", command=translate_text)
translate_button.grid(row=0, column=0, padx=5, pady=5)

# Button to clear text widget
clear_button = tk.Button(button_frame, text="Clear", command=clear_text)
clear_button.grid(row=0, column=1, padx=5, pady=5)

# Button to trigger download
download_button = tk.Button(button_frame, text="Download", command=download_video)
download_button.grid(row=0, column=2, padx=5, pady=5)

# Button to show downloaded videos
show_button = tk.Button(button_frame, text="Show Downloaded Videos", command=show_downloaded_videos)
show_button.grid(row=0, column=3, padx=5, pady=5)

# Button to open YouTube homepage
youtube_button = tk.Button(button_frame, text="YouTube", command=open_youtube)
youtube_button.grid(row=0, column=4, padx=5, pady=5)

# Button to add subtitles
convert_button = tk.Button(button_frame, text="Convert", command=lambda: convert_audio_to_text(language_options.get()))
convert_button.grid(row=0, column=5, padx=5, pady=5)

# Center the frame containing buttons
button_frame.grid_columnconfigure(0, weight=1)
button_frame.grid_columnconfigure(1, weight=1)
button_frame.grid_columnconfigure(2, weight=1)
button_frame.grid_columnconfigure(3, weight=1)
button_frame.grid_columnconfigure(4, weight=1)
button_frame.grid_columnconfigure(5, weight=1)

# Run the main event loop
root.mainloop()
