#Libs
import pygame
from pygame.locals import *
from pygame.math import Vector2
import os

#Local files
from constants import *
from pacman import Pacman
from nodes import NodeGroup
from pellets import PelletGroup
from ghosts import Ghost

#Main game object.
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
        self.nodes = NodeGroup(os.path.join(os.path.dirname(__file__), "maze1.txt"))
        
        #manually add portals
        self.nodes.setPortalPair((0,17), (27,17))
        
        self.pacman = Pacman(self.nodes.getStartTempNode())
        self.pellets = PelletGroup(os.path.join(os.path.dirname(__file__), "maze1.txt"))
        self.ghost = Ghost(self.nodes.getStartTempNode())
    def update(self):
        delta = self.clock.tick(30) / 1000.0 #time since last frame in seconds
        
        self.pacman.update(delta)
        self.ghost.update(delta)
        self.pellets.update(delta)

        self.checkPelletEvents()
        self.checkEvents()
        self.render()

    def checkEvents(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()

    def checkPelletEvents(self):
        pellet = self.pacman.eatPellets(self.pellets.pelletList)
        if pellet:
            self.pellets.numEaten += 1
            self.pellets.pelletList.remove(pellet)

    def render(self):
        self.screen.blit(self.background, (0, 0))
        self.nodes.render(self.screen)

        self.pellets.render(self.screen)
        self.pacman.render(self.screen)
        self.ghost.render(self.screen)

        pygame.display.update()


#start execution
if __name__ == "__main__":
    game = MainGame()
    game.startGame()
    while True:
        game.update()
        