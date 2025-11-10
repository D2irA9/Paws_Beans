from globals import *
from classes.tiled import Map
from classes.character import Player
from classes.node import Button

# # # Карты
coffee_house_map = Map('assets/tiled/tmx/coffee_house.tmx', 48, 1)
stations_map = Map('assets/tiled/tmx/stations.tmx', 48, 1)
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

# # # Кнопки
button_left  = Button(300, 100, ORANGE, (900, 620))
# button_right  = Button(300, 100, ORANGE, (0, 620))

def game(events):
    global map_loaded, current_status

    for event in events:
        if event.type == py.QUIT:
            py.quit()
            sys.exit()
        elif event.type == py.MOUSEBUTTONDOWN:
            if button_left.signal(event.pos):
                if current_status == condition[0]:
                    current_status = condition[1]
                    button_left.change_color(GREEN)
                elif current_status == condition[1]:
                    current_status = condition[0]
                    button_left.change_color(ORANGE)

    if not map_loaded:
        coffee_house_map.load_map()
        stations_map.load_map()
        map_loaded = True

    if current_status == condition[0]:
        coffee_house_map.draw(screen)
        player.update()
        player.draw(screen)
    elif current_status == condition[1]:
        stations_map.draw(screen)

    button_left.draw(screen)