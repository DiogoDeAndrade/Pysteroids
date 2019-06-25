from ScreenAsteroids import *
from FontManager import *

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

        colorMin = 32
        colorMax = 255
        yTitle = 150
        yPrompt = 650

        if (self.time < 4):
            colorMin = (self.time / 4) * colorMin
            colorMax = (self.time / 4) * colorMax
            yTitle = 320
            yPrompt = 450
        elif (self.time < 6):
            t = (self.time - 4) / 2
            yTitle = t * 150 + (1 - t) * 320
            yPrompt = t * 650 + (1 - t) * 450
        elif (self.time > 6):
            GameDefs.DisplayHighScores(yTitle + 130)

        FontManager.WriteCenter(Screen.screen, "Vector", "PYSTEROIDS", (640, yTitle), (random.uniform(colorMin, colorMax), random.uniform(colorMin, colorMax), random.uniform(colorMin, colorMax)), spacingScale = self.scaling)
        if (self.scaling <= 1):
            FontManager.WriteCenter(Screen.screen, "Vector", "PRESS FIRE TO START", (640, yPrompt), (random.uniform(colorMin, colorMax), random.uniform(colorMin, colorMax), random.uniform(colorMin, colorMax)), scale = 0.2, widthScale = 0.5)
