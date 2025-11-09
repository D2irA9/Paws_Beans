import pygame as py

class Player(py.sprite.Sprite):
    """ Класс Игрока """
    def __init__(self, scale, pos):
        super().__init__()
        self.width_spr = 16
        self.height_spr = 32
        self.scale =scale
        self.sprite = py.image.load('assets/sprites/characters/Adam_16x16.png').convert_alpha()
        self.animation_speed = 0.9
        self.animations = {
            'idle': [
                py.transform.scale(self.sprite.subsurface((288, 32, self.width_spr, self.height_spr)), (self.width_spr * self.scale, self.height_spr * self.scale)),
                py.transform.scale(self.sprite.subsurface((304, 32, self.width_spr, self.height_spr)), (self.width_spr * self.scale, self.height_spr * self.scale)),
                py.transform.scale(self.sprite.subsurface((320, 32, self.width_spr, self.height_spr)), (self.width_spr * self.scale, self.height_spr * self.scale)),
                py.transform.scale(self.sprite.subsurface((336, 32, self.width_spr, self.height_spr)), (self.width_spr * self.scale, self.height_spr * self.scale)),
                py.transform.scale(self.sprite.subsurface((352, 32, self.width_spr, self.height_spr)), (self.width_spr * self.scale, self.height_spr * self.scale)),
                py.transform.scale(self.sprite.subsurface((368, 32, self.width_spr, self.height_spr)), (self.width_spr * self.scale, self.height_spr * self.scale)),
            ]
        }
        self.pos = pos
        self.last_update = py.time.get_ticks()
        self.current_animation = 'idle'
        self.current_frame = 0
        self.image = self.animations[self.current_animation][self.current_frame]
        self.rect = self.image.get_rect(topleft=pos)

    def update(self):
        """ Обновление анимации """
        now = py.time.get_ticks()
        if now - self.last_update > 100:
            self.current_frame = (self.current_frame + 1) % len(self.animations[self.current_animation])
            self.image = self.animations[self.current_animation][self.current_frame]
            self.last_update = now


    def draw(self, screen):
        """ Отображение игрока """
        screen.blit(self.image, self.rect)
