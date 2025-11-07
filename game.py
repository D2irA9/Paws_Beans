from globals import *
from classes.tiled import Map

""" Переменные """
map = Map('assets/tiled/tmx/coffee_house.tmx', 48, 1)

def game():
    map.load_map()
    map.draw(screen)