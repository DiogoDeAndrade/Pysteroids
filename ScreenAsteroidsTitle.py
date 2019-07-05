from ScreenAsteroids import *

class ScreenAsteroidsTitle(ScreenAsteroids):
    def init(self):
        ScreenAsteroids.init(self)

        self.scaling = 40
        self.init_objects(0)
        self.time = 0

    def update(self, delta_time):
        ScreenAsteroids.update(self, delta_time)

        if (self.scaling  > 1):
            self.scaling = self.scaling - delta_time * 10
            if (self.scaling < 1):
                self.scaling = 1

        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LCTRL]):
            self.set_exit(1)

        self.time = self.time + delta_time
        

    def render(self):
        ScreenAsteroids.render(self)

        color_min = 32
        color_max = 255
        y_title = 150
        y_prompt = 650

        if (self.time < 4):
            color_min = (self.time / 4) * color_min
            color_max = (self.time / 4) * color_max
            y_title = 320
            y_prompt = 450
        elif (self.time < 6):
            t = (self.time - 4) / 2
            y_title = t * 150 + (1 - t) * 320
            y_prompt = t * 650 + (1 - t) * 450
        elif (self.time > 6):
            GameDefs.display_highscores(y_title + 130)

        FontManager.write_center(Engine.Screen.screen, "Vector", "PYSTEROIDS", (640, y_title), (random.uniform(color_min, color_max), random.uniform(color_min, color_max), random.uniform(color_min, color_max)), spacing_scale = self.scaling)
        if (self.scaling <= 1):
            FontManager.write_center(Engine.Screen.screen, "Vector", "PRESS FIRE TO START", (640, y_prompt), (random.uniform(color_min, color_max), random.uniform(color_min, color_max), random.uniform(color_min, color_max)), scale = 0.2, width_scale = 0.5)
