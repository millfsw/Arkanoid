import pygame
import os
import sys
from pygame.locals import *

pygame.init()
pygame.display.set_caption("Арканоид")
screen_size = screen_width, screen_height = 1580, 900
screen = pygame.display.set_mode(screen_size, pygame.SCALED | pygame.FULLSCREEN)

running = True
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

brick_width = 55
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


def start_screen():
    fon = pygame.transform.scale(load_image("start_window.png"), (1580, 900))
    screen.blit(fon, (0, 0))

    width = screen.get_width()
    height = screen.get_height()

    smallfont = pygame.font.SysFont("Corbel", 35)
    color_light = (170, 170, 170)
    color_dark = (100, 100, 100)

    text_play = smallfont.render("play", True, "white")
    text_quit = smallfont.render("quit", True, "white")
    text_settings = smallfont.render("settings", True, "white")
    text_guide = smallfont.render("guide", True, "white")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if width / 2 - 140 <= mouse[0] <= width / 2 and 250 <= mouse[1] <= 290:
                    return
                elif (
                    width / 2 - 140 <= mouse[0] <= width / 2 and 300 <= mouse[1] <= 340
                ):
                    pass
                elif (
                    width / 2 - 140 <= mouse[0] <= width / 2 and 350 <= mouse[1] <= 390
                ):
                    pass
                elif (
                    width / 2 - 140 <= mouse[0] <= width / 2 and 400 <= mouse[1] <= 440
                ):
                    terminate()

        mouse = pygame.mouse.get_pos()

        if width / 2 - 140 <= mouse[0] <= width / 2 and 250 <= mouse[1] <= 290:
            pygame.draw.rect(screen, color_light, [width / 2 - 140, 250, 140, 40])
        else:
            pygame.draw.rect(screen, color_dark, [width / 2 - 140, 250, 140, 40])

        if width / 2 - 140 <= mouse[0] <= width / 2 and 300 <= mouse[1] <= 340:
            pygame.draw.rect(screen, color_light, [width / 2 - 140, 300, 140, 40])
        else:
            pygame.draw.rect(screen, color_dark, [width / 2 - 140, 300, 140, 40])

        if width / 2 - 140 <= mouse[0] <= width / 2 and 350 <= mouse[1] <= 390:
            pygame.draw.rect(screen, color_light, [width / 2 - 140, 350, 140, 40])
        else:
            pygame.draw.rect(screen, color_dark, [width / 2 - 140, 350, 140, 40])

        if width / 2 - 140 <= mouse[0] <= width / 2 and 400 <= mouse[1] <= 440:
            pygame.draw.rect(screen, color_light, [width / 2 - 140, 400, 140, 40])
        else:
            pygame.draw.rect(screen, color_dark, [width / 2 - 140, 400, 140, 40])

        screen.blit(text_play, (width / 2 - 100, 250))
        screen.blit(text_settings, (width / 2 - 125, 300))
        screen.blit(text_guide, (width / 2 - 110, 350))
        screen.blit(text_quit, (width / 2 - 100, 400))

        pygame.display.flip()


start_screen()

while running:
    screen.fill("black")
    pygame.draw.rect(screen, "blue", platform)
    pygame.draw.circle(screen, "red", (ball.x, ball.y), ball_radius)

    for brick in bricks:
        pygame.draw.rect(screen, "white", brick)

    d = pygame.key.get_pressed()

    for event in pygame.event.get():

        if d[pygame.K_ESCAPE] or event.type == QUIT:
            running = False

    if d[K_LEFT] and platform.left > 0:
        platform.left -= 10
    if d[K_RIGHT] and platform.right < screen_width:
        platform.right += 10

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
            break

    if ball.bottom >= screen_height or len(bricks) == 0:
        running = False

    clock.tick(fps)
    pygame.display.flip()

pygame.quit()
