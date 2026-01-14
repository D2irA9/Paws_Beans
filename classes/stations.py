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
        return None

class BrewStation(Station):
    """ Станция приготовления кофе """
    def __init__(self):
        super().__init__("Приготовление", ORANGE_fon, ORANGE)

        # Кнопки станции
        self.milk = CircleButton(30, WHITE, (350, 200))
        self.bt_skimmed_milk = CircleButton(30, WHITE, (410, 160))
        self.bt_strawberry_milk = CircleButton(30, ORANGE_fon, (410, 240))

        self.espresso = CircleButton(30, (110, 59, 9), (350, 450))
        self.bt_city_roast = CircleButton(30, BLUE, (410, 410))
        self.bt_decaf_roast = CircleButton(30, ORANGE, (410, 490))

        # Состояния
        self.milk_sub_visible = False
        self.espresso_sub_visible = False

        # Выбранные ингредиенты
        self.selected_milk = None
        self.selected_espresso = None

    def draw(self, screen):
        """ Отрисовка станции приготовления """
        screen.fill(self.bg_color)
        py.draw.rect(screen, ORANGE1, (200, 75, 300, 500))

        self.milk.draw(screen)
        self.espresso.draw(screen)

    def events(self, events):
        """ Обработка событий на станции приготовления """
        return None

class BuildStation(Station):
    """ Станция сборки """
    def __init__(self):
        super().__init__("Сборка", BLUE1, BLUE)

    def draw(self, screen):
        """ Отрисовка станции сборки """
        screen.fill(self.bg_color)

    def events(self, events):
        return None

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