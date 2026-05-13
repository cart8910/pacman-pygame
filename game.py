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
from pause import Pause

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

        self.level = 0
        self.lives = 5
        
        self.pause = Pause(True)

    def setBackground(self):
        self.background = self.bg_image

    #reset game state
    def restartGame(self):
        self.lives = 5
        self.level = 0
        self.pause.paused = True
        self.startGame()

    def resetLevel(self):
        self.pause.paused = True
        self.pacman.reset()
        self.ghosts.reset()


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

    def nextLevel(self):
        self.showEntities()
        self.level += 1
        self.pause.paused = True
        self.startGame()


    def update(self):
        #update delta
        delta = self.clock.tick(30) / 1000.0 #time since last frame in seconds
        self.pellets.update(delta)

        if not self.pause.paused:
            #tick the game
            self.pacman.update(delta)
            self.ghosts.update(delta)

            #check logic
            self.checkPelletEvents()
            self.checkGhostEvents()
        
        afterPauseMethod = self.pause.update(delta)
        if afterPauseMethod is not None:
            afterPauseMethod()

        self.checkEvents()
        
        self.render()

    def checkEvents(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if self.pacman.alive: #Don't pause the game while pacman is dying
                        self.pause.setPause(playerPaused=True)
                        if not self.pause.paused:
                            self.showEntities()
                        else:
                            self.hideEntities()


    def checkPelletEvents(self):
        pellet = self.pacman.eatPellets(self.pellets.pelletList)
        if pellet:
            self.pellets.numEaten += 1
            self.pellets.pelletList.remove(pellet)
            if pellet.name == POWERPELLET:
               self.ghosts.startFright()
            
            if self.pellets.isEmpty():
                self.hideEntities()
                self.pause.setPause(pauseTime=3, func=self.nextLevel)

    def checkGhostEvents(self):
        for ghost in self.ghosts:
            if self.pacman.collideGhost(ghost):
                if ghost.mode.current is FRIGHT:
                    self.pacman.visible = False
                    ghost.visible = False
                    self.pause.setPause(pauseTime=1, func=self.showEntities)
                    ghost.startSpawn()

                elif ghost.mode.current is not SPAWN:
                     if self.pacman.alive:
                         self.lives -=  1
                         self.pacman.die()
                         self.ghosts.hide()
                         if self.lives <= 0:
                             self.pause.setPause(pauseTime=3, func=self.restartGame)
                         else:
                             self.pause.setPause(pauseTime=3, func=self.resetLevel)
    
    def showEntities(self):
        self.pacman.visible = True
        self.ghosts.show()

    def hideEntities(self):
        self.pacman.visible = False
        self.ghosts.hide()

    def render(self):
        self.screen.blit(self.background, (0, 0))
        
        #View node paths
        #self.nodes.render(self.screen)

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
        
        