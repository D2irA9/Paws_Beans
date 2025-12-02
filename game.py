from globals import *
from classes.tiled import Map
from classes.character import Player
from classes.node import Button, CircleButton
from  classes.recipe import Recipe

# # # Карты
coffee_house_map = Map('assets/tiled/tmx/coffee_house.tmx', 48, 1)
# stations1_map = Map('assets/tiled/tmx/stations1.tmx', 48, 1)
# stations2_map = Map('assets/tiled/tmx/stations2.tmx', 48, 1)
# stations3_map = Map('assets/tiled/tmx/stations3.tmx', 48, 1)

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

# # # Заказ
r = Recipe()
order = r.generate_random_order()
# print(f"Чашка: {order['cup']}, Молоко: {order['milk']}({order["SM"]}), Эспрессо: {order['espresso']}({order["SE"]})")
cup = order['cup']
SM = order["SM"]
SE = order["SE"]
# print(cup, SM, SE)
def draw_order(screen, cup, SM, SE):
    """Отрисовка заказа"""
    x, y, width, height = 1000, 0, 200, 300

    py.draw.rect(screen, WHITE, (x, y, width, height))
    py.draw.rect(screen, CONTOUR, (x, y, width, height), 3)

    lines = [
        f"Чашка: {cup}",
        f"Молоко: {SM}",
        f"Эспрессо: {SE}"
    ]

    text_surfaces = []
    for line in lines:
        text_surface = font.text_ret(size=32, text=line, color=BLACK)
        text_surfaces.append(text_surface)

    line_height = 40
    start_y = y + 30

    for i, text_surface in enumerate(text_surfaces):
        text_rect = text_surface.get_rect()
        text_rect.centerx = x + width // 2
        text_rect.y = start_y + i * line_height
        screen.blit(text_surface, text_rect)

# # # Кнопки
# Баковые кнопки
button_left  = Button(300, 100, BLUE, (0, 620))
button_left_S = False
button_right  = Button(300, 100, ORANGE, (900, 620))
#
circle_btn_S = CircleButton(35, ORANGE, (500, 350))
circle_btn_S_signal = False
circle_btn_M = CircleButton(35, GREEN, (600, 350))
# circle_btn_M_signal = False
circle_btn_L = CircleButton(35, VIOLET, (700, 350))
# circle_btn_L_signal = False

def game(events):
    global map_loaded, current_status, button_left_S, circle_btn_S_signal

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

            if circle_btn_S.signal(event.pos):
                print("!!!S")
            elif circle_btn_M.signal(event.pos):
                print("!!!M")
            elif circle_btn_L.signal(event.pos):
                print("!!!L")

            if button_left.signal(event.pos):
                # Если stations1
                if current_status == condition[1]:
                    current_status = condition[2]
                # Если stations2
                elif current_status == condition[2]:
                    current_status = condition[3]

    # Проверка загружена ли карта
    if not map_loaded:
        coffee_house_map.load_map()
        # stations1_map.load_map()
        # stations2_map.load_map()
        # stations3_map.load_map()
        map_loaded = True

    # Если coffee_house
    if current_status == condition[0]:
        button_left_S = False
        circle_btn_S_signal = False
        coffee_house_map.draw(screen)
        player.update()
        player.draw(screen)

        button_right.change_color(ORANGE)
    # Если stations1
    elif current_status == condition[1]:
        button_left_S = True
        circle_btn_S_signal = True
        # stations1_map.draw(screen)
        screen.fill(ORANGE1)
        button_right.change_color(GREEN)
        button_left.change_color(BLUE)
        draw_order(screen, cup, SM, SE)
    # Если stations2
    elif current_status == condition[2]:
        button_left_S = True
        circle_btn_S_signal = True
        # stations2_map.draw(screen)
        screen.fill(BLUE1)
        button_right.change_color(ORANGE)
        button_left.change_color(VIOLET)
    # Если stations3
    else:
        button_left_S = False
        circle_btn_S_signal = False
        # stations3_map.draw(screen)
        screen.fill(VIOLET1)
        button_right.change_color(BLUE)

    # Прорисовка кнопок
    button_right.draw(screen)
    if button_left_S:
        button_left.draw(screen)
    # Прорисовка круглой кнопки
    if circle_btn_S_signal:
        circle_btn_S.draw(screen)
        circle_btn_M.draw(screen)
        circle_btn_L.draw(screen)

