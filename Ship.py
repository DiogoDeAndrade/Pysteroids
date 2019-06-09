from GameObject import *
from WireMeshExplosion import *
from Shockwave import *
from ParticleSystem import *

class Ship(GameObject):
    def __init__(self, name):
        GameObject.__init__(self, name)

        self.acceleration = 200.0
        self.break_acceleration = 100.0
        self.velocity = Vector2(0,0)
        self.maxVelocity = 200.0
        self.drag = 0.75
        self.radius = 20

        self.tags.append("Ship")

    def Update(self, delta_time):
        GameObject.Update(self, delta_time)

        if (self.drag > 0):
            self.AddVelocity(-self.velocity * self.drag * delta_time)

        self.position += self.velocity * delta_time        

    def AddVelocity(self, velocity):
        self.velocity += velocity

        if (self.velocity.magnitude() > self.maxVelocity):
            self.velocity = self.velocity.normalize() * self.maxVelocity

    def Explode(self):
        explosion = WireMeshExplosion(self.gfx, self.position, self.rotation, self.scale, True, 150, 300, 0.5, 3)
        explosion.fadeMethod = FadeMethod.Color
        explosion.colors = [Color(1.0, 1.0, 0.0, 1.0), Color(1.0, 0.0, 0.0, 1.0), Color(0.0, 0.0, 0.0, 1.0), Color(0.0, 0.0, 0.0, 0.0)]
        explosion.duration = 2

        shockwave = Shockwave(self.position, 0.75, 200, [Color(1.0, 1.0, 0.0, 1.0), Color(1.0, 0.0, 0.0, 1.0), Color(0.0, 0.0, 0.0, 1.0), Color(0.0, 0.0, 0.0, 0.0)])

        particle_system = ParticleSystem(self.position)
        particle_system.colorOverTime = [Color(1.0, 1.0, 0.0, 1.0), Color(1.0, 0.0, 0.0, 1.0), Color(0.0, 0.0, 0.0, 1.0), Color(0.0, 0.0, 0.0, 0.0)]
        particle_system.startSpeed = (50, 100)
        particle_system.particleLife = (2, 4)
        particle_system.drag = 0.995
        particle_system.rate = 0
        particle_system.Spawn(50)

        Scene.main.Add(explosion)
        Scene.main.Add(shockwave)
        Scene.main.Add(particle_system)

        self.Destroy()
