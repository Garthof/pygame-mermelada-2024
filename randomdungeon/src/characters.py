import enum
import pygame

from game import *
from globals import *
from utils import *


class MovementState(enum.Enum):
    IDLE = enum.auto()
    CHECK_MOVE = enum.auto()
    MOVE = enum.auto()
    REACHED_NEXT_TILE = enum.auto()
    REACHED_TARGET_TILE = enum.auto()
    BLOCKED = enum.auto()


class StanceState(enum.Enum):
    NORMAL = enum.auto()
    PURSUIT = enum.auto()
    ATTACK = enum.auto()


class TileCursor:
    def __init__(self) -> None:
        self.color = "green"
        self.thickness = 5
        self.position = pygame.Vector2()
        self.tile_idx = pygame.Vector2()

    def animate(self) -> None:
        self.tile_idx = tile_idx(self.position)

    def render(self) -> None:
        screen = pygame.display.get_surface()
        tile_width, tile_height = tile_size()
        target_tile_rect = pygame.Rect(0, 0, tile_width, tile_height)
        target_tile_rect.topleft = tile_top_left(self.tile_idx)  # type: ignore
        pygame.draw.rect(screen, self.color, target_tile_rect, self.thickness)


class Character:
    def __init__(self, tile_idx: str) -> None:
        self.game: Game | None = None
        self.surface = load_tile(tile_idx)
        self.position = pygame.Vector2()
        self.current_tile_idx = pygame.Vector2()
        self.target_tile_idx: pygame.Vector2 | None = None
        self.next_tile_idx = self.current_tile_idx
        self.movement_state = MovementState.IDLE
        self.life_points = 1

    def update(self) -> None:
        if self.movement_state == MovementState.IDLE:
            if self.target_tile_idx:
                self.movement_state = MovementState.CHECK_MOVE

        elif self.movement_state == MovementState.CHECK_MOVE:
            self.__set_next_tile_towards_target()
            if self.__can_move_to_next_tile():
                self.movement_state = MovementState.MOVE
            else:
                self.movement_state = MovementState.BLOCKED

        elif self.movement_state == MovementState.MOVE:
            if self.__has_reached_tile(self.next_tile_idx):
                self.movement_state = MovementState.REACHED_NEXT_TILE

        elif self.movement_state == MovementState.REACHED_NEXT_TILE:
            self.current_tile_idx = self.next_tile_idx
            self.position = tile_center(self.current_tile_idx)
            if self.current_tile_idx == self.target_tile_idx:
                self.movement_state = MovementState.REACHED_TARGET_TILE
            else:
                self.movement_state = MovementState.CHECK_MOVE

        elif self.movement_state == MovementState.REACHED_TARGET_TILE:
            self.target_tile_idx = None
            self.movement_state = MovementState.IDLE

        elif self.movement_state == MovementState.BLOCKED:
            self.target_tile_idx = None
            self.next_tile_idx = self.current_tile_idx
            self.movement_state = MovementState.IDLE

        else:
            raise RuntimeError("Invalid movement state")

    def animate(self, time_delta_in_secs: float) -> None:
        if self.movement_state == MovementState.MOVE:
            self.__move_to_next_tile(time_delta_in_secs)

    def render(self) -> None:
        screen = pygame.display.get_surface()
        hero_rect = self.surface.get_rect(center=self.position)
        screen.blit(self.surface, hero_rect)

        if DEBUG_RENDER_CHARACTER_TILES:
            if self.target_tile_idx:
                self.__render_tile_cursor(self.target_tile_idx, "red")
            self.__render_tile_cursor(self.next_tile_idx, "green")
            self.__render_tile_cursor(self.current_tile_idx, "blue")

    def __set_next_tile_towards_target(self) -> None:
        if self.target_tile_idx:
            self.next_tile_idx = self.current_tile_idx
            dist_to_target_in_tiles = self.target_tile_idx - self.current_tile_idx

            if abs(dist_to_target_in_tiles.x) > abs(dist_to_target_in_tiles.y):
                if dist_to_target_in_tiles.x > 0:
                    self.next_tile_idx = self.current_tile_idx + pygame.Vector2(1, 0)
                elif dist_to_target_in_tiles.x < 0:
                    self.next_tile_idx = self.current_tile_idx - pygame.Vector2(1, 0)
            else:
                if dist_to_target_in_tiles.y < 0:
                    self.next_tile_idx = self.current_tile_idx - pygame.Vector2(0, 1)
                elif dist_to_target_in_tiles.y > 0:
                    self.next_tile_idx = self.current_tile_idx + pygame.Vector2(0, 1)

    def __can_move_to_next_tile(self) -> bool:
        if self.game:
            object_in_next_tile = self.game.object_at(self.next_tile_idx)
            return object_in_next_tile == GameObjectType.FLOOR

        return True

    def __move_to_next_tile(self, time_delta_in_secs: float) -> None:
        delta = self.next_tile_idx - self.current_tile_idx
        self.position += delta * HERO_SPEED * time_delta_in_secs

    def __has_reached_tile(self, tile_idx: pygame.Vector2 | tuple[int, int]) -> bool:
        hero_top_left = self.position - pygame.Vector2(TILE_RADIUS, TILE_RADIUS)
        squared_dist_to_tile = hero_top_left.distance_squared_to(
            tile_top_left(tile_idx)
        )
        return (
            squared_dist_to_tile
            <= CHARACTER_DISTANCE_TO_TILE_EPSILON * CHARACTER_DISTANCE_TO_TILE_EPSILON
        )

    def __render_tile_cursor(
        self, tile_idx: pygame.Vector2 | tuple[int, int], color: str
    ) -> None:
        tile_cursor = TileCursor()
        tile_cursor.color = color
        tile_cursor.position = tile_center(tile_idx)
        tile_cursor.animate()
        tile_cursor.render()


class Hero(Character):
    def __init__(self, tile_idx: str) -> None:
        super().__init__(tile_idx)
        self.stance_state = StanceState.NORMAL
        self.target_enemy: Enemy | None = None


class Enemy(Character):
    pass
