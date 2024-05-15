from tkinter import *
from tkinter.ttk import Combobox
import time
import random
import pygame
from tkinter import messagebox

red_horse_x = 0
red_horse_y = 10

blue_horse_x = 0
blue_horse_y = 110

green_horse_x = 0
green_horse_y = 210

purple_horse_x = 0
purple_horse_y = 310

pink_horse_x = 0
pink_horse_y = 410

winner = False
selected_horse = ""  # To store the user's selected horse

# Initialize pygame
pygame.mixer.init()

# Load sounds
running_sound = pygame.mixer.Sound("./sounds/single-horse-galopp-6152.wav")
winning_sound = pygame.mixer.Sound("./sounds/win.wav")
tie_sound = pygame.mixer.Sound("./sounds/ambient-metal-whoosh-2-174462.wav")
losting_sound = pygame.mixer.Sound("./sounds/game-over-31-179699.wav")


def start_game():
    global selected_horse
    selected_horse = horse_selection.get()  # Get the selected horse from the Combobox

    global red_horse_x, blue_horse_x, green_horse_x, purple_horse_x, pink_horse_x, winner, winner_label

    while winner == False:
        time.sleep(0.05)
        random_move_red_horse = random.randint(0, 20)
        random_move_blue_horse = random.randint(0, 20)
        random_move_green_horse = random.randint(0, 20)
        random_move_purple_horse = random.randint(0, 20)
        random_move_pink_horse = random.randint(0, 20)
        # Update the x positions of both horses
        red_horse_x += random_move_red_horse
        blue_horse_x += random_move_blue_horse
        green_horse_x += random_move_green_horse
        purple_horse_x += random_move_purple_horse
        pink_horse_x += random_move_pink_horse
        move_horses(random_move_red_horse, random_move_blue_horse, random_move_green_horse, random_move_purple_horse, random_move_pink_horse)
        main_screen.update()
        winner = check_winner()

        if winner:
            running_sound.stop()

    if winner == "Tie":
        winner_label = Label(main_screen, text=winner, font=('calibri', 20), fg="green")
        winner_label.place(x=580, y=750)
        play_tie_sound()
        messagebox.showinfo("Result", "It's a tie!")
    elif winner == selected_horse:
        winner_label = Label(main_screen, text=winner + " Wins !!", font=('calibri', 20), fg="green")
        winner_label.place(x=498, y=750)
        play_winning_sound()
        messagebox.showinfo("Result", "You win!!!")
    else:
        winner_label = Label(main_screen, text=winner + " Wins !!", font=('calibri', 20), fg="green")
        winner_label.place(x=498, y=750)
        play_losting_sound()
        messagebox.showinfo("Result", "You lost!!!")


def reset_game():
    global red_horse_x, blue_horse_x, green_horse_x, purple_horse_x, pink_horse_x, winner

    red_horse_x = 0
    blue_horse_x = 0
    green_horse_x = 0
    purple_horse_x = 0
    pink_horse_x = 0
    winner = False

    canvas.coords(red_horse, red_horse_x, red_horse_y)
    canvas.coords(blue_horse, blue_horse_x, blue_horse_y)
    canvas.coords(green_horse, green_horse_x, green_horse_y)
    canvas.coords(purple_horse, purple_horse_x, purple_horse_y)
    canvas.coords(pink_horse, pink_horse_x, pink_horse_y)

    l1.config(text='Select your horse')
    l2.config(text='Click play when ready!')

    if pygame.mixer.get_busy():
        pygame.mixer.stop()

    # Xóa thông báo về ngựa chiến thắng
    winner_label.place_forget()


def move_horses(red_horse_random_move, blue_horse_random_move, green_horse_random_move, purple_horse_random_move, pink_horse_random_move):
    canvas.move(red_horse, red_horse_random_move, 0)
    canvas.move(blue_horse, blue_horse_random_move, 0)
    canvas.move(green_horse, green_horse_random_move, 0)
    canvas.move(purple_horse, purple_horse_random_move, 0)
    canvas.move(pink_horse, pink_horse_random_move, 0)

    if red_horse_random_move != 0:  # Kiểm tra nếu ngựa đỏ đang di chuyển
        play_running_sound()
    if blue_horse_random_move != 0:  # Kiểm tra nếu ngựa xanh đang di chuyển
        play_running_sound()
    if green_horse_random_move != 0:  # Kiểm tra nếu ngựa xanh đang di chuyển
        play_running_sound()
    if purple_horse_random_move != 0:  # Kiểm tra nếu ngựa tím đang di chuyển
        play_running_sound()
    if pink_horse_random_move != 0:  # Kiểm tra nếu ngựa hồng đang di chuyển
        play_running_sound()


def play_running_sound():
    running_sound.play()


def play_winning_sound():
    winning_sound.play()


def play_tie_sound():
    tie_sound.play()


def play_losting_sound():
    losting_sound.play()


def check_winner():
    if red_horse_x >= 1150 and blue_horse_x >= 1150 and green_horse_x >= 1150 and purple_horse_x >= 1150 and pink_horse_x >= 1150:
        return "Tie"
    if red_horse_x >= 1150 and blue_horse_x >= 1150 and green_horse_x >= 1150 and purple_horse_x >= 1150:
        return "Tie"
    if red_horse_x >= 1150 and blue_horse_x >= 1150 and green_horse_x >= 1150 and pink_horse_x >= 1150:
        return "Tie"
    if red_horse_x >= 1150 and blue_horse_x >= 1150 and purple_horse_x >= 1150 and pink_horse_x >= 1150:
        return "Tie"
    if red_horse_x >= 1150 and green_horse_x >= 1150 and purple_horse_x >= 1150 and pink_horse_x >= 1150:
        return "Tie"
    if blue_horse_x >= 1150 and green_horse_x >= 1150 and purple_horse_x >= 1150 and pink_horse_x >= 1150:
        return "Tie"
    if red_horse_x >= 1150 and blue_horse_x >= 1150 and green_horse_x >= 1150:
        return "Tie"
    if red_horse_x >= 1150 and blue_horse_x >= 1150 and purple_horse_x >= 1150:
        return "Tie"
    if red_horse_x >= 1150 and blue_horse_x >= 1150 and pink_horse_x >= 1150:
        return "Tie"
    if red_horse_x >= 1150 and purple_horse_x >= 1150 and pink_horse_x >= 1150:
        return "Tie"
    if red_horse_x >= 1150 and green_horse_x >= 1150 and purple_horse_x >= 1150:
        return "Tie"
    if red_horse_x >= 1150 and green_horse_x >= 1150 and pink_horse_x >= 1150:
        return "Tie"
    if blue_horse_x >= 1150 and green_horse_x >= 1150 and purple_horse_x >= 1150:
        return "Tie"
    if blue_horse_x >= 1150 and green_horse_x >= 1150 and pink_horse_x >= 1150:
        return "Tie"
    if blue_horse_x >= 1150 and purple_horse_x >= 1150 and pink_horse_x >= 1150:
        return "Tie"
    if green_horse_x >= 1150 and purple_horse_x >= 1150 and pink_horse_x >= 1150:
        return "Tie"
    if red_horse_x >= 1150 and blue_horse_x >= 1150:
        return "Tie"
    if red_horse_x >= 1150 and green_horse_x >= 1150:
        return "Tie"
    if red_horse_x >= 1150 and purple_horse_x >= 1150:
        return "Tie"
    if red_horse_x >= 1150 and pink_horse_x >= 1150:
        return "Tie"
    if blue_horse_x >= 1150 and green_horse_x >= 1150:
        return "Tie"
    if blue_horse_x >= 1150 and purple_horse_x >= 1150:
        return "Tie"
    if blue_horse_x >= 1150 and pink_horse_x >= 1150:
        return "Tie"
    if green_horse_x >= 1150 and purple_horse_x >= 1150:
        return "Tie"
    if green_horse_x >= 1150 and pink_horse_x >= 1150:
        return "Tie"
    if purple_horse_x >= 1150 and pink_horse_x >= 1150:
        return "Tie"
    if red_horse_x >= 1150:
        return "Red Horse"
    if blue_horse_x >= 1150:
        return "Blue Horse"
    if green_horse_x >= 1150:
        return "Green Horse"
    if purple_horse_x >= 1150:
        return "Purple Horse"
    if pink_horse_x >= 1150:
        return "Pink Horse"
    return False


# Setting up the main screen
main_screen = Tk()
main_screen.title('Horse Racing')
main_screen.geometry('1200x800')
main_screen.config(background='white')

# Tắt chức năng phóng to màn hình
main_screen.resizable(False, False)

# Setting up the Canvas
canvas = Canvas(main_screen, width=1200, height=500, bg="white")
canvas.pack(pady=20)

# Import the images
red_horse_img = PhotoImage(file="./images/red_horse.png")
blue_horse_img = PhotoImage(file="./images/blue_horse.png")
green_horse_img = PhotoImage(file="./images/green_horse.png")
purple_horse_img = PhotoImage(file="./images/purple_horse.png")
pink_horse_img = PhotoImage(file="./images/pink_horse.png")

# Resizing the images
red_horse_img = red_horse_img.zoom(10)
red_horse_img = red_horse_img.subsample(60)
blue_horse_img = blue_horse_img.zoom(10)
blue_horse_img = blue_horse_img.subsample(60)
green_horse_img = green_horse_img.zoom(10)
green_horse_img = green_horse_img.subsample(60)
purple_horse_img = purple_horse_img.zoom(10)
purple_horse_img = purple_horse_img.subsample(60)
pink_horse_img = pink_horse_img.zoom(10)
pink_horse_img = pink_horse_img.subsample(60)

# Adding images to the canvas
red_horse = canvas.create_image(red_horse_x, red_horse_y, anchor=NW, image=red_horse_img)
blue_horse = canvas.create_image(blue_horse_x, blue_horse_y, anchor=NW, image=blue_horse_img)
green_horse = canvas.create_image(green_horse_x, green_horse_y, anchor=NW, image=green_horse_img)
purple_horse = canvas.create_image(purple_horse_x, purple_horse_y, anchor=NW, image=purple_horse_img)
pink_horse = canvas.create_image(pink_horse_x, pink_horse_y, anchor=NW, image=pink_horse_img)

# Adding labels to screen (text)
l1 = Label(main_screen, text='Select your horse', font=('calibri', 20), bg="white")
l1.place(x=430, y=580)

# Combobox for horse selection
horse_selection = Combobox(main_screen, values=["Red Horse", "Blue Horse", "Green Horse", "Purple Horse", "Pink Horse"])
horse_selection.place(x=630, y=590)
horse_selection.current()  # Set the default value

l2 = Label(main_screen, text='Click play when ready!', font=('calibri', 20), bg="white")
l2.place(x=480, y=630)

b1 = Button(main_screen, text='Play', height=2, width=14, bg="white", font=('calibri', 10), command=start_game)
b1.place(x=490, y=690)

b2 = Button(main_screen, text='Reset', height=2, width=14, bg="white", font=('calibri', 10), command=reset_game)
b2.place(x=605, y=690)

main_screen.mainloop()
