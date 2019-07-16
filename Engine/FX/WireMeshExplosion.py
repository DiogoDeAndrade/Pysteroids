"""A WireMesh explosion is an effect that takes a WireMesh and decomposes it in different lines that go flying off.

Usage example:
```
    # Create the object, with the given mesh, position, rotation and scale
    # This explosion will make the lines shoot outward, at a speed in the range of [150, 300], and rotation [0.5, 3] radius per second
    explosion = Engine.FX.WireMeshExplosion(mesh, position, rotation, scale, True, 150, 300, 0.5, 3)
    # Fading will be done by changing the color
    explosion.fade_method = Engine.FX.FadeMethod.Color
    # Lines will start yellow, then go redish, then go fully black
    explosion.colors = [Color(1.0, 1.0, 0.0, 1.0), Color(1.0, 0.0, 0.0, 1.0), Color(0.0, 0.0, 0.0, 1.0), Color(0.0, 0.0, 0.0, 0.0)]
    # Explosion will last two seconds
    explosion.duration = 2
```

"""
import enum

from Engine import *
from Engine.Color import Color

class FadeMethod(enum.Enum): 
    """How to fade out each line"""
    Shrink = 0
    """Each line gets smaller relative to its center"""
    Color = 1
    """The color will fade out"""

class ExplosionParticle:
    """Each line segment is a ExplosionParticle.

    This is used internally."""
    def __init__(self, p1, p2, from_center, speed, rotation):
        """        
        
        Arguments:
            p1 {Vector2} -- First vertex of the line

            p2 {Vector2} -- Second vertex of the line

            from_center {bool} -- Defines if the velocity vector is relative to the center of the line, or the perpendicular to the line segment

            speed {float} -- Speed of this line segment

            rotation {float} -- Rotation speed of this line segment
        """
        self.center = (p1 + p2) * 0.5
        self.p1 = p1 - self.center
        self.p2 = p2 - self.center
        self.d1 = self.p1.magnitude()
        self.p1.normalize_ip()
        self.d2 = self.p2.magnitude()
        self.p2.normalize_ip()
        self.velocity = (p2 - p1).normalize()
        if (from_center):
            self.velocity = self.center.normalize() * speed
        else:
            self.velocity = Vector2(-self.velocity.y, self.velocity.x) * speed
        self.rotation = rotation

class WireMeshExplosion(GameObject):
    """WireMeshExplosion class"""
    def __init__(self, original_mesh, original_pos, original_rotation, original_scale, from_center, min_speed, max_speed, min_rotation, max_rotation):
        """        
        Arguments:
            original_mesh {WireMesh} -- Original WireMesh to create explosion from. At time = 0, this object and the WireMesh will be visually the same.

            original_pos {Vector2} -- Position of the original WireMesh at the moment of the explosion

            original_rotation {float} -- Rotation of the original WireMesh at the moment of the explosion

            original_scale {Vector2} -- Scale of the original WireMesh at the moment of the explosion

            from_center {bool} -- Defines if the velocity vector is relative to the center of the line, or the perpendicular to the line segment

            min_speed {float} -- Minimum speed of each segment

            max_speed {float} -- Maximum speed of each segment

            min_rotation {float} -- Minimum rotation speed of each segment (radians/sec)

            max_rotation {float} -- Maximum rotation speed of each segment (radians/sec)
        """
        GameObject.__init__(self, "")

        # Create a copy of the mesh
        self.gfx = WireMesh.copy(original_mesh)
        self.gfx.apply_transform()
        self.gfx.convert_to_unindexed_line_list()
        self.gfx.override_color_enable = True
        self.gfx.override_color = (0, 255, 0)
        self.position = original_pos
        self.rotation = original_rotation
        self.scale = original_scale
        self.line_particle = []
        for vertex_index in range(0, len(self.gfx.vertex), 2):
            p1 = self.gfx.vertex[vertex_index]
            p2 = self.gfx.vertex[vertex_index + 1]
            tmp = ExplosionParticle(p1, p2, from_center, random.uniform(min_speed, max_speed), random.uniform(min_rotation, max_rotation))
            self.line_particle.append(tmp)

        self.fade_method = FadeMethod.Shrink
        self.duration = 0
        self.time = 0
        self.colors = []
        self.drag = 1

    def update(self, delta_time):
        """Updates the explosion effect.
        
        Arguments:
            delta_time {float} -- Elapsed time in seconds
        """
        particle_index = 0
        t = self.time / self.duration
        for vertex_index in range(0, len(self.gfx.vertex), 2):
            particle_prop = self.line_particle[particle_index]
            delta_pos =  particle_prop.velocity * delta_time

            p1 = particle_prop.p1
            p2 = particle_prop.p2

            s = math.sin(particle_prop.rotation * delta_time)
            c = math.cos(particle_prop.rotation * delta_time)

            p1 = Vector2(c * p1.x - s * p1.y, s * p1.x + c * p1.y)
            p2 = Vector2(c * p2.x - s * p2.y, s * p2.x + c * p2.y)
            
            particle_prop.p1 = p1
            particle_prop.p2 = p2

            d1 = particle_prop.d1
            d2 = particle_prop.d2

            if (self.duration > 0):
                if (self.fade_method == FadeMethod.Shrink):
                    d1 = (1 - t) * d1
                    d2 = (1 - t) * d2

            particle_prop.center = particle_prop.center + delta_pos
            self.gfx.vertex[vertex_index] = p1 * d1 + particle_prop.center
            self.gfx.vertex[vertex_index + 1] = p2 * d2 + particle_prop.center
            particle_prop.velocity = particle_prop.velocity * self.drag

            particle_index = particle_index + 1

        if (self.duration > 0):
            if (self.fade_method == FadeMethod.Color):
                self.gfx.override_color = Color.interpolate_with_array(self.colors, t).tuple()

        self.time = self.time + delta_time

        if (not self.is_alive()):
            Scene.main.remove(self)

    def is_alive(self):
        """Checks if the explosion is still alive, i.e. any particle is still alive, and if the duration has elapsed
        
        Returns:
            bool -- True if the explosion is alive
        """
        return ((self.duration == 0) or (self.time < self.duration))

    def render(self, screen):
        """Renders the explosion
        
        Arguments:
            screen {int} -- Display surface handle
        """
        self.gfx.drawPRS(screen, self.position, self.rotation, self.scale)

