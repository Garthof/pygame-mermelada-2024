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
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Random Dungeon")

        tile_width = TILE_RADIUS * 2
        tile_height = TILE_RADIUS * 2
        screen_width_in_tiles = WINDOW_WIDTH // tile_width
        screen_height_in_tiles = WINDOW_HEIGHT // tile_height

        self.hero = Hero()
        self.hero.current_tile_idx = pygame.Vector2(
            screen_width_in_tiles // 2, screen_height_in_tiles // 2
        )
        self.hero.next_tile_idx = self.hero.current_tile_idx
        self.hero.position = tile_center(self.hero.current_tile_idx)

        self.mouse_tile_cursor = TileCursor()
        self.mouse_tile_cursor.color = "white"
        self.mouse_tile_cursor.thickness = 5

        self.room = Room()

        self.background_music = pygame.mixer.Sound(MUSIC_PATH / "dungeon-maze.mp3")

        self.initialized = True
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pygame.freetype.quit()
        pygame.mixer.quit()
        pygame.quit()

    def run(self):
        if not self.initialized:
            raise RuntimeError("Engine not initialized")

        self.background_music.play(-1, 0, 5000)
        self.background_music.set_volume(0.5)

        self.previous_time_in_secs = time.time()
        self.running = True
        while self.running:
            self.__read_input()
            self.__animate()
            self.__render()
            self.__update_time()
            self.clock.tick(FPS)

    def __read_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # closing window
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pressed_buttons = pygame.mouse.get_pressed()
                if pressed_buttons[0]:
                    pressed_tile = tile_idx(pygame.mouse.get_pos())
                    if is_valid_tile(pressed_tile):
                        self.hero.target_tile_idx = pressed_tile

        pressed_tile = pygame.mouse.get_pos()
        self.mouse_tile_cursor.position = pygame.Vector2(pressed_tile)

    def __animate(self):
        self.hero.animate(self.time_delta_in_secs)
        self.mouse_tile_cursor.animate()

    def __render(self):
        self.screen.fill(BACKGROUND_COLOR)
        self.room.render()
        self.hero.render()
        self.mouse_tile_cursor.render()

        debug(f"FPS: {round(self.clock.get_fps(), 1)}")

        pygame.display.flip()

    def __update_time(self):
        self.current_time_in_secs = time.time()
        self.time_delta_in_secs = self.current_time_in_secs - self.previous_time_in_secs
        self.previous_time_in_secs = self.current_time_in_secs
