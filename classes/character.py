import pygame as py

class Player(py.sprite.Sprite):
    """ Класс Игрока """
    def __init__(self, scale, pos):
        super().__init__()
        self.width_spr = 16
        self.height_spr = 32
        self.scale = scale
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

class Nps(py.sprite.Sprite):
    """ Класс NPC """
    def __init__(self, scale, pos, path=None):
        super().__init__()
        self.width_spr = 16
        self.height_spr = 32
        self.scale = scale
        self.sprite = py.image.load(path).convert_alpha()
        self.animations = {
            'idle_right':[
                py.transform.scale(self.sprite.subsurface((0, 32, self.width_spr, self.height_spr)),(self.width_spr * self.scale, self.height_spr * self.scale)),
                py.transform.scale(self.sprite.subsurface((16, 32, self.width_spr, self.height_spr)),(self.width_spr * self.scale, self.height_spr * self.scale)),
                py.transform.scale(self.sprite.subsurface((32, 32, self.width_spr, self.height_spr)),(self.width_spr * self.scale, self.height_spr * self.scale)),
                py.transform.scale(self.sprite.subsurface((48, 32, self.width_spr, self.height_spr)),(self.width_spr * self.scale, self.height_spr * self.scale)),
                py.transform.scale(self.sprite.subsurface((64, 32, self.width_spr, self.height_spr)),(self.width_spr * self.scale, self.height_spr * self.scale)),
                py.transform.scale(self.sprite.subsurface((80, 32, self.width_spr, self.height_spr)),(self.width_spr * self.scale, self.height_spr * self.scale)),
            ],
            'idle_up':[
                py.transform.scale(self.sprite.subsurface((96, 32, self.width_spr, self.height_spr)),(self.width_spr * self.scale, self.height_spr * self.scale)),
                py.transform.scale(self.sprite.subsurface((112, 32, self.width_spr, self.height_spr)),(self.width_spr * self.scale, self.height_spr * self.scale)),
                py.transform.scale(self.sprite.subsurface((128, 32, self.width_spr, self.height_spr)),(self.width_spr * self.scale, self.height_spr * self.scale)),
                py.transform.scale(self.sprite.subsurface((144, 32, self.width_spr, self.height_spr)),(self.width_spr * self.scale, self.height_spr * self.scale)),
                py.transform.scale(self.sprite.subsurface((160, 32, self.width_spr, self.height_spr)),(self.width_spr * self.scale, self.height_spr * self.scale)),
                py.transform.scale(self.sprite.subsurface((176, 32, self.width_spr, self.height_spr)),(self.width_spr * self.scale, self.height_spr * self.scale)),
            ],
            'idle_left':[
                py.transform.scale(self.sprite.subsurface((192, 32, self.width_spr, self.height_spr)),(self.width_spr * self.scale, self.height_spr * self.scale)),
                py.transform.scale(self.sprite.subsurface((208, 32, self.width_spr, self.height_spr)),(self.width_spr * self.scale, self.height_spr * self.scale)),
                py.transform.scale(self.sprite.subsurface((224, 32, self.width_spr, self.height_spr)),(self.width_spr * self.scale, self.height_spr * self.scale)),
                py.transform.scale(self.sprite.subsurface((240, 32, self.width_spr, self.height_spr)),(self.width_spr * self.scale, self.height_spr * self.scale)),
                py.transform.scale(self.sprite.subsurface((256, 32, self.width_spr, self.height_spr)),(self.width_spr * self.scale, self.height_spr * self.scale)),
                py.transform.scale(self.sprite.subsurface((272, 32, self.width_spr, self.height_spr)),(self.width_spr * self.scale, self.height_spr * self.scale)),
            ],
            'idle_down':[
                py.transform.scale(self.sprite.subsurface((288, 32, self.width_spr, self.height_spr)),(self.width_spr * self.scale, self.height_spr * self.scale)),
                py.transform.scale(self.sprite.subsurface((304, 32, self.width_spr, self.height_spr)),(self.width_spr * self.scale, self.height_spr * self.scale)),
                py.transform.scale(self.sprite.subsurface((320, 32, self.width_spr, self.height_spr)),(self.width_spr * self.scale, self.height_spr * self.scale)),
                py.transform.scale(self.sprite.subsurface((336, 32, self.width_spr, self.height_spr)),(self.width_spr * self.scale, self.height_spr * self.scale)),
                py.transform.scale(self.sprite.subsurface((352, 32, self.width_spr, self.height_spr)),(self.width_spr * self.scale, self.height_spr * self.scale)),
                py.transform.scale(self.sprite.subsurface((368, 32, self.width_spr, self.height_spr)),(self.width_spr * self.scale, self.height_spr * self.scale)),
            ],
            'right':[
                py.transform.scale(self.sprite.subsurface((0, 64, self.width_spr, self.height_spr)),(self.width_spr * self.scale, self.height_spr * self.scale)),
                py.transform.scale(self.sprite.subsurface((16, 64, self.width_spr, self.height_spr)),(self.width_spr * self.scale, self.height_spr * self.scale)),
                py.transform.scale(self.sprite.subsurface((32, 64, self.width_spr, self.height_spr)),(self.width_spr * self.scale, self.height_spr * self.scale)),
                py.transform.scale(self.sprite.subsurface((48, 64, self.width_spr, self.height_spr)),(self.width_spr * self.scale, self.height_spr * self.scale)),
                py.transform.scale(self.sprite.subsurface((64, 64, self.width_spr, self.height_spr)),(self.width_spr * self.scale, self.height_spr * self.scale)),
                py.transform.scale(self.sprite.subsurface((80, 64, self.width_spr, self.height_spr)),(self.width_spr * self.scale, self.height_spr * self.scale)),
            ],
            'up':[
                py.transform.scale(self.sprite.subsurface((96, 64, self.width_spr, self.height_spr)),(self.width_spr * self.scale, self.height_spr * self.scale)),
                py.transform.scale(self.sprite.subsurface((112, 64, self.width_spr, self.height_spr)),(self.width_spr * self.scale, self.height_spr * self.scale)),
                py.transform.scale(self.sprite.subsurface((128, 64, self.width_spr, self.height_spr)),(self.width_spr * self.scale, self.height_spr * self.scale)),
                py.transform.scale(self.sprite.subsurface((144, 64, self.width_spr, self.height_spr)),(self.width_spr * self.scale, self.height_spr * self.scale)),
                py.transform.scale(self.sprite.subsurface((160, 64, self.width_spr, self.height_spr)),(self.width_spr * self.scale, self.height_spr * self.scale)),
                py.transform.scale(self.sprite.subsurface((176, 64, self.width_spr, self.height_spr)),(self.width_spr * self.scale, self.height_spr * self.scale)),
            ],
            'left':[
                py.transform.scale(self.sprite.subsurface((192, 64, self.width_spr, self.height_spr)),(self.width_spr * self.scale, self.height_spr * self.scale)),
                py.transform.scale(self.sprite.subsurface((208, 64, self.width_spr, self.height_spr)),(self.width_spr * self.scale, self.height_spr * self.scale)),
                py.transform.scale(self.sprite.subsurface((224, 64, self.width_spr, self.height_spr)),(self.width_spr * self.scale, self.height_spr * self.scale)),
                py.transform.scale(self.sprite.subsurface((240, 64, self.width_spr, self.height_spr)),(self.width_spr * self.scale, self.height_spr * self.scale)),
                py.transform.scale(self.sprite.subsurface((256, 64, self.width_spr, self.height_spr)),(self.width_spr * self.scale, self.height_spr * self.scale)),
                py.transform.scale(self.sprite.subsurface((272, 64, self.width_spr, self.height_spr)),(self.width_spr * self.scale, self.height_spr * self.scale)),
            ],
            'down':[
                py.transform.scale(self.sprite.subsurface((288, 64, self.width_spr, self.height_spr)),(self.width_spr * self.scale, self.height_spr * self.scale)),
                py.transform.scale(self.sprite.subsurface((304, 64, self.width_spr, self.height_spr)),(self.width_spr * self.scale, self.height_spr * self.scale)),
                py.transform.scale(self.sprite.subsurface((320, 64, self.width_spr, self.height_spr)),(self.width_spr * self.scale, self.height_spr * self.scale)),
                py.transform.scale(self.sprite.subsurface((336, 64, self.width_spr, self.height_spr)),(self.width_spr * self.scale, self.height_spr * self.scale)),
                py.transform.scale(self.sprite.subsurface((352, 64, self.width_spr, self.height_spr)),(self.width_spr * self.scale, self.height_spr * self.scale)),
                py.transform.scale(self.sprite.subsurface((368, 64, self.width_spr, self.height_spr)),(self.width_spr * self.scale, self.height_spr * self.scale)),
            ],
        }
        self.current_animation = 'idle_down'
        self.current_frame = 0
        self.animations_speed = 0.9
        self.pos = pos
        self.last_update = py.time.get_ticks()
        self.image = self.animations[self.current_animation][self.current_frame]
        self.rect = self.image.get_rect(topleft=pos)
        # Маршрут
        self.route = []
        self.current_path_index = 0
        self.path_completed = False





