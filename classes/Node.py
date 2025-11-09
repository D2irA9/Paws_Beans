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
        self.image = py.Surface((width, height))
        self.image.fill(bg_color)
        self.rect = self.image.get_rect(topleft=pos)

    def draw(self, screen):
        """ Отображение кнопки """
        screen.blit(self.image, self.rect)

    def signal(self, pos):
        """ Получение сигнала """
        return self.rect.collidepoint(pos)