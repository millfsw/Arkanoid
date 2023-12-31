import pygame
import os
import sys
from pygame.locals import *


# coconut = pygame.image.load("coconut.png").convert_alpha()
# monkey = pygame.image.load("monkey.png").convert_alpha()


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
        "  - Разрушить все дощечки на уровне, отбивая кокос с помощью обезьянки.",
        "",
        "Управление:",
        "  - Используйте стрелки для управления обезьянкой",
        "  - Нажмите ESC для выхода из игры",
        "  - Нажмите Space, чтобы поставить паузу в игре или снять игру с паузы",
        "",
        "Геймплей:",
        "  - Кокос отскакивает от обезьянки и дощечек",
        "  - Разбейте все дощечки для того, чтобы пройти на следующий уровень.",
        "  - Если кокос уйдет за нижнию границу экрана, игра будет окончено",
        "  - Накапливайте очки за каждую сломанную дощечку",
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
#     settings_screen = pygame.display.set_mode(
#         screen_size, pygame.SCALED | pygame.FULLSCREEN
#     )

#     settings_font = pygame.font.SysFont("Corbel", 35)
#     settings_title = settings_font.render("Настройки игры 'Арканоид'", True, "black")
#     settings_text = [
#         "Звук: Вкл",
#         "Музыка: Вкл",
#         "Полноэкранный режим: Вкл",
#     ]

#     settings_y = 120

#     settings_screen.fill((207, 143, 103))

#     settings_screen.blit(settings_title, (200, 50))

#     for line in settings_text:
#         settings_line = settings_font.render(line, True, "black")
#         settings_screen.blit(settings_line, (250, settings_y))
#         settings_y += 50

#     while True:
#         d = pygame.key.get_pressed()
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT or d[pygame.K_ESCAPE]:
#                 return
#         pygame.display.flip()


def start_screen():
    fon = pygame.transform.scale(load_image("start_window.png"), (1580, 900))
    screen.blit(fon, (0, 0))

    smallfont = pygame.font.SysFont("Corbel", 35)
    color_light = (170, 170, 170)
    color_dark = (100, 100, 100)

    text_play = smallfont.render("Играть", True, "white")
    text_quit = smallfont.render("Выйти", True, "white")
    text_settings = smallfont.render("Настройки", True, "white")
    text_guide = smallfont.render("Справка", True, "white")

    while True:
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
    result_screen = pygame.display.set_mode(
        screen_size, pygame.SCALED | pygame.FULLSCREEN
    )
    result_screen.fill((0, 0, 0))

    result_font = pygame.font.SysFont("Corbel", 60)
    if result == "win":
        result_text = result_font.render("Победа!", True, "white")
    else:
        result_text = result_font.render("Game Over", True, "white")

    result_text_rect = result_text.get_rect(
        center=(screen_width // 2, screen_height // 2)
    )
    score_surface = score_font.render("Score: " + str(score), True, "white")
    result_screen.blit(result_text, result_text_rect)
    result_screen.blit(score_surface, (screen_width // 2 - 50, screen_height // 2 + 40))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
                terminate()

        pygame.display.flip()


pygame.init()
pygame.display.set_caption("Арканоид")
screen_size = screen_width, screen_height = 1580, 900
screen = pygame.display.set_mode(screen_size, pygame.SCALED | pygame.FULLSCREEN)

running = True
pause = False
clock = pygame.time.Clock()
fps = 60

platform_width = 100
platform_height = 10
platform_x = screen_width // 2 - platform_width // 2
platform_y = screen_height - platform_height - 10
platform = pygame.Rect(platform_x, platform_y, platform_width, platform_height)

ball_radius = 10
ball_x = screen_width // 2
ball_y = platform_y - ball_radius - 1
ball = pygame.Rect(ball_x, ball_y, ball_radius, ball_radius)

ball_speed_x = 6
ball_speed_y = -6
platform_speed = 10

brick_width = 130
brick_height = 30
brick_gap = 10
brick_rows = 5
brick_cols = (screen_width - brick_gap) // (brick_width + brick_gap)
bricks = []
for row in range(brick_rows):
    for col in range(brick_cols):
        brick_x = brick_gap + col * (brick_width + brick_gap)
        brick_y = brick_gap + row * (brick_height + brick_gap)
        brick = pygame.Rect(brick_x, brick_y, brick_width, brick_height)
        bricks.append(brick)

fon = pygame.transform.scale(load_image("fon_screen.png"), (1580, 900))
score = 0
score_font = pygame.font.SysFont("Corbel", 30)
pause_font = pygame.font.SysFont("Corbel", 60)

start_screen()
while running:
    screen.blit(fon, (0, 0))
    # screen.fill("black")
    pygame.draw.rect(screen, "blue", platform)
    pygame.draw.circle(screen, "red", (ball.x, ball.y), ball_radius)

    for brick in bricks:
        pygame.draw.rect(screen, "brown", brick)

    d = pygame.key.get_pressed()

    for event in pygame.event.get():

        if d[pygame.K_ESCAPE] or event.type == QUIT:
            running = False
        if d[K_SPACE]:
            if not pause:
                memory = ball_speed_y, ball_speed_x, platform_speed
                ball_speed_y = 0
                ball_speed_x = 0
                platform_speed = 0
                pause = True
                pause_surface = pause_font.render("Пауза", True, "white")
            else:
                ball_speed_y, ball_speed_x, platform_speed = memory
                pause = False

    if d[K_LEFT] and platform.left > 0:
        platform.left -= platform_speed
    if d[K_RIGHT] and platform.right < screen_width:
        platform.right += platform_speed

    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.left < 10 or ball.right >= screen_width:
        ball_speed_x *= -1
    if ball.top < 10 or ball.colliderect(platform):
        ball_speed_y *= -1

    for brick in bricks:
        if ball.colliderect(brick):
            bricks.remove(brick)
            ball_speed_y *= -1
            score += 10
            break

    if ball.bottom >= screen_height:
        show_result_window("gameover")
        running = False

    elif len(bricks) == 0:
        show_result_window("win")
        running = False

    score_surface = score_font.render("Score: " + str(score), True, "white")
    screen.blit(score_surface, (10, 10))
    if pause:
        screen.blit(pause_surface, (screen_width // 2 - 90, screen_height // 2))

    clock.tick(fps)
    pygame.display.flip()

pygame.quit()
