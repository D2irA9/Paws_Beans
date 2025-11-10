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
GREEN = (76,187,23)
BLUE = (100, 100, 255)
VIOLET = (153,50,204)

CONTOUR = (58, 58, 80)

# # # Переменные
font = Label('assets/font/PixelizerBold.ttf')