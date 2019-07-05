from pygame.math import Vector2

import Engine

from Ship import *
from Laser import *
from GameDefs import *

class PlayerShip(Ship):
    def __init__(self, name):
        Ship.__init__(self, name)

        self.gfx = Engine.WireMesh.get_model("PlayerShip")
        self.collider = Engine.Circle2d(Vector2(0,0), self.gfx.get_radius())
        self.radius = self.max_radius = self.gfx.get_radius()
        self.shot_cooldown = 0.25
        self.current_shot_cooldown = 0

        self.tags.append("PlayerShip")

        self.engine_sound = Engine.SoundManager.play("Engine", 0, True)
        
    def update(self, delta_time):

        self.current_shot_cooldown = self.current_shot_cooldown - delta_time

        keys = pygame.key.get_pressed()

        self.thruster_m = self.thruster_r = self.thruster_l = 0

        # Accelerate ship
        if (keys[pygame.K_UP]):
            self.add_velocity(self.acceleration * delta_time * self.get_direction_vector())
            self.thruster_m = self.thruster_r = self.thruster_l = 1
            
            if (self.engine_sound != None):
                self.engine_sound.set_volume(0.1)
        else:
            if (self.engine_sound != None):
                self.engine_sound.set_volume(0.0)

        # Rotate ship
        rotationSpeed = delta_time * GameDefs.player_defs.rotationSpeed
        if (keys[pygame.K_LEFT]):
            self.thruster_m = 0
            self.thruster_r = 0.5
            self.thruster_l = 0
            self.rotation -= rotationSpeed

        if (keys[pygame.K_RIGHT]):
            self.thruster_m = 0
            self.thruster_r = 0
            self.thruster_l = 0.5
            self.rotation += rotationSpeed

        # Break ship
        if (keys[pygame.K_DOWN]):
            self.add_velocity(-self.break_acceleration * delta_time * self.get_direction_vector())

        # Fire
        if (keys[pygame.K_LCTRL]):
            if (self.current_shot_cooldown <= 0):
                laser_pos, laser_dir = self.get_mountpoint("laser_pos0")
                Engine.Scene.main.add(Laser("PlayerLaser", (64, 255, 64), 4, 20, laser_pos, laser_dir * 400, 2))
                self.current_shot_cooldown = self.shot_cooldown
                Engine.SoundManager.play("Laser", 0.5)

        Ship.update(self, delta_time)

        # Check bounds
        if (self.position.x < -self.max_radius):
            self.position.x = 1280 + self.max_radius
        elif (self.position.x > (1280 + self.max_radius)):
            self.position.x = self.max_radius

        if (self.position.y < -self.max_radius):
            self.position.y = 720 + self.max_radius
        elif (self.position.y > (720 + self.max_radius)):
            self.position.y = -self.max_radius

    def render(self, screen):
        Ship.render(self, screen)

        self.gfx.drawPRS(screen, self.position, self.rotation, self.scale)

    def on_destroy(self):
        Engine.GameObject.on_destroy(self)

        if (self.engine_sound != None):
            self.engine_sound.stop()
