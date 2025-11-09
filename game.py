from globals import *
from classes.tiled import Map
from classes.character import Player
from classes.Node import Button

# # # Переменные
map = Map('assets/tiled/tmx/coffee_house.tmx', 48, 1)
player = Player(3, (530, 60))

start  = Button(300, 100, WHITE, (300, 300))

def game():
    map.load_map()
    map.draw(screen)
    player.update()
    player.draw(screen)