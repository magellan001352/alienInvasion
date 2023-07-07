import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    #A Class to manage the she ship
    def __init__(self, ai_game):
        #Initialize the ship and set the starting position
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()


        #load the ship image and get its rectangle
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        #start each new ship at the bottom center of the screen
        self.rect.midbottom = self.screen_rect.midbottom

        #Store a float for the ship's exact horizontal position
        self.x = float(self.rect.x)

        # Movement flag; start with a ship that's not moving
        self.moving_right = False
        self.moving_left = False

    def update(self):
        #Update ship's position based on the movement flag
        #update ship X value not the rect
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        #Update rect object from self.x
        self.rect.x = self.x

    def blitme(self):
        #draw the ship and its current location
        self.screen.blit(self.image, self.rect)
    
    def center_ship(self):
        #center the ship on the screen
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)