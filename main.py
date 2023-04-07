# Import
import math
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
        self.vision = pygame.Rect(0,0,150,640)

        img = pygame.image.load('Sprites/ninja_hero_sprite.png')
        health = pygame.image.load('Sprites/temp_healthbar.jpg')
        self.image = pygame.transform.scale(img, (img.get_width() / scale, img.get_height()/scale))
        #crop the image 5 pixels from the bottom
        self.image = self.image.subsurface(5,0,self.image.get_width()-14,self.image.get_height()-20)
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

    def throw(self):
        if self.throw == 0 and self.ammo > 0:
            self.throw = 20
            star = Star(self.rect.centerx + (0.75 * self.rect.size[0] * self.direction), self.rect.centery, self.direction)
            star_group.add(star)
            #reduce ammo
            self.ammo -= 1
            
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
    
    def ai(self):
         if self.alive and ninja.alive:
            if self.idling == False and random.randint(1, 200) == 1:
                self.update_action(0)#0: idle
                self.idling = True
                self.idling_counter = 50
			#check if the ai in near the player
            if self.vision.colliderect(ninja.rect):
				#stop running and face the player
                self.update_action(0)#0: idle
				#throw
                self.throw()
            else:
                if self.idling == False:
                    if self.direction == 1:
                        ai_moving_right = True
                    else:
                        ai_moving_right = False
                    ai_moving_left = not ai_moving_right
                    self.move(ai_moving_left, ai_moving_right)
                    self.update_action(1)#1: run
                    self.move_counter += 1
					#update ai vision as the enemy moves
                    self.vision.center = (self.rect.centerx + 75 * self.direction, self.rect.centery)
                    
                    if self.move_counter > TILE_SIZE:
                        self.direction *= -1
                        self.move_counter *= -1
                else:
                    self.idling_counter -= 1
                    if self.idling_counter <= 0:
                        self.idling = False

class Stars(pygame.sprite.Sprite):
    def __init__(self, image, x, y, target_x, target_y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 5
        self.target = pygame.math.Vector2(target_x, target_y)
        self.direction = self.target - pygame.math.Vector2(x, y)
        self.distance = self.direction.length()
        self.direction.normalize_ip()
    
    def update(self):
        self.rect.move_ip(self.direction * self.speed)
        self.distance -= self.speed
        if self.distance <= 0:
            self.kill()

                                        
class EnemyNinja(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, speed):
        super().__init__()
        img = pygame.image.load('Assets/Ninja/ninja_hero_sprite_orange.png')
        self.image = pygame.transform.scale(img, (img.get_width() / scale, img.get_height()/scale))   
        self.image = self.image.subsurface(5,0,self.image.get_width()-14,self.image.get_height()-20)      
        self.rect = self.image.get_rect() 
        self.rect.center = (x, y)
        self.stars_image = pygame.image.load('Sprites/Star.png').convert_alpha()
        self.stars_rect = self.stars_image.get_rect()
        self.speed = 3
        self.distance = 200
        self.attack_distance = 50
        self.is_throwing_stars = False
    
    def update(self, ninja):
        dx, dy = ninja.rect.x - self.rect.x, ninja.rect.y - self.rect.y
        distance = (dx ** 2 + dy ** 2) ** 0.5
        if distance < self.distance:
            self.is_throwing_stars = True
            self.throw_stars(ninja)
        else:
            self.is_throwing_stars = False
        if distance < self.attack_distance:
            self.attack(ninja)
        else:
            self.move(dx, dy)
    
    def move(self, dx, dy):
        angle = math.atan2(dy, dx)
        self.rect.x += self.speed * math.cos(angle)
        self.rect.y += self.speed * math.sin(angle)
    
    def attack(self, ninja):
        pass  # TODO: implement attack behavior
    
    def throw_stars(self, ninja):
        if self.is_throwing_stars:
            for i in range(3):
                stars = Stars(self.stars_image, self.rect.x, self.rect.y, ninja.rect.x, ninja.rect.y)
                star_group.add(stars)

    #class that throws 1 star from the enemy ninja of GameObjects.py EnemyStar class
    #def throw_star(self):
        #throw one star surface
     #   star = GameObjects.EnemyStar(self.rect.centerx + (0.5 * self.rect.size[0] * self.direction), self.rect.centery, self.direction)
            
    



    def update(self):
        #self.update_animation()
        self.is_alive()


    def is_alive(self):
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
    
    #def ai(self,ninja):
     #   if self.alive and ninja.alive:
      #      if self.idling == False and random.randint(1,200) == 1: 
       #         self.idling = True 
        #        self.idling_counter = 50 
            # if self.vision.colliderect(ninja.rect):
            # #     self.throw_star(sprite_group)
            # else:
            #     if self.idling == False:
            #         if self.direction ==1:
         #   self.move()


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
                        enemy = EnemyNinja(x * TILE_SIZE, y * TILE_SIZE, 15,7)
                        enemy_ninja_group.add(enemy)
                    
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
BG = (144,201,100)
red = (255,0,0)


def draw_bg():
    screen.fill(BG)
    width = ninja_forest.get_width()
    for x in range(5):
        screen.blit(ninja_forest, ((x * width) - bg_scroll * 0.5, 0))


enemy_ninja_group = pygame.sprite.Group()

star_group = pygame.sprite.Group()

# creating enemies
# enemy_ninjas_group = pygame.sprite.Group()


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
ninja, healthbar = world.process_data(world_data)            
star_img = pygame.image.load('Sprites/star.png').convert_alpha()
#method to find enemy closest to player
def find_closest_enemy(ninja):
    closest_enemy = enemy_ninja_group.sprites()[0]
    for enemy in enemy_ninja_group:
        if abs(enemy.rect.x - ninja.rect.x) < abs(closest_enemy.rect.x - ninja.rect.x):
            closest_enemy = enemy
    return closest_enemy

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
        enemy.ai(enemy)
        enemy.draw(screen)
        enemy.update()

   #update and draw groups
    star_group.update()
    star_group.draw(screen)
        

    if ninja.alive:
        screen_scroll = ninja.move(moving_left,moving_right)
        bg_scroll -= screen_scroll

    
    
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
            if event.key == pygame.K_p:
                # Play punch sound effect
                #punch_sound.play()

                # Calculate the distance between the hero and the enemy closest to the hero using pythagoras theorem and find_closest_enemy function
                distance = math.sqrt((ninja.rect.x - find_closest_enemy(ninja).rect.x)**2 + (ninja.rect.y - find_closest_enemy(ninja).rect.y)**2)

                # If the distance is less than 200 pixels, the enemy is close enough to punch
                if distance < 80:
                    # Punch the enemy
                    find_closest_enemy(ninja).health -= 10

                    # If the enemy's health is less than or equal to 0, kill the enemy
                    if find_closest_enemy(ninja).health <= 0:
                        find_closest_enemy(ninja).alive = False
                        find_closest_enemy(ninja).kill()

                    # Draw the punch sprite to last for 0.5s but 10x smaller (Sprites/hero_punch.png) at the enemies's position
                    punch_sprite = pygame.image.load('Sprites/hero_punch.png')
                    punch_sprite = pygame.transform.scale(punch_sprite, (int(punch_sprite.get_width()/10), int(punch_sprite.get_height()/10)))
                    #make the punch sprite appear at the enemy's position for 0.5s
                    screen.blit(punch_sprite, (find_closest_enemy(ninja).rect.x, find_closest_enemy(ninja).rect.y))
                    pygame.display.update()
                    pygame.time.delay(500)
            
                

        
        #keyboard release
        if event.type == pygame.KEYUP:
           if event.key == pygame.K_LEFT:
               moving_left = False
           if event.key == pygame.K_RIGHT:
               moving_right= False       
    
    

    pygame.display.update()
    #render

pygame.quit()
