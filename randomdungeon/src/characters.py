import pygame

from globals import *
from utils import *


class Hero:
    def __init__(self):
        self.position = pygame.Vector2()
        self.surface = load_tile("0099")
        self.target_tile = 0, 0

    def render(self, screen: pygame.Surface):
        hero_rect = self.surface.get_rect(center=self.position)
        screen.blit(self.surface, hero_rect)

        if DEBUG_RENDER_HERO_TARGET_TILE:
            tile_width = TILE_RADIUS * 2
            tile_height = TILE_RADIUS * 2
            target_tile_rect = pygame.Rect(0, 0, tile_width, tile_height)
            target_tile_rect.topleft = (
                tile_width * self.target_tile[0],
                tile_height * self.target_tile[1],
            )
            pygame.draw.rect(screen, "green", target_tile_rect, 5)
