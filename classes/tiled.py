import pygame as py
from pytmx import load_pygame

class Tile(py.sprite.Sprite):
    """ Класс Плиток карты """
    def __init__(self, pos, surf, groups, scale, tile_size):
        self.tile_size = tile_size
        super().__init__(groups)
        if surf is not None:
            self.image = py.transform.scale(surf, (int(surf.get_width() * scale), int(surf.get_height() * scale)))
            self.rect = self.image.get_rect(topleft=pos)
        else:
            self.image = py.Surface((int(self.tile_size * scale), int(self.tile_size * scale)))
            self.image.fill((255, 0, 0))
            self.rect = self.image.get_rect(topleft=pos)

        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect

class Map:
    """ Класс Карты """
    def __init__(self, tmx_path, tile_size, scale):
        self.tile_size = tile_size
        self.scale = scale
        self.tile_group = py.sprite.Group()
        self.tmx_path = tmx_path

    def load_map(self):
        """ Загрузка карты """
        map = load_pygame(self.tmx_path)

        for layer in map.visible_layers:
            if hasattr(layer, 'data'):
                for x, y, surf in layer.tiles():
                    pos = (x * self.tile_size * self.scale, y * self.tile_size * self.scale)
                    Tile(pos=pos, surf = surf, groups=self.tile_group, scale=self.scale, tile_size=self.tile_size)

    def draw(self, screen):
        """ Отрисовка всей карты """
        for tile in self.tile_group:
            screen.blit(tile.image, (tile.rect.x, tile.rect.y))