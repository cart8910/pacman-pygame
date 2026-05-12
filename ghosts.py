import pygame
from pygame.locals import *
from pygame.math import Vector2
from constants import *
from entity import Entity
from modes import ModeController

class Ghost(Entity):
    def __init__(self, node, pacman=None):
        Entity.__init__(self, node)
        self.name = GHOST
        self.points = 200
        self.goal = Vector2()
        self.directionMethod = self.goalDirection
        self.pacman = pacman #Track pacman entity on spawn
        self.mode = ModeController(self)

    def update(self, delta):
        self.mode.update(delta)
        if self.mode.current is SCATTER:
            self.scatter()
        elif self.mode.current is CHASE:
            self.chase()
        Entity.update(self, delta)

    def scatter(self):
        self.goal = Vector2()

    def chase(self):
        self.goal = self.pacman.position