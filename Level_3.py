#import libraries
import pygame
import random
import os

with open("Level_2.py") as f:
    exec(f.read())

#initialise pygame
pygame.init()

#game window dimensions
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
#create game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Level 3')

#set frame rate
clock = pygame.time.Clock()
FPS = 60

#game variables
SCROLL_THRESH = 200
GRAVITY = 0.3
MAX_PLATFORMS = 50
scroll = 0
bg_scroll = 0
game_over = False
score3 = score2
fade_counter = 0
fontScore = pygame.font.SysFont('Condolas',35)
score_increment = 0.05
moving_left = False
moving_right = False


#define colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PANEL = (153, 217, 234)

#define font
font_big = pygame.font.SysFont('Comic Sans', 24)

#load images
ninja_image = pygame.image.load(f'Assets/Ninja/ninja_hero_sprite_{selected_color}.png').convert_alpha()
bg_image = pygame.image.load('Assets/Backgrounds/jungle_forest_background.jpg').convert_alpha()
platform_image = pygame.image.load('Assets/Sprites/wood.png').convert_alpha()



#function for outputting text onto the screen
def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))

# #function for drawing info panel
# def draw_panel():
# 	pygame.draw.rect(screen, PANEL, (0, 0, SCREEN_WIDTH, 30))
# 	pygame.draw.line(screen, WHITE, (0, 30), (SCREEN_WIDTH, 30), 2)
# 	draw_text('SCORE: ' + str(score), font_small, WHITE, 0, 0)


#function for drawing the background
def draw_bg(bg_scroll):
	screen.blit(bg_image, (0, 0 + bg_scroll))
	screen.blit(bg_image, (0, -100 + bg_scroll))
	
#player class
class Ninja():
	def __init__(self, x, y):
		self.image = pygame.transform.scale(ninja_image, (ninja_image.get_width() / 18, ninja_image.get_height()/18))
		self.width = 25
		self.height = 40
		self.rect = pygame.Rect(0, 0, self.width, self.height-10)
		self.rect.center = (x, y)
		self.vel_y = 0
		self.flip = False
		self.jump = False
		self.jump_counter = 0

	def move(self, moving_left, moving_right):
		#reset variables
		scroll = 0
		dx = 0
		dy = 0
		if moving_left:
			dx = -5
			self.flip = True
		if moving_right:
			dx = 5
			self.flip = False

		if self.jump == True and self.jump_counter < 2:
			self.vel_y = -15
			self.jump_counter +=1
			self.jump = False

			



		# for event in pygame.event.get():
		# 	#keyboard press
		# 	if event.type == pygame.KEYDOWN:
		# 		if event.key == pygame.K_UP:
		# 			print(str(self.jump_counter))
		# 			if self.jump_counter < 2:
		# 				self.vel_y = -20
		# 				self.jump_counter +=1
						
		# #process keypresses
		# key = pygame.key.get_pressed()
		# if key[pygame.K_LEFT]:
		# 	dx = -8
		# 	self.flip = True
		# if key[pygame.K_RIGHT]:
		# 	dx = 8
		# 	self.flip = False
			

		#gravity
		self.vel_y += GRAVITY
		dy += self.vel_y

		#ensure player doesn't go off the edge of the screen
		if self.rect.left + dx < 0:
			dx = -self.rect.left
		if self.rect.right + dx > SCREEN_WIDTH:
			dx = SCREEN_WIDTH - self.rect.right


		#check collision with platforms
		for platform in platform_group:
			#collision in the y direction
			if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
				#check if above the platform
				if self.rect.bottom < platform.rect.centery:
					if self.vel_y > 0:
						self.rect.bottom = platform.rect.top
						dy = 0
						self.vel_y = 0
						self.jump_counter = 0
						
        #check if the player has bounced to the top or bottom of the screen
		if self.rect.top <= SCROLL_THRESH:
			#if player is jumping
			if self.vel_y < 0:
				scroll = -dy


		self.rect.x += dx
		self.rect.y += dy + scroll

		#update mask
		self.mask = pygame.mask.from_surface(self.image)

		return scroll

	def draw(self):
		screen.blit(pygame.transform.flip(self.image, self.flip, False), (self.rect.x - 12, self.rect.y - 5))




#platform class
class Platform(pygame.sprite.Sprite):
	def __init__(self, x, y, width, moving):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.transform.scale(platform_image, (width, 10))
		self.moving = moving
		self.move_counter = random.randint(0, 50)
		self.direction = random.choice([-1, 1])
		self.speed = random.randint(1, 2)
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

	def update(self, scroll):
		#moving platform side to side if it is a moving platform
		if self.moving == True:
			self.move_counter += 1
			self.rect.x += self.direction * self.speed

		#change platform direction if it has moved fully or hit a wall
		if self.move_counter >= 100 or self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
			self.direction *= -1
			self.move_counter = 0

		#update platform's vertical position
		self.rect.y += scroll

		#check if platform has gone off the screen
		if self.rect.top > SCREEN_HEIGHT:
			self.kill()

		


#player instance
ninja = Ninja(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150)

#create sprite groups
platform_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()

# Create starting platform
platform = Platform(0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, False)
platform_group.add(platform)

last_platform_y = platform.rect.y

for p in range(MAX_PLATFORMS-1):
    p_w = random.randint(50, 60)
    p_x = random.randint(0, SCREEN_WIDTH - p_w)
    p_y = last_platform_y - random.randint(80, 120)
    p_type = random.choices([1, 2], weights=[0.2, 0.8])[0] # Randomly choose between 1 and 2 with 20% and 80% probability respectively
    p_moving = False
    if p_type == 1:
        p_moving = True
    platform = Platform(p_x, p_y, p_w, p_moving)
    platform_group.add(platform)
    last_platform_y = platform.rect.y

# Generate last platform
last_platform_w = SCREEN_WIDTH
last_platform_x = 0
last_platform_y -= random.randint(80, 120)
last_platform = Platform(0, last_platform_y, SCREEN_WIDTH, False)
platform_group.add(last_platform)

def display_win_screen(screen, award_image, score, WIN_WIDTH=600, WIN_HEIGHT=600):
    # Load the image
    start_background = pygame.image.load("Assets/Backgrounds/start_background.png")

    # Render the "You Win!" text
    win_font = pygame.font.Font(None, 48)
    win_text = win_font.render("You win the ultimate sushi!", True, (255, 255, 255))
    win_text_rect = win_text.get_rect(center=(300, 300 - 200))

    # Load the award image and position it
    award = pygame.image.load(award_image)
    award_rect = award.get_rect(center=(300, 320))

    # Render the new skill text
    skill_font = pygame.font.Font(None, 40)
    skill_text = skill_font.render(f"Your final score is: {score}", True, (0, 0, 0))
    skill_text_rect = skill_text.get_rect(center=(300, 300 + 110))

    # Draw everything on the screen
    screen.blit(start_background, (-100, -50))
    screen.blit(win_text, win_text_rect)
    screen.blit(award, award_rect)
    screen.blit(skill_text, skill_text_rect)

    # Update the display and wait
    pygame.display.update()
    pygame.time.delay(5000)





#game loop
run = True
while run:

	clock.tick(FPS)
	

	if game_over == False:
		scroll = ninja.move(moving_left,moving_right)

		draw_bg(bg_scroll)

		#generate platforms
		
		#update platforms
		platform_group.update(scroll)

		#draw sprites
		platform_group.draw(screen)
		enemy_group.draw(screen)
		ninja.draw()
		
		

		#check if ninja has past the last platform
		if ninja.rect.bottom < platform_group.sprites()[-1].rect.top:
			# game_over = True
			display_win_screen(screen,"Assets/Sushi/sushi.png",s)

		if ninja.rect.top > SCREEN_HEIGHT:
			game_over = True

	else:
		if fade_counter < SCREEN_WIDTH:
			fade_counter += 5
			for y in range(0, 6, 2):
				pygame.draw.rect(screen, BLACK, (0, y * 100, fade_counter, 100))
				pygame.draw.rect(screen, BLACK, (SCREEN_WIDTH - fade_counter, (y + 1) * 100, SCREEN_WIDTH, 100))
		else:
			draw_text('Game Over!', font_big, WHITE, 220, 200)
			draw_text('Press space to try again', font_big, WHITE, 150, 300)
			#update high score
			key = pygame.key.get_pressed()
			if key[pygame.K_SPACE]:
				#reset variables
				game_over = False
				scroll = 0
				score3 = score2
				fade_counter = 0
				#reposition ninja
				ninja.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150)
				#reset platforms
				platform_group.empty()
				#create starting platform
				platform = Platform(0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, False)
				platform_group.add(platform)
				for p in range(MAX_PLATFORMS):
					p_w = random.randint(50, 60)
					p_x = random.randint(0, SCREEN_WIDTH - p_w)
					p_y = platform.rect.y - random.randint(80, 120)
					p_type = random.choices([1, 2], weights=[0.2, 0.8])[0] # Randomly choose between 1 and 2 with 20% and 80% probability respectively
					p_moving = False
					if p_type == 1:
						p_moving = True
					platform = Platform(p_x, p_y, p_w, p_moving)
					platform_group.add(platform)
	ninja.move(moving_left,moving_right)

	#event handler
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			# #update high score
			# if score > high_score:
			# 	high_score = score
			# 	with open('score.txt', 'w') as file:
			# 		file.write(str(high_score))
			run = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				moving_left = True
			if event.key == pygame.K_RIGHT:
				moving_right = True
			if event.key == pygame.K_UP:
				ninja.jump = True
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT:
				moving_left = False
			if event.key == pygame.K_RIGHT:
				moving_right = False
	score3 += score_increment
	sc = round(score3)
	s = str(sc)
	screen.blit(fontScore.render("Score: " + s,True,(255,0,0)),(10,10))


	#update display window
	pygame.display.update()



pygame.quit()