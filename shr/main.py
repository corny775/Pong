import pygame
import random
from pygame.locals import *
pygame.init()

screen_width = 750
screen_height = 600

fpsClock = pygame.time.Clock()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong')

#define font
font = pygame.font.SysFont('Cooper Black', 30)
#define game variables
margin = 50
cpu_score = 0
player_score = 0
fps = 60
live_ball = False
winner = 0
speed_increase = 0
#define colours
bg = (50, 25, 50)
white = (255, 255, 255)
black = (0, 0, 0)

galaxy = pygame.image.load("creeper2.png")
galaxy_rect = galaxy.get_rect(topleft = (0, 0))

chicken = pygame.image.load("chicken3.png")
chicken_rect = chicken.get_rect()

def draw_board():
	screen.fill(bg)
	screen.blit(galaxy, galaxy_rect)
	pygame.draw.line(screen, white, (0, margin), (screen_width, margin), 2)

def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))

class paddle():
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.rect = Rect(x, y, 20, 125)
		self.speed = 5
		self.ai_speed = 5
	def move(self):
		key = pygame.key.get_pressed()
		if key[pygame.K_UP] and self.rect.top > margin:
			self.rect.move_ip(0, -1 * self.speed)
		if key[pygame.K_DOWN] and self.rect.bottom < screen_height:
			self.rect.move_ip(0, self.speed)
	def draw(self):
		pygame.draw.rect(screen, white, self.rect)
	def ai(self):
		#ai to move the paddle automatically
		#move down
		if self.rect.centery < pong.rect.top and self.rect.bottom < screen_height:
			self.rect.move_ip(0, self.ai_speed)
		#move up
		if self.rect.centery > pong.rect.bottom and self.rect.top > margin:
			self.rect.move_ip(0, -1 * self.ai_speed)

class ball():
    def __init__(self, x, y):
        # Load the image of the ball
        self.images = [pygame.image.load("chicken2.png"), pygame.image.load("Bird1001.png"), pygame.image.load("explodingtnt2.jpg"),
                       pygame.image.load("jablinski2.png"), pygame.image.load("herobrine2.jpg"), pygame.image.load("mumbo2.jpg"),
                       pygame.image.load("football2.jpg")]
        self.images = [pygame.transform.scale(img, (30, 30)) for img in self.images] # Scale the image to fit the ball size
        self.image = random.choice(self.images)
        self.reset(x, y)

    def move(self):
        # Check collision with top margin
        if self.rect.top < margin:
            self.speed_y *= -1
        # Check collision with bottom of the screen
        if self.rect.bottom > screen_height:
            self.speed_y *= -1
        # Paddle collision
        if self.rect.colliderect(player_paddle) or self.rect.colliderect(cpu_paddle):
            self.speed_x *= -1
            # Randomly change image when ball touches paddle
            self.image = random.choice(self.images)
        # Check for out of bounds
        if self.rect.left < 0:
            self.winner = 1
        if self.rect.left > screen_width:
            self.winner = -1
        # Update ball position
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        return self.winner

    def draw(self):
        # Draw the ball image instead of a circle
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def reset(self, x, y):
        self.x = x
        self.y = y
        self.ball_rad = 8
        self.rect = Rect(x, y, self.ball_rad * 2, self.ball_rad * 2)
        self.speed_x = -4
        self.speed_y = 4
        self.winner = 0  # 1 is the player and -1 is the CPU

#create paddles
player_paddle = paddle(screen_width - 40, screen_height // 2)
cpu_paddle = paddle(20, screen_height // 2)
#create pong ball
pong = ball(screen_width - 60, screen_height // 2 + 50)
#create game loop
run = True
while run:
	fpsClock.tick(fps)
	draw_board()
	draw_text('CPU: ' + str(cpu_score), font, white, 20, 15)
	draw_text('P1: ' + str(player_score), font, white, screen_width - 100, 15)
	draw_text('BALL SPEED: ' + str(abs(pong.speed_x)), font, white, screen_width // 2 - 100 , 15)
	#draw paddles
	player_paddle.draw()
	cpu_paddle.draw()
	if live_ball == True:
		speed_increase += 1
		winner = pong.move()
		if winner == 0:
			#draw ball
			pong.draw()
			#move paddles
			player_paddle.move()
			cpu_paddle.ai()
		else:
			live_ball = False
			if winner == 1:
				player_score += 1
			elif winner == -1:
				cpu_score += 1
	#print player instructions
	if live_ball == False:
		if winner == 0:
			draw_text('CLICK ANYWHERE TO START', font, white, 150, screen_height // 2 + 125)
		if winner == 1:
			draw_text('YOU SCORED!', font, white, 275, screen_height // 2 -200)
			draw_text('CLICK ANYWHERE TO START', font, white, 150, screen_height // 2 +125)
		if winner == -1:
			draw_text('CPU SCORED!', font, white, 275, screen_height // 2 -200)
			draw_text('CLICK ANYWHERE TO START', font, white, 150, screen_height // 2 +125)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		if event.type == pygame.MOUSEBUTTONDOWN and live_ball == False:
			live_ball = True
			pong.reset(screen_width - 60, screen_height // 2 + 50)
	if speed_increase > 500:
		speed_increase = 0
		if pong.speed_x < 0:
			pong.speed_x -= 1
		if pong.speed_x > 0:
			pong.speed_x += 1
		if pong.speed_y < 0:
			pong.speed_y -= 1
		if pong.speed_y > 0:
			pong.speed_y += 1
	pygame.display.update()
pygame.quit()