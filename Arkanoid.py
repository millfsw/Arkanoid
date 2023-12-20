import pygame
from pygame.locals import *

pygame.init()
pygame.display.set_caption("Арканоид")
screen_size = screen_width, screen_height = 800, 600
screen = pygame.display.set_mode(screen_size)

running = True
clock = pygame.time.Clock()
fps = 60

platform_width = 100
platform_height = 10

ball_radius = 10

platform_x = screen_width // 2 - platform_width // 2
platform_y = screen_height - platform_height - 10
platform = pygame.Rect(platform_x, platform_y, platform_width, platform_height)

ball_x = screen_width // 2
ball_y = platform_y - ball_radius - 1
ball = pygame.Rect(ball_x, ball_y, ball_radius, ball_radius)
ball_speed_x = 3
ball_speed_y = -3

coconut = pygame.image.load("coconut.png").convert_alpha()
monkey = pygame.image.load("monkey.png").convert_alpha()

while running:
    screen.fill("white")
    pygame.draw.rect(screen, (0, 0, 0), platform)
    pygame.draw.circle(screen, (0, 0, 0), (ball.x, ball.y), ball_radius)

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    d = pygame.key.get_pressed()
    if d[K_LEFT] and platform.left > 0:
        platform.x -= 5
    if d[K_RIGHT] and platform.right < screen_width:
        platform.x += 5

    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.left < 10 or ball.right > screen_width:
        ball_speed_x *= -1
    if ball.top < 10 or ball.colliderect(platform):
        ball_speed_y *= -1

    clock.tick(fps)
    pygame.display.flip()

pygame.quit()
