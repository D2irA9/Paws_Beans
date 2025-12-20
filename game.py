from globals import *
from classes.tiled import Map
from classes.character import Player
from classes.node import Button, CircleButton
from  classes.recipe import Recipe

# # # Карты
coffee_house_map = Map('assets/tiled/tmx/coffee_house.tmx', 48, 1)
map_loaded = False # Флаг для проверки загрузки карт

# Все состояния
condition = [
    'coffee_house',
    'station 1',
    'station 2',
    'station 3',
    'station 4'
]
current_status = condition[0]

# # # Игрок
player = Player(3, (530, 60))

# # # Заказ
recipe = Recipe()
order = recipe.generate_random_order()

# # # Кнопки
# Баковые кнопки
button_left  = Button(300, 100, BLUE, (0, 620))
button_left_S = False
button_right  = Button(300, 100, ORANGE, (900, 620))
button_right_S = True

def game(events):
    global map_loaded, current_status, button_left_S, button_right_S

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
                    current_status = condition[2]
                # Если stations2
                elif current_status == condition[2]:
                    current_status = condition[3]
                # Если stations3
                elif current_status == condition[3]:
                    current_status = condition[4]
                # Если stations4
                else:
                    current_status = condition[3]

            if button_left.signal(event.pos):
                # Если stations1
                if current_status == condition[1]:
                    current_status = condition[0]
                # Если stations2
                elif current_status == condition[2]:
                    current_status = condition[1]
                # Если stations3
                elif current_status == condition[3]:
                    current_status = condition[2]
                # Если stations4
                else:
                    current_status = condition[3]

    # Проверка загружена ли карта
    if not map_loaded:
        coffee_house_map.load_map()
        map_loaded = True

    # Если coffee_house
    if current_status == condition[0]:
        coffee_house_map.draw(screen)
        player.update()
        player.draw(screen)
        button_right.change_color(GREEN)
        button_left_S = False

    # Если stations1
    elif current_status == condition[1]:
        screen.fill(GREEN1)
        button_left_S = True
        button_right.change_color(ORANGE)
        button_left.change_color(WHITE)
        recipe.draw_order(screen, [1000, 0], WHITE, CONTOUR, font, BLACK, order)

    # Если stations2
    elif current_status == condition[2]:
        screen.fill(ORANGE1)
        button_left_S = True
        button_left.change_color(GREEN)
        button_right.change_color(BLUE)
        recipe.draw_order(screen, [1000, 0], WHITE, CONTOUR, font, BLACK, order)

    # Если stations3
    elif current_status == condition[3]:
        screen.fill(BLUE1)
        button_left.change_color(ORANGE)
        button_right.change_color(VIOLET)
        button_right_S = True
        recipe.draw_order(screen, [1000, 0], WHITE, CONTOUR, font, BLACK, order)

    # Если stations4
    elif current_status == condition[4]:
        screen.fill(VIOLET1)
        button_left_S = True
        button_left.change_color(BLUE)
        button_right_S = False
        recipe.draw_order(screen, [1000, 0], WHITE, CONTOUR, font, BLACK, order)


    # Прорисовка кнопок
    if button_left_S:
        button_left.draw(screen)
    if button_right_S:
        button_right.draw(screen)

    print(recipe.glass)
