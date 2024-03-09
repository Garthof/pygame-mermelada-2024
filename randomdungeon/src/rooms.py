import pygame

from globals import *
from utils import *


class Room:
    def __init__(self):
        self.tile_width = TILE_RADIUS * 2
        self.tile_height = TILE_RADIUS * 2
        self.tile_size = self.tile_width, self.tile_height

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

        self.map_width_in_tiles = WINDOW_WIDTH // self.tile_width
        self.map_height_in_tiles = WINDOW_HEIGHT // self.tile_height
        self.map = self.__generate_map()

    def __generate_map(self):
        map = [
            [None] * self.map_width_in_tiles for _ in range(self.map_height_in_tiles)
        ]

        # Render floor
        for j in range(self.map_height_in_tiles):
            for i in range(self.map_width_in_tiles):
                map[j][i] = self.tile_surfs["floor"]

        # Render walls
        for j in range(self.map_height_in_tiles):
            for i in range(self.map_width_in_tiles):
                if j == 0:
                    if i == 0:
                        map[j][i] = self.tile_surfs["wall_parapet_bottom_right_corner"]
                    elif i == self.map_width_in_tiles - 1:
                        map[j][i] = self.tile_surfs["wall_parapet_bottom_left_corner"]
                    else:
                        map[j][i] = self.tile_surfs["wall_parapet_bottom"]

                elif j == 1:
                    if i == 0:
                        map[j][i] = self.tile_surfs["wall_left"]
                    elif i == self.map_width_in_tiles - 1:
                        map[j][i] = self.tile_surfs["wall_right"]
                    else:
                        map[j][i] = self.tile_surfs["wall_front"]

                elif j == self.map_height_in_tiles - 1:
                    if i == 0:
                        map[j][i] = self.tile_surfs["wall_parapet_top_right_corner"]
                    elif i == self.map_width_in_tiles - 1:
                        map[j][i] = self.tile_surfs["wall_parapet_top_left_corner"]
                    else:
                        map[j][i] = self.tile_surfs["wall_parapet_top"]

                elif i == 0:
                    map[j][i] = self.tile_surfs["wall_left"]
                elif i == self.map_width_in_tiles - 1:
                    map[j][i] = self.tile_surfs["wall_right"]

        # Render exits
        horizontal_exit_left_i = self.map_width_in_tiles // 2 - 1
        map[1][horizontal_exit_left_i] = self.tile_surfs["corridor_left"]
        map[1][horizontal_exit_left_i + 1] = self.tile_surfs["corridor_right"]

        vertical_exit_top_j = self.map_height_in_tiles // 2 - 2
        map[vertical_exit_top_j][0] = self.tile_surfs["wall_parapet_bottom_right"]
        map[vertical_exit_top_j + 1][0] = self.tile_surfs["wall_front"]
        map[vertical_exit_top_j + 2][0] = self.tile_surfs["floor"]
        map[vertical_exit_top_j + 3][0] = self.tile_surfs["wall_parapet_top_right"]

        map[vertical_exit_top_j][self.map_width_in_tiles - 1] = self.tile_surfs[
            "wall_parapet_bottom_left"
        ]
        map[vertical_exit_top_j + 1][self.map_width_in_tiles - 1] = self.tile_surfs[
            "wall_front"
        ]
        map[vertical_exit_top_j + 2][self.map_width_in_tiles - 1] = self.tile_surfs[
            "floor"
        ]
        map[vertical_exit_top_j + 3][self.map_width_in_tiles - 1] = self.tile_surfs[
            "wall_parapet_top_left"
        ]

        map[self.map_height_in_tiles - 1][horizontal_exit_left_i - 1] = self.tile_surfs[
            "wall_parapet_top_right"
        ]
        map[self.map_height_in_tiles - 1][horizontal_exit_left_i] = self.tile_surfs[
            "floor"
        ]
        map[self.map_height_in_tiles - 1][horizontal_exit_left_i + 1] = self.tile_surfs[
            "floor"
        ]
        map[self.map_height_in_tiles - 1][horizontal_exit_left_i + 2] = self.tile_surfs[
            "wall_parapet_top_left"
        ]

        return map

    def render(self, screen: pygame.Surface):
        for j, tile_row in enumerate(self.map):
            for i, tile_surf in enumerate(tile_row):
                tile_pos = i * self.tile_width, j * self.tile_height
                tile_rect = tile_surf.get_rect(topleft=tile_pos)
                screen.blit(tile_surf, tile_rect)

                if DEBUG_DRAW_TILE_BORDERS:
                    pygame.draw.rect(screen, "black", tile_rect, 1)
