import pygame

from globals import *


def load_tile(file_idx: str, alpha=True) -> pygame.Surface:
    surf = pygame.image.load(GRAPHICS_TILES_PATH / f"tile_{file_idx}.png")
    if alpha:
        surf = surf.convert_alpha()
    else:
        surf = surf.convert()

    tile_width = TILE_RADIUS * 2
    tile_height = TILE_RADIUS * 2
    tile_size = tile_width, tile_height
    surf = pygame.transform.scale(surf, tile_size)

    return surf


def tile_position(tile_idx: pygame.Vector2 | tuple[int, int]) -> pygame.Vector2:
    return pygame.Vector2(
        tile_idx[0] * TILE_RADIUS * 2 + TILE_RADIUS,
        tile_idx[1] * TILE_RADIUS * 2 + TILE_RADIUS,
    )
