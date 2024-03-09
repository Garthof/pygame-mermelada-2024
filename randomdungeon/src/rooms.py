import enum
import pygame

from globals import *


class Room:
    def __init__(self):
        self.tile_width = ROOM_TILE_RADIUS * 2
        self.tile_height = ROOM_TILE_RADIUS * 2
        self.tile_size = self.tile_width, self.tile_height

        def load_file(file_idx: Path):
            return pygame.image.load(
                PATH_GRAPHICS_TILES / f"tile_{file_idx}.png"
            ).convert()

        self.tile_surfs = {}
        self.tile_surfs["wall_top"] = load_file("0014")
        self.tile_surfs["wall_bottom"] = load_file("0006")
        self.tile_surfs["wall_left"] = load_file("0013")
        self.tile_surfs["wall_right"] = load_file("0015")
        self.tile_surfs["floor"] = load_file("0048")

        for tile_name in self.tile_surfs:
            tile_surf = self.tile_surfs[tile_name]
            tile_surf = pygame.transform.scale(tile_surf, self.tile_size)
            self.tile_surfs[tile_name] = tile_surf

        self.map_width_in_tiles = WINDOW_WIDTH // self.tile_width
        self.map_height_in_tiles = WINDOW_HEIGHT // self.tile_height

    def render(self, screen: pygame.Surface):
        for j in range(self.map_height_in_tiles):
            for i in range(self.map_width_in_tiles):
                if j == 0:
                    tile_surf = self.tile_surfs["wall_top"]
                elif j == self.map_height_in_tiles - 1:
                    tile_surf = self.tile_surfs["wall_bottom"]
                elif i == 0:
                    tile_surf = self.tile_surfs["wall_left"]
                elif i == self.map_width_in_tiles - 1:
                    tile_surf = self.tile_surfs["wall_right"]
                else:
                    tile_surf = self.tile_surfs["floor"]

                tile_pos = i * self.tile_width, j * self.tile_height
                tile_rect = tile_surf.get_rect(topleft=tile_pos)
                screen.blit(tile_surf, tile_rect)
