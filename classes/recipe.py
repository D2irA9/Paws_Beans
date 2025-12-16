import pygame as py, random

class Recipe:
    """ Класс рецепты """

    def __init__(self):
        # self.milk_types = ["обычное"] # "обезжиренное", "соевое"
        # self.espresso_types = ["кофе"] # "городское", "без кофеина"
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

        # milk = random.choice(self.milk_types)
        # espresso = random.choice(self.espresso_types)

        return {
            "cup": cup,
            # "milk": milk,
            "SM": SM,
            # "espresso": espresso,
            "SE": SE
        }