import enum
import pygame

from rooms import *
from utils import *


class ElementType(enum.StrEnum):
    FLOOR = "F"
    OBSTACLE = "X"
    HERO = "H"
    ENEMY = "E"


class Game:
    def __init__(self, map_size_in_tiles: tuple[int, int]) -> None:
        self.map_width_in_tiles, self.map_height_in_tiles = map_size_in_tiles
        self.map = [
            [ElementType.FLOOR] * self.map_width_in_tiles
            for _ in range(self.map_height_in_tiles)
        ]

    def update_map_from_room(self, room: Room) -> None:
        self.map = [
            [
                ElementType.FLOOR if tile == TileType.FLOOR else ElementType.OBSTACLE
                for tile in tile_row
            ]
            for tile_row in room.room_map
        ]

    def render_map(self) -> None:
        # Cache text surfaces
        element_type_text_surfs = {
            element_type: render_text(str(element_type)) for element_type in ElementType
        }

        # Blit the cached text surfaces on screen, instead of calling debug on each iteration
        # (used to incur in a huge performance loss)
        screen = pygame.display.get_surface()
        for j, tile_row in enumerate(self.map):
            for i, element_type in enumerate(tile_row):
                text_surf = element_type_text_surfs[element_type]
                text_rect = text_surf.get_rect(topleft=tile_top_left((i, j)))
                screen.blit(text_surf, text_rect)
