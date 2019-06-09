from Color import *
from WireMesh import *
from Scene import *
from GameObject import *

class FadeMethod(enum.Enum): 
    Shrink = 0
    Color = 1

class ExplosionParticle:
    def __init__(self, p1, p2, fromCenter, speed, rotation):
        self.center = (p1 + p2) * 0.5
        self.p1 = p1 - self.center
        self.p2 = p2 - self.center
        self.d1 = self.p1.magnitude()
        self.p1.normalize_ip()
        self.d2 = self.p2.magnitude()
        self.p2.normalize_ip()
        self.velocity = (p2 - p1).normalize()
        if (fromCenter):
            self.velocity = self.center.normalize() * speed
        else:
            self.velocity = Vector2(-self.velocity.y, self.velocity.x) * speed
        self.rotation = rotation

class WireMeshExplosion(GameObject):
    def __init__(self, original_mesh, original_pos, original_rotation, original_scale, fromCenter, minSpeed, maxSpeed, minRotation, maxRotation):

        GameObject.__init__(self, "")

        # Create a copy of the mesh
        self.gfx = WireMesh.Copy(original_mesh)
        self.gfx.ApplyTransform()
        self.gfx.ConvertToLineList()
        self.gfx.overrideColorEnable = True
        self.gfx.overrideColor = (0, 255, 0)
        self.position = original_pos
        self.rotation = original_rotation
        self.scale = original_scale
        self.line_particle = []
        for vertexIndex in range(0, len(self.gfx.vertex), 2):
            p1 = self.gfx.vertex[vertexIndex]
            p2 = self.gfx.vertex[vertexIndex + 1]
            tmp = ExplosionParticle(p1, p2, fromCenter, random.uniform(minSpeed, maxSpeed), random.uniform(minRotation, maxRotation))
            self.line_particle.append(tmp)

        self.fadeMethod = FadeMethod.Shrink
        self.duration = 0
        self.time = 0
        self.colors = []
        self.drag = 1

    def Update(self, delta_time):
        particleIndex = 0
        t = self.time / self.duration
        for vertexIndex in range(0, len(self.gfx.vertex), 2):
            particle_prop = self.line_particle[particleIndex]
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
                if (self.fadeMethod == FadeMethod.Shrink):
                    d1 = (1 - t) * d1
                    d2 = (1 - t) * d2

            particle_prop.center = particle_prop.center + delta_pos
            self.gfx.vertex[vertexIndex] = p1 * d1 + particle_prop.center
            self.gfx.vertex[vertexIndex + 1] = p2 * d2 + particle_prop.center
            particle_prop.velocity = particle_prop.velocity * self.drag

            particleIndex = particleIndex + 1

        if (self.duration > 0):
            if (self.fadeMethod == FadeMethod.Color):
                self.gfx.overrideColor = Color.InterpolateWithArray(self.colors, t).tuple()

        self.time = self.time + delta_time

        if (not self.IsAlive()):
            Scene.main.Remove(self)

    def IsAlive(self):
        return ((self.duration == 0) or (self.time < self.duration))

    def Render(self, screen):
        self.gfx.DrawPRS(screen, self.position, self.rotation, self.scale)

