from WireMesh import *
from Ship import *
from Laser import *
from GameDefs import *
from pygame.math import Vector2

class PlayerShip(Ship):
    def __init__(self, name):
        Ship.__init__(self, name)

        self.gfx = WireMesh.GetModel("PlayerShip")
        self.collider = Circle2d(Vector2(0,0), self.gfx.GetRadius())
        self.radius = self.maxRadius = self.gfx.GetRadius()
        self.shot_cooldown = 0.25
        self.current_shot_cooldown = 0

        self.tags.append("PlayerShip")

        self.engine_sound = SoundManager.Play("Engine", 0, True)
        
    def Update(self, delta_time):

        self.current_shot_cooldown = self.current_shot_cooldown - delta_time

        keys = pygame.key.get_pressed()

        self.thrusterM = self.thrusterR = self.thrusterL = 0

        # Accelerate ship
        if (keys[pygame.K_UP]):
            self.AddVelocity(self.acceleration * delta_time * self.GetDirectionVector())
            self.thrusterM = self.thrusterR = self.thrusterL = 1
            
            if (self.engine_sound != None):
                self.engine_sound.set_volume(0.1)
        else:
            if (self.engine_sound != None):
                self.engine_sound.set_volume(0.0)

        # Rotate ship
        rotationSpeed = delta_time * GameDefs["player_defs"]["rotation_speed"] 
        if (keys[pygame.K_LEFT]):
            self.thrusterM = 0
            self.thrusterR = 0.5
            self.thrusterL = 0
            self.rotation -= rotationSpeed

        if (keys[pygame.K_RIGHT]):
            self.thrusterM = 0
            self.thrusterR = 0
            self.thrusterL = 0.5
            self.rotation += rotationSpeed

        # Break ship
        if (keys[pygame.K_DOWN]):
            self.AddVelocity(-self.break_acceleration * delta_time * self.GetDirectionVector())

        # Fire
        if (keys[pygame.K_LCTRL]):
            if (self.current_shot_cooldown <= 0):
                laserPos, laserDir = self.GetMountpoint("LaserPos0")
                Scene.main.Add(Laser("PlayerLaser", (64, 255, 64), 4, 20, laserPos, laserDir * 400, 2))
                self.current_shot_cooldown = self.shot_cooldown
                SoundManager.Play("Laser", 0.5)

        Ship.Update(self, delta_time)

        # Check bounds
        if (self.position.x < -self.maxRadius):
            self.position.x = 1280 + self.maxRadius
        elif (self.position.x > (1280 + self.maxRadius)):
            self.position.x = self.maxRadius

        if (self.position.y < -self.maxRadius):
            self.position.y = 720 + self.maxRadius
        elif (self.position.y > (720 + self.maxRadius)):
            self.position.y = -self.maxRadius

    def Render(self, screen):
        Ship.Render(self, screen)

        self.gfx.DrawPRS(screen, self.position, self.rotation, self.scale)

    def OnDestroy(self):
        GameObject.OnDestroy(self)

        if (self.engine_sound != None):
            self.engine_sound.stop()
