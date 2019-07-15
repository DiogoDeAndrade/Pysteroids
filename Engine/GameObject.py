"""GameObject class.

The GameObject is the base class of all interactive objects in the engine.

It implements some basic properties, like position, rotation and scale, besides a collider and tags.
"""
import math
from pygame.math import Vector2

from Engine.Collider2d import *
from Engine.Scene import *

class GameObject:
    def __init__(self, name):
        """Initializes a GameObject, with a given name.
        
        Arguments:
            name {string} -- Name of the object. It can be duplicated, there's no validation/enforcing, but it's usually better to have unique names to quickly identify relevant objects while debugging.
        """
        self.name = name
        self.position = Vector2(640, 360)
        self.rotation = 0
        self.scale = Vector2(1,1)
        self.tags = [ "GameObject" ]
        self.collider = Circle2d(Vector2(0,0), 1)

    def get_direction_vector(self):
        """Returns the direction vector of the GameObject.

        A rotation of 0 degrees means the object is pointing at (0, -1) (it's pointing upwards)
        
        Returns:
            Vector2 -- Direction vector of the object
        """
        # Rotation of 0 means pointing up
        angle = math.radians(self.rotation)
        return Vector2(math.sin(angle), -math.cos(angle))

    def get_right_vector(self):
        """Returns the right vector of the GameObject.

        A rotation of 0 degrees means the object is pointing at (0, -1) (it's pointing upwards), so it's right vector will point to (1, 0)
        
        Returns:
            Vector2 -- Direction vector of the object
        """
        angle = math.radians(self.rotation + 90)
        return Vector2(math.sin(angle), -math.cos(angle))

    def get_mountpoint(self, name):
        """Gets the position of the given mountpoint.

        Currently, mountpoints only work if there's a gfx property on the GameObject that implements a get_mountpointPRS function.
        
        Arguments:
            name {string} -- Name of the mountpoint
        
        Returns:
            Vector2 -- World space position of this mountpoint
        """
        if (self.gfx == None):
            return Vector2(self.position)

        return self.gfx.get_mountpointPRS(name, self.position, self.rotation, self.scale)

    def destroy(self):
        """Destroys this GameObject, removing it from the main scene, and running the on_destroy callback.
        """
        Scene.main.remove(self)
        self.on_destroy()

    def get_tags(self):
        """Returns the tag array of this object.
        
        Returns:
            string[] -- Tag array of this object.
        """
        return self.tags

    def intersects(self, other_object):
        """Checks if this object intersects another object.
        
        Arguments:
            other_object {GameObject / Collider2d} -- Other object or collider to check intersection with.
        
        Returns:
            bool -- True if there is an intersection.
        """
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
        """Callback that gets called when this object is destroyed.
        """
        pass
