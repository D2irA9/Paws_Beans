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

        for i, (x, y) in enumerate(self.cells_pos):
            cell = {
                "id": i,
                "x": x,
                "y": y,
                "main_milk": CircleButton(30, WHITE, (x + 150, y + 125)),
                "main_espresso": CircleButton(30, (110, 59, 9), (x + 150, y + 375)),

                # Уровни меню(0-основное, 1-тип, 2-температура, 3-наливка, 4-взбивание)
                "milk_menu_level": 0,
                "show_espresso_menu": False,

                # Кнопки для каждого уровня
                "milk_level1_buttons": [],
                "milk_level2_buttons": [],
                "espresso_buttons": [],

                # Кнопка наливки
                "pour_button": None,

                # Кнопка остановки взбивания
                "stop_whisk_button": None,

                # Выбранные значения
                "selected_milk_type": None,
                "selected_milk_temp": None,
                "selected_espresso": None,

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
            }

            # Уровень 1
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

            # Уровень 2
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
                cell["espresso_buttons"].append(btn)

            self.cells.append(cell)

    def draw(self, screen):
        """ Отрисовка станции приготовления """
        screen.fill(self.bg_color)

        for cell in self.cells:
            x, y = cell["x"], cell["y"]

            # Уровень 0
            if cell["milk_menu_level"] == 0 and not cell["show_espresso_menu"]:
                py.draw.rect(screen, ORANGE1, (x, y, 300, 500))
                py.draw.rect(screen, CONTOUR, (x, y, 300, 500), 3)
                cell["main_milk"].draw(screen)
                cell["main_espresso"].draw(screen)

            # Уровень 1
            elif cell["milk_menu_level"] == 1:
                py.draw.rect(screen, ORANGE1, (x, y, 300, 500))
                py.draw.rect(screen, CONTOUR, (x, y, 300, 500), 3)
                for btn in cell["milk_level1_buttons"]:
                    if btn.visible:
                        btn.draw(screen)

            # Уровень 2
            elif cell["milk_menu_level"] == 2:
                py.draw.rect(screen, ORANGE1, (x, y, 300, 500))
                py.draw.rect(screen, CONTOUR, (x, y, 300, 500), 3)
                for btn in cell["milk_level2_buttons"]:
                    if btn.visible:
                        btn.draw(screen)

            # Уровень 3
            elif cell["milk_menu_level"] == 3:
                self.draw_pour_level(screen, cell)

            # Уровень 4
            elif cell["milk_menu_level"] == 4:
                self.draw_whisk_level(screen, cell)

            # Меню эспрессо
            elif cell["show_espresso_menu"]:
                py.draw.rect(screen, ORANGE1, (x, y, 300, 500))
                py.draw.rect(screen, CONTOUR, (x, y, 300, 500), 3)
                for btn in cell["espresso_buttons"]:
                    if btn.visible:
                        btn.draw(screen)

    def draw_pour_level(self, screen, cell):
        """ Отрисовка уровня 3: наливка молока """
        x, y = cell["x"], cell["y"]

        # Основная ячейка
        py.draw.rect(screen, ORANGE1, (x, y, 300, 500))
        py.draw.rect(screen, CONTOUR, (x, y, 300, 500), 3)

        # Темный прямоугольник для стакана
        dark_rect_y = y + 50
        dark_rect_height = 300
        darker_orange = (140, 60, 0)
        py.draw.rect(screen, darker_orange,
                     (x + 20, dark_rect_y, 260, dark_rect_height))
        py.draw.rect(screen, CONTOUR,
                     (x + 20, dark_rect_y, 260, dark_rect_height), 2)

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
            py.draw.line(screen, (180, 180, 180),
                         (glass_x, divider_y), (glass_x + glass_width, divider_y), 1)

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

        # Ножка стакана
        stem_width = glass_width // 3
        stem_height = 15
        stem_x = glass_x + (glass_width - stem_width) // 2
        stem_y = glass_y + glass_height
        py.draw.rect(screen, (210, 210, 210),
                     (stem_x, stem_y, stem_width, stem_height))

        # Кнопка наливки
        if cell["pour_button"] and cell["pour_button"].visible:
            cell["pour_button"].draw(screen)

        # Инструкция
        instruction_y = y + 420
        font = py.font.Font(None, 22)
        if cell["is_pouring"]:
            instruction = font.render("Держите для наливания...", True, WHITE)
        else:
            instruction = font.render("Нажмите и держите кнопку", True, WHITE)
        screen.blit(instruction, (x + 60, instruction_y))

        # Индикатор порций
        portions_font = py.font.Font(None, 20)
        portions_text = portions_font.render(f"Порций: {cell['portions_poured']}/4", True, WHITE)
        screen.blit(portions_text, (x + 20, y + 20))

    def draw_whisk_level(self, screen, cell):
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
        py.draw.rect(screen, darker_orange,
                     (x + 20, dark_rect_y, 260, dark_rect_height))
        py.draw.rect(screen, CONTOUR,
                     (x + 20, dark_rect_y, 260, dark_rect_height), 2)

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
            py.draw.line(screen, (180, 180, 180),
                         (glass_x, divider_y), (glass_x + glass_width, divider_y), 1)

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

        # Ножка стакана
        stem_width = glass_width // 3
        stem_height = 15
        stem_x = glass_x + (glass_width - stem_width) // 2
        stem_y = glass_y + glass_height
        py.draw.rect(screen, (210, 210, 210),
                     (stem_x, stem_y, stem_width, stem_height))

        # Кнопка остановки
        if cell["stop_whisk_button"] and cell["stop_whisk_button"].visible:
            cell["stop_whisk_button"].draw(screen)

        # Инструкция
        instruction_y = y + 420
        font = py.font.Font(None, 22)
        instruction = font.render("Нажмите 'Остановить' в зеленой зоне", True, WHITE)
        screen.blit(instruction, (x + 40, instruction_y))

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

        # Текст прогресса
        font = py.font.Font(None, 24)
        progress_text = font.render(f"{int(cell['whisk_progress'])}%", True, BLACK)
        text_rect = progress_text.get_rect(center=(x + 150, timer_y + timer_height // 2))
        screen.blit(progress_text, text_rect)

        # Информация о порциях
        portions_font = py.font.Font(None, 20)
        portions_text = portions_font.render(f"Порций: {portions}", True, WHITE)
        screen.blit(portions_text, (x + 20, timer_y - 25))

        # Подсказка
        hint_font = py.font.Font(None, 18)
        hint_text = hint_font.render("Нажмите когда желтый дойдет до зеленого", True, WHITE)
        screen.blit(hint_text, (x + 30, timer_y + timer_height + 5))

    def events(self, events):
        """ Обработка событий на станции приготовления """
        current_time = py.time.get_ticks()
        # Обновление процессов
        for cell in self.cells:
            if cell["is_pouring"]:
                self.update_pouring(cell, current_time)
            if cell["is_whisking"]:
                self.update_whisking(cell, current_time)

        for event in events:
            if event.type == py.MOUSEBUTTONDOWN:
                for cell in self.cells:

                    # Уровень 3
                    if cell["milk_menu_level"] == 3:
                        if cell["pour_button"] and cell["pour_button"].signal(event.pos):
                            print(f"Ячейка {cell['id']}: начата наливка молока")
                            cell["is_pouring"] = True
                            cell["pour_start_time"] = current_time
                            cell["pour_progress"] = 0
                            cell["glass_fill"] = []
                            cell["portions_poured"] = 0

                    # Уровень 4:
                    elif cell["milk_menu_level"] == 4:
                        if cell["stop_whisk_button"] and cell["stop_whisk_button"].signal(event.pos):
                            self.finish_whisking(cell)
                            cell["is_whisking"] = False

                    # Уровень 1
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

                    # Уровень 2
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

                    # Уровень 0
                    elif cell["milk_menu_level"] == 0 and not cell["show_espresso_menu"]:
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
                            cell["show_espresso_menu"] = False

                            for btn in cell["milk_level1_buttons"]:
                                btn.visible = True
                            for btn in cell["milk_level2_buttons"]:
                                btn.visible = False
                            for btn in cell["espresso_buttons"]:
                                btn.visible = False

                        elif cell["main_espresso"].signal(event.pos):
                            print(f"Ячейка {cell['id']}: открыто меню эспрессо")
                            cell["show_espresso_menu"] = True
                            cell["milk_menu_level"] = 0

                            for btn in cell["espresso_buttons"]:
                                btn.visible = True

                            for btn in cell["milk_level1_buttons"]:
                                btn.visible = False
                            for btn in cell["milk_level2_buttons"]:
                                btn.visible = False

                    # Меню эспрессо
                    elif cell["show_espresso_menu"]:
                        for btn in cell["espresso_buttons"]:
                            if btn.signal(event.pos):
                                if btn.espresso_type == "back":
                                    cell["show_espresso_menu"] = False
                                    for espresso_btn in cell["espresso_buttons"]:
                                        espresso_btn.visible = False
                                else:
                                    cell["selected_espresso"] = btn.espresso_type

            # Отпускание кнопки мыши
            elif event.type == py.MOUSEBUTTONUP:
                for cell in self.cells:
                    if cell["is_pouring"]:
                        self.finish_pouring(cell)
                        cell["is_pouring"] = False

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

    def finish_pouring(self, cell):
        """ Завершение наливки и переход к взбиванию """
        portions = cell["portions_poured"]
        print(f"Ячейка {cell['id']}: налито {portions} порций")

        # Переход на уровень 4
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