import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import random
import pygame

class SlidingPuzzle(tk.Tk):
    def __init__(self, image_path, rows, columns):
        super().__init__()
        self.rows = rows
        self.columns = columns
        self.tiles = []
        self.game_started = False
        self.tiles_moved = False  # Track if tiles have been moved
        self.moves_made = 0  # Track number of moves made

        # Khởi tạo pygame
        pygame.init()
        # Phát nhạc liên tục
        pygame.mixer.music.load(
            "musics/complicated-puzzle-176796.mp3")  # Thay đổi "your_music_file.mp3" bằng đường dẫn đến file nhạc của bạn
        pygame.mixer.music.play(loops=-1)  # Số âm là phát nhạc liên tục

        self.image = Image.open(image_path)
        self.tile_width = (self.image.width - 2 * (columns - 1)) // columns
        self.tile_height = (self.image.height - 2 * (rows - 1)) // rows

        # Calculate window size based on tile size and gap between them
        window_width = columns * (self.tile_width + 2)
        window_height = rows * (self.tile_height + 2)

        # Adjust window size to fit within 806x606
        window_width = min(window_width, 806)
        window_height = min(window_height, 606)
        self.geometry(f"{window_width}x{window_height}")

        self.canvas = tk.Canvas(self, width=window_width, height=window_height)
        self.canvas.pack()

        self.create_tiles()
        self.shuffle_tiles()
        self.swap_empty_with_number_9()

        # Load and resize the small image
        small_image = Image.open(image_path)
        small_image = small_image.resize((100, 100), Image.ANTIALIAS)
        self.small_image = ImageTk.PhotoImage(small_image)

        # Draw the small image on the right side of the puzzle board
        self.small_image_canvas = self.canvas.create_image(window_width - 50, 50, anchor="ne", image=self.small_image)

        # Draw black border for the small image
        x0 = window_width - 50
        y0 = 50
        x1 = window_width - 150
        y1 = 150
        self.canvas.create_rectangle(x0, y0, x1, y1, outline="#242424", width=2)

        # Add a Restart button
        self.restart_button = tk.Button(self, text="Restart", command=self.restart_game, state="disabled")
        self.restart_button.place(relx=0.5, rely=1.0, anchor='s')
        self.restart_button.place_configure(relx=0.5, rely=1.0, anchor='s', x=255, y=-350, width=80, height=40)
        self.restart_button.config(font=("Arial", 14), fg="yellow", bg="red")

        # Add a Shuffle button
        self.shuffle_button = tk.Button(self, text="Shuffle", command=self.shuffle_tiles)
        self.shuffle_button.place(relx=0.5, rely=1.0, anchor='s')
        self.shuffle_button.place_configure(relx=0.5, rely=1.0, anchor='s', x=350, y=-350, width=80, height=40)
        self.shuffle_button.config(font=("Arial", 14), fg="black", bg="#FFCC99", state="normal")

        # Add a Change Image button
        self.change_image_button = tk.Button(self, text="Change the image", command=self.choose_image)
        self.change_image_button.place(relx=0.5, rely=1.0, anchor='s')
        self.change_image_button.place_configure(relx=0.5, rely=1.0, anchor='s', x=302, y=-300, width=175, height=40)
        self.change_image_button.config(font=("Arial", 14), fg="#333300", bg="silver", state="normal")

        # Add a label to display moves made
        self.moves_label = tk.Label(self, text="Moves made: 0", font=("Arial", 16), fg="#00BFFF")
        self.moves_label.place(relx=0.5, rely=1.0, anchor='s')
        self.moves_label.place_configure(relx=0.5, rely=1.0, anchor='s', x=300, y=-240)

    def create_tiles(self):
        # Xóa đi các mảnh ghép cũ trên bảng
        for tile in self.tiles:
            self.canvas.delete(tile.canvas_image)
            if hasattr(tile, 'canvas_number'):
                self.canvas.delete(tile.canvas_number)
        self.tiles.clear()

        # Tạo các mảnh ghép mới từ hình ảnh mới
        for row in range(self.rows):
            for col in range(self.columns):
                x0 = col * (self.tile_width + 2)
                y0 = row * (self.tile_height + 2)
                x1 = x0 + self.tile_width
                y1 = y0 + self.tile_height
                tile_image = self.image.crop((x0, y0, x1, y1))
                tile_image = tile_image.resize((200, 200), Image.ANTIALIAS)  # Resize the tile image to 200x200
                number = row * self.columns + col + 1  # Calculate the number to draw on the tile
                tile = Tile(self.canvas, tile_image, (row, col), number, self.on_tile_click)
                self.tiles.append(tile)
                if (row, col) == (self.rows - 1, self.columns - 1):
                    self.empty_tile = tile

        # Create and position the empty tile on the right side of the grid
        empty_row = self.rows - 1
        empty_col = self.columns
        empty_x0 = empty_col * (self.tile_width + 2)
        empty_y0 = empty_row * (self.tile_height + 2)
        empty_x1 = empty_x0 + self.tile_width
        empty_y1 = empty_y0 + self.tile_height
        empty_image = Image.new("RGB", (self.tile_width, self.tile_height), color="#006666")  # Create pink empty tile
        empty_image_resized = empty_image.resize((200, 200), Image.ANTIALIAS)  # Resize the empty tile image to 200x200
        empty_tile = Tile(self.canvas, empty_image_resized, (empty_row, empty_col), None, self.on_tile_click)
        self.empty_tile = empty_tile

    def on_tile_click(self, tile):
        if tile != self.empty_tile and self.is_adjacent(tile, self.empty_tile):
            self.swap_tiles(tile, self.empty_tile)
            self.moves_made += 1  # Increment moves made
            self.moves_label.config(text=f"Moves made: {self.moves_made}")  # Update moves label
            if not self.game_started:
                self.game_started = True
                self.disable_shuffle_button()
            if self.is_solved():
                self.check_win()  # Check for win after each move
            else:
                self.tiles_moved = True  # Tiles have been moved
                self.disable_shuffle_button()  # Disable shuffle button after tiles have been moved
                self.enable_restart_button()  # Enable restart button after tiles have been moved

    def is_adjacent(self, tile1, tile2):
        row1, col1 = tile1.position
        row2, col2 = tile2.position
        return abs(row1 - row2) + abs(col1 - col2) == 1

    def shuffle_tiles(self):
        # Shuffle the positions of number tiles (excluding the empty tile)
        number_tiles = [tile for tile in self.tiles if tile.number is not None and tile.number != 9]
        random.shuffle(number_tiles)
        for index, tile in enumerate(number_tiles):
            row, col = divmod(index, self.columns)
            tile.position = (row, col)
            tile.update_position()

    def swap_tiles(self, tile1, tile2):
        tile1.position, tile2.position = tile2.position, tile1.position
        tile1.update_position()
        tile2.update_position()

    def is_solved(self):
        for index, tile in enumerate(self.tiles):
            row, col = divmod(index, self.columns)
            if tile.position != (row, col):
                return False
        return True

    def swap_empty_with_number_9(self):
        number_9_tile = None
        for tile in self.tiles:
            if tile.number == 9:
                number_9_tile = tile
                break
        if number_9_tile is not None:
            self.swap_tiles(number_9_tile, self.empty_tile)

    def restart_game(self):
        self.moves_made = 0  # Reset moves made
        self.moves_label.config(text=f"Moves made: {self.moves_made}")  # Update moves label
        self.create_tiles()
        self.shuffle_tiles()
        self.swap_empty_with_number_9()
        self.disable_restart_button()  # Disable restart button after restart
        self.enable_shuffle_button()   # Enable shuffle button after restart

    def check_win(self):
        if self.is_solved():
            messagebox.showinfo("Result", f"You win!!! Moves made is: {self.moves_made}")
            self.restart_game()

    def is_displayed_correctly(self):
        for index, tile in enumerate(self.tiles):
            row, col = divmod(index, self.columns)
            if tile.position != (row, col):
                return False
        return True

    def disable_shuffle_button(self):
        self.shuffle_button.config(state="disabled")

    def disable_restart_button(self):
        self.restart_button.config(state="disabled")

    def choose_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
        if file_path:
            self.update_image(file_path)
            if self.has_moved_tiles():
                self.enable_shuffle_button()  # Enable shuffle button if tiles have been moved
            else:
                self.disable_shuffle_button()  # Disable shuffle button if no tiles have been moved

    def has_moved_tiles(self):
        return self.tiles_moved or not self.is_displayed_correctly()

    def enable_shuffle_button(self):
        self.shuffle_button.config(state="normal")

    def enable_restart_button(self):
        self.restart_button.config(state="normal")

    def update_image(self, image_path):
        self.moves_made = 0  # Reset moves made when image is updated
        self.moves_label.config(text=f"Moves made: {self.moves_made}")  # Update moves label
        self.image = Image.open(image_path)
        self.create_tiles()
        self.shuffle_tiles()
        self.swap_empty_with_number_9()

        # Load and resize the new small image
        small_image = Image.open(image_path)
        small_image = small_image.resize((100, 100), Image.ANTIALIAS)
        self.small_image = ImageTk.PhotoImage(small_image)

        # Update the small image on the right side of the puzzle board
        self.canvas.itemconfig(self.small_image_canvas, image=self.small_image)

        # Check if tiles have been moved, if yes, disable shuffle button
        if self.has_moved_tiles():
            self.disable_shuffle_button()  # Disable shuffle button if tiles have been moved
        else:
            self.enable_shuffle_button()  # Enable shuffle button if no tiles have been moved

    def __del__(self):
        # Dừng nhạc khi game kết thúc
        pygame.mixer.music.stop()

class Tile:
    def __init__(self, canvas, image, position, number, onclick):
        self.canvas = canvas
        self.image = ImageTk.PhotoImage(image)
        self.position = position
        self.number = number
        self.onclick = onclick

        self.canvas_image = self.canvas.create_image(0, 0, anchor="nw", image=self.image)
        if number is not None:
            self.canvas_number = self.canvas.create_text(100, 100, text=str(number), font=("Arial", 50), fill="white")
        self.update_position()
        self.canvas.tag_bind(self.canvas_image, "<Button-1>", self.on_click)

    def update_position(self):
        row, col = self.position
        x0 = col * (200 + 2)
        y0 = row * (200 + 2)
        self.canvas.coords(self.canvas_image, x0, y0)
        if hasattr(self, 'canvas_number'):
            self.canvas.coords(self.canvas_number, x0 + 100, y0 + 100)

    def set_position(self, position):
        self.position = position

    def on_click(self, event):
        self.onclick(self)

if __name__ == "__main__":
    app = SlidingPuzzle("Images/m.png", 3, 3)
    app.title("Sliding Puzzle")
    app.resizable(width=False, height=False)
    app.mainloop()
