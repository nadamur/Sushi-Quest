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
ninja = pygame.image.load('groupproject-team-8/Sprites/ninja_hero_sprite.png')
ninja = pygame.transform.scale(ninja, (ninja.get_width() / scale, ninja.get_height()/scale))

rect = ninja.get_rect()
rect.center = (x, y)

# Game functions




# UI functions

run = True
# Game loop
while run:
    #event loop
    screen.blit(ninja, rect)
    #game logic
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    

    pygame.display.update()
    #render

pygame.quit()
