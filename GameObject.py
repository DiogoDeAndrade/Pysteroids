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

    def GetDirectionVector(self):
        # Rotation of 0 means pointing up
        angle = math.radians(self.rotation)
        return Vector2(math.sin(angle), -math.cos(angle))

    def GetMountpoint(self, name):
        if (self.gfx == None):
            return Vector2(self.position)

        return self.gfx.GetMountpointPRS(name, self.position, self.rotation, self.scale)

    def Destroy(self):
        Scene.main.Remove(self)
        self.OnDestroy()

    def GetTags(self):
        return self.tags

    def Intersects(self, otherObject):
        if (self.collider == None):
            return False

        if (otherObject.collider == None):
            return False

        self.collider.position = self.position
        otherObject.collider.position = otherObject.position

        if (self.collider.Intersects(otherObject.collider)):
            return True

        return False

    def OnDestroy(self):
        pass
