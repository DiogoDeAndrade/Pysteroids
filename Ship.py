from GameObject import *
from WireMeshExplosion import *
from Shockwave import *
from ParticleSystem import *
from SoundManager import *

class Ship(GameObject):
    def __init__(self, name):
        GameObject.__init__(self, name)

        self.acceleration = 200.0
        self.break_acceleration = 100.0
        self.velocity = Vector2(0,0)
        self.max_velocity = 200.0
        self.drag = 0.75
        self.radius = 20
        self.thruster_m = self.current_thruster_m = 0
        self.thruster_r = self.current_thruster_r = 0
        self.thruster_l = self.current_thruster_l = 0
        self.gfx = None
        self.thruster_color = (255, 0, 0)
        self.thruster_length = 20
        self.thruster_width = 5
        self.thruster_line_width = 1
        self.thruster_speed = 5
        self.score_to_add = 100

        self.tags.append("Ship")

    def update(self, delta_time):

        if (self.drag > 0):
            self.add_velocity(-self.velocity * self.drag * delta_time)

        self.position += self.velocity * delta_time        

        self.current_thruster_r = self.current_thruster_r + (self.thruster_r - self.current_thruster_r) * (self.thruster_speed * delta_time)
        self.current_thruster_m = self.current_thruster_m + (self.thruster_m - self.current_thruster_m) * (self.thruster_speed * delta_time)
        self.current_thruster_l = self.current_thruster_l + (self.thruster_l - self.current_thruster_l) * (self.thruster_speed * delta_time)

    def add_velocity(self, velocity):
        self.velocity += velocity

        if (self.velocity.magnitude() > self.max_velocity):
            self.velocity = self.velocity.normalize() * self.max_velocity

    def explode(self):
        explosion = WireMeshExplosion(self.gfx, self.position, self.rotation, self.scale, True, 150, 300, 0.5, 3)
        explosion.fade_method = FadeMethod.Color
        explosion.colors = [Color(1.0, 1.0, 0.0, 1.0), Color(1.0, 0.0, 0.0, 1.0), Color(0.0, 0.0, 0.0, 1.0), Color(0.0, 0.0, 0.0, 0.0)]
        explosion.duration = 2

        shockwave = Shockwave(self.position, 0.75, 200, [Color(1.0, 1.0, 0.0, 1.0), Color(1.0, 0.0, 0.0, 1.0), Color(0.0, 0.0, 0.0, 1.0), Color(0.0, 0.0, 0.0, 0.0)])

        particle_system = ParticleSystem(self.position)
        particle_system.color_over_time = [Color(1.0, 1.0, 0.0, 1.0), Color(1.0, 0.0, 0.0, 1.0), Color(0.0, 0.0, 0.0, 1.0), Color(0.0, 0.0, 0.0, 0.0)]
        particle_system.start_speed = (50, 100)
        particle_system.particle_life = (2, 4)
        particle_system.drag = 0.995
        particle_system.rate = 0
        particle_system.spawn(50)

        Scene.main.add(explosion)
        Scene.main.add(shockwave)
        Scene.main.add(particle_system)

        SoundManager.play("Explosion")

        self.destroy()

    def render(self, screen):
        if (self.gfx != None):
            if (self.current_thruster_l > 0.05):
                if (self.gfx.mountpoint_exists("ThrusterL")):
                    mp_pos, mp_dir = self.gfx.get_mountpointPRS("ThrusterL", self.position, self.rotation, self.scale)
                    self.draw_thruster(screen, mp_pos, mp_dir, self.current_thruster_l)
            if (self.current_thruster_m > 0.05):
                if (self.gfx.mountpoint_exists("ThrusterM")):
                    mp_pos, mp_dir = self.gfx.get_mountpointPRS("ThrusterM", self.position, self.rotation, self.scale)
                    self.draw_thruster(screen, mp_pos, mp_dir, self.current_thruster_m)
            if (self.current_thruster_r > 0.05):
                if (self.gfx.mountpoint_exists("ThrusterR")):
                    mp_pos, mp_dir = self.gfx.get_mountpointPRS("ThrusterR", self.position, self.rotation, self.scale)
                    self.draw_thruster(screen, mp_pos, mp_dir, self.current_thruster_r)

    def draw_thruster(self, screen, pos, dir, length):
        perpDir = Vector2(dir.y, -dir.x)
        pygame.draw.line(screen, self.thruster_color, pos + perpDir * self.thruster_width, pos + dir * self.thruster_length * length, self.thruster_line_width)
        pygame.draw.line(screen, self.thruster_color, pos - perpDir * self.thruster_width, pos + dir * self.thruster_length * length, self.thruster_line_width)
