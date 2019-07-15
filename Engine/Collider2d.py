"""Bounding surface classes"""
import enum
from pygame import Vector2

class ColliderType2d(enum.Enum): 
    """Type of collider. Currently only circle is supported."""
    circle = 0
    """Collider is a circle"""

class Collision2d:
    """Structure to hold the result of a collision.

    It stores two objects."""
    def __init__(self, obj1, obj2):
        self.obj1 = obj1
        self.obj2 = obj2

class Collider2d:
    """Collider base class."""

    def intersects(self, other_collider):
        """Checks collision between this collider and another one.
        
        Arguments:
            other_collider {Collider2d} -- The other collider to detect collision with
        
        Returns:
            bool -- True if there is a collision, false otherwise
        """
        if (self.type == ColliderType2d.circle):
            return self.intersects_circle(other_collider)
        
        return False

    def intersects_circle(self, other_collider):
        """Checks collision between this circle collider and another one.
        
        Arguments:
            other_collider {Collider2d} -- The other collider to detect collision with
        
        Returns:
            bool -- True if there is a collision, false otherwise
        """
        if (other_collider.type == ColliderType2d.circle):
            return self.intersects_circle_circle(other_collider)
        
        return False

    def intersects_circle_circle(self, other_collider):
        """Checks collision between this circle collider and another circle collider.
        
        Arguments:
            other_collider {Circle2d} -- The other circle collider to detect collision with
        
        Returns:
            bool -- True if there is a collision, false otherwise
        """
        vector = (self.position + self.offset) - (other_collider.position + other_collider.offset)
        dist = vector.magnitude()

        if (dist < self.radius + other_collider.radius):
            return True
        
        return False


class Circle2d(Collider2d):
    """Circle collider class"""
    def __init__(self, offset, radius):
        """        
        Arguments:
            offset {Vector2} -- Center offset relative to the owner's pivot
            
            radius {float} -- Radius of the circle
        """
        self.type = ColliderType2d.circle
        self.radius = radius
        self.offset = offset
        self.position = Vector2(0,0)
        
    