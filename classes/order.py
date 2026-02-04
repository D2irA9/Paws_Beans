import random
from globals import *

class Order:
    """ Класс заказов """
    def __init__(self):
        self.milk = ['SKIM_MILK', 'STRAWBERRY_MILK']
        self.milk_temperatures = ['HOT', 'COLD']
        self.espresso = ['CITY_ROAST', 'DECAF_ROAST']
        self.cup_capacity = {'S': 6, 'M': 5, 'L': 4}
        self.syrups = ['CHOCOLATE', 'RED_VELVET', 'SALTED_CARAMEL', 'SUGARPLUM']

        # Цвета для сиропов
        self.syrup_colors = {
            'CHOCOLATE': CHOCOLATE,
            'RED_VELVET': RED_VELVET,
            'SALTED_CARAMEL': SALTED_CARAMEL,
            'SUGARPLUM': SUGARPLUM
        }

        # Цвета для молока
        self.milk_colors = {
            'SKIM_MILK': SKIM_MILK,
            'STRAWBERRY_MILK': STRAWBERRY_MILK
        }

        self.temperature_symbols = {
            'HOT': 'Г',
            'COLD': 'Х'
        }

        # Цвета для эспрессо
        self.espresso_colors = {
            'CITY_ROAST': CITY_ROAST,
            'DECAF_ROAST': DECAF_ROAST
        }

        self.current_order = self.generate_random_order()
        self.show_order = False
        self.order_visible = False
        self.milk = ['SKIM_MILK', 'STRAWBERRY_MILK']
        self.espresso = ['CITY_ROAST', 'DECAF_ROAST']
        self.cup_capacity = {'S': 6, 'M': 5, 'L': 4}
        self.syrups = ['CHOCOLATE', 'RED_VELVET', 'SALTED_CARAMEL', 'SUGARPLUM']

    def generate_random_order(self):
        """Генерирует случайный заказ с гибким распределением порций"""
        cup = random.choice(['S', 'M', 'L'])
        capacity = self.cup_capacity[cup]

        esp_qty = random.randint(1, min(3, capacity - 1))
        milk_qty = capacity - esp_qty
        if milk_qty > 4:
            milk_qty = random.randint(1, min(4, capacity - 1))
            esp_qty = capacity - milk_qty

        milk_temp = random.choice(self.milk_temperatures)

        print(f"Сгенерирован заказ: размер {cup}, емкость {capacity}")
        print(f"  Эспрессо: {esp_qty} порций (допустимо 1-3)")
        print(f"  Молоко: {milk_qty} порций (допустимо 1-4)")
        print(f"  Сумма: {esp_qty + milk_qty} порций")

        return {
            'cup': cup,
            'cup_capacity': capacity,
            'espresso': {
                'type': random.choice(self.espresso),
                'portions': esp_qty
            },
            'milk': {
                'type': random.choice(self.milk),
                'portions': milk_qty,
                'temperature': milk_temp
            },
            'syrup': random.choice(self.syrups)
        }

    def draw_order(self, screen):
        """ Отображение тикета заказа """
        x, y = 920, 0
        width, height = 280, 400

        # Основной прямоугольник
        py.draw.rect(screen, ORDER_TICKET, (x, y, width, height))
        py.draw.rect(screen, CONTOUR, (x, y, width, height), 3)

        # Разделительные линии
        syrup_rect = (x, y, width, 40)
        py.draw.rect(screen, CONTOUR, syrup_rect, 3)

        # Средняя часть
        milk_espresso_rect = (x, y + 40, width, 360)
        py.draw.rect(screen, CONTOUR, milk_espresso_rect, 3)

        # Нижняя часть
        cup_rect = (x, y + 40 + 360, width, 40)
        py.draw.rect(screen, CONTOUR, cup_rect, 3)

        # Отрисовка сиропа
        self._draw_syrup_section(screen, x, y, width)

        # Отрисовка молока и эспрессо
        self._draw_milk_espresso_section(screen, x, y + 40, width, 360)

        # Отрисовка стакана
        self._draw_cup_section(screen, x, y + 400, width, 40)

    def _draw_syrup_section(self, screen, x, y, width):
        """ Отрисовка секции сиропа """
        syrup_color = self.syrup_colors.get(self.current_order['syrup'], (200, 200, 200))
        py.draw.rect(screen, syrup_color, (x + 2, y + 2, width - 4, 36))

        font = py.font.Font(None, 28)
        text = font.render(f"{self.current_order['syrup']}", True, (0, 0, 0))
        text_rect = text.get_rect(center=(x + width // 2, y + 20))
        screen.blit(text, text_rect)

    def _draw_milk_espresso_section(self, screen, x, y, width, height):
        """ Отрисовка секции молока и эспрессо """
        milk_width = width // 2
        espresso_width = width - milk_width

        # Молоко
        milk_color = self.milk_colors.get(self.current_order['milk']['type'], (255, 255, 255))
        py.draw.rect(screen, milk_color, (x + 2, y + 2, milk_width - 4, height - 4))
        py.draw.rect(screen, CONTOUR, (x, y, milk_width, height), 1)

        # Эспрессо
        espresso_x = x + milk_width
        espresso_color = self.espresso_colors.get(self.current_order['espresso']['type'], (101, 67, 33))
        py.draw.rect(screen, espresso_color, (espresso_x + 2, y + 2, espresso_width - 4, height - 4))
        py.draw.rect(screen, CONTOUR, (espresso_x, y, espresso_width, height), 1)

        # Вертикальная разделительная линия
        py.draw.line(screen, CONTOUR, (x + milk_width, y), (x + milk_width, y + height), 2)

        # Текст для молока
        milk_font = py.font.Font(None, 24)
        milk_type_text = milk_font.render(self.current_order['milk']['type'], True, (0, 0, 0))
        milk_qty_text = milk_font.render(f"x{self.current_order['milk']['portions']}", True, (0, 0, 0))
        screen.blit(milk_type_text, (x + 10, y + 10))
        screen.blit(milk_qty_text, (x + 10, y + 40))

        # Температура молока
        temp_symbol = self.temperature_symbols.get(self.current_order['milk']['temperature'], '?')
        temp_text = milk_font.render(f"{temp_symbol} {self.current_order['milk']['temperature']}",  True, BLACK)

        screen.blit(milk_type_text, (x + 10, y + 10))
        screen.blit(milk_qty_text, (x + 10, y + 40))
        screen.blit(temp_text, (x + 10, y + 70))

        # Текст для эспрессо
        espresso_type_text = milk_font.render(self.current_order['espresso']['type'], True, (255, 255, 255))
        espresso_qty_text = milk_font.render(f"x{self.current_order['espresso']['portions']}", True, (255, 255, 255))
        screen.blit(espresso_type_text, (espresso_x + 10, y + 10))
        screen.blit(espresso_qty_text, (espresso_x + 10, y + 40))

    def _draw_cup_section(self, screen, x, y, width, height):
        """ Отрисовка секции стакана """
        py.draw.rect(screen, (240, 240, 240), (x + 2, y + 2, width - 4, height - 4))

        font = py.font.Font(None, 48)
        cup_color = {
            'S': (0, 128, 0),
            'M': (255, 165, 0),
            'L': (255, 0, 0)
        }.get(self.current_order['cup'], (0, 0, 0))

        cup_text = font.render(self.current_order['cup'], True, cup_color)
        text_rect = cup_text.get_rect(center=(x + width // 2, y + height // 2))
        screen.blit(cup_text, text_rect)

    def _draw_click_indicator(self, screen):
        """ Отрисовка мини тикета """
        x, y = 970, 0
        width, height = 50, 100

        # Простой зеленый квадратик
        py.draw.rect(screen, ORDER_TICKET, (x, y, width, height))
        py.draw.rect(screen, CONTOUR, (x, y, width, height), 3)

    def generate_new_order(self):
        """ Сгенерировать новый заказ """
        self.current_order = self.generate_random_order()
        print(f"Новый заказ: {self.current_order}")

    def events(self, events):
        """ Обработка событий """
        for event in events:
            if event.type == py.KEYDOWN:
                if event.key == py.K_SPACE:
                    self.show_order = not self.show_order

    def draw(self, screen):
        """ Отрисовка заказа """
        if self.show_order  and self.order_visible:
            self.draw_order(screen)
        else:
            self._draw_click_indicator(screen)


order = Order()