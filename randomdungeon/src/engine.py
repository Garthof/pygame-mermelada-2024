import pygame
import time

from characters import *
from globals import *
from rooms import *
from utils import *


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

        tile_width = TILE_RADIUS * 2
        tile_height = TILE_RADIUS * 2
        screen_width_in_tiles = WINDOW_WIDTH // tile_width
        screen_height_in_tiles = WINDOW_HEIGHT // tile_height

        self.hero = Hero()
        self.hero.current_tile = pygame.Vector2(
            screen_width_in_tiles // 2, screen_height_in_tiles // 2
        )
        self.hero.position = tile_position(self.hero.current_tile)

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
            self.__animate()
            self.__render()
            self.__update_time()

    def __read_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # closing window
                self.running = False

        hero_target_tile_delta = pygame.Vector2(0.0, 0.0)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            hero_target_tile_delta.y = -1.0
        if keys[pygame.K_s]:
            hero_target_tile_delta.y = +1.0
        if keys[pygame.K_a]:
            hero_target_tile_delta.x = -1.0
        if keys[pygame.K_d]:
            hero_target_tile_delta.x = +1.0
        if not self.hero.is_walking:
            self.hero.target_tile = self.hero.current_tile + hero_target_tile_delta

    def __animate(self):
        self.hero.animate(self.time_delta_in_secs)

    def __render(self):
        self.screen.fill(BACKGROUND_COLOR)
        self.room.render(self.screen)
        self.hero.render(self.screen)

        pygame.display.flip()

    def __update_time(self):
        self.current_time_in_secs = time.time()
        self.time_delta_in_secs = self.current_time_in_secs - self.previous_time_in_secs
        self.previous_time_in_secs = self.current_time_in_secs
