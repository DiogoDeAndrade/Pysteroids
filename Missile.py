from pygame.math import Vector2

import Engine.FX

from Ship import *
from GameDefs import *

class Missile(Ship):
    """Missile class.
    This class encapsulates the functionality of a homing missile
    """
    def __init__(self, name, target, tag):
        """
        
        Arguments:
            name {string} -- Name of this missile

            target {GameObject} -- GameObject to track

            tag {string} -- tag for this missile
        """
        Ship.__init__(self, name)

        # Create visual objects (model and trail)
        self.gfx = WireMesh.get_model("Missile")
        self.trail = Trail("MissileTrail", 2, Color(0, 1, 1, 1), Color(0, 0, 0, 0), 5, self, "TrailAnchor0", 0.1)
        
        self.collider = Circle2d(Vector2(0,0), self.gfx.get_radius())
        self.radius = self.gfx.get_radius()

        self.target = target
        self.max_rotation_angle = 450
        self.life = 7.5

        self.score_to_add = 150

        self.tags.append("Missile")
        self.tags.append(tag)
        
    def update(self, delta_time):
        """Update position of the missile, and handle lifetime
        
        Arguments:
            delta_time {float} -- Time to elapse in seconds
        """
        # If there is no target (if it has been destroyed), detonate missile
        if (self.target == None):
            self.explode()
            return

        # Update the trail effect
        self.trail.update(delta_time)

        # Aim at target
        desired_direction = (self.target.position - self.position).normalize()
        current_direction = self.get_direction_vector()

        # Get desired angle of rotation
        angle = math.degrees(math.acos(current_direction.dot(desired_direction))) * delta_time
        # Get sign of rotation
        if (self.get_right_vector().dot(desired_direction) < 0):
            angle = -angle

        angle = max(min(angle, self.max_rotation_angle), -self.max_rotation_angle)

        self.rotation = self.rotation + angle

        self.velocity = self.get_direction_vector() * 150

        Ship.update(self, delta_time)

        # Destroy missile when time expires
        self.life = self.life - delta_time
        if (self.life < 0):
            self.explode()

    def render(self, screen):
        """Renders the missile
        
        Arguments:
            screen {int} -- Display surface handle
        """
        Ship.render(self, screen)

        # Draw graphical object
        self.gfx.drawPRS(screen, self.position, self.rotation, self.scale)

        # Render trail effect
        self.trail.render(screen)

    def on_destroy(self):
        """Bypass explosion effect of Ship, just straight up destroy the object"""
        Engine.GameObject.on_destroy(self)

