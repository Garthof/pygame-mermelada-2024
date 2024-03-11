import enum
import pygame

from actors import *
from rooms import *
from utils import *


class GameObjectType(enum.StrEnum):
    FLOOR = "   "
    OBSTACLE = "X"
    HERO = "H"
    ENEMY = "E"


class Game:
    def __init__(self, map_size_in_tiles: tuple[int, int]) -> None:
        self.map_width_in_tiles, self.map_height_in_tiles = map_size_in_tiles
        self.map = [
            [GameObjectType.FLOOR] * self.map_width_in_tiles
            for _ in range(self.map_height_in_tiles)
        ]

    def update_map_from_room(self, room: Room) -> None:
        self.map = [
            [
                (
                    GameObjectType.FLOOR
                    if tile == TileType.FLOOR
                    else GameObjectType.OBSTACLE
                )
                for tile in tile_row
            ]
            for tile_row in room.room_map
        ]

    def object_at(self, tile_idx: pygame.Vector2 | tuple[int, int]) -> GameObjectType:
        return self.map[int(tile_idx[1])][int(tile_idx[0])]

    def render_map(self) -> None:
        # Cache text surfaces
        object_type_text_surfs = {
            object_type: render_text(str(object_type)) for object_type in GameObjectType
        }

        # Blit the cached text surfaces on screen, instead of calling debug on each iteration
        # (used to incur in a huge performance loss)
        screen = pygame.display.get_surface()
        for j, tile_row in enumerate(self.map):
            for i, element_type in enumerate(tile_row):
                text_surf = object_type_text_surfs[element_type]
                text_rect = text_surf.get_rect(topleft=tile_top_left((i, j)))
                screen.blit(text_surf, text_rect)
