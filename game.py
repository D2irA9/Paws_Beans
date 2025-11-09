from globals import *
from classes.tiled import Map
from classes.character import Player
from classes.node import Button

# # # Карты
coffee_house = Map('assets/tiled/tmx/coffee_house.tmx', 48, 1)
stations = Map('assets/tiled/tmx/stations.tmx', 48, 1)
map_loaded = False # Флаг для проверки загрузки карт

# Все состояния
condition = [
    'coffee_house',
    'station 1',
    'station 2',
    'station 3',
]
current_status = condition[0]
# # # Игрок
player = Player(3, (530, 60))

# # # Узлы
start  = Button(300, 100, ORANGE, (900, 620))

def game(events):
    global map_loaded, current_status

    for event in events:
        if event.type == py.QUIT:
            py.quit()
            sys.exit()
        elif event.type == py.MOUSEBUTTONDOWN:
            if start.signal(event.pos):
                if current_status == condition[0]:
                    current_status = condition[1]
                elif current_status == condition[1]:
                    current_status = condition[0]

    if not map_loaded:
        coffee_house.load_map()
        stations.load_map()
        map_loaded = True

    if current_status == condition[0]:
        coffee_house.draw(screen)
        player.update()
        player.draw(screen)
    elif current_status == condition[1]:
        stations.draw(screen)

    start.draw(screen)