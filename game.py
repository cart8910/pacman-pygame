#Libs
import pygame
from pygame.locals import *
from pygame.math import Vector2
import os

#Local files
from constants import *
from pacman import Pacman
from nodes import NodeGroup

class MainGame(object):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREENSIZE, 0, 32)
        self.background = None

        #this ensures we load from the Assets folder even if the project is run from another working dir.
        assets_path = os.path.join(os.path.dirname(__file__), "Assets")

        #bg image
        self.bg_image = pygame.image.load(os.path.join(assets_path, "maze.bmp"))
        self.bg_image = pygame.transform.scale(self.bg_image, SCREENSIZE)

        self.clock = pygame.time.Clock()

    def setBackground(self):
        self.background = self.bg_image

    def startGame(self):
        self.setBackground()
        self.nodes = NodeGroup()
        self.nodes.setupTestNodes()

        self.pacman = Pacman(self.nodes.nodeList[0])

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
        self.nodes.render(self.screen)

        self.pacman.render(self.screen)
        
        pygame.display.update()


#start execution
if __name__ == "__main__":
    game = MainGame()
    game.startGame()
    while True:
        game.update()
        