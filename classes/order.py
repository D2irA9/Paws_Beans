import pygame as py, random

class Order:
    """ Класс заказов """
    def __init__(self):
        self.milk = ['skimmed milk', 'strawberry milk']
        self.espresso = ['city roast', 'decaf roast']
        self.cups = ['small', 'medium', 'large']
        self.syrups = ['chocolate', 'red velvet', 'salted caramel', 'sugarplum']
        self.ice = ['ice cubes']

    def generate_random_order(self):
        """Генерирует случайный заказ"""
