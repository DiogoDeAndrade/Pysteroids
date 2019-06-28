import pygame

class SoundManager:
    instance = None

    def __init__(self):
        if (SoundManager.instance == None):
            SoundManager.instance = self
        else:
            raise Exception("This class is a singleton!")

        self.sounds = dict()
        self.channels = []
        if (pygame.mixer.get_init() != None):
            for i in range(0, min(16, pygame.mixer.get_num_channels())):
                self.channels.append(pygame.mixer.Channel(i))

        self.global_volume = 1.0
            
    def _load(self, path, name):
        if (pygame.mixer.get_init() == None):
            return

        snd = pygame.mixer.Sound(path)
        if (snd != None):
            self.sounds[name] = snd            

    def _play(self, name, volume, loop):
        if (pygame.mixer.get_init() == None):
            return None

        if (name in self.sounds):
            channel = self.get_channel()
            
            if (channel != None):
                channel.play(self.sounds[name], (-1) if (loop) else 0)
                channel.set_volume(volume * self.global_volume)

                return channel

        return None

    def get_channel(self):
        if (pygame.mixer.get_init() == None):
            return None

        for channel in self.channels:
            if (not channel.get_busy()):
                return channel

        return None

    @staticmethod
    def get_instance():
        if (SoundManager.instance == None):
            gSnd = SoundManager()
        
        return SoundManager.instance

    @staticmethod
    def load(path, name):
        return SoundManager.get_instance()._load(path, name)

    @staticmethod
    def play(name, volume = 1.0, loop = False):
        return SoundManager.get_instance()._play(name, volume, loop)

    @staticmethod
    def set_global_volume(volume):
        SoundManager.get_instance().global_volume = volume
