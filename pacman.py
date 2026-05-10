import pygame
from pygame.locals import *
from pygame.math import Vector2
from constants import *

class Pacman(object):
    def __init__(self, node):
        self.name = PACMAN
        self.position = Vector2(200, 400)
        #velocity vectors
        self.directions = {STOP:Vector2(), UP:Vector2(0,-1), DOWN:Vector2(0,1), LEFT:Vector2(-1,0), RIGHT:Vector2(1,0)}
        #default direction. defines where pacman is going
        self.direction = STOP
        self.speed = 100 * TILEWIDTH/16
        self.radius = 10
        self.color = YELLOW
        self.node = node
        self.setPosition()
        self.target = node

    def setPosition(self):
        self.position = self.node.position.copy()

    def update(self, delta):	
        #update position
        self.position += self.directions[self.direction]*self.speed*delta
        direction = self.getValidKey()
        
        #Checks if pacman has reached the destination node yet.
        if self.overshotTarget():
            self.node = self.target
            self.target = self.getNewTarget(direction)
            if self.target is not self.node:
                self.direction = direction
            else:
                self.target = self.getNewTarget(self.direction)

            if self.target is self.node:
                self.direction = STOP
            self.setPosition()
        else: 
            if self.validOppositeDirection(direction):
                self.reverseDirection()

    #inverts pacman's direction.    
    def reverseDirection(self):
        self.direction *= -1
        temp = self.node
        self.node = self.target
        self.target = temp

    #Check if the current direction has a node we can move to  
    def validDirection(self, direction):
        if direction is not STOP:
            if self.node.neighbors[direction] is not None:
                return True
        return False

    #check if the current direction is opposite to what pacman is moving
    def validOppositeDirection(self, direction):
        if direction is not STOP:
            if direction == self.direction * -1:
                return True
        return False

    def getNewTarget(self, direction):
        if self.validDirection(direction):
            return self.node.neighbors[direction]
        return self.node
    
    def overshotTarget(self):
        if self.target is not None:
            vec1 = self.target.position - self.node.position
            vec2 = self.position - self.node.position
            node2Target = vec1.magnitude_squared()
            node2Self = vec2.magnitude_squared()
            return node2Self >= node2Target
        return False

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
    
    def render(self, screen):
        p = self.position
        pygame.draw.circle(screen, self.color, p, self.radius)