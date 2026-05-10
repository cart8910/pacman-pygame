#Libs
import pygame
from pygame.locals import *
from pygame.math import Vector2
import os

#Local files
from constants import *
from pacman import Pacman

class MainGame(object):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREENSIZE, 0, 32)
        self.background = None

        #this ensures we load from the Assets folder even if the project is run from another working dir.
        image_path = os.path.join(os.path.dirname(__file__), "Assets", "maze.bmp")

        self.bg_image = pygame.image.load(image_path)
        self.bg_image = pygame.transform.scale(self.bg_image, SCREENSIZE)

        self.clock = pygame.time.Clock()

    def setBackground(self):
        self.background = self.bg_image

    def startGame(self):
        self.setBackground()
        self.pacman = Pacman()

    def update(self):
        delta = self.clock.tick(30) / 1000.0 #time since last frame in seconds
        
        self.pacman.update(delta)

        self.checkEvents()
        self.render()


    def checkEvents(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()

    def render(self):
        self.screen.blit(self.background, (0, 0))
        self.pacman.render(self.screen)
        
        pygame.display.update()


#start execution
if __name__ == "__main__":
    game = MainGame()
    game.startGame()
    while True:
        game.update()
        