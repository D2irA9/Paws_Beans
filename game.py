from globals import *
from classes.tiled import Map
from classes.character import Character
from classes.node import Button, CircleButton
from  classes.recipe import Recipe

# # # Карты
coffee_house_map = Map('assets/tiled/tmx/coffee_house.tmx', 48, 1)
map_loaded = False # - Флаг для проверки загрузки карт

# Все состояния
condition = [
    'coffee_house',
    'station 1',
    'station 2',
    'station 3',
]
current_status = condition[0]

# # # Игрок
player = Character(3, (530, 60), 'assets/sprites/characters/Adam_16x16.png', [(530,60)])

# # # NPS
nps = Character(3, (240, 0), 'assets/sprites/characters/Alex_16x16.png', [(240, 140), (530, 140), (530, 120)])

# # # Кнопки
# Баковые кнопки
button_left  = Button(300, 100, BLUE, (0, 620))
button_left_S = False
button_right  = Button(300, 100, ORANGE, (900, 620))

def game(events):
    global map_loaded, current_status, button_left_S

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
                # Если stations3
                elif current_status == condition[3]:
                    animate_finish = True
                    current_status = condition[0]

    # Проверка загружена ли карта
    if not map_loaded:
        coffee_house_map.load_map()
        map_loaded = True

    # Если coffee_house
    if current_status == condition[0]:
        button_left_S = False
        coffee_house_map.draw(screen)
        player.update()
        player.draw(screen)
        nps.update()
        nps.draw(screen)
        button_right.change_color(ORANGE)

    # Если stations1
    elif current_status == condition[1]:
        screen.fill(ORANGE1)
        button_right.change_color(GREEN)
        button_left_S = True
        button_left.change_color(BLUE)

    # Если stations2
    elif current_status == condition[2]:
        screen.fill(BLUE1)
        button_right.change_color(ORANGE)
        button_left_S = True
        button_left.change_color(VIOLET)

    # Если stations3
    else:
        screen.fill(VIOLET1)
        button_left_S = False
        button_right.change_color(BLUE)

    # Прорисовка кнопок
    button_right.draw(screen)
    if button_left_S:
        button_left.draw(screen)