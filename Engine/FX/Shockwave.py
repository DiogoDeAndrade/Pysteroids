"""Shockwave effect

The shockwave effect is just a growing cirlce that changes color.

Usage example:
```
    # Spawn a shockwave at the given position, lasting for 750 ms, and 200 pixels wide.
    # The color will go from a yellow to a red, then to a black.
    shockwave = Engine.FX.Shockwave(position, 0.75, 200, [Color(1.0, 1.0, 0.0, 1.0), Color(1.0, 0.0, 0.0, 1.0), Color(0.0, 0.0, 0.0, 1.0), Color(0.0, 0.0, 0.0, 0.0)])
```
"""
import pygame

from Engine import *
from Engine.Color import Color

class Shockwave(GameObject):
    """Shockwave effect class"""
    def __init__(self, position, duration, radius, colors):
        """
        
        Arguments:
            position {Vector2} -- Position of the shockwave

            duration {float} -- Duration (in seconds)

            radius {float} -- Maximum radius

            colors {Color[]} -- Array of colors for the shockwave
        """
        GameObject.__init__(self, "")

        self.position = position
        self.duration = duration
        self.radius = radius
        self.colors = colors
        self.time = 0
        self.width = 1
        self.tags.append("Shockwave")

    def is_alive(self):
        """Check if the shockwave is still alive
        
        Returns:
            bool -- Check if the shockwave is still alive
        """
        return (self.time < self.duration)

    def update(self, delta_time):
        """Updates the shockwave
        
        Arguments:
            delta_time {float} -- Elapsed time from last frame (in seconds)
        """
        self.time = self.time + delta_time

        if (not self.is_alive()):
            Scene.main.remove(self)
 
    def render(self, screen):
        """Renders the shockwave
        
        Arguments:
            screen {int} -- Display surface handle
        """
        r = (int)(self.radius)
        t = 0
        if (self.duration > 0):
            t = self.time / self.duration
            r = (int)(self.radius * t)
        
        pos = ((int)(self.position.x), (int)(self.position.y))

        color = Color.interpolate_with_array(self.colors, t)

        if (r > self.width):
            pygame.draw.circle(screen, color.tuple(), pos, r, self.width)
