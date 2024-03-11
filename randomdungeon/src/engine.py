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
        self.room: Room | None = None

        self.initialized = True
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        pygame.mixer.quit()
        pygame.quit()

    def run(self) -> None:
        if not self.initialized:
            raise RuntimeError("Engine not initialized")

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
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:  # closing window
                self.running = False

        if self.room:
            self.room.read_events(events)

    def __update(self) -> None:
        match self.game.state:
            case GameState.START_DISPLAY_MENU:
                self.room = MenuRoom(self.game)
                self.room.enter()
                self.game.state = GameState.DISPLAY_MENU

            case GameState.DISPLAY_MENU:
                if self.room:
                    self.room.update(self.time_delta_in_secs)

            case GameState.START_PLAY:
                self.game.level = 1
                self.game.hero_life_points = 3
                self.room = MonsterRoom(self.game, self.game.level)
                self.room.hero.current_tile_idx = pygame.Vector2(
                    window_size_in_tiles()[0] // 2, window_size_in_tiles()[1] // 2
                )
                self.room.enter()
                self.game.state = GameState.PLAY

            case GameState.PLAY if isinstance(self.room, MonsterRoom):
                self.game.background_music.play(-1, 0, 5000)
                self.game.background_music.set_volume(0.2)
                self.room.update(self.time_delta_in_secs)

                if self.game.hero_life_points == 0:
                    self.game.state = GameState.DISPLAY_GAME_OVER

                if not self.room.monsters and (
                    self.room.hero.current_tile_idx == self.game.door_left_tile_idx
                    or self.room.hero.current_tile_idx == self.game.door_right_tile_idx
                ):
                    self.__move_to_next_room()

            case GameState.DISPLAY_GAME_OVER:
                self.game.background_music.stop()
                self.room = MenuRoom(self.game, render_achievements=True)
                self.room.enter()
                self.game.state = GameState.DISPLAY_MENU

            case _:
                raise ValueError(f"Invalid game state: {self.game.state}")

    def __move_to_next_room(self) -> None:
        if self.room:
            self.room.exit()

            self.game.level += 1
            self.room = MonsterRoom(self.game, self.game.level)
            self.room.hero.current_tile_idx = pygame.Vector2(8.0, 11.0)

            self.room.enter()

    def __animate(self) -> None:
        if self.room:
            self.room.animate(self.time_delta_in_secs)

    def __render(self) -> None:
        if self.room:
            self.room.render()

        if DEBUG_RENDER_GAME_MAP:
            self.game.render_map()

        if DEBUG_RENDER_STATS:
            self.__render_stats()

        pygame.display.flip()

    def __render_stats(self) -> None:
        x_pos, y_pos = 10, 10
        debug(f"FPS: {round(self.clock.get_fps(), 1)}", (x_pos, y_pos))

        if self.game.state == GameState.PLAY and isinstance(self.room, DungeonRoom):
            debug(
                f"Mouse: {self.room.mouse_tile_cursor.tile_idx}",
                (x_pos, y_pos := y_pos + 20),
            )

    def __update_time(self) -> None:
        self.current_time_in_secs = time.time()
        self.time_delta_in_secs = self.current_time_in_secs - self.previous_time_in_secs
        self.previous_time_in_secs = self.current_time_in_secs
