import enum
import pygame

from globals import *
from utils import *


class TileType(enum.Enum):
    FLOOR = enum.auto()
    WALL = enum.auto()


class Room:
    def __init__(self):
        self.tile_surfs = {}

        self.tile_surfs["wall_parapet_top"] = load_tile("0026")
        self.tile_surfs["wall_parapet_bottom"] = load_tile("0002")

        self.tile_surfs["wall_parapet_top_left"] = load_tile("0004")
        self.tile_surfs["wall_parapet_top_right"] = load_tile("0005")
        self.tile_surfs["wall_parapet_bottom_left"] = load_tile("0016")
        self.tile_surfs["wall_parapet_bottom_right"] = load_tile("0017")

        self.tile_surfs["wall_parapet_top_left_corner"] = load_tile("0027")
        self.tile_surfs["wall_parapet_top_right_corner"] = load_tile("0025")
        self.tile_surfs["wall_parapet_bottom_left_corner"] = load_tile("0003")
        self.tile_surfs["wall_parapet_bottom_right_corner"] = load_tile("0001")

        self.tile_surfs["wall_front"] = load_tile("0014")
        self.tile_surfs["wall_left"] = load_tile("0013")
        self.tile_surfs["wall_right"] = load_tile("0015")

        self.tile_surfs["floor"] = load_tile("0048")

        self.tile_surfs["corridor_left"] = load_tile("0010")
        self.tile_surfs["corridor_right"] = load_tile("0011")

        self.map_width_in_tiles, self.map_height_in_tiles = window_size_in_tiles()
        self.tile_map, self.room_map = self.__generate_maps()

    def __generate_maps(
        self,
    ) -> tuple[list[list[pygame.Surface | None]], list[list[TileType | None]]]:
        tile_map: list[list[pygame.Surface | None]] = [
            [None] * self.map_width_in_tiles for _ in range(self.map_height_in_tiles)
        ]
        room_map: list[list[TileType | None]] = [
            [None] * self.map_width_in_tiles for _ in range(self.map_height_in_tiles)
        ]

        # Render floor
        for j in range(self.map_height_in_tiles):
            for i in range(self.map_width_in_tiles):
                tile_map[j][i] = self.tile_surfs["floor"]
                room_map[j][i] = TileType.FLOOR

        # Render walls
        for j in range(self.map_height_in_tiles):
            for i in range(self.map_width_in_tiles):
                if j == 0:
                    if i == 0:
                        tile_map[j][i] = self.tile_surfs[
                            "wall_parapet_bottom_right_corner"
                        ]
                        room_map[j][i] = TileType.WALL
                    elif i == self.map_width_in_tiles - 1:
                        tile_map[j][i] = self.tile_surfs[
                            "wall_parapet_bottom_left_corner"
                        ]
                        room_map[j][i] = TileType.WALL
                    else:
                        tile_map[j][i] = self.tile_surfs["wall_parapet_bottom"]
                        room_map[j][i] = TileType.WALL

                elif j == 1:
                    if i == 0:
                        tile_map[j][i] = self.tile_surfs["wall_left"]
                        room_map[j][i] = TileType.WALL
                    elif i == self.map_width_in_tiles - 1:
                        tile_map[j][i] = self.tile_surfs["wall_right"]
                        room_map[j][i] = TileType.WALL
                    else:
                        tile_map[j][i] = self.tile_surfs["wall_front"]
                        room_map[j][i] = TileType.WALL

                elif j == self.map_height_in_tiles - 1:
                    if i == 0:
                        tile_map[j][i] = self.tile_surfs[
                            "wall_parapet_top_right_corner"
                        ]
                        room_map[j][i] = TileType.WALL
                    elif i == self.map_width_in_tiles - 1:
                        tile_map[j][i] = self.tile_surfs["wall_parapet_top_left_corner"]
                        room_map[j][i] = TileType.WALL
                    else:
                        tile_map[j][i] = self.tile_surfs["wall_parapet_top"]
                        room_map[j][i] = TileType.WALL

                elif i == 0:
                    tile_map[j][i] = self.tile_surfs["wall_left"]
                    room_map[j][i] = TileType.WALL
                elif i == self.map_width_in_tiles - 1:
                    tile_map[j][i] = self.tile_surfs["wall_right"]
                    room_map[j][i] = TileType.WALL

        # Render exits
        horizontal_exit_left_i = self.map_width_in_tiles // 2 - 1
        tile_map[1][horizontal_exit_left_i] = self.tile_surfs["corridor_left"]
        tile_map[1][horizontal_exit_left_i + 1] = self.tile_surfs["corridor_right"]

        vertical_exit_top_j = self.map_height_in_tiles // 2 - 2
        tile_map[vertical_exit_top_j][0] = self.tile_surfs["wall_parapet_bottom_right"]
        tile_map[vertical_exit_top_j + 1][0] = self.tile_surfs["wall_front"]
        tile_map[vertical_exit_top_j + 2][0] = self.tile_surfs["floor"]
        room_map[vertical_exit_top_j + 2][0] = TileType.FLOOR
        tile_map[vertical_exit_top_j + 3][0] = self.tile_surfs["wall_parapet_top_right"]

        tile_map[vertical_exit_top_j][self.map_width_in_tiles - 1] = self.tile_surfs[
            "wall_parapet_bottom_left"
        ]
        tile_map[vertical_exit_top_j + 1][self.map_width_in_tiles - 1] = (
            self.tile_surfs["wall_front"]
        )
        tile_map[vertical_exit_top_j + 2][self.map_width_in_tiles - 1] = (
            self.tile_surfs["floor"]
        )
        room_map[vertical_exit_top_j + 2][self.map_width_in_tiles - 1] = TileType.FLOOR
        tile_map[vertical_exit_top_j + 3][self.map_width_in_tiles - 1] = (
            self.tile_surfs["wall_parapet_top_left"]
        )

        tile_map[self.map_height_in_tiles - 1][horizontal_exit_left_i - 1] = (
            self.tile_surfs["wall_parapet_top_right"]
        )
        tile_map[self.map_height_in_tiles - 1][horizontal_exit_left_i] = (
            self.tile_surfs["floor"]
        )
        tile_map[self.map_height_in_tiles - 1][horizontal_exit_left_i + 1] = (
            self.tile_surfs["floor"]
        )
        room_map[self.map_height_in_tiles - 1][horizontal_exit_left_i] = TileType.FLOOR
        room_map[self.map_height_in_tiles - 1][
            horizontal_exit_left_i + 1
        ] = TileType.FLOOR
        tile_map[self.map_height_in_tiles - 1][horizontal_exit_left_i + 2] = (
            self.tile_surfs["wall_parapet_top_left"]
        )

        return tile_map, room_map

    def render(self):
        screen = pygame.display.get_surface()
        tile_width, tile_height = tile_size()

        for j, tile_row in enumerate(self.tile_map):
            for i, tile_surf in enumerate(tile_row):
                tile_pos = i * tile_width, j * tile_height
                tile_rect = tile_surf.get_rect(topleft=tile_pos)
                screen.blit(tile_surf, tile_rect)

                if DEBUG_RENDER_TILE_BORDERS:
                    pygame.draw.rect(screen, "black", tile_rect, 1)
