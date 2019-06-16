import time
import pygame

class Screen:
    current = None

    def init(self):
        current = self
        self.running = True
        self.exit_code = 0   

    def shutdown(self):
        pass     

    def update(self, delta_time):
        keys = pygame.key.get_pressed()
        if ((keys[pygame.K_ESCAPE]) and (keys[pygame.K_LSHIFT])):
            self.set_exit(-1)

    def render(self, screen):
        pass

    def run(self, screen):

        self.init()

        dt = 0
        prev_time = time.time()

        while self.running:
            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    set_exit(-1)

            self.update(dt)
            self.render(screen)
        
            pygame.display.flip()

            dt = time.time() - prev_time
            prev_time = time.time()

        self.shutdown()

        return self.exit_code

    def set_exit(self, ret):
        self.exit_code = ret
        self.running = False