import enum
import pygame

from utils import *


class GameState(enum.Enum):
    START_DISPLAY_MENU = enum.auto()
    DISPLAY_MENU = enum.auto()
    START_PLAY = enum.auto()
    PLAY = enum.auto()
    DISPLAY_GAME_OVER = enum.auto()


class GameObjectType(enum.StrEnum):
    FLOOR = "   "
    OBSTACLE = "X"
    HERO = "H"
    MONSTER = "M"
    CLOSED_DOOR = "C"
    OPEN_DOOR = "O"


class Game:
    def __init__(self, map_size_in_tiles: tuple[int, int]) -> None:
        self.state = GameState.START_DISPLAY_MENU

        self.title_font = pygame.font.Font(None, 80)
        self.menu_font = pygame.font.Font(None, 40)

        self.map_width_in_tiles, self.map_height_in_tiles = map_size_in_tiles
        self.map = [
            [GameObjectType.FLOOR] * self.map_width_in_tiles
            for _ in range(self.map_height_in_tiles)
        ]

        self.level = 1

        self.door_left_tile_idx = pygame.Vector2(7.0, 1.0)
        self.door_right_tile_idx = pygame.Vector2(8.0, 1.0)

        self.background_music = pygame.mixer.Sound(MUSIC_PATH / "dungeon-maze.mp3")

    def object_at(self, tile_idx: pygame.Vector2 | tuple[int, int]) -> GameObjectType:
        return self.map[int(tile_idx[1])][int(tile_idx[0])]

    def render_map(self) -> None:
        # Cache text surfaces
        object_type_text_surfs = {
            object_type: render_text(str(object_type)) for object_type in GameObjectType
        }

        # Blit the cached text surfaces on screen, instead of calling debug on each iteration
        # (used to incur in a huge performance loss)
        screen = pygame.display.get_surface()
        for j, tile_row in enumerate(self.map):
            for i, element_type in enumerate(tile_row):
                text_surf = object_type_text_surfs[element_type]
                text_rect = text_surf.get_rect(topleft=tile_top_left((i, j)))
                screen.blit(text_surf, text_rect)
