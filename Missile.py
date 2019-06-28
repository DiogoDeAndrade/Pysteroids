from WireMesh import *
from Ship import *
from GameDefs import *
from Trail import *
from pygame.math import Vector2

class Missile(Ship):
    def __init__(self, name, target, tag):
        Ship.__init__(self, name)

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
        if (self.target == None):
            self.explode()
            return

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

        self.life = self.life - delta_time
        if (self.life < 0):
            self.explode()

    def render(self, screen):
        Ship.render(self, screen)

        self.gfx.drawPRS(screen, self.position, self.rotation, self.scale)

        self.trail.render(screen)

    def on_destroy(self):
        GameObject.on_destroy(self)

