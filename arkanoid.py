import pygame
import os
import sys
from pygame.locals import *

pygame.init()
pygame.display.set_caption("Арканоид")

screen_size = screen_width, screen_height = 1580, 900
screen = pygame.display.set_mode(screen_size, pygame.SCALED | pygame.FULLSCREEN)

clock = pygame.time.Clock()
fps = 60

name_player = ""
data_player = ""


running = True
is_pause = False
is_menu = False

platform_width = 250
platform_height = 100

ball_radius = 70

block_width = 130
block_height = 80
block_gap = 26


class Platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(
            load_image("monkey.png"), (platform_width, platform_height)
        )
        self.image.set_colorkey(0)
        self.rect = self.image.get_rect()
        self.rect.x = screen_width // 2 - platform_width // 2
        self.rect.y = screen_height - platform_height
        self.platform_speed = 10

    def update(self):
        d = pygame.key.get_pressed()
        if d[K_LEFT] and self.rect.left > 0:
            self.rect.left -= self.platform_speed
        if d[K_RIGHT] and self.rect.right < screen_width:
            self.rect.right += self.platform_speed


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(
            load_image("coconut.png"), (ball_radius, ball_radius)
        )
        self.image.set_colorkey(0)
        self.rect = self.image.get_rect()
        self.rect.x = (screen_width - ball_radius) // 2
        self.rect.y = screen_height - platform_height - ball_radius * 2 - 10
        self.ball_speed_x = 6
        self.ball_speed_y = -6

    def update(self):
        if Rect(
            self.rect.x,
            self.rect.y + self.ball_speed_y,
            ball_radius,
            ball_radius,
        ).colliderect(platform):
            pygame.mixer.Sound("data/collision_1.wav").play()
            self.ball_speed_x, self.ball_speed_y = detect_collision(
                self.ball_speed_x, self.ball_speed_y, self.rect, platform.rect
            )

        self.rect.x += self.ball_speed_x
        self.rect.y += self.ball_speed_y

        if self.rect.left < 10 or self.rect.right >= screen_width:
            self.ball_speed_x *= -1
        if self.rect.top < 10:
            self.ball_speed_y *= -1
        if self.rect.colliderect(platform):
            pygame.mixer.Sound("data/collision_1.wav").play()
            self.ball_speed_x, self.ball_speed_y = detect_collision(
                self.ball_speed_x, self.ball_speed_y, self.rect, platform.rect
            )


class Block(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(
            load_image("banana.png"), (block_width, block_height)
        )
        self.image.set_colorkey(0)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        if self.rect.colliderect(ball):
            ball.ball_speed_x, ball.ball_speed_y = detect_collision(
                ball.ball_speed_x,
                ball.ball_speed_y,
                ball.rect,
                self.rect,
            )


class No_Destructive_Block(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(
            load_image("block.png"), (block_width, block_height)
        )
        self.image.set_colorkey(0)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        if self.rect.colliderect(ball):
            pygame.mixer.Sound("data/collision_1.wav").play()
            ball.ball_speed_x, ball.ball_speed_y = detect_collision(
                ball.ball_speed_x,
                ball.ball_speed_y,
                ball.rect,
                self.rect,
            )


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, color_key=None):
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
    guide_screen = pygame.display.set_mode(
        screen_size, pygame.SCALED | pygame.FULLSCREEN
    )

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

    guide_y = 120

    guide_screen.fill((207, 143, 103))
    guide_screen.blit(guide_title, (250, 50))

    for line in guide_text:
        guide_line = guide_font.render(line, True, "black")
        guide_screen.blit(guide_line, (250, guide_y))
        guide_y += 40

    while True:
        d = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or d[pygame.K_ESCAPE]:
                return

        pygame.display.flip()


# def open_settings_window():
#     pass


def registration_window():
    global name_player, data_player
    fon = pygame.transform.scale(load_image("result_window.png"), (1580, 900))
    clock = pygame.time.Clock()
    color = (255, 255, 255)
    backcolor = None
    font = pygame.font.SysFont(None, 100)
    active = False
    text = ""

    while True:
        screen.blit(fon, (0, 0))
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
                    data_player = [x for x in lines if name_player in x]
                    if data_player:
                        data_player = data_player[-1].split("\t")
                    else:
                        data_player = [name_player, "0", "1"]
                f.close()
                return

        t_surf = font.render(text, True, color, backcolor)
        image = pygame.Surface(
            (max(700, t_surf.get_width() + 10), t_surf.get_height() + 10),
            pygame.SRCALPHA,
        )
        if backcolor:
            image.fill(self.backcolor)
        image.blit(t_surf, (5, 5))
        pygame.draw.rect(image, color, image.get_rect().inflate(-2, -2), 2)
        rect = image.get_rect(topleft=(700, 450))
        screen.blit(image, (700, 450))

        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and not active:
                active = rect.collidepoint(event.pos)
            if event.type == pygame.KEYDOWN and active:
                if event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode

<<<<<<< HEAD
=======
        pygame.display.flip()


>>>>>>> 5981425 (Edit presentation, add datebase and sound)
def open_rating_window():
    fon = pygame.transform.scale(load_image("result_window.png"), (1580, 900))

    smallfont = pygame.font.SysFont("Corbel", 35)
    color_dark = (100, 100, 100)

    text_name = smallfont.render("Игрок", True, "white")
    text_score = smallfont.render("Очки", True, "white")
    text_level = smallfont.render("Уровень", True, "white")

    while True:
        screen.blit(fon, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN and event.key == K_ESCAPE:
<<<<<<< HEAD
                start_screen()
=======
                return
>>>>>>> 5981425 (Edit presentation, add datebase and sound)

        pygame.draw.rect(screen, color_dark, [600, 100, 250, 40])
        pygame.draw.rect(screen, color_dark, [900, 100, 250, 40])
        pygame.draw.rect(screen, color_dark, [1200, 100, 250, 40])

        screen.blit(text_name, (680, 103))
        screen.blit(text_score, (985, 103))
        screen.blit(text_level, (1265, 103))

        pygame.display.flip()
<<<<<<< HEAD
=======

>>>>>>> 5981425 (Edit presentation, add datebase and sound)

def start_screen():
    pygame.mouse.set_visible(True)
    fon = pygame.transform.scale(load_image("start_window.png"), (1580, 900))

    smallfont = pygame.font.SysFont("Corbel", 35)
    cup_image = load_image("cup.png")
    color_light = (170, 170, 170)
    color_dark = (100, 100, 100)

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
                    screen_width / 2 - 150 <= mouse[0] <= screen_width / 2 + 100
                    and 550 <= mouse[1] <= 590
                ):
                    registration_window()
                    return
                elif (
                    screen_width / 2 - 150 <= mouse[0] <= screen_width / 2 + 100
                    and 600 <= mouse[1] <= 640
                ):
                    pass
                    # open_settings_window()
                elif (
                    screen_width / 2 - 150 <= mouse[0] <= screen_width / 2 + 100
                    and 650 <= mouse[1] <= 690
                ):
                    open_guide_window()
                elif (
                    screen_width / 2 - 150 <= mouse[0] <= screen_width / 2 + 100
                    and 700 <= mouse[1] <= 740
                ):
                    terminate()
                elif (
                    30 <= mouse[0] <= 90
                    and screen_height - 90 <= mouse[1] <= screen_height - 30
                ):
                    open_rating_window()
<<<<<<< HEAD
                    # pass
=======
>>>>>>> 5981425 (Edit presentation, add datebase and sound)

        mouse = pygame.mouse.get_pos()

        if (
            30 <= mouse[0] <= 90
            and screen_height - 90 <= mouse[1] <= screen_height - 30
        ):
            pygame.draw.rect(screen, color_light, [30, screen_height - 90, 60, 60])
        else:
            pygame.draw.rect(screen, color_dark, [30, screen_height - 90, 60, 60])

        if (
            screen_width / 2 - 150 <= mouse[0] <= screen_width / 2 + 100
            and 550 <= mouse[1] <= 590
        ):
            pygame.draw.rect(
                screen, color_light, [screen_width / 2 - 150, 550, 250, 40]
            )
        else:
            pygame.draw.rect(screen, color_dark, [screen_width / 2 - 150, 550, 250, 40])

        if (
            screen_width / 2 - 150 <= mouse[0] <= screen_width / 2 + 100
            and 600 <= mouse[1] <= 640
        ):
            pygame.draw.rect(
                screen, color_light, [screen_width / 2 - 150, 600, 250, 40]
            )
        else:
            pygame.draw.rect(screen, color_dark, [screen_width / 2 - 150, 600, 250, 40])

        if (
            screen_width / 2 - 150 <= mouse[0] <= screen_width / 2 + 100
            and 650 <= mouse[1] <= 690
        ):
            pygame.draw.rect(
                screen, color_light, [screen_width / 2 - 150, 650, 250, 40]
            )
        else:
            pygame.draw.rect(screen, color_dark, [screen_width / 2 - 150, 650, 250, 40])

        if (
            screen_width / 2 - 150 <= mouse[0] <= screen_width / 2 + 100
            and 700 <= mouse[1] <= 740
        ):
            pygame.draw.rect(
                screen, color_light, [screen_width / 2 - 150, 700, 250, 40]
            )
        else:
            pygame.draw.rect(screen, color_dark, [screen_width / 2 - 150, 700, 250, 40])

        screen.blit(text_play, (screen_width / 2 - 80, 555))
        screen.blit(text_settings, (screen_width / 2 - 105, 605))
        screen.blit(text_guide, (screen_width / 2 - 90, 655))
        screen.blit(text_quit, (screen_width / 2 - 75, 705))
        screen.blit(cup_image, [30, screen_height - 90, 60, 60])

        pygame.display.flip()


def show_result_window(result):
    global selected_level, score
    result_screen = pygame.transform.scale(load_image("result_window.png"), (1580, 900))

    result_font = pygame.font.SysFont("MAIN_FONT", 80)
    if result == "win":
        result_text = result_font.render("Победа!", True, "white")
        selected_level += 1

    else:
        result_text = result_font.render("Поражение!", True, "white")

    result_text_rect = result_text.get_rect(
        center=(screen_width // 2 + 250, screen_height // 2)
    )
    score_surface = score_font.render("Итоговый Счёт: " + str(score), True, "white")
    screen.blit(result_screen, (0, 0))
    screen.blit(result_text, result_text_rect)
    screen.blit(score_surface, (screen_width // 2 + 130, screen_height // 2 + 40))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN and event.key == K_ESCAPE:
                start_screen()
                return
            if event.type == pygame.KEYDOWN and event.key == K_RETURN:
                return

        pygame.display.flip()


def read_level_from_file(file_path):
    level = []

    with open(file_path, "r") as file:
        for line in file:
            row = []
            for char in line.strip():
                row.append(char)
            level.append(row)
    return level


def detect_collision(ball_speed_x, ball_speed_y, ball, rect):
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
    blocks = pygame.sprite.Group()
    no_destructive_blocks = pygame.sprite.Group()
    level_data = read_level_from_file(f"data/level_{level}.txt")
    for row in range(len(level_data)):
        for col in range(len(level_data[row])):
            if level_data[row][col] == "B":
                block_x = block_gap + col * (block_width + block_gap)
                block_y = block_gap + row * (block_height + block_gap)
                block = Block(block_x, block_y)
                blocks.add(block)
            elif level_data[row][col] == "X":
                block_x = block_gap + col * (block_width + block_gap)
                block_y = block_gap + row * (block_height + block_gap)
                block = No_Destructive_Block(block_x, block_y)
                no_destructive_blocks.add(block)
    return blocks, no_destructive_blocks


def pause_game(is_pause):
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
    pause_game(is_menu)
    if is_menu:
        pass
    else:
        pass


fon = pygame.transform.scale(load_image("fon_screen.png"), (1580, 900))
score = 0
score_font = pygame.font.SysFont("MAIN_FONT", 40)
pause_font = pygame.font.SysFont("Corbel", 60)
smallfont = pygame.font.SysFont("Corbel", 35)
color_light = (170, 170, 170)
color_dark = (100, 100, 100)


def start_game():
    global is_pause, is_menu, score
    all_score_player = data_player[1]
    score = 0
    while True:
        if not is_pause and not is_menu:
            pygame.mouse.set_visible(False)
        screen.blit(fon, (0, 0))
        d = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == QUIT:
                if selected_level != 1 and int(all_score_player) + int(score) > int(
                    data_player[1]
                ):
                    data_player[1] = str(int(score) + int(all_score_player))

                elif selected_level == 1 and int(score) > int(data_player[1]):
                    data_player[1] = score
                f = open("data/data_players.txt", "a")
                f.write("\n")
                f.write("\t".join(map(str, data_player)))
                terminate()

            if d[pygame.K_ESCAPE]:
                if not is_pause:
                    is_menu = not (is_menu)
                    menu_surface = menu_game(is_menu)

            if d[K_SPACE]:
                if not is_menu:
                    is_pause = not (is_pause)
                    pause_surface = pause_game(is_pause)

            if is_menu:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if (
                        screen_width / 2 - 150 <= mouse[0] <= screen_width / 2 + 100
                        and 400 <= mouse[1] <= 440
                    ):
                        is_menu = not (is_menu)
                        menu_game(is_menu)
                    elif (
                        screen_width / 2 - 150 <= mouse[0] <= screen_width / 2 + 100
                        and 450 <= mouse[1] <= 490
                    ):
                        if selected_level != 1 and int(all_score_player) + int(
                            score
                        ) > int(data_player[1]):
                            data_player[1] = str(int(score) + int(all_score_player))

                        elif selected_level == 1 and int(score) > int(data_player[1]):
                            data_player[1] = score
                        f = open("data/data_players.txt", "a")
                        f.write("\n")
                        f.write("\t".join(map(str, data_player)))
                        start_screen()
                        return

        if ball.rect.bottom >= screen_height:
            if selected_level != 1 and int(all_score_player) + int(score) > int(
                data_player[1]
            ):
                data_player[1] = str(int(score) + int(all_score_player))

            elif selected_level == 1 and int(score) > int(data_player[1]):
                data_player[1] = score
            f = open("data/data_players.txt", "a")
            f.write("\n")
            f.write("\t".join(map(str, data_player)))

            show_result_window("gameover")
            return

        if pygame.sprite.spritecollide(ball, blocks, True):
            score = all_score - len(blocks) * 10

        elif len(blocks) == 0:
            data_player[1] = (
                str(int(score) + int(all_score_player))
                if selected_level != 1
                else score
            )
            data_player[2] = data_player[2] + 1
            f = open("data/data_players.txt", "a")
            f.write("\n")
            f.write("\t".join(map(str, data_player)))
            show_result_window("win")
            return

        score_surface = score_font.render("Кол-во очков: " + str(score), True, "white")

        group.update()
        group.draw(screen)

        if is_pause:
            screen.blit(pause_surface, (screen_width // 2 - 90, screen_height // 2))
            pygame.mouse.set_visible(True)

        if is_menu:
            mouse = pygame.mouse.get_pos()
            text_continue = smallfont.render("Продолжить", True, "white")
            text_menu = smallfont.render("Выйти в главное меню", True, "white")
            pygame.mouse.set_visible(True)

            if (
                screen_width / 2 - 165 <= mouse[0] <= screen_width / 2 + 115
                and 400 <= mouse[1] <= 440
            ):
                pygame.draw.rect(
                    screen, color_light, [screen_width / 2 - 165, 400, 280, 40]
                )
            else:
                pygame.draw.rect(
                    screen, color_dark, [screen_width / 2 - 165, 400, 280, 40]
                )
            if (
                screen_width / 2 - 195 <= mouse[0] <= screen_width / 2 + 150
                and 450 <= mouse[1] <= 490
            ):
                pygame.draw.rect(
                    screen, color_light, [screen_width / 2 - 195, 450, 345, 40]
                )
            else:
                pygame.draw.rect(
                    screen, color_dark, [screen_width / 2 - 195, 450, 345, 40]
                )

            screen.blit(text_continue, (screen_width // 2 - 115, 405))
            screen.blit(text_menu, (screen_width // 2 - 190, 455))

        screen.blit(score_surface, (10, 10))
        clock.tick(fps)
        pygame.display.update()


start_screen()

while True:
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
