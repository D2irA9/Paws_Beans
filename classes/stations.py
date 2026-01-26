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
            "SKIM_MILK": WHITE,
            "back": RED,
            "STRAWBERRY_MILK": STRAWBERRY_MILK,
        }

        # Цвета холодное и горячее
        self.milk_level2_colors = {
            "cold": BLUE,
            "hot": RED,
        }

        # Цвета для кнопок эспрессо
        self.espresso_colors = {
            "CITY_ROAST": CITY_ROAST,
            "back": RED,
            "DECAF_ROAST": DECAF_ROAST,
        }
        # Цвета для кнопок порций эспрессо
        self.portion_colors = {
            1: (139, 69, 19),
            2: (160, 82, 45),
            3: (205, 133, 63),
        }

        for i, (x, y) in enumerate(self.cells_pos):
            cell = {
                "id": i,
                "x": x,
                "y": y,
                "main_milk": CircleButton(30, WHITE, (x + 150, y + 125)),
                "main_espresso": CircleButton(30, (110, 59, 9), (x + 150, y + 375)),

                # Уровни меню (0-основное, 1-тип, 2-температура, 3-наливка, 4-взбивание)
                "milk_menu_level": 0,

                # Уровни эспрессо (0-нет, 1-тип эспрессо, 2-порция)
                "espresso_menu_level": 0,

                # Кнопки для каждого уровня
                "milk_level1_buttons": [],
                "milk_level2_buttons": [],
                "espresso_type_buttons": [],
                "espresso_portion_buttons": [],
                "espresso_stop_button": Button(150, 40, BLUE, (x + 75, y + 450)),
                "espresso_start_button": Button(150, 40, GREEN, (x + 75, y + 400)),

                # Кнопка наливки
                "pour_button": None,

                # Кнопка остановки взбивания
                "stop_whisk_button": None,

                # Выбранные значения
                "selected_milk_type": None,
                "selected_milk_temp": None,
                "selected_espresso_type": None,
                "selected_espresso_portion": 1,

                # Состояние процесса
                "is_pouring": False,
                "is_whisking": False,
                "pour_start_time": 0,
                "pour_progress": 0,
                "whisk_start_time": 0,
                "whisk_progress": 0,
                "glass_fill": [],
                "portions_poured": 0,
                "ideal_zone_start": 45,
                "ideal_zone_end": 55,

                # Новые свойства для мини-игры эспрессо
                "roast_slider_stopped": False,
                "roast_slider_direction": 1,
                # УВЕЛИЧЕНА СКОРОСТЬ с 0.5 до 1.2
                "roast_slider_speed": 1.2,
                "roast_target_progress": 0,
                "is_roasting": False,
                "roast_progress": 0,
                "roast_slider_progress": 0,
                "roast_start_time": 0,
            }

            # Уровень 1 (Молоко)
            milk_level1_positions = [
                (x + 150, y + 125),
                (x + 150, y + 250),
                (x + 150, y + 375),
            ]

            for j, (btn_x, btn_y) in enumerate(milk_level1_positions):
                milk_types = list(self.milk_colors.keys())
                milk_type = milk_types[j]
                btn = CircleButton(25, self.milk_colors[milk_type], (btn_x, btn_y), text="")
                btn.value = milk_type
                btn.visible = False
                cell["milk_level1_buttons"].append(btn)

            # Уровень 2 (Молоко)
            milk_level2_positions = [
                (x + 150, y + 175),
                (x + 150, y + 325),
            ]

            for j, (btn_x, btn_y) in enumerate(milk_level2_positions):
                temp_types = ["cold", "hot"]
                temp_type = temp_types[j]
                color = self.milk_level2_colors[temp_type]
                text = "Х" if temp_type == "cold" else "Г"
                btn = CircleButton(25, color, (btn_x, btn_y), text=text)
                btn.value = temp_type
                btn.visible = False
                cell["milk_level2_buttons"].append(btn)

            # Кнопка наливки молока
            pour_button_x = x + 75
            pour_button_y = y + 450
            cell["pour_button"] = Button(150, 40, BLUE, (pour_button_x, pour_button_y))
            cell["pour_button"].visible = False

            # Кнопка остановки взбивания
            stop_button_x = x + 75
            stop_button_y = y + 450
            cell["stop_whisk_button"] = Button(150, 40, RED, (stop_button_x, stop_button_y))
            cell["stop_whisk_button"].visible = False

            # Кнопки для эспрессо
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
                cell["espresso_type_buttons"].append(btn)

            # Кнопки для порций эспрессо (уровень 2)
            espresso_portion_positions = [
                (x + 150, y + 120),
                (x + 150, y + 250),
                (x + 150, y + 375),
            ]
            for j, (btn_x, btn_y) in enumerate(espresso_portion_positions):
                if j < 3:
                    portion = j + 1
                    btn = CircleButton(25, self.portion_colors[portion], (btn_x, btn_y), text=str(portion))
                    btn.portion = portion
                    btn.is_back = False
                    btn.visible = False
                    cell["espresso_portion_buttons"].append(btn)

            self.cells.append(cell)
            self.build_station = None

    def draw(self, screen):
        """ Отрисовка станции приготовления """
        screen.fill(self.bg_color)

        for cell in self.cells:
            x, y = cell["x"], cell["y"]

            # Уровень 0
            if cell["milk_menu_level"] == 0 and cell["espresso_menu_level"] == 0:
                py.draw.rect(screen, ORANGE1, (x, y, 300, 500))
                py.draw.rect(screen, CONTOUR, (x, y, 300, 500), 3)
                cell["main_milk"].draw(screen)
                cell["main_espresso"].draw(screen)

            # Уровни молока
            elif cell["milk_menu_level"] == 1:
                self.draw_milk_level1(screen, cell)
            elif cell["milk_menu_level"] == 2:
                self.draw_milk_level2(screen, cell)
            elif cell["milk_menu_level"] == 3:
                self.draw_milk_level3(screen, cell)
            elif cell["milk_menu_level"] == 4:
                self.draw_milk_level4(screen, cell)

            # Уровни эспрессо
            elif cell["espresso_menu_level"] == 1:
                self.draw_espresso_level1(screen, cell)
            elif cell["espresso_menu_level"] == 2:
                self.draw_espresso_level2(screen, cell)
            elif cell["espresso_menu_level"] == 3:
                self.draw_espresso_level3(screen, cell)
            elif cell["espresso_menu_level"] == 4:
                self.draw_espresso_level4(screen, cell)

    def draw_milk_level1(self, screen, cell):
        """ Отрисовка уровня 1 молока: выбор типа молока """
        x, y = cell["x"], cell["y"]
        py.draw.rect(screen, ORANGE1, (x, y, 300, 500))
        py.draw.rect(screen, CONTOUR, (x, y, 300, 500), 3)

        # Рисуем кнопки
        for btn in cell["milk_level1_buttons"]:
            if btn.visible:
                btn.draw(screen)

    def draw_milk_level2(self, screen, cell):
        """ Отрисовка уровня 2 молока: выбор температуры """
        x, y = cell["x"], cell["y"]
        py.draw.rect(screen, ORANGE1, (x, y, 300, 500))
        py.draw.rect(screen, CONTOUR, (x, y, 300, 500), 3)

        # Рисуем кнопки
        for btn in cell["milk_level2_buttons"]:
            if btn.visible:
                btn.draw(screen)

    def draw_milk_level3(self, screen, cell):
        """ Отрисовка уровня 3: наливка молока """
        x, y = cell["x"], cell["y"]

        # Основная ячейка
        py.draw.rect(screen, ORANGE1, (x, y, 300, 500))
        py.draw.rect(screen, CONTOUR, (x, y, 300, 500), 3)

        # Темный прямоугольник для стакана
        dark_rect_y = y + 50
        dark_rect_height = 300
        darker_orange = (140, 60, 0)
        py.draw.rect(screen, darker_orange, (x + 20, dark_rect_y, 260, dark_rect_height))
        py.draw.rect(screen, CONTOUR, (x + 20, dark_rect_y, 260, dark_rect_height), 2)

        # Стакан
        glass_width = 120
        glass_height = 200
        glass_x = x + (300 - glass_width) // 2
        glass_y = dark_rect_y + (dark_rect_height - glass_height) // 2

        # Отрисовка стакана с порциями
        max_portions = 4
        portion_height = glass_height // max_portions

        # Внешний контур стакана
        glass_color = (240, 240, 240)
        py.draw.rect(screen, glass_color, (glass_x, glass_y, glass_width, glass_height))
        py.draw.rect(screen, (200, 200, 200), (glass_x, glass_y, glass_width, glass_height), 3)

        # Разделители порций
        for i in range(1, max_portions):
            divider_y = glass_y + i * portion_height
            py.draw.line(screen, (180, 180, 180), (glass_x, divider_y), (glass_x + glass_width, divider_y), 1)

        # Заливаем заполненные порции
        for i in range(max_portions):
            if i < len(cell["glass_fill"]) and cell["glass_fill"][i]:
                # Цвет молока
                if cell["selected_milk_type"] == "SKIM_MILK":
                    milk_color = (255, 250, 240)
                else:  # STRAWBERRY_MILK
                    milk_color = (255, 200, 220)

                if cell["selected_milk_temp"] == "hot":
                    milk_color = tuple(min(255, c + 20) for c in milk_color)

                # Координаты заполнения
                fill_y = glass_y + glass_height - (i + 1) * portion_height
                fill_height = portion_height

                # Рисуем заполненную порцию
                py.draw.rect(screen, milk_color, (glass_x, fill_y, glass_width, fill_height))
                py.draw.rect(screen, (220, 220, 220), (glass_x, fill_y, glass_width, fill_height), 1)

        # Кнопка наливки
        if cell["pour_button"] and cell["pour_button"].visible:
            cell["pour_button"].draw(screen)

    def draw_milk_level4(self, screen, cell):
        """ Отрисовка уровня 4: взбивание молока """
        x, y = cell["x"], cell["y"]

        # Основная ячейка
        py.draw.rect(screen, ORANGE1, (x, y, 300, 500))
        py.draw.rect(screen, CONTOUR, (x, y, 300, 500), 3)

        # Таймер взбивания
        self.draw_whisk_timer(screen, cell)

        # Темный прямоугольник для стакана
        dark_rect_y = y + 80
        dark_rect_height = 300
        darker_orange = (140, 60, 0)
        py.draw.rect(screen, darker_orange, (x + 20, dark_rect_y, 260, dark_rect_height))
        py.draw.rect(screen, CONTOUR, (x + 20, dark_rect_y, 260, dark_rect_height), 2)

        # Стакан
        glass_width = 120
        glass_height = 200
        glass_x = x + (300 - glass_width) // 2
        glass_y = dark_rect_y + (dark_rect_height - glass_height) // 2

        # Отрисовка стакана с порциями
        portions = cell["portions_poured"]
        max_portions = 4
        portion_height = glass_height // max_portions

        # Внешний контур стакана
        glass_color = (240, 240, 240)
        py.draw.rect(screen, glass_color, (glass_x, glass_y, glass_width, glass_height))
        py.draw.rect(screen, (200, 200, 200), (glass_x, glass_y, glass_width, glass_height), 3)

        # Разделители порций
        for i in range(1, max_portions):
            divider_y = glass_y + i * portion_height
            py.draw.line(screen, (180, 180, 180), (glass_x, divider_y), (glass_x + glass_width, divider_y), 1)

        # Цвет молока
        if cell["selected_milk_type"] == "SKIM_MILK":
            milk_color = (255, 250, 240)
        else:
            milk_color = (255, 200, 220)

        if cell["selected_milk_temp"] == "hot":
            milk_color = tuple(min(255, c + 20) for c in milk_color)

        # Заполняем все налитые порции
        for i in range(portions):
            fill_y = glass_y + glass_height - (i + 1) * portion_height
            fill_height = portion_height
            py.draw.rect(screen, milk_color, (glass_x, fill_y, glass_width, fill_height))
            py.draw.rect(screen, (220, 220, 220), (glass_x, fill_y, glass_width, fill_height), 1)

        # Эффект пены сверху
        if cell["is_whisking"]:
            foam_color = tuple(min(255, c + 30) for c in milk_color)
            foam_height = portion_height
            foam_y = glass_y + glass_height - portions * portion_height
            py.draw.rect(screen, foam_color, (glass_x, foam_y, glass_width, foam_height))

        # Кнопка остановки
        if cell["stop_whisk_button"] and cell["stop_whisk_button"].visible:
            cell["stop_whisk_button"].draw(screen)

    def draw_espresso_level1(self, screen, cell):
        """ Отрисовка уровня 1 эспрессо: выбор типа """
        x, y = cell["x"], cell["y"]

        # Рисуем фон
        py.draw.rect(screen, ORANGE1, (x, y, 300, 500))
        py.draw.rect(screen, CONTOUR, (x, y, 300, 500), 3)

        # Рисуем кнопки
        for btn in cell["espresso_type_buttons"]:
            if btn.visible:
                btn.draw(screen)

    def draw_espresso_level2(self, screen, cell):
        """ Отрисовка уровня 2 эспрессо: выбор порции """
        x, y = cell["x"], cell["y"]

        # Рисуем фон
        py.draw.rect(screen, ORANGE1, (x, y, 300, 500))
        py.draw.rect(screen, CONTOUR, (x, y, 300, 500), 3)

        # Рисуем кнопки порций
        for btn in cell["espresso_portion_buttons"]:
            if btn.visible:
                btn.draw(screen)

    def draw_espresso_level3(self, screen, cell):
        """ Отрисовка уровня 3 эспрессо: мини-игра """
        x, y = cell["x"], cell["y"]
        py.draw.rect(screen, ORANGE1, (x, y, 300, 500))
        py.draw.rect(screen, CONTOUR, (x, y, 300, 500), 3)

        self.draw_mini_game(screen, cell)

        # Темный прямоугольник для стакана
        dark_rect_y = y + 80
        dark_rect_height = 300
        darker_orange = (140, 60, 0)
        py.draw.rect(screen, darker_orange, (x + 20, dark_rect_y, 260, dark_rect_height))
        py.draw.rect(screen, CONTOUR, (x + 20, dark_rect_y, 260, dark_rect_height), 2)

        # Стакан
        glass_width = 120
        glass_height = 200
        glass_x = x + (300 - glass_width) // 2
        glass_y = dark_rect_y + (dark_rect_height - glass_height) // 2

        # Отрисовка стакана с порциями
        portions = cell["selected_espresso_portion"]
        max_portions = 3
        portion_height = glass_height // max_portions

        # Внешний контур стакана
        glass_color = (240, 240, 240)
        py.draw.rect(screen, glass_color, (glass_x, glass_y, glass_width, glass_height))
        py.draw.rect(screen, (200, 200, 200), (glass_x, glass_y, glass_width, glass_height), 3)

        # Разделители порций
        for i in range(1, max_portions):
            divider_y = glass_y + i * portion_height
            py.draw.line(screen, (180, 180, 180), (glass_x, divider_y), (glass_x + glass_width, divider_y), 1)

        # Цвет эспрессо
        if cell["selected_espresso_type"] == "CITY_ROAST":
            espresso_color = CITY_ROAST
        else:
            espresso_color = DECAF_ROAST
        # Заполняем все налитые порции
        for i in range(portions):
            fill_y = glass_y + glass_height - (i + 1) * portion_height
            fill_height = portion_height
            py.draw.rect(screen, espresso_color, (glass_x, fill_y, glass_width, fill_height))
            py.draw.rect(screen, (220, 220, 220), (glass_x, fill_y, glass_width, fill_height), 1)

        # Отрисовка кнопок
        if not cell.get("roast_slider_stopped", False):
            # Если ползунок еще не остановлен - кнопка "СТОП"
            cell["espresso_stop_button"].draw(screen)
            cell["espresso_start_button"].visible = False
        else:
            # Если ползунок остановлен - кнопка "НАЧАТЬ ОБЖАРКУ"
            cell["espresso_start_button"].draw(screen)
            cell["espresso_stop_button"].visible = False

    def draw_espresso_level4(self, screen, cell):
        """ Отрисовка уровня 4 эспрессо: процесс обжарки """
        x, y = cell["x"], cell["y"]
        py.draw.rect(screen, ORANGE1, (x, y, 300, 500))
        py.draw.rect(screen, CONTOUR, (x, y, 300, 500), 3)

        # Таймер обжарки
        self.draw_roast_timer(screen, cell)

        dark_rect_y = y + 80
        dark_rect_height = 300
        darker_orange = (140, 60, 0)
        py.draw.rect(screen, darker_orange, (x + 20, dark_rect_y, 260, dark_rect_height))
        py.draw.rect(screen, CONTOUR, (x + 20, dark_rect_y, 260, dark_rect_height), 2)

        # Стакан
        glass_width = 120
        glass_height = 200
        glass_x = x + (300 - glass_width) // 2
        glass_y = dark_rect_y + (dark_rect_height - glass_height) // 2

        # Отрисовка стакана с порциями
        portions = cell["selected_espresso_portion"]
        max_portions = 3
        portion_height = glass_height // max_portions

        # Внешний контур стакана
        glass_color = (240, 240, 240)
        py.draw.rect(screen, glass_color, (glass_x, glass_y, glass_width, glass_height))
        py.draw.rect(screen, (200, 200, 200), (glass_x, glass_y, glass_width, glass_height), 3)

        # Разделители порций
        for i in range(1, max_portions):
            divider_y = glass_y + i * portion_height
            py.draw.line(screen, (180, 180, 180), (glass_x, divider_y), (glass_x + glass_width, divider_y), 1)

        # Цвет эспрессо
        if cell["selected_espresso_type"] == "CITY_ROAST":
            espresso_color = CITY_ROAST
        else:
            espresso_color = DECAF_ROAST

        # Заполняем все налитые порции
        for i in range(portions):
            fill_y = glass_y + glass_height - (i + 1) * portion_height
            fill_height = portion_height
            py.draw.rect(screen, espresso_color, (glass_x, fill_y, glass_width, fill_height))
            py.draw.rect(screen, (220, 220, 220), (glass_x, fill_y, glass_width, fill_height), 1)

    def finish_pouring(self, cell):
        """ Завершение наливки и переход к взбиванию """
        portions = cell["portions_poured"]
        print(f"Ячейка {cell['id']}: налито {portions} порций")

        # Переход на уровень 4 (взбивание)
        cell["milk_menu_level"] = 4

        # Скрываем кнопку наливки
        if cell["pour_button"]:
            cell["pour_button"].visible = False
        if cell["stop_whisk_button"]:
            cell["stop_whisk_button"].visible = True

        # Запускаем взбивание
        cell["is_whisking"] = True
        cell["whisk_start_time"] = py.time.get_ticks()
        cell["whisk_progress"] = 0

        # Определяем время взбивания
        print(f"Ячейка {cell['id']}: начато взбивание для {portions} порций")
        print(f"  Идеальная зона: {cell['ideal_zone_start']}-{cell['ideal_zone_end']}%")

    def draw_mini_game(self, screen, cell):
        """ Отображение мини-игры """
        x, y = cell["x"], cell["y"]

        # Позиция
        timer_y = y + 20
        timer_height = 40
        timer_width = 260

        # Фон
        py.draw.rect(screen, (80, 80, 80), (x + 20, timer_y, timer_width, timer_height))

        portions = cell.get("selected_espresso_portion", 1)
        if portions == 1:
            zone_start = 40
            zone_end = 50
        elif portions == 2:
            zone_start = 60
            zone_end = 70
        else:
            zone_start = 80
            zone_end = 90

        # Сохраняем зону в ячейке
        cell["ideal_zone_start"] = zone_start
        cell["ideal_zone_end"] = zone_end

        zone_width = zone_end - zone_start
        zone_x = x + 20 + int(timer_width * (zone_start / 100))
        zone_w = int(timer_width * (zone_width / 100))
        py.draw.rect(screen, GREEN, (zone_x, timer_y, zone_w, timer_height))

        # Обновляем позицию ползунка если он не остановлен
        if not cell.get("roast_slider_stopped", False):
            cell["roast_slider_progress"] += cell["roast_slider_direction"] * cell["roast_slider_speed"]

            # Меняем направление при достижении границ
            if cell["roast_slider_progress"] >= 95:
                cell["roast_slider_progress"] = 95
                cell["roast_slider_direction"] = -1
            elif cell["roast_slider_progress"] <= 0:
                cell["roast_slider_progress"] = 0
                cell["roast_slider_direction"] = 1

        # Рисуем ползунок
        slider_x = x + 20 + int(timer_width * (cell["roast_slider_progress"] / 100))
        slider_width = 10
        if zone_start <= cell["roast_slider_progress"] <= zone_end:
            slider_color = GREEN
        else:
            slider_color = YELLOW

        py.draw.rect(screen, slider_color, (slider_x, timer_y, slider_width, timer_height))
        py.draw.rect(screen, (200, 180, 0), (slider_x, timer_y, slider_width, timer_height), 2)

        # Контур таймера
        py.draw.rect(screen, (40, 40, 40), (x + 20, timer_y, timer_width, timer_height), 3)

    def draw_whisk_timer(self, screen, cell):
        """ Отрисовка таймера взбивания """
        x, y = cell["x"], cell["y"]

        # Позиция таймера
        timer_y = y + 20
        timer_height = 40
        timer_width = 260

        # Фон таймера
        py.draw.rect(screen, (80, 80, 80), (x + 20, timer_y, timer_width, timer_height))

        # Заполненная часть таймера
        fill_width = int(timer_width * (cell["whisk_progress"] / 100))
        py.draw.rect(screen, YELLOW,
                     (x + 20, timer_y, fill_width, timer_height))

        # Зеленая зона
        portions = cell["portions_poured"]

        # Определяем зеленую зону в зависимости от порций
        if portions == 1:
            zone_start = 40
            zone_end = 60
        elif portions == 2:
            zone_start = 50
            zone_end = 70
        elif portions == 3:
            zone_start = 60
            zone_end = 80
        else:
            zone_start = 90
            zone_end = 100

        # Сохраняем зону
        cell["ideal_zone_start"] = zone_start
        cell["ideal_zone_end"] = zone_end

        # Рисуем зеленую зону
        zone_width = zone_end - zone_start
        zone_x = x + 20 + int(timer_width * (zone_start / 100))
        zone_w = int(timer_width * (zone_width / 100))
        py.draw.rect(screen, GREEN, (zone_x, timer_y, zone_w, timer_height))

        # Контур таймера
        py.draw.rect(screen, (40, 40, 40), (x + 20, timer_y, timer_width, timer_height), 3)

    def events(self, events):
        """ Обработка событий на станции приготовления """
        current_time = py.time.get_ticks()
        # Обновление процессов
        for cell in self.cells:
            if cell["is_pouring"]:
                self.update_pouring(cell, current_time)
            if cell["is_whisking"]:
                self.update_whisking(cell, current_time)
            if cell.get("is_roasting", False):
                self.update_roasting(cell, current_time)

        for event in events:
            if event.type == py.MOUSEBUTTONDOWN:
                for cell in self.cells:

                    # Уровень 3 (Молоко)
                    if cell["milk_menu_level"] == 3:
                        if cell["pour_button"] and cell["pour_button"].signal(event.pos):
                            print(f"Ячейка {cell['id']}: начата наливка молока")
                            cell["is_pouring"] = True
                            cell["pour_start_time"] = current_time
                            cell["pour_progress"] = 0
                            cell["glass_fill"] = []
                            cell["portions_poured"] = 0

                    # Уровень 4 (Молоко)
                    elif cell["milk_menu_level"] == 4:
                        if cell["stop_whisk_button"] and cell["stop_whisk_button"].signal(event.pos):
                            self.finish_whisking(cell)
                            cell["is_whisking"] = False

                    # Уровень 1 (Молоко)
                    elif cell["milk_menu_level"] == 1:
                        for btn in cell["milk_level1_buttons"]:
                            if btn.signal(event.pos):
                                if btn.value == "back":
                                    cell["milk_menu_level"] = 0
                                    for milk_btn in cell["milk_level1_buttons"]:
                                        milk_btn.visible = False
                                else:
                                    cell["selected_milk_type"] = btn.value
                                    cell["milk_menu_level"] = 2
                                    for milk_btn in cell["milk_level1_buttons"]:
                                        milk_btn.visible = False
                                    for temp_btn in cell["milk_level2_buttons"]:
                                        temp_btn.visible = True

                    # Уровень 2 (Молоко)
                    elif cell["milk_menu_level"] == 2:
                        for btn in cell["milk_level2_buttons"]:
                            if btn.signal(event.pos):
                                cell["selected_milk_temp"] = btn.value
                                cell["milk_menu_level"] = 3
                                for temp_btn in cell["milk_level2_buttons"]:
                                    temp_btn.visible = False
                                if cell["pour_button"]:
                                    cell["pour_button"].visible = True
                                print(f"Ячейка {cell['id']}: выбрана температура - {btn.value}")

                    # Уровень 0 (Молоко) - исправленная часть
                    elif cell["milk_menu_level"] == 0 and cell["espresso_menu_level"] == 0:
                        if cell["main_milk"].signal(event.pos):
                            # Сброс
                            cell["selected_milk_type"] = None
                            cell["selected_milk_temp"] = None
                            cell["is_pouring"] = False
                            cell["is_whisking"] = False
                            cell["glass_fill"] = []
                            cell["portions_poured"] = 0
                            if cell["pour_button"]:
                                cell["pour_button"].visible = False
                            if cell["stop_whisk_button"]:
                                cell["stop_whisk_button"].visible = False

                            cell["milk_menu_level"] = 1
                            cell["espresso_menu_level"] = 0

                            for btn in cell["milk_level1_buttons"]:
                                btn.visible = True
                            for btn in cell["milk_level2_buttons"]:
                                btn.visible = False
                            for btn in cell["espresso_type_buttons"]:
                                btn.visible = False
                            for btn in cell["espresso_portion_buttons"]:
                                btn.visible = False

                        elif cell["main_espresso"].signal(event.pos):
                            print(f"Ячейка {cell['id']}: нажата кнопка 'main_espresso' - открыто меню эспрессо")

                            # Сброс состояния эспрессо
                            cell["selected_espresso_type"] = None
                            cell["selected_espresso_portion"] = 1

                            cell["espresso_menu_level"] = 1
                            cell["milk_menu_level"] = 0

                            # Показываем кнопки типа эспрессо
                            for btn in cell["espresso_type_buttons"]:
                                btn.visible = True

                            # Скрываем все кнопки молока
                            for btn in cell["milk_level1_buttons"]:
                                btn.visible = False
                            for btn in cell["milk_level2_buttons"]:
                                btn.visible = False
                            for btn in cell["espresso_portion_buttons"]:
                                btn.visible = False

                    # Уровень 1 эспрессо: выбор типа
                    elif cell["espresso_menu_level"] == 1:
                        for btn in cell["espresso_type_buttons"]:
                            if btn.signal(event.pos):
                                print(f"Ячейка {cell['id']}: нажата кнопка типа эспрессо - {btn.espresso_type}")

                                if btn.espresso_type == "back":
                                    # Возвращаемся на основной уровень
                                    cell["espresso_menu_level"] = 0
                                    for espresso_btn in cell["espresso_type_buttons"]:
                                        espresso_btn.visible = False
                                else:
                                    # Сохраняем выбранный тип и переходим к выбору порции
                                    cell["selected_espresso_type"] = btn.espresso_type
                                    cell["espresso_menu_level"] = 2

                                    # Скрываем кнопки типа
                                    for espresso_btn in cell["espresso_type_buttons"]:
                                        espresso_btn.visible = False

                                    # Показываем кнопки порций
                                    for portion_btn in cell["espresso_portion_buttons"]:
                                        portion_btn.visible = True

                                    print(f"Ячейка {cell['id']}: выбран тип - {btn.espresso_type}")

                    # Уровень 2 эспрессо: выбор порции
                    elif cell["espresso_menu_level"] == 2:
                        for btn in cell["espresso_portion_buttons"]:
                            if btn.signal(event.pos):
                                print(f"Ячейка {cell['id']}: нажата кнопка порции эспрессо")

                                if hasattr(btn, 'is_back') and btn.is_back:
                                    # Возвращаемся к выбору типа
                                    cell["espresso_menu_level"] = 1

                                    # Скрываем кнопки порций
                                    for portion_btn in cell["espresso_portion_buttons"]:
                                        portion_btn.visible = False

                                    # Показываем кнопки типа
                                    for type_btn in cell["espresso_type_buttons"]:
                                        type_btn.visible = True

                                    print(f"Ячейка {cell['id']}: возврат к выбору типа")
                                else:
                                    # Сохраняем выбранную порцию
                                    cell["selected_espresso_portion"] = btn.portion

                                    # Возвращаемся на основной уровень
                                    cell["espresso_menu_level"] = 3

                                    # Скрываем кнопки порций
                                    for portion_btn in cell["espresso_portion_buttons"]:
                                        portion_btn.visible = False

                                    print(f"Ячейка {cell['id']}: выбрано {btn.portion} порций эспрессо")
                                    print(f"  Тип: {cell['selected_espresso_type']}")
                                    print(f"  Порций: {cell['selected_espresso_portion']}")

                    # Уровень 3 эспрессо: мини-игра (остановка ползунка)
                    elif cell["espresso_menu_level"] == 3:
                        # Кнопка остановки ползунка
                        if cell["espresso_stop_button"].signal(event.pos) and not cell.get("roast_slider_stopped", False):
                            zone_start = cell.get("ideal_zone_start", 40)
                            zone_end = cell.get("ideal_zone_end", 60)
                            stop_position = cell["roast_slider_progress"]

                            # Определяем целевой прогресс обжарки
                            if zone_start <= stop_position <= zone_end:
                                # Если в зеленой зоне - заполняем до конца зеленой зоны
                                cell["roast_target_progress"] = zone_end
                                print(f"Ячейка {cell['id']}: ✓ УСПЕХ! Ползунок в зеленой зоне ({stop_position:.1f}%)")
                            else:
                                # Если вне зеленой зоны - заполняем до позиции ползунка
                                cell["roast_target_progress"] = stop_position
                                print(f"Ячейка {cell['id']}: ✗ ПРОМАХ! Ползунок вне зеленой зоны ({stop_position:.1f}%)")

                            cell["roast_slider_stopped"] = True
                            cell["roast_slider_stop_position"] = stop_position
                            print(f"Целевой прогресс обжарки: {cell['roast_target_progress']:.1f}%")

                        # Кнопка начала обжарки (только если ползунок уже остановлен)
                        elif cell["espresso_start_button"].signal(event.pos) and cell.get("roast_slider_stopped", False):
                            # Начинаем обжарку
                            print(f"Ячейка {cell['id']}: начата обжарка эспрессо")
                            cell["espresso_menu_level"] = 4
                            cell["is_roasting"] = True
                            cell["roast_progress"] = 0
                            cell["roast_start_time"] = current_time

            # Отпускание кнопки мыши
            elif event.type == py.MOUSEBUTTONUP:
                for cell in self.cells:
                    if cell["is_pouring"]:
                        self.finish_pouring(cell)
                        cell["is_pouring"] = False

    def update_roasting(self, cell, current_time):
        """ Обновление процесса обжарки """
        if not cell.get("is_roasting", False):
            return

        if "roast_start_time" not in cell:
            cell["roast_start_time"] = current_time
            return

        target_progress = cell.get("roast_target_progress", 0)
        stop_position = cell.get("roast_slider_stop_position", 0)
        zone_start = cell.get("ideal_zone_start", 40)
        zone_end = cell.get("ideal_zone_end", 60)

        # Определяем время обжарки
        if zone_start <= stop_position <= zone_end:
            # Если попали в зеленую зону - быстро (2 секунды)
            roast_time = 2.0
        else:
            # Если промахнулись - медленнее (4 секунды)
            roast_time = 4.0

        # Вычисляем прогресс обжарки
        elapsed_time = (current_time - cell["roast_start_time"]) / 1000.0
        progress = min(target_progress, (elapsed_time / roast_time) * 100)
        cell["roast_progress"] = progress

        # Если достигли цели
        if progress >= target_progress:
            quality = "отличное" if zone_start <= stop_position <= zone_end else "среднее"
            print(f"Ячейка {cell['id']}: эспрессо готово! Качество: {quality}")

            if self.build_station:
                self.build_station.add_ready_drink(
                    drink_type="espresso",
                    espresso_type=cell["selected_espresso_type"],
                    espresso_quality=quality
                )
            else:
                print("ОШИБКА: BuildStation не подключена!")

            cell["espresso_menu_level"] = 0
            cell["is_roasting"] = False

            # Сброс всех переменных мини-игры
            cell["roast_slider_progress"] = 0
            cell["roast_slider_stopped"] = False
            cell["roast_slider_direction"] = 1
            cell["roast_target_progress"] = 0
            cell["roast_progress"] = 0
            cell.pop("roast_start_time", None)
            cell.pop("roast_slider_stop_position", None)

            # Сброс выбора эспрессо
            cell["selected_espresso_type"] = None
            cell["selected_espresso_portion"] = 1

    def draw_roast_timer(self, screen, cell):
        """ Отрисовка таймера обжарки """
        x, y = cell["x"], cell["y"]

        # Позиция таймера
        timer_y = y + 20
        timer_height = 40
        timer_width = 260

        # Фон таймера
        py.draw.rect(screen, (80, 80, 80), (x + 20, timer_y, timer_width, timer_height))

        # Заполненная часть
        fill_width = int(timer_width * (cell["roast_progress"] / 100))
        py.draw.rect(screen, YELLOW, (x + 20, timer_y, fill_width, timer_height))

        # Целевая отметка
        target_progress = cell.get("roast_target_progress", 0)
        if target_progress > 0:
            target_x = x + 20 + int(timer_width * (target_progress / 100))
            target_width = 10
            py.draw.rect(screen, GREEN, (target_x, timer_y, target_width, timer_height))

        # Контур
        py.draw.rect(screen, (40, 40, 40), (x + 20, timer_y, timer_width, timer_height), 3)

        # Информация о времени
        if cell.get("is_roasting", False):
            stop_position = cell.get("roast_slider_stop_position", 0)
            zone_start = cell.get("ideal_zone_start", 40)
            zone_end = cell.get("ideal_zone_end", 60)

            if zone_start <= stop_position <= zone_end:
                time_text = "Быстрая обжарка (2 сек)"
            else:
                time_text = "Медленная обжарка (4 сек)"

    def update_pouring(self, cell, current_time):
        """ Обновление процесса наливки """
        if not cell["pour_start_time"]:
            return

        mouse_pressed = py.mouse.get_pressed()[0]
        if not mouse_pressed:
            self.finish_pouring(cell)
            cell["is_pouring"] = False
        # Время с начала наливки
        elapsed_time = (current_time - cell["pour_start_time"]) / 1000.0
        max_portions = 4
        max_time = max_portions * 1.0

        # Прогресс наливки
        progress = min(100, (elapsed_time / max_time) * 100)
        cell["pour_progress"] = progress

        # Определяем сколько порций налито
        portions = min(max_portions, int(elapsed_time / 1.0))
        cell["portions_poured"] = portions

        # Обновляем заполнение порций
        if len(cell["glass_fill"]) < portions:
            cell["glass_fill"] = [True] * portions

        # Авто остановка при максимальном количестве порций
        if portions >= max_portions:
            self.finish_pouring(cell)
            cell["is_pouring"] = False

    def update_whisking(self, cell, current_time):
        """ Обновление процесса взбивания """
        if not cell["whisk_start_time"]:
            return
        elapsed_time = (current_time - cell["whisk_start_time"]) / 1000.0
        # Время взбивания зависит от порций
        portions = cell["portions_poured"]
        base_time = 6.0
        if portions == 1:
            target_time = base_time
        elif portions == 2:
            target_time = base_time * 1.5
        elif portions == 4:
            target_time = base_time * 2.0
        else:
            target_time = base_time * 2.5

        progress = min(100, (elapsed_time / target_time) * 100)
        cell["whisk_progress"] = progress

        # Авто остановка если проскочили зеленую зону
        if progress > cell["ideal_zone_end"] + 15:
            self.finish_whisking(cell, missed=True)
            cell["is_whisking"] = False

    def finish_whisking(self, cell, missed=False):
        """ Завершение взбивания """
        progress = cell["whisk_progress"]
        zone_start = cell["ideal_zone_start"]
        zone_end = cell["ideal_zone_end"]
        portions = cell["portions_poured"]
        in_green_zone = zone_start <= progress <= zone_end
        if in_green_zone:
            quality = "perfect"
            print(f"Ячейка {cell['id']}: ✓ ИДЕАЛЬНО! ({progress:.1f}%)")
        elif missed:
            quality = "missed"
            print(f"Ячейка {cell['id']}: ✗ ПРОПУЩЕНО! ({progress:.1f}%)")
        else:
            quality = "early"
            print(f"Ячейка {cell['id']}: ⚠ СЛИШКОМ РАНО! ({progress:.1f}%)")

        # Завершаем процесс, возвращаемся на уровень 0
        cell["milk_menu_level"] = 0
        cell["is_whisking"] = False
        if cell["stop_whisk_button"]:
            cell["stop_whisk_button"].visible = False

        print(f"Ячейка {cell['id']}: Молоко готово! "
              f"Тип: {cell['selected_milk_type']}, "
              f"Температура: {cell['selected_milk_temp']}, "
              f"Порций: {portions}, "
              f"Качество взбивания: {quality}")

        # Передача напитка
        if self.build_station:
            self.build_station.add_ready_drink(
                drink_type="milk",
                milk_type=cell["selected_milk_type"],
                milk_temp=cell["selected_milk_temp"]
            )
        else:
            print("ОШИБКА: BuildStation не подключена к BrewStation!")

class BuildStation(Station):
    """ Станция сборки """
    def __init__(self):
        super().__init__("Сборка", BLUE1, BLUE)
        self.ready_drinks = []
        self.dragging_drink = None
        self.dragging_offset = (0, 0)

        # Выбранный размер и финальный стакан
        self.selected_size = None
        self.show_final_stage = False

        # Параметры для финального стакана
        self.final_glass = {
            "x": 0,
            "y": 0,
            "width": 120,
            "height": 0,
            "max_percentage": 100,
            "filled_percentage": 0,
            "pouring": False,
            "pour_progress": 0,
            "pour_start_time": 0,
            "base_color": None,
            "syrup_color": None,
            "has_syrup": False
        }

        # Горизонтальная полоса с элементами над стаканом
        self.top_bar_items = []
        self.current_bar_index = 0
        self.max_visible_items = 6
        self.init_top_bar_items()

        # Кнопки перелистывания для полосы
        self.bar_prev_button = Button(40, 60, (100, 100, 150), (50, 180))
        self.bar_next_button = Button(40, 60, (100, 100, 150), (1200 - 90, 180))

        # Параметры отрисовки
        self.start_x = 50
        self.start_y = 10
        self.cell_width = 200
        self.cell_height = 200
        self.cell_spacing = 20

        # Параметры для перелистывания напитков
        self.current_start_index = 0
        self.max_visible_drinks = 5

        # Кнопки перелистывания напитков
        self.prev_button = Button(80, 40, (100, 100, 150), (10, 200))
        self.next_button = Button(80, 40, (100, 100, 150), (1200 - 90, 200))

        # Кнопки L, S, M
        self.size_buttons = []
        self.create_size_buttons()

        # Кнопка сброса
        self.reset_button = Button(150, 40, (150, 100, 100), (525, 650))
        self.reset_button.visible = False

        # Прямоугольники внизу для сборки
        self.assembly_boxes = [
            {
                "id": 0,
                "x": 150,
                "y": 450,
                "width": 300,
                "height": 200,
                "bg_color": (80, 80, 120),
                "drink": None,
            },
            {
                "id": 1,
                "x": 750,
                "y": 450,
                "width": 300,
                "height": 200,
                "bg_color": (80, 80, 120),
                "drink": None,
            }
        ]

    def init_top_bar_items(self):
        """ Инициализация горизонтальной полосы над стаканом """
        # Сиропы
        syrups = [
            {"type": "syrup", "name": "Шоколадный", "color": (101, 67, 33)},
            {"type": "syrup", "name": "Красный бархат", "color": (178, 34, 34)},
            {"type": "syrup", "name": "Солёная карамель", "color": (255, 193, 37)},
            {"type": "syrup", "name": "Сахарный сироп", "color": (255, 250, 240)}
        ]

        # Промежуток
        gap = {"type": "empty", "name": "промежуток", "color": (50, 50, 50), "is_gap": True}

        # Начальная полоса: сиропы + промежуток
        self.top_bar_items = syrups + [gap]

    def create_size_buttons(self):
        """ Создание кнопок L, S, M """
        center_x = 600
        button_y = 350
        button_spacing = 10

        sizes = ["S", "M", "L"]
        colors = [(150, 200, 150), (200, 200, 150), (200, 150, 150)]
        total_width = 3 * 80 + 2 * button_spacing
        start_x = center_x - total_width // 2

        for i, (size, color) in enumerate(zip(sizes, colors)):
            x = start_x + i * (80 + button_spacing)
            button = CircleButton(35, color, (x + 40, button_y), text=size, text_color=(0, 0, 0), font_size=30)
            button.size = size
            button.visible = False
            self.size_buttons.append(button)

    def add_ready_drink(self, drink_type, milk_type=None, milk_temp=None, espresso_type=None, espresso_quality=None):
        """ Добавить готовый напиток на станцию сборки """
        drink = {
            "type": drink_type,
            "milk_type": milk_type,
            "milk_temp": milk_temp,
            "espresso_type": espresso_type,
            "espresso_quality": espresso_quality,
            "id": len(self.ready_drinks),
            "dragging": False,
            "pos": None,
        }
        self.ready_drinks.append(drink)

        print("=" * 50)
        print(f"Добавлен напиток В BuildStation:")
        print(f"   Тип: {drink_type}")
        if milk_type:
            print(f"   Молоко: {milk_type}, Температура: {milk_temp}")
        if espresso_type:
            print(f"   Эспрессо: {espresso_type}, Качество: {espresso_quality}")
        print(f"   Всего напитков: {len(self.ready_drinks)}")
        print("=" * 50)

        drink_color = self.get_drink_color(drink)

        if drink_type == "milk":
            item = {
                "type": "milk",
                "name": f"Молоко {milk_type}" if milk_type else "Молоко",
                "color": drink_color,
                "percentage": 60,  # Молоко заполняет 60%
                "drink_data": drink.copy(),
                "pouring": False,
                "pour_progress": 0
            }
        elif drink_type == "espresso":
            item = {
                "type": "espresso",
                "name": f"Эспрессо {espresso_type}" if espresso_type else "Эспрессо",
                "color": drink_color,
                "percentage": 100,  # Эспрессо заполняет 40%
                "drink_data": drink.copy(),
                "pouring": False,
                "pour_progress": 0
            }

        # Добавляем после промежутка, если он есть
        gap_index = next((i for i, item in enumerate(self.top_bar_items) if item.get("is_gap", False)), -1)
        if gap_index != -1:
            self.top_bar_items.insert(gap_index + 1, item)
        else:
            self.top_bar_items.append(item)

        print(f"Добавлен в полосу: {item['name']}")

    def show_size_buttons(self):
        """ Показать кнопки размеров """
        for button in self.size_buttons:
            button.visible = True

    def hide_size_buttons(self):
        """ Скрыть кнопки размеров """
        for button in self.size_buttons:
            button.visible = False

    def draw_assembly_boxes(self, screen):
        """ Отрисовка прямоугольников для сборки """
        for box in self.assembly_boxes:
            x, y, width, height = box["x"], box["y"], box["width"], box["height"]

            py.draw.rect(screen, box["bg_color"], (x, y, width, height))
            py.draw.rect(screen, (40, 40, 60), (x, y, width, height), 3)

    def draw_drinks_in_boxes(self, screen):
        """ Отрисовка напитков внутри прямоугольников """
        for box in self.assembly_boxes:
            if box["drink"]:
                x = box["x"] + (box["width"] - self.cell_width) // 2
                y = box["y"] + (box["height"] - self.cell_height) // 2
                self.draw_drink_cell(screen, box["drink"], x, y, self.cell_width, self.cell_height)

    def get_visible_drinks(self):
        """ Получить список напитков для отображения на текущей странице """
        if not self.ready_drinks:
            return []
        end_index = min(self.current_start_index + self.max_visible_drinks, len(self.ready_drinks))
        return self.ready_drinks[self.current_start_index:end_index]

    def get_visible_bar_items(self):
        """ Получить видимые элементы из полосы (листание по кругу) """
        if not self.top_bar_items:
            return []

        visible_items = []
        for i in range(self.max_visible_items):
            index = (self.current_bar_index + i) % len(self.top_bar_items)
            visible_items.append(self.top_bar_items[index])

        return visible_items

    def draw(self, screen):
        """ Отрисовка станции сборки """
        screen.fill(self.bg_color)

        # Если на этапе финальной сборки
        if self.show_final_stage:
            self.draw_final_stage(screen)
            return

        # Рисуем кнопки перелистывания напитков
        if len(self.ready_drinks) > self.max_visible_drinks:
            self.prev_button.draw(screen)
            self.next_button.draw(screen)

            if self.current_start_index == 0:
                self.prev_button.change_color((70, 70, 100))
            else:
                self.prev_button.change_color((100, 100, 150))

            if self.current_start_index + self.max_visible_drinks >= len(self.ready_drinks):
                self.next_button.change_color((70, 70, 100))
            else:
                self.next_button.change_color((100, 100, 150))

        # Рисуем напитки
        visible_drinks = self.get_visible_drinks()
        if visible_drinks:
            for i, drink in enumerate(visible_drinks):
                if drink.get("dragging") and drink.get("pos"):
                    x, y = drink["pos"]
                    self.draw_drink_cell(screen, drink, x, y, self.cell_width, self.cell_height)
                else:
                    x = self.start_x + i * (self.cell_width + self.cell_spacing)
                    y = self.start_y + 40
                    drink["cell_pos"] = (x, y)
                    self.draw_drink_cell(screen, drink, x, y, self.cell_width, self.cell_height)

        # Рисуем прямоугольники для сборки
        self.draw_assembly_boxes(screen)

        # Рисуем напитки внутри прямоугольников
        self.draw_drinks_in_boxes(screen)

        # Проверяем, заполнены ли оба прямоугольника
        both_filled = (self.assembly_boxes[0]["drink"] is not None and
                       self.assembly_boxes[1]["drink"] is not None)

        # Показываем кнопки размеров если оба прямоугольника заполнены
        if both_filled:
            self.show_size_buttons()
            for button in self.size_buttons:
                button.draw(screen)
        else:
            self.hide_size_buttons()

    def draw_final_stage(self, screen):
        """ Отрисовка финальной стадии сборки """
        # Рисуем стакан
        self.draw_empty_glass(screen)

        # Рисуем серую полосу над стаканом
        self.draw_top_bar(screen)

        # Рисуем кнопку сброса
        self.reset_button.visible = True
        self.reset_button.draw(screen)

    def draw_top_bar(self, screen):
        """ Отрисовка горизонтальной полосы над стаканом """
        # Серая полоса (фон)
        bar_y = 180
        bar_height = 100
        bar_width = 1100
        bar_x = (screen.get_width() - bar_width) // 2

        # Фон полосы
        py.draw.rect(screen, (70, 70, 90), (bar_x, bar_y, bar_width, bar_height))
        py.draw.rect(screen, (40, 40, 60), (bar_x, bar_y, bar_width, bar_height), 3)

        # Всегда показываем кнопки листания
        self.bar_prev_button.draw(screen)
        self.bar_next_button.draw(screen)

        # Кнопки всегда активные
        self.bar_prev_button.change_color((100, 100, 150))
        self.bar_next_button.change_color((100, 100, 150))

        # Рисуем видимые элементы полосы
        visible_items = self.get_visible_bar_items()
        item_width = 120
        item_height = 70
        item_spacing = 20
        start_x = bar_x + 70

        for i, item in enumerate(visible_items):
            x = start_x + i * (item_width + item_spacing)
            y = bar_y + (bar_height - item_height) // 2

            # Если это промежуток - рисуем пустой прямоугольник
            if item.get("is_gap", False):
                py.draw.rect(screen, (50, 50, 50), (x, y, item_width, item_height))
                py.draw.rect(screen, (30, 30, 40), (x, y, item_width, item_height), 2)
                # Текст "промежуток"
                font = py.font.Font(None, 18)
                text = font.render("промежуток", True, (150, 150, 150))
                screen.blit(text, (x + (item_width - text.get_width()) // 2, y + 25))
            else:
                # Рисуем элемент полосы
                self.draw_bar_item(screen, item, x, y, item_width, item_height)

    def draw_bar_item(self, screen, item, x, y, width, height):
        """ Отрисовка элемента в полосе """
        # Фон элемента
        item_color = item["color"]
        py.draw.rect(screen, item_color, (x, y, width, height))

        # Обводка
        border_color = (255, 255, 100) if item.get("pouring", False) else (40, 40, 60)
        border_width = 4 if item.get("pouring", False) else 2
        py.draw.rect(screen, border_color, (x, y, width, height), border_width)

        # Название
        font = py.font.Font(None, 20)
        name = item["name"]
        # Обрезаем слишком длинные названия
        if len(name) > 12:
            name = name[:10] + ".."
        text = font.render(name, True, (255, 255, 255))
        screen.blit(text, (x + (width - text.get_width()) // 2, y + 10))

        # Тип элемента
        type_font = py.font.Font(None, 16)
        type_text = type_font.render(item["type"], True, (200, 200, 200))
        screen.blit(type_text, (x + (width - type_text.get_width()) // 2, y + 30))

        # Индикатор наливания
        if item.get("pouring", False):
            progress = item.get("pour_progress", 0)
            progress_width = int(width * progress / 100)
            progress_x = x + (width - progress_width) // 2

            # Полупрозрачный индикатор сверху
            progress_surface = py.Surface((progress_width, 10), py.SRCALPHA)
            progress_surface.fill((255, 255, 255, 150))
            screen.blit(progress_surface, (progress_x, y))

    def draw_empty_glass(self, screen):
        """ Отрисовка пустого стакана """
        center_x = screen.get_width() // 2
        center_y = 350

        # Определяем размер стакана
        if self.selected_size == "S":
            glass_height = 180
        elif self.selected_size == "M":
            glass_height = 150
        elif self.selected_size == "L":
            glass_height = 120
        else:
            glass_height = 150

        glass_width = 120

        # Сохраняем параметры
        self.final_glass["x"] = center_x - glass_width // 2
        self.final_glass["y"] = center_y
        self.final_glass["width"] = glass_width
        self.final_glass["height"] = glass_height

        x, y = self.final_glass["x"], self.final_glass["y"]

        # Фон для стакана
        bg_color = (50, 50, 80)
        py.draw.rect(screen, bg_color, (x - 10, y - 10, glass_width + 20, glass_height + 40))
        py.draw.rect(screen, (70, 70, 100), (x - 10, y - 10, glass_width + 20, glass_height + 40), 3)

        # Стакан
        glass_color = (240, 240, 240)
        py.draw.rect(screen, glass_color, (x, y, glass_width, glass_height))
        py.draw.rect(screen, (200, 200, 200), (x, y, glass_width, glass_height), 2)

        # Определяем цвет для отрисовки
        draw_color = self.final_glass["base_color"]
        if self.final_glass["has_syrup"] and self.final_glass["syrup_color"]:
            # Смешиваем цвета если есть сироп (50% основной + 50% сироп)
            if draw_color:
                draw_color = (
                    (draw_color[0] + self.final_glass["syrup_color"][0]) // 2,
                    (draw_color[1] + self.final_glass["syrup_color"][1]) // 2,
                    (draw_color[2] + self.final_glass["syrup_color"][2]) // 2
                )
            else:
                draw_color = self.final_glass["syrup_color"]

        # Заполненная часть
        filled_percentage = self.final_glass["filled_percentage"]
        if filled_percentage > 0 and draw_color:
            fill_height = int(glass_height * (filled_percentage / 100))
            fill_y = y + glass_height - fill_height

            py.draw.rect(screen, draw_color, (x + 2, fill_y, glass_width - 4, fill_height))
            py.draw.rect(screen, (220, 220, 220), (x + 2, fill_y, glass_width - 4, fill_height), 1)

        # Ножка стакана
        stem_width = glass_width // 3
        stem_height = 15
        stem_x = x + (glass_width - stem_width) // 2
        stem_y = y + glass_height
        py.draw.rect(screen, (210, 210, 210), (stem_x, stem_y, stem_width, stem_height))

    def update_pouring(self):
        """ Обновление процесса наливания """
        current_time = py.time.get_ticks()

        # Обновляем наливание для всех элементов
        for item in self.top_bar_items:
            if item.get("pouring", False):
                if "pour_start_time" not in item:
                    item["pour_start_time"] = current_time

                elapsed_time = (current_time - item["pour_start_time"]) / 1000.0
                total_pour_time = 1.5
                progress = min(100, (elapsed_time / total_pour_time) * 100)
                item["pour_progress"] = progress

                if progress >= 100:
                    # Завершаем наливание
                    self.complete_pouring(item)

    def complete_pouring(self, item):
        """ Завершение наливания элемента в стакан """
        item["pouring"] = False
        item["pour_progress"] = 0
        if "pour_start_time" in item:
            del item["pour_start_time"]

        if item["type"] == "syrup":
            # Сироп только меняет цвет, не заполняет
            self.final_glass["syrup_color"] = item["color"]
            self.final_glass["has_syrup"] = True
            print(f"Добавлен сироп: {item['name']}")
            print(f"Цвет стакана изменен")

        elif item["type"] in ["milk", "espresso"]:
            # Напиток заполняет стакан
            if self.final_glass["filled_percentage"] + item["percentage"] <= 100:
                self.final_glass["filled_percentage"] += item["percentage"]
                self.final_glass["base_color"] = item["color"]
                print(f"Добавлено: {item['name']} ({item['percentage']}%)")
                print(f"Всего заполнено: {self.final_glass['filled_percentage']}%")
            else:
                print("Стакан переполнен!")

    def handle_final_stage_events(self, event, pos):
        """ Обработка событий на финальной стадии """
        if event.type == py.MOUSEBUTTONDOWN:
            # Обработка кнопки сброса
            if self.reset_button.signal(pos):
                self.reset_all()
                return

            # Листание полосы по кругу
            if self.bar_prev_button.signal(pos):
                self.current_bar_index = (self.current_bar_index - 1) % len(self.top_bar_items)
                print(f"Листание назад. Текущий индекс: {self.current_bar_index}")

            elif self.bar_next_button.signal(pos):
                self.current_bar_index = (self.current_bar_index + 1) % len(self.top_bar_items)
                print(f"Листание вперед. Текущий индекс: {self.current_bar_index}")

            # Проверяем клик по элементам полосы
            bar_y = 180
            bar_height = 100
            bar_width = 1100
            bar_x = (1200 - bar_width) // 2

            visible_items = self.get_visible_bar_items()
            item_width = 120
            item_height = 70
            item_spacing = 20
            start_x = bar_x + 70

            for i, item in enumerate(visible_items):
                x = start_x + i * (item_width + item_spacing)
                y = bar_y + (bar_height - item_height) // 2

                # Проверяем клик по элементу
                if (not item.get("is_gap", False) and
                        x <= pos[0] <= x + item_width and
                        y <= pos[1] <= y + item_height):

                    # Проверяем можно ли добавить
                    if not item.get("pouring", False):
                        # Для напитков проверяем заполнение
                        if item["type"] in ["milk", "espresso"]:
                            if self.final_glass["filled_percentage"] + item["percentage"] <= 100:
                                item["pouring"] = True
                                item["pour_start_time"] = py.time.get_ticks()
                                print(f"Начато наливание: {item['name']}")
                            else:
                                print("Стакан переполнен!")
                        # Для сиропов всегда можно добавить
                        elif item["type"] == "syrup":
                            item["pouring"] = True
                            item["pour_start_time"] = py.time.get_ticks()
                            print(f"Начато добавление сиропа: {item['name']}")

                    break

    def reset_all(self):
        """ Сбросить все и начать заново """
        for box in self.assembly_boxes:
            box["drink"] = None

        self.selected_size = None
        self.show_final_stage = False
        self.reset_button.visible = False

        self.final_glass["filled_percentage"] = 0
        self.final_glass["pouring"] = False
        self.final_glass["pour_progress"] = 0
        self.final_glass["base_color"] = None
        self.final_glass["syrup_color"] = None
        self.final_glass["has_syrup"] = False

        # Останавливаем все наливания в полосе
        for item in self.top_bar_items:
            item["pouring"] = False
            item["pour_progress"] = 0
            if "pour_start_time" in item:
                del item["pour_start_time"]

        print("Сброшено. Можно собирать новый напиток.")

    def get_drink_at_position(self, pos):
        """ Получить напиток по позиции мыши """
        visible_drinks = self.get_visible_drinks()
        for i, drink in enumerate(visible_drinks):
            x = self.start_x + i * (self.cell_width + self.cell_spacing)
            y = self.start_y + 40

            if (x <= pos[0] <= x + self.cell_width and
                    y <= pos[1] <= y + self.cell_height):
                return drink, i
        return None, -1

    def get_box_at_position(self, pos):
        """ Получить прямоугольник по позиции мыши """
        for box in self.assembly_boxes:
            x, y, width, height = box["x"], box["y"], box["width"], box["height"]
            if (x <= pos[0] <= x + width and
                    y <= pos[1] <= y + height):
                return box
        return None

    def prev_page(self):
        """ Перейти к предыдущей странице напитков """
        if len(self.ready_drinks) > 0:
            self.current_start_index = (self.current_start_index - 1) % len(self.ready_drinks)

    def next_page(self):
        """ Перейти к следующей странице напитков """
        if len(self.ready_drinks) > 0:
            self.current_start_index = (self.current_start_index + 1) % len(self.ready_drinks)

    def draw_drink_cell(self, screen, drink, x, y, width, height):
        """ Отрисовка ячейки с напитком """
        cell_color = (70, 70, 100)
        py.draw.rect(screen, cell_color, (x, y, width, height))
        py.draw.rect(screen, (100, 100, 140), (x, y, width, height), 3)

        glass_width = 100
        glass_height = 120
        glass_x = x + (width - glass_width) // 2
        glass_y = y + 50

        if drink["type"] == "milk":
            self.draw_milk_glass(screen, drink, glass_x, glass_y, glass_width, glass_height)
        elif drink["type"] == "espresso":
            self.draw_espresso_glass(screen, drink, glass_x, glass_y, glass_width, glass_height)

    def draw_milk_glass(self, screen, drink, x, y, width, height):
        """ Отрисовка стакана с молоком """
        glass_color = (240, 240, 240)
        py.draw.rect(screen, glass_color, (x, y, width, height))
        py.draw.rect(screen, (200, 200, 200), (x, y, width, height), 2)

        milk_color = WHITE
        if drink["milk_type"] == "STRAWBERRY_MILK":
            milk_color = (255, 200, 220)
        if drink["milk_temp"] == "hot":
            milk_color = tuple(min(255, c + 20) for c in milk_color)

        fill_height = height - 15
        fill_y = y + 5
        py.draw.rect(screen, milk_color, (x + 2, fill_y, width - 4, fill_height))

        foam_color = tuple(min(255, c + 30) for c in milk_color)
        foam_height = 20
        py.draw.rect(screen, foam_color, (x + 2, fill_y, width - 4, foam_height))

        stem_width = width // 3
        stem_height = 10
        stem_x = x + (width - stem_width) // 2
        stem_y = y + height
        py.draw.rect(screen, (210, 210, 210), (stem_x, stem_y, stem_width, stem_height))

    def draw_espresso_glass(self, screen, drink, x, y, width, height):
        """ Отрисовка стакана с эспрессо """
        glass_color = (240, 240, 240)
        py.draw.rect(screen, glass_color, (x, y, width, height))
        py.draw.rect(screen, (200, 200, 200), (x, y, width, height), 2)

        espresso_color = CITY_ROAST
        if drink["espresso_type"] == "DECAF_ROAST":
            espresso_color = DECAF_ROAST

        if drink["espresso_quality"] == "отличное":
            espresso_color = tuple(min(255, c + 20) for c in espresso_color)
        elif drink["espresso_quality"] == "среднее":
            espresso_color = tuple(min(255, c + 40) for c in espresso_color)

        fill_height = (height - 15) * 0.6
        fill_y = y + height - fill_height - 5
        py.draw.rect(screen, espresso_color, (x + 2, fill_y, width - 4, fill_height))

        cream_color = tuple(min(255, c + 50) for c in espresso_color)
        cream_height = 10
        py.draw.rect(screen, cream_color, (x + 2, fill_y, width - 4, cream_height))

        stem_width = width // 3
        stem_height = 10
        stem_x = x + (width - stem_width) // 2
        stem_y = y + height
        py.draw.rect(screen, (210, 210, 210), (stem_x, stem_y, stem_width, stem_height))

    def get_drink_color(self, drink):
        """ Получить цвет напитка """
        if drink["type"] == "milk":
            milk_color = WHITE
            if drink["milk_type"] == "STRAWBERRY_MILK":
                milk_color = (255, 200, 220)
            if drink["milk_temp"] == "hot":
                milk_color = tuple(min(255, c + 20) for c in milk_color)
            return milk_color
        else:
            espresso_color = CITY_ROAST if drink["espresso_type"] == "CITY_ROAST" else DECAF_ROAST
            if drink["espresso_quality"] == "отличное":
                espresso_color = tuple(min(255, c + 20) for c in espresso_color)
            elif drink["espresso_quality"] == "среднее":
                espresso_color = tuple(min(255, c + 40) for c in espresso_color)
            return espresso_color

    def events(self, events):
        """ Обработка событий на станции сборки """
        # Обновляем процессы наливания
        if self.show_final_stage:
            self.update_pouring()

        for event in events:
            if event.type == py.MOUSEBUTTONDOWN:
                pos = event.pos

                # Если на этапе финальной сборки
                if self.show_final_stage:
                    self.handle_final_stage_events(event, pos)
                    return

                # Обработка кнопок перелистывания напитков
                if len(self.ready_drinks) > 0:
                    if self.prev_button.signal(pos):
                        self.prev_page()
                    elif self.next_button.signal(pos):
                        self.next_page()

                # Обработка кнопок размеров
                if (self.assembly_boxes[0]["drink"] is not None and
                        self.assembly_boxes[1]["drink"] is not None and
                        not self.selected_size):

                    for button in self.size_buttons:
                        if button.visible and button.signal(pos):
                            self.selected_size = button.size
                            self.show_final_stage = True
                            print(f"Выбран размер: {button.size}")
                            self.hide_size_buttons()
                            break

                # Начало перетаскивания напитка
                if not self.selected_size:
                    drink, index = self.get_drink_at_position(pos)
                    if drink:
                        self.dragging_drink = drink
                        drink["dragging"] = True
                        cell_x = self.start_x + index * (self.cell_width + self.cell_spacing)
                        cell_y = self.start_y + 40
                        self.dragging_offset = (pos[0] - cell_x, pos[1] - cell_y)

            elif event.type == py.MOUSEMOTION:
                if self.dragging_drink:
                    self.dragging_drink["pos"] = (
                        event.pos[0] - self.dragging_offset[0],
                        event.pos[1] - self.dragging_offset[1]
                    )

            elif event.type == py.MOUSEBUTTONUP:
                if self.dragging_drink:
                    pos = event.pos
                    box = self.get_box_at_position(pos)

                    if box and box["drink"] is None:
                        box["drink"] = self.dragging_drink.copy()

                        visible_drinks = self.get_visible_drinks()
                        if self.dragging_drink in visible_drinks:
                            index_in_visible = visible_drinks.index(self.dragging_drink)
                            global_index = (self.current_start_index + index_in_visible) % len(self.ready_drinks)
                            self.ready_drinks.pop(global_index)

                            # Обновляем индекс если нужно
                            if self.current_start_index >= len(self.ready_drinks) > 0:
                                self.current_start_index %= len(self.ready_drinks)

                    self.dragging_drink["dragging"] = False
                    self.dragging_drink["pos"] = None
                    self.dragging_drink = None
                    self.dragging_offset = (0, 0)

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
        self.connect_stations()
        self.update_navigation()

    def connect_stations(self):
        """ Связываем станции между собой """
        brew_station = self.stations["brew"]
        build_station = self.stations["build"]

        # Передаем ссылку на build_station в brew_station
        brew_station.build_station = build_station

        # Отладочная информация
        print("=== СВЯЗЬ СТАНЦИЙ ===")
        print(f"BrewStation имеет ссылку на BuildStation: {brew_station.build_station is not None}")
        print("=====================")

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
                if self.show_left_button and self.navigation_buttons['left'].signal(event.pos):
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