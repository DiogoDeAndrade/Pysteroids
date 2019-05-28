import math
from pygame.math import Vector2

class GameObject:
    def __init__(self, name):
        self.name = name
        self.position = Vector2(640, 360)
        self.rotation = 0
        self.scale = Vector2(1,1)

    def Update(self, delta_time):
        pass

    def Render(self, screen):
        pass

    def GetDirectionVector(self):
        # Rotation of 0 means pointing up
        angle = math.radians(self.rotation)
        return Vector2(math.sin(angle), -math.cos(angle))

