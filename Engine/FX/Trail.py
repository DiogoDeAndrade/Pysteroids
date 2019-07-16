"""Trail effect

Usage example:
```
    # This will spawn a trail that will trail for two seconds, going from cyan to black.
    # It will be 5 pixels wide, following <target_object>'s on his "TrailAnchor0" mountpoint.
    # It will spawn a new segment every 100 ms
    trail = Trail("MissileTrail", 2, Color(0, 1, 1, 1), Color(0, 0, 0, 0), 5, target_object, "TrailAnchor0", 0.1)
```
"""

import pygame

from Engine import *

class TrailParticle:
    """Trail particle structure.

    Used internally to keep track on where the trail should be."""
    def __init__(self, pos, color):
        """Initializes a trail particle.
        
        Arguments:
            pos {Vector2} -- Position of the trail at this time
            color {Color} -- Color of the trail
        """
        self.pos = pos
        self.color = color
        self.time = 0

class Trail(GameObject):
    """Trail object"""
    def __init__(self, name, duration, colorStart, colorEnd, width, target, mountpoint, tick_time):
        """
        
        Arguments:
            name {string} -- Name of the object. It can be duplicated, there's no validation/enforcing, but it's usually better to have unique names to quickly identify relevant objects while debugging.

            duration {float} -- Duration of the trail (defines the length of the trail)

            colorStart {Color} -- Start color of the trail

            colorEnd {Color} -- End color of the trail

            width {int} -- Width of the trail

            target {GameObject} -- Object to track

            mountpoint {string} -- Mountpoint in the object to track

            tick_time {float} -- Time between trail segments
        """
        GameObject.__init__(self, name)

        self.duration = duration
        self.start_color = colorStart
        self.end_color = colorEnd
        self.width = width
        self.target = target
        self.mountpoint = mountpoint
        self.tick_time = self.tick = tick_time

        self.points = []

    def update(self, delta_time):
        """Updates the trail
        
        Arguments:
            delta_time {float} -- Time to elapse in seconds
        """

        for pt in self.points:
            pt.time = pt.time + delta_time
            pt.color = Color.interpolate(self.start_color, self.end_color, pt.time / self.duration).tuple()        

        for index in range(len(self.points)-1, -1, -1):
            if (self.points[index].time > self.duration):
                del(self.points[index])

        self.tick = self.tick + delta_time
        if (self.tick > self.tick_time):
            self.points.append(TrailParticle(self.target.get_mountpoint(self.mountpoint)[0], self.start_color))
            self.tick = 0
        elif (len(self.points) > 0):
            self.points[len(self.points) - 1].pos = self.target.get_mountpoint(self.mountpoint)[0]


    def render(self, screen):
        """Renders the trail
        
        Arguments:
            screen {int} -- Display surface handle
        """
        for i in range(0, len(self.points) - 1):
            c = self.points[i].color
            p1 = self.points[i].pos
            p2 = self.points[i + 1].pos
            pygame.draw.line(screen, c, p1, p2, self.width)
