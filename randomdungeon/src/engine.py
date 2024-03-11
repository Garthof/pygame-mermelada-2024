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

        self.game = GameStatus(window_size_in_tiles())
        self.room = MonsterRoom(self.game)

        self.initialized = True
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        pygame.mixer.quit()
        pygame.quit()

    def run(self) -> None:
        if not self.initialized:
            raise RuntimeError("Engine not initialized")

        self.room.enter()

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

        self.room.read_events(events)

    def __update(self) -> None:
        self.room.update(self.time_delta_in_secs)

    def __animate(self) -> None:
        self.room.animate(self.time_delta_in_secs)

    def __render(self) -> None:
        self.screen.fill(BACKGROUND_COLOR)
        self.room.render()

        if DEBUG_RENDER_GAME_MAP:
            self.game.render_map()

        if DEBUG_RENDER_STATS:
            self.__render_stats()

        pygame.display.flip()

    def __render_stats(self) -> None:
        x_pos, y_pos = 10, 10
        debug(f"FPS: {round(self.clock.get_fps(), 1)}", (x_pos, y_pos))
        debug(
            f"Mouse: {self.room.mouse_tile_cursor.tile_idx}",
            (x_pos, y_pos := y_pos + 20),
        )

    def __update_time(self) -> None:
        self.current_time_in_secs = time.time()
        self.time_delta_in_secs = self.current_time_in_secs - self.previous_time_in_secs
        self.previous_time_in_secs = self.current_time_in_secs
