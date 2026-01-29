import pygame as py, random

class Order:
    """ Класс заказов """
    def __init__(self):
        self.milk = ['SKIM_MILK', 'STRAWBERRY_MILK']
        self.espresso = ['CITY_ROAST', 'DECAF_ROAST']
        self.cup_capacity = {'S': 6, 'M': 5, 'L': 4}
        self.syrups = ['CHOCOLATE', 'RED_VELVET', 'SALTED_CARAMEL', 'SUGARPLUM']

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