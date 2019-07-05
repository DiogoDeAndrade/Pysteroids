import pygame

from Engine import *
from Engine.Color import Color

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

    def is_alive(self):
        return ((self.duration == 0) or (self.time < self.duration))

    def update(self, delta_time):
        self.time = self.time + delta_time

        if (not self.is_alive()):
            Scene.main.remove(self)
 
    def render(self, screen):
        r = (int)(self.radius)
        t = 0
        if (self.duration > 0):
            t = self.time / self.duration
            r = (int)(self.radius * t)
        
        pos = ((int)(self.position.x), (int)(self.position.y))

        color = Color.interpolate_with_array(self.colors, t)

        if (r > self.width):
            pygame.draw.circle(screen, color.tuple(), pos, r, self.width)
