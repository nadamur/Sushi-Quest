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
SCROLL_THRESH = 200
screen_scroll = 0
bg_scroll = 0

#loading the background
ninja_forest = pygame.image.load('assets/backgrounds/ninja_forest_background.png')
original_width, original_height = ninja_forest.get_size()
new_width = int(SCREEN_HEIGHT * (original_width / original_height))
ninja_forest = pygame.transform.scale(ninja_forest, (new_width, SCREEN_HEIGHT))

#making list for different blocks in the game
img_list = []
for x in range(TILE_TYPES):
    img = pygame.image.load(f'tile/{x}.png')
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)
    

#creating the player
class Ninja(pygame.sprite.Sprite):
    def __init__(self, char_type,x, y, scale,speed):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.flip = False
        self.frame_index = 0
        self.action = 0
        self.health = 100
        self.max_health = self.health
        self.jump_counter = 0
        self.update_time = pygame.time.get_ticks()
        self.idling = False
        self.idling_counter = 0

        img = pygame.image.load('Sprites/ninja_hero_sprite.png')
        health = pygame.image.load('Sprites/temp_healthbar.jpg')
        self.image = pygame.transform.scale(img, (img.get_width() / scale, img.get_height()/scale))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.dead()

    def dead(self):
        if self.health <=0:
            self.health = 0
            self.speed = 0
            self.alive = False

    
    def draw(self,screen):
        screen.blit(pygame.transform.flip(self.image,self.flip,False),self.rect)

    def ai(self):
            if self.alive and ninja.alive:
                if self.idling == False and random.randint(1,200) == 1:
                    self.idling = True

    def move(self, moving_left,moving_right):
        screen_scroll = 0
        dx = 0
        dy = 0

        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -.75
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 0.75

        #jumping
        if self.jump == True and self.jump_counter < 2:
            self.vel_y = -14
            self.jump = False
            self.jump_counter +=1

        #gravity
        self.vel_y += 0.75
        if self.vel_y>10:
            self.vel_y
        dy += self.vel_y

        #collision check
        for tile in world.obstacle_list:
            #check collision in x direction
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.rect.width, self.rect.height):
                dx = 0
            #check collision in y direction
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.rect.width, self.rect.height):
                #check if below the ground i.e. jumping
                if self.vel_y < 0:
                    dy = tile[1].bottom - self.rect.top
                    self.vel_y = 0
                #check if above the ground i.e. falling
                elif self.vel_y >= 0:
                    dy = tile[1].top - self.rect.bottom
                    self.vel_y = 0
                    self.jump_counter = 0

        #check if going off the edges of the screen
        if self.rect.left + dx < 0 or self.rect.right + dx > SCREEN_WIDTH:
            dx = 0

        #update rectangle position
        self.rect.x += dx
        self.rect.y += dy

        #update scroll based on player position
        if self.char_type == 'ninja':
            if (self.rect.right > SCREEN_WIDTH - SCROLL_THRESH and bg_scroll < (world.level_length * TILE_SIZE) - SCREEN_WIDTH)\
            or (self.rect.left < SCROLL_THRESH and bg_scroll > abs(dx)):
                self.rect.x -= dx
                screen_scroll = -dx

        return screen_scroll


#creating the world
class World():
    def __init__(self):
        self.obstacle_list = []

    def process_data(self, data):
        self.level_length = len(data[0])
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
                    elif tile == 15:  # create player
                        ninja = Ninja('ninja', x * TILE_SIZE, y * TILE_SIZE, 15, 7)
                    elif tile == 16: # create enemy
                        self.obstacle_list.append(tile_data)
                        enemy = Ninja('enemy', x * TILE_SIZE, y * TILE_SIZE, 15, 7)
                        enemy_ninja_group.add(enemy)
                    
        return ninja

    def draw(self):
        for tile in self.obstacle_list:
            tile[1][0] += screen_scroll
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
    width = ninja_forest.get_width()
    for x in range(5):
        screen.blit(ninja_forest, ((x * width) - bg_scroll * 0.5, 0))


enemy_ninja_group = pygame.sprite.Group()


# healthbar = GameObjects.HealthBar(20,20,ninja.health,ninja.health)
# star_group = pygame.sprite.Group()

# creating enemies
# enemy_ninjas_group = pygame.sprite.Group()
# enemy = GameObjects.EnemyNinja(600,578,13)
# enemy_ninjas_group.add(enemy_ninja1)


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
   
    # commenting out the enemy for now
    # healthbar.draw(ninja.health,screen)

    ninja.draw(screen)

    #draw enemies on screen
    for enemy in enemy_ninja_group:
        enemy.draw(screen)
        enemy.update()
        enemy.ai()


    if ninja.alive:
        screen_scroll = ninja.move(moving_left,moving_right)
        bg_scroll -= screen_scroll


    #star collision logic
    # star_collisions = pygame.sprite.groupcollide(star_group,ninja,True,False)
    # for star in star_collisions:
    #     star_hit()
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
