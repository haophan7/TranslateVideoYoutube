import pygame
import os
import random

os.environ['SDL_VIDEO_CENTERED'] = '1'  # THIS LINE IS USED TO CENTER THE WINDOW

pygame.init()  # INITIALIZING pygame
pygame.mixer.init()  # INITIALIZING pygame.mixer
font = pygame.font.Font('files/fonts/revue.ttf', 50)  # LOADING THE FONT FILE FROM THE PATH AND SIZE OF IT IS 50.
game_font = pygame.font.Font('files/fonts/revue.ttf', 30)  # LOADING THE FONT FILE FROM THE PATH AND SIZE OF IT IS 30.
pygame.mixer.music.load('files/sounds/music.mp3')
pygame.mixer.music.play(-1, 3.0)  # -1 IS USED FOR LOOP AND 3.0 MEANS THAT MUSIC WILL START FROM 3.0 SECONDS
clock = pygame.time.Clock()  # ADDING CLOCK FOR SETTING THE FPS

# COLORS #
WHITE = (225, 225, 225)  # PUTTING HEX WHITE COLOR IN A VARIABLE (WHITE)
BLACK = (60, 60, 60)  # PUTTING HEX GREY COLOR IN A VARIABLE (BLACK)
YELLOW = (255, 255, 0)  # PUTTING HEX YELLOW COLOR IN A VARIABLE (YELLOW)
GREEN = (0, 128, 0)  # PUTTING HEX GREEN COLOR IN A VARIABLE (GREEN)
LIME = (0, 139, 0)  # PUTTING HEX LIME COLOR IN A VARIABLE (LIME)
RED = (255, 0, 0)  # PUTTING HEX RED COLOR IN A VARIABLE (RED)
BLUE = (0, 0, 255)  # PUTTING HEX BLUE COLOR IN A VARIABLE (BLUE)

screen = pygame.display.set_mode((1000, 600))  # SETTING THE WINDOW SIZE OF THE GAME
pygame.display.set_caption("TABLE TENNIS GAME")  # SETTING THE TITLE OF THE GAME WINDOW
pygame.display.set_icon(pygame.image.load('files/images/pong.png'))

# VARIABLES #
FPS = 60  # FPS = FRAME PER SECOND (IF U DON'T KNOW)
running = True
click = False
clicked = False
clicking = False
player = pygame.Rect(10, 230, 30, 140)
opponent = pygame.Rect(960, 230, 30, 140)
ball = pygame.Rect(481, 281, 38, 38)
player_change, ballX, ballY, opponent_change = 0, 20, 20, 0
player_score, opponent_score = 0, 0
score_time = 0


# ================================= GAME AREA FUNCTION ========================================== #
def start():
    global ballX, ballY, score_time, game_font

    current_time = pygame.time.get_ticks()
    ball.center = (495, 295)
    one, two, three = "1", "2", "3"

    if current_time - score_time < 700:
        number_three = game_font.render(str(three), True, YELLOW)
        screen.blit(number_three, (492, 288))
    if 700 < current_time - score_time < 1400:
        number_two = game_font.render(str(two), True, YELLOW)
        screen.blit(number_two, (492, 288))
    if 1400 < current_time - score_time < 2100:
        number_one = game_font.render(str(one), True, YELLOW)
        screen.blit(number_one, (492, 288))

    if current_time - score_time < 2100:
        ballX, ballY = 0, 0
    else:
        ballX = random.choice((20, -20))
        ballY = random.choice((20, -20))
        score_time = 0


def display_winner(winner):
    winner_font = pygame.font.Font(None, 70)
    winner_text = winner_font.render(f"{winner} wins!", True, BLACK)
    screen.blit(winner_text, (340, 250))
    pygame.display.update()
    pygame.time.delay(10000)  # Delay for 10 seconds


def game():
    global running, player_score, opponent_score, score_time, player_change, opponent_change, ballX, ballY
    pop = pygame.mixer.Sound('files/sounds/pop.wav')
    win_sound = pygame.mixer.Sound('files/sounds/win.wav')

    ball_image = pygame.image.load('files/images/ball.png')  # Load ball image
    ball_image = pygame.transform.scale(ball_image, (48, 48))  # Resize ball image

    winner = ""  # Khởi tạo biến winner trước khi sử dụng

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    if player.top - 70 >= 40:
                        player.y -= 70
                    else:
                        player.y = 40
                if event.key == pygame.K_s:
                    if player.bottom + 70 <= 580:
                        player.y += 70
                    else:
                        player.y = 580 - player.height
                if event.key == pygame.K_UP:
                    if opponent.top - 70 >= 40:
                        opponent.y -= 70
                    else:
                        opponent.y = 40
                if event.key == pygame.K_DOWN:
                    if opponent.bottom + 70 <= 580:
                        opponent.y += 70
                    else:
                        opponent.y = 580 - opponent.height

        screen.fill(LIME)
        pygame.draw.aaline(screen, WHITE, (40, 40), (40, 580))
        pygame.draw.aaline(screen, WHITE, (960, 40), (960, 580))
        pygame.draw.line(screen, WHITE, (500, 40), (500, 580), 2)
        pygame.draw.line(screen, WHITE, (0, 300), (1000, 300), 2)
        pygame.draw.line(screen, WHITE, (0, 40), (1000, 40), 2)
        pygame.draw.line(screen, WHITE, (0, 580), (1000, 580), 2)
        pygame.draw.rect(screen, RED, player)
        screen.blit(ball_image, ball)  # Draw ball image
        pygame.draw.rect(screen, BLUE, opponent)

        player.x = 40
        opponent.x = 1000 - 40 - opponent.width

        player_score_str = str(player_score)
        if len(player_score_str) > 1:
            player_text = game_font.render(player_score_str, True, BLACK)
        else:
            player_text = game_font.render(" " + player_score_str, True, BLACK)
        # Clear previous player score
        pygame.draw.rect(screen, LIME, (430, 10, 30, 50))
        screen.blit(player_text, (430, 10))  # Display updated player score
        # Draw line underneath player score
        pygame.draw.rect(screen, WHITE, (430, 40, 30, 2), 2)

        opponent_text = game_font.render(f"{opponent_score}", True, BLACK)
        # Clear previous opponent score
        pygame.draw.rect(screen, LIME, (535, 10, 30, 50))
        screen.blit(opponent_text, (535, 10))  # Display updated opponent score
        # Draw line underneath opponent score
        pygame.draw.rect(screen, WHITE, (535, 40, 30, 2), 2)

        if score_time:
            start()

        pygame.display.update()
        clock.tick(FPS)

        player.y += player_change
        if player.y <= 40:
            player_change = 0
            player.y = 40
        if player.y >= 600 - 150:
            player_change = 0
            player.y = 600 - 150

        opponent.y += opponent_change
        if opponent.y <= 40:
            opponent_change = 0
            opponent.y = 40
        if opponent.y >= 600 - 150:
            opponent_change = 0
            opponent.y = 600 - 150

        ball.x += ballX
        ball.y += ballY

        if ball.colliderect(player):  # Kiểm tra va chạm với player
            pop.play()
            ball.left = player.right - 1
            ballX = abs(ballX)  # Thay đổi hướng di chuyển theo chiều dương
        elif ball.colliderect(opponent):  # Kiểm tra va chạm với opponent
            pop.play()
            ball.right = opponent.left + 1
            ballX = -abs(ballX)  # Thay đổi hướng di chuyển theo chiều âm

        if ball.y >= 600 - 38:
            ballY = -20
        if ball.y <= 0:
            ballY = 20

        if ball.x >= 1000 - 32:  # Nếu quả bóng đi qua phía bên phải
            start()
            if ball.y >= 40 and ball.y <= 580:  # Nếu quả bóng nằm trong khoảng đường biên ngang
                player_score += 1
                if player_score >= 10:
                    player_score = 10
                    winner = "Player"
                    running = False
                score_time = pygame.time.get_ticks()
                if player_score == 10:
                    player_text = game_font.render("10", True, BLACK)  # Update player score to 10
                    # Clear previous player score
                    pygame.draw.rect(screen, LIME, (430, 10, 30, 50))
                    screen.blit(player_text, (430, 10))  # Display updated player score
                    # Draw line underneath player score
                    pygame.draw.rect(screen, WHITE, (430, 40, 30, 2), 2)
        elif ball.x <= -20:  # Nếu quả bóng đi qua phía bên trái
            start()
            if ball.y >= 40 and ball.y <= 580:  # Nếu quả bóng nằm trong khoảng đường biên ngang
                opponent_score += 1
                if opponent_score >= 10:
                    opponent_score = 10
                    winner = "Opponent"
                    running = False
                score_time = pygame.time.get_ticks()
                if opponent_score == 10:
                    opponent_text = game_font.render("10", True, BLACK)  # Update opponent score to 10
                    # Clear previous opponent score
                    pygame.draw.rect(screen, LIME, (535, 10, 30, 50))
                    screen.blit(opponent_text, (535, 10))  # Display updated opponent score
                    # Draw line underneath opponent score
                    pygame.draw.rect(screen, WHITE, (535, 40, 30, 2), 2)

        pygame.display.update()
        clock.tick(FPS)

        if not running:
            win_sound.play()
            display_winner(winner)
            pygame.time.delay(10000)  # Delay for 10 seconds


# =============================== START MENU FUNCTION ================================= #
def menu():
    def __quit__():
        quit()

    global running, clicked
    main_font = pygame.font.Font('files/fonts/capsconst.ttf', 50)  # LOADING FONT AND SIZE OF IT IS 50.
    screen.fill(BLACK)  # FILLING THE GREY(LIGHT BLACK) COLOR ON THE SCREEN TO HIDE PREVIOUS OBJECTS

    heading = main_font.render("MAIN MENU", True, WHITE)  # (1)TEXT, (2)ANTI-ALIASING, (3)COLOR OF FONT
    screen.blit(heading, (30, 30))  # DISPLAYING THE ABOVE TEXT

    pic = pygame.image.load('files/textures/pong.png')  # LOADING AN IMAGE
    screen.blit(pic, (100, 150))  # DISPLAYING ABOVE IMAGE

    play_game_rect = pygame.Rect(545, 195, 380, 60)  # MAKING A RECTANGLE OF DESIRED SIDES
    play_game = main_font.render("PLAY GAME", True, WHITE)  # (1)TEXT, (2)ANTI-ALIASING, (3)COLOR OF FONT
    screen.blit(play_game, (550, 200))  # DISPLAYING THE ABOVE TEXT
    pygame.draw.rect(screen, BLACK, play_game_rect, 1)  # DISPLAYING THE ABOVE RECTANGLE

    exit_game_rect = pygame.Rect(545, 295, 405, 60)  # MAKING A RECTANGLE OF DESIRED SIDES
    exit_game = main_font.render("EXIT GAME", True, WHITE)  # (1)TEXT, (2)ANTI-ALIASING, (3)COLOR OF FONT
    screen.blit(exit_game, (550, 300))  # DISPLAYING THE ABOVE TEXT
    pygame.draw.rect(screen, BLACK, exit_game_rect, 1)  # DISPLAYING THE ABOVE RECTANGLE

    pygame.display.update()  # UPDATING THE SCREEN (TO MAKE OBJECTS VISIBLE)

    while running:  # MAKING A INFINITE WHILE LOOP THAT WILL STOP WHEN USER QUITS THE GAME
        for events in pygame.event.get():
            if events.type == pygame.QUIT:  # WHEN USER CLICKS ON CLOSE BUTTON THEN THE LOOP WILL END AND GAME ENDS
                running = False
            if events.type == pygame.MOUSEBUTTONUP:
                if events.button == 1:
                    x, y = pygame.mouse.get_pos()  # THIS WILL GET THE RELEASE POSITION
                    clicked = True
                    if play_game_rect.collidepoint(x, y):
                        if clicked:
                            game()
                    if exit_game_rect.collidepoint(x, y):
                        if clicked:
                            __quit__()

        pygame.display.update()
        clock.tick(FPS)


while running:  # MAKING A INFINITE WHILE LOOP THAT WILL STOP WHEN USER QUITS THE GAME
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # WHEN USER CLICKS ON CLOSE BUTTON THEN THE LOOP WILL END AND GAME ENDS
            running = False
        if event.type == pygame.KEYUP:  # IF ANY BUTTON IS RELEASED
            if event.key == pygame.K_SPACE:  # WHEN SPACEBAR IS PRESSED THEN IT WILL CHANGE THE VALUE OF VARIABLE TO TRUE
                click = True

    screen.fill(BLACK)  # FILL THE BLACK COLOR TO THE SCREEN

    box = pygame.Rect(50, 50, 900, 500)  # MAKING A RECTANGLE OF DESIRED LENGTH
    pygame.draw.rect(screen, WHITE, box, 3)  # DRAWING THE ABOVE RECTANGLE ON THE SCREEN

    image = pygame.image.load('files/textures/pong.png')  # LOADING THE IMAGE TO THE VARIABLE
    screen.blit(image, (320, 80))  # DISPLAY THE ABOVE IMAGE AT DESIRED LOCATION

    ahead = font.render('PRESS SPACEBAR TO CONTINUE', True, WHITE)  # LOADING TEXT
    screen.blit(ahead, (85, 480))  # DISPLAYING TEXT ON THE SCREEN AT DESIRED POSITION

    if click:  # IF VALUE OF click VARIABLE IS True THEN CALL menu() FUNCTION
        menu()

    pygame.display.update()  # USED TO UPDATE THE SCREEN (FOR MAKING OBJECT ABOVE VISIBLE ON THE SCREEN)
    clock.tick(FPS)
