import pygame
import time

from characters import *
from globals import *


class Engine:
    def __init__(self):
        self.time_delta_in_secs = 0.0
        self.current_time_in_secs = 0.0
        self.previous_time_in_secs = 0.0

    def __enter__(self):
        pygame.init()
        pygame.freetype.init()
        pygame.mixer.init()

        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Random Dungeon")

        screen_center = pygame.Vector2(
            self.screen.get_width() / 2.0, self.screen.get_height() / 2.0
        )
        self.player = Hero(screen_center.copy())

        self.initialized = True
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pygame.quit()

    def run(self):
        if not self.initialized:
            raise RuntimeError("Engine is not initialiyzed")

        self.previous_time_in_secs = time.time()
        running = True
        while running:
            # Input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # closing window
                    running = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                self.player.position.y -= PLAYER_SPEED * self.time_delta_in_secs
            if keys[pygame.K_s]:
                self.player.position.y += PLAYER_SPEED * self.time_delta_in_secs
            if keys[pygame.K_a]:
                self.player.position.x -= PLAYER_SPEED * self.time_delta_in_secs
            if keys[pygame.K_d]:
                self.player.position.x += PLAYER_SPEED * self.time_delta_in_secs

            # Render characters
            self.screen.fill(BACKGROUND_COLOR)

            self.player.render(self.screen)

            pygame.display.flip()

            self.__update_time()

    def __update_time(self):
        self.current_time_in_secs = time.time()
        self.time_delta_in_secs = self.current_time_in_secs - self.previous_time_in_secs
        self.previous_time_in_secs = self.current_time_in_secs
