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
score2 = 0
score_increment = 0.05
fade_counter = 0
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PANEL = (153, 217, 234)
font_small = pygame.font.SysFont('Lucida Sans', 20)
font_big = pygame.font.SysFont('Lucida Sans', 24)

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
        self.punch_expire = 0
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
        if self.punch_expire > 0:
            self.punch_expire -=1
        # self.update_animation()
        if self.punch_cooldown > 0:
            self.punch_cooldown -=1
        if self.punch_expire ==0:
            for pun in punch_group:
                pun.kill()

    def punch(self):
        if self.punch_cooldown == 0:
            self.punch_cooldown = 50
            self.punch_expire = 20
            for pun in punch_group:
                pun.kill()
            punch = Punch(self.rect.centerx + (0.6*self.rect.size[0]*self.direction),self.rect.centery,self.direction)
            punch_group.add(punch)

    def dead(self):
        if self.health <=0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(1)
        else:
            self.update_action(0)

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
        if self.jump == True and self.jump_counter < 1:
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
class Hit(pygame.sprite.Sprite):
    def __init__(self,x,y,direction):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('Sprites/viking_hit_3.png').convert_alpha()
        img = pygame.transform.scale(img,(img.get_width()/3,img.get_height()/3))
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.hitting = False
        self.flip = False
        self.direction = direction
        self.animation_cooldown = 5
        
    def draw (self):
        screen.blit(pygame.transform.flip(self.image,self.flip,False),self.rect)
    def update(self):
        if self.animation_cooldown > 0:
            self.animation_cooldown -= 1
        if pygame.sprite.spritecollide(ninja,hit_group,False):
            if ninja.alive:  
                if self.animation_cooldown == 0:
                    self.kill()
                    ninja.health -= 5
                    
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
        self.animation_cooldown = 30
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
        for enemy in enemy_ninja_group:
            if pygame.sprite.spritecollide(enemy, punch_group,False):
                if self.dead == False:
                    if enemy.alive:
                        enemy.health -= 10
                        self.dead = True
                if self.animation_cooldown == 0:
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
        if self.jump == True and self.jump_counter < 1:
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
        self.health = 10
        self.max_health = self.health
        self.jump_counter = 0
        self.update_time = pygame.time.get_ticks()
        self.idling = False
        self.hit_cooldowon = 0
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

    def update(self):
        self.dead()
        if self.hit_cooldowon > 0:
            self.hit_cooldowon -=1
        
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
            self.update_animation()

    def hit(self):
        if ninja.alive:
            if self.hit_cooldowon == 0:
                self.hit_cooldowon = 20
                k = Hit(self.rect.centerx + (0.25 * self.rect.size[0]*self.direction),self.rect.centery,self.direction)
                hit_group.add(k)
        
    def move_towards_ninja(self,ninja):
        if ninja.alive:
            if self.alive:
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
hit_group = pygame.sprite.Group()

star_group = pygame.sprite.Group()


# Game functions
def star_hit(self):
    if ninja.alive:
        ninja.health -= 5
        self.kill()

def createEnemy():
    x = random.randint(150,650)
    enemy = Viking(x, 350, 2.5,3)
    enemy_ninja_group.add(enemy)

level_done = False
def check_level_done():
    test = True
    if len(enemy_ninja_group)>= 3:
        for enemy in enemy_ninja_group:
            if enemy.alive:
                test = False
    else:
        test = False
    
    return test

def reset_count(counter,reset_counter):
    if reset_counter == True:
        counter = 7
    return counter

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def reset_enemies():
    for enemy in enemy_ninja_group:
        enemy.kill()

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
counter, text = 5, '3'
getReadyText = 'Get Ready for Phase 1!'
pygame.time.set_timer(pygame.USEREVENT,1000)
fontNum = pygame.font.SysFont('Consolas',100)
fontText = pygame.font.SysFont('Consolas',50)
fontScore = pygame.font.SysFont('Condolas',35)
hero_group = pygame.sprite.Group()
hero_group.add(ninja)

phaseNum = 0
x = 0
level1_done = False
level2_done = False
level3_done = False
reset_counter_2 = True
reset_counter_3 = True




def display_win_screen(screen, award_image, new_skill, WIN_WIDTH=640, WIN_HEIGHT=800):
    # Render the "You Win!" text
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



run = True
# Game loop
while run:
    if ninja.alive:
        clock.tick(FPS)
        draw_bg()
        world.draw()
        sc = round(score2)
        s = str(sc)
        screen.blit(fontScore.render("Score: " + s,True,(255,0,0)),(20,50))
        if ninja.alive:
            score2 += score_increment
    
        # commenting out the enemy for now
        healthbar.draw(ninja.health,screen)
        ninja.update()
        ninja.draw(screen)

        #draw enemies on screen
        for enemy in enemy_ninja_group:
            enemy.draw(screen)
            enemy.ai(ninja)
            enemy.update()
            enemy.move_towards_ninja(ninja)
            if pygame.sprite.spritecollide(enemy,hero_group,False):
                if enemy.alive:
                    enemy.hit()

        for p in punch_group:
            p.move(moving_left,moving_right)
            p.draw()
            p.update()
        for h in hit_group:
            h.update()
            h.draw()


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
                if phaseNum ==0:
                    if counter > 2:
                        text = str(counter-2)
                    elif counter > 0:
                        text = 'Start'
                    elif counter == 0:
                        text = 'Start!'
                        phaseNum += 1
                if phaseNum == 2:
                    counter = reset_count(counter,reset_counter_2)
                    reset_counter_2 = False
                    if counter == 7:
                        getReadyText = '   Phase 1 Complete!'
                    elif counter > 3:
                        text = str(counter -3)
                        getReadyText = 'Get Ready for Phase 2!'
                    elif counter > 0:
                        text = 'Start'
                    elif counter ==0:
                        text = 'Start!'
                        level1_done = True
                if phaseNum == 3:
                    counter = reset_count(counter,reset_counter_3)
                    reset_counter_3 = False
                    if counter == 7:
                        getReadyText = '   Phase 2 Complete!'
                    if counter > 3:
                        text = str(counter -3)
                        getReadyText = 'Get Ready for Phase 3!'
                    elif counter > 0:
                        text = 'Start'
                    elif counter ==0:
                        text = 'Start!'
                        level2_done = True
        
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    moving_left = True
                if event.key == pygame.K_RIGHT:
                    moving_right= True
                if event.key == pygame.K_UP and ninja.alive:
                    ninja.jump = True
                    for p in punch_group:
                        p.jump = True
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
            text = ''
            getReadyText = ''
        start = pygame.time.get_ticks()

        if level_done:
            phaseNum += 1
            level_done = False
        
        if phaseNum == 1 and x == 0:
            print(phaseNum)
            createEnemy()
            timer = threading.Timer(2,createEnemy)
            timer.start()
            timer = threading.Timer(3,createEnemy)
            timer.start()
            x = 1
            level1_intro_done = True

        if phaseNum == 2 and level1_done == True:
            createEnemy()
            createEnemy()
            timer = threading.Timer(2,createEnemy)
            timer.start()
            timer = threading.Timer(2,createEnemy)
            timer.start()
            level1_done = False

        if phaseNum ==3 and level2_done == True:
            level1_done = False
            createEnemy()
            createEnemy()
            timer = threading.Timer(2,createEnemy)
            timer.start()
            timer = threading.Timer(2,createEnemy)
            timer.start()
            timer = threading.Timer(2,createEnemy)
            timer.start()
            level2_done = False
        if phaseNum == 4:
            getReadyText = '     YOU DID IT!'
            display_win_screen(screen,"Assets/Sushi/salmon+cucumber.png","Level up")
            
        level_done = check_level_done()
        if level_done == True:
            reset_enemies()
    else:
        screen.fill((0, 0, 0))
        draw_text('Game Over!', font_big, WHITE, 220, 200)
        draw_text('Press space to try again', font_big, WHITE, 150, 300)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Reset the game state
                    ninja.alive = True
                    ninja.health = 100  # Reset ninja health
                    score2 = 0
                    phaseNum = 0
                    x = 0
                    level1_done = False
                    level2_done = False
                    level3_done = False
                    move_on = False
                    reset_counter_2 = True
                    reset_counter_3 = True
                    counter = 10
                    text = str(counter)
                    getReadyText = 'Get Ready for Phase 1!'
                    for enemy in enemy_ninja_group:
                        enemy.kill()
                    for p in punch_group:
                        p.kill()
                    for h in hit_group:
                        h.kill()
                    for e in hero_group:
                        e.kill()
                

    

    pygame.display.update()
    #render

pygame.quit()
