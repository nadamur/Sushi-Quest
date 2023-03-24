# Import
import pygame, random, time, sys
import GameObjects

# Creating the game objects 
pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('ninjagame')

x = 200
y = 200

scale = 13
img = pygame.image.load('sprites/ninja_hero_sprite.png')
img = pygame.transform.scale(img, (img.get_width() / scale, img.get_height()/scale))

rect = img.get_rect()
rect.center = (x, y)

# Game functions




# UI functions

run = True
# Game loop
while run:
    #event loop
    screen.blit(img, rect)
    #game logic
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()
    #render

pygame.quit()
