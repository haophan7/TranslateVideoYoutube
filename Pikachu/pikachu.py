import os
import random
import pygame
import sys
import time
from tkinter import Tk, messagebox
from pygame.locals import *


class Square:
    def __init__(self):
        self._isDropped = True
        self.value = None

    def isDropped(self):
        return self._isDropped

    def setDropped(self, isDropped):
        self._isDropped = isDropped

    def getValue(self):
        return self.value

    def setValue(self, value):
        self.value = value


class Board:
    NUM_ROWS = 12
    NUM_COLUMNS = 18

    def __init__(self):
        self.listSquare = [[Square() for _ in range(self.NUM_COLUMNS)] for _ in range(self.NUM_ROWS)]
        gallery = "images"
        images = os.listdir(gallery)
        self.listPokemon = []
        if len(images) >= (self.NUM_ROWS - 2) * (self.NUM_COLUMNS - 2) // 8:
            for i in range((self.NUM_ROWS - 2) * (self.NUM_COLUMNS - 2) // 8):
                for _ in range(8):
                    self.listPokemon.append(images[i])
        else:
            print("Khong du so anh")
        self.initBoard()

    def getListSquare(self):
        return self.listSquare

    def setListSquare(self, list):
        self.listSquare = list

    def initBoard(self):
        index = 0
        random.shuffle(self.listPokemon)
        for i in range(len(self.listSquare)):
            for j in range(len(self.listSquare[0])):
                if i > 0 and i < self.NUM_ROWS - 1 and j > 0 and j < self.NUM_COLUMNS - 1:
                    self.listSquare[i][j].setDropped(False)
                    self.listSquare[i][j].setValue(self.listPokemon[index])
                    index += 1

    def checkMatching(self, x0, y0, x1, y1):
        if self.listSquare[x0][y0].getValue() == self.listSquare[x1][y1].getValue():
            top0, bot0 = x0, x0
            while bot0 - 1 >= 0:
                if self.listSquare[bot0 - 1][y0].isDropped():
                    bot0 -= 1
                else:
                    break
            while top0 + 1 <= self.NUM_ROWS - 1:
                if self.listSquare[top0 + 1][y0].isDropped():
                    top0 += 1
                else:
                    break
            top1, bot1 = x1, x1
            while bot1 - 1 >= 0:
                if self.listSquare[bot1 - 1][y1].isDropped():
                    bot1 -= 1
                else:
                    break
            while top1 + 1 <= self.NUM_ROWS - 1:
                if self.listSquare[top1 + 1][y1].isDropped():
                    top1 += 1
                else:
                    break
            minTop = min(top0, top1)
            maxBot = max(bot0, bot1)
            minY = min(y0, y1)
            maxY = max(y0, y1)
            for i in range(maxBot, minTop + 1):
                count = 0
                for j in range(minY + 1, maxY):
                    if self.listSquare[i][j].isDropped():
                        count += 1
                    else:
                        break
                if count == maxY - minY - 1:
                    self.listSquare[x0][y0].setDropped(True)
                    self.listSquare[x1][y1].setDropped(True)
                    return True

            left0, right0 = y0, y0
            while left0 - 1 >= 0:
                if self.listSquare[x0][left0 - 1].isDropped():
                    left0 -= 1
                else:
                    break
            while right0 + 1 <= self.NUM_COLUMNS - 1:
                if self.listSquare[x0][right0 + 1].isDropped():
                    right0 += 1
                else:
                    break
            left1, right1 = y1, y1
            while left1 - 1 >= 0:
                if self.listSquare[x1][left1 - 1].isDropped():
                    left1 -= 1
                else:
                    break
            while right1 + 1 <= self.NUM_COLUMNS - 1:
                if self.listSquare[x1][right1 + 1].isDropped():
                    right1 += 1
                else:
                    break
            minRight = min(right0, right1)
            maxLeft = max(left0, left1)
            minX = min(x0, x1)
            maxX = max(x0, x1)
            for i in range(maxLeft, minRight + 1):
                count = 0
                for j in range(minX + 1, maxX):
                    if self.listSquare[j][i].isDropped():
                        count += 1
                    else:
                        break
                if count == maxX - minX - 1:
                    self.listSquare[x0][y0].setDropped(True)
                    self.listSquare[x1][y1].setDropped(True)
                    return True
        return False

    def isAllMatched(self):
        for i in range(1, self.NUM_ROWS - 1):
            for j in range(1, self.NUM_COLUMNS - 1):
                if not self.listSquare[i][j].isDropped():
                    return False
        return True


class BoardPanel:
    def __init__(self, gui, board):
        self.gui = gui
        self.board = board
        self.selectedSlot = [None, None]
        self.selectedImage = None
        self.NORMAL_BORDER = "gray"
        self.SELECTED_BORDER = "red"
        self.initComp()

    def initComp(self):
        self.screen = pygame.display.set_mode((self.gui.WIDTH, self.gui.HEIGHT))
        self.font = pygame.font.Font(None, 36)
        self.pause_button = pygame.Rect(self.gui.WIDTH - 130, 10, 80, 40)
        self.is_paused = False

    def drawPausePlayButton(self):
        button_text = "Pause"
        button_color = (0, 128, 255)
        if self.is_paused:
            button_text = "Go"
            button_color = (255, 140, 0)

        if button_text == "Pause":
            position_x = self.gui.WIDTH - 125  # Vị trí x cho nút Pause
        else:
            position_x = self.gui.WIDTH - 110  # Vị trí x cho nút Play

        pygame.draw.rect(self.screen, button_color, self.pause_button)
        pause_text = self.font.render(button_text, True, (255, 255, 255))
        self.screen.blit(pause_text, (position_x, 20))

    def drawBoard(self):
        self.screen.fill((169, 169, 169))

        # Kiểm tra trạng thái Pause để quyết định có vẽ bảng trò chơi hay không
        if not self.is_paused:
            listSquare = self.board.getListSquare()
            for i in range(len(listSquare)):
                for j in range(len(listSquare[0])):
                    x = j * 48
                    y = i * 48 + 15
                    if not listSquare[i][j].isDropped():
                        border_color = self.NORMAL_BORDER
                        if (i, j) == self.selectedSlot[0] or (i, j) == self.selectedSlot[1]:
                            border_color = "green"
                        try:
                            image_path = os.path.join("images", listSquare[i][j].getValue())
                            image = pygame.image.load(image_path)
                            image = pygame.transform.scale(image, (44, 44))
                            self.screen.blit(image, (x + 2, y + 2))
                            pygame.draw.rect(self.screen, pygame.Color(border_color), (x, y, 48, 48), 3)
                        except Exception as e:
                            print(e)
        else:
            # Hiển thị thông báo khi trò chơi đang ở trạng thái Pause
            pause_text = self.font.render("PAUSED", True, pygame.Color("black"))
            text_rect = pause_text.get_rect(center=(self.gui.WIDTH // 2, self.gui.HEIGHT // 2))
            self.screen.blit(pause_text, text_rect.topleft)

        # Tính thời gian đã trôi qua khi đã bấm Pause
        elapsed_time = time.time() - self.gui.start_time
        if self.is_paused:
            elapsed_time -= time.time() - self.gui.paused_time

        time_left_total_seconds = self.gui.TIME_LIMIT - int(elapsed_time)
        time_left_minutes = time_left_total_seconds // 60
        time_left_seconds = time_left_total_seconds % 60

        percentage = time_left_total_seconds / self.gui.TIME_LIMIT

        if time_left_total_seconds > 150:  # 5 phút - 2 phút 30 giây
            time_color = pygame.Color("brown")  # Màu nền cho số phút:giây
            text_color = pygame.Color("green")  # Màu chữ cho số phút:giây
        elif time_left_total_seconds > 30:  # 2 phút 30 giây - 30 giây
            time_color = pygame.Color("blue")  # Màu nền cho số phút:giây
            text_color = pygame.Color("yellow")  # Màu chữ cho số phút:giây
        else:  # 30 giây cuối cùng
            time_color = pygame.Color("cyan")  # Màu nền cho số phút:giây
            text_color = pygame.Color("red")  # Màu chữ cho số phút:giây

        rect_width = int((self.gui.WIDTH // 2) * percentage)
        pygame.draw.rect(self.screen, pygame.Color("white"), (self.gui.WIDTH // 4, 10, self.gui.WIDTH // 2, 40), 2)
        pygame.draw.rect(self.screen, text_color, (self.gui.WIDTH // 4 + 2, 12, rect_width - 4, 36))

        # Vẽ thời gian đếm ngược
        time_left_str = f"{time_left_minutes:02}:{time_left_seconds:02}"
        text_surface = self.font.render(f"{time_left_str}", True, time_color)
        text_rect = text_surface.get_rect(center=(self.gui.WIDTH // 2, 30))
        self.screen.blit(text_surface, text_rect.topleft)

        # Vẽ điểm số
        score_text = self.font.render(f"Score: {self.gui.score}", True, pygame.Color("pink"))
        self.screen.blit(score_text, (47, 20))  # Vị trí (20, 20) là phía trên bên trái

        # Vẽ nút Pause/Play bằng cách gọi hàm drawPausePlayButton
        self.drawPausePlayButton()

        pygame.display.flip()

    def update(self):
        self.drawBoard()
        pygame.display.flip()

    def handleEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if self.pause_button.collidepoint(x, y):
                self.is_paused = not self.is_paused
                if self.is_paused:
                    self.gui.paused = True
                    self.gui.paused_time = time.time()
                else:
                    self.gui.paused = False
                    self.gui.start_time += time.time() - self.gui.paused_time
                self.update()  # Cập nhật giao diện sau khi thay đổi trạng thái Pause/Play
            else:
                col = x // 48
                row = y // 48

                if 0 <= row < len(self.board.getListSquare()) and 0 <= col < len(self.board.getListSquare()[0]):
                    if self.selectedSlot[0] is None:
                        self.selectedSlot[0] = (row, col)
                        self.selectedImage = self.board.getListSquare()[row][col].getValue()
                    else:
                        self.selectedSlot[1] = (row, col)
                        x0, y0 = self.selectedSlot[0]
                        x1, y1 = self.selectedSlot[1]
                        if self.board.checkMatching(x0, y0, x1, y1):
                            self.selectedSlot = [None, None]

                            # Cập nhật điểm cho người chơi dựa trên thời gian còn lại
                            minutes, seconds = self.gui.get_time_left()
                            time_left_total_seconds = minutes * 60 + seconds

                            if time_left_total_seconds > 150:  # 5 phút - 2 phút 30 giây
                                self.gui.score += 10
                            elif time_left_total_seconds > 30:  # 2 phút 30 giây - 30 giây
                                self.gui.score += 30
                            else:  # 30 giây cuối cùng
                                self.gui.score += 50

                            self.update()
                        else:
                            self.selectedSlot[0] = None
                            self.selectedSlot[1] = None
                        self.update()


class ControlPanel:
    def __init__(self, gui, board_panel):
        self.gui = gui
        self.board_panel = board_panel
        self.initComp()

    def initComp(self):
        self.running = True

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                self.board_panel.handleEvent(event)
            if not self.gui.paused:
                self.board_panel.update()

                if self.board_panel.board.isAllMatched():
                    self.running = False
                    self.gui.show_message("You win!!!", "Congratulations! You have won the game!")
                    pygame.quit()
                    sys.exit()

                if self.gui.get_time_left() == (0, 0):
                    self.running = False
                    self.gui.show_message("You lost!!!", "Time's up! You have lost the game!")
                    pygame.quit()
                    sys.exit()

            pygame.display.flip()

        pygame.quit()
        sys.exit()


class Gui:
    WIDTH = 865
    HEIGHT = 585
    TIME_LIMIT = 300

    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption("Pikachu")
        pygame.display.set_icon(pygame.image.load("images/pikachu.png"))
        pygame.mixer.music.load("sounds/NhacNenGamePikachu-VA-4698057.mp3")
        pygame.mixer.music.play(-1)

        self.root = Tk()
        self.root.withdraw()

        self.board = Board()
        self.board_panel = BoardPanel(self, self.board)
        self.control_panel = ControlPanel(self, self.board_panel)
        self.start_time = time.time()
        self.paused = False
        self.paused_time = None
        self.score = 0  # Điểm số ban đầu là 0
        self.control_panel.run()

    def get_time_left(self):
        if self.paused:
            return 0, 0
        elapsed_time = time.time() - self.start_time
        time_left = self.TIME_LIMIT - int(elapsed_time)
        minutes = time_left // 60
        seconds = time_left % 60
        return minutes, seconds

    def show_message(self, title, message):
        messagebox.showinfo(title, message)

    def close_window(self):
        self.root.destroy()


if __name__ == "__main__":
    gui = Gui()
