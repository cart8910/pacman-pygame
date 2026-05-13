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
from ghosts import GhostGroup

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
        
        #Manually add the home for the ghosts
        homekey = self.nodes.createHomeNodes(11.5, 14)
        self.nodes.connectHomeNodes(homekey, (12,14), LEFT)
        self.nodes.connectHomeNodes(homekey, (15,14), RIGHT)

        self.pacman = Pacman(self.nodes.getNodeFromTiles(15, 26))
        self.pellets = PelletGroup(os.path.join(os.path.dirname(__file__), "maze1.txt"))
        self.ghosts = GhostGroup(self.nodes.getStartTempNode(), self.pacman)
        
        self.ghosts.blinky.setStartNode(self.nodes.getNodeFromTiles(2+11.5, 0+14))
        self.ghosts.pinky.setStartNode(self.nodes.getNodeFromTiles(2+11.5, 3+14))
        self.ghosts.inky.setStartNode(self.nodes.getNodeFromTiles(0+11.5, 3+14))
        self.ghosts.clyde.setStartNode(self.nodes.getNodeFromTiles(4+11.5, 3+14))

        #this is hardcoded for now
        self.ghosts.setSpawnNode(self.nodes.getNodeFromTiles(2+11.5, 3+14))

    def update(self):
        #update delta
        delta = self.clock.tick(30) / 1000.0 #time since last frame in seconds
        
        #tick the game
        self.pacman.update(delta)
        self.ghosts.update(delta)
        self.pellets.update(delta)

        #check logic
        self.checkPelletEvents()
        self.checkGhostEvents()
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
            if pellet.name == POWERPELLET:
               self.ghosts.startFright()

    def checkGhostEvents(self):
        for ghost in self.ghosts:
            if self.pacman.collideGhost(ghost):
                if ghost.mode.current is FRIGHT:
                    ghost.startSpawn()

    def render(self):
        self.screen.blit(self.background, (0, 0))
        self.nodes.render(self.screen)

        self.pellets.render(self.screen)
        self.pacman.render(self.screen)
        self.ghosts.render(self.screen)

        pygame.display.update()


#start execution
if __name__ == "__main__":
    game = MainGame()
    game.startGame()
    while True:
        game.update()
        
        