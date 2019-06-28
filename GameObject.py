import math
from pygame.math import Vector2
from Scene import * 
from Collider2d import *

class GameObject:
    def __init__(self, name):
        self.name = name
        self.position = Vector2(640, 360)
        self.rotation = 0
        self.scale = Vector2(1,1)
        self.tags = [ "GameObject" ]
        self.collider = Circle2d(Vector2(0,0), 1)

    def get_direction_vector(self):
        # Rotation of 0 means pointing up
        angle = math.radians(self.rotation)
        return Vector2(math.sin(angle), -math.cos(angle))

    def get_right_vector(self):
        angle = math.radians(self.rotation + 90)
        return Vector2(math.sin(angle), -math.cos(angle))

    def get_mountpoint(self, name):
        if (self.gfx == None):
            return Vector2(self.position)

        return self.gfx.get_mountpointPRS(name, self.position, self.rotation, self.scale)

    def destroy(self):
        Scene.main.remove(self)
        self.on_destroy()

    def get_tags(self):
        return self.tags

    def intersects(self, other_object):
        if (self.collider == None):
            return False

        self.collider.position = self.position

        if (isinstance(other_object, GameObject)):
            if (other_object.collider == None):
                return False

            other_object.collider.position = other_object.position

            if (self.collider.intersects(other_object.collider)):
                return True

        elif (isinstance(other_object, Collider2d)):

            if (self.collider.intersects(other_object)):
                return True

        return False

    def on_destroy(self):
        pass
