from globals import *
from game import game

# # # Настройки
clock = py.time.Clock()
fps = 30

# # # Переменные
game_show = False

def screen_saver():
    """ Заставка """
    screen.fill(BLACK)

    lines = [
        'ВНИМАНИЕ: ПРОТОТИП!',
        'Игра ещё не обрела свою окончательную форму.',
        'Ваше мур-мнение помогут нам стать лучше!',
        '[тг: @D2i_rA9]'
    ]

    text_surfaces = []
    for line in lines:
        text_surface = font.text_ret(size=24, text=line, color=WHITE)
        text_surfaces.append(text_surface)

    line_height = 30
    total_height = len(lines) * line_height

    start_y = (720 - total_height) // 2

    for i, text_surface in enumerate(text_surfaces):
        text_rect = text_surface.get_rect()
        text_rect.centerx = 1200 // 2
        text_rect.y = start_y + i * line_height
        screen.blit(text_surface, text_rect)

    l5 = font.text_ret(size=18, text='(Нажмите любую клавишу)', color=GRAY)
    l5_rect = l5.get_rect()
    l5_rect.centerx = 1200 // 2
    l5_rect.y = start_y + 4 * line_height + 20
    screen.blit(l5, l5_rect)

while True:
    events = py.event.get()
    for event in events:
        if event.type == py.QUIT:
            py.quit()
            sys.exit()
        elif event.type == py.KEYDOWN:
            if event.key == py.K_LALT:
                py.quit()
                sys.exit()
            else:
                game_show = True

    if not game_show:
        screen_saver()
    else:
        game(events)

    py.display.flip()
    clock.tick(fps)