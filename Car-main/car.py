import pygame
import random

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.mixer.init()
pygame.init()
pygame.font.init()
clock = pygame.time.Clock()
SCREEN_WIDTH, SCREEN_HEIGHT, FPS = 900, 800, 120
WINDOW = pygame.display
WINDOW.set_caption('Car Race')
WINDOW.set_icon(pygame.image.load('graphics/icon.png'))
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


class Background:
    def __init__(self):
        self.bg_image1 = pygame.transform.scale(pygame.image.load('graphics/bg.png').convert_alpha(), (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.bg_image2 = pygame.transform.scale(pygame.image.load('graphics/bg.png').convert_alpha(), (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.rect1 = self.bg_image1.get_rect()
        self.rect1.topleft = (0, 0)
        self.rect2 = self.bg_image2.get_rect()
        self.rect2.topleft = (0, -SCREEN_HEIGHT)
        self.speed = -0.5  # Giảm tốc độ di chuyển của ảnh nền

    def draw(self):
        self.rect1.y += self.speed
        self.rect2.y += self.speed

        if self.rect1.y >= SCREEN_HEIGHT:
            self.rect1.y = self.rect2.y - SCREEN_HEIGHT

        if self.rect2.y >= SCREEN_HEIGHT:
            self.rect2.y = self.rect1.y - SCREEN_HEIGHT

        SCREEN.blit(self.bg_image1, self.rect1)
        SCREEN.blit(self.bg_image2, self.rect2)

        # Kiểm tra nếu ảnh nền 2 (phía dưới) đã di chuyển hơn 0 pixel lên trên màn hình
        if self.rect2.y > 0:
            # Vẽ ảnh nền 1 (phía trên) tiếp theo phía dưới ảnh nền 2 để nối tiếp đường
            SCREEN.blit(self.bg_image1, (self.rect1.x, self.rect2.y - SCREEN_HEIGHT))


class Player:
    def __init__(self):
        self.image_straight = pygame.transform.scale(pygame.image.load('graphics/player_.png').convert_alpha(), (70, 120))
        self.image_left = pygame.transform.scale(pygame.image.load('graphics/player_left_.png').convert_alpha(), (70, 120))
        self.image_right = pygame.transform.scale(pygame.image.load('graphics/player_right_.png').convert_alpha(), (70, 120))
        self.sound_revup = pygame.mixer.Sound('sounds/engine_revup.ogg')
        self.sound_revup.set_volume(0.5)
        self.sound_horn = pygame.mixer.Sound('sounds/horn.ogg')
        self.sound_horn.set_volume(0.3)
        self.image = self.image_straight
        self.trace = (0, 0, 0, 0, 0)
        self.posx, self.posy, self.speed, self.carspeed = 410, 670, 0, -5
        self.moving_left, self.moving_right, self.gas, self.brake = False, False, False, False

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.gameover = True
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.moving_left = True
                elif event.key == pygame.K_RIGHT:
                    self.moving_right = True
                elif event.key == pygame.K_UP:
                    self.gas = True
                elif event.key == pygame.K_DOWN:
                    self.brake = True
            if event.type == pygame.KEYUP:
                self.moving_left, self.moving_right, self.gas, self.brake = False, False, False, False
                self.sound_revup.stop()
        self.image = self.image_straight
        if self.moving_left and not self.posx - 2.5 <= 200:
            self.posx -= 2.5
            self.image = self.image_left
        if self.moving_right and not self.posx + 2.5 >= 625:
            self.posx += 2.5
            self.image = self.image_right
        if self.gas and self.speed < 300:
            self.speed += 1/3
            bg.speed += .05/3
            flag.speed += .005/3
            self.carspeed += .03/3
            if not pygame.mixer.get_busy():
                self.sound_revup.play(loops=0, maxtime=0, fade_ms=1)
        if self.brake and self.speed > 0:
            self.speed -= 1*2
            bg.speed -= .05*2
            flag.speed -= .005*2
            self.carspeed -= .03*2
            self.sound_revup.stop()
        if self.speed <= 0 or bg.speed <= 0:
            self.speed = 0
            bg.speed = 0

    def draw(self):
        self.trace = SCREEN.blit(self.image, (int(self.posx), int(self.posy)))
        self.trace = (self.trace[0], self.trace[1], self.trace[2], self.trace[3])
        # pygame.draw.rect(SCREEN, (255, 206, 28), self.trace, 2)


class Car:
    def __init__(self, posx):
        self.image0 = pygame.transform.scale(pygame.image.load('graphics/car1_.png').convert_alpha(), (140, 120))
        self.image1 = pygame.transform.scale(pygame.image.load('graphics/car2_.png').convert_alpha(), (110, 100))
        self.image2 = pygame.transform.scale(pygame.image.load('graphics/car3_.png').convert_alpha(), (100, 120))
        self.image_list = (self.image0, self.image1, self.image2)
        self.image = self.image_list[2]
        self.trace = (0, 0, 0, 0, 0)
        self.posx, self.posy, self.speed = posx, -500, 0
        self.is_moving = False

    def move(self):
        if not self.is_moving:
            rnd = random.randint(1, game.difficulty)
            if rnd == 50:
                self.is_moving = True
                self.image = self.image_list[random.randint(0, 2)]
                self.speed = random.randint(0, 3)
                if self.speed == 3 and player.speed > 200:
                    player.sound_horn.play(loops=0, maxtime=0, fade_ms=0)
        else:
            self.posy += player.carspeed + self.speed
            if self.posy >= SCREEN_HEIGHT or self.posy <= -999:
                self.is_moving = False
                self.posy = -150

    def draw(self):
        self.trace = SCREEN.blit(self.image, (int(self.posx), int(self.posy)))
        self.trace = (self.trace[0], self.trace[1], self.trace[2], self.trace[3])
        # pygame.draw.rect(SCREEN, (255, 206, 28), self.trace, 2)


class Flag:
    def __init__(self):
        self.image = pygame.image.load('graphics/flag_.png').convert_alpha()
        self.trace = (0, 0, 0, 0)
        self.posx, self.posy, self.speed = random.randint(200, 625), -999, 0
        self.is_moving = False

    def move(self):
        if not self.is_moving:
            self.is_moving = True
            self.posx = random.randint(200, 625)
        else:
            self.posy += self.speed
            if self.posy >= SCREEN_HEIGHT:
                self.is_moving = False
                self.posy = -50
                game.difficulty -= 100
                if game.difficulty <= 100:
                    game.difficulty = 100

    def draw(self):
        self.trace = SCREEN.blit(self.image, (int(self.posx), int(self.posy)))
        # pygame.draw.rect(SCREEN, (255, 206, 28), self.trace, 2)


class Game:
    def __init__(self):
        self.score, self.gameover, self.difficulty = 0, False, 500
        self.FONT = pygame.font.Font('graphics/font_helvetica.ttf', 18)
        pygame.mixer.music.load('sounds/engine_steady.mp3')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(loops=-1)
        self.image = pygame.image.load('graphics/crash_.png').convert_alpha()
        self.sound_crash = pygame.mixer.Sound('sounds/crash.ogg')
        self.sound_crash.set_volume(0.5)
        self.sound_point = pygame.mixer.Sound('sounds/point.ogg')
        self.sound_point.set_volume(0.5)

    def draw_score(self):
        txt_speed = self.FONT.render('Speed: ' + str(int(player.speed)) + ' mph', True, (255, 255, 255))
        txt_score = self.FONT.render('Score: ' + str(self.score), True, (255, 255, 255))
        SCREEN.blit(txt_speed, (5, 605))
        SCREEN.blit(txt_score, (5, 635))

    def collission(self):
        p = pygame.Rect(player.trace)
        f = pygame.Rect(flag.trace)
        cars = [pygame.Rect(car1.trace), pygame.Rect(car2.trace), pygame.Rect(car3.trace), pygame.Rect(car4.trace), pygame.Rect(car5.trace)]

        if p.colliderect(f):
            flag.posx = -50
            game.score += 1
            self.sound_point.play(loops=0, maxtime=0, fade_ms=0)

        for car in cars:
            player_rect = pygame.Rect(player.trace)
            car_rect = pygame.Rect(car)

            if player_rect.colliderect(car_rect):
                player_center = player_rect.centerx
                car_center = car_rect.centerx
                distance = abs(player_center - car_center)

                if distance <= 45:
                    # Tính toán vị trí cho hình ảnh CRASH nằm trên xe người chơi
                    crash_posx = int(player.posx + (player.image.get_width() / 2) - (game.image.get_width() / 2))
                    crash_posy = int(player.posy + (player.image.get_height() / 2) - (game.image.get_height() / 2))
                    SCREEN.blit(self.image, (crash_posx, crash_posy))
                    pygame.mixer.music.stop()
                    player.sound_revup.stop()
                    self.sound_crash.play(loops=0, maxtime=0, fade_ms=1)
                    pygame.display.update()
                    pygame.time.delay(10000)
                    self.gameover = True

    def mainloop(self):
        while not self.gameover:
            clock.tick(FPS)
            SCREEN.fill((0, 0, 0))
            bg.draw()
            flag.move()
            flag.draw()
            player.move()
            player.draw()
            car1.move()
            car1.draw()
            car2.move()
            car2.draw()
            car3.move()
            car3.draw()
            car4.move()
            car4.draw()
            car5.move()
            car5.draw()
            game.draw_score()
            game.collission()
            WINDOW.update()


bg = Background()
player = Player()
car1 = Car(posx=200)
car2 = Car(posx=292)
car3 = Car(posx=395)
car4 = Car(posx=498)
car5 = Car(posx=590)
flag = Flag()
game = Game()

game.mainloop()
pygame.quit()
quit()
