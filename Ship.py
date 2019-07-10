import pygame
from pygame.math import Vector2

import Engine
import Engine.FX

from Engine.Color import Color

class Ship(Engine.GameObject):
    """The ship is the main class of the game, it encapsulates the asteroids, missiles, enemy and player ships.

    It defines newtonian pseudo-physics: objects have a velocity and move according to it, without any foreign influences.

    The object also considers thrusters (visual effect)."""
    def __init__(self, name):
        """
        
        Arguments:
            name {string} -- Name of the ship
        """
        Engine.GameObject.__init__(self, name)

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
        """Updates the ship position.
        
        Arguments:
            delta_time {float} -- Time to elapse in seconds
        """
        # Drag
        if (self.drag > 0):
            self.add_velocity(-self.velocity * self.drag * delta_time)

        # Update position
        self.position += self.velocity * delta_time        

        # Update thruster power.
        self.current_thruster_r = self.current_thruster_r + (self.thruster_r - self.current_thruster_r) * (self.thruster_speed * delta_time)
        self.current_thruster_m = self.current_thruster_m + (self.thruster_m - self.current_thruster_m) * (self.thruster_speed * delta_time)
        self.current_thruster_l = self.current_thruster_l + (self.thruster_l - self.current_thruster_l) * (self.thruster_speed * delta_time)

    def add_velocity(self, velocity):
        """Changes the velocity of the ship.
        
        Arguments:
            velocity {Vector2} -- Velocity to add to the current velocity.
        """
        self.velocity += velocity

        # Accounts for max. velocity
        if (self.velocity.magnitude() > self.max_velocity):
            self.velocity = self.velocity.normalize() * self.max_velocity

    def explode(self):
        """Makes this ship explode.

        An explosion is the combination of a all the segments that make up the graphics of the ship fly appart, a particle system and a shockwave.

        The object is also removed from the scene and destroyed.
        """
        explosion = Engine.FX.WireMeshExplosion(self.gfx, self.position, self.rotation, self.scale, True, 150, 300, 0.5, 3)
        explosion.fade_method = Engine.FX.FadeMethod.Color
        explosion.colors = [Color(1.0, 1.0, 0.0, 1.0), Color(1.0, 0.0, 0.0, 1.0), Color(0.0, 0.0, 0.0, 1.0), Color(0.0, 0.0, 0.0, 0.0)]
        explosion.duration = 2

        shockwave = Engine.FX.Shockwave(self.position, 0.75, 200, [Color(1.0, 1.0, 0.0, 1.0), Color(1.0, 0.0, 0.0, 1.0), Color(0.0, 0.0, 0.0, 1.0), Color(0.0, 0.0, 0.0, 0.0)])

        particle_system = Engine.FX.ParticleSystem(self.position)
        particle_system.color_over_time = [Color(1.0, 1.0, 0.0, 1.0), Color(1.0, 0.0, 0.0, 1.0), Color(0.0, 0.0, 0.0, 1.0), Color(0.0, 0.0, 0.0, 0.0)]
        particle_system.start_speed = (50, 100)
        particle_system.particle_life = (2, 4)
        particle_system.drag = 0.995
        particle_system.rate = 0
        particle_system.spawn(50)

        Engine.Scene.main.add(explosion)
        Engine.Scene.main.add(shockwave)
        Engine.Scene.main.add(particle_system)

        Engine.SoundManager.play("Explosion")

        self.destroy()

    def render(self, screen):
        """Renders the ship.
        This renders the visual model, but also the thrusters.
        
        Arguments:
            screen {int} -- Display surface handler
        """

        # Render thrusters
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
        """Draw a thruster, which is a small triangle at a mountpoint
        
        Arguments:
            screen {int} -- Display surface handler on which to draw

            pos {Vector2} -- Base position of the thruster

            dir {Vector2} -- Direction of the thruster
            
            length {float} -- Lenght of the thruster
        """
        perpDir = Vector2(dir.y, -dir.x)
        pygame.draw.line(screen, self.thruster_color, pos + perpDir * self.thruster_width, pos + dir * self.thruster_length * length, self.thruster_line_width)
        pygame.draw.line(screen, self.thruster_color, pos - perpDir * self.thruster_width, pos + dir * self.thruster_length * length, self.thruster_line_width)
