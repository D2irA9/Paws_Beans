from globals import *
from classes.tiled import Map
from classes.character import Player
from classes.node import Button

# # # Переменные
coffee_house = Map('assets/tiled/tmx/coffee_house.tmx', 48, 1)
stations = Map('assets/tiled/tmx/stations.tmx', 48, 1)
map_loaded = False # Флаг для проверки загрузки карт
condition = 'coffee_house'

player = Player(3, (530, 60))

start  = Button(300, 100, ORANGE, (900, 620))

def game(events):
    global map_loaded, condition

    for event in events:
        if event.type == py.QUIT:
            py.quit()
            sys.exit()

        if event.type == py.MOUSEBUTTONDOWN:
            if start.signal(event.pos):
                print('Сигнал получен ')
                condition = 'stations'

    if not map_loaded:
        coffee_house.load_map()
        stations.load_map()
        map_loaded = True

    if condition == 'coffee_house':
        coffee_house.draw(screen)
        player.update()
        player.draw(screen)
    else:
        stations.draw(screen)
    start.draw(screen)