"""Sound manager. It stores and plays the loaded audio.

Access to the SoundManager should be done through the static functions, although it's of course possible to get a reference to the SoundManager singleton and access it's functions.
"""
import pygame

class SoundManager:
    """SoundManager class is a singleton."""
    instance = None
    """Singleton that stores the sound manager."""

    def __init__(self):
        """Initializes the audio system of Pygame. If it fails, the game will keep running, but without audio.

        Currently this fails on the Mac, for unknown reasons."""
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
        """Loads a sound and gives it a specific internal name.
        
        Arguments:
            path {string} -- Filename of the file. Any Pygame supported file can be used.
            
            name {string} -- Internal name for this sound.
        """
        if (pygame.mixer.get_init() == None):
            return

        snd = pygame.mixer.Sound(path)
        if (snd != None):
            self.sounds[name] = snd            

    def _play(self, name, volume, loop):
        """Plays a sound.
        
        Arguments:
            name {string} -- Internal name of the sound

            volume {float} -- Volume to play the sound. This is modulated with the global volume.

            loop {bool} -- Should the sound play in a loop?
        
        Returns:
            int -- Channel number where the sound is playing.
        """
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
        """Fetches a free audio channel. This is used internally by the sound playing functions."""
        if (pygame.mixer.get_init() == None):
            return None

        for channel in self.channels:
            if (not channel.get_busy()):
                return channel

        return None

    @staticmethod
    def get_instance():
        """Retrieves the singleton instance of the sound manager, or creates a new one.
        
        Returns:
            SoundManager -- Singleton reference to the SoundManager.
        """
        if (SoundManager.instance == None):
            gSnd = SoundManager()
        
        return SoundManager.instance

    @staticmethod
    def load(path, name):
        """Loads a sound
        
        Arguments:
            path {string} -- Filename to load

            name {string} -- Internal name of this sound
        """
        return SoundManager.get_instance()._load(path, name)

    @staticmethod
    def play(name, volume = 1.0, loop = False):
        """Plays a sound
        
        Arguments:
            name {string} -- Sound internal name     
            
            volume {float} -- Volume of the sound (default: {1.0})

            loop {bool} -- Should the sound loop at the end? (default: {False})
        
        Returns:
            int -- Channel number where the sound is playing.
        """
        return SoundManager.get_instance()._play(name, volume, loop)

    @staticmethod
    def set_global_volume(volume):
        """Sets the global volume of the audio.
        
        Arguments:
            volume {float} -- Volume to set, in the range [0..1]
        """
        SoundManager.get_instance().global_volume = volume
