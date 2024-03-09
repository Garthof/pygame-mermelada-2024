import pygame
import time

from characters import *
from globals import *


pygame.init()
pygame.freetype.init()
pygame.mixer.init()

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Random Dungeon")
clock = pygame.time.Clock()

screen_center = pygame.Vector2(screen.get_width() / 2.0, screen.get_height() / 2.0)
player = Hero(screen_center.copy())

time_delta_in_secs = 0.0
tower_timer_in_secs = 0.0
enemy_timer_in_secs = 0.0

previous_time_in_secs = time.time()
running = True
while running:
    # Input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # closing window
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player.position.y -= PLAYER_SPEED * time_delta_in_secs
    if keys[pygame.K_s]:
        player.position.y += PLAYER_SPEED * time_delta_in_secs
    if keys[pygame.K_a]:
        player.position.x -= PLAYER_SPEED * time_delta_in_secs
    if keys[pygame.K_d]:
        player.position.x += PLAYER_SPEED * time_delta_in_secs

    # Render characters
    screen.fill(BACKGROUND_COLOR)

    player.render(screen)

    pygame.display.flip()

    current_time_in_secs = time.time()
    time_delta_in_secs = current_time_in_secs - previous_time_in_secs
    previous_time_in_secs = current_time_in_secs

pygame.quit()
