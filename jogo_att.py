
import pygame
import os
import random

pygame.init()
pygame.mixer.music.load('musicalucs.wav')
pygame.mixer.music.play(loops=-1, start=0.0)

# Variaveis/Constantes definidas:

clock = pygame.time.Clock()
FPS = 60

SCREEN_WIDTH = 1050
SCREEN_HEIGHT = 590

x = 50
y = 380
vel_y = 18

jump = False

High_score = 0

floor_position = 0

can_jump = False

# Cores

deep_blue = pygame.Color("#14195a")
light_blue = pygame.Color("#0dd3f3")
light_pink = pygame.Color("#f02e9b")
reddish = pygame.Color("#cc1e3d")
deep_purple = (120, 30, 155)
yellowish = pygame.Color("#ff9656")

white = (255, 255, 255)

# Opacidade 0%

transparent = (0,0,0,0)

# Hit-box do Player

transparent_rect = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)

active = False

font = pygame.font.Font("visby-round-cf-heavy.otf", 16)

points = 0

#Criando a janela do game
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen.fill(deep_blue)
pygame.display.set_caption("Neon Run")

#Carrega a imagem:

bg3 = pygame.image.load('imgs/backgr3_8bit.png').convert()
resized_bg3 = pygame.transform.scale(bg3, (1100, 600))

bg2 = pygame.image.load('imgs/backgr2.png').convert()
resized_bg2 = pygame.transform.scale(bg2, (1100, 600))

bg = pygame.image.load('imgs/backgr1.jpg').convert()
resized_bg = pygame.transform.scale(bg, (1100, 600))

floor_pic = pygame.image.load('imgs/floor1.png')
resized_floor = pygame.transform.scale(floor_pic, (1100, 600))

logo = pygame.image.load('imgs/logo_v2.png')

#Colisão:

collide = pygame.Rect.colliderect

class Player(pygame.sprite.Sprite):

    def __init__(self, x, y):

        # Variáveis para o pulo

        self.x = x
        self.y = y
        self.vel_y = 17
        self.jump = False

        # Codigo do sprite do player:

        super().__init__()

        self.sprites = []
        self.sprites.append(pygame.image.load('imgs/frames_fred/fred_frame_1.png'))
        self.sprites.append(pygame.image.load('imgs/frames_fred/fred_frame_2.png'))
        self.sprites.append(pygame.image.load('imgs/frames_fred/fred_frame_3.png'))

        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]

        self.width = self.image.get_rect().width
        self.height = self.image.get_rect().height

        self.image = pygame.transform.scale(self.image, (300, 300))

        self.rect = self.image.get_rect()

    def update(self):

        self.current_sprite += 0.15

        self.current_sprite = self.current_sprite % len(self.sprites)

        self.image = self.sprites[int(self.current_sprite)]

        self.image = pygame.transform.scale(self.image, (self.width*0.075, self.height*0.075))

    # Desenha o boneco na janela desejada
    
    def draw(self, win):

        # Hit_box do Player é um retângulo invisível

        self.player = pygame.draw.rect(transparent_rect, light_blue, [self.x + 40, self.y, 55, 90])

        # Posicao de Fred

        self.rect.topleft = [self.x,self.y - 18]     


    #fisica do pulo
    def player_jump(self, userInput):

        if userInput[pygame.K_SPACE] and self.jump is False:

            self.jump = True

        if self.jump:

            self.y -= self.vel_y

            self.vel_y -= 1

            if self.vel_y < -17:

                self.jump = False

                self.vel_y = 17

class Obstacle0:

    def __init__(self, x, y):

        self.obstacles = [900,1300,1700]

        self.x = x

        self.y = y

        self.vel_x = 8
    
    def draw_obstacle(self, win):

        self.obstacle0 = pygame.draw.rect(screen, reddish, [self.obstacles[0], 420, 40, 50])
        self.obstacle1 = pygame.draw.rect(screen, deep_purple, [self.obstacles[1], 440, 35, 30])
        self.obstacle2 = pygame.draw.rect(screen, yellowish, [self.obstacles[2], 420, 45, 50])

    def move_obstacle(self):
            
        for obstacle in range (len(self.obstacles)):

            self.obstacles[obstacle] -= self.vel_x

            if self.obstacles[obstacle] < -20:

                self.obstacles[obstacle] = random.randint(1000, 1300)

class Coin0(pygame.sprite.Sprite):

    def __init__(self, x, y, specified_coin):
            
        if specified_coin == "img_coin1":

            self.image = pygame.image.load("imgs/coin_base.png")

        if specified_coin == "img_coin2":

            self.image = pygame.image.load("imgs/coin_2.png")
        
        if specified_coin == "img_coin3":

            self.image = pygame.image.load("imgs/coin_3.png")

        self.image = pygame.transform.scale(self.image, (225, 225))

        self.x = x

        self.y = y

        self.vel_x = 4

    def draw_coin(self, win, color):

        screen.blit(self.image, (self.x -100, self.y - 100))

        self.coin0 = pygame.draw.circle(win, color, [self.x, self.y], 15)

    def move_coin(self):

        self.x -= self.vel_x

        if self.x < -20:

            self.x = random.randint(1000, 1300)
   
# Definindo coordenadas do personagem

obstacle = Obstacle0(600, 435)

coin_yellow = Coin0(1200, 250, "img_coin1")
coin_white = Coin0(1100,330, "img_coin2")
coin_deepblue = Coin0(1300, 425, "img_coin3")

moving_sprites = pygame.sprite.Group()
char = Player(x,y)
moving_sprites.add(char)

#Permite que a janela fique aberta:

run = True

while run:

    clock.tick(FPS)
    screen.fill(deep_blue)
    screen.blit(resized_bg3, (-40, 10))

    # chão
    screen.blit(resized_floor, (floor_position, 0))

    # chão duplicado para ser infinito
    screen.blit(resized_floor, (floor_position + 1100, 0))
 
    userInput = pygame.key.get_pressed()

    # Tela de start

    if not active:

        instruction_text = font.render(f"Pressione ENTER para começar", True, white)
        screen.blit(instruction_text, (380, 390))

        screen.blit(logo, (380, -40))

        if points > High_score:
            High_score = points
    
    High_score_text = font.render(f"Recorde atual: {High_score}", True, white)
    screen.blit(High_score_text, (0, 0))

    moving_sprites.draw(screen)
    moving_sprites.update()
    # Desenha personagem da tela:
    char.draw(screen)
    
    # Define o pulo do personagem
    char.player_jump(userInput)

    # Desenha obstáculo na tela
    obstacle.draw_obstacle(screen)

    # Define movimentação dos obstaculos
    if active:
        obstacle.move_obstacle()
    if char.player.colliderect(obstacle.obstacle0):
        active = False
    if char.player.colliderect(obstacle.obstacle1):
        active = False
    if char.player.colliderect(obstacle.obstacle2):
        active = False

    # Desenha coin na tela:

    coin_yellow.draw_coin(transparent_rect, (0,0,0,0))
    coin_white.draw_coin(transparent_rect, (0,0,0,0))
    coin_deepblue.draw_coin(transparent_rect, (0,0,0,0))

    # Define movimentação da coin:

    if active:
        coin_yellow.move_coin()
        coin_deepblue.move_coin()
        coin_white.move_coin()

        floor_position -= 8

        if floor_position < -1100:
            floor_position = 0

    if char.player.colliderect(coin_yellow.coin0):
        newx = random.randint(1300, 1500)
        coin_yellow = Coin0(newx, 250, "img_coin1")
        points += 100

    if char.player.colliderect(coin_white.coin0):
        newx = random.randint(1000, 1200)
        coin_white = Coin0(newx, 330, "img_coin2")
        points += 150

    if char.player.colliderect(coin_deepblue.coin0):
        newx = random.randint(1200, 1400)
        coin_deepblue = Coin0(newx, 425, "img_coin3")
        points += 200
    
    score_text = font.render(f"Score: {points}", True, pygame.Color("#FFFFFF"))
    screen.blit(score_text, (480, 520))


    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN and not active:

            if event.key == pygame.K_RETURN:
                obstacle = Obstacle0(600, 435)
                points = 0
                active = True

        if event.type == pygame.KEYDOWN and active:
            userInput = pygame.key.get_pressed()

    pygame.display.update()
pygame.quit() 