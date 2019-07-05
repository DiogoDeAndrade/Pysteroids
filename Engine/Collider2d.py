import enum
from pygame import Vector2

class ColliderType2d(enum.Enum): 
    circle = 0

class Collision2d:
    def __init__(self, obj1, obj2):
        self.obj1 = obj1
        self.obj2 = obj2

class Collider2d:
    def intersects(self, other_collider):
        if (self.type == ColliderType2d.circle):
            return self.intersects_circle(other_collider)
        
        return False

    def intersects_circle(self, other_collider):
        if (other_collider.type == ColliderType2d.circle):
            return self.intersects_circle_circle(other_collider)
        
        return False

    def intersects_circle_circle(self, other_collider):
        vector = (self.position + self.offset) - (other_collider.position + other_collider.offset)
        dist = vector.magnitude()

        if (dist < self.radius + other_collider.radius):
            return True
        
        return False


class Circle2d(Collider2d):
    def __init__(self, offset, radius):
        self.type = ColliderType2d.circle
        self.radius = radius
        self.offset = offset
        self.position = Vector2(0,0)
        
    