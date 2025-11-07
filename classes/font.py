import pygame as py

class Font:
    def __init__(self, font_path):
        self.font_path = font_path

    def text_ret(self, size = 36,text = 'None', antialias=True, color=(255, 255,255)):
        """ Создание переменной текста """  
        lable = py.font.Font(self.font_path, size)
        return lable.render(text, antialias, color)