from WireMesh import *
from Ship import *
from GameDefs import *
from pygame.math import Vector2

class PlayerShip(Ship):
    def __init__(self, name):
        Ship.__init__(self, name)

        self.gfx = WireMesh.GetModel("PlayerShip")
        
        self.color = (255, 255, 0)

    def Update(self, delta_time):
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

        Ship.Update(self, delta_time)

    def Render(self, screen):
        self.gfx.DrawPRS(screen, self.position, self.rotation, self.scale, self.color)
