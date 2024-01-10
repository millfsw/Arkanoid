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

running = True
is_pause = False
is_menu = False

platform_width = 250
platform_height = 100

ball_radius = 70

block_width = 130
block_height = 80
block_gap = 10
block_rows = 4
block_cols = (screen_width - block_gap) // (block_width + block_gap)


class Platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(
            load_image("monkey.png"), (platform_width, platform_height)
        )
        self.image.set_colorkey(0)
        self.rect = self.image.get_rect()
        self.rect.x = screen_width // 2 - platform_width // 2 + 10
        self.rect.y = screen_height - platform_height - 10
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
        self.rect.x += self.ball_speed_x
        self.rect.y += self.ball_speed_y

        if self.rect.left < 10 or self.rect.right >= screen_width:
            self.ball_speed_x *= -1
        if self.rect.top < 10:
            self.ball_speed_y *= -1
        if self.rect.colliderect(platform):
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
        "  - Разрушить все бананы на уровне, отбивая кокос с помощью обезьянки.",
        "",
        "Управление:",
        "  - Используйте стрелки для управления обезьянкой",
        "  - Нажмите ESC для выхода из игры",
        "  - Нажмите Space, чтобы поставить паузу в игре или снять игру с паузы",
        "",
        "Геймплей:",
        "  - Кокос отскакивает от обезьянки, бананов и дощечек",
        "  - Разбейте все бананы для того, чтобы пройти на следующий уровень.",
        "  - Если кокос уйдет за нижнию границу экрана, игра будет окончено",
        "  - Накапливайте очки за каждый банан",
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


def start_screen():
    fon = pygame.transform.scale(load_image("start_window.png"), (1580, 900))

    smallfont = pygame.font.SysFont("Corbel", 35)
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

        mouse = pygame.mouse.get_pos()

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

        pygame.display.flip()


def show_result_window(result):
    result_screen = pygame.transform.scale(load_image("result_window.png"), (1580, 900))

    result_font = pygame.font.SysFont("Corbel", 80)
    if result == "win":
        result_text = result_font.render("Победа!", True, "white")
    else:
        result_text = result_font.render("Game Over", True, "white")

    result_text_rect = result_text.get_rect(
        center=(screen_width // 2 + 250, screen_height // 2)
    )
    score_surface = score_font.render("Score: " + str(score), True, "white")
    screen.blit(result_screen, (0, 0))
    screen.blit(result_text, result_text_rect)
    screen.blit(score_surface, (screen_width // 2 + 160, screen_height // 2 + 40))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
                terminate()

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


def build_level(level_data):
    max_count = len(max(level_data, key=lambda x: len(x)))


level_data_1 = read_level_from_file("level_1.txt")
build_level(level_data_1)
# level_data_2 = read_level_from_file("level_2.txt")
# level_data_3 = read_level_from_file("level_3.txt")


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


def show_blocks():
    blocks = pygame.sprite.Group()
    for row in range(block_rows):
        for col in range(block_cols):
            block_x = block_gap + col * (block_width + block_gap)
            block_y = block_gap + row * (block_height + block_gap)
            block = Block(block_x, block_y)
            blocks.add(block)
    return blocks


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
score_font = pygame.font.SysFont("Corbel", 40)
pause_font = pygame.font.SysFont("Corbel", 60)
smallfont = pygame.font.SysFont("Corbel", 35)
color_light = (170, 170, 170)
color_dark = (100, 100, 100)


group = pygame.sprite.Group()
platform = Platform()
ball = Ball()
blocks = show_blocks()
group.add(platform)
group.add(ball)
group.add(blocks)

start_screen()
while running:
    screen.blit(fon, (0, 0))
    d = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

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
                    start_screen()

    if ball.rect.bottom >= screen_height:
        show_result_window("gameover")
        running = False

    if pygame.sprite.spritecollide(ball, blocks, True):
        ball.ball_speed_y *= -1
        score += 10

    elif len(blocks) == 0:
        show_result_window("win")
        running = False

    score_surface = score_font.render("Score: " + str(score), True, "white")

    group.update()
    group.draw(screen)
    if is_pause:
        screen.blit(pause_surface, (screen_width // 2 - 90, screen_height // 2))

    if is_menu:
        mouse = pygame.mouse.get_pos()
        text_continue = smallfont.render("Продолжить", True, "white")
        text_menu = smallfont.render("Выйти в главное меню", True, "white")

        if (
            screen_width / 2 - 165 <= mouse[0] <= screen_width / 2 + 115
            and 400 <= mouse[1] <= 440
        ):
            pygame.draw.rect(
                screen, color_light, [screen_width / 2 - 165, 400, 280, 40]
            )
        else:
            pygame.draw.rect(screen, color_dark, [screen_width / 2 - 165, 400, 280, 40])
        if (
            screen_width / 2 - 195 <= mouse[0] <= screen_width / 2 + 150
            and 450 <= mouse[1] <= 490
        ):
            pygame.draw.rect(
                screen, color_light, [screen_width / 2 - 195, 450, 345, 40]
            )
        else:
            pygame.draw.rect(screen, color_dark, [screen_width / 2 - 195, 450, 345, 40])

        screen.blit(text_continue, (screen_width // 2 - 115, 405))
        screen.blit(text_menu, (screen_width // 2 - 190, 455))

    screen.blit(score_surface, (10, 10))
    clock.tick(fps)
    pygame.display.update()

pygame.quit()
