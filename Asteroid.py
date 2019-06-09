from WireMesh import *
from Ship import *
from GameDefs import *
from pygame.math import Vector2

class Asteroid(Ship):
    def __init__(self, name, radius = 40, variance = 0.5, rotation_speed = 90.0, speed = 25):
        Ship.__init__(self, name)

        self.radius = radius
        self.variance = variance
        self.gfx = WireMesh.Circle(8, self.radius, self.radius * self.variance, (200, 128, 0))
        self.gfx.renderMode = RenderMode.Normal
        self.gfx.width = 2
        self.maxRadius = self.radius * (1 + self.variance)
        
        self.rotation_speed = random.uniform(-rotation_speed, rotation_speed)
        self.velocity = Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize()
        self.velocity *= random.uniform(speed, speed * 2)
        self.drag = 0

        self.collider = Circle2d(Vector2(0,0), self.gfx.GetRadius())

        self.tags.append("Asteroid")

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

    def Explode(self):
        Ship.Explode(self)

        if (self.radius >= 20):
            asteroid1 = Asteroid(self.name + "_0", 
                                 self.radius / 2, 
                                 self.variance / 2, 
                                 self.rotation_speed * 1.25, 
                                 self.velocity.magnitude() * 1.1)
            asteroid1.position = Vector2(self.position)
            Scene.main.Add(asteroid1)

            asteroid2 = Asteroid(self.name + "_1", 
                                 self.radius / 2, 
                                 self.variance / 2, 
                                 self.rotation_speed * 1.25, 
                                 self.velocity.magnitude() * 1.1)
            asteroid2.position = Vector2(self.position)
            Scene.main.Add(asteroid2)
