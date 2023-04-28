
import pygame
import os
import random

pygame.init()

#Variaveis/Constantes definidas:

clock = pygame.time.Clock()
FPS = 60

SCREEN_WIDTH = 1050
SCREEN_HEIGHT = 590

x = 50
y = 380
vel_y = 18

jump = False

deep_blue = pygame.Color("#14195a")
light_blue = pygame.Color("#0dd3f3")
light_pink = pygame.Color("#f02e9b")
reddish = pygame.Color("#cc1e3d")

active = False

font = pygame.font.Font("visby-round-cf-heavy.otf", 16)

points = 0

#Criando a janela do game
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen.fill(deep_blue)
pygame.display.set_caption("Neon Run")

#Carrega a imagem:

bg2 = pygame.image.load('imgs/backgr2.png').convert()
resized_bg2 = pygame.transform.scale(bg2, (1100, 600))

bg = pygame.image.load('imgs/backgr1.jpg').convert()
resized_bg = pygame.transform.scale(bg, (1100, 600))

#colisão:
collide = pygame.Rect.colliderect

class Player:
    def __init__(self, x, y):
        #variáveis para o pulo
        self.x = x
        self.y = y
        self.vel_y = 18
        self.jump = False
        
    #Desenha o boneco na janela desejada
    def draw(self, win):
        self.player = pygame.draw.rect(win, light_blue, [self.x, self.y, 35, 90])

    #fisica do pulo
    def player_jump(self, userInput):
        if userInput[pygame.K_SPACE] and self.jump is False:
            self.jump = True
        if self.jump:
            self.y -= self.vel_y
            self.vel_y -= 1
            if self.vel_y < -18:
                self.jump = False
                self.vel_y = 18

class Obstacle0:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel_x = 5
    
    def draw_obstacle(self, win):
        self.obstacle0 = pygame.draw.rect(win, reddish, [self.x, self.y, 35, 35])
    
    def move_obstacle(self):
            self.x -= self.vel_x
            if self.x < -20:
                self.x = random.randint(1000, 1300)

class Coin0:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel_x = 5

    def draw_coin(self, win, color):
        self.coin0 = pygame.draw.circle(win, color, [self.x, self.y], 15)

    def move_coin(self):
        self.x -= self.vel_x
        if self.x < -20:
            self.x = random.randint(1000, 1300)

                
#definindo coordenadas do personagem
char = Player(x, y)
obstacle = Obstacle0(600, 435)

coin_yellow = Coin0(650, 300)
coin_white = Coin0(600,250)
coin_deepblue = Coin0(600,350)


#Permite que a janela fique aberta:
run = True
while run:

    clock.tick(FPS)
    screen.fill(deep_blue)
    screen.blit(resized_bg2, (-40, 10))

 
    userInput = pygame.key.get_pressed()
    floor2 = pygame.draw.rect(screen, light_pink, [0, 470, SCREEN_WIDTH, 10])
    floor = pygame.draw.rect(screen, deep_blue, [0, 480, SCREEN_WIDTH, 200])

    #Tela de start
    if not active:
        instruction_text = font.render(f"Pressione espaço para começar", True, pygame.Color("#FFFFFF"))
        screen.blit(instruction_text, (380, 390))
    
    #desenha personagem da tela:
    char.draw(screen)
    
    #define o pulo do personagem
    char.player_jump(userInput)

    #desenha obstáculo na tela
    obstacle.draw_obstacle(screen)

    #define movimentação dos obstaculos
    if active:
        obstacle.move_obstacle()
    if char.player.colliderect(obstacle.obstacle0):
        active = False

    #desenha coin na tela:
    coin_yellow.draw_coin(screen, pygame.Color("#FFFF00"))
    coin_white.draw_coin(screen, pygame.Color("#FFFFFF"))
    coin_deepblue.draw_coin(screen, pygame.Color("#14195a"))

    #define movimentação da coin:
    if active:
        coin_yellow.move_coin()
        coin_deepblue.move_coin()
        coin_white.move_coin()
    if char.player.colliderect(coin_yellow.coin0):
        newx = random.randint(1000, 1300)
        coin_yellow = Coin0(newx, 300)
        points += 100
    if char.player.colliderect(coin_white.coin0):
        newx = random.randint(900, 1100)
        coin_white = Coin0(newx, 250)
        points += 150
    if char.player.colliderect(coin_deepblue.coin0):
        newx = random.randint(800, 1200)
        coin_deepblue = Coin0(newx, 350)
        points += 200
    
    score_text = font.render(f"Score: {points}", True, pygame.Color("#FFFFFF"))
    screen.blit(score_text, (480, 520))


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN and not active:
            if event.key == pygame.K_SPACE:
                obstacle = Obstacle0(600, 435)
                points = 0
                active = True


        if event.type == pygame.KEYDOWN and active:
            userInput = pygame.key.get_pressed()



    pygame.display.update()
pygame.quit() 