import pygame
from Color import *

class Shockwave:
    def __init__(self, position, duration, radius, colors):
        self.position = position
        self.duration = duration
        self.radius = radius
        self.colors = colors
        self.time = 0
        self.width = 1

    def IsAlive(self):
        return ((self.duration == 0) or (self.time < self.duration))

    def Update(self, delta_time):
        self.time = self.time + delta_time
 
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
