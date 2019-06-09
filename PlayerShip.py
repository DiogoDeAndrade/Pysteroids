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
        self.radius = self.gfx.GetRadius()
        self.shot_cooldown = 0.5
        self.current_shot_cooldown = 0

        self.tags.append("PlayerShip")
        
    def Update(self, delta_time):

        self.current_shot_cooldown = self.current_shot_cooldown - delta_time

        keys = pygame.key.get_pressed()

        # Rotate ship
        rotationSpeed = delta_time * GameDefs["player_defs"]["rotation_speed"] 
        if (keys[pygame.K_LEFT]):
            self.rotation -= rotationSpeed

        if (keys[pygame.K_RIGHT]):
            self.rotation += rotationSpeed

        # Accelerate ship
        if (keys[pygame.K_UP]):
            self.AddVelocity(self.acceleration * delta_time * self.GetDirectionVector())

        # Break ship
        if (keys[pygame.K_DOWN]):
            self.AddVelocity(-self.break_acceleration * delta_time * self.GetDirectionVector())

        # Fire
        if (keys[pygame.K_SPACE]):
            if (self.current_shot_cooldown <= 0):
                Scene.main.Add(Laser("PlayerLaser", (64, 255, 64), 4, 20, self.GetMountpoint("LaserPos0"), self.GetDirectionVector() * 400, 2))
                self.current_shot_cooldown = self.shot_cooldown

        Ship.Update(self, delta_time)

    def Render(self, screen):
        self.gfx.DrawPRS(screen, self.position, self.rotation, self.scale)

