import pygame as py, random

class Recipe:
    """ Класс рецепты """
    def __init__(self):
        self.cup_sizes = ["S", "M", "L"]

    def generate_random_order(self):
        """Генерирует случайный заказ"""
        cup = random.choice(self.cup_sizes)
        if cup == "S":
            SE = random.randint(1, 4)
            SM = 4 - SE
        elif cup == "M":
            SE = random.randint(1, 5)
            SM = 5 - SE
        else:
            SE = random.randint(1, 6)
            SM = 6 - SE

        return {
            "cup": cup,
            "SM": SM,
            "SE": SE
        }