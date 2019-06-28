from Screen import *
from Asteroid import *
from Starfield import *

class ScreenAsteroids(Screen):
    def init(self):
       
        keys = pygame.key.get_pressed()
        while (keys[pygame.K_LCTRL]):
            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    running = False
            keys = pygame.key.get_pressed()

        Screen.init(self)

        Scene.main.clear()

    def init_objects(self, level):

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
        Screen.update(self, delta_time)

        Scene.main.update(delta_time)

    def render(self):
        Screen.render(self)

        Screen.screen.fill((5, 5, 15))

        Scene.main.render(Screen.screen)

    