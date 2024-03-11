import pygame

from typing import Never, NoReturn

from globals import *


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


def are_adjacent_tiles(
    tile_idx_1: pygame.Vector2 | tuple[int, int],
    tile_idx_2: pygame.Vector2 | tuple[int, int],
) -> bool:
    dist_in_tiles = pygame.Vector2(tile_idx_1).distance_squared_to(
        pygame.Vector2(tile_idx_2)
    )
    return dist_in_tiles < 1.5


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


def load_tile(file_idx: str, alpha=True) -> pygame.Surface:
    surf = pygame.image.load(GRAPHICS_TILES_PATH / f"tile_{file_idx}.png")
    if alpha:
        surf = surf.convert_alpha()
    else:
        surf = surf.convert()

    surf = pygame.transform.scale(surf, tile_size())

    return surf


def is_valid_position(position: pygame.Vector2 | tuple[int, int]) -> bool:
    return 0 <= position[0] < WINDOW_WIDTH and 0 <= position[1] < WINDOW_HEIGHT


def render_text(
    text: str,
    font: pygame.font.Font | None = None,
    foreground: str = "white",
    background: str | None = None,
) -> pygame.Surface:
    if not font:
        font = pygame.font.Font(None, 30)

    text_surf = font.render(text, True, foreground)
    text_rect = text_surf.get_rect()
    render_surf = pygame.Surface(text_rect.size)

    if background:
        pygame.draw.rect(render_surf, background, text_rect)

    render_surf.blit(text_surf, text_rect)

    return render_surf


def debug(text: str, position=pygame.Vector2(10, 10)) -> None:
    text_surf = render_text(text, background="black")
    text_rect = text_surf.get_rect(topleft=position)
    screen = pygame.display.get_surface()
    screen.blit(text_surf, text_rect)


def assert_unreachable(arg: Never) -> NoReturn:
    raise AssertionError(f"Unreachable code")
