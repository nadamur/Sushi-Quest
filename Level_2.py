# Import
import pygame, random, time, sys
import GameObjects
import csv
import os
import threading

# Creating the game objects 
pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

#defining level (starting with level 1 for testing)
level = 2
rows1 = 16
TILE_TYPES = 21
TILE_SIZE = SCREEN_HEIGHT // rows1
cols1 = 20
SCROLL_THRESH = 200
screen_scroll = 0
bg_scroll = 0

#loading the background
viking_sea = pygame.image.load('assets/backgrounds/viking_sea_background.jpg')
original_width, original_height = viking_sea.get_size()
new_width = int(SCREEN_HEIGHT * (original_width / original_height))
ninja_forest = pygame.transform.scale(viking_sea, (new_width, SCREEN_HEIGHT))

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
        self.scale = scale
        self.flip = False
        self.frame_index = 0
        self.action = 0
        self.health = 100
        self.punching = False
        self.max_health = self.health
        self.jump_counter = 0
        self.update_time = pygame.time.get_ticks()
        self.idling = False
        self.idling_counter = 0
        self.vision = pygame.Rect(0,0,150,640)
        self.punch_cooldown = 0
        self.animation_list = []
        img = pygame.image.load('Sprites/ninja_hero.png')
        img = pygame.transform.scale(img, (img.get_width() / scale, img.get_height()/scale))
        self.animation_list.append(img)
        img = pygame.image.load('Sprites/dead_hero.png')
        img = pygame.transform.scale(img, (img.get_width() / self.scale, img.get_height()/self.scale))
        self.animation_list.append(img)
        self.image = self.animation_list[self.action]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.update_animation()
        self.dead()
        # self.update_animation()
        if self.punch_cooldown > 0:
            self.punch_cooldown -=1

    def punch(self):
        print("punch")
        if self.punch_cooldown == 0:
            self.punch_cooldown = 2
            punch = Punch(self.rect.centerx + (0.6*self.rect.size[0]*self.direction),self.rect.centery,self.direction)
            punch_group.add(punch)

    def dead(self):
        if self.health <=0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(1)

    def update_animation(self):
        self.image = self.animation_list[self.action]
        
    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
    
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

        return screen_scroll
    
    def ai(self,ninja):
        if self.alive and ninja.alive:
            if self.idling == False and random.randint(1,200) == 1:
                self.idling = True
                self.idling_counter = 50
            # if self.vision.colliderect(ninja.rect):
            #     self.throw_star(sprite_group)

class Punch(pygame.sprite.Sprite):
    def __init__(self,x,y,direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 7
        self.direction = direction
        self.vel_y = 0
        self.jump = False
        self.scale = 15
        self.flip = False
        img = pygame.image.load('Sprites/hero_punch.png')
        img = pygame.transform.scale(img, (img.get_width() / 15, img.get_height()/15))
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

    def draw(self):
        screen.blit(pygame.transform.flip(self.image,self.flip,False),self.rect)
    def update(self):
        for enemy in enemy_ninja_group:
            if pygame.sprite.spritecollide(enemy, punch_group,False):
                if enemy.alive:
                    enemy.health -= 1
                    self.kill()

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

        

class Viking(pygame.sprite.Sprite):
    def __init__(self, x, y, scale,speed):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.vision = pygame.Rect(0,0,150,640)
        self.speed = speed
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.flip = False
        self.frame_index = 0
        self.scale = scale
        self.action = 0
        self.health = 1
        self.max_health = self.health
        self.jump_counter = 0
        self.update_time = pygame.time.get_ticks()
        self.idling = False
        self.idling_counter = 0
        self.animation_list = []
        img = pygame.image.load('Sprites/viking_test.png')
        img = pygame.transform.scale(img, (img.get_width() / scale, img.get_height()/scale))
        self.animation_list.append(img)
        img = pygame.image.load('Sprites/dead_viking.png')
        img = pygame.transform.scale(img, (img.get_width() / self.scale, img.get_height()/self.scale))
        self.animation_list.append(img)
        self.image = self.animation_list[self.action]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def dead(self):
        if self.health <=0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(1)

    def update_animation(self):
        self.image = self.animation_list[self.action]
        
    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action

    def update(self):
        self.dead()

    def move_towards_ninja(self,ninja):
        # Find direction vector (dx, dy) between enemy and player.
        dx = ninja.rect.x - self.rect.x
        if(dx <0):
            self.flip = False
        else:
            self.flip = True
        dirvect = pygame.math.Vector2(ninja.rect.x - self.rect.x, ninja.rect.y - self.rect.y)
        dirvect.normalize()
        # Move along this normalized vector towards the player at current speed.
        dirvect.scale_to_length(self.speed)
        self.rect.move_ip(dirvect)

    def dead(self):
        if self.health <=0:
            self.health = 0
            self.speed = 0
            self.alive = False
    
    def draw(self,screen):
        screen.blit(pygame.transform.flip(self.image,self.flip,False),self.rect)

    def move(self):
        #screen_scroll = 0
        dx = 0
        dy = 0

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

        return screen_scroll
    
    def ai(self,ninja):
        if self.alive and ninja.alive:
            if self.idling == False and random.randint(1,200) == 1:
                self.idling = True
                self.idling_counter = 50
            # if self.vision.colliderect(ninja.rect):
            # #     self.throw_star(sprite_group)
            # else:
            #     if self.idling == False:
            #         if self.direction ==1:
            self.move()


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
                        healthbar = GameObjects.HealthBar(20,20,ninja.health,ninja.health)
                    elif tile == 16: # create enemy
                        enemy = Viking(x * TILE_SIZE, y * TILE_SIZE, 15,7)
                        enemy_ninja_group.add(enemy)
                    elif tile == 12: # create boxes
                        self.obstacle_list.append(tile_data)
                    
        return ninja, healthbar

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
punch = False
BG = (144,201,100)
red = (255,0,0)


def draw_bg():
    screen.fill(BG)
    width = ninja_forest.get_width()
    for x in range(5):
        screen.blit(ninja_forest, ((x * width) - bg_scroll * 0.5, 0))


enemy_ninja_group = pygame.sprite.Group()
punch_group = pygame.sprite.Group()


star_group = pygame.sprite.Group()

# creating enemies
# enemy_ninjas_group = pygame.sprite.Group()


# Game functions
def star_hit(self):
    if ninja.alive:
        ninja.health -= 5
        self.kill()

def createEnemy():
    x = random.randint(0,1)
    if x == 0:
        enemy = Viking(150, 350, 2.5,3)
        enemy_ninja_group.add(enemy)
    else:
        enemy = Viking(650, 350, 2.5,3)
        enemy_ninja_group.add(enemy)

def update_animation(ninja,screen):
    img = pygame.image.load('Sprites/ninja_hero.png')
    ninja.image = pygame.transform.scale(img, (img.get_width() / ninja.scale, img.get_height()/ninja.scale))
    ninja.draw(screen)



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
ninja, healthbar = world.process_data(world_data)            
counter, text = 3, '3'
getReadyText = 'Get Ready for Phase 1!'
pygame.time.set_timer(pygame.USEREVENT,1000)
fontNum = pygame.font.SysFont('Consolas',100)
fontText = pygame.font.SysFont('Consolas',50)
hero_group = pygame.sprite.Group()
hero_group.add(ninja)

phaseNum = 0
phase1_done = False
phase2_done = False
phase3_done = False

run = True
# Game loop
while run:
    #event loop
    clock.tick(FPS)
    draw_bg()
    world.draw()
   
    # commenting out the enemy for now
    healthbar.draw(ninja.health,screen)
    ninja.update()
    ninja.draw(screen)

    #draw enemies on screen
    for enemy in enemy_ninja_group:
        enemy.draw(screen)
        enemy.update()
        enemy.ai(ninja)
        enemy.move_towards_ninja(ninja)

    for p in punch_group:
        p.move(moving_left,moving_right)
        p.draw()


    if ninja.alive:
        screen_scroll = ninja.move(moving_left,moving_right)
        bg_scroll -= screen_scroll
        if punch:
            ninja.punch()
            punch = False
            



    #game logic
    screen.blit(fontText.render(getReadyText,True,(0,0,0)),(100,100))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        #keyboard press
        if event.type == pygame.USEREVENT:
            counter -= 1
            if counter > 0:
                text = str(counter)
            elif phaseNum == 0:
                text = 'Start!'
            else:
                text = ''
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                moving_left = True
            if event.key == pygame.K_RIGHT:
                moving_right= True
            if event.key == pygame.K_UP and ninja.alive:
                ninja.jump = True
            if event.key == pygame.K_SPACE:
                punch = True
        #keyboard release
        if event.type == pygame.KEYUP:
           if event.key == pygame.K_LEFT:
               moving_left = False
           if event.key == pygame.K_RIGHT:
               moving_right= False
    screen.blit(fontNum.render(text,True,(0,0,0)),(350,200))
    if text == 'Start!':
        phaseNum += 1
        text = ''
        getReadyText = ''
    start = pygame.time.get_ticks()
    if phaseNum == 1:
        createEnemy()
        timer = threading.Timer(2,createEnemy)
        timer.start()
        timer = threading.Timer(4,createEnemy)
        timer.start()
        phaseNum +=1
        phase1_done = True


    
    
    

    pygame.display.update()
    #render

pygame.quit()
