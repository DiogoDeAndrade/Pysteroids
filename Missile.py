from WireMesh import *
from Ship import *
from GameDefs import *
from Trail import *
from pygame.math import Vector2

class Missile(Ship):
    def __init__(self, name, target, tag):
        Ship.__init__(self, name)

        self.gfx = WireMesh.GetModel("Missile")
        self.trail = Trail("MissileTrail", 2, Color(0, 1, 1, 1), Color(0, 0, 0, 0), 5, self, "TrailAnchor0", 0.1)
        
        self.collider = Circle2d(Vector2(0,0), self.gfx.GetRadius())
        self.radius = self.gfx.GetRadius()

        self.target = target
        self.maxRotationAngle = 450
        self.life = 7.5

        self.tags.append("Missile")

        self.tags.append(tag)
        
    def Update(self, delta_time):
        if (self.target == None):
            self.Explode()
            return

        self.trail.Update(delta_time)

        # Aim at target
        desiredDirection = (self.target.position - self.position).normalize()
        currentDirection = self.GetDirectionVector()

        # Get desired angle of rotation
        angle = math.degrees(math.acos(currentDirection.dot(desiredDirection))) * delta_time
        # Get sign of rotation
        if (self.GetRightVector().dot(desiredDirection) < 0):
            angle = -angle

        angle = max(min(angle, self.maxRotationAngle), -self.maxRotationAngle)

        self.rotation = self.rotation + angle

        self.velocity = self.GetDirectionVector() * 150

        Ship.Update(self, delta_time)

        self.life = self.life - delta_time
        if (self.life < 0):
            self.Explode()

    def Render(self, screen):
        Ship.Render(self, screen)

        self.gfx.DrawPRS(screen, self.position, self.rotation, self.scale)

        self.trail.Render(screen)

    def OnDestroy(self):
        GameObject.OnDestroy(self)

