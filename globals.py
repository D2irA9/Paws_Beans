# # # Глобальные переменные
import pygame as py, sys
from classes.Node import Label

py.init()
screen = py.display.set_mode((1200, 720))
py.display.set_caption('Paws & Beans')

# # # Цвет
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (100, 100, 255)
GRAY = (128, 128, 128)

# # # Переменные
font = Label('assets/font/PixelizerBold.ttf')