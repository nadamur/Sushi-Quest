import pygame, random, time, sys

class GameObjects(pygame.sprite.Sprite):
    def __init__(self, image_file):
        super().__init__()
        self.image = pygame.image.load(image_file).convert_alpha()
        self.rect = self.image.get_rect()

class Actor(GameObjects):
    def __init__(self, image_file, health, name, skillLvl, costume, position, speed):
        super().__init__(image_file)
        self.name = name
        self.health = health
        self.skillLvl = skillLvl
        self.position = position
        self.speed = speed
        self.costume_images = {'Black': '', 'Blue': '', 'Red': ''} # Shirley: Add costume images

    # Setters and Getters

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_health(self, health):
        self.health = health

    def get_health(self):
        return self.health

    def set_skillLvl(self, skillLvl):
        self.skillLvl = skillLvl

    def get_skillLvl(self):
        return self.skillLvl

    def set_costume(self, costume):
        self.costume = costume
        self.image = pygame.image.load(self.costume_images[costume]).convert_alpha()

    def get_costume(self):
        return self.costume

    def set_position(self, position):
        self.position = position

    def get_position(self):
        return self.position

    def set_speed(self, speed):
        self.speed = speed

    def get_speed(self):
        return self.speed
    
    #Methods

    #Note to Neda: Feel free to change the move method to whatever you want. I just wanted to get something working.
    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

    #Note to Neda: We should have a skill method or a skill class for the double jump and everything? 

    # Note to Shirley: Just a placeholder for now, can change later
        # def isHit(self):
        #     # check if the player is hit by something
        #     if pygame.sprite.spritecollide(self, enemies_group, False):
        #         self.health -= 10  # decrease health by 10 points
        #         if self.health <= 0:
        #             # player is dead, game over
        #             game_over()


class Enemy(GameObjects):
    def __init__(self, image_file, health, speed, position):
        super().__init__(image_file)
        self.health = health
        self.speed = speed
        self.position = position

    # Setters and Getters
    def set_health(self, health):
        self.health = health

    def get_health(self):
        return self.health

    def set_speed(self, speed):
        self.speed = speed

    def get_speed(self):
        return self.speed

    def set_position(self, position):
        self.position = position

    def get_position(self):
        return self.position

    # Methods
    def move(self):
        # Add enemy movement logic here
        pass

    def hit(self):
        self.health -= 10  # decrease health by 10 points
        if self.health <= 0:
            self.die()

    def die(self):
        # Add death animation and logic here
        pass


    




