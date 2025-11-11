from globals import *
from classes.tiled import Map
from classes.character import Player
from classes.node import Button

# # # Карты
coffee_house_map = Map('assets/tiled/tmx/coffee_house.tmx', 48, 1)

stations1_map = Map('assets/tiled/tmx/stations1.tmx', 48, 1)
stations2_map = Map('assets/tiled/tmx/stations2.tmx', 48, 1)
stations3_map = Map('assets/tiled/tmx/stations3.tmx', 48, 1)

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
button_left  = Button(300, 100, BLUE, (0, 620))
button_right  = Button(300, 100, ORANGE, (900, 620))

def game(events):
    global map_loaded, current_status

    for event in events:
        if event.type == py.QUIT:
            py.quit()
            sys.exit()
        elif event.type == py.MOUSEBUTTONDOWN:
            if button_right.signal(event.pos):
                # Если coffee_house
                if current_status == condition[0]:
                    current_status = condition[1]
                # Если stations1
                elif current_status == condition[1]:
                    current_status = condition[0]
                # Если stations2
                elif current_status == condition[2]:
                    current_status = condition[1]
                # Если stations3
                else:
                    current_status = condition[2]

            if button_left.signal(event.pos):
                # Если stations1
                if current_status == condition[1]:
                    current_status = condition[2]
                # Если stations2
                elif current_status == condition[2]:
                    current_status = condition[3]

    if not map_loaded:
        coffee_house_map.load_map()
        stations1_map.load_map()
        stations2_map.load_map()
        stations3_map.load_map()
        map_loaded = True

    # Если coffee_house
    if current_status == condition[0]:
        coffee_house_map.draw(screen)
        player.update()
        player.draw(screen)
        button_right.draw(screen)
    # Если stations1
    elif current_status == condition[1]:
        stations1_map.draw(screen)
        button_right.draw(screen)
        button_left.draw(screen)
    # Если stations2
    elif current_status == condition[2]:
        stations2_map.draw(screen)
        button_right.draw(screen)
        button_left.draw(screen)
    # Если stations3
    else:
        stations3_map.draw(screen)
        button_right.draw(screen)