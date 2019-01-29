import pygame
import random
from os import path
from pygame.sprite import Sprite


# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

root_dir =  path.dirname(__file__)
images_dir = path.join(root_dir, "img")
sounds_dir = path.join(root_dir, "snd")

meteor_list = ["meteorBrown_big1.png", "meteorBrown_big2.png", "meteorBrown_big3.png", "meteorBrown_med1.png",
               "meteorBrown_small1.png", "meteorBrown_small2.png", "meteorBrown_tiny1.png"]


player_life_list = ["numeral0.png", "numeral1.png", "numeral2.png", "numeral3.png", "numeral4.png", "numeral5.png" ]

all_images = {"meteors" : [], "player_life_num" : [], "explosion_lg" : [], "explosion_sm" : []}

all_sounds = {}


# Load all images and sounds
def init():

    all_images["background"] = pygame.image.load(path.join(images_dir, "background.png")).convert()
    all_images["spaceship"] = pygame.image.load(path.join(images_dir, "playerShip2_green.png")).convert()
    all_images["laser"] = pygame.image.load(path.join(images_dir, "laserGreen13.png")).convert()
    all_images["player_life_img"] = pygame.image.load(path.join(images_dir, "playerLife2_green.png")).convert()

    for img in meteor_list:
        all_images["meteors"].append(pygame.image.load(path.join(images_dir, img)).convert())

    for img in player_life_list:
        all_images["player_life_num"].append(pygame.image.load(path.join(images_dir, img)).convert())

    all_sounds["laser"] = pygame.mixer.Sound(path.join(sounds_dir, "sfx_laser1.ogg"))
    all_sounds["music_game"] = pygame.mixer.Sound(path.join(sounds_dir, "magic_space.ogg"))
    all_sounds["meteor_explosion"] = pygame.mixer.Sound(path.join(sounds_dir, "Explosion16.wav"))


class GameObject(Sprite):

    def __init__(self):
        super(GameObject, self).__init__()


class SpaceShip(GameObject):

    def __init__(self, screenWidth, screenHeight):
        super(SpaceShip, self).__init__()
        self.image = all_images["spaceship"]
        self.rect = self.image.get_rect()
        self.image.set_colorkey(BLACK)
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.rect.centerx = screenWidth / 2
        self.rect.bottom = screenHeight - 10
        self.x_speed = 7
        self.lives = 5

    def update(self):
        # Define horizontal movement
        keystate = pygame.key.get_pressed()

        if keystate[pygame.K_LEFT]:
            self.rect.x -= self.x_speed

        if keystate[pygame.K_RIGHT]:
            self.rect.x += self.x_speed

        # Define walls
        if self.rect.right > self.screenWidth:
            self.rect.right = self.screenWidth

        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self, all_sprites, laser_group):
        laser = Laser(self.rect.centerx - 5, self.rect.top - 30)
        all_sprites.add(laser)
        laser_group.add(laser)
        all_sounds["laser"].play()

class Meteor(GameObject):

    def __init__(self, screenWidth, screenHeight):
        super(Meteor, self).__init__()
        self.image = random.choice(all_images["meteors"])
        self.rect = self.image.get_rect()
        self.image.set_colorkey(BLACK)
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.rect.x = random.randrange(0, self.screenWidth - self.rect.width)
        self.rect.y = random.randrange(-100, -50)
        self.speed_y = random.randrange(1, 5)

    def __randomPosition(self):
        self.rect.x = random.randrange(0, self.screenWidth - self.rect.width)
        self.rect.y = random.randrange(-100, -50)
        self.speed_y = random.randrange(1, 5)

    def update(self):
        self.rect.y += self.speed_y
        # Define a new random position for the meteor
        if self.rect.top > self.screenHeight or self.rect.right < 0 or self.rect.left > self.screenWidth:
            self.__randomPosition()


class Laser(GameObject):

    def __init__(self, x, y):
        super(Laser, self).__init__()
        self.image = all_images["laser"]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.y_speed = 10


    def update(self):
        self.rect.y -= self.y_speed

        # kill if it goes off the the screen
        if self.rect.bottom < 0:
            self.kill()

class Player_Life_Img(GameObject):

    def __init__(self):
        super(Player_Life_Img, self,).__init__()
        self.image = all_images["player_life_img"]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = 10
        self.rect.y = 10

    def update(self):
        pass

class Player_Life_Num(GameObject):

        def __init__(self, spaceship):
            super(Player_Life_Num, self).__init__()
            self.image = all_images["player_life_num"][spaceship.lives]
            self.rect = self.image.get_rect()
            self.rect.x = 65
            self.rect.y = 15


        def update(self):
             pass
