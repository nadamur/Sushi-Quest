import pygame, random, time, sys

# class Ninja(pygame.sprite.Sprite):
#     def __init__(self, char_type,x, y, scale,speed):
#         pygame.sprite.Sprite.__init__(self)
#         self.alive = True
#         self.char_type = char_type
#         self.speed = speed
#         self.direction = 1
#         self.vel_y = 0
#         self.jump = False
#         self.flip = False
#         self.frame_index = 0
#         self.action = 0
#         self.health = 0
#         self.max_health = self.health
#         self.jump_counter = 0
#         self.update_time = pygame.time.get_ticks()

#         img = pygame.image.load('Sprites/ninja_hero_sprite.png')
#         health = pygame.image.load('Sprites/temp_healthbar.jpg')
#         self.image = pygame.transform.scale(img, (img.get_width() / scale, img.get_height()/scale))
#         self.rect = self.image.get_rect()
#         self.rect.center = (x, y)

#     def update(self):
#         self.dead()

#     def dead(self):
#         if self.health <=0:
#             self.health = 0
#             self.speed = 0
#             self.alive = False

    
#     def draw(self,screen):
#         screen.blit(pygame.transform.flip(self.image,self.flip,False),self.rect)

#     def move(self, moving_left,moving_right):
#         dx = 0
#         dy = 0
#         if moving_left:
#             dx = -self.speed
#             self.flip = True
#             self.direction = -1
#         if moving_right:
#             dx = self.speed
#             self.flip = False
#             self.direction = 1

#         #jumping
#         if self.jump == True and self.jump_counter < 2:
#             self.vel_y = -11
#             self.jump = False
#             self.jump_counter +=1

#         #gravity
#         self.vel_y += 0.75
#         if self.vel_y>10:
#             self.vel_y
#         dy += self.vel_y

#         #hit the floor
#         if self.rect.bottom + dy > 622:
#             dy = 622 - self.rect.bottom
#             self.jump_counter = 0

#         self.rect.x += dx
#         self.rect.y += dy


# commenting out the enemy ninja for now
# class EnemyNinja(pygame.sprite.Sprite):
#     def __init__(self, x, y, scale):
#         pygame.sprite.Sprite.__init__(self)
#         self.alive = True
#         self.direction = 1
#         self.flip = False
#         self.vel_y = 0
#         self.action = 0
#         self.health = 100
#         self.max_health = self.health
#         self.jump_counter = 0
#         self.update_time = pygame.time.get_ticks()
#         self.move_counter = 0
#         self. vision = pygame.Rect(0,0,300,640)
#         self.idling = False
#         self.idling_counter = 0
#         img = pygame.image.load('Assets/Ninja/ninja_hero_sprite_orange.png')
#         self.image = pygame.transform.scale(img, (img.get_width() / scale, img.get_height()/scale))
#         self.rect = self.image.get_rect()
#         self.rect.center = (x, y)

#     def update(self):
#         self.dead()

#     def dead(self):
#         if self.health <=0:
#             self.health = 0
#             self.speed = 0
#             self.alive = False

    
#     def draw(self,screen):
#         screen.blit(pygame.transform.flip(self.image,self.flip,False),self.rect)

#     # def throw_star(self,sprite_group):
#     #     star = Star(self.rect.centerx + (0.75 * self.rect.size[0]*self.direction),self.rect.centery,self.direction)
#     #     sprite_group.add(star)

#     def move(self):
#         dx = 0
#         dy = 0

#         #gravity
#         self.vel_y += 0.75
#         if self.vel_y>10:
#             self.vel_y
#         dy += self.vel_y

#         #collision check
#         for tile in world.obstacle_list:
#             #check collision in x direction
#             if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.rect.width, self.rect.height):
#                 dx = 0
#             #check collision in y direction
#             if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.rect.width, self.rect.height):
#                 #check if below the ground i.e. jumping
#                 if self.vel_y < 0:
#                     dy = tile[1].bottom - self.rect.top
#                     self.vel_y = 0
#                 #check if above the ground i.e. falling
#                 elif self.vel_y >= 0:
#                     dy = tile[1].top - self.rect.bottom
#                     self.vel_y = 0
#                     self.jump_counter = 0


    # def ai(self,ninja,sprite_group):
    #     if self.alive and ninja.alive:
    #         if self.idling == False and random.randint(1,200) == 1:
    #             self.idling = True
    #             self.idling_counter = 50
    #         # if self.vision.colliderect(ninja.rect):
    #         #     self.throw_star(sprite_group)


  
# commenting out the star class for now because for some reason it's not working

# class Star(pygame.sprite.Sprite):
#     def __init__(self, x,y,direction):
#         pygame.sprite.Sprite.__init__(self)
#         self.speed = 10
#         self.image = pygame.image.load('groupproject-team-8/Sprites/star.png')
#         self.rect = self.image.get_rect()
#         self.rect.center = (x,y)
#         self.direction = direction

#     def update(self):
#         self.rect.x += (self.direction*self.speed)
#         #check if off screen, 800 is screen width
#         if self.rect.right < 0 or self.rect.left > 800:
#             self.kill()

class HealthBar():
    def __init__(self, x, y, health, max_health):
        self.x = x
        self.y = y
        self.health = health
        self.max_health = max_health

    def draw(self, health,screen):
        black = (0,0,0)
        red = (255,0,0)
        green = (0,255,0)
        self.health = health
        ratio = self.health / self.max_health
        pygame.draw.rect(screen, black, (self.x - 2, self.y - 2, 154, 24))
        pygame.draw.rect(screen, red, (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, green, (self.x, self.y, 150 * ratio, 20))



class EnemyStar():
    #game object class for the star
    def __init__(self, x, y, scale):
        #moves towards the player at a constant speed and then disappears when it hits the player or the edge of the screen or the ground and starts at the enemy's position
        self.x = x
        self.y = y
        self.scale = scale
        self.speed = 10
        self.image = pygame.image.load('Sprites/star.png')
        self.image = pygame.transform.scale(self.image, (self.image.get_width() / scale, self.image.get_height()/scale))
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)












# class GameObjects(pygame.sprite.Sprite):
#     def __init__(self,x,y,image):
#         super().__init__()
#         self.image = pygame.image.load(image)
#         self.rect = self.image.get_rect()
#         self.rect.center = (x,y)
#     def update(self):
#         pass
#     def draw(self,screen):
#         screen.blit(self.image,self.rect)

# class Ninja(GameObjects):
#     def __init__(self, x,y):
#         self.image = 'groupproject-team-8/Sprites/ninja_hero_sprite.png'
#         pygame.transform.scale(self.image, (self.image.get_width() / 13, self.image.get_height()/13))
#         super().__init__(x,y,self.image)

# class Actor(GameObjects):
#     def __init__(self, x,y,image_file, health, name, skillLvl, speed):
#         super().__init__(x,y,image_file)
#         self.name = name
#         self.health = health
#         self.skillLvl = skillLvl
#         self.speed = speed
#         self.costume_images = {'Black': '', 'Blue': '', 'Red': ''} # Shirley: Add costume images

#     def update(self):
#         keys = pygame.key.get_pressed()
#         if keys[pygame.K_LEFT]:
#             self.move(-10,0)
#         if keys[pygame.K_RIGHT]:
#             self.move(10,0)  

#     def move(self,x,y):
#         self.rect.move_ip([x,y])

#     def draw(self, screen):
#         super().draw(screen)
#                     # Setters and Getters

#     def set_name(self, name):
#         self.name = name

#     def get_name(self):
#         return self.name

#     def set_health(self, health):
#         self.health = health

#     def get_health(self):
#         return self.health

#     def set_skillLvl(self, skillLvl):
#         self.skillLvl = skillLvl

#     def get_skillLvl(self):
#         return self.skillLvl

#     def set_costume(self, costume):
#         self.costume = costume
#         self.image = pygame.image.load(self.costume_images[costume]).convert_alpha()

#     def get_costume(self):
#         return self.costume

#     def set_position(self, position):
#         self.position = position

#     def get_position(self):
#         return self.position

#     def set_speed(self, speed):
#         self.speed = speed

#     def get_speed(self):
#         return self.speed
    
#     #Methods

#     #Note to Neda: Feel free to change the move method to whatever you want. I just wanted to get something working.


#     #side note: we probably need to run this in the main class under 'while running' since it has to be permanently happening
    
#     def move(self):
#         #will keep track of whether the player is currently mid-air
#         isJump = False
#         #v is the velocity of the jump
#         v = 5
#         #m is just for the sake of keeping track of gravity
#         m = 1
#         #self explanatory
#         jumpCounter = 0
#         keys = pygame.key.get_pressed()
#         if keys[pygame.K_LEFT]:
#             self.rect.x -= self.speed
#         if keys[pygame.K_RIGHT]:
#             self.rect.x += self.speed

#         #jumping
#         if self.skillLvl == 0:
#             if isJump ==False:
#                 if keys[pygame.K_SPACE]:
#                    isJump = True
#             if isJump:
#                 #F is the force
#                 F = (1/2)*m*(v**2)
#                 #we need to properly clean up the Player class before this method can work
#                 y_position = self.get_position()
#                 v = v-1
#                 if v<0:
#                     m=-1
#                 if v==-6:
#                     isJump= False

#                     #reset
#                     v=5
#                     m=1

#         #if double jump is unlocked
#         if self.skillLvl>0:
#             if isJump ==False and jumpCounter<=2:
#                 if keys[pygame.K_SPACE]:
#                    isJump = True
#                    jumpCounter+=1
#             if isJump:
#                 F = (1/2)*m*(v**2)
#                 self.position.y -= F
#                 v = v-1
#                 if v<0:
#                     m=-1
#                 if v==-6:
#                     jumpCounter=0
#                     isJump= False
#                     v=5
#                     m=1
#         pygame.time.delay(10)
#         pygame.display.update()    

        


#     #Note to Neda: We should have a skill method or a skill class for the double jump and everything? 

#     # Note to Shirley: Just a placeholder for now, can change later
#         # def isHit(self):
#         #     # check if the player is hit by something
#         #     if pygame.sprite.spritecollide(self, enemies_group, False):
#         #         self.health -= 10  # decrease health by 10 points
#         #         if self.health <= 0:
#         #             # player is dead, game over
#         #             game_over()


# class Enemy(GameObjects):
#     def __init__(self, image_file, health, speed, position):
#         super().__init__(image_file)
#         self.health = health
#         self.speed = speed
#         self.position = position

#     # Setters and Getters
#     def set_health(self, health):
#         self.health = health

#     def get_health(self):
#         return self.health

#     def set_speed(self, speed):
#         self.speed = speed

#     def get_speed(self):
#         return self.speed

#     def set_position(self, position):
#         self.position = position

#     def get_position(self):
#         return self.position

#     # Methods
#     def move(self):
#         # Add enemy movement logic here
#         pass

#     def hit(self):
#         self.health -= 10  # decrease health by 10 points
#         if self.health <= 0:
#             self.die()

#     def die(self):
#         # Add death animation and logic here
#         pass


# class Projectile(GameObjects):
#     def __init__(self, image_file, speed, position,damage):
#         super().__init__(image_file)
#         self.speed = speed
#         self.position = position
#         self.damage = damage

#     # Setters and Getters
#     def set_speed(self, speed):
#         self.speed = speed

#     def get_speed(self):
#         return self.speed

#     def set_position(self, position):
#         self.position = position

#     def get_position(self):
#         return self.position
    
#     def set_damage(self, damage):
#         self.damage = damage
    
#     def get_damage(self):
#         return self.damage

#     # Methods
#     def move(self):
#         # Add projectile movement logic here
#         pass

#     def hit(self):
#         # Add projectile hit logic here
#         pass

#     def die(self):
#         # Add projectile death logic here
#         pass

    




