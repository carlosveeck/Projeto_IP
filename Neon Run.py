
import random
import pygame

import os

pygame.init()

# COLORS CODES

white = (255, 255, 255)
black = (0, 0, 0)

deep_blue = pygame.Color("#14195a")
light_blue = pygame.Color("#0dd3f3")

deep_purple = (120, 30, 155)

light_pink = pygame.Color("#f02e9b")

yellowish = pygame.Color("#ff9656")

reddish = pygame.Color("#cc1e3d")

WIDTH = 1050
HEIGHT = 600

# GAME VARIABLES

score = 0

player_x = 50
player_y = 380

static_y = 380

y_change = 0

gravity = 1

obstacles = [600, 900, 1200]
obstacle_speed = 5 

active = False

# DISPLAY STATS

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Neon Run")

background = deep_blue
fps = 60

font = pygame.font.Font("visby-round-cf-heavy.otf", 16)

timer = pygame.time.Clock()

running = True

# IMAGES

backgr_image = pygame.image.load(os.path.join("imgs", "backgr1.jpg"))
resized_backgr = pygame.transform.scale(backgr_image, (1100, 600))

logo = pygame.image.load(os.path.join("imgs", "logo_v2.png"))

player_skin = pygame.image.load(os.path.join("imgs", "boneco_base.png"))
resized_player = pygame.transform.scale(player_skin, (550, 300))

# GAME EVENTS

while running == True:

    # BACKGROUND SETTING

    timer.tick(fps)
    screen.blit(resized_backgr, (-40, 10))

    # WHILE STATIONARY

    if not active:

        instruction_text = font.render(f"Pressione espaço para começar", True, white)
        screen.blit(instruction_text, (380, 390))

        instruction_text2 = font.render(f"( Alfa | Build 1.0.0 )", True, white)
        screen.blit(instruction_text2, (430, 560))

        screen.blit(logo, (380, -40))

    score_text = font.render(f"Score: {score}", True, white)
    screen.blit(score_text, (480, 520))

    floor = pygame.draw.rect(screen, light_pink, [0, 470, WIDTH, 10])
    player = pygame.draw.rect(screen, light_blue, [player_x, player_y, 35, 90])

    obstacle0 = pygame.draw.rect(screen, reddish, [obstacles[0], 435, 35, 35])
    obstacle1 = pygame.draw.rect(screen, deep_purple, [obstacles[1], 445, 30, 25])
    obstacle2 = pygame.draw.rect(screen, yellowish, [obstacles[2], 425, 40, 45])

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False

        if event.type == pygame.KEYDOWN and not active:

            if event.key == pygame.K_SPACE:

                obstacles = [600, 800, 1200]

                player_x = 50
                score = 0

                active = True
                
        if event.type == pygame.KEYDOWN and active == True:

            if event.key == pygame.K_SPACE and y_change == 0:

                y_change = 18

    # SPAWNANDO OBSTÁCULOS POR RNG

    for i in range(len(obstacles)):

        if active == True:

            obstacles[i] -= obstacle_speed

            if obstacles[i] < -20:

                obstacles[i] = random.randint(1000, 1300)
                score += 1

            if player.colliderect(obstacle0) or player.colliderect(obstacle1) or player.colliderect(obstacle2):

                active = False 

    if y_change > 0 or player_y < static_y:

        player_y -= y_change
        y_change -= gravity

    if player_y > static_y:

        player_y = static_y

    if player_y == static_y and y_change < 0:

        y_change = 0

    pygame.display.flip()

pygame.quit()