from ScreenAsteroids import *
from FontManager import *

class ScreenAsteroidsTitle(ScreenAsteroids):
    def init(self):
        ScreenAsteroids.init(self)

        self.scaling = 40
        self.init_objects(0)

    def update(self, delta_time):
        ScreenAsteroids.update(self, delta_time)

        if (self.scaling  > 1):
            self.scaling = self.scaling - delta_time * 10
            if (self.scaling < 1):
                self.scaling = 1

        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LCTRL]):
            self.set_exit(1)
        

    def render(self, screen):
        Screen.render(self, screen)

        screen.fill((5, 5, 15))

        Scene.main.Render(screen)

        FontManager.WriteCenter(screen, "Vector", "PYSTEROIDS", (640, 320), (random.uniform(32, 255), random.uniform(32, 255), random.uniform(32, 255)), spacingScale = self.scaling)
        if (self.scaling <= 1):
            FontManager.WriteCenter(screen, "Vector", "PRESS FIRE TO START", (640, 450), (random.uniform(32, 255), random.uniform(32, 255), random.uniform(32, 255)), scale = 0.2)
