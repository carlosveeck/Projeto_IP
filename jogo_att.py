import pygame, random


# iniciar o pygame
pygame.init()

# iniciar a música do jogo em um loop infinito:
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

game_speed = 9
speed_increase = 0

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

# superfície transparente
transparent_rect = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)


# estado inicial do jogo
active = False

font = pygame.font.Font("visby-round-cf-heavy.otf", 16)

# pontuação inicial
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
        self.player = pygame.draw.rect(transparent_rect, light_blue, [self.x + 58, self.y + 10, 20, 70])

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

        self.vel_x = game_speed

        self.image1 = pygame.image.load("imgs\obstacle1.png")
        self.image2 = pygame.image.load("imgs\obstacle2.png")
        self.image3 = pygame.image.load("imgs\obstacle3.png")


    def draw_obstacle(self, win):

        self.obstacle0 = pygame.draw.rect(screen, reddish, [self.obstacles[0], 420, 40, 50])
        self.image1 = pygame.transform.scale(self.image1, (150, 80))
        screen.blit(self.image1, (self.obstacles[0] - 55 , self.y - 45))

        self.obstacle1 = pygame.draw.rect(screen, deep_purple, [self.obstacles[1], 440, 35, 30])
        self.image2 = pygame.transform.scale(self.image2, (100, 60))
        screen.blit(self.image2, (self.obstacles[1] - 33, self.y - 25))

        self.obstacle2 = pygame.draw.rect(screen, yellowish, [self.obstacles[2], 420, 45, 50])
        self.image3 = pygame.transform.scale(self.image3, (150, 105))
        screen.blit(self.image3, (self.obstacles[2] - 52, self.y - 70))


    def move_obstacle(self):

        for obstacle in range (len(self.obstacles)):

            self.obstacles[obstacle] -= self.vel_x

            if self.obstacles[obstacle] < -20:

                random_number = random.randint(1000 + (game_speed*(2**(game_speed-9))), 1300 + (game_speed*(2**(game_speed-9))))

                while ((abs(random_number - self.obstacles[obstacle - 1]) > 140 and abs(random_number - self.obstacles[obstacle - 1]) < 300 or abs(random_number - self.obstacles[obstacle - 1]) < 110) or
                       (abs(random_number - self.obstacles[obstacle - 2]) > 140 and abs(random_number - self.obstacles[obstacle - 2]) < 300 or abs(random_number - self.obstacles[obstacle - 2]) < 110)):

                    random_number = random.randint(1000 + (game_speed*(2**(game_speed-9))), 1300 + (game_speed*(2**(game_speed-9))))

                self.obstacles[obstacle] = abs(random_number)



class Coin0(pygame.sprite.Sprite):

    def __init__(self, x, y, specified_coin):

        if specified_coin == "img_coin1":

            self.image = pygame.image.load("imgs/def2_coin1.png")

        if specified_coin == "img_coin2":

            self.image = pygame.image.load("imgs/def2_coin2.png")

        if specified_coin == "img_coin3":

            self.image = pygame.image.load("imgs/def2_coin3.png")

        self.image = pygame.transform.scale(self.image, (275, 275))

        self.x = x

        self.y = y

        self.vel_x = 4


    def draw_coin(self, win, color):

        screen.blit(self.image, (self.x -150, self.y - 150))

        self.coin0 = pygame.draw.circle(win, color, [self.x - 12, self.y - 12], 30)


    def move_coin(self):

        self.x -= self.vel_x

        if self.x < -20:

            self.x = random.randint(1000, 1300)



# Criando todos os objetos:

# obstáculos
obstacle = Obstacle0(600, 435)

# moedas
coin_yellow = Coin0(1200, 270, "img_coin1")
coin_white = Coin0(1100,360, "img_coin2")
coin_deepblue = Coin0(1300, 420, "img_coin3")

# player
moving_sprites = pygame.sprite.Group()
char = Player(x,y)
moving_sprites.add(char)



# funções úteis:
def menu():

    instruction_text = font.render(f"Pressione ENTER para começar", True, white)
    screen.blit(instruction_text, (380, 390))

    screen.blit(logo, (380, -40))



def update_high_score(points, High_score):

    if points > High_score:
        High_score = points

    return High_score



def draw_interactive_objects():

    # Desenha coin na tela:
    coin_yellow.draw_coin(transparent_rect, (0,0,0,0))
    coin_white.draw_coin(transparent_rect, (0,0,0,0))
    coin_deepblue.draw_coin(transparent_rect, (0,0,0,0))

    # Desenha obstáculo na tela
    obstacle.draw_obstacle(screen)



def obstacle_colision(active):

    # colicao com obstáculos:
    if (char.player.colliderect(obstacle.obstacle0) or
        char.player.colliderect(obstacle.obstacle1) or
        char.player.colliderect(obstacle.obstacle2)):
        active = False

    return active



def move_interactive_objects(active):
    if active:

        obstacle.move_obstacle()

        coin_yellow.move_coin()
        coin_deepblue.move_coin()
        coin_white.move_coin()



def move_floor(active, floor_position):

    if active:
        floor_position -= game_speed

        if floor_position < -1100:
            floor_position = 0

    return floor_position



#Permite que a janela fique aberta:
run = True

# laço principal do programa
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
        menu()
        High_score = update_high_score(points, High_score)


    # texto do recorde atual
    High_score_text = font.render(f"Recorde atual: {High_score}", True, white)
    screen.blit(High_score_text, (0, 0))


    # desenha o player:
    moving_sprites.draw(screen)
    moving_sprites.update()
    char.draw(screen)

    # Define o pulo do personagem
    if active:
        char.player_jump(userInput)


    # desenha os obstaculos e as coins:
    draw_interactive_objects()


    # Define movimentação dos obstaculos, das coins e do chão
    move_interactive_objects(active)
    floor_position = move_floor(active, floor_position)


    # detecta colisão com obstaculos
    active = obstacle_colision(active)


    # colisões com as coins:
    if char.player.colliderect(coin_yellow.coin0):
        newx = random.randint(1300, 1500)
        coin_yellow = Coin0(newx, 250, "img_coin1")
        points += 1000
        speed_increase += 100

    if char.player.colliderect(coin_white.coin0):
        newx = random.randint(1000, 1200)
        coin_white = Coin0(newx, 330, "img_coin2")
        points += 500
        speed_increase += 500

    if char.player.colliderect(coin_deepblue.coin0):
        newx = random.randint(1200, 1400)
        coin_deepblue = Coin0(newx, 425, "img_coin3")
        points += 100
        speed_increase += 1000


    score_text = font.render(f"Score: {points}", True, pygame.Color("#FFFFFF"))
    screen.blit(score_text, (480, 520))


    # dificultar o jogo de acordo com a pontuação atual do player
    if speed_increase >= 3200:
        speed_increase -= 3200
        game_speed += 1
        obstacle.vel_x += 1


    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN and not active:

            if event.key == pygame.K_RETURN:

                # reiniciar todas as informações ao iniciar um novo jogo
                obstacle = Obstacle0(600, 435)
                points = 0
                game_speed = 10
                obstacle.vel_x = 10
                speed_increase = 0
                active = True


        if event.type == pygame.KEYDOWN and active:
            userInput = pygame.key.get_pressed()


    pygame.display.update()

# finalizar.
pygame.quit()