import pygame
import math
import random
from pygame import mixer

pygame.display.init()
pygame.font.init()
pygame.mixer.init()

screen = pygame.display.set_mode((1366, 700))

mixer.music.load('back.mp3')
mixer.music.play(-1)
pygame.display.set_caption("TANK WAR")
pygame.display.set_icon(pygame.image.load("title.png"))

bgimg = pygame.image.load("bg.png")
heroimg = pygame.image.load("tank.png")
enemyimg = pygame.image.load("enemy_tank.png")
bullet = pygame.image.load("bullet.png")
enemybullet = pygame.image.load("enemy_bullet.png")
heart_img = pygame.image.load("heart.png")
enemyheart_img = pygame.image.load("enemy_heart.png")
brick_img = pygame.image.load("break_brick.png")
solid_brick_img = pygame.image.load("solid_brick.png")
other_tank_img = pygame.image.load("other_tank.png")
other_bullet_img = pygame.image.load("other_bullet.png")

hero_width, hero_height = heroimg.get_size()
bullet_width, bullet_height = bullet.get_size()

herox = 1228
heroy = 600
enemyx = 72
enemyy = 600

hx = 0
hy = 0
ex = 0
ey = 0

last = 'up'
elast = 'up'

state = 'ready'
e_state = 'ready'

bullets = []
enemy_bullets = []

player_health = 3
enemy_health = 3

boom_sound = mixer.Sound("boom.wav")

bricks = []

other_tank_health = 10

speed = 0.5  # Tốc độ di chuyển

other_tank_x = random.randint(0, 1366 - hero_width)
other_tank_y = random.randint(0, 700 - hero_height)
other_tank_speed = 0.5
other_tank_directions = ['up', 'down', 'left', 'right']
other_tank_direction = random.choice(other_tank_directions)
other_bullets = []

r_hero_up = pygame.transform.rotate(heroimg, 0)
r_hero_right = pygame.transform.rotate(heroimg, -90)
r_hero_left = pygame.transform.rotate(heroimg, 90)
r_hero_down = pygame.transform.rotate(heroimg, 180)

r_enemy_up = pygame.transform.rotate(enemyimg, 0)
r_enemy_right = pygame.transform.rotate(enemyimg, -90)
r_enemy_left = pygame.transform.rotate(enemyimg, 90)
r_enemy_down = pygame.transform.rotate(enemyimg, 180)

r_other_tank_up = pygame.transform.rotate(other_tank_img, 0)
r_other_tank_right = pygame.transform.rotate(other_tank_img, -90)
r_other_tank_left = pygame.transform.rotate(other_tank_img, 90)
r_other_tank_down = pygame.transform.rotate(other_tank_img, 180)

r_other_bullet_up = pygame.transform.rotate(other_bullet_img, 0)
r_other_bullet_right = pygame.transform.rotate(other_bullet_img, -90)
r_other_bullet_left = pygame.transform.rotate(other_bullet_img, 90)
r_other_bullet_down = pygame.transform.rotate(other_bullet_img, 180)

def hero(m_hero, x, y):
    screen.blit(m_hero, (x, y))

def bul(m_bu, xx, yy):
    screen.blit(m_bu, (xx, yy))

def enemy(m_enemy, x, y):
    screen.blit(m_enemy, (x, y))

def ebul(m_ebu, exx, eyy):
    screen.blit(m_ebu, (exx, eyy))

def draw_other_tank(x, y, direction):
    if direction == 'up':
        screen.blit(r_other_tank_up, (x, y))
    elif direction == 'down':
        screen.blit(r_other_tank_down, (x, y))
    elif direction == 'left':
        screen.blit(r_other_tank_left, (x, y))
    elif direction == 'right':
        screen.blit(r_other_tank_right, (x, y))

def draw_other_bullets(bullets_list):
    for bullet_data in bullets_list:
        direction = bullet_data['direction']
        if direction == 'up':
            screen.blit(r_other_bullet_up, (bullet_data['x'], bullet_data['y']))
        elif direction == 'down':
            screen.blit(r_other_bullet_down, (bullet_data['x'], bullet_data['y']))
        elif direction == 'left':
            screen.blit(r_other_bullet_left, (bullet_data['x'], bullet_data['y']))
        elif direction == 'right':
            screen.blit(r_other_bullet_right, (bullet_data['x'], bullet_data['y']))

# Function to fire other tank bullet
def fire_other_bullet(x, y, direction, bullets_list):
    bullet_speed = 5
    bullet_data = {
        'x': x + (hero_width - bullet_width) / 2,
        'y': y + (hero_height - bullet_height) / 2,
        'direction': direction,
        'image': other_bullet_img,
        'speed': bullet_speed
    }
    bullets_list.append(bullet_data)

def draw_brick(x, y):
    screen.blit(brick_img, (x, y))

def check_bullet_solid_collision(bullets_list, solids):
    for bullet_data in bullets_list:
        bullet_rect = pygame.Rect(bullet_data['x'], bullet_data['y'], bullet_width, bullet_height)
        for solid in solids:
            solid_rect = pygame.Rect(solid['x'], solid['y'], solid_brick_img.get_width(), solid_brick_img.get_height())
            if bullet_rect.colliderect(solid_rect):
                bullets_list.remove(bullet_data)
                return True
    return False

def fire_bullet(x, y, direction, bullets_list, bullet_img):
    bullet_speed = 5  # Tốc độ di chuyển của viên đạn
    bullet_data = {
        'x': x + (hero_width - bullet_width) / 2,
        'y': y + (hero_height - bullet_height) / 2,
        'direction': direction,
        'image': bullet_img,
        'speed': bullet_speed
    }
    bullets_list.append(bullet_data)

def check_collision(bullets_list, target_x, target_y, target_width, target_height):
    global player_health, enemy_health
    for bullet_data in bullets_list:
        bullet_rect = pygame.Rect(bullet_data['x'], bullet_data['y'], bullet_width, bullet_height)
        target_rect = pygame.Rect(target_x, target_y, target_width, target_height)
        if bullet_rect.colliderect(target_rect):
            bullets_list.remove(bullet_data)
            boom_sound.play()
            if target_x == herox and target_y == heroy:  # Nếu đạn bắn trúng player
                player_health -= 1
                if player_health == 0:
                    display_text("ENEMY WINS!", (1366 // 2, 700 // 2), 60, (0, 255, 0))
                    pygame.display.update()
                    pygame.time.delay(5000)
                    pygame.quit()
                    quit()
            elif target_x == enemyx and target_y == enemyy:  # Nếu đạn bắn trúng enemy
                enemy_health -= 1
                if enemy_health == 0:
                    display_text("PLAYER WINS!", (1366 // 2, 700 // 2), 60, (255, 0, 0))
                    pygame.display.update()
                    pygame.time.delay(5000)
                    pygame.quit()
                    quit()
            else:
                return True
    return False

def check_solid_collision(rect, solids):
    for solid in solids:
        solid_rect = pygame.Rect(solid['x'], solid['y'], solid_brick_img.get_width(), solid_brick_img.get_height())
        if rect.colliderect(solid_rect):
            return True
    return False

# Kiểm tra va chạm cho other tank với các viên gạch solid và break
def check_other_tank_collision(rect, direction, bricks):
    for brick in bricks:
        brick_rect = pygame.Rect(brick['x'], brick['y'], brick_img.get_width(), brick_img.get_height())
        if rect.colliderect(brick_rect):
            if direction == 'right':
                rect.right = brick_rect.left
                return 'left'  # quay đầu và di chuyển sang trái
            elif direction == 'left':
                rect.left = brick_rect.right
                return 'right'  # quay đầu và di chuyển sang phải
            elif direction == 'down':
                rect.bottom = brick_rect.top
                return 'up'  # quay đầu và di chuyển lên trên
            elif direction == 'up':
                rect.top = brick_rect.bottom
                return 'down'  # quay đầu và di chuyển xuống dưới
    return direction  # nếu không có va chạm, giữ nguyên hướng di chuyển

def update_brick_status(bullets_list, bricks):
    for bullet_data in bullets_list:
        bullet_rect = pygame.Rect(bullet_data['x'], bullet_data['y'], bullet_width, bullet_height)
        for brick in bricks:
            brick_rect = pygame.Rect(brick['x'], brick['y'], brick_img.get_width(), brick_img.get_height())
            if bullet_rect.colliderect(brick_rect):
                if brick in bricks:
                    bricks.remove(brick)
                bullets_list.remove(bullet_data)
                break

def update_solid_brick_status(bullets_list, solid_bricks):
    for bullet_data in bullets_list:
        bullet_rect = pygame.Rect(bullet_data['x'], bullet_data['y'], bullet_width, bullet_height)
        for brick in solid_bricks:
            brick_rect = pygame.Rect(brick['x'], brick['y'], solid_brick_img.get_width(), solid_brick_img.get_height())
            if bullet_rect.colliderect(brick_rect):
                bullets_list.remove(bullet_data)
                break

def adjust_position_due_to_collision(rect, direction, brick_rect):
    if direction == 'right':
        rect.right = brick_rect.left
    elif direction == 'left':
        rect.left = brick_rect.right
    elif direction == 'down':
        rect.bottom = brick_rect.top
    elif direction == 'up':
        rect.top = brick_rect.bottom

def check_tank_collision():
    global herox, heroy, enemyx, enemyy, hx, hy, ex, ey, other_tank_x, other_tank_y, other_tank_direction
    player_rect = pygame.Rect(herox, heroy, hero_width, hero_height)
    enemy_rect = pygame.Rect(enemyx, enemyy, hero_width, hero_height)
    other_tank_rect = pygame.Rect(other_tank_x, other_tank_y, hero_width, hero_height)

    # Kiểm tra va chạm giữa player và enemy
    if player_rect.colliderect(enemy_rect):
        herox -= hx
        heroy -= hy
        enemyx -= ex
        enemyy -= ey
        hx = hy = ex = ey = 0

    # Kiểm tra va chạm giữa player và other
    if player_rect.colliderect(other_tank_rect):
        herox -= hx
        heroy -= hy
        hx = hy = 0

    # Kiểm tra va chạm giữa enemy và other
    if enemy_rect.colliderect(other_tank_rect):
        enemyx -= ex
        enemyy -= ey
        ex = ey = 0

def display_text(text, position, size, color):
    font = pygame.font.SysFont(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=position)
    screen.blit(text_surface, text_rect)

# Adding multiple bricks to the list
for i in range(5):
    bricks.append({'x': 0, 'y': 490})
    bricks.append({'x': 50, 'y': 490})
    bricks.append({'x': 100, 'y': 490})
    bricks.append({'x': 150, 'y': 490})
    bricks.append({'x': 150, 'y': 540})
    bricks.append({'x': 150, 'y': 590})
    bricks.append({'x': 150, 'y': 640})
    bricks.append({'x': 1306, 'y': 490})
    bricks.append({'x': 1256, 'y': 490})
    bricks.append({'x': 1206, 'y': 490})
    bricks.append({'x': 1156, 'y': 490})
    bricks.append({'x': 1156, 'y': 540})
    bricks.append({'x': 1156, 'y': 590})
    bricks.append({'x': 1156, 'y': 640})

    bricks.append({'x': 653, 'y': 0})
    bricks.append({'x': 653, 'y': 50})
    bricks.append({'x': 653, 'y': 100})
    bricks.append({'x': 653, 'y': 150})
    bricks.append({'x': 653, 'y': 200})
    bricks.append({'x': 653, 'y': 250})
    bricks.append({'x': 653, 'y': 300})
    bricks.append({'x': 653, 'y': 350})
    bricks.append({'x': 653, 'y': 400})
    bricks.append({'x': 653, 'y': 450})
    bricks.append({'x': 653, 'y': 500})
    bricks.append({'x': 653, 'y': 550})
    bricks.append({'x': 653, 'y': 600})
    bricks.append({'x': 653, 'y': 650})

# Khai báo danh sách vị trí cho các viên gạch cố định
solid_bricks = [
    {'x': 0, 'y': 430},
    {'x': 70, 'y': 290},
    {'x': 70, 'y': 150},
    {'x': 210, 'y': 360},
    {'x': 210, 'y': 220},
    {'x': 210, 'y': 80},
    {'x': 140, 'y': 430},
    {'x': 210, 'y': 500},
    {'x': 350, 'y': 10},
    {'x': 350, 'y': 150},
    {'x': 350, 'y': 290},
    {'x': 350, 'y': 430},
    {'x': 350, 'y': 570},
    {'x': 590, 'y': 10},
    {'x': 590, 'y': 150},
    {'x': 590, 'y': 290},
    {'x': 590, 'y': 430},
    {'x': 590, 'y': 570},
    {'x': 210, 'y': 640},
    {'x': 1306, 'y': 430},
    {'x': 1236, 'y': 290},
    {'x': 1236, 'y': 150},
    {'x': 1166, 'y': 430},
    {'x': 1096, 'y': 500},
    {'x': 1096, 'y': 360},
    {'x': 1096, 'y': 220},
    {'x': 1096, 'y': 80},
    {'x': 956, 'y': 10},
    {'x': 956, 'y': 150},
    {'x': 956, 'y': 290},
    {'x': 956, 'y': 430},
    {'x': 956, 'y': 570},
    {'x': 1096, 'y': 640},
    {'x': 716, 'y': 640},
    {'x': 716, 'y': 500},
    {'x': 716, 'y': 360},
    {'x': 716, 'y': 220},
    {'x': 716, 'y': 80},
]

while True:
    screen.blit(bgimg, (0, 0))

    font = pygame.font.SysFont(None, 36)
    player_text = font.render("PLAYER:", True, (255, 255, 255))
    screen.blit(player_text, (1100, 20))

    heart_x = 1210
    heart_y = 15
    heart_spacing = 40
    for i in range(player_health):
        screen.blit(heart_img, (heart_x + i * heart_spacing, heart_y))

    enemy_text = font.render("ENEMY:", True, (255, 255, 255))
    screen.blit(enemy_text, (50, 20))

    heart_x = 150
    heart_y = 15
    heart_spacing = 40
    for i in range(enemy_health):
        screen.blit(enemyheart_img, (heart_x + i * heart_spacing, heart_y))

    # Drawing all bricks
    for brick in bricks:
        draw_brick(brick['x'], brick['y'])

    # Vẽ tất cả các viên gạch cố định từ danh sách
    for brick in solid_bricks:
        screen.blit(solid_brick_img, (brick['x'], brick['y']))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT and herox + hero_width < 1366:
                hx = speed
                last = 'right'
            if event.key == pygame.K_LEFT and herox > 0:
                hx = -speed
                last = 'left'
            if event.key == pygame.K_UP and heroy > 0:
                hy = -speed
                last = 'up'
            if event.key == pygame.K_DOWN and heroy + hero_height < 700:
                hy = speed
                last = 'down'
            if event.key == pygame.K_p:
                bullm = mixer.Sound("shoot.wav")
                bullm.play()
                fire_bullet(herox, heroy, last, bullets, bullet)

            if event.key == pygame.K_d and enemyx + hero_width < 1366:
                ex = speed
                elast = 'right'
            if event.key == pygame.K_a and enemyx > 0:
                ex = -speed
                elast = 'left'
            if event.key == pygame.K_w and enemyy > 0:
                ey = -speed
                elast = 'up'
            if event.key == pygame.K_s and enemyy + hero_height < 700:
                ey = speed
                elast = 'down'
            if event.key == pygame.K_b:
                bullm = mixer.Sound("shoot.wav")
                bullm.play()
                fire_bullet(enemyx, enemyy, elast, enemy_bullets, enemybullet)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                hx = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                hy = 0
            if event.key == pygame.K_w or event.key == pygame.K_s:
                ey = 0
            if event.key == pygame.K_a or event.key == pygame.K_d:
                ex = 0

    herox += hx
    heroy += hy
    enemyx += ex
    enemyy += ey

    # Player
    next_hero_x = herox + hx
    next_hero_y = heroy + hy

    hero_rect = pygame.Rect(next_hero_x, next_hero_y, hero_width, hero_height)
    for brick in bricks:
        brick_rect = pygame.Rect(brick['x'], brick['y'], brick_img.get_width(), brick_img.get_height())
        if hero_rect.colliderect(brick_rect):
            if hx > 0:  # Điều chỉnh sang phải
                next_hero_x = brick['x'] - hero_width
            elif hx < 0:  # Điều chỉnh sang trái
                next_hero_x = brick['x'] + brick_img.get_width()

            if hy > 0:  # Điều chỉnh xuống
                next_hero_y = brick['y'] - hero_height
            elif hy < 0:  # Điều chỉnh lên
                next_hero_y = brick['y'] + brick_img.get_height()

            break

    herox = next_hero_x
    heroy = next_hero_y

    # Enemy
    next_enemy_x = enemyx + ex
    next_enemy_y = enemyy + ey

    enemy_rect = pygame.Rect(next_enemy_x, next_enemy_y, hero_width, hero_height)
    for brick in bricks:
        brick_rect = pygame.Rect(brick['x'], brick['y'], brick_img.get_width(), brick_img.get_height())
        if enemy_rect.colliderect(brick_rect):
            if ex > 0:  # Điều chỉnh sang phải
                next_enemy_x = brick['x'] - hero_width
            elif ex < 0:  # Điều chỉnh sang trái
                next_enemy_x = brick['x'] + brick_img.get_width()

            if ey > 0:  # Điều chỉnh xuống
                next_enemy_y = brick['y'] - hero_height
            elif ey < 0:  # Điều chỉnh lên
                next_enemy_y = brick['y'] + brick_img.get_height()

            break

    enemyx = next_enemy_x
    enemyy = next_enemy_y

    # Kiểm tra va chạm viên đạn của player với other tank
    if check_collision(bullets, other_tank_x, other_tank_y, hero_width, hero_height):
        other_tank_health -= 1
        if other_tank_health == 0:
            display_text("PLAYER WINS!", (1366 // 2, 700 // 2), 60, (255, 0, 0))
            pygame.display.update()
            pygame.time.delay(5000)
            pygame.quit()
            quit()

    # Kiểm tra va chạm viên đạn của enemy với other tank
    if check_collision(enemy_bullets, other_tank_x, other_tank_y, hero_width, hero_height):
        other_tank_health -= 1
        if other_tank_health == 0:
            display_text("ENEMY WINS!", (1366 // 2, 700 // 2), 60, (0, 255, 0))
            pygame.display.update()
            pygame.time.delay(5000)
            pygame.quit()
            quit()

    # Kiểm tra và điều chỉnh vị trí cho player khi va chạm với các viên gạch solid
    next_hero_rect = pygame.Rect(next_hero_x, next_hero_y, hero_width, hero_height)
    for brick in solid_bricks:
        brick_rect = pygame.Rect(brick['x'], brick['y'], solid_brick_img.get_width(), solid_brick_img.get_height())
        if next_hero_rect.colliderect(brick_rect):
            adjust_position_due_to_collision(next_hero_rect, last, brick_rect)

    herox = next_hero_rect.x
    heroy = next_hero_rect.y

    # Kiểm tra và điều chỉnh vị trí cho enemy khi va chạm với các viên gạch solid
    next_enemy_rect = pygame.Rect(next_enemy_x, next_enemy_y, hero_width, hero_height)
    for brick in solid_bricks:
        brick_rect = pygame.Rect(brick['x'], brick['y'], solid_brick_img.get_width(), solid_brick_img.get_height())
        if next_enemy_rect.colliderect(brick_rect):
            adjust_position_due_to_collision(next_enemy_rect, elast, brick_rect)

    enemyx = next_enemy_rect.x
    enemyy = next_enemy_rect.y

    # Movement for other tank
    if other_tank_direction == 'up':
        other_tank_y -= other_tank_speed
    elif other_tank_direction == 'down':
        other_tank_y += other_tank_speed
    elif other_tank_direction == 'left':
        other_tank_x -= other_tank_speed
    elif other_tank_direction == 'right':
        other_tank_x += other_tank_speed

    # Change direction randomly
    if random.randint(0, 100) < 2:  # 2% chance to change direction
        other_tank_direction = random.choice(other_tank_directions)

    # Fire bullet randomly
    if random.randint(0, 100) < 2:  # 2% chance to fire
        fire_other_bullet(other_tank_x, other_tank_y, other_tank_direction, other_bullets)

    # Move other bullets
    for bullet_data in other_bullets:
        direction = bullet_data['direction']
        bullet_speed = bullet_data['speed']
        if direction == 'up':
            bullet_data['y'] -= bullet_speed
        elif direction == 'down':
            bullet_data['y'] += bullet_speed
        elif direction == 'left':
            bullet_data['x'] -= bullet_speed
        elif direction == 'right':
            bullet_data['x'] += bullet_speed

    # Movement for other tank
    if other_tank_direction == 'up':
        other_tank_y -= other_tank_speed
        if other_tank_y < 0:
            other_tank_y = 0
    elif other_tank_direction == 'down':
        other_tank_y += other_tank_speed
        if other_tank_y > 700 - hero_height:
            other_tank_y = 700 - hero_height
    elif other_tank_direction == 'left':
        other_tank_x -= other_tank_speed
        if other_tank_x < 0:
            other_tank_x = 0
    elif other_tank_direction == 'right':
        other_tank_x += other_tank_speed
        if other_tank_x > 1366 - hero_width:
            other_tank_x = 1366 - hero_width

    # Kiểm tra và điều chỉnh vị trí cho other tank khi va chạm với các viên gạch solid và break
    next_other_tank_rect = pygame.Rect(other_tank_x, other_tank_y, hero_width, hero_height)
    new_direction = check_other_tank_collision(next_other_tank_rect, other_tank_direction, bricks)
    new_direction1 = check_other_tank_collision(next_other_tank_rect, other_tank_direction, solid_bricks)
    if new_direction:
        other_tank_direction = new_direction
    if new_direction1:
        other_tank_direction = new_direction1

    other_tank_x = next_other_tank_rect.x
    other_tank_y = next_other_tank_rect.y

    # Lựa chọn hình ảnh phù hợp với hướng di chuyển
    r_hero = r_hero_up if last == 'up' else r_hero_right if last == 'right' else r_hero_left if last == 'left' else r_hero_down
    r_enemy = r_enemy_up if elast == 'up' else r_enemy_right if elast == 'right' else r_enemy_left if elast == 'left' else r_enemy_down

    # Kiểm tra và cập nhật vị trí cho player và enemy
    if herox < 0:
        herox = 0
    elif herox + hero_width > 1366:
        herox = 1366 - hero_width

    if heroy < 0:
        heroy = 0
    elif heroy + hero_height > 700:
        heroy = 700 - hero_height

    if enemyx < 0:
        enemyx = 0
    elif enemyx + hero_width > 1366:
        enemyx = 1366 - hero_width

    if enemyy < 0:
        enemyy = 0
    elif enemyy + hero_height > 700:
        enemyy = 700 - hero_height

    for bullet_data in bullets:
        direction = bullet_data['direction']
        bullet_speed = bullet_data['speed']
        if direction == 'up':
            bullet_data['y'] -= bullet_speed
        elif direction == 'down':
            bullet_data['y'] += bullet_speed
        elif direction == 'left':
            bullet_data['x'] -= bullet_speed
        elif direction == 'right':
            bullet_data['x'] += bullet_speed
        bul(bullet_data['image'], bullet_data['x'], bullet_data['y'])

    for bullet_data in enemy_bullets:
        direction = bullet_data['direction']
        bullet_speed = bullet_data['speed']
        if direction == 'up':
            bullet_data['y'] -= bullet_speed
        elif direction == 'down':
            bullet_data['y'] += bullet_speed
        elif direction == 'left':
            bullet_data['x'] -= bullet_speed
        elif direction == 'right':
            bullet_data['x'] += bullet_speed
        ebul(bullet_data['image'], bullet_data['x'], bullet_data['y'])

    for brick in bricks:
        if check_collision(bullets, brick['x'], brick['y'], brick_img.get_width(), brick_img.get_height()):
            bricks.remove(brick)
            break
    for brick in bricks:
        if check_collision(enemy_bullets, brick['x'], brick['y'], brick_img.get_width(), brick_img.get_height()):
            bricks.remove(brick)
            break

    # Kiểm tra va chạm viên đạn với các viên gạch break brick
    update_brick_status(other_bullets, bricks)

    # Kiểm tra và cập nhật trạng thái viên gạch solid khi bị bắn
    update_solid_brick_status(other_bullets, solid_bricks)

    # Draw other tank
    draw_other_tank(other_tank_x, other_tank_y, other_tank_direction)

    # Draw other bullets
    draw_other_bullets(other_bullets)

    # Kiểm tra va chạm giữa hai tank
    check_tank_collision()

    # Kiểm tra va chạm viên đạn của other tank với player và enemy
    check_collision(other_bullets, herox, heroy, hero_width, hero_height)
    check_collision(other_bullets, enemyx, enemyy, hero_width, hero_height)
    check_collision(enemy_bullets, herox, heroy, hero_width, hero_height)
    check_collision(bullets, enemyx, enemyy, hero_width, hero_height)

    # Kiểm tra va chạm với các viên gạch solid cho các viên đạn của player và enemy
    check_bullet_solid_collision(bullets, solid_bricks)
    check_bullet_solid_collision(enemy_bullets, solid_bricks)

    hero(r_hero, herox, heroy)
    enemy(r_enemy, enemyx, enemyy)

    pygame.display.update()
