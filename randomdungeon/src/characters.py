import pygame

from globals import *
from utils import *


class TileCursor:
    def __init__(self) -> None:
        self.color = "green"
        self.thickness = 5
        self.position = pygame.Vector2()
        self.tile_idx = pygame.Vector2()

    def animate(self):
        self.tile_idx = tile_idx(self.position)

    def render(self):
        screen = pygame.display.get_surface()
        tile_width, tile_height = tile_size()
        target_tile_rect = pygame.Rect(0, 0, tile_width, tile_height)
        target_tile_rect.topleft = tile_top_left(self.tile_idx)
        pygame.draw.rect(screen, self.color, target_tile_rect, self.thickness)


class Character:
    def __init__(self, tile_idx: str):
        self.surface = load_tile(tile_idx)
        self.position = pygame.Vector2()
        self.current_tile_idx = pygame.Vector2()
        self.target_tile_idx = None
        self.next_tile_idx = self.current_tile_idx
        self.is_walking = False
        self.life_points = 1

    def animate(self, time_delta_in_secs: float):
        if self.target_tile_idx and are_same_tile(
            self.current_tile_idx, self.next_tile_idx
        ):
            self.__set_next_tile_towards_target()
            return

        if not are_same_tile(self.current_tile_idx, self.next_tile_idx):
            self.__move_to_next_tile(time_delta_in_secs)
            if self.__has_reached_tile(self.next_tile_idx):
                self.current_tile_idx = self.next_tile_idx
                self.position = tile_center(self.current_tile_idx)

                if self.target_tile_idx and are_same_tile(
                    self.current_tile_idx, self.target_tile_idx
                ):
                    self.target_tile_idx = None

    def render(self):
        screen = pygame.display.get_surface()
        hero_rect = self.surface.get_rect(center=self.position)
        screen.blit(self.surface, hero_rect)

        if DEBUG_RENDER_HERO_TILES:
            if self.target_tile_idx:
                self.__render_tile_cursor(self.target_tile_idx, "red")
            self.__render_tile_cursor(self.next_tile_idx, "green")
            self.__render_tile_cursor(self.current_tile_idx, "blue")

    def __set_next_tile_towards_target(self):
        self.next_tile_idx = self.current_tile_idx
        dist_to_target_in_tiles = self.target_tile_idx - self.current_tile_idx

        if abs(dist_to_target_in_tiles.x) > abs(dist_to_target_in_tiles.y):
            if dist_to_target_in_tiles.x > 0:
                self.next_tile_idx = self.current_tile_idx + pygame.Vector2(1, 0)
            elif dist_to_target_in_tiles.x < 0:
                self.next_tile_idx = self.current_tile_idx - pygame.Vector2(1, 0)
        else:
            if dist_to_target_in_tiles.y < 0:
                self.next_tile_idx = self.current_tile_idx - pygame.Vector2(0, 1)
            elif dist_to_target_in_tiles.y > 0:
                self.next_tile_idx = self.current_tile_idx + pygame.Vector2(0, 1)

    def __move_to_next_tile(self, time_delta_in_secs: float):
        delta = self.next_tile_idx - self.current_tile_idx
        self.position += delta * HERO_SPEED * time_delta_in_secs

    def __has_reached_tile(self, tile_idx: pygame.Vector2 | tuple[int, int]):
        hero_top_left = self.position - pygame.Vector2(TILE_RADIUS, TILE_RADIUS)
        dist_to_tile = hero_top_left.distance_to(tile_top_left(tile_idx))
        return dist_to_tile <= HERO_DISTANCE_TO_TILE_EPSILON

    def __render_tile_cursor(
        self, tile_idx: pygame.Vector2 | tuple[int, int], color: str
    ):
        tile_cursor = TileCursor()
        tile_cursor.color = color
        tile_cursor.position = tile_center(tile_idx)
        tile_cursor.animate()
        tile_cursor.render()
