import pygame
from pygame.locals import *
pygame.init()
screen_width = 750
screen_height = 600
fpsClock = pygame.time.Clock()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong')

#define font
font = pygame.font.SysFont('Cooper Black', 30)

#define game variable
margin = 50
cpu_score = 0
player_score = 0
fps = 60
winner = 0
#define colours
bg = (50, 25, 50)
white = (255, 255, 255)
black = (0, 0, 0)

galaxy = pygame.image.load("creeper2.png")
galaxy_rect = galaxy.get_rect(topleft = (0, 0))

def draw_board():
    screen.fill(bg)
    screen.blit(galaxy, galaxy_rect)
    pygame.draw.line(screen, black, (0, margin), (screen_width, margin))
    pygame.draw.line(screen, black, (0, margin+1), (screen_width, margin+1))

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

class paddle():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = Rect(self.x, self.y, 20, 125)
        self.speed = 5
    def move(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_UP] and self.rect.top > (margin+1):
            self.rect.move_ip(0, -1*self.speed)
        if key[pygame.K_DOWN] and self.rect.bottom < screen_height:
            self.rect.move_ip(0, self.speed)
    def draw(self):
        pygame.draw.rect(screen, black, self.rect)

class ball(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.speed_x = -4
        self.speed_y = 4
        self.winner = 0 # 1 means p1 has scored, -1 means cpu scored
        self.images = []
        self.index = 0
        self.counter = 0
        self.image = pygame.image.load('chicken3.png')
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        #add collision detection
        #check collision with top margin
        if self.rect.top < (margin+1):
            self.speed_y *= -1
         #check collision with bottom margin
        if self.rect.bottom > screen_height:
            self.speed_y *= -1
        #check for out of bounds
        if self.rect.left < 0:
            return 1
        if self.rect.left > screen_width:
            return -1
        #update ball position
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        
    
        

#create paddles
player_paddle = paddle(screen_width-50, (screen_height//2)-30)
cpu_paddle = paddle(40, (screen_height//2)-30)
#create pong ball

ball_group = pygame.sprite.Group()
pong = ball(screen_width-100, (screen_height//2)-20)
ball_group.add(pong)
run = True
while run:
    fpsClock.tick(fps)
    draw_board()
    draw_text('CPU: ' + str(cpu_score), font, black, 25, 10)
    draw_text('P1: ' + str(player_score), font, black, screen_width - 85, 10)
    
    #draw paddles
    player_paddle.draw()
    cpu_paddle.draw()

    #move paddle
    player_paddle.move()
    
    ball_group.draw(screen)
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    
    #move ball
    print(winner)
    winner = ball_group.update()
    
    pygame.display.update()

pygame.quit()