import pygame
from pygame.math import Vector2

import Engine

class Laser(Engine.GameObject):
    def __init__(self, tag, color, width, length, position, velocity, time_to_live):
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
        self.position = self.position + self.velocity * delta_time

        self.time_to_live = self.time_to_live - delta_time
        if (self.time_to_live <= 0):
            self.destroy()

    def render(self, screen):
        length = min((self.position - self.start_position).magnitude(), self.length)
        pygame.draw.line(screen, self.color, self.position, self.position - self.direction * length, self.width)

    def explode(self):
        pass
