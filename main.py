from youtube_transcript_api import YouTubeTranscriptApi
from googletrans import Translator
from pytube import YouTube
import os
import tkinter as tk
from tkinter import messagebox
import tkinter.filedialog
from PIL import Image, ImageTk
import moviepy.editor as mp
import speech_recognition as sr
from pydub import AudioSegment
import time
import webbrowser
import subprocess

translator = Translator()


# Function to translate text
def translate_text():
    # Clear the text widget
    output_text.delete(1.0, tk.END)

    # Get the YouTube video URL from the entry widget
    video_url = url_entry.get()

    # Extract video ID from the URL
    video_id = video_url.split("v=")[1].split("&")[0]

    # Get selected language code from the option menu
    selected_language_code = language_options.get()

    # Get transcript of the video
    try:
        tx = YouTubeTranscriptApi.get_transcript(video_id, languages=[selected_language_code])
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
    text_input.delete(1.0, tk.END)  # Xóa nội dung trong text_input
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

    # Function to delete selected video
    def delete_video():
        selected_index = video_listbox.curselection()
        if selected_index:
            selected_video = video_listbox.get(selected_index)
            selected_video_path = os.path.join(download_dir, selected_video)

            # Hiển thị hộp thoại thông báo
            confirm_delete = messagebox.askyesno("Confirm Delete",
                                                 f"Bạn có chắc chắn muốn xóa file {selected_video} không?")

            # Xác nhận người dùng muốn xóa file
            if confirm_delete:
                os.remove(selected_video_path)  # Xóa file video đã chọn
                # Xóa video đã xóa khỏi listbox
                video_listbox.delete(selected_index)

    # Create a frame to contain buttons
    button_frame = tk.Frame(videos_window)
    button_frame.pack()

    # Button to play selected video
    play_button = tk.Button(button_frame, text="Play", command=play_video)
    play_button.pack(side=tk.LEFT, padx=5)  # Đặt nút "Play" bên trái và thêm một khoảng cách ngang

    # Button to delete selected video
    delete_button = tk.Button(button_frame, text="Delete", command=delete_video)
    delete_button.pack(side=tk.LEFT, padx=5)  # Đặt nút "Delete" bên phải của nút "Play" và thêm một khoảng cách ngang

    # Center the frame containing buttons
    button_frame.pack(pady=10)  # Thêm một khoảng cách dọc giữa các nút và đáy cửa sổ


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


# Function to perform translation
def perform_translation():
    # Clear the text widget
    output_text.delete(1.0, tk.END)

    # Get the text from the text widget
    input_text = text_input.get("1.0", tk.END).strip()

    # Get selected language code from the option menu
    selected_language_code = language_options.get()

    try:
        # Check if selected language is "auto", if yes, detect language
        if selected_language_code == "auto":
            detected_language = translator.detect(input_text).lang
            if detected_language == "vi":
                messagebox.showerror("Error", "Lỗi: Vui lòng chọn ngôn ngữ đầu vào khác tiếng Việt.")
                return
        else:
            # Check if selected language matches with detected language of the text
            detected_language = translator.detect(input_text).lang
            if detected_language != selected_language_code:
                messagebox.showerror("Error", f"Lỗi: Ngôn ngữ được chọn không phù hợp với ngôn ngữ của văn bản ({detected_language}).")
                return

        # Translate text to Vietnamese using Google Translate
        translated_text = translator.translate(input_text, src=detected_language, dest='vi').text

        # Display translated text in the text widget
        output_text.config(state=tk.NORMAL)
        # Insert the translated text into the output_text widget
        output_text.insert(tk.END, f"Translated Text:\n{translated_text}\n\n")
        output_text.config(state=tk.DISABLED)

        # Show success message in a dialog box
        messagebox.showinfo("Translation Complete", "Đã dịch văn bản sang tiếng Việt thành công.")
    except Exception as e:
        # Show error message if there is an error during translation
        messagebox.showerror("Error", f"Lỗi khi dịch văn bản: {str(e)}")


# Function to check language of input text
def check_language():
    # Get the text from the text widget
    input_text = text_input.get("1.0", tk.END).strip()

    try:
        # Create translator object
        translator = Translator()

        # Detect language using Google Translate
        detected_language = translator.detect(input_text).lang

        # Set detected language as selected language in option menu
        language_options.set(detected_language)

        # Show the detected language in a message box
        messagebox.showinfo("Detected Language", f"The input text is in {detected_language.upper()} language.")
    except Exception as e:
        # Show error message if there is an error during language detection
        messagebox.showerror("Error", f"Error detecting language: {str(e)}")


# Function to open Facebook homepage
def open_facebook():
    webbrowser.open("https://www.facebook.com")


# Function to open Twitter homepage
def open_twitter():
    webbrowser.open("https://www.twitter.com")


# Function to open Instagram homepage
def open_instagram():
    webbrowser.open("https://www.instagram.com")


# Function to open Google homepage
def open_google():
    webbrowser.open("https://www.google.com")


# Function to open Tiktok homepage
def open_tiktok():
    webbrowser.open("https://www.tiktok.com")


# Function to open We chat homepage
def open_wechat():
    webbrowser.open("https://www.wechat.com")


# Function to open Zing MP3 homepage
def open_zingmp3():
    webbrowser.open("https://www.zingmp3.vn")


# Function to open Spotify homepage
def open_spotify():
    webbrowser.open("https://www.spotify.com")


# Function to open Thap Cam TV homepage
def open_thapcamtv():
    webbrowser.open("https://live9.thapcam4.net/")


# Function to open the game window
def open_game_window():
    # Create a new window for the game
    game_window = tk.Toplevel(root)
    game_window.title("Games")
    game_window.resizable(False, False)
    game_window.geometry("830x630")  # Set window size to 685x685

    # Function to open the selected game
    def open_game(game_name):
        if game_name == "Snake":
            # Define the directory containing Snake game
            game_directory = os.path.join(os.path.dirname(__file__), "Snake-main")
            if os.path.exists(game_directory):
                try:
                    # Run snake.py in a subprocess
                    subprocess.Popen(["python", "snake.py"], cwd=game_directory)
                except Exception as e:
                    messagebox.showerror("Error", f"Error running Snake game: {e}")
            else:
                messagebox.showerror("Error", "Snake game directory not found!")
        elif game_name == "Horse Racing":
            # Define the directory containing Horse Racing game
            game_directory = os.path.join(os.path.dirname(__file__), "Horse Racing")
            if os.path.exists(game_directory):
                try:
                    # Run horse racing.py in a subprocess
                    subprocess.Popen(["python", "horse racing.py"], cwd=game_directory)
                except Exception as e:
                    messagebox.showerror("Error", f"Error running Horse Racing game: {e}")
            else:
                messagebox.showerror("Error", "Horse Racing game directory not found!")
        elif game_name == "Tetris":
            # Define the directory containing Tetris game
            game_directory = os.path.join(os.path.dirname(__file__), "Tetris-main")
            if os.path.exists(game_directory):
                try:
                    # Run tetris.py in a subprocess
                    subprocess.Popen(["python", "main.py"], cwd=game_directory)
                except Exception as e:
                    messagebox.showerror("Error", f"Error running Tetris game: {e}")
            else:
                messagebox.showerror("Error", "Tetris game directory not found!")
        elif game_name == "Car Racing":
            # Define the directory containing Car Racing game
            game_directory = os.path.join(os.path.dirname(__file__), "Car-main")
            if os.path.exists(game_directory):
                try:
                    # Run car.py in a subprocess
                    subprocess.Popen(["python", "car.py"], cwd=game_directory)
                except Exception as e:
                    messagebox.showerror("Error", f"Error running Car Racing game: {e}")
            else:
                messagebox.showerror("Error", "Car Racing game directory not found!")
        elif game_name == "Pong":
            # Define the directory containing Pong game
            game_directory = os.path.join(os.path.dirname(__file__), "Table Tennis")
            if os.path.exists(game_directory):
                try:
                    # Run pong.py in a subprocess
                    subprocess.Popen(["python", "Table-Tennis.py"], cwd=game_directory)
                except Exception as e:
                    messagebox.showerror("Error", f"Error running Pong game: {e}")
            else:
                messagebox.showerror("Error", "Pong game directory not found!")
        elif game_name == "Dinosaur":
            # Define the directory containing Dinosaur game
            game_directory = os.path.join(os.path.dirname(__file__), "Dinosaur-main")
            if os.path.exists(game_directory):
                try:
                    # Run main.py in a subprocess
                    subprocess.Popen(["python", "main.py"], cwd=game_directory)
                except Exception as e:
                    messagebox.showerror("Error", f"Error running Dinosaur game: {e}")
            else:
                messagebox.showerror("Error", "Dinosaur game directory not found!")
        elif game_name == "Space Invaders":
            # Define the directory containing Space Invaders game
            game_directory = os.path.join(os.path.dirname(__file__), "Space-Invaders-main")
            if os.path.exists(game_directory):
                try:
                    # Run main.py in a subprocess
                    subprocess.Popen(["python", "main.py"], cwd=game_directory)
                except Exception as e:
                    messagebox.showerror("Error", f"Error running Space Invaders game: {e}")
            else:
                messagebox.showerror("Error", "Space Invaders game directory not found!")
        elif game_name == "2048":
            # Define the directory containing 2048 game
            game_directory = os.path.join(os.path.dirname(__file__), "2048")
            if os.path.exists(game_directory):
                try:
                    # Run 2048.py in a subprocess
                    subprocess.Popen(["python", "2048.py"], cwd=game_directory)
                except Exception as e:
                    messagebox.showerror("Error", f"Error running 2048 game: {e}")
            else:
                messagebox.showerror("Error", "2048 game directory not found!")
        elif game_name == "Sudoku":
            # Define the directory containing Sudoku game
            game_directory = os.path.join(os.path.dirname(__file__), "Sudoku")
            if os.path.exists(game_directory):
                try:
                    # Run GUI.py in a subprocess
                    subprocess.Popen(["python", "GUI.py"], cwd=game_directory)
                except Exception as e:
                    messagebox.showerror("Error", f"Error running Sudoku game: {e}")
            else:
                messagebox.showerror("Error", "Sudoku game directory not found!")
        elif game_name == "Tank":
            # Define the directory containing Tank game
            game_directory = os.path.join(os.path.dirname(__file__), "Tank Battle")
            if os.path.exists(game_directory):
                try:
                    # Run Tank-Battle.py in a subprocess
                    subprocess.Popen(["python", "Tank-Battle.py"], cwd=game_directory)
                except Exception as e:
                    messagebox.showerror("Error", f"Error running Tank game: {e}")
            else:
                messagebox.showerror("Error", "Tank game directory not found!")
        elif game_name == "Flappy Bird":
            # Define the directory containing Flappy Bird game
            game_directory = os.path.join(os.path.dirname(__file__), "Floppy_bird-main")
            if os.path.exists(game_directory):
                try:
                    # Run flappy.py in a subprocess
                    subprocess.Popen(["python", "flappy.py"], cwd=game_directory)
                except Exception as e:
                    messagebox.showerror("Error", f"Error running Flappy Bird game: {e}")
            else:
                messagebox.showerror("Error", "Flappy Bird game directory not found!")
        elif game_name == "Pool":
            # Define the directory containing Pool game
            game_directory = os.path.join(os.path.dirname(__file__), "Pool-main")
            if os.path.exists(game_directory):
                try:
                    # Run main.py in a subprocess
                    subprocess.Popen(["python", "main.py"], cwd=game_directory)
                except Exception as e:
                    messagebox.showerror("Error", f"Error running Pool game: {e}")
            else:
                messagebox.showerror("Error", "Pool game directory not found!")
        elif game_name == "Pikachu":
            # Define the directory containing Pikachu game
            game_directory = os.path.join(os.path.dirname(__file__), "Pikachu")
            if os.path.exists(game_directory):
                try:
                    # Run pikachu.py in a subprocess
                    subprocess.Popen(["python", "pikachu.py"], cwd=game_directory)
                except Exception as e:
                    messagebox.showerror("Error", f"Error running Pikachu game: {e}")
            else:
                messagebox.showerror("Error", "Pikachu game directory not found!")
        elif game_name == "Minesweeper":
            # Define the directory containing Minesweeper game
            game_directory = os.path.join(os.path.dirname(__file__), "Minesweeper-main")
            if os.path.exists(game_directory):
                try:
                    # Run main.py in a subprocess
                    subprocess.Popen(["python", "main.py"], cwd=game_directory)
                except Exception as e:
                    messagebox.showerror("Error", f"Error running Minesweeper game: {e}")
            else:
                messagebox.showerror("Error", "Minesweeper game directory not found!")
        elif game_name == "Memory":
            # Define the directory containing Memory game
            game_directory = os.path.join(os.path.dirname(__file__), "Memory-main")
            if os.path.exists(game_directory):
                try:
                    # Run main.py in a subprocess
                    subprocess.Popen(["python", "main.py"], cwd=game_directory)
                except Exception as e:
                    messagebox.showerror("Error", f"Error running Memory game: {e}")
            else:
                messagebox.showerror("Error", "Memory game directory not found!")
        elif game_name == "Mario":
            # Define the directory containing Mario game
            game_directory = os.path.join(os.path.dirname(__file__), "Mario")
            if os.path.exists(game_directory):
                try:
                    # Run mario.py in a subprocess
                    subprocess.Popen(["python", "mario.py"], cwd=game_directory)
                except Exception as e:
                    messagebox.showerror("Error", f"Error running Mario game: {e}")
            else:
                messagebox.showerror("Error", "Mario game directory not found!")
        elif game_name == "Sliding Puzzle":
            # Define the directory containing Sliding Puzzle game
            game_directory = os.path.join(os.path.dirname(__file__), "Sliding-Puzzle-main")
            if os.path.exists(game_directory):
                try:
                    # Run main.py in a subprocess
                    subprocess.Popen(["python", "main.py"], cwd=game_directory)
                except Exception as e:
                    messagebox.showerror("Error", f"Error running Sliding Puzzle game: {e}")
            else:
                messagebox.showerror("Error", "Sliding Puzzle game directory not found!")
        elif game_name == "Solitaire":
            # Define the directory containing Solitaire game
            game_directory = os.path.join(os.path.dirname(__file__), "Solitaire")
            if os.path.exists(game_directory):
                try:
                    # Run main.py in a subprocess
                    subprocess.Popen(["python", "main.py"], cwd=game_directory)
                except Exception as e:
                    messagebox.showerror("Error", f"Error running Solitaire game: {e}")
            else:
                messagebox.showerror("Error", "Solitaire game directory not found!")
        elif game_name == "Ninja Fruit":
            # Define the directory containing Ninja Fruit game
            game_directory = os.path.join(os.path.dirname(__file__), "Ninja Fruit")
            if os.path.exists(game_directory):
                try:
                    # Run main.py in a subprocess
                    subprocess.Popen(["python", "main.py"], cwd=game_directory)
                except Exception as e:
                    messagebox.showerror("Error", f"Error running Ninja Fruit game: {e}")
            else:
                messagebox.showerror("Error", "Ninja Fruit game directory not found!")
        elif game_name == "Pacman":
            # Define the directory containing Pacman game
            game_directory = os.path.join(os.path.dirname(__file__), "Pacman")
            if os.path.exists(game_directory):
                try:
                    # Run 1-PyManImproved.py in a subprocess
                    subprocess.Popen(["python", "1-PyManImproved.py"], cwd=game_directory)
                except Exception as e:
                    messagebox.showerror("Error", f"Error running Pacman game: {e}")
            else:
                messagebox.showerror("Error", "Pacman game directory not found!")
        elif game_name == "Contra":
            # Define the directory containing Contra game
            game_directory = os.path.join(os.path.dirname(__file__), "Contra")
            if os.path.exists(game_directory):
                try:
                    # Run main.py in a subprocess
                    subprocess.Popen(["python", "main.py"], cwd=game_directory)
                except Exception as e:
                    messagebox.showerror("Error", f"Error running Contra game: {e}")
            else:
                messagebox.showerror("Error", "Contra game directory not found!")
        else:
            messagebox.showerror("Error", "Game not found!")

    # Define game images and names
    games = {
        "snake": {"image": "snakegame.png", "name": "Snake"},
        "horse racing": {"image": "horseracing.png", "name": "Horse Racing"},
        "tetris": {"image": "tetrisgame.png", "name": "Tetris"},
        "car racing": {"image": "cargame.png", "name": "Car Racing"},
        "pong": {"image": "ponggame.png", "name": "Pong"},
        "dinosaur": {"image": "dinosaurgame.png", "name": "Dinosaur"},
        "space invaders": {"image": "spaceinvadersgame.png", "name": "Space Invaders"},
        "2048_": {"image": "2048game.png", "name": "2048"},
        "sudoku": {"image": "sudokugame.png", "name": "Sudoku"},
        "tank": {"image": "tankgame.png", "name": "Tank"},
        "flappy bird": {"image": "flappybirdgame.png", "name": "Flappy Bird"},
        "pool": {"image": "poolgame.png", "name": "Pool"},
        "pikachu": {"image": "pikachugame.png", "name": "Pikachu"},
        "minesweeper": {"image": "minesweepergame.png", "name": "Minesweeper"},
        "memory": {"image": "memorygame.png", "name": "Memory"},
        "mario": {"image": "mariogame.png", "name": "Mario"},
        "sliding puzzle": {"image": "slidingpuzzlegame.png", "name": "Sliding Puzzle"},
        "solitaire": {"image": "solitairegame.png", "name": "Solitaire"},
        "ninja fruit": {"image": "ninjafruitgame.png", "name": "Ninja Fruit"},
        "pacman": {"image": "pacmangame.png", "name": "Pacman"},
        "contra": {"image": "contragame.png", "name": "Contra"},
    }

    # Load and resize the image for Snake game
    snake_image = Image.open(games["snake"]["image"])
    snake_image = snake_image.resize((100, 100), Image.ANTIALIAS)  # Decrease the size of the image
    snake_image = ImageTk.PhotoImage(snake_image)

    # Create label for the resized image and place it in the top-left corner
    snake_image_label = tk.Label(game_window, image=snake_image)
    snake_image_label.image = snake_image
    snake_image_label.place(x=10, y=10)

    # Create text below the Snake game image with increased font size
    snake_label = tk.Label(game_window, text=games["snake"]["name"], font=("Helvetica", 16, "bold"))
    snake_label.place(x=30, y=120)  # Increase the y-coordinate to leave space between image and text

    # Function to handle click event on the Snake game image
    def snake_image_click(event):
        open_game("Snake")  # Open the Snake game when the image is clicked

    # Bind click event to the Snake game image label
    snake_image_label.bind("<Button-1>", snake_image_click)

    # Load and resize the image for Horse Racing game
    hr_image = Image.open(games["horse racing"]["image"])
    hr_image = hr_image.resize((100, 100), Image.ANTIALIAS)  # Decrease the size of the image
    hr_image = ImageTk.PhotoImage(hr_image)

    # Create label for the resized image and place it in the top-left corner
    hr_image_label = tk.Label(game_window, image=hr_image)
    hr_image_label.image = hr_image
    hr_image_label.place(x=150, y=10)

    # Create text below the Horse Racing game image with increased font size
    hr_label = tk.Label(game_window, text=games["horse racing"]["name"], font=("Helvetica", 16, "bold"))
    hr_label.place(x=133, y=120)  # Increase the y-coordinate to leave space between image and text

    # Function to handle click event on the Horse Racing game image
    def hr_image_click(event):
        open_game("Horse Racing")  # Open the Horse Racing game when the image is clicked

    # Bind click event to the Horse Racing game image label
    hr_image_label.bind("<Button-1>", hr_image_click)

    # Load and resize the image for Tetris game
    tt_image = Image.open(games["tetris"]["image"])
    tt_image = tt_image.resize((100, 100), Image.ANTIALIAS)  # Decrease the size of the image
    tt_image = ImageTk.PhotoImage(tt_image)

    # Create label for the resized image and place it in the top-left corner
    tt_image_label = tk.Label(game_window, image=tt_image)
    tt_image_label.image = tt_image
    tt_image_label.place(x=290, y=10)

    # Create text below the Tetris game image with increased font size
    tt_label = tk.Label(game_window, text=games["tetris"]["name"], font=("Helvetica", 16, "bold"))
    tt_label.place(x=310, y=120)  # Increase the y-coordinate to leave space between image and text

    # Function to handle click event on the Tetris game image
    def tt_image_click(event):
        open_game("Tetris")  # Open the Tetris game when the image is clicked

    # Bind click event to the Tetris game image label
    tt_image_label.bind("<Button-1>", tt_image_click)

    # Load and resize the image for Car Racing game
    cr_image = Image.open(games["car racing"]["image"])
    cr_image = cr_image.resize((100, 100), Image.ANTIALIAS)  # Decrease the size of the image
    cr_image = ImageTk.PhotoImage(cr_image)

    # Create label for the resized image and place it in the top-left corner
    cr_image_label = tk.Label(game_window, image=cr_image)
    cr_image_label.image = cr_image
    cr_image_label.place(x=430, y=10)

    # Create text below the Car Racing game image with increased font size
    cr_label = tk.Label(game_window, text=games["car racing"]["name"], font=("Helvetica", 16, "bold"))
    cr_label.place(x=423, y=120)  # Increase the y-coordinate to leave space between image and text

    # Function to handle click event on the Car Racing game image
    def cr_image_click(event):
        open_game("Car Racing")  # Open the Car Racing game when the image is clicked

    # Bind click event to the Car Racing game image label
    cr_image_label.bind("<Button-1>", cr_image_click)

    # Load and resize the image for Pong game
    pong_image = Image.open(games["pong"]["image"])
    pong_image = pong_image.resize((100, 100), Image.ANTIALIAS)  # Decrease the size of the image
    pong_image = ImageTk.PhotoImage(pong_image)

    # Create label for the resized image and place it in the top-left corner
    pong_image_label = tk.Label(game_window, image=pong_image)
    pong_image_label.image = pong_image
    pong_image_label.place(x=570, y=10)

    # Create text below the Pong game image with increased font size
    pong_label = tk.Label(game_window, text=games["pong"]["name"], font=("Helvetica", 16, "bold"))
    pong_label.place(x=590, y=120)  # Increase the y-coordinate to leave space between image and text

    # Function to handle click event on the Pong game image
    def pong_image_click(event):
        open_game("Pong")  # Open the Pong game when the image is clicked

    # Bind click event to the Pong game image label
    pong_image_label.bind("<Button-1>", pong_image_click)

    # Load and resize the image for Dinosaur game
    d_image = Image.open(games["dinosaur"]["image"])
    d_image = d_image.resize((100, 100), Image.ANTIALIAS)  # Decrease the size of the image
    d_image = ImageTk.PhotoImage(d_image)

    # Create label for the resized image and place it in the top-left corner
    d_image_label = tk.Label(game_window, image=d_image)
    d_image_label.image = d_image
    d_image_label.place(x=710, y=10)

    # Create text below the Dinosaur game image with increased font size
    d_label = tk.Label(game_window, text=games["dinosaur"]["name"], font=("Helvetica", 16, "bold"))
    d_label.place(x=713, y=120)  # Increase the y-coordinate to leave space between image and text

    # Function to handle click event on the Dinosaur game image
    def d_image_click(event):
        open_game("Dinosaur")  # Open the Dinosaur game when the image is clicked

    # Bind click event to the Dinosaur game image label
    d_image_label.bind("<Button-1>", d_image_click)

    # Load and resize the image for Space Invaders game
    si_image = Image.open(games["space invaders"]["image"])
    si_image = si_image.resize((100, 100), Image.ANTIALIAS)  # Decrease the size of the image
    si_image = ImageTk.PhotoImage(si_image)

    # Create label for the resized image and place it in the top-left corner
    si_image_label = tk.Label(game_window, image=si_image)
    si_image_label.image = si_image
    si_image_label.place(x=60, y=170)

    # Create text below the Space Invaders game image with increased font size
    si_label = tk.Label(game_window, text=games["space invaders"]["name"], font=("Helvetica", 16, "bold"))
    si_label.place(x=30, y=280)  # Increase the y-coordinate to leave space between image and text

    # Function to handle click event on the Space Invaders game image
    def si_image_click(event):
        open_game("Space Invaders")  # Open the Space Invaders game when the image is clicked

    # Bind click event to the Space Invaders game image label
    si_image_label.bind("<Button-1>", si_image_click)

    # Load and resize the image for 2048 game
    X_image = Image.open(games["2048_"]["image"])
    X_image = X_image.resize((100, 100), Image.ANTIALIAS)  # Decrease the size of the image
    X_image = ImageTk.PhotoImage(X_image)

    # Create label for the resized image and place it in the top-left corner
    X_image_label = tk.Label(game_window, image=X_image)
    X_image_label.image = X_image
    X_image_label.place(x=215, y=170)

    # Create text below the 2048 game image with increased font size
    X_label = tk.Label(game_window, text=games["2048_"]["name"], font=("Helvetica", 16, "bold"))
    X_label.place(x=240, y=280)  # Increase the y-coordinate to leave space between image and text

    # Function to handle click event on the 2048 game image
    def X_image_click(event):
        open_game("2048")  # Open the 2048 game when the image is clicked

    # Bind click event to the 2048 game image label
    X_image_label.bind("<Button-1>", X_image_click)

    # Load and resize the image for Sudoku game
    sdk_image = Image.open(games["sudoku"]["image"])
    sdk_image = sdk_image.resize((100, 100), Image.ANTIALIAS)  # Decrease the size of the image
    sdk_image = ImageTk.PhotoImage(sdk_image)

    # Create label for the resized image and place it in the top-left corner
    sdk_image_label = tk.Label(game_window, image=sdk_image)
    sdk_image_label.image = sdk_image
    sdk_image_label.place(x=359, y=170)

    # Create text below the Sudoku game image with increased font size
    sdk_label = tk.Label(game_window, text=games["sudoku"]["name"], font=("Helvetica", 16, "bold"))
    sdk_label.place(x=369, y=280)  # Increase the y-coordinate to leave space between image and text

    # Function to handle click event on the Sudoku game image
    def sdk_image_click(event):
        open_game("Sudoku")  # Open the Sudoku game when the image is clicked

    # Bind click event to the Sudoku game image label
    sdk_image_label.bind("<Button-1>", sdk_image_click)

    # Load and resize the image for Tank game
    tank_image = Image.open(games["tank"]["image"])
    tank_image = tank_image.resize((100, 100), Image.ANTIALIAS)  # Decrease the size of the image
    tank_image = ImageTk.PhotoImage(tank_image)

    # Create label for the resized image and place it in the top-left corner
    tank_image_label = tk.Label(game_window, image=tank_image)
    tank_image_label.image = tank_image
    tank_image_label.place(x=509, y=170)

    # Create text below the Tank game image with increased font size
    tank_label = tk.Label(game_window, text=games["tank"]["name"], font=("Helvetica", 16, "bold"))
    tank_label.place(x=529, y=280)  # Increase the y-coordinate to leave space between image and text

    # Function to handle click event on the Tank game image
    def tank_image_click(event):
        open_game("Tank")  # Open the Tank game when the image is clicked

    # Bind click event to the Tank game image label
    tank_image_label.bind("<Button-1>", tank_image_click)

    # Load and resize the image for Flappy Bird game
    fb_image = Image.open(games["flappy bird"]["image"])
    fb_image = fb_image.resize((100, 100), Image.ANTIALIAS)  # Decrease the size of the image
    fb_image = ImageTk.PhotoImage(fb_image)

    # Create label for the resized image and place it in the top-left corner
    fb_image_label = tk.Label(game_window, image=fb_image)
    fb_image_label.image = fb_image
    fb_image_label.place(x=659, y=170)

    # Create text below the Flappy Bird game image with increased font size
    fb_label = tk.Label(game_window, text=games["flappy bird"]["name"], font=("Helvetica", 16, "bold"))
    fb_label.place(x=650, y=280)  # Increase the y-coordinate to leave space between image and text

    # Function to handle click event on the Flappy Bird game image
    def fb_image_click(event):
        open_game("Flappy Bird")  # Open the Flappy Bird game when the image is clicked

    # Bind click event to the Flappy Bird game image label
    fb_image_label.bind("<Button-1>", fb_image_click)

    # Load and resize the image for Pool game
    pool_image = Image.open(games["pool"]["image"])
    pool_image = pool_image.resize((100, 100), Image.ANTIALIAS)  # Decrease the size of the image
    pool_image = ImageTk.PhotoImage(pool_image)

    # Create label for the resized image and place it in the top-left corner
    pool_image_label = tk.Label(game_window, image=pool_image)
    pool_image_label.image = pool_image
    pool_image_label.place(x=10, y=330)

    # Create text below the Pool game image with increased font size
    pool_label = tk.Label(game_window, text=games["pool"]["name"], font=("Helvetica", 16, "bold"))
    pool_label.place(x=30, y=440)  # Increase the y-coordinate to leave space between image and text

    # Function to handle click event on the Pool game image
    def pool_image_click(event):
        open_game("Pool")  # Open the Pool game when the image is clicked

    # Bind click event to the Pool game image label
    pool_image_label.bind("<Button-1>", pool_image_click)

    # Load and resize the image for Pikachu game
    pikachu_image = Image.open(games["pikachu"]["image"])
    pikachu_image = pikachu_image.resize((100, 100), Image.ANTIALIAS)  # Decrease the size of the image
    pikachu_image = ImageTk.PhotoImage(pikachu_image)

    # Create label for the resized image and place it in the top-left corner
    pikachu_image_label = tk.Label(game_window, image=pikachu_image)
    pikachu_image_label.image = pikachu_image
    pikachu_image_label.place(x=180, y=330)

    # Create text below the Pikachu game image with increased font size
    pikachu_label = tk.Label(game_window, text=games["pikachu"]["name"], font=("Helvetica", 16, "bold"))
    pikachu_label.place(x=190, y=440)  # Increase the y-coordinate to leave space between image and text

    # Function to handle click event on the Pikachu game image
    def pikachu_image_click(event):
        open_game("Pikachu")  # Open the Pikachu game when the image is clicked

    # Bind click event to the Pikachu game image label
    pikachu_image_label.bind("<Button-1>", pikachu_image_click)

    # Load and resize the image for Minesweeper game
    ms_image = Image.open(games["minesweeper"]["image"])
    ms_image = ms_image.resize((100, 100), Image.ANTIALIAS)  # Decrease the size of the image
    ms_image = ImageTk.PhotoImage(ms_image)

    # Create label for the resized image and place it in the top-left corner
    ms_image_label = tk.Label(game_window, image=ms_image)
    ms_image_label.image = ms_image
    ms_image_label.place(x=360, y=330)

    # Create text below the Minesweeper game image with increased font size
    ms_label = tk.Label(game_window, text=games["minesweeper"]["name"], font=("Helvetica", 16, "bold"))
    ms_label.place(x=340, y=440)  # Increase the y-coordinate to leave space between image and text

    # Function to handle click event on the Minesweeper game image
    def ms_image_click(event):
        open_game("Minesweeper")  # Open the Minesweeper game when the image is clicked

    # Bind click event to the Minesweeper game image label
    ms_image_label.bind("<Button-1>", ms_image_click)

    # Load and resize the image for Memory game
    me_image = Image.open(games["memory"]["image"])
    me_image = me_image.resize((100, 100), Image.ANTIALIAS)  # Decrease the size of the image
    me_image = ImageTk.PhotoImage(me_image)

    # Create label for the resized image and place it in the top-left corner
    me_image_label = tk.Label(game_window, image=me_image)
    me_image_label.image = me_image
    me_image_label.place(x=530, y=330)

    # Create text below the Memory game image with increased font size
    me_label = tk.Label(game_window, text=games["memory"]["name"], font=("Helvetica", 16, "bold"))
    me_label.place(x=540, y=440)  # Increase the y-coordinate to leave space between image and text

    # Function to handle click event on the Memory game image
    def me_image_click(event):
        open_game("Memory")  # Open the Memory game when the image is clicked

    # Bind click event to the Memory game image label
    me_image_label.bind("<Button-1>", me_image_click)

    # Load and resize the image for Mario game
    ma_image = Image.open(games["mario"]["image"])
    ma_image = ma_image.resize((100, 100), Image.ANTIALIAS)  # Decrease the size of the image
    ma_image = ImageTk.PhotoImage(ma_image)

    # Create label for the resized image and place it in the top-left corner
    ma_image_label = tk.Label(game_window, image=ma_image)
    ma_image_label.image = ma_image
    ma_image_label.place(x=710, y=330)

    # Create text below the Mario game image with increased font size
    ma_label = tk.Label(game_window, text=games["mario"]["name"], font=("Helvetica", 16, "bold"))
    ma_label.place(x=732, y=440)  # Increase the y-coordinate to leave space between image and text

    # Function to handle click event on the Mario game image
    def ma_image_click(event):
        open_game("Mario")  # Open the Mario game when the image is clicked

    # Bind click event to the Mario game image label
    ma_image_label.bind("<Button-1>", ma_image_click)

    # Load and resize the image for Sliding Puzzle game
    sp_image = Image.open(games["sliding puzzle"]["image"])
    sp_image = sp_image.resize((100, 100), Image.ANTIALIAS)  # Decrease the size of the image
    sp_image = ImageTk.PhotoImage(sp_image)

    # Create label for the resized image and place it in the top-left corner
    sp_image_label = tk.Label(game_window, image=sp_image)
    sp_image_label.image = sp_image
    sp_image_label.place(x=60, y=490)

    # Create text below the Sliding Puzzle game image with increased font size
    sp_label = tk.Label(game_window, text=games["sliding puzzle"]["name"], font=("Helvetica", 16, "bold"))
    sp_label.place(x=40, y=600)  # Increase the y-coordinate to leave space between image and text

    # Function to handle click event on the Sliding Puzzle game image
    def sp_image_click(event):
        open_game("Sliding Puzzle")  # Open the Sliding Puzzle game when the image is clicked

    # Bind click event to the Sliding Puzzle game image label
    sp_image_label.bind("<Button-1>", sp_image_click)

    # Load and resize the image for Solitaire game
    so_image = Image.open(games["solitaire"]["image"])
    so_image = so_image.resize((100, 100), Image.ANTIALIAS)  # Decrease the size of the image
    so_image = ImageTk.PhotoImage(so_image)

    # Create label for the resized image and place it in the top-left corner
    so_image_label = tk.Label(game_window, image=so_image)
    so_image_label.image = so_image
    so_image_label.place(x=220, y=490)

    # Create text below the Solitaire game image with increased font size
    so_label = tk.Label(game_window, text=games["solitaire"]["name"], font=("Helvetica", 16, "bold"))
    so_label.place(x=230, y=600)  # Increase the y-coordinate to leave space between image and text

    # Function to handle click event on the Solitaire game image
    def so_image_click(event):
        open_game("Solitaire")  # Open the Solitaire game when the image is clicked

    # Bind click event to the Solitaire game image label
    so_image_label.bind("<Button-1>", so_image_click)

    # Load and resize the image for Ninja Fruit game
    nf_image = Image.open(games["ninja fruit"]["image"])
    nf_image = nf_image.resize((100, 100), Image.ANTIALIAS)  # Decrease the size of the image
    nf_image = ImageTk.PhotoImage(nf_image)

    # Create label for the resized image and place it in the top-left corner
    nf_image_label = tk.Label(game_window, image=nf_image)
    nf_image_label.image = nf_image
    nf_image_label.place(x=380, y=490)

    # Create text below the Ninja Fruit game image with increased font size
    nf_label = tk.Label(game_window, text=games["ninja fruit"]["name"], font=("Helvetica", 16, "bold"))
    nf_label.place(x=378, y=600)  # Increase the y-coordinate to leave space between image and text

    # Function to handle click event on the Ninja Fruit game image
    def nf_image_click(event):
        open_game("Ninja Fruit")  # Open the Ninja Fruit game when the image is clicked

    # Bind click event to the Ninja Fruit game image label
    nf_image_label.bind("<Button-1>", nf_image_click)

    # Load and resize the image for Pacman game
    p_image = Image.open(games["pacman"]["image"])
    p_image = p_image.resize((100, 100), Image.ANTIALIAS)  # Decrease the size of the image
    p_image = ImageTk.PhotoImage(p_image)

    # Create label for the resized image and place it in the top-left corner
    p_image_label = tk.Label(game_window, image=p_image)
    p_image_label.image = p_image
    p_image_label.place(x=540, y=490)

    # Create text below the Pacman game image with increased font size
    p_label = tk.Label(game_window, text=games["pacman"]["name"], font=("Helvetica", 16, "bold"))
    p_label.place(x=547, y=600)  # Increase the y-coordinate to leave space between image and text

    # Function to handle click event on the Pacman game image
    def p_image_click(event):
        open_game("Pacman")  # Open the Pacman game when the image is clicked

    # Bind click event to the Pacman game image label
    p_image_label.bind("<Button-1>", p_image_click)

    # Load and resize the image for Contra game
    c_image = Image.open(games["contra"]["image"])
    c_image = c_image.resize((100, 100), Image.ANTIALIAS)  # Decrease the size of the image
    c_image = ImageTk.PhotoImage(c_image)

    # Create label for the resized image and place it in the top-left corner
    c_image_label = tk.Label(game_window, image=c_image)
    c_image_label.image = c_image
    c_image_label.place(x=700, y=490)

    # Create text below the Contra game image with increased font size
    c_label = tk.Label(game_window, text=games["contra"]["name"], font=("Helvetica", 16, "bold"))
    c_label.place(x=712, y=600)  # Increase the y-coordinate to leave space between image and text

    # Function to handle click event on the Contra game image
    def c_image_click(event):
        open_game("Contra")  # Open the Contra game when the image is clicked

    # Bind click event to the Contra game image label
    c_image_label.bind("<Button-1>", c_image_click)


# Create main window
root = tk.Tk()
root.title("YouTube Transcript Translation")
root.resizable(False, False)

# Label for URL entry
url_label = tk.Label(root, text="Enter YouTube Video URL or Choose MP4 File:")
url_label.pack()

# Entry widget for URL input
url_entry = tk.Entry(root, width=50)
url_entry.pack()

# Button to select file
select_file_button = tk.Button(root, text="Choose File", command=select_file)
select_file_button.pack(pady=5)

# Label for URL entry
text_label = tk.Label(root, text="Enter Text to Translate:")
text_label.pack()

# Text widget for text input
text_input = tk.Text(root, width=50, height=10)
text_input.pack()

# Get all language codes and their names
all_languages = ["af", "sq", "am", "ar", "hy", "az", "eu", "be", "bn", "bs", "bg", "ca", "ceb", "ny", "zh-CN", "zh-TW",
                 "co", "hr", "cs", "da", "nl", "en", "eo", "et", "tl", "fi", "fr", "fy", "gl", "ka", "de", "el",
                 "gu", "ht", "ha", "haw", "iw", "hi", "hmn", "hu", "is", "ig", "id", "ga", "it", "ja", "jw", "kn",
                 "kk", "km", "ko", "ku", "ky", "lo", "la", "lv", "lt", "lb", "mk", "mg", "ms", "ml", "mt", "mi",
                 "mr", "mn", "my", "ne", "no", "or", "ps", "fa", "pl", "pt", "pa", "ro", "ru", "sm", "gd", "sr",
                 "st", "sn", "sd", "si", "sk", "sl", "so", "es", "su", "sw", "sv", "tg", "ta", "tt", "te", "th",
                 "tr", "tk", "uk", "ur", "ug", "uz", "vi", "cy", "xh", "yi", "yo", "zu"]

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
translate_button = tk.Button(button_frame, text="Translate Video", command=translate_text)
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

# Button to trigger translation
translation_button = tk.Button(button_frame, text="Translate Text", command=perform_translation)
translation_button.grid(row=0, column=6, padx=5, pady=5)

# Create a button to check language
check_language_button = tk.Button(button_frame, text="Check Language", command=check_language)
check_language_button.grid(row=0, column=7, padx=5, pady=5)

# Button to open Facebook homepage
facebook_button = tk.Button(button_frame, text="Facebook", command=open_facebook)
facebook_button.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

# Button to open Twitter homepage
twitter_button = tk.Button(button_frame, text="Twitter", command=open_twitter)
twitter_button.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

# Button to open Instagram homepage
instagram_button = tk.Button(button_frame, text="Instagram", command=open_instagram)
instagram_button.grid(row=1, column=2, padx=5, pady=5, sticky="ew")

# Button to open Google homepage
google_button = tk.Button(button_frame, text="Google", command=open_google)
google_button.grid(row=1, column=3, padx=5, pady=5, sticky="ew")

# Button to open Tiktok homepage
tiktok_button = tk.Button(button_frame, text="Tiktok", command=open_tiktok)
tiktok_button.grid(row=1, column=4, padx=5, pady=5, sticky="ew")

# Button to open Wechat homepage
wechat_button = tk.Button(button_frame, text="Wechat", command=open_wechat)
wechat_button.grid(row=1, column=5, padx=5, pady=5, sticky="ew")

# Button to open Zing MP3 homepage
zingmp3_button = tk.Button(button_frame, text="Zing MP3", command=open_zingmp3)
zingmp3_button.grid(row=1, column=6, padx=5, pady=5, sticky="ew")

# Button to open Spotify homepage
spotify_button = tk.Button(button_frame, text="Spotify", command=open_spotify)
spotify_button.grid(row=1, column=7, padx=5, pady=5, sticky="ew")

# Button to open Thap Cam TV homepage
thapcamtv_button = tk.Button(button_frame, text="Thap Cam TV", command=open_thapcamtv)
thapcamtv_button.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

# Button to open game window
game_button = tk.Button(button_frame, text="Game", command=open_game_window)
game_button.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

# Center the frame containing buttons
button_frame.grid_columnconfigure(0, weight=1)
button_frame.grid_columnconfigure(1, weight=1)
button_frame.grid_columnconfigure(2, weight=1)
button_frame.grid_columnconfigure(3, weight=1)
button_frame.grid_columnconfigure(4, weight=1)
button_frame.grid_columnconfigure(5, weight=1)
button_frame.grid_columnconfigure(6, weight=1)
button_frame.grid_columnconfigure(7, weight=1)

# Run the main event loop
root.mainloop()
