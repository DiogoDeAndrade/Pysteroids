"""Screens are functionality equivelent to a section of your game. 

In a normal game, you could have a TitleScreen, a GameplayScreen, a CreditsScreen, etc.

Each of them would then be implemented as a separate Screen."
"""
import time
import pygame

from Engine.SoundManager import *

class Screen:
    """Screen base class"""
    current = None
    """Currently active screen"""
    screen = None
    """Current display surface handle"""
    fullscreen = False
    """Is the game in fullscreen mode?"""

    @staticmethod
    def startup():
        """Initializes the screen system, alongside pygame and other libraries that require initialization.

        By default, the following parameters are used in the inicialization:

        * Audio system uses 16 bit per sample, 2 channels, 44100 Hz, with a 1024 byte buffer (approx. 5 ms delay)
        
        * Application icon is fetch from sprites/icon.png

        * Name of the application currently is hardcoded (Pysteroids) - Possible improvement

        * Graphics are double buffered, fullscreen is disabled by default. Resolution is 1280x720.
        """
        pygame.mixer.pre_init(44100, 16, 2, 1024)
        pygame.init()
        logo = pygame.image.load("sprites/icon.png")
        pygame.display.set_icon(logo)
        pygame.display.set_caption("Pysteroids")

        flags = pygame.DOUBLEBUF
        if (Screen.fullscreen):
            flags = flags | pygame.FULLSCREEN

        Screen.screen = pygame.display.set_mode((1280, 720), flags)

        SoundManager.set_global_volume(0.25)

    def init(self):
        """Initializes this screen, so it can start running. 

        This is called internally by run() and should not be called explicitely.
        """
        Screen.current = self
        self.running = True
        self.exit_code = 0   

    def shutdown(self):
        """Disables this screen.

        This is called internally by run() and should not be called explicitely.
        """
        Screen.current = None

    def update(self, delta_time):
        """Updates this screen.

        All screens implement by default LSHIFT+ESCAPE to exit the application, and ALT+RETURN to toggle fullscreen.
        
        This is called internally by run() and should not be called explicitely."""
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
        """Renders this screen.
        
        This is called internally by run() and should not be called explicitely."""
        pass

    def run(self):
        """Runs this screen. 
        
        This function only returns when Screen.current.set_exit() is called, otherwise it just implements the game loop:
        ```
        Process OS events
        Update screen
        Render screen
        Flip backbuffer
        ```
        
        Returns:
            int -- Value passed to set_exit()
        """
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
        """Sets the exit flag of this screen to true, and the exit code to the given value, so break the game loop.
        
        Arguments:
            ret {int} -- Exit code of the screen
        """
        self.exit_code = ret
        self.running = False