import pygame
from Color import *
from Scene import *
from GameObject import *

class Shockwave(GameObject):
    def __init__(self, position, duration, radius, colors):
        GameObject.__init__(self, "")

        self.position = position
        self.duration = duration
        self.radius = radius
        self.colors = colors
        self.time = 0
        self.width = 1
        self.tags.append("Shockwave");

    def IsAlive(self):
        return ((self.duration == 0) or (self.time < self.duration))

    def Update(self, delta_time):
        self.time = self.time + delta_time

        if (not self.IsAlive()):
            Scene.main.Remove(self)
 
    def Render(self, screen):
        r = (int)(self.radius)
        t = 0
        if (self.duration > 0):
            t = self.time / self.duration
            r = (int)(self.radius * t)
        
        pos = ((int)(self.position.x), (int)(self.position.y))

        color = Color.InterpolateWithArray(self.colors, t)

        if (r > self.width):
            pygame.draw.circle(screen, color.tuple(), pos, r, self.width)
