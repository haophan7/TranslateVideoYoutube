import pygame, os, random

pygame.init()

# Variables for Game
gameWidth = 870
gameHeight = 670
picSize = 128
gameColumns = 5
gameRows = 4
padding = 10
leftMargin = (gameWidth - ((picSize + padding) * gameColumns)) // 2
rightMargin = leftMargin
topMargin = (gameHeight - ((picSize + padding) * gameRows)) // 2
bottomMargin = topMargin
WHITE = (255, 255, 255)
MAROON = (128, 0, 0)
GREEN = (0, 128, 0)
SILVER = (192, 192, 192)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
selection1 = None
selection2 = None

# Loading the pygame screen.
screen = pygame.display.set_mode((gameWidth, gameHeight))
pygame.display.set_caption('Memory Game')
gameIcon = pygame.image.load('images/Apple.png')
pygame.display.set_icon(gameIcon)
pygame.mixer.music.load("musics/music-for-puzzle-game-146738.mp3")
pygame.mixer.music.play(loops=-1)

# Load the BackGround image into Python
bgImage = pygame.image.load('Background.png')
bgImage = pygame.transform.scale(bgImage, (gameWidth, gameHeight))
bgImageRect = bgImage.get_rect()

# Create list of Memory Pictures
memoryPictures = []
for item in os.listdir('images/'):
    memoryPictures.append(item.split('.')[0])
memoryPicturesCopy = memoryPictures.copy()
memoryPictures.extend(memoryPicturesCopy)
memoryPicturesCopy.clear()
random.shuffle(memoryPictures)

# Load each of the images into the python memory
memPics = []
memPicsRect = []
hiddenImages = []
for item in memoryPictures:
    picture = pygame.image.load(f'images/{item}.png')
    picture = pygame.transform.scale(picture, (picSize, picSize))
    memPics.append(picture)
    pictureRect = picture.get_rect()
    memPicsRect.append(pictureRect)

for i in range(len(memPicsRect)):
    memPicsRect[i][0] = leftMargin + ((picSize + padding) * (i % gameColumns))
    memPicsRect[i][1] = topMargin + ((picSize + padding) * (i % gameRows))
    hiddenImages.append(False)

#print(memoryPictures)
#print(memPics)
#print(memPicsRect)
#print(hiddenImages)

# Variables for score, time, tries
score = 0
tries = 0
time_limit = 60  # 1 phút
start_time = pygame.time.get_ticks()  # Thời gian bắt đầu

gameLoop = True
while gameLoop:
    # Load background image
    screen.blit(bgImage, bgImageRect)

    # Input events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameLoop = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for item in memPicsRect:
                if item.collidepoint(event.pos):
                    if hiddenImages[memPicsRect.index(item)] != True:
                        if selection1 != None:
                            selection2 = memPicsRect.index(item)
                            hiddenImages[selection2] = True
                        else:
                            selection1 = memPicsRect.index(item)
                            hiddenImages[selection1] = True

    for i in range(len(memoryPictures)):
        if hiddenImages[i] == True:
            screen.blit(memPics[i], memPicsRect[i])
        else:
            pygame.draw.rect(screen, WHITE, (memPicsRect[i][0], memPicsRect[i][1], picSize, picSize))

    # Update score and tries
    font = pygame.font.Font(None, 36)
    score_text = font.render(f'Score: {score}', True, MAROON)
    tries_text = font.render(f'Tries: {tries}', True, GREEN)
    time_text = font.render(f'Time: {time_limit - (pygame.time.get_ticks() - start_time) // 1000}', True, SILVER)
    screen.blit(score_text, (10, gameHeight - 60))
    screen.blit(tries_text, (10, gameHeight - 30))
    screen.blit(time_text, (gameWidth - 110, gameHeight - 45))

    pygame.display.update()

    if selection1 != None and selection2 != None:
        if memoryPictures[selection1] == memoryPictures[selection2]:
            score += 10
            tries += 1
            selection1, selection2 = None, None
        else:
            pygame.time.wait(1000)
            hiddenImages[selection1] = False
            hiddenImages[selection2] = False
            tries += 1
            selection1, selection2 = None, None

    # Check win condition
    win = 1
    for number in range(len(hiddenImages)):
        win *= hiddenImages[number]

    # Check time limit
    current_time = pygame.time.get_ticks()
    time_elapsed = (current_time - start_time) // 1000  # Chuyển từ milliseconds sang giây
    time_remaining = max(time_limit - time_elapsed, 0)

    if time_remaining == 0:
        gameLoop = False

    # Check win and lose conditions
    if win == 1:
        gameLoop = False
        end_text = font.render("You win!!!", True, RED)
        end_text_rect = end_text.get_rect(center=(gameWidth // 2, gameHeight // 2 + 300))
        screen.blit(end_text, end_text_rect)
        pygame.display.update()
        pygame.time.wait(7000)
        pygame.quit()
        quit()

    if time_remaining == 0:
        gameLoop = False
        end_text = font.render("You lost!!!", True, BLUE)
        end_text_rect = end_text.get_rect(center=(gameWidth // 2, gameHeight // 2 + 300))
        screen.blit(end_text, end_text_rect)
        pygame.display.update()
        pygame.time.wait(7000)
        pygame.quit()
        quit()

    pygame.display.update()

pygame.quit()
