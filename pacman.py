import pygame
from pygame.locals import *
from pygame.math import Vector2
from constants import *

class Pacman(object):
    def __init__(self):
        self.name = PACMAN
        self.position = Vector2(200, 400)
        #velocity vectors
        self.directions = {STOP:Vector2(), UP:Vector2(0,-1), DOWN:Vector2(0,1), LEFT:Vector2(-1,0), RIGHT:Vector2(1,0)}
        #default direction. defines where pacman is going
        self.direction = STOP
        self.speed = 100 * TILEWIDTH/16
        self.radius = 10
        self.color = YELLOW

    def update(self, delta):	
        #update position
        self.position += self.directions[self.direction]*self.speed*delta
        direction = self.getValidKey()
        self.direction = direction

    #convert input into a directions keyword.
    def getValidKey(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[K_UP]:
            return UP
        if key_pressed[K_DOWN]:
            return DOWN
        if key_pressed[K_LEFT]:
            return LEFT
        if key_pressed[K_RIGHT]:
            return RIGHT
        return STOP