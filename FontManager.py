import pygame
import os
import json
import pygame.freetype

from WireMesh import *

class TTFont:
    def __init__(self, path, size):
        self.fnt = pygame.freetype.Font(path, size)

    def render_to(self, screen, position, str, color, scale, width_scale, spacing_scale):
        self.fnt.render_to(screen, position, str, color)

class VectorFont:
    def __init__(self):
        self.characters = dict()
        self.size_x = self.size_y = 0
        self.spacing_x = self.spacing_y = 0
        self.scale = 1
        self.lineWidth = 1

    def render_at(self, screen, position, str, color, scale, width_scale, spacing_scale):
        currentPos = position

        for c in str:
            if (c in self.characters):
                self.characters[c].override_color = color
                self.characters[c].width = self.lineWidth * width_scale
                self.characters[c].drawPRS(screen, currentPos, 0, Vector2(self.scale * scale, self.scale * scale))
            currentPos.x = currentPos.x + (self.size_x + self.spacing_x * spacing_scale) * self.scale * scale

    def render_to(self, screen, position, str, color, scale, width_scale, spacing_scale):
        currentPos = Vector2(position[0] + self.size_x * 0.5 * self.scale * scale * width_scale, position[1] + self.size_y * 0.5 * self.scale * scale)

        self.render_at(screen, currentPos, str, color, scale, width_scale, spacing_scale)

    def render_to_centered(self, screen, position, str, color, scale, width_scale, spacing_scale):
        size = len(str) * self.size_x + (len(str) - 1) * self.spacing_x * spacing_scale

        currentPos = Vector2(position[0] - (size ) * 0.5 * self.scale * scale, position[1] + self.size_y * 0.5 * self.scale * scale)

        self.render_at(screen, currentPos, str, color, scale, width_scale, spacing_scale)

    @staticmethod
    def load(filename, size):
        fnt = VectorFont()
        fnt.scale = size
        fnt.lineWidth = size

        text_file = open(filename, "rt")
        json_string = text_file.read()
        text_file.close()

        meshes = json.loads(json_string)

        for name in meshes:
            if (name == "Size"):
                fnt.size_x = meshes[name][0]
                fnt.size_y = meshes[name][1]
            elif (name == "Spacing"):
                fnt.spacing_x = meshes[name][0]
                fnt.spacing_y = meshes[name][1]
            else:
                new_mesh = WireMesh()
                new_mesh.from_JSON(meshes[name])
                new_mesh.override_color_enable = True

                new_mesh.name = name
                fnt.characters[name] = new_mesh

        return fnt

class FontManager:
    instance = None

    def __init__(self):
        if (FontManager.instance == None):
            FontManager.instance = self
        else:
            raise Exception("This class is a singleton!")

        self.fonts = dict()
            
    def _load(self, path, size, name):
        just_filename, file_extension = os.path.splitext(path)

        fnt = None
        if (file_extension == ".json"):
            fnt = VectorFont.load(path, size)
        else:
            fnt = TTFont(path, size)            
        
        if (fnt != None):
            self.fonts[name] = fnt

        return fnt

    def _write(self, screen, name, str, position, color, scale = 1, width_scale = 1, spacing_scale = 1):
        if (name in self.fonts):
            self.fonts[name].render_to(screen, position, str, color, scale, width_scale, spacing_scale)

    def _write_center(self, screen, name, str, position, color, scale = 1, width_scale = 1, spacing_scale = 1):
        if (name in self.fonts):
            self.fonts[name].render_to_centered(screen, position, str, color, scale, width_scale, spacing_scale)

    @staticmethod
    def get_instance():
        if (FontManager.instance == None):
            gFnt = FontManager()
        
        return FontManager.instance

    @staticmethod
    def load(path, size, name):
        return FontManager.get_instance()._load(path, size, name)

    @staticmethod
    def write(screen, name, str, position, color, scale = 1, width_scale = 1, spacing_scale = 1):
        return FontManager.get_instance()._write(screen, name, str, position, color, scale, width_scale, spacing_scale)

    @staticmethod
    def write_center(screen, name, str, position, color, scale = 1, width_scale = 1, spacing_scale = 1):
        return FontManager.get_instance()._write_center(screen, name, str, position, color, scale, width_scale, spacing_scale)

