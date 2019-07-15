"""Font manager. It stores and uses the loaded fonts.

Access to the FontManager should be done through the static functions, although it's of course possible to get a reference to the FontManager singleton and access it's functions.
"""
import pygame
import os
import json
import pygame.freetype

from Engine.WireMesh import *

class TTFont:
    """True type font, supported by Pygame"""
    def __init__(self, path, size):
        """        
        Arguments:
            path {string} -- Path to the true type font to load

            size {float} -- Size of the font to load.
        """
        self.fnt = pygame.freetype.Font(path, size)

    def render_to(self, screen, position, str, color, scale, width_scale, spacing_scale):
        """Renders the given text on the screen.
        
        Arguments:
            screen {int} -- Display surface handle

            position {tuple(x,y)} -- Position to render text, in pixel coordinates

            str {string} -- Text to display

            color {tuple(R,G,B,A)} -- Color of the text

            scale {float} -- Scale of the text to display. Ignored in true type fonts

            width_scale {float} -- Width scale of the text to display. Ignored in true type fonts

            spacing_scale {float} -- Spacing scale of the text to display. Ignored in true type fonts
        """
        self.fnt.render_to(screen, position, str, color)

class VectorFont:
    """Vector type font"""
    def __init__(self):
        """Initializes an empty vector font"""
        self.characters = dict()
        self.size_x = self.size_y = 0
        self.spacing_x = self.spacing_y = 0
        self.scale = 1
        self.lineWidth = 1

    def render_at(self, screen, position, str, color, scale, width_scale, spacing_scale):
        """Internal function, renders the given text on the screen.
        
        Arguments:
            screen {int} -- Display surface handle

            position {tuple(x,y)} -- Position to render text, in pixel coordinates

            str {string} -- Text to display

            color {tuple(R,G,B,A)} -- Color of the text

            scale {float} -- Scale of the text to display. 

            width_scale {float} -- Width scale of the text to display. 

            spacing_scale {float} -- Spacing scale of the text to display. 
        """
        currentPos = position

        for c in str:
            if (c in self.characters):
                self.characters[c].override_color = color
                self.characters[c].width = self.lineWidth * width_scale
                self.characters[c].drawPRS(screen, currentPos, 0, Vector2(self.scale * scale, self.scale * scale))
            currentPos.x = currentPos.x + (self.size_x + self.spacing_x * spacing_scale) * self.scale * scale

    def render_to(self, screen, position, str, color, scale, width_scale, spacing_scale):
        """Renders the given text on the screen. This is the function that should be used to actually display text. 
        
        Arguments:
            screen {int} -- Display surface handle

            position {tuple(x,y)} -- Position to render text, in pixel coordinates

            str {string} -- Text to display

            color {tuple(R,G,B,A)} -- Color of the text

            scale {float} -- Scale of the text to display. 

            width_scale {float} -- Width scale of the text to display. 

            spacing_scale {float} -- Spacing scale of the text to display. 
        """
        currentPos = Vector2(position[0] + self.size_x * 0.5 * self.scale * scale * width_scale, position[1] + self.size_y * 0.5 * self.scale * scale)

        self.render_at(screen, currentPos, str, color, scale, width_scale, spacing_scale)

    def render_to_centered(self, screen, position, str, color, scale, width_scale, spacing_scale):
        """Renders the given text on the screen, centered.
        
        Arguments:
            screen {int} -- Display surface handle

            position {tuple(x,y)} -- Position to render text, in pixel coordinates

            str {string} -- Text to display

            color {tuple(R,G,B,A)} -- Color of the text

            scale {float} -- Scale of the text to display. 

            width_scale {float} -- Width scale of the text to display. 

            spacing_scale {float} -- Spacing scale of the text to display. 
        """
        size = len(str) * self.size_x + (len(str) - 1) * self.spacing_x * spacing_scale

        currentPos = Vector2(position[0] - (size ) * 0.5 * self.scale * scale, position[1] + self.size_y * 0.5 * self.scale * scale)

        self.render_at(screen, currentPos, str, color, scale, width_scale, spacing_scale)

    @staticmethod
    def load(filename, size):
        """Loads a vector font from a JSON file.
        
        File is standard JSON with the following structure:
        ```
        {
            Size: Tuple with the size of the font
            Spacing: Tuple with the spacing between lines (vector fonts are monospaced)
            Characters.....
        }
        ```

        Characters are defined as follows:
        ```
        "<character>: { * Definition as in a normal WireMesh (check WireMesh documentation for format) * }
        ```
        
        Arguments:
            filename {string} -- Filename of file that contains the vector font.

            size {float} -- Scale of the font loaded (can be overwriten in individual calls)
        
        Returns:
            VectorFont -- Loaded font
        """
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
    """Font Manager singleton object.
    """
    instance = None
    """Singleton object"""

    def __init__(self):
        """Initializes the singleton"""
        if (FontManager.instance == None):
            FontManager.instance = self
        else:
            raise Exception("This class is a singleton!")

        self.fonts = dict()
            
    def _load(self, path, size, name):
        """Loads a font from the hard drive.
        
        Arguments:
            path {string} -- Filename of the font file. Format of font is defined by the file extension (.json for VectorFonts, everything else for any font supported by Pygame)

            size {float} -- Size or scale of the font to load

            name {string} -- Internal name of the font, so you can use it on the static draw text calls.
        
        Returns:
            [TTFont / VectorFont] -- Loaded font
        """
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
        """Writes the given text on the screen.
        
        Arguments:
            screen {int} -- Display surface handler

            name {string} -- Name of the font to use to draw

            str {string} -- String to display

            position {tuple(x,y)} -- Position of the text in screen coordinates

            color {tuple(R,G,B,A)} -- Color of the text
            
            scale {float} -- Scale of the text (only applicable on VectorFonts) (default: {1})

            width_scale {float} -- Width scale of the text (only applicable on VectorFonts) (default: {1})

            spacing_scale {float} -- Spacing scale of the text (only applicable on VectorFonts) (default: {1})
        """
        if (name in self.fonts):
            self.fonts[name].render_to(screen, position, str, color, scale, width_scale, spacing_scale)

    def _write_center(self, screen, name, str, position, color, scale = 1, width_scale = 1, spacing_scale = 1):
        """Writes the given text on the screen, centered on the given position.
        
        Arguments:
            screen {int} -- Display surface handler

            name {string} -- Name of the font to use to draw

            str {string} -- String to display

            position {tuple(x,y)} -- Position of the text in screen coordinates

            color {tuple(R,G,B,A)} -- Color of the text
        
            scale {float} -- Scale of the text (only applicable on VectorFonts) (default: {1})

            width_scale {float} -- Width scale of the text (only applicable on VectorFonts) (default: {1})
            
            spacing_scale {float} -- Spacing scale of the text (only applicable on VectorFonts) (default: {1})
        """
        if (name in self.fonts):
            self.fonts[name].render_to_centered(screen, position, str, color, scale, width_scale, spacing_scale)

    @staticmethod
    def get_instance():
        """Retrieves the singleton instance of the FontManager, or initializes one if there isn't one.
        
        Returns:
            FontManager -- Singleton of FontManager
        """
        if (FontManager.instance == None):
            gFnt = FontManager()
        
        return FontManager.instance

    @staticmethod
    def load(path, size, name):
        """Loads a font from the hard drive.
        
        Arguments:
            path {string} -- Filename of the font file. Format of font is defined by the file extension (.json for VectorFonts, everything else for any font supported by Pygame)

            size {float} -- Size or scale of the font to load

            name {string} -- Internal name of the font, so you can use it on the static draw text calls.
        
        Returns:
            [TTFont / VectorFont] -- Loaded font
        """
        return FontManager.get_instance()._load(path, size, name)

    @staticmethod
    def write(screen, name, str, position, color, scale = 1, width_scale = 1, spacing_scale = 1):
        """Writes the given text on the screen.
        
        Arguments:
            screen {int} -- Display surface handler

            name {string} -- Name of the font to use to draw

            str {string} -- String to display

            position {tuple(x,y)} -- Position of the text in screen coordinates

            color {tuple(R,G,B,A)} -- Color of the text
     
            scale {float} -- Scale of the text (only applicable on VectorFonts) (default: {1})
            
            width_scale {float} -- Width scale of the text (only applicable on VectorFonts) (default: {1})
            
            spacing_scale {float} -- Spacing scale of the text (only applicable on VectorFonts) (default: {1})
        """
        return FontManager.get_instance()._write(screen, name, str, position, color, scale, width_scale, spacing_scale)

    @staticmethod
    def write_center(screen, name, str, position, color, scale = 1, width_scale = 1, spacing_scale = 1):
        """Writes the given text on the screen, centered on the given position.
        
        Arguments:
            screen {int} -- Display surface handler

            name {string} -- Name of the font to use to draw

            str {string} -- String to display

            position {tuple(x,y)} -- Position of the text in screen coordinates

            color {tuple(R,G,B,A)} -- Color of the text
        
            scale {float} -- Scale of the text (only applicable on VectorFonts) (default: {1})

            width_scale {float} -- Width scale of the text (only applicable on VectorFonts) (default: {1})
            
            spacing_scale {float} -- Spacing scale of the text (only applicable on VectorFonts) (default: {1})
        """
        return FontManager.get_instance()._write_center(screen, name, str, position, color, scale, width_scale, spacing_scale)

