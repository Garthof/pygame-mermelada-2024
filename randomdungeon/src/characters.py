import pygame
import pygame.freetype

from dataclasses import dataclass
from globals import *

NULL_VECTOR = pygame.Vector2(0.0, 0.0)
NULL_RECTANGLE = pygame.Rect(0.0, 0.0, 0.0, 0.0)


@dataclass
class Hero:
    position: pygame.Vector2
    rectangle = NULL_RECTANGLE.copy()

    def render(self, screen: pygame.Surface):
        player_rectangle = pygame.Rect(0, 0, HERO_RADIUS * 2, HERO_RADIUS * 2)
        player_rectangle.center = self.position  # type: ignore
        self.rectangle = pygame.draw.rect(screen, HERO_COLOR, player_rectangle, 0, 2)
