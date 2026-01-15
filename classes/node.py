import pygame as py

class Label:
    """ Текст """
    def __init__(self, font_path):
        self.font_path = font_path

    def text_ret(self, size, text, color, antialias=True):
        """ Создание переменной текста """  
        label = py.font.Font(self.font_path, size)
        return label.render(text, antialias, color)

class Button:
    """ Кнопки """
    def __init__(self, width, height, bg_color, pos):
        self.width = width
        self.height = height
        self.bg_color = bg_color
        self.pos = pos
        self.border_width = 3
        self.image = py.Surface((self.width, self.height))
        self.image.fill(bg_color)
        py.draw.rect(self.image, (58, 58, 80), (0, 0, self.width, self.height), self.border_width)
        self.rect = self.image.get_rect(topleft=self.pos)

    def redraw(self):
        """ Перерисовка с новым цветом """
        self.image = py.Surface((self.width, self.height))
        self.image.fill(self.bg_color)
        py.draw.rect(self.image, (58, 58, 80), (0, 0, self.width, self.height), self.border_width)
        self.rect = self.image.get_rect(topleft=self.pos)

    def change_color(self, new_color):
        """ Получаем новый цвет """
        self.bg_color = new_color
        self.redraw()

    def draw(self, screen):
        """ Отображение кнопки """
        screen.blit(self.image, self.rect)

    def signal(self, pos):
        """ Получение сигнала """
        return self.rect.collidepoint(pos)

class CircleButton:
    """ Круглые кнопки с текстом """
    def __init__(self, radius, bg_color, pos, text="", text_color=(0, 0, 0), font_size=20):
        self.radius = radius
        self.bg_color = bg_color
        self.pos = pos
        self.text = text
        self.text_color = text_color
        self.font_size = font_size
        self.border_width = 3
        diameter = radius * 2
        self.image = py.Surface((diameter, diameter), py.SRCALPHA)
        self.font = py.font.Font(None, font_size)

        self.redraw()
        self.rect = self.image.get_rect(center=pos)

        self.visible = True
        self.was_clicked = False

    def redraw(self):
        """ Перерисовка кнопки с текстом """
        diameter = self.radius * 2
        self.image.fill((0, 0, 0, 0))

        # Рисуем круг
        py.draw.circle(self.image, self.bg_color, (self.radius, self.radius), self.radius)
        py.draw.circle(self.image, (58, 58, 80), (self.radius, self.radius), self.radius, self.border_width)

        # Если есть текст
        if self.text:
            text_surface = self.font.render(self.text, True, self.text_color)

            # Центрируем текст
            text_rect = text_surface.get_rect(center=(self.radius, self.radius))

            # Проверяем, помещается ли текст в круг
            text_width, text_height = text_surface.get_size()
            max_dimension = self.radius * 1.5

            # Если текст слишком большой
            if text_width > max_dimension or text_height > max_dimension:
                scale = min(max_dimension / text_width, max_dimension / text_height)
                new_font_size = max(12, int(self.font_size * scale * 0.8))
                self.font = py.font.Font(None, new_font_size)
                text_surface = self.font.render(self.text, True, self.text_color)
                text_rect = text_surface.get_rect(center=(self.radius, self.radius))

            self.image.blit(text_surface, text_rect)

    def change_color(self, new_color):
        """ Смена цвета фона """
        self.bg_color = new_color
        self.redraw()

    def change_text_color(self, new_color):
        """ Смена цвета текста """
        self.text_color = new_color
        self.redraw()

    def set_text(self, text):
        """ Изменить текст кнопки """
        self.text = text
        self.redraw()

    def set_font_size(self, size):
        """ Изменить размер шрифта """
        self.font_size = size
        self.font = py.font.Font(None, size)
        self.redraw()

    def draw(self, screen):
        """ Отрисовка кнопки """
        if self.visible:
            screen.blit(self.image, self.rect)

    def signal(self, pos):
        """ Получение сигнала (клик) """
        if not self.visible:
            return False

        distance = ((pos[0] - self.rect.centerx) ** 2 + (pos[1] - self.rect.centery) ** 2) ** 0.5
        return distance <= self.radius

    def set_visible(self, visible):
        """ Установить видимость кнопки """
        self.visible = visible
        self.redraw()

    def set_pos(self, pos):
        """ Изменить положение кнопки """
        self.pos = pos
        self.rect = self.image.get_rect(center=pos)
        self.redraw()