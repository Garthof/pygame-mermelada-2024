import enum
import pygame
import random
import time
import typing

from actors import *
from game import *
from globals import *
from rooms import *
from utils import *


class Engine:
    def __init__(self) -> None:
        self.time_delta_in_secs = 0.0
        self.current_time_in_secs = 0.0
        self.previous_time_in_secs = 0.0
        self.running = False

    def __enter__(self) -> typing.Self:
        pygame.init()
        pygame.mixer.init()

        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Random Dungeon")

        self.game = Game(window_size_in_tiles())

        self.hero = Hero(HERO_TILE_FILE_IDX)
        self.hero.game = self.game
        self.hero.current_tile_idx = pygame.Vector2(
            window_size_in_tiles()[0] // 2, window_size_in_tiles()[1] // 2
        )
        self.hero.next_tile_idx = self.hero.current_tile_idx
        self.hero.position = tile_center(self.hero.current_tile_idx)

        self.hero_attack_countdown_in_secs = 0.0

        self.enemy = Enemy(ENEMY_CRAB_TILE_FILE_IDX)
        self.enemy.game = self.game
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

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        pygame.mixer.quit()
        pygame.quit()

    def run(self) -> None:
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

    def __read_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # closing window
                self.running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pressed_buttons = pygame.mouse.get_pressed()
                if pressed_buttons[0]:
                    pressed_tile = tile_idx(pygame.mouse.get_pos())
                    if is_valid_tile(pressed_tile):
                        self.hero.target_tile_idx = pressed_tile
                        for enemy in self.enemies:
                            if are_same_tile(enemy.current_tile_idx, pressed_tile):
                                self.hero.enemy_target = enemy
                                self.hero.attack_on_sight = True
                                break

            if event.type == self.enemy_walk_event:
                for enemy in self.enemies:
                    enemy.target_tile_idx = pygame.Vector2(-1, -1)
                    while not is_valid_tile(enemy.target_tile_idx):
                        enemy.target_tile_idx = enemy.current_tile_idx + pygame.Vector2(
                            random.randint(-5, 5), 0
                        )

        hover_mouse_position = pygame.mouse.get_pos()
        self.mouse_tile_cursor.position = pygame.Vector2(hover_mouse_position)

    def __update(self) -> None:
        self.__update_game_map()

        self.hero.update(self.time_delta_in_secs)
        for enemy in self.enemies:
            enemy.update(self.time_delta_in_secs)

        self.hero_attack_countdown_in_secs -= self.time_delta_in_secs
        if self.hero_attack_countdown_in_secs < 0:
            self.hero_attack_countdown_in_secs = 0

        self.enemies = [enemy for enemy in self.enemies if enemy.life_points > 0]

    def __update_game_map(self) -> None:
        self.game.update_map_from_room(self.room)

        self.game.map[int(self.hero.current_tile_idx.y)][
            int(self.hero.current_tile_idx.x)
        ] = GameObjectType.HERO

        for enemy in self.enemies:
            self.game.map[int(enemy.current_tile_idx.y)][
                int(enemy.current_tile_idx.x)
            ] = GameObjectType.ENEMY

    def __animate(self) -> None:
        self.hero.animate(self.time_delta_in_secs)
        for enemy in self.enemies:
            enemy.animate(self.time_delta_in_secs)
        self.mouse_tile_cursor.animate()

    def __render(self) -> None:
        self.screen.fill(BACKGROUND_COLOR)
        self.room.render()
        for enemy in self.enemies:
            enemy.render()
        self.hero.render()
        self.mouse_tile_cursor.render()

        if DEBUG_RENDER_GAME_MAP:
            self.game.render_map()

        if DEBUG_RENDER_STATS:
            self.__render_stats()

        pygame.display.flip()

    def __render_stats(self) -> None:
        x_pos, y_pos = 10, 10
        debug(f"FPS: {round(self.clock.get_fps(), 1)}", (x_pos, y_pos))
        debug(f"Mouse: {self.mouse_tile_cursor.tile_idx}", (x_pos, y_pos := y_pos + 20))
        debug(f"Hero: {self.hero.stance_state}", (x_pos, y_pos := y_pos + 20))

    def __update_time(self) -> None:
        self.current_time_in_secs = time.time()
        self.time_delta_in_secs = self.current_time_in_secs - self.previous_time_in_secs
        self.previous_time_in_secs = self.current_time_in_secs
