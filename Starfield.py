import random
from GameObject import *

class Starfield(GameObject):
    def __init__(self, name, nStars):
        GameObject.__init__(self, name)

        self.nStars = nStars
        self.starPos = []
        self.starColor = []
        for i in range(0, nStars):
            self.starPos.append(((int)(random.uniform(0, 1280)), (int)(random.uniform(0, 720))))
            r = (int)(random.uniform(64, 255))
            self.starColor.append((r, r, r))            

    def Render(self, screen):
        for i in range(0, self.nStars):
            screen.set_at(self.starPos[i], self.starColor[i])

