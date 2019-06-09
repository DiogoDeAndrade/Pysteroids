import pygame
import pygame.freetype

class FontManager:
    instance = None

    def __init__(self):
        if (FontManager.instance == None):
            FontManager.instance = self
        else:
            raise Exception("This class is a singleton!")

        self.fonts = dict()
            
    def _Load(self, path, size, name):
        fnt = pygame.freetype.Font(path, size)
        if (fnt != None):
            self.fonts[name] = fnt

    def _Write(self, screen, name, str, position, color):
        if (name in self.fonts):
            self.fonts[name].render_to(screen, position, str, color)

    @staticmethod
    def GetInstance():
        if (FontManager.instance == None):
            gFnt = FontManager()
        
        return FontManager.instance

    @staticmethod
    def Load(path, size, name):
        return FontManager.GetInstance()._Load(path, size, name)

    @staticmethod
    def Write(screen, name, str, position, color):
        return FontManager.GetInstance()._Write(screen, name, str, position, color)

