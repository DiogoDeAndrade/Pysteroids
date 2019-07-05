import enum

from Engine import *
from Engine.Color import Color

class FadeMethod(enum.Enum): 
    Shrink = 0
    Color = 1

class ExplosionParticle:
    def __init__(self, p1, p2, from_center, speed, rotation):
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
    def __init__(self, original_mesh, original_pos, original_rotation, original_scale, from_center, min_speed, max_speed, min_rotation, max_rotation):

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
        return ((self.duration == 0) or (self.time < self.duration))

    def render(self, screen):
        self.gfx.drawPRS(screen, self.position, self.rotation, self.scale)

