from globals import *
from classes.node import CircleButton, Button
from abc import ABC, abstractmethod
from classes.tiled import Map
from classes.character import Character

class Station(ABC):
    """ Класс станции """
    def __init__(self, name, bg_color, button_color):
        self.name = name
        self.bg_color = bg_color
        self.button_color = button_color
        self.is_active = False
        self.buttons = []

    @abstractmethod
    def draw(self, screen):
        """ Отрисовка станции """
        pass

    @abstractmethod
    def events(self, events):
        """ Обработка событий станции """
        pass

    def add_button(self, button):
        """ Добавить кнопку к станции """
        self.buttons.append(button)

    def activate(self):
        """ Активировать станцию """
        self.is_active = True

    def deactivate(self):
        """ Деактивировать станцию """
        self.is_active = False

class OrderStation(Station):
    """ Станция заказов """
    def __init__(self):
        super().__init__("Заказы", BLACK, GREEN)
        self.map = Map('assets/tiled/tmx/coffee_house.tmx', 48, 1)
        self.map_loaded = False

        # Персонажи
        self.player = Character(3, (530, 60), 'assets/sprites/characters/Adam_16x16.png', [(530,60)])
        self.nps = Character(3, (240, 0), 'assets/sprites/characters/Alex_16x16.png', [(240, 140), (530, 140), (530, 120)])

    def draw(self, screen):
        """ Отрисовка станции заказов """
        if not self.map_loaded:
            self.map.load_map()
            self.map_loaded = True

        self.map.draw(screen)
        self.player.update()
        self.player.draw(screen)
        self.nps.update()
        self.nps.draw(screen)

    def events(self, events):
        """ Обработка событий на станции """
        pass

class BrewStation(Station):
    """ Станция приготовления кофе """
    def __init__(self):
        super().__init__("Приготовление", ORANGE_fon, ORANGE)

        self.cells = []
        self.cells_pos = [(0, 75), (300, 75), (600, 75), (900, 75)]

        # Цвета для кнопок молока
        self.milk_colors = {
            "SKIM_MILK" : WHITE,
            "back": RED,
            "STRAWBERRY_MILK": STRAWBERRY_MILK,
        }
        # Цвета для кнопок эспрессо
        self.espresso_colors = {
            "CITY_ROAST": CITY_ROAST,
            "back": RED,
            "DECAF_ROAST": DECAF_ROAST,
        }

        for i, (x, y) in enumerate(self.cells_pos):
            cell = {
                "id": i,
                "x": x,
                "y": y,
                "main_milk": CircleButton(30, WHITE, (x + 150, y + 125)),
                "main_espresso": CircleButton(30, (110, 59, 9), (x + 150, y + 375)),
                "show_milk_menu": False,
                "show_espresso_menu": False,
                "milk_buttons": [],
                "espresso_buttons": [],
                "selected_milk": None,
                "selected_espresso": None
            }

            milk_button_positions = [
                (x + 150, y + 125),
                (x + 150, y + 250),
                (x + 150, y + 375),
            ]

            for j, (btn_x, btn_y) in enumerate(milk_button_positions):
                milk_types = list(self.milk_colors.keys())
                milk_type = milk_types[j]
                btn = CircleButton(25, self.milk_colors[milk_type], (btn_x, btn_y))
                btn.milk_type = milk_type
                btn.visible = False
                cell["milk_buttons"].append(btn)


            espresso_button_positions = [
                (x + 150, y + 120),
                (x + 150, y + 250),
                (x + 150, y + 375),
            ]

            for j, (btn_x, btn_y) in enumerate(espresso_button_positions):
                espresso_types = list(self.espresso_colors.keys())
                espresso_type = espresso_types[j]
                btn = CircleButton(25, self.espresso_colors[espresso_type], (btn_x, btn_y))
                btn.espresso_type = espresso_type
                btn.visible = False
                cell["espresso_buttons"].append(btn)

            self.cells.append(cell)

    def draw(self, screen):
        """ Отрисовка станции приготовления """
        screen.fill(self.bg_color)
        for cell in self.cells:
            py.draw.rect(screen, ORANGE1, (cell["x"], cell["y"], 300, 500))
            py.draw.rect(screen, CONTOUR, (cell["x"], cell["y"], 300, 500), 3)

            # Если ни одно меню не открыто и компоненты не выбраны
            if not cell["show_milk_menu"] and not cell["show_espresso_menu"] and \
               not cell["selected_milk"] and not cell["selected_espresso"]:
                cell["main_milk"].draw(screen)
                cell["main_espresso"].draw(screen)
            # Если открыто меню молока
            elif cell["show_milk_menu"]:
                for btn in cell["milk_buttons"]:
                    if btn.visible:
                        btn.draw(screen)
            # Если открыто меню эспрессо
            elif cell["show_espresso_menu"]:
                for btn in cell["espresso_buttons"]:
                    if btn.visible:
                        btn.draw(screen)

    def events(self, events):
        """ Обработка событий на станции приготовления """
        for event in events:
            if event.type == py.MOUSEBUTTONDOWN:
                for cell in self.cells:

                    # Если открыто меню молока
                    if cell["show_milk_menu"]:
                        for btn in cell["milk_buttons"]:
                            if btn.signal(event.pos):
                                if btn.milk_type == "back":
                                    print(f"Ячейка {cell['id']}: возврат из меню молока")
                                    cell["show_milk_menu"] = False
                                    cell["show_espresso_menu"] = False
                                    # Скрываем все кнопки меню
                                    for milk_btn in cell["milk_buttons"]:
                                        milk_btn.visible = False
                                    for espresso_btn in cell["espresso_buttons"]:
                                        espresso_btn.visible = False
                                else:
                                    cell["selected_milk"] = btn.milk_type
                                    milk_name = "Обезжиренное молоко" if btn.milk_type == "SKIM_MILK" else "Клубничное молоко"
                                    print(f"Ячейка {cell['id']}: выбрано {milk_name}")

                    # Если открыто меню эспрессо
                    elif cell["show_espresso_menu"]:
                        for btn in cell["espresso_buttons"]:
                            if btn.signal(event.pos):
                                if btn.espresso_type == "back":
                                    print(f"Ячейка {cell['id']}: возврат из меню эспрессо")
                                    cell["show_milk_menu"] = False
                                    cell["show_espresso_menu"] = False
                                    # Скрываем все кнопки меню
                                    for milk_btn in cell["milk_buttons"]:
                                        milk_btn.visible = False
                                    for espresso_btn in cell["espresso_buttons"]:
                                        espresso_btn.visible = False
                                else:
                                    # Выбрали тип эспрессо
                                    cell["selected_espresso"] = btn.espresso_type
                                    coffee_name = "Городское жаркое" if btn.espresso_type == "CITY_ROAST" else "Жаркое без кофеина"
                                    print(f"Ячейка {cell['id']}: выбрано {coffee_name}")

                    # Если меню не открыты
                    else:
                        if cell["selected_milk"] and cell["main_milk"].signal(event.pos):
                            print(f"Ячейка {cell['id']}: открыто меню молока (уже выбрано: {cell['selected_milk']})")
                            cell["show_milk_menu"] = True
                            cell["show_espresso_menu"] = False
                            for btn in cell["milk_buttons"]:
                                btn.visible = True
                            for btn in cell["espresso_buttons"]:
                                btn.visible = False

                        elif cell["selected_espresso"] and cell["main_espresso"].signal(event.pos):
                            print(f"Ячейка {cell['id']}: открыто меню эспрессо (уже выбрано: {cell['selected_espresso']})")
                            cell["show_espresso_menu"] = True
                            cell["show_milk_menu"] = False
                            for btn in cell["espresso_buttons"]:
                                btn.visible = True
                            for btn in cell["milk_buttons"]:
                                btn.visible = False

                        elif not cell["selected_milk"] and cell["main_milk"].signal(event.pos):
                            print(f"Ячейка {cell['id']}: открыто меню молока")
                            cell["show_milk_menu"] = True
                            cell["show_espresso_menu"] = False
                            for btn in cell["milk_buttons"]:
                                btn.visible = True
                            for btn in cell["espresso_buttons"]:
                                btn.visible = False

                        elif not cell["selected_espresso"] and cell["main_espresso"].signal(event.pos):
                            print(f"Ячейка {cell['id']}: открыто меню эспрессо")
                            cell["show_espresso_menu"] = True
                            cell["show_milk_menu"] = False
                            for btn in cell["espresso_buttons"]:
                                btn.visible = True
                            for btn in cell["milk_buttons"]:
                                btn.visible = False

class BuildStation(Station):
    """ Станция сборки """
    def __init__(self):
        super().__init__("Сборка", BLUE1, BLUE)

    def draw(self, screen):
        """ Отрисовка станции сборки """
        screen.fill(self.bg_color)

    def events(self, events):
        pass

class StationManager:
    """ Менеджер управления станциями """
    def __init__(self):
        self.stations = {
            "order": OrderStation(),
            "brew": BrewStation(),
            "build": BuildStation(),
        }
        self.current_station = "order"
        self.navigation_buttons = {
            "left": Button(300, 100, BLUE, (0, 620)),
            "right": Button(300, 100, ORANGE, (900, 620))
        }

        self.show_left_button = False
        self.show_right_button = False

        self.navigation_map = {
            "order": {"left": None, "right": "brew"},
            "brew": {"left": "build", "right": "order"},
            "build": {"left": None, "right": "brew"}
        }

        self.update_navigation()

    def update_navigation(self):
        """ Обновление видимости и цветов кнопок навигации """
        current_nav = self.navigation_map[self.current_station]

        # Левая кнопка
        left_target = current_nav.get("left")
        if left_target:
            self.show_left_button = True
            self.navigation_buttons["left"].bg_color = self.stations[left_target].button_color
            self.navigation_buttons["left"].redraw()
        else:
            self.show_left_button = False

        # Правая кнопка
        right_target = current_nav.get("right")
        if right_target:
            self.show_right_button = True
            self.navigation_buttons["right"].bg_color = self.stations[right_target].button_color
            self.navigation_buttons["right"].redraw()
        else:
            self.show_right_button = False

    def handle_events(self, events):
        """ Обработка событий для всех станций """
        for event in events:
            if event.type == py.MOUSEBUTTONDOWN:
                current_nav = self.navigation_map[self.current_station]
                # Правая кнопка
                if self.show_right_button and self.navigation_buttons["right"].signal(event.pos):
                    target = current_nav.get("right")
                    if target:
                        self.switch_to(target)

                # Левая кнопка
                if self.show_left_button and self.navigation_buttons["left"].signal(event.pos):
                    target = current_nav.get("left")
                    if target:
                        self.switch_to(target)

        # Передача событий текущей станции
        self.stations[self.current_station].events(events)

    def switch_to(self, station_name):
        """ Переключиться на другую станцию """
        if station_name in self.stations:
            self.stations[self.current_station].deactivate()
            self.current_station = station_name
            self.stations[station_name].activate()
            self.update_navigation()

    def draw(self, screen):
        """ Отрисовка всего """
        # Рисуем текущую станцию
        current_station = self.stations[self.current_station]
        current_station.draw(screen)

        # Рисуем кнопки
        if self.show_right_button:
            self.navigation_buttons["right"].draw(screen)
        if self.show_left_button:
            self.navigation_buttons["left"].draw(screen)