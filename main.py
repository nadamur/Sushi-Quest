# Import
import pygame, random, time, sys
import GameObjects

# Creating the game objects 
pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

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
star_group = pygame.sprite.Group()

# Game functions
def star_hit(self):
    if ninja.alive:
        ninja.health -= 5
        self.kill()



# UI functions

run = True
# Game loop
while run:
    #event loop
    clock.tick(FPS)
    draw_bg()
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
