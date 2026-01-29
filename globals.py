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

RED = (225, 0, 0)

ORANGE = (255,165,0)
ORANGE1 = (255, 228, 179)
ORANGE_fon = (238, 144, 51)

YELLOW =(242, 245, 64)

GREEN = (76,187,23)
GREEN1 = (172, 241, 138)

BLUE = (66,170,255)
BLUE1 = (189, 226, 255)

VIOLET = (153,50,204)
VIOLET1 = (218, 181, 237)

CONTOUR = (58, 58, 80)

# Молоко
SKIM_MILK = (248, 248, 248)
STRAWBERRY_MILK = (228, 172, 195)
# Эспрессо
CITY_ROAST = (110, 59, 9)
DECAF_ROAST = (70, 39, 6)

# # # Переменные
font = Label('assets/font/PixelizerBold.ttf')