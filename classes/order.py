from globals import *
import random

class Order:
    """ Класс заказов """
    def __init__(self):
        self.milk = ['SKIM_MILK', 'STRAWBERRY_MILK']
        self.espresso = ['CITY_ROAST', 'DECAF_ROAST']
        self.cup_capacity = {'S': 6, 'M': 5, 'L': 4}
        self.syrups = ['CHOCOLATE', 'RED_VELVET', 'SALTED_CARAMEL', 'SUGARPLUM']

        # Цвета для сиропов
        self.syrup_colors = {
            'CHOCOLATE': (139, 69, 19),  # Коричневый
            'RED_VELVET': (178, 34, 34),  # Красный бархат
            'SALTED_CARAMEL': (210, 180, 140),  # Карамельный
            'SUGARPLUM': (221, 160, 221)  # Сливовый
        }

        # Цвета для молока
        self.milk_colors = {
            'SKIM_MILK': (255, 250, 240),  # Обезжиренное
            'STRAWBERRY_MILK': (255, 182, 193)  # Клубничное
        }

        # Цвета для эспрессо
        self.espresso_colors = {
            'CITY_ROAST': (101, 67, 33),  # Темный
            'DECAF_ROAST': (139, 90, 43)  # Светлее
        }
        self.current_order = self.generate_random_order()

    def generate_random_order(self):
        """Генерирует случайный заказ"""

        # Выбираем стакан
        cup = random.choice(['S', 'M', 'L'])
        capacity = self.cup_capacity[cup]

        # Максимальное количество эспрессо
        max_esp = max(1, capacity - 2)

        # Количество эспрессо
        esp_qty = random.randint(1, max_esp)

        # Создаем заказ
        return {
            'cup': cup,
            'cup_capacity': capacity,
            'espresso': {
                'type': random.choice(self.espresso),
                'portions': esp_qty
            },
            'milk': {
                'type': random.choice(self.milk),
                'portions': capacity - esp_qty
            },
            'syrup': random.choice(self.syrups)
        }

    def draw_order(self, screen):
        """ Отображение заказа """
        x, y = 920, 0
        width, height = 280, 400

        # Основной прямоугольник
        py.draw.rect(screen, ORDER_TICKET, (x, y, width, height))
        py.draw.rect(screen, CONTOUR, (x, y, width, height), 3)

        # Разделительные линии
        syrup_rect = (x, y, width, 40)
        py.draw.rect(screen, CONTOUR, syrup_rect, 1)

        # Средняя часть
        milk_espresso_rect = (x, y + 40, width, 360)
        py.draw.rect(screen, CONTOUR, milk_espresso_rect, 1)

        # Нижняя часть
        cup_rect = (x, y + 40 + 360, width, 40)
        py.draw.rect(screen, CONTOUR, cup_rect, 1)

        # Отрисовка сиропа
        self._draw_syrup_section(screen, x, y, width)

        # Отрисовка молока и эспрессо
        self._draw_milk_espresso_section(screen, x, y + 40, width, 360)

        # Отрисовка стакана
        self._draw_cup_section(screen, x, y + 400, width, 40)

    def _draw_syrup_section(self, screen, x, y, width):
        """ Отрисовка секции сиропа """
        # Фон сиропа
        syrup_color = self.syrup_colors.get(self.current_order['syrup'], (200, 200, 200))
        py.draw.rect(screen, syrup_color, (x + 2, y + 2, width - 4, 36))

        # Название сиропа
        font = py.font.Font(None, 28)
        text = font.render(f"{self.current_order['syrup']}", True, (0, 0, 0))
        text_rect = text.get_rect(center=(x + width // 2, y + 20))
        screen.blit(text, text_rect)

    def _draw_milk_espresso_section(self, screen, x, y, width, height):
        """ Отрисовка секции молока и эспрессо """
        # Разделяем среднюю часть пополам
        milk_width = width // 2
        espresso_width = width - milk_width

        # Молоко
        milk_rect = (x, y, milk_width, height)
        py.draw.rect(screen, CONTOUR, milk_rect, 1)  # Контур

        # Цвет молока
        milk_color = self.milk_colors.get(self.current_order['milk']['type'], (255, 255, 255))
        py.draw.rect(screen, milk_color, (x + 2, y + 2, milk_width - 4, height - 4))

        # Информация о молоке
        milk_font = py.font.Font(None, 24)
        milk_type_text = milk_font.render(self.current_order['milk']['type'], True, (0, 0, 0))
        milk_qty_text = milk_font.render(f"x{self.current_order['milk']['portions']}", True, (0, 0, 0))

        screen.blit(milk_type_text, (x + 10, y + 10))
        screen.blit(milk_qty_text, (x + 10, y + 40))

        # Эспрессо
        espresso_x = x + milk_width
        espresso_rect = (espresso_x, y, espresso_width, height)
        py.draw.rect(screen, CONTOUR, espresso_rect, 1)  # Контур

        # Цвет эспрессо
        espresso_color = self.espresso_colors.get(self.current_order['espresso']['type'], (101, 67, 33))
        py.draw.rect(screen, espresso_color, (espresso_x + 2, y + 2, espresso_width - 4, height - 4))

        # Информация об эспрессо
        espresso_type_text = milk_font.render(self.current_order['espresso']['type'], True, (255, 255, 255))
        espresso_qty_text = milk_font.render(f"x{self.current_order['espresso']['portions']}", True, (255, 255, 255))

        screen.blit(espresso_type_text, (espresso_x + 10, y + 10))
        screen.blit(espresso_qty_text, (espresso_x + 10, y + 40))

        # Вертикальная разделительная линия
        py.draw.line(screen, CONTOUR, (x + milk_width, y), (x + milk_width, y + height), 2)

    def _draw_cup_section(self, screen, x, y, width, height):
        """ Отрисовка секции стакана """
        # Фон
        py.draw.rect(screen, (240, 240, 240), (x + 2, y + 2, width - 4, height - 4))

        # Буква стакана
        font = py.font.Font(None, 48)

        # Цвет буквы в зависимости от размера
        cup_color = {
            'S': (0, 128, 0),  # Зеленый для Small
            'M': (255, 165, 0),  # Оранжевый для Medium
            'L': (255, 0, 0)  # Красный для Large
        }.get(self.current_order['cup'], (0, 0, 0))

        # Отображаем букву стакана
        cup_text = font.render(self.current_order['cup'], True, cup_color)
        text_rect = cup_text.get_rect(center=(x + width // 2, y + height // 2))
        screen.blit(cup_text, text_rect)

    def generate_new_order(self):
        """ Сгенерировать новый заказ """
        self.current_order = self.generate_random_order()
        print(f"Новый заказ: {self.current_order}")

    def event(self, event):
        """ Обработка событий """

order = Order()