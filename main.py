# Import
import math
import pygame, random, time, sys
import GameObjects
import csv
import os
from characterCustomization import selected_color




with open("characterCustomization.py") as f:
    exec(f.read())


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
BLACK = (0, 0, 0)
score = [0]
score_increment = 0.05
color = selected_color
fontScore = pygame.font.SysFont('Condolas',35)
font_big = pygame.font.SysFont('Comic Sans',35)
WHITE = (255,255,255)
BLACK = (0,0,0)
fade_counter = 0

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
    
#creating the text for the game over screen
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

#creating the player
class Ninja(pygame.sprite.Sprite):
    def __init__(self, char_type,x, y, scale,speed):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.direction = 1
        self.scale = scale
        self.throw_cooldown = 0
        self.vel_y = 0
        self.jump = False
        self.dead_counter = 15
        self.flip = False
        self.frame_index = 0
        self.action = 0
        self.punching = False
        self.punch_cooldown = 0
        self.punch_expire = 0
        self.health = 100
        self.max_health = self.health
        self.jump_counter = 0
        self.update_time = pygame.time.get_ticks()
        self.idling = False
        self.idling_counter = 0
        self.move_counter = 0
        self.action = 0
        self.vision = pygame.Rect(0,0,150,20)
        self.animation_list = []
        if char_type == 'ninja':
            img = pygame.image.load(f'Assets/Ninja/ninja_hero_sprite_{selected_color}.png')
            img = pygame.transform.scale(img, (img.get_width() / scale, img.get_height()/scale))
            self.animation_list.append(img)
            img = pygame.image.load(f'Assets/Ninja/dead_{selected_color}.png')
            img = pygame.transform.scale(img, (img.get_width() / self.scale, img.get_height()/self.scale))
            self.animation_list.append(img)  
        else:
            img = pygame.image.load('Assets/Ninja/enemy_ninja.gif')
            img = pygame.transform.scale(img, (img.get_width() / scale, img.get_height()/scale))
            self.animation_list.append(img)
            img = pygame.image.load('Assets/Ninja/dead_enemy_ninja.png')
            img = pygame.transform.scale(img, (img.get_width() / self.scale, img.get_height()/self.scale))
            self.animation_list.append(img)  

        
        self.image = self.animation_list[self.action]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()

                                
    def update(self):
        if self.char_type == 'enemy':
            if self.alive == False:
                self.dead_counter -= 1
            if self.dead_counter == 0:
                score[0] -= 20
                self.kill()
        self.update_animation()
        self.dead()
        if self.throw_cooldown > 0:
            self.throw_cooldown -=1
        if self.punch_expire > 0:
            self.punch_expire -=1
        if self.punch_cooldown > 0:
            self.punch_cooldown -=1
        # if self.punch_expire ==0:
            # for pun in punch_group:
            #     pun.kill()

    def move(self, moving_left,moving_right):
        screen_scroll = 0
        dx = 0
        dy = 0

        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1

        #jumping
        if self.jump == True and self.jump_counter < 1:
            self.vel_y = -16
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
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
                if self.char_type == 'enemy':
                    self.direction *= -1
                    self.move_counter = 0
            #check collision in y direction
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                #check if below the ground i.e. jumping
                if self.vel_y < 0:
                    dy = tile[1].bottom - self.rect.top
                    self.vel_y = 0
                #check if above the ground i.e. falling
                elif self.vel_y >= 0:
                    dy = tile[1].top - self.rect.bottom
                    self.vel_y = 0
                    self.jump_counter = 0

        if self.rect.bottom > SCREEN_HEIGHT:
            self.health = 0

        #check if going off the edges of the screen
        if self.char_type == 'ninja':
            if self.rect.left + dx < 0 or self.rect.right + dx > SCREEN_WIDTH:
                dx = 0
        
        level_complete = False
        if self.char_type == 'ninja':
        #checking for collision with exit
            if pygame.sprite.spritecollide(self, exit_group, False):
                level_complete = True

        #update rectangle position
        self.rect.x += dx
        self.rect.y += dy

        #update scroll based on player position
        if self.char_type == 'ninja':
            if (self.rect.right > SCREEN_WIDTH - SCROLL_THRESH and bg_scroll < (world.level_length * TILE_SIZE) - SCREEN_WIDTH)\
            or (self.rect.left < SCROLL_THRESH and bg_scroll > abs(dx)):
                self.rect.x -= dx
                screen_scroll = -dx

        return screen_scroll, level_complete
    
    def throw(self):
        if self.throw_cooldown == 0:
            self.throw_cooldown = 20
            star = Star(self.rect.centerx + (0.75 * self.rect.size[0] * self.direction), self.rect.centery, self.direction)
            star_group.add(star)
    
    def ai(self):
         if self.alive and ninja.alive:
            if self.idling == False and random.randint(1, 200) == 1:
                self.idling = True
                self.idling_counter = 50
			#check if the ai in near the player
            if self.vision.colliderect(ninja.rect):
                self.throw()
            else:
                if self.idling == False:
                    if self.direction == 1:
                        ai_moving_right = True
                    else:
                        ai_moving_right = False
                    ai_moving_left = not ai_moving_right
                    self.move(ai_moving_left, ai_moving_right)
                    self.move_counter += 1
                    self.vision.center = (self.rect.centerx + 75 * self.direction, self.rect.centery)
                    
                    if self.move_counter > TILE_SIZE:
                        self.direction *= -1
                        self.move_counter *= -1
                else:
                    self.idling_counter -= 1
                    if self.idling_counter <= 0:
                        self.idling = False
            self.rect.x += screen_scroll

    def update_animation(self):
        self.image = self.animation_list[self.action]            
            
    def dead(self):
        if self.health <=0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(1)
    
    def draw(self,screen):
        screen.blit(pygame.transform.flip(self.image,self.flip,False),self.rect)

    


    def update_action(self,new_action):
        if new_action != self.action:
            self.action = new_action

    def punch(self):
        if self.char_type == 'ninja':
            if self.punch_cooldown == 0:
                self.punch_cooldown = 50
                self.punch_expire = 20
                for pun in punch_group:
                    pun.kill()
                punch = Punch(self.rect.centerx + (0.6*self.rect.size[0]*self.direction),self.rect.centery,self.direction)
                punch_group.add(punch)


class Exit(pygame.sprite.Sprite):
	def __init__(self, img, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = img
		self.rect = self.image.get_rect()
		self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

	def update(self):
		self.rect.x += screen_scroll

class Star(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('Sprites/star.png')
        img = pygame.transform.scale(img,(int(img.get_width()/20),int(img.get_height()/20)))
        self.image = img
        self.rect = self.image.get_rect()
        self.speed = 10
        self.rect.center = (x,y)
        self.direction = direction
    
    def update(self):
        self.rect.x += (self.direction*self.speed) + screen_scroll
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()
        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect):
                self.kill()
        if pygame.sprite.spritecollide(ninja,star_group,False):
            if ninja.alive:
                ninja.health -= 5
                self.kill()

class Punch(pygame.sprite.Sprite):
    def __init__(self,x,y,direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 7
        self.direction = direction
        self.vel_y = 0
        self.jump = False
        self.scale = 15
        self.flip = False
        self.dead = False
        self.moved = False
        self.animation_cooldown = 30
        self.jump_counter = 0
        img = pygame.image.load('Sprites/hero_punch.png')
        img = pygame.transform.scale(img, (img.get_width() / 15, img.get_height()/15))
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

    def draw(self):
        screen.blit(pygame.transform.flip(self.image,self.flip,False),self.rect)
    def update(self):
        if self.animation_cooldown > 0:
            self.animation_cooldown -= 1
        if self.animation_cooldown == 0:
            self.kill()
        for enemy in enemy_ninja_group:
            if pygame.sprite.spritecollide(enemy, punch_group,False):
                if self.dead == False:
                    if enemy.alive:
                        enemy.health -= 50
                        self.dead = True
                if self.animation_cooldown == 0:
                    self.kill()
                
                
                    
    def move(self, moving_left,moving_right):
        if ninja.direction ==1:
            if self.moved == False:
                self.flip = True
            self.moved = True
            self.rect.x = ninja.rect.x + 20
        elif ninja.direction == -1:
            if self.moved == False:
               self.flip = False 
            self.rect.x = ninja.rect.x -20
            self.moved = True
            
        
        self.rect.y = ninja.rect.y+10
        
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
                        # self.obstacle_list.append(tile_data)
                        enemy = Ninja('enemy',x * TILE_SIZE, y * TILE_SIZE, 15,7)
                        enemy_ninja_group.add(enemy)
                    elif tile == 20: #create exit to the stage
                        exit = Exit(img,x * TILE_SIZE, y * TILE_SIZE)
                        exit_group.add(exit)
                    
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

def display_win_screen(screen, award_image, new_skill, WIN_WIDTH=640, WIN_HEIGHT=800):
    # Render the "You Win!" text
    screen.fill(BLACK)
    win_font = pygame.font.Font(None, 72)
    win_text = win_font.render("You Win!", True, (255, 255, 255))
    win_text_rect = win_text.get_rect(center=(400, 300 - 100))

    # Load the award image and position it
    award = pygame.image.load(award_image)
    award_rect = award.get_rect(center=(400, 300))

    # Render the new skill text
    skill_font = pygame.font.Font(None, 48)
    skill_text = skill_font.render(f"New Skill: {new_skill}", True, (255, 255, 255))
    
    skill_text_rect = skill_text.get_rect(center=(400, 300 + 100))

    # Draw everything on the screen
    screen.blit(win_text, win_text_rect)
    screen.blit(award, award_rect)
    screen.blit(skill_text, skill_text_rect)

    # Update the display and wait
    pygame.display.update()
    pygame.time.delay(3000)



enemy_ninja_group = pygame.sprite.Group()
star_group = pygame.sprite.Group()
punch_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()




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

run = True
# Game loop
while run:
    #event loop
    clock.tick(FPS)
    draw_bg()
    world.draw()
    sc = round(score[0])
    s = str(sc)
    screen.blit(fontScore.render("Score: " + s,True,(255,0,0)),(20,50))
    if ninja.alive:
        score[0] += score_increment
    ninja.draw(screen)
    for enemy in enemy_ninja_group:
        enemy.draw(screen)
    for p in punch_group:
            p.move(moving_left,moving_right)
            p.draw()
            p.update()
    # commenting out the enemy for now
    healthbar.draw(ninja.health,screen)
    ninja.update()
    

    #draw enemies on screen
    for enemy in enemy_ninja_group:
        enemy.ai()
        enemy.update()
    star_group.draw(screen)

   #update and draw groups
    star_group.update()
    star_group.draw(screen)
    
    exit_group.update()
    exit_group.draw(screen)

    
        
    if ninja.alive:
        screen_scroll,level_complete = ninja.move(moving_left,moving_right)
        bg_scroll -= screen_scroll
        #check if player has reached the end of the level
        if level_complete == True:
            display_win_screen(screen,"Assets/Sushi/rice+seaweed.png","Power Up Punching")
            
        if punch:
                ninja.punch()
                punch = False
    else:
        if fade_counter < SCREEN_WIDTH:
            fade_counter += 5
            for y in range(0, 6, 2):
                pygame.draw.rect(screen, BLACK, (0, y * 100, fade_counter, 100))
                pygame.draw.rect(screen, BLACK, (SCREEN_WIDTH - fade_counter, (y + 1) * 100, SCREEN_WIDTH, 100))
        else:
            sc = 0
            screen.fill(BLACK)
            draw_text('Game Over!', font_big, WHITE, 300, 200)
            draw_text('Press R to try again', font_big, WHITE, 230, 300)


            key = pygame.key.get_pressed()
            enemy_ninja_group.empty()
           
            if key[pygame.K_r]:
                run = True
                fade_counter = 0
                score[0] = 0
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


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            score[0] = 0
            run = False
        #keyboard press
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
    score1 = score[0]
    
    

    pygame.display.update()
    #render

pygame.quit()
