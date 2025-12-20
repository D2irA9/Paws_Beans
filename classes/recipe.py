import pygame as py, random

class Recipe:
    """ Класс рецепты """
    def __init__(self):
        self.cup_sizes = ["S", "M", "L"]
        self.cup = ''
        self.milk = 0
        self.espresso = 0
        self.glass = {
            "cup": '',
            "SM": 0,
            "SE": 0,
        }

    def generate_random_order(self):
        """Генерирует случайный заказ"""
        self.cup = random.choice(self.cup_sizes)
        if self.cup == "S":
            self.espresso = random.randint(1, 4)
            self.milk = 4 - self.espresso
        elif self.cup == "M":
            self.espresso = random.randint(1, 5)
            self.milk = 5 - self.espresso
        else:
            self.espresso = random.randint(1, 6)
            self.milk = 6 - self.espresso

        return {
            "cup": self.cup,
            "SM": self.milk,
            "SE": self.espresso
        }

    def draw_order(self, screen, pos, color, border_color, font, text_color,  order, num_order=None):
        """ Отрисовка заказа """
        order_cup = order['cup']
        order_SM = order["SM"]
        order_SE = order["SE"]
        width = 200
        heigth = 300

        py.draw.rect(screen, color, (pos[0], pos[1], width, heigth))
        py.draw.rect(screen, border_color, (pos[0], pos[1], width, heigth), 3)

        lines = [
            '#1',
            f'{order_cup}',
            f'Milk: {order_SM}',
            f'Espresso: {order_SE}',
        ]

        text_surfaces = []
        for line in lines:
            text_surface = font.text_ret(size=32, text=line, color=text_color)
            text_surfaces.append(text_surface)

        line_height = 40
        start_y = pos[1] + 30

        for i, text_surface in enumerate(text_surfaces):
            text_rect = text_surface.get_rect()
            text_rect.centerx = pos[0] + width // 2
            text_rect.y = start_y + i * line_height
            screen.blit(text_surface, text_rect)