from globals import *
from game import game
from classes.db import DB
import json, os

# # # Настройки
clock = py.time.Clock()
fps = 30

# # # Переменные
condition = ['Заставка', 'Регистрация', 'Игра']
specific_condition = condition[0]
db = DB()

# Параметры входа
user_id = None
username = None

SESSION_FILE = "user_session.json"

def check_session():
    """ Проверка, есть ли сохраненная сессия """
    try:
        if os.path.exists(SESSION_FILE):
            with open(SESSION_FILE, 'r', encoding='utf-8') as f:
                data = f.read().strip()
                if data:  # Если файл не пустой
                    session = json.loads(data)
                    if 'user_id' in session and 'username' in session:
                        global current_user_id, current_username
                        current_user_id = session['user_id']
                        current_username = session['username']
                        return True
    except Exception as e:
        print(f"Ошибка загрузки сессии: {e}")
    return False

def save_session(user_id, username):
    """Сохраняем сессию пользователя"""
    try:
        session_data = {
            'user_id': user_id,
            'username': username
        }
        with open(SESSION_FILE, 'w', encoding='utf-8') as f:
            json.dump(session_data, f, indent=4)
    except Exception as e:
        print(f"Ошибка сохранения сессии: {e}")

def screen_saver():
    """ Заставка """
    py.display.set_caption("Предупреждение")
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

def screen_registration():
    """ Регистрация """
    py.display.set_caption("Регистрация")

    # Поле для ввода имени
    input_box = py.Rect(500, 350, 200, 50)
    input_text = ''
    active = False
    color_inactive = py.Color('lightskyblue3')
    color_active = py.Color('dodgerblue2')
    color = color_inactive

    # Шрифт
    font_reg = py.font.Font(None, 32)

    # Сообщение об ошибке/успехе
    message = ''
    message_color = WHITE

    running = True
    while running:
        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                sys.exit()

            if event.type == py.MOUSEBUTTONDOWN:
                # Проверяем клик по полю ввода
                if input_box.collidepoint(event.pos):
                    active = True
                else:
                    active = False
                color = color_active if active else color_inactive

            if event.type == py.KEYDOWN:
                if event.key == py.K_ESCAPE:
                    return None

                if active:
                    if event.key == py.K_RETURN and input_text.strip():
                        username = input_text.strip()

                        # Подключаемся к БД и добавляем пользователя
                        db.connect()
                        user_id = db.add_user(username)

                        if user_id:
                            global current_user_id, current_username
                            current_user_id = user_id
                            current_username = username

                            # Сохраняем сессию
                            save_session(user_id, username)

                            message = f"Привет, {username}!"
                            message_color = GREEN
                            py.time.wait(1500)
                            running = False
                        else:
                            message = "Ошибка регистрации! Имя занято?"
                            message_color = RED

                    elif event.key == py.K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        # Ограничиваем длину имени
                        if len(input_text) < 20 and event.unicode.isprintable():
                            input_text += event.unicode

        # Отрисовка
        screen.fill(BLACK)

        # Заголовок
        title = font.text_ret(size=48, text="Регистрация", color=WHITE)
        title_rect = title.get_rect(center=(600, 150))
        screen.blit(title, title_rect)

        # Инструкция
        instr = font.text_ret(size=24, text="Введите ваше имя:", color=WHITE)
        instr_rect = instr.get_rect(center=(600, 300))
        screen.blit(instr, instr_rect)

        # Поле ввода
        py.draw.rect(screen, color, input_box, 2)
        text_surface = font_reg.render(input_text, True, WHITE)
        screen.blit(text_surface, (input_box.x + 5, input_box.y + 10))

        # Подсказка
        hint = font.text_ret(size=18, text="Нажмите Enter для подтверждения", color=GRAY)
        hint_rect = hint.get_rect(center=(600, 450))
        screen.blit(hint, hint_rect)

        # Сообщение
        if message:
            msg_surface = font.text_ret(size=24, text=message, color=message_color)
            msg_rect = msg_surface.get_rect(center=(600, 500))
            screen.blit(msg_surface, msg_rect)

        py.display.flip()
        clock.tick(fps)

    return condition[2]

has_session = check_session()

while True:
    events = py.event.get()
    for event in events:
        if event.type == py.QUIT:
            py.quit()
            sys.exit()
            db.close()
        elif event.type == py.KEYDOWN:
            if event.key == py.K_LALT:
                py.quit()
                sys.exit()
                db.close()
            else:
                if specific_condition == condition[0]:
                    if has_session:
                        # Если есть сохраненная сессия, сразу в игру
                        specific_condition = condition[2]
                    else:
                        # Иначе в регистрацию
                        specific_condition = condition[1]

    if specific_condition == condition[0]:
        screen_saver()
    elif specific_condition == condition[1]:
        specific_condition = screen_registration()
    else:
        game(events)

    py.display.flip()
    clock.tick(fps)