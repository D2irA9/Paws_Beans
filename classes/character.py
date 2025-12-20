import pygame as py

class Character(py.sprite.Sprite):
    """ Класс Персонажей """
    def __init__(self, scale, pos, sprite_path, path=None):
        super().__init__()
        self.width_spr = 16
        self.height_spr = 32
        self.scale = scale
        self.speed = 2
        self.sprite = py.image.load(sprite_path).convert_alpha()
        self.animations = {
            'idle_down': self.load_animation_frames(32, 288, 6),
            'idle_up': self.load_animation_frames(32, 96, 6),
            'idle_left': self.load_animation_frames(32, 192, 6),
            'idle_right': self.load_animation_frames(32, 0, 6),

            'walk_down': self.load_animation_frames(64, 288, 6),
            'walk_up': self.load_animation_frames(64, 96, 6),
            'walk_left': self.load_animation_frames(64, 192, 6),
            'walk_right': self.load_animation_frames(64, 0, 6),
        }
        self.current_animation = 'idle_down'
        self.current_frame = 0
        self.pos = list(pos)
        self.last_update = py.time.get_ticks()
        self.image = self.animations[self.current_animation][self.current_frame]
        self.rect = self.image.get_rect(topleft=pos)
        self.path = path or []
        self.current_path_index = 0
        self.is_moving = bool(self.path)
        self.target_pos = None
        if self.path:
            self.target_pos = self.path[0]

    def load_animation_frames(self, start_y, start_x, frame_count):
        """ Загрузка кадров анимации """
        frames = []
        for i in range(frame_count):
            x = start_x + (i * self.width_spr)
            frame = self.sprite.subsurface((x, start_y, self.width_spr, self.height_spr))
            scaled_frame = py.transform.scale(frame, (self.width_spr * self.scale, self.height_spr * self.scale))
            frames.append(scaled_frame)
        return frames

    def set_path(self, new_path):
        """ Установить новый путь """
        self.path = new_path
        self.current_path_index = 0
        self.is_moving = bool(new_path)
        if new_path:
            self.target_pos = new_path[0]
            self.start_moving_to_target()

    def start_moving_to_target(self):
        """ Начать движение к текущей цели """
        if self.current_path_index < len(self.path):
            self.target_pos = self.path[self.current_path_index]
            self.is_moving = True

    def update(self):
        """ Обновление анимация + движение """
        now = py.time.get_ticks()
        if now - self.last_update > 100:
            self.current_frame = (self.current_frame + 1) % len(self.animations[self.current_animation])
            self.image = self.animations[self.current_animation][self.current_frame]
            self.last_update = now
        if self.is_moving and self.target_pos:
            self.move_to_target()

    def move_to_target(self):
        """ Плавное движение к целевой точке """
        target_x, target_y = self.target_pos
        dx = target_x - self.pos[0]
        dy = target_y - self.pos[1]
        distance = (dx ** 2 + dy ** 2) ** 0.5
        if distance < self.speed:
            self.pos[0] = target_x
            self.pos[1] = target_y
            self.go_to_next_target()
        else:
            move_x = (dx / distance) * self.speed
            move_y = (dy / distance) * self.speed
            self.pos[0] += move_x
            self.pos[1] += move_y
            self.update_walking_animation(move_x, move_y)

        self.rect.x = int(self.pos[0])
        self.rect.y = int(self.pos[1])

    def update_walking_animation(self, dx, dy):
        """ Обновляет анимацию ходьбы в зависимости от направления """
        if abs(dx) > abs(dy):
            if dx > 0:
                self.current_animation = 'walk_right'
            else:
                self.current_animation = 'walk_left'
        else:
            if dy > 0:
                self.current_animation = 'walk_down'
            else:
                self.current_animation = 'walk_up'

    def go_to_next_target(self):
        """ Переход к следующей точке пути """
        self.current_path_index += 1
        if self.current_path_index < len(self.path):
            self.target_pos = self.path[self.current_path_index]
        else:
            self.is_moving = False
            self.path = []
            self.current_path_index = 0
            if 'walk' in self.current_animation:
                self.current_animation = self.current_animation.replace('walk', 'idle')

    def draw(self, screen):
        """ Отрисовка """
        screen.blit(self.image, self.rect)



