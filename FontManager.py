import pygame
import os
import json
import pygame.freetype

from WireMesh import *

class TTFont:
    def __init__(self, path, size):
        self.fnt = pygame.freetype.Font(path, size)

    def render_to(self, screen, position, str, color, scale, widthScale, spacingScale):
        self.fnt.render_to(screen, position, str, color)

class VectorFont:
    def __init__(self):
        self.characters = dict()
        self.sizeX = self.sizeY = 0
        self.spacingX = self.spacingY = 0
        self.scale = 1
        self.lineWidth = 1

    def render_at(self, screen, position, str, color, scale, widthScale, spacingScale):
        currentPos = position

        for c in str:
            if (c in self.characters):
                self.characters[c].overrideColor = color
                self.characters[c].width = self.lineWidth * widthScale
                self.characters[c].DrawPRS(screen, currentPos, 0, Vector2(self.scale * scale, self.scale * scale))
            currentPos.x = currentPos.x + (self.sizeX + self.spacingX * spacingScale) * self.scale * scale

    def render_to(self, screen, position, str, color, scale, widthScale, spacingScale):
        currentPos = Vector2(position[0] + self.sizeX * 0.5 * self.scale * scale * widthScale, position[1] + self.sizeY * 0.5 * self.scale * scale)

        self.render_at(screen, currentPos, str, color, scale, widthScale, spacingScale)

    def render_to_centered(self, screen, position, str, color, scale, widthScale, spacingScale):
        size = len(str) * self.sizeX + (len(str) - 1) * self.spacingX * spacingScale

        currentPos = Vector2(position[0] - (size ) * 0.5 * self.scale * scale, position[1] + self.sizeY * 0.5 * self.scale * scale)

        self.render_at(screen, currentPos, str, color, scale, widthScale, spacingScale)

    @staticmethod
    def Load(filename, size):
        fnt = VectorFont()
        fnt.scale = size
        fnt.lineWidth = size

        text_file = open(filename, "rt")
        jsonString = text_file.read()
        text_file.close()

        meshes = json.loads(jsonString)

        for name in meshes:
            if (name == "Size"):
                fnt.sizeX = meshes[name][0]
                fnt.sizeY = meshes[name][1]
            elif (name == "Spacing"):
                fnt.spacingX = meshes[name][0]
                fnt.spacingY = meshes[name][1]
            else:
                newMesh = WireMesh()
                newMesh.FromJSON(meshes[name])
                newMesh.overrideColorEnable = True

                newMesh.name = name
                fnt.characters[name] = newMesh

        return fnt

class FontManager:
    instance = None

    def __init__(self):
        if (FontManager.instance == None):
            FontManager.instance = self
        else:
            raise Exception("This class is a singleton!")

        self.fonts = dict()
            
    def _Load(self, path, size, name):
        just_filename, file_extension = os.path.splitext(path)

        fnt = None
        if (file_extension == ".json"):
            fnt = VectorFont.Load(path, size)
        else:
            fnt = TTFont(path, size)            
        
        if (fnt != None):
            self.fonts[name] = fnt

        return fnt

    def _Write(self, screen, name, str, position, color, scale = 1, widthScale = 1, spacingScale = 1):
        if (name in self.fonts):
            self.fonts[name].render_to(screen, position, str, color, scale, widthScale, spacingScale)

    def _WriteCenter(self, screen, name, str, position, color, scale = 1, widthScale = 1, spacingScale = 1):
        if (name in self.fonts):
            self.fonts[name].render_to_centered(screen, position, str, color, scale, widthScale, spacingScale)

    @staticmethod
    def GetInstance():
        if (FontManager.instance == None):
            gFnt = FontManager()
        
        return FontManager.instance

    @staticmethod
    def Load(path, size, name):
        return FontManager.GetInstance()._Load(path, size, name)

    @staticmethod
    def Write(screen, name, str, position, color, scale = 1, widthScale = 1, spacingScale = 1):
        return FontManager.GetInstance()._Write(screen, name, str, position, color, scale, widthScale, spacingScale)

    @staticmethod
    def WriteCenter(screen, name, str, position, color, scale = 1, widthScale = 1, spacingScale = 1):
        return FontManager.GetInstance()._WriteCenter(screen, name, str, position, color, scale, widthScale, spacingScale)

