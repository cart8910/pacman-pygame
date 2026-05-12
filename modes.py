
from constants import *

#The mode that a ghost has
class MainMode(object):
    def __init__(self):
        self.timer = 0
        self.scatter()

    def update(self, delta):
        self.timer += delta
        if self.timer >= self.time:
            if self.mode is SCATTER:
                self.chase()
            elif self.mode is CHASE:
                self.scatter()

    def scatter(self):
        self.mode = SCATTER
        self.time = 7
        self.timer = 0

    def chase(self):
        self.mode = CHASE
        self.time = 20
        self.timer = 0

#manages the entity and the mode
class ModeController(object):
    def __init__(self, entity):
        self.timer = 0
        self.time = None
        self.mainmode = MainMode()
        self.current = self.mainmode.mode
        self.entity = entity 

    def update(self, delta):
        self.mainmode.update(delta)
        if self.current is FRIGHT:
            self.timer += delta
            if self.timer >= self.time:
                self.time = None
                self.entity.normalMode()
                self.current = self.mainmode.mode
        else:
            self.current = self.mainmode.mode

    def setFrightMode(self):
        if self.current in [SCATTER, CHASE]:
            self.timer = 0
            self.time = 7
            self.current = FRIGHT
        elif self.current is FRIGHT: #If a ghost is already frightened, it won't go back again
            self.timer = 0