# # # Глобальные переменные
import pygame as py, sys
from classes.node import Label

py.init()
screen = py.display.set_mode((1200, 720))
py.display.set_caption('Paws & Beans')

# # # Цвет
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)

ORANGE = (255,165,0)
ORANGE1 = (255, 228, 179)

GREEN = (76,187,23)
GREEN1 = (172, 241, 138)

BLUE = (66,170,255)
BLUE1 = (189, 226, 255)

VIOLET = (153,50,204)
VIOLET1 = (218, 181, 237)

CONTOUR = (58, 58, 80)

# # # Переменные
font = Label('assets/font/PixelizerBold.ttf')