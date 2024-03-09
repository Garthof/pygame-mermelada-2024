import math
import pygame

from globals import *
from utils import *


class Hero:
    def __init__(self):
        self.surface = load_tile("0099")
        self.position = pygame.Vector2()
        self.current_tile = pygame.Vector2()
        self.target_tile = pygame.Vector2()
        self.is_walking = False

    def animate(self, time_delta_in_secs: float):
        if self.current_tile == self.target_tile:
            self.is_walking = False
            return

        self.is_walking = True
        dist_in_tiles = self.target_tile - self.current_tile
        if dist_in_tiles.x > 0:
            self.position.x += HERO_SPEED * time_delta_in_secs
        elif dist_in_tiles.x < 0:
            self.position.x -= HERO_SPEED * time_delta_in_secs
        elif dist_in_tiles.y < 0:
            self.position.y -= HERO_SPEED * time_delta_in_secs
        elif dist_in_tiles.y > 0:
            self.position.y += HERO_SPEED * time_delta_in_secs

        dist_to_target = self.position.distance_to(tile_position(self.target_tile))
        if dist_to_target < 1.0:
            self.current_tile = self.target_tile
            self.position = tile_position(self.current_tile)

    def render(self, screen: pygame.Surface):
        hero_rect = self.surface.get_rect(center=self.position)
        screen.blit(self.surface, hero_rect)

        if DEBUG_RENDER_HERO_TARGET_TILE:
            tile_width = TILE_RADIUS * 2
            tile_height = TILE_RADIUS * 2
            target_tile_rect = pygame.Rect(0, 0, tile_width, tile_height)
            target_tile_rect.topleft = (
                tile_width * int(self.target_tile.x),
                tile_height * int(self.target_tile.y),
            )
            pygame.draw.rect(screen, "green", target_tile_rect, 5)
