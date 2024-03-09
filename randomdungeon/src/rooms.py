import pygame

from globals import *


class Room:
    def __init__(self):
        self.tile_width = ROOM_TILE_RADIUS * 2
        self.tile_height = ROOM_TILE_RADIUS * 2
        self.tile_size = self.tile_width, self.tile_height

        tile_surf = pygame.image.load(PATH_GRAPHICS_TILES / "tile_0033.png").convert()
        tile_surf = pygame.transform.scale(tile_surf, self.tile_size)

        self.map_width_in_tiles = WINDOW_WIDTH // self.tile_width
        self.map_height_in_tiles = WINDOW_HEIGHT // self.tile_height
        self.map = [
            [tile_surf for i in range(self.map_width_in_tiles)]
            for j in range(self.map_height_in_tiles)
        ]

    def render(self, screen: pygame.Surface):
        for j, tile_row in enumerate(self.map):
            for i, tile_surf in enumerate(tile_row):
                tile_pos = i * self.tile_width, j * self.tile_height
                tile_rect = tile_surf.get_rect(topleft=tile_pos)
                screen.blit(tile_surf, tile_rect)
