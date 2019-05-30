from WireMesh import *
from Ship import *
from GameDefs import *
from pygame.math import Vector2

class Asteroid(Ship):
    def __init__(self, name):
        Ship.__init__(self, name)

        self.radius = 40
        self.variance = 0.5
        self.gfx = WireMesh.Circle(8, self.radius, self.radius * self.variance, (200, 128, 0))
        self.gfx.renderMode = RenderMode.Normal
        self.gfx.width = 2
        self.maxRadius = self.radius * (1 + self.variance)
        
        self.rotation_speed = random.uniform(-90, 90)
        self.velocity = Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize()
        self.velocity *= random.uniform(20, 50)
        self.drag = 0

    def Update(self, delta_time):
        Ship.Update(self, delta_time)

        self.rotation += self.rotation_speed * delta_time

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
        self.gfx.DrawPRS(screen, self.position, self.rotation, self.scale)

