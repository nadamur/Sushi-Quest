# Import
import pygame, random, time, sys
import GameObjects
import csv
import os

# Creating the game objects 
pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

#defining level (starting with level 1 for testing)
level = 1
rows1 = 16
TILE_TYPES = 21
TILE_SIZE = SCREEN_HEIGHT // rows1
cols1 = 150

#making list for different blocks in the game
img_list = []
for x in range(TILE_TYPES):
    img = pygame.image.load(f'tile/{x}.png')
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)


class World():
	def __init__(self):
		self.obstacle_list = []

	def process_data(self, data):
		#iterate through each value in level data file
		for y, row in enumerate(data):
			for x, tile in enumerate(row):
				if tile >= 0:
					img = img_list[tile]
					img_rect = img.get_rect()
					img_rect.x = x * TILE_SIZE
					img_rect.y = y * TILE_SIZE
					tile_data = (img, img_rect)
					if tile >= 0 and tile <= 8:
						self.obstacle_list.append(tile_data)
					elif tile == 15:#create player
						ninja = GameObjects.Ninja('ninja', x * TILE_SIZE, y * TILE_SIZE,13, 7)
						
		return ninja
            
	def draw(self):
		for tile in self.obstacle_list:
			screen.blit(tile[0], tile[1])
    


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption('ninjagame')
clock = pygame.time.Clock()
FPS = 60
moving_left = False
moving_right = False
BG = (144,201,100)
red = (255,0,0)


def draw_bg():
    screen.fill(BG)
    pygame.draw.line(screen,red,(0,600),(SCREEN_WIDTH,600))

ninja = GameObjects.Ninja('ninja',200,200,13,7)
healthbar = GameObjects.HealthBar(20,20,ninja.health,ninja.health)
star_group = pygame.sprite.Group()

# Game functions
def star_hit(self):
    if ninja.alive:
        ninja.health -= 5
        self.kill()



# UI functions

#create empty tile list
world_data = []
for row in range(rows1):
    r = [-1] * cols1
    world_data.append(r)

#load in level data and create world
with open(f'level{level}_data.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            world_data[x][y] = int(tile)
world = World()
ninja = world.process_data(world_data)            


run = True
# Game loop
while run:
    #event loop
    clock.tick(FPS)
    draw_bg()
    world.draw()
    healthbar.draw(ninja.health,screen)
    ninja.draw(screen)
    if ninja.alive:
        ninja.move(moving_left,moving_right)
    #star collision logic
    star_collisions = pygame.sprite.groupcollide(star_group,ninja,True,False)
    for star in star_collisions:
        star_hit()
    #game logic
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        #keyboard press
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                moving_left = True
            if event.key == pygame.K_RIGHT:
                moving_right= True
            if event.key == pygame.K_UP and ninja.alive:
                ninja.jump = True
        #keyboard release
        if event.type == pygame.KEYUP:
           if event.key == pygame.K_LEFT:
               moving_left = False
           if event.key == pygame.K_RIGHT:
               moving_right= False       
    

    pygame.display.update()
    #render

pygame.quit()
