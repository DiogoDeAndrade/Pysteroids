import pygame

class SpriteInfo:
    def __init__(self):
        self.sprites = []

    def load_image(self, filename, hotspot):
        img = dict()
        img["hotspot"] = hotspot
        img["surface"] = pygame.image.load(filename)
        self.sprites.append(img)

    def draw(self, screen, index, position):
        img = self.sprites[index]["surface"]
        hotspot = self.sprites[index]["hotspot"]
        pos = position - hotspot
        screen.blit(img, pos)

    def rescale(self, scale):
        for idx, img in enumerate(self.sprites):
            size = img["surface"].get_size()
            surface = img["surface"]
            size = ((int)(size[0] * scale), (int)(size[1] * scale))
            img["surface"] = pygame.transform.scale(surface,size)
