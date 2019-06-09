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
        for i in range(0, min(16, pygame.mixer.get_num_channels())):
            self.channels.append(pygame.mixer.Channel(i))

        self.global_volume = 1.0
            
    def _Load(self, path, name):
        snd = pygame.mixer.Sound(path)
        if (snd != None):
            self.sounds[name] = snd            

    def _Play(self, name, volume, loop):
        if (name in self.sounds):
            channel = self.GetChannel()
            
            if (channel != None):
                channel.play(self.sounds[name], (-1) if (loop) else 0)
                channel.set_volume(volume * self.global_volume)

                return channel

        return None

    def GetChannel(self):
        for channel in self.channels:
            if (not channel.get_busy()):
                return channel

        return None

    @staticmethod
    def GetInstance():
        if (SoundManager.instance == None):
            gSnd = SoundManager()
        
        return SoundManager.instance

    @staticmethod
    def Load(path, name):
        return SoundManager.GetInstance()._Load(path, name)

    @staticmethod
    def Play(name, volume = 1.0, loop = False):
        return SoundManager.GetInstance()._Play(name, volume, loop)

    @staticmethod
    def SetGlobalVolume(volume):
        SoundManager.GetInstance().global_volume = volume
