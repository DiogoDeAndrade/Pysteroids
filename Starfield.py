import random

import Engine

class Starfield(Engine.GameObject):
    """This object draws some stars on the background."""
    def __init__(self, name, nStars):
        """
        
        Arguments:
            name {string} -- Name of the starfield object
            nStars {int} -- Number of stars to spawn
        """
        Engine.GameObject.__init__(self, name)

        self.nStars = nStars
        self.starPos = []
        self.starColor = []
        for i in range(0, nStars):
            self.starPos.append(((int)(random.uniform(0, 1280)), (int)(random.uniform(0, 720))))
            r = (int)(random.uniform(64, 255))
            self.starColor.append((r, r, r))            

    def render(self, screen):
        """Render the starfield.
        
        Arguments:
            screen {int} -- Display surface handler
        """
        for i in range(0, self.nStars):
            screen.set_at(self.starPos[i], self.starColor[i])

