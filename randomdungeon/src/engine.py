import pygame
import time

from characters import *
from globals import *
from rooms import *


class Engine:
    def __init__(self):
        self.time_delta_in_secs = 0.0
        self.current_time_in_secs = 0.0
        self.previous_time_in_secs = 0.0
        self.running = False

    def __enter__(self):
        pygame.init()
        pygame.freetype.init()
        pygame.mixer.init()

        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Random Dungeon")

        screen_center = pygame.Vector2(
            self.screen.get_width() / 2.0, self.screen.get_height() / 2.0
        )

        self.hero = Hero()
        self.hero.position = screen_center.copy()
        self.room = Room()

        self.initialized = True
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pygame.quit()

    def run(self):
        if not self.initialized:
            raise RuntimeError("Engine not initialized")

        self.previous_time_in_secs = time.time()
        self.running = True
        while self.running:
            self.__read_input()
            self.__render()
            self.__update_time()

    def __read_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # closing window
                self.running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.hero.position.y -= HERO_SPEED * self.time_delta_in_secs
        if keys[pygame.K_s]:
            self.hero.position.y += HERO_SPEED * self.time_delta_in_secs
        if keys[pygame.K_a]:
            self.hero.position.x -= HERO_SPEED * self.time_delta_in_secs
        if keys[pygame.K_d]:
            self.hero.position.x += HERO_SPEED * self.time_delta_in_secs

    def __render(self):
        self.screen.fill(BACKGROUND_COLOR)
        self.room.render(self.screen)
        self.hero.render(self.screen)

        pygame.display.flip()

    def __update_time(self):
        self.current_time_in_secs = time.time()
        self.time_delta_in_secs = self.current_time_in_secs - self.previous_time_in_secs
        self.previous_time_in_secs = self.current_time_in_secs
