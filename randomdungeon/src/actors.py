import enum
import pygame
import random

from game import *
from globals import *
from utils import *


class CharacterState(enum.Enum):
    IDLE = enum.auto()
    CHECK_MOVE = enum.auto()
    MOVE = enum.auto()
    REACHED_NEXT_TILE = enum.auto()
    REACHED_TARGET_TILE = enum.auto()
    BLOCKED = enum.auto()


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
    def __init__(self, game: Game, tile_idx: str) -> None:
        self.game = game
        self.surface = load_tile(tile_idx)
        self.position = pygame.Vector2()
        self.current_tile_idx = pygame.Vector2()
        self.target_tile_idx: pygame.Vector2 | None = None
        self.next_tile_idx = self.current_tile_idx
        self.movement_state = CharacterState.IDLE
        self.life_points = 1
        self.collision_box = self.surface.get_rect().scale_by(0.8, 0.8)

    def update(self, time_delta_in_secs: float) -> None:
        if self.movement_state == CharacterState.IDLE:
            if self.target_tile_idx:
                self.movement_state = CharacterState.CHECK_MOVE

        elif self.movement_state == CharacterState.CHECK_MOVE:
            self.__set_next_tile_towards_target()
            if self.__can_move_to_next_tile():
                self.movement_state = CharacterState.MOVE
            else:
                self.movement_state = CharacterState.BLOCKED

        elif self.movement_state == CharacterState.MOVE:
            if self.__has_reached_tile(self.next_tile_idx):
                self.movement_state = CharacterState.REACHED_NEXT_TILE

        elif self.movement_state == CharacterState.REACHED_NEXT_TILE:
            self.current_tile_idx = self.next_tile_idx
            self.position = tile_center(self.current_tile_idx)
            if self.current_tile_idx == self.target_tile_idx:
                self.movement_state = CharacterState.REACHED_TARGET_TILE
            else:
                self.movement_state = CharacterState.CHECK_MOVE

        elif self.movement_state == CharacterState.REACHED_TARGET_TILE:
            self.target_tile_idx = None
            self.movement_state = CharacterState.IDLE

        elif self.movement_state == CharacterState.BLOCKED:
            self.target_tile_idx = None
            self.next_tile_idx = self.current_tile_idx
            self.movement_state = CharacterState.IDLE

        else:
            raise RuntimeError("Invalid character state")

    def animate(self, time_delta_in_secs: float) -> None:
        if self.movement_state == CharacterState.MOVE:
            delta = (
                (self.next_tile_idx - self.current_tile_idx)
                * HERO_SPEED
                * time_delta_in_secs
            )
            self.position += delta
            self.collision_box.center = self.position  # type: ignore

    def render(self) -> None:
        screen = pygame.display.get_surface()
        character_rect = self.surface.get_rect(center=self.position)
        screen.blit(self.surface, character_rect)

        if DEBUG_RENDER_CHARACTER_TILES:
            if self.target_tile_idx:
                self.__render_tile_cursor(self.target_tile_idx, "red")
            self.__render_tile_cursor(self.next_tile_idx, "green")
            self.__render_tile_cursor(self.current_tile_idx, "blue")

        if DEBUG_RENDER_COLLISION_BOX:
            pygame.draw.rect(screen, "black", self.collision_box, 3)

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

    def __has_reached_tile(self, tile_idx: pygame.Vector2 | tuple[int, int]) -> bool:
        character_top_left = self.position - pygame.Vector2(TILE_RADIUS, TILE_RADIUS)
        squared_dist_to_tile = character_top_left.distance_squared_to(
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


class Monster(Character):
    def __init__(self, game: Game, tile_idx: str):
        super().__init__(game, tile_idx)
        self.life_points = 3
        self.countdown_in_secs = 5.0

    def update(self, delta_time_in_secs: float):
        super().update(delta_time_in_secs)

        self.countdown_in_secs -= delta_time_in_secs
        if self.countdown_in_secs <= 0:
            self.countdown_in_secs = 5.0
            self.trigger()

    def trigger(self):
        pass


class MonsterCrab(Monster):
    def __init__(self, game: Game):
        super().__init__(game, MONSTER_CRAB_TILE_FILE_IDX)

    def trigger(self):
        super().trigger()

        self.target_tile_idx = pygame.Vector2(-1, -1)
        while not is_valid_tile(self.target_tile_idx):
            direction = random.choice(
                [
                    pygame.Vector2(-1, 0),
                    pygame.Vector2(+1, 0),
                    pygame.Vector2(0, -1),
                    pygame.Vector2(0, +1),
                ]
            )
            distance = random.randint(1, 5)
            self.target_tile_idx = self.current_tile_idx + direction * distance

        self.countdown_in_secs += random.uniform(-2.0, +2.0)


class Hero(Character):
    def __init__(self, game: Game) -> None:
        super().__init__(game, HERO_TILE_FILE_IDX)
        self.weapon = Weapon()

    def animate(self, time_delta_in_secs: float) -> None:
        super().animate(time_delta_in_secs)
        self.weapon.position = self.position + WEAPON_POSITION_DELTA

    def render(self) -> None:
        super().render()
        self.weapon.render()


class Weapon:
    def __init__(self) -> None:
        self.surface = load_tile(WEAPON_TILE_FILE_IDX)
        self.surface = pygame.transform.rotozoom(
            self.surface, WEAPON_IDLE_ANGLE_IN_DEGREES, 1.0
        )
        self.position = pygame.Vector2()

    def render(self) -> None:
        screen = pygame.display.get_surface()
        weapon_rect = self.surface.get_rect(center=self.position)
        screen.blit(self.surface, weapon_rect)


class Fireball:
    def __init__(self) -> None:
        self.surface = load_tile(FIREBALL_TILE_FILE_IDX)
        self.rotated_surface = self.surface
        self.position = pygame.Vector2()
        self.direction = pygame.Vector2()
        self.angle = 0.0
        self.collision_box = self.surface.get_rect().scale_by(0.8, 0.8)

    def animate(self, time_delta_in_secs) -> None:
        self.angle += FIREBALL_ROTATION_SPEED * time_delta_in_secs
        if self.angle >= 90.0:
            self.angle = 0.0

        self.position += self.direction * FIREBALL_SPEED * time_delta_in_secs
        self.collision_box.center = self.position  # type: ignore

    def render(self) -> None:
        screen = pygame.display.get_surface()
        rotated_surface = pygame.transform.rotozoom(self.surface, self.angle, 0.8)
        surface_rect = rotated_surface.get_rect(center=self.position)
        screen.blit(rotated_surface, surface_rect)

        if DEBUG_RENDER_COLLISION_BOX:
            pygame.draw.rect(screen, "black", self.collision_box, 3)
