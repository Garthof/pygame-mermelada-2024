import pygame
import random
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

        self.hero = Character(HERO_TILE_FILE_IDX)
        self.hero.current_tile_idx = pygame.Vector2(
            window_size_in_tiles()[0] // 2, window_size_in_tiles()[1] // 2
        )
        self.hero.next_tile_idx = self.hero.current_tile_idx
        self.hero.position = tile_center(self.hero.current_tile_idx)
        self.hero_enemy_target = None

        self.enemy = Character("0110")
        self.enemy.current_tile_idx = pygame.Vector2(12, 3)
        self.enemy.next_tile_idx = self.enemy.current_tile_idx
        self.enemy.position = tile_center(self.enemy.current_tile_idx)

        self.enemies = [self.enemy]

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

        self.enemy_walk_event = pygame.USEREVENT
        pygame.time.set_timer(self.enemy_walk_event, 2500)

        self.previous_time_in_secs = time.time()
        self.running = True
        while self.running:
            self.__read_events()
            self.__update()
            self.__animate()
            self.__render()
            self.__update_time()
            self.clock.tick(FPS)

    def __read_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # closing window
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pressed_buttons = pygame.mouse.get_pressed()
                if pressed_buttons[0]:
                    pressed_tile = tile_idx(pygame.mouse.get_pos())
                    if is_valid_tile(pressed_tile):
                        self.hero_enemy_target = None
                        self.hero.target_tile_idx = pressed_tile
                        for enemy in self.enemies:
                            if are_same_tile(enemy.current_tile_idx, pressed_tile):
                                self.hero_enemy_target = enemy

            if event.type == self.enemy_walk_event:
                self.enemy.target_tile_idx = (
                    self.enemy.current_tile_idx
                    + pygame.Vector2(random.randint(-5, 5), 0)
                )

        pressed_tile = pygame.mouse.get_pos()
        self.mouse_tile_cursor.position = pygame.Vector2(pressed_tile)

    def __update(self):
        if self.hero_enemy_target:
            self.hero.target_tile_idx = self.enemy.current_tile_idx

    def __animate(self):
        self.hero.animate(self.time_delta_in_secs)
        self.enemy.animate(self.time_delta_in_secs)
        self.mouse_tile_cursor.animate()

    def __render(self):
        self.screen.fill(BACKGROUND_COLOR)
        self.room.render()
        for enemy in self.enemies:
            enemy.render()
        self.hero.render()
        self.mouse_tile_cursor.render()

        if DEBUG_RENDER_STATS:
            self.__render_stats()

        pygame.display.flip()

    def __render_stats(self):
        x_pos, y_pos = 10, 10
        debug(f"FPS: {round(self.clock.get_fps(), 1)}", (x_pos, y_pos))
        debug(f"Mouse: {self.mouse_tile_cursor.tile_idx}", (x_pos, y_pos := y_pos + 20))

    def __update_time(self):
        self.current_time_in_secs = time.time()
        self.time_delta_in_secs = self.current_time_in_secs - self.previous_time_in_secs
        self.previous_time_in_secs = self.current_time_in_secs
