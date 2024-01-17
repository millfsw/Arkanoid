import pygame
import os
import sys
from pygame.locals import *

# Инициализация игры
pygame.init()
pygame.display.set_caption("Арканоид")


SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 1580, 900
screen = pygame.display.set_mode(SCREEN_SIZE, pygame.SCALED | pygame.FULLSCREEN)

clock = pygame.time.Clock()

name_player = ""
data_player = ""

running = True
is_pause = False
is_menu = False

# Константы
FPS = 60

COLOR_LIGHT = (170, 170, 170)
COLOR_DARK = (100, 100, 100)

PLATFORM_WIDTH = 250
PLATFORM_HEIGHT = 100

BALL_RADIUS = 70

BLOCK_WIDTH = 130
BLOCK_HEIGHT = 80
BLOCK_GAP = 25


class Platform(pygame.sprite.Sprite):
    # Этот класс отвечает за платформу в виде обезьянки. С помощью этого класса платформа двигается влево и вправо при нажатии на стрелочки
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(
            load_image("monkey.png"), (PLATFORM_WIDTH, PLATFORM_HEIGHT)
        )
        self.image.set_colorkey(0)
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH // 2 - PLATFORM_WIDTH // 2
        self.rect.y = SCREEN_HEIGHT - PLATFORM_HEIGHT
        self.platform_speed = 10

    def update(self):
        # Функция отвечает за обновление местоположения платформы
        d = pygame.key.get_pressed()
        if d[K_LEFT] and self.rect.left > 0:
            self.rect.left -= self.platform_speed
        if d[K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.right += self.platform_speed


class Ball(pygame.sprite.Sprite):
    # Этот класс отвечает за мячик в виде кокоса. С помощью этого класса мячик отскакивает от платформы и разбивает блоки
    def __init__(self):
        super().__init__()
        sprite = sprite_selection("Мяч")
        self.image = pygame.transform.scale(
            load_image(sprite), (BALL_RADIUS, BALL_RADIUS)
        )
        self.image.set_colorkey(0)
        self.rect = self.image.get_rect()
        self.rect.x = (SCREEN_WIDTH - BALL_RADIUS) // 2
        self.rect.y = SCREEN_HEIGHT - PLATFORM_HEIGHT - BALL_RADIUS * 2 - 10
        self.ball_speed_x = 6
        self.ball_speed_y = -6

    def update(self):
        # Функция отвечает за обновление местоположения платформы и за проыерку столкновения с платформой и границами экрана
        if Rect(
            self.rect.x,
            self.rect.y + self.ball_speed_y,
            BALL_RADIUS,
            BALL_RADIUS,
        ).colliderect(platform):
            file = open("data/colors.txt")
            lines = file.read().splitlines()
            sound = pygame.mixer.Sound("data/collision_1.wav")
            if lines[1] == "green":
                sound.play()
            else:
                pygame.mixer.pause()
            self.ball_speed_x, self.ball_speed_y = detect_collision(
                self.ball_speed_x, self.ball_speed_y, self.rect, platform.rect
            )

        self.rect.x += self.ball_speed_x
        self.rect.y += self.ball_speed_y

        if self.rect.left < 10 or self.rect.right >= SCREEN_WIDTH:
            self.ball_speed_x *= -1
        if self.rect.top < 10:
            self.ball_speed_y *= -1
        if self.rect.colliderect(platform):
            file = open("data/colors.txt")
            lines = file.read().splitlines()
            sound = pygame.mixer.Sound("data/collision_1.wav")
            if lines[1] == "green":
                sound.play()
            else:
                pygame.mixer.pause()
            self.ball_speed_x, self.ball_speed_y = detect_collision(
                self.ball_speed_x, self.ball_speed_y, self.rect, platform.rect
            )


class Block(pygame.sprite.Sprite):
    # Класс отвечает за  блоки в виде бананов, арбузов и анасов, которые можно изменить в настройках
    def __init__(self, x, y):
        super().__init__()
        sprite = sprite_selection("Блок")
        self.image = pygame.transform.scale(
            load_image(sprite), (BLOCK_WIDTH, BLOCK_HEIGHT)
        )
        self.image.set_colorkey(0)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        # Функция, которая проверяет столкновение с мячом
        if self.rect.colliderect(ball):
            file = open("data/colors.txt")
            lines = file.read().splitlines()
            sound = pygame.mixer.Sound("data/collision_2.wav")
            if lines[1] == "green":
                sound.play()
            else:
                pygame.mixer.pause()
            ball.ball_speed_x, ball.ball_speed_y = detect_collision(
                ball.ball_speed_x,
                ball.ball_speed_y,
                ball.rect,
                self.rect,
            )


class No_Destructive_Block(pygame.sprite.Sprite):
    # Класс отвечает за неразрушаемые блоки в виде дощечек
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(
            load_image("block.png"), (BLOCK_WIDTH, BLOCK_HEIGHT)
        )
        self.image.set_colorkey(0)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        # Функция, которая проверяет столкновение с мячом
        if self.rect.colliderect(ball):
            file = open("data/colors.txt")
            lines = file.read().splitlines()
            sound = pygame.mixer.Sound("data/collision_1.wav")
            if lines[1] == "green":
                sound.play()
            else:
                pygame.mixer.pause()
            ball.ball_speed_x, ball.ball_speed_y = detect_collision(
                ball.ball_speed_x,
                ball.ball_speed_y,
                ball.rect,
                self.rect,
            )


def terminate():
    # Эта функция отвечает за выход из игры
    pygame.quit()
    sys.exit()


def sprite_selection(object_sprite):
    # Выбор страйта обЪекта засчеь выбранной настройки
    file = open("data/colors.txt", "r")
    lines = file.read().splitlines()
    if object_sprite == "Блок":
        sprite = "banana.png" if lines[4] == "green" else "pineapple.png"

    elif object_sprite == "Мяч":
        sprite = "coconut.png" if lines[2] == "green" else "watermelon.png"

    return sprite


def play_music(res):
    # Проигрыш музыки
    pygame.mixer.music.load("data/music.mp3")
    if res == "play":
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.1)
    else:
        pygame.mixer.music.pause()


def writing_to_file(data_player):
    # Функция записывает в БД данные игрока
    f = open("data/data_players.txt", "a")
    f.write("\t".join(map(str, data_player)))
    f.write("\n")


def score_identifier(selected_level):
    # Функция, которая подсчитывает кол-во общих очков для пользователя после окончания игры исходя из уровня
    if selected_level == 1:
        data_player[1] = max(int(score), int(data_player[1]))

    elif selected_level == 2:
        data_player[1] = max(int(data_player[1]), score + 400)

    elif selected_level == 3:
        data_player[1] = max(int(data_player[1]), score + 600)


def load_image(name, color_key=None):
    # Эта функция отвечает за загрузку картинок по имени файла
    fullname = os.path.join("data", name)
    try:
        image = pygame.image.load(fullname).convert_alpha()
    except pygame.error as message:
        print("Cannot load image:", name)
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


def open_guide_window():
    # Эта функция отвечает за открытие гайда по игре
    guide_font = pygame.font.SysFont("Corbel", 35)
    guide_title = guide_font.render("Гайд по игре 'Арканоид'", True, "black")
    guide_text = [
        "Добро пожаловать в игру 'Арканоид'",
        "",
        "Цель:",
        "  - Разрушить все фрукты на уровне, отбивая кокос с помощью обезьянки.",
        "",
        "Управление:",
        "  - Используйте стрелки для управления обезьянкой",
        "  - Нажмите ESC для выхода из игры",
        "  - Нажмите Space, чтобы поставить паузу в игре или снять игру с паузы",
        "",
        "Геймплей:",
        "  - Кокос отскакивает от обезьянки, фруктов и дощечек",
        "  - Разбейте все фрукты для того, чтобы пройти на следующий уровень.",
        "  - Если кокос уйдет за нижнию границу экрана, игра будет окончено",
        "  - Накапливайте очки за каждый фрукт и попади в рейтин лучших",
        "  - На уровнях могут попадаться дощечки, которые не ломаются",
        "",
        "Наслаждайтесь игрой 'Арканоид'!",
    ]

    screen.fill((207, 143, 103))
    screen.blit(guide_title, (250, 50))

    guide_y = 120

    for line in guide_text:
        guide_line = guide_font.render(line, True, "black")
        screen.blit(guide_line, (250, guide_y))
        guide_y += 40

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            elif event.type == pygame.KEYDOWN and event.key == K_ESCAPE:
                return

        pygame.display.flip()


def open_settings_window():
    # Функция отвечает за открытие настроек. В txt-файле записаны цвета, в соответствии с этим меняются кнопки цветом. С помощью кнопок можно включать и выключать звук и музыку и изменять спрайты блоков, плтаформы и мячика
    settings_screen = pygame.display.set_mode(
        SCREEN_SIZE, pygame.SCALED | pygame.FULLSCREEN
    )
    settings_screen.fill((207, 143, 103))

    red = (255, 0, 0)
    green = (0, 255, 0)

    file = open("data/colors.txt", "r")
    lines = file.read().splitlines()
    pygame.draw.rect(settings_screen, lines[0], [200, 50, 200, 50])
    pygame.draw.rect(settings_screen, lines[1], [200, 200, 200, 50])
    pygame.draw.rect(settings_screen, lines[2], [200, 350, 200, 50])
    pygame.draw.rect(settings_screen, lines[3], [200, 500, 200, 50])
    pygame.draw.rect(settings_screen, lines[4], [1000, 350, 200, 50])
    pygame.draw.rect(settings_screen, lines[5], [1000, 500, 200, 50])
    file.close()

    note = pygame.transform.scale(load_image("note.png"), (70, 70))
    note_rect = (100, 50, 70, 70)
    settings_screen.blit(note, note_rect)

    rupor = pygame.transform.scale(load_image("rupor.png"), (70, 70))
    rupor_rect = (100, 200, 70, 70)
    settings_screen.blit(rupor, rupor_rect)

    coconut = pygame.transform.scale(load_image("coconut.png"), (80, 70))
    coconut_rect = (90, 350, 80, 70)
    settings_screen.blit(coconut, coconut_rect)

    watermelon = pygame.transform.scale(load_image("watermelon.png"), (80, 70))
    watermelon_rect = (85, 500, 80, 70)
    settings_screen.blit(watermelon, watermelon_rect)

    banana = pygame.transform.scale(load_image("banana.png"), (80, 70))
    banana_rect = (900, 350, 80, 70)
    settings_screen.blit(banana, banana_rect)

    pineapple = pygame.transform.scale(load_image("pineapple.png"), (80, 70))
    pineapple_rect = (900, 500, 80, 70)
    settings_screen.blit(pineapple, pineapple_rect)

    while True:
        d = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or d[pygame.K_ESCAPE]:
                f = open("data/colors.txt", "w")
                for line in lines:
                    f.write(line)
                    f.write("\n")
                f.close()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 200 <= mouse[0] <= 400 and 50 <= mouse[1] <= 100:
                    pygame.mixer.Sound("data/clicked_button.wav").play()
                    if lines[0] == "red":
                        lines[0] = "green"
                        play_music("play")
                    else:
                        lines[0] = "red"
                        play_music("stop")
                    pygame.draw.rect(settings_screen, lines[0], [200, 50, 200, 50])

                if 200 <= mouse[0] <= 400 and 200 <= mouse[1] <= 250:
                    pygame.mixer.Sound("data/clicked_button.wav").play()
                    if lines[1] == "red":
                        lines[1] = "green"
                    else:
                        lines[1] = "red"
                    pygame.draw.rect(settings_screen, lines[1], [200, 200, 200, 50])

                if 200 <= mouse[0] <= 400 and 350 <= mouse[1] <= 400:
                    pygame.mixer.Sound("data/clicked_button.wav").play()
                    if lines[2] == "red":
                        lines[2] = "green"
                    else:
                        lines[2] = "red"
                    pygame.draw.rect(settings_screen, lines[2], [200, 350, 200, 50])

                if 200 <= mouse[0] <= 400 and 500 <= mouse[1] <= 550:
                    pygame.mixer.Sound("data/clicked_button.wav").play()
                    if lines[3] == "green":
                        lines[3] = "red"
                    else:
                        lines[3] = "green"
                    pygame.draw.rect(settings_screen, lines[3], [200, 500, 200, 50])

                if 1000 <= mouse[0] <= 1200 and 350 <= mouse[1] <= 400:
                    pygame.mixer.Sound("data/clicked_button.wav").play()
                    if lines[4] == "red":
                        lines[4] = "green"
                    else:
                        lines[4] = "red"
                    pygame.draw.rect(settings_screen, lines[4], [1000, 350, 200, 50])

                if 1000 <= mouse[0] <= 1200 and 500 <= mouse[1] <= 550:
                    pygame.mixer.Sound("data/clicked_button.wav").play()
                    if lines[5] == "green":
                        lines[5] = "red"
                    else:
                        lines[5] = "green"
                    pygame.draw.rect(settings_screen, lines[5], [1000, 500, 200, 50])

        pygame.display.flip()

        pygame.display.flip()


def registration_window():
    # Функция отвечает за открытие окна регистрации игрока. Здесь сверяются его введеные данные, которые потом берутся из БД или создаются новые
    global name_player, data_player

    registr_fon = pygame.transform.scale(load_image("result_window.png"), (1580, 900))
    font = pygame.font.SysFont(None, 100)
    name_font = pygame.font.SysFont("MAIN_FONT", 80)
    active = False
    text = ""

    while True:
        data_player = ""
        screen.blit(registr_fon, (0, 0))

        event_list = pygame.event.get()

        for event in event_list:

            if event.type == pygame.QUIT:
                terminate()

            elif event.type == pygame.KEYDOWN and event.key == K_ESCAPE:
                start_screen()
                return

            elif event.type == pygame.KEYDOWN and event.key == K_RETURN:
                name_player = text

                with open("data/data_players.txt") as f:
                    lines = f.read().splitlines()
                    for i in range(len(lines)):
                        if lines[i].split("\t")[0] == name_player:
                            data_player = lines.pop(i).split("\t")
                            break
                    f.close()

                    f = open("data/data_players.txt", "w")
                    for line in lines:
                        f.write(f"{line}\n")
                    f.close()

                    if not data_player:
                        data_player = [name_player, "0", "1"]

                return

        t_surf = font.render(text, True, "white", None)
        enter_name = name_font.render("Введите свой никнейм:", True, "white")

        image = pygame.Surface(
            (max(700, t_surf.get_width() + 10), t_surf.get_height() + 10),
            pygame.SRCALPHA,
        )

        image.blit(t_surf, (5, 5))

        pygame.draw.rect(image, "white", image.get_rect().inflate(-2, -2), 2)
        rect = image.get_rect(topleft=(700, 450))

        screen.blit(image, (700, 450))
        screen.blit(enter_name, (SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT // 2 - 60))

        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and not active:
                active = rect.collidepoint(event.pos)
            if event.type == pygame.KEYDOWN and active:
                if event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode

        pygame.display.flip()


def open_rating_window():
    # Функция, которая открывает окно рейтинга, в котором в порядке уменьшения кол-ва очков расположены топ-10 игроков
    rating_fon = pygame.transform.scale(load_image("result_window.png"), (1580, 900))

    smallfont = pygame.font.SysFont("Corbel", 35)

    text_name = smallfont.render("Игрок", True, "white")
    text_score = smallfont.render("Очки", True, "white")

    with open("data/data_players.txt") as f:
        data_players = f.read().splitlines()

    data_players = sorted(data_players, key=lambda x: -int(x.split("\t")[1]))

    while True:
        screen.blit(rating_fon, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN and event.key == K_ESCAPE:
                return

        rating_list = []

        for i in range(min(len(data_players), 10)):
            rating_list.append(data_players[i])

        y = 150

        for player in rating_list:
            name = smallfont.render(player.split("\t")[0], True, "white")
            score = smallfont.render(player.split("\t")[1], True, "white")
            screen.blit(name, (855, y))
            screen.blit(score, (1170, y))
            y += 45

        pygame.draw.rect(screen, COLOR_DARK, [770, 100, 250, 40])
        pygame.draw.rect(screen, COLOR_DARK, [1070, 100, 250, 40])

        screen.blit(text_name, (850, 103))
        screen.blit(text_score, (1155, 103))

        pygame.display.flip()


def start_screen():
    # Функция, которая инициализирует главное меню игры
    file = open("data/colors.txt")
    lines = file.read().splitlines()
    if lines[0] == "green":
        play_music("play")
    else:
        play_music("stop")
    pygame.mouse.set_visible(True)
    fon = pygame.transform.scale(load_image("start_window.png"), (1580, 900))

    smallfont = pygame.font.SysFont("Corbel", 35)

    cup_image = load_image("cup.png")

    text_play = smallfont.render("Играть", True, "white")
    text_quit = smallfont.render("Выйти", True, "white")
    text_settings = smallfont.render("Настройки", True, "white")
    text_guide = smallfont.render("Справка", True, "white")

    while True:
        screen.blit(fon, (0, 0))

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                terminate()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if (
                    SCREEN_WIDTH / 2 - 150 <= mouse[0] <= SCREEN_WIDTH / 2 + 100
                    and 550 <= mouse[1] <= 590
                ):
                    registration_window()
                    return

                elif (
                    SCREEN_WIDTH / 2 - 150 <= mouse[0] <= SCREEN_WIDTH / 2 + 100
                    and 600 <= mouse[1] <= 640
                ):
                    open_settings_window()

                elif (
                    SCREEN_WIDTH / 2 - 150 <= mouse[0] <= SCREEN_WIDTH / 2 + 100
                    and 650 <= mouse[1] <= 690
                ):
                    open_guide_window()

                elif (
                    SCREEN_WIDTH / 2 - 150 <= mouse[0] <= SCREEN_WIDTH / 2 + 100
                    and 700 <= mouse[1] <= 740
                ):
                    terminate()

                elif (
                    30 <= mouse[0] <= 90
                    and SCREEN_HEIGHT - 90 <= mouse[1] <= SCREEN_HEIGHT - 30
                ):
                    open_rating_window()

        mouse = pygame.mouse.get_pos()

        if (
            30 <= mouse[0] <= 90
            and SCREEN_HEIGHT - 90 <= mouse[1] <= SCREEN_HEIGHT - 30
        ):
            pygame.draw.rect(screen, COLOR_LIGHT, [30, SCREEN_HEIGHT - 90, 60, 60])
        else:
            pygame.draw.rect(screen, COLOR_DARK, [30, SCREEN_HEIGHT - 90, 60, 60])

        if (
            SCREEN_WIDTH / 2 - 150 <= mouse[0] <= SCREEN_WIDTH / 2 + 100
            and 550 <= mouse[1] <= 590
        ):
            pygame.draw.rect(
                screen, COLOR_LIGHT, [SCREEN_WIDTH / 2 - 150, 550, 250, 40]
            )
        else:
            pygame.draw.rect(screen, COLOR_DARK, [SCREEN_WIDTH / 2 - 150, 550, 250, 40])

        if (
            SCREEN_WIDTH / 2 - 150 <= mouse[0] <= SCREEN_WIDTH / 2 + 100
            and 600 <= mouse[1] <= 640
        ):
            pygame.draw.rect(
                screen, COLOR_LIGHT, [SCREEN_WIDTH / 2 - 150, 600, 250, 40]
            )
        else:
            pygame.draw.rect(screen, COLOR_DARK, [SCREEN_WIDTH / 2 - 150, 600, 250, 40])

        if (
            SCREEN_WIDTH / 2 - 150 <= mouse[0] <= SCREEN_WIDTH / 2 + 100
            and 650 <= mouse[1] <= 690
        ):
            pygame.draw.rect(
                screen, COLOR_LIGHT, [SCREEN_WIDTH / 2 - 150, 650, 250, 40]
            )
        else:
            pygame.draw.rect(screen, COLOR_DARK, [SCREEN_WIDTH / 2 - 150, 650, 250, 40])

        if (
            SCREEN_WIDTH / 2 - 150 <= mouse[0] <= SCREEN_WIDTH / 2 + 100
            and 700 <= mouse[1] <= 740
        ):
            pygame.draw.rect(
                screen, COLOR_LIGHT, [SCREEN_WIDTH / 2 - 150, 700, 250, 40]
            )
        else:
            pygame.draw.rect(screen, COLOR_DARK, [SCREEN_WIDTH / 2 - 150, 700, 250, 40])

        screen.blit(text_play, (SCREEN_WIDTH / 2 - 80, 555))
        screen.blit(text_settings, (SCREEN_WIDTH / 2 - 105, 605))
        screen.blit(text_guide, (SCREEN_WIDTH / 2 - 90, 655))
        screen.blit(text_quit, (SCREEN_WIDTH / 2 - 75, 705))
        screen.blit(cup_image, [30, SCREEN_HEIGHT - 90, 60, 60])

        pygame.display.flip()


def show_result_window(result, data_player):
    # Функция, которая отвечает за окно после окончания игры: как за проигрыш, так и за выигрыш
    global selected_level, score

    result_screen = pygame.transform.scale(load_image("result_window.png"), (1580, 900))

    result_font = pygame.font.SysFont("MAIN_FONT", 80)

    if result == "win":
        if selected_level == 1:
            data_player[1] = max(int(data_player[1]), score)
            result_text = result_font.render("Победа!", True, "white")
            file = open("data/colors.txt")
            lines = file.read().splitlines()
            sound = pygame.mixer.Sound("data/win.wav")
            if lines[1] == "green":
                sound.play()
            else:
                pygame.mixer.pause()

        elif selected_level == 2:
            data_player[1] = max(int(data_player[1]), 400 + score)
            result_text = result_font.render("Победа!", True, "white")
            file = open("data/colors.txt")
            lines = file.read().splitlines()
            sound = pygame.mixer.Sound("data/win.wav")
            if lines[1] == "green":
                sound.play()
            else:
                pygame.mixer.pause()

        elif selected_level == 3:
            data_player[1] = max(int(data_player[1]), 600 + score)
            result_text = result_font.render(
                "Поздравляем, вы прошли игру!", True, "white"
            )
            file = open("data/colors.txt")
            lines = file.read().splitlines()
            sound = pygame.mixer.Sound("data/win.wav")
            if lines[1] == "green":
                sound.play()
            else:
                pygame.mixer.pause()

    else:
        score_identifier(selected_level)

        result_text = result_font.render("Поражение!", True, "white")
        file = open("data/colors.txt")
        lines = file.read().splitlines()
        sound = pygame.mixer.Sound("data/game_over.wav")
        if lines[1] == "green":
            sound.play()
        else:
            pygame.mixer.pause()

    result_text_rect = result_text.get_rect(
        center=(SCREEN_WIDTH // 2 + 250, SCREEN_HEIGHT // 2)
    )
    score_surface = score_font.render("Итоговый Счёт: " + str(score), True, "white")

    screen.blit(result_screen, (0, 0))
    screen.blit(result_text, result_text_rect)
    screen.blit(score_surface, (SCREEN_WIDTH // 2 + 130, SCREEN_HEIGHT // 2 + 40))

    while True:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                data_player = [name_player, data_player[1], data_player[2]]
                writing_to_file(data_player)
                terminate()

            if event.type == pygame.KEYDOWN and event.key == K_ESCAPE:
                data_player = [name_player, data_player[1], data_player[2]]
                writing_to_file(data_player)
                start_screen()
                return

            if event.type == pygame.KEYDOWN and event.key == K_RETURN:
                return

        pygame.display.flip()


def read_level_from_file(file_path):
    # Чтение уровня из txt-файла
    level = []

    with open(file_path, "r") as file:
        for line in file:
            row = []
            for char in line.strip():
                row.append(char)
            level.append(row)
    return level


def detect_collision(ball_speed_x, ball_speed_y, ball, rect):
    # Определение вектора напрвления скорости мяча после столкновения его с обЪектами
    if ball_speed_x > 0:
        delta_x = ball.right - rect.left
    else:
        delta_x = rect.right - ball.left

    if ball_speed_y > 0:
        delta_y = ball.bottom - rect.top
    else:
        delta_y = rect.bottom - ball.top

    if abs(delta_x - delta_y) < 10:
        ball_speed_x, ball_speed_y = -ball_speed_x, -ball_speed_y

    elif delta_x > delta_y:
        ball_speed_y = -ball_speed_y

    elif delta_y > delta_x:
        ball_speed_x = -ball_speed_x

    return ball_speed_x, ball_speed_y


def show_blocks(level):
    # Функция, отвечающая за расстановку блоков в игре из прочитанного файла
    blocks = pygame.sprite.Group()
    no_destructive_blocks = pygame.sprite.Group()
    level_data = read_level_from_file(f"data/level_{level}.txt")

    for row in range(len(level_data)):
        for col in range(len(level_data[row])):

            block_x = BLOCK_GAP + col * (BLOCK_WIDTH + BLOCK_GAP)
            block_y = BLOCK_GAP + row * (BLOCK_HEIGHT + BLOCK_GAP)

            if level_data[row][col] == "B":
                block = Block(block_x, block_y)
                blocks.add(block)

            elif level_data[row][col] == "X":
                block = No_Destructive_Block(block_x, block_y)
                no_destructive_blocks.add(block)

    return blocks, no_destructive_blocks


def pause_game(is_pause):
    # Функция, которая ставит игру на паузу
    global memory

    if is_pause:
        memory = ball.ball_speed_y, ball.ball_speed_x, platform.platform_speed
        ball.ball_speed_y, ball.ball_speed_x, platform.platform_speed = 0, 0, 0
        pause_surface = pause_font.render("Пауза", True, "white")

        return pause_surface

    else:
        ball.ball_speed_y, ball.ball_speed_x, platform.platform_speed = memory

        return


def menu_game(is_menu):
    # Функция, которая ставит игру на паузу для открытия меню в процессе игры
    pause_game(is_menu)

    if is_menu:
        pass

    else:
        pass


def start_game():
    # Основная функция самой игры
    global is_pause, is_menu, score, data_player
    is_menu = False
    is_pause = False
    score = 0
    while True:
        if not is_pause and not is_menu:
            # Отключение курсора, если игра не стоит на паузе
            pygame.mouse.set_visible(False)
        screen.blit(fon, (0, 0))
        d = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == QUIT:

                score_identifier(selected_level)
                data_player = [name_player, data_player[1], data_player[2]]
                writing_to_file(data_player)

                terminate()

            if event.type == pygame.KEYDOWN and event.key == K_ESCAPE:
                # При нажатии на ESC игра ставится на паузу и открывается меню в игре
                if not is_pause:
                    is_menu = not (is_menu)
                    menu_surface = menu_game(is_menu)

            if event.type == pygame.KEYDOWN and event.key == K_SPACE:
                # При нажатии на Space игра ставится на паузу и наоборот
                if not is_menu:
                    is_pause = not (is_pause)
                    pause_surface = pause_game(is_pause)

            if is_menu:
                # При открытом меню можно продолжить игру или выйти из нее
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if (
                        SCREEN_WIDTH / 2 - 150 <= mouse[0] <= SCREEN_WIDTH / 2 + 100
                        and 400 <= mouse[1] <= 440
                    ):
                        is_menu = not (is_menu)
                        menu_game(is_menu)
                    elif (
                        SCREEN_WIDTH / 2 - 150 <= mouse[0] <= SCREEN_WIDTH / 2 + 100
                        and 450 <= mouse[1] <= 490
                    ):
                        score_identifier(selected_level)

                        data_player = [name_player, data_player[1], data_player[2]]
                        writing_to_file(data_player)
                        start_screen()
                        return

        if ball.rect.bottom >= SCREEN_HEIGHT:
            # Проверка на проигрыщ в игре в случае вылета мяча за нижнюю границу
            show_result_window("gameover", data_player)
            return

        if pygame.sprite.spritecollide(ball, blocks, True):
            # Счетчик очков, которые срабатывает при столкновении мяча с блоком
            score = all_score - len(blocks) * 10

        elif len(blocks) == 0:
            # Проверка на победу в игре в случае разрушения всех блоков
            data_player[2] = str(int(data_player[2]) + 1)
            show_result_window("win", data_player)
            return

        score_surface = score_font.render("Кол-во очков: " + str(score), True, "white")

        group.update()
        group.draw(screen)

        if is_pause:
            screen.blit(pause_surface, (SCREEN_WIDTH // 2 - 90, SCREEN_HEIGHT // 2))
            pygame.mouse.set_visible(True)

        if is_menu:
            mouse = pygame.mouse.get_pos()
            text_continue = smallfont.render("Продолжить", True, "white")
            text_menu = smallfont.render("Выйти в главное меню", True, "white")
            pygame.mouse.set_visible(True)

            if (
                SCREEN_WIDTH / 2 - 165 <= mouse[0] <= SCREEN_WIDTH / 2 + 115
                and 400 <= mouse[1] <= 440
            ):
                pygame.draw.rect(
                    screen, COLOR_LIGHT, [SCREEN_WIDTH / 2 - 165, 400, 280, 40]
                )
            else:
                pygame.draw.rect(
                    screen, COLOR_DARK, [SCREEN_WIDTH / 2 - 165, 400, 280, 40]
                )
            if (
                SCREEN_WIDTH / 2 - 195 <= mouse[0] <= SCREEN_WIDTH / 2 + 150
                and 450 <= mouse[1] <= 490
            ):
                pygame.draw.rect(
                    screen, COLOR_LIGHT, [SCREEN_WIDTH / 2 - 195, 450, 345, 40]
                )
            else:
                pygame.draw.rect(
                    screen, COLOR_DARK, [SCREEN_WIDTH / 2 - 195, 450, 345, 40]
                )

            screen.blit(text_continue, (SCREEN_WIDTH // 2 - 115, 405))
            screen.blit(text_menu, (SCREEN_WIDTH // 2 - 190, 455))

        screen.blit(score_surface, (10, 10))
        clock.tick(FPS)
        pygame.display.update()


fon = pygame.transform.scale(load_image("fon_screen.png"), (1580, 900))

score_font = pygame.font.SysFont("MAIN_FONT", 40)
pause_font = pygame.font.SysFont("Corbel", 60)
smallfont = pygame.font.SysFont("Corbel", 35)

# В самом начале вызывается функция для стартового экрана
start_screen()

while True:
    # Цикл, в котором инициализируются обЪекты, выбирается уровень исходя из данных игрока
    if int(data_player[2]) > 3:
        data_player[2] = 1
    selected_level = int(data_player[2])
    group = pygame.sprite.Group()
    platform = Platform()
    ball = Ball()
    blocks, no_destructive_blocks = show_blocks(selected_level)
    group.add(platform)
    group.add(ball)
    group.add(blocks)
    group.add(no_destructive_blocks)

    level_data = read_level_from_file(f"data/level_{selected_level}.txt")
    all_score = sum([x.count("B") for x in level_data]) * 10
    start_game()


pygame.quit()
