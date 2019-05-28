from GameObject import *

class Ship(GameObject):
    def __init__(self, name):
        GameObject.__init__(self, name)

        self.acceleration = 200.0
        self.break_acceleration = 100.0
        self.velocity = Vector2(0,0)
        self.maxVelocity = 200.0
        self.drag = 0.75

    def Update(self, delta_time):
        GameObject.Update(self, delta_time)

        if (self.drag > 0):
            self.AddVelocity(-self.velocity * self.drag * delta_time)

        self.position += self.velocity * delta_time        

    def AddVelocity(self, velocity):
        self.velocity += velocity

        if (self.velocity.magnitude() > self.maxVelocity):
            self.velocity = self.velocity.normalize() * self.maxVelocity
