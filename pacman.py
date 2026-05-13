import pygame
from pygame.locals import *
from pygame.math import Vector2
from constants import *
from entity import Entity

class Pacman(Entity):
    def __init__(self, node):
        Entity.__init__(self, node)
        self.name = PACMAN
        self.color = YELLOW
        self.direction = LEFT
        self.setBetweenNodes(LEFT)

    def update(self, delta):	
        #update position
        self.position += self.directions[self.direction]*self.speed*delta
        direction = self.getValidKey()
        
        #Checks if pacman has reached the destination node yet.
        if self.overshotTarget():
            self.node = self.target
            if self.node.neighbors[PORTAL] is not None:
                self.node = self.node.neighbors[PORTAL]
            
            self.target = self.getNewTarget(direction)
            if self.target is not self.node:
                self.direction = direction
            else:
                self.target = self.getNewTarget(self.direction)

            if self.target is self.node:
                self.direction = STOP
            self.setPosition()
        else: 
            if self.oppositeDirection(direction):
                self.reverseDirection()

    def eatPellets(self, pelletList):
        #RA + RB > D, -> collision
        for pellet in pelletList:
            if self.collideCheck(pellet):
                return pellet
        return None

    #checks collision of two circles by comparting radii.
    def collideCheck(self, other):
        d = self.position - other.position
        dSquared = d.magnitude_squared()
        rSquared = (other.radius+self.collideRadius)**2
        if dSquared <= rSquared:
            return True
        return False
    
    def collideGhost(self, ghost):
        return self.collideCheck(ghost)

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