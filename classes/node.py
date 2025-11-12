import pygame as py

class Label:
    """ Текст """
    def __init__(self, font_path):
        self.font_path = font_path

    def text_ret(self, size, text, color, antialias=True):
        """ Создание переменной текста """  
        lable = py.font.Font(self.font_path, size)
        return lable.render(text, antialias, color)

class Button:
    """ Кнопки """
    def __init__(self, width, height, bg_color, pos):
        self.width = width
        self.height = height
        self.bg_color = bg_color
        self.pos = pos
        self.border_width = 3
        self.image = py.Surface((self.width, self.height))
        self.image.fill(bg_color)
        py.draw.rect(self.image, (58, 58, 80), (0, 0, self.width, self.height), self.border_width)
        self.rect = self.image.get_rect(topleft=self.pos)

    def redraw(self):
        """ Перерисовка с новым цветом """
        self.image = py.Surface((self.width, self.height))
        self.image.fill(self.bg_color)
        py.draw.rect(self.image, (58, 58, 80), (0, 0, self.width, self.height), self.border_width)
        self.rect = self.image.get_rect(topleft=self.pos)

    def change_color(self, new_color):
        """ Получаем новый цвет """
        self.bg_color = new_color
        self.redraw()

    def draw(self, screen):
        """ Отображение кнопки """
        screen.blit(self.image, self.rect)

    def signal(self, pos):
        """ Получение сигнала """
        return self.rect.collidepoint(pos)

class CircleButton:
    """ Круглые кнопки """
    def __init__(self, radius, bg_color, pos):
        self.radius = radius
        self.bg_color = bg_color
        self.pos = pos
        self.border_width = 3

        diameter = radius * 2
        self.image = py.Surface((diameter, diameter), py.SRCALPHA)
        self.redraw()
        self.rect = self.image.get_rect(center=pos)

    def redraw(self):
        """ Перерисовка кнопки """
        diameter = self.radius * 2
        self.image.fill((0, 0, 0, 0))
        py.draw.circle(self.image, self.bg_color, (self.radius, self.radius), self.radius)
        py.draw.circle(self.image, (58, 58, 80), (self.radius, self.radius), self.radius, self.border_width)

    def change_color(self, new_color):
        """ Смена цвета """
        self.bg_color = new_color
        self.redraw()

    def draw(self, screen):
        """ Отрисовка кнопки """
        screen.blit(self.image, self.rect)

    def signal(self, pos):
        """ Получение сигнала"""
        distance = ((pos[0] - self.rect.centerx) ** 2 + (pos[1] - self.rect.centery) ** 2) ** 0.5
        return  distance <= self.radius