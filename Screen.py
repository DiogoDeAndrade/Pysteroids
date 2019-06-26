import time
import pygame
from SoundManager import *

class Screen:
    current = None
    screen = None
    fullscreen = False

    @staticmethod
    def startup():
        pygame.mixer.pre_init(44100, 16, 2, 1024)
        pygame.init()
        logo = pygame.image.load("sprites/icon.png")
        pygame.display.set_icon(logo)
        pygame.display.set_caption("Pysteroids")

        flags = pygame.DOUBLEBUF
        if (Screen.fullscreen):
            flags = flags | pygame.FULLSCREEN

        Screen.screen = pygame.display.set_mode((1280, 720), flags)

        SoundManager.SetGlobalVolume(0.25)

    def init(self):
        Screen.current = self
        self.running = True
        self.exit_code = 0   

    def shutdown(self):
        Screen.current = None

    def update(self, delta_time):
        keys = pygame.key.get_pressed()
        if ((keys[pygame.K_ESCAPE]) and (keys[pygame.K_LSHIFT])):
            self.set_exit(-1)

        if ((keys[pygame.K_RETURN]) and ((keys[pygame.K_LALT]) or (keys[pygame.K_RALT]))):
            Screen.fullscreen = not Screen.fullscreen
            if (Screen.fullscreen):
                Screen.screen = pygame.display.set_mode((1280, 720), pygame.DOUBLEBUF | pygame.FULLSCREEN)
            else:
                Screen.screen = pygame.display.set_mode((1280, 720), pygame.DOUBLEBUF)

    def render(self):
        pass

    def run(self):

        self.init()

        dt = 0
        prev_time = time.time()

        while self.running:
            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    self.set_exit(-1)

            self.update(dt)
            self.render()
        
            pygame.display.flip()

            dt = time.time() - prev_time
            prev_time = time.time()

        self.shutdown()

        return self.exit_code

    def set_exit(self, ret):
        self.exit_code = ret
        self.running = False