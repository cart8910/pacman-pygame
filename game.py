import pygame
from pygame.locals import *
from pygame.math import Vector2
from constants import *

class MainGame(object):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREENSIZE, 0, 32)
        self.background = None

        self.clock = pygame.time.Clock()

    def setBackground(self):
        self.background = pygame.surface.Surface(SCREENSIZE).convert()
        self.background.fill(BLACK)

    def startGame(self):
        self.setBackground()

    def update(self):
        delta = self.clock.tick(30) / 1000.0 #time since last frame in seconds
        
        self.checkEvents()
        self.render()


    def checkEvents(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()

    def render(self):
        pygame.display.update()


#start execution
if __name__ == "__main__":
    game = MainGame()
    game.startGame()
    while True:
        game.update()
        