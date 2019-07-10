from pygame.math import Vector2

from Engine import *
from Ship import *
from GameDefs import *

class Asteroid(Ship):
    """Asteroid class."""
    def __init__(self, name, radius = 40, variance = 0.5, rotation_speed = 90.0, speed = 25):
        """This defines an asteroid in the game world, that floats and gets split in smaller pieces if the player shoots it.
        
        Arguments:
            name {string} -- Name of this asteroid
        

        Keyword Arguments:
            radius {int} -- Asteroid average radius (default: {40})

            variance {float} -- Radius variance (default: {0.5})

            rotation_speed {float} -- Rotation speed of the asteroid (in degrees per second) (default: {90.0})

            speed {int} -- Linear speed of the asteroid (in pixels per second) (default: {25})

        """
        Ship.__init__(self, name)

        self.radius = radius
        self.variance = variance
        # Create graphics for the asteroid
        self.gfx = WireMesh.circle(8, self.radius, self.radius * self.variance, (130, 68, 0))
        self.gfx.render_mode = Engine.RenderMode.Normal
        self.gfx.width = 2
        self.max_radius = self.radius * (1 + self.variance)
        
        self.rotation_speed = random.uniform(-rotation_speed, rotation_speed)
        self.velocity = Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize()
        self.velocity *= random.uniform(speed, speed * 2)
        self.drag = 0

        # Creates the collider for the object (in this case, a circle)
        self.collider = Circle2d(Vector2(0,0), self.gfx.get_radius())

        # Adds a tag to the asteroid, so the collision system can identify this object type
        self.tags.append("Asteroid")

    def update(self, delta_time):
        """Updates the position of the asteroid
        
        Arguments:
            delta_time {float} -- Time to elapse, in seconds
        """

        # Use velocity and physics to move asteroid
        Ship.update(self, delta_time)

        # Rotate asteroid around itself
        self.rotation += self.rotation_speed * delta_time

        # Check bounds, and wrap the playfield around
        if (self.position.x < -self.max_radius):
            self.position.x = 1280 + self.max_radius
        elif (self.position.x > (1280 + self.max_radius)):
            self.position.x = self.max_radius

        if (self.position.y < -self.max_radius):
            self.position.y = 720 + self.max_radius
        elif (self.position.y > (720 + self.max_radius)):
            self.position.y = -self.max_radius

    def render(self, screen):
        """Renders the asteroid
        
        Arguments:
            screen {int} -- Display surface handle
        """
        
        self.gfx.drawPRS(screen, self.position, self.rotation, self.scale)

    def explode(self):
        """Explodes the asteroid, like any other Ship, but if the radius of the asteroid is larger than 20, create two new asteroids that have derived properties (smaller, faster)."""
        
        Ship.explode(self)

        if (self.radius >= 20):
            asteroid1 = Asteroid(self.name + "_0", 
                                 self.radius / 2, 
                                 self.variance / 2, 
                                 self.rotation_speed * 1.25, 
                                 self.velocity.magnitude() * 1.1)
            asteroid1.position = Vector2(self.position)
            Scene.main.add(asteroid1)

            asteroid2 = Asteroid(self.name + "_1", 
                                 self.radius / 2, 
                                 self.variance / 2, 
                                 self.rotation_speed * 1.25, 
                                 self.velocity.magnitude() * 1.1)
            asteroid2.position = Vector2(self.position)
            Scene.main.add(asteroid2)
