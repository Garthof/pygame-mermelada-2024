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


def tile_size():
    return TILE_RADIUS * 2, TILE_RADIUS * 2


def window_size_in_tiles():
    tile_width, tile_height = tile_size()
    return WINDOW_WIDTH // tile_width, WINDOW_HEIGHT // tile_height


def is_valid_tile(tile_idx: pygame.Vector2 | tuple[int, int]) -> pygame.Vector2:
    window_width_in_tiles, window_height_in_tiles = window_size_in_tiles()
    return (
        0 <= int(tile_idx[0]) < window_width_in_tiles
        and 0 <= int(tile_idx[1]) < window_height_in_tiles
    )


def tile_idx(position: pygame.Vector2 | tuple[int, int]) -> pygame.Vector2:
    return pygame.Vector2(
        int(position[0] / (TILE_RADIUS * 2)), int(position[1] / (TILE_RADIUS * 2))
    )


def are_same_tile(
    tile_idx_1: pygame.Vector2 | tuple[int, int],
    tile_idx_2: pygame.Vector2 | tuple[int, int],
):
    return int(tile_idx_1[0]) == int(tile_idx_2[0]) and int(tile_idx_1[1]) == int(
        tile_idx_2[1]
    )


def tile_center(tile_idx: pygame.Vector2 | tuple[int, int]) -> pygame.Vector2:
    return pygame.Vector2(
        tile_idx[0] * TILE_RADIUS * 2 + TILE_RADIUS,
        tile_idx[1] * TILE_RADIUS * 2 + TILE_RADIUS,
    )


def tile_top_left(tile_idx: pygame.Vector2 | tuple[int, int]) -> pygame.Vector2:
    return pygame.Vector2(
        tile_idx[0] * TILE_RADIUS * 2,
        tile_idx[1] * TILE_RADIUS * 2,
    )
