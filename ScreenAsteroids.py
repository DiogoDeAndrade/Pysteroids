import pygame

import Engine

from Asteroid import *
from Starfield import *

class ScreenAsteroids(Engine.Screen):
    """ScreenAsteroids class.
    This is the base class for the screens in the game, that spawns automatically some asteroids and a starfield.
    """
    def init(self):
        """Initialization of this screen will be suspended while the shoot button is pressed."""
       
        keys = pygame.key.get_pressed()
        while (keys[pygame.K_LCTRL]):
            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    running = False
            keys = pygame.key.get_pressed()

        Engine.Screen.init(self)

        Scene.main.clear()

    def init_objects(self, level):
        """Initializes a playfield, by adding stars and creating some asteroids.
        
        Arguments:
            level {int} -- Level to initialize (changes the number of asteroids in the playfield)
        """
        Scene.main.add(Starfield("Starfield", 400))

        n_asteroids = 3 + level

        for i in range(0,n_asteroids):
            asteroid = Asteroid("Asteroid" + str(i))
            dir = Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize()
            asteroid.position = Vector2(640, 360)
            asteroid.position.x = asteroid.position.x + dir.x * random.uniform(200, 640)
            asteroid.position.y = asteroid.position.y + dir.y * random.uniform(100, 360)
            Scene.main.add(asteroid)

    def update(self, delta_time):
        """Updates the screen, which in turn updates the scene.
        
        Arguments:
            delta_time {float} -- Time to elapse in seconds
        """
        Screen.update(self, delta_time)

        Scene.main.update(delta_time)

    def render(self):
        """Renders the screen (fills the background and renders the scene)"""
        Engine.Screen.render(self)

        Engine.Screen.screen.fill((5, 5, 15))

        Scene.main.render(Engine.Screen.screen)

    