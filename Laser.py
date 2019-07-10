import pygame
from pygame.math import Vector2

import Engine

class Laser(Engine.GameObject):
    """Laser class.
    This class encapsulates the functionality of a laser shot.
    """
    def __init__(self, tag, color, width, length, position, velocity, time_to_live):
        """
        
        Arguments:
            tag {string} -- tag for this laser

            color {RGB tuple} -- color of the laser

            width {int} -- width of the laser

            length {float} -- length of the laser

            position {Vector2} -- start position of the laser

            velocity {Vector2} -- velocity vector for the laser
            
            time_to_live {float} -- time to live of the laser
        """
        Engine.GameObject.__init__(self, tag)

        self.collider = Engine.Circle2d(Vector2(0,0), width)
        self.start_position = position
        self.position = position
        self.velocity = velocity
        self.direction = velocity.normalize()
        self.color = color
        self.width = width
        self.length = length
        self.time_to_live = time_to_live
        self.tags.append(tag)

    def update(self, delta_time):
        """Updates the laser position and destroys it when the timer runs out.
        
        Arguments:
            delta_time {float} -- Time to elapse in seconds
        """
        self.position = self.position + self.velocity * delta_time

        self.time_to_live = self.time_to_live - delta_time
        if (self.time_to_live <= 0):
            self.destroy()

    def render(self, screen):
        """Renders the laser
        
        Arguments:
            screen {int} -- Display surfer handle
        """
        length = min((self.position - self.start_position).magnitude(), self.length)
        pygame.draw.line(screen, self.color, self.position, self.position - self.direction * length, self.width)

    def explode(self):
        """Explode function - Currently, the laser just disappears without any effects"""
        pass
