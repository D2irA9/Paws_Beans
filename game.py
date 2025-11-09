from globals import *
from classes.tiled import Map
from classes.character import Player
from classes.node import Button

# # # Переменные
map = Map('assets/tiled/tmx/coffee_house.tmx', 48, 1)
map_loaded = False # Флаг для проверки загрузки карты

player = Player(3, (530, 60))

start  = Button(300, 100, ORANGE, (900, 620))

def game(events):
    global map_loaded

    for event in events:
        if event.type == py.QUIT:
            py.quit()
            sys.exit()

        if event.type == py.MOUSEBUTTONDOWN:
            if start.signal(event.pos):
                print('Сигнал получен ')

    if not map_loaded:
        map.load_map()
        map_loaded = True

    map.draw(screen)
    player.update()
    player.draw(screen)
    start.draw(screen)