import pygame as py, random

class Order:
    """ Класс заказов """
    def __init__(self):
        self.milk = ['SKIM_MILK', 'STRAWBERRY_MILK']
        self.espresso = ['CITY_ROAST', 'DECAF_ROAST']
        self.cups = ['S', 'M', 'L']
        self.syrups = ['CHOCOLATE', 'RED_VELVET', 'SALTED_CARAMEL', 'SUGARPLUM']

    def generate_random_order(self):
        """Генерирует случайный заказ"""
