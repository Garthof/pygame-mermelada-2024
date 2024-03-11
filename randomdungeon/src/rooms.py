import enum
import pygame
import random

from actors import *
from game import *
from globals import *
from utils import *


class TileType(enum.Enum):
    FLOOR = enum.auto()
    WALL = enum.auto()


class Room:
    def __init__(self, game: Game) -> None:
        self.game = game
        self.tile_surfs: dict[str, pygame.Surface] = {}
        self.__load_tiles()

        self.map_width_in_tiles, self.map_height_in_tiles = window_size_in_tiles()
        self.tile_map, self.room_map = self.__generate_maps()

        self.hero = Hero()
        self.hero.game = self.game
        self.hero.current_tile_idx = pygame.Vector2(
            window_size_in_tiles()[0] // 2, window_size_in_tiles()[1] // 2
        )
        self.hero.next_tile_idx = self.hero.current_tile_idx
        self.hero.position = tile_center(self.hero.current_tile_idx)
        self.hero.collision_box.center = self.hero.position  # type: ignore

        self.hero_attack_countdown_in_secs = 0.0

        self.enemy = Enemy(ENEMY_CRAB_TILE_FILE_IDX)
        self.enemy.game = self.game
        self.enemy.current_tile_idx = pygame.Vector2(12, 3)
        self.enemy.next_tile_idx = self.enemy.current_tile_idx
        self.enemy.position = tile_center(self.enemy.current_tile_idx)
        self.enemy.collision_box.center = self.enemy.position  # type: ignore

        self.enemies = [self.enemy]

        self.fireball: Fireball | None = None

        self.mouse_tile_cursor = TileCursor()
        self.mouse_tile_cursor.color = "white"
        self.mouse_tile_cursor.thickness = 5

    def __load_tiles(self) -> None:
        self.tile_surfs["wall_parapet_top"] = load_tile("0026")
        self.tile_surfs["wall_parapet_bottom"] = load_tile("0002")

        self.tile_surfs["wall_parapet_top_left"] = load_tile("0004")
        self.tile_surfs["wall_parapet_top_right"] = load_tile("0005")
        self.tile_surfs["wall_parapet_bottom_left"] = load_tile("0016")
        self.tile_surfs["wall_parapet_bottom_right"] = load_tile("0017")

        self.tile_surfs["wall_parapet_top_left_corner"] = load_tile("0027")
        self.tile_surfs["wall_parapet_top_right_corner"] = load_tile("0025")
        self.tile_surfs["wall_parapet_bottom_left_corner"] = load_tile("0003")
        self.tile_surfs["wall_parapet_bottom_right_corner"] = load_tile("0001")

        self.tile_surfs["wall_front"] = load_tile("0014")
        self.tile_surfs["wall_left"] = load_tile("0013")
        self.tile_surfs["wall_right"] = load_tile("0015")

        self.tile_surfs["floor"] = load_tile("0048")

        self.tile_surfs["corridor_left"] = load_tile("0010")
        self.tile_surfs["corridor_right"] = load_tile("0011")

    def __generate_maps(
        self,
    ) -> tuple[list[list[pygame.Surface | None]], list[list[TileType | None]]]:
        tile_map: list[list[pygame.Surface | None]] = [
            [None] * self.map_width_in_tiles for _ in range(self.map_height_in_tiles)
        ]
        room_map: list[list[TileType | None]] = [
            [None] * self.map_width_in_tiles for _ in range(self.map_height_in_tiles)
        ]

        # Render floor
        for j in range(self.map_height_in_tiles):
            for i in range(self.map_width_in_tiles):
                tile_map[j][i] = self.tile_surfs["floor"]
                room_map[j][i] = TileType.FLOOR

        # Render walls
        for j in range(self.map_height_in_tiles):
            for i in range(self.map_width_in_tiles):
                if j == 0:
                    if i == 0:
                        tile_map[j][i] = self.tile_surfs[
                            "wall_parapet_bottom_right_corner"
                        ]
                        room_map[j][i] = TileType.WALL
                    elif i == self.map_width_in_tiles - 1:
                        tile_map[j][i] = self.tile_surfs[
                            "wall_parapet_bottom_left_corner"
                        ]
                        room_map[j][i] = TileType.WALL
                    else:
                        tile_map[j][i] = self.tile_surfs["wall_parapet_bottom"]
                        room_map[j][i] = TileType.WALL

                elif j == 1:
                    if i == 0:
                        tile_map[j][i] = self.tile_surfs["wall_left"]
                        room_map[j][i] = TileType.WALL
                    elif i == self.map_width_in_tiles - 1:
                        tile_map[j][i] = self.tile_surfs["wall_right"]
                        room_map[j][i] = TileType.WALL
                    else:
                        tile_map[j][i] = self.tile_surfs["wall_front"]
                        room_map[j][i] = TileType.WALL

                elif j == self.map_height_in_tiles - 1:
                    if i == 0:
                        tile_map[j][i] = self.tile_surfs[
                            "wall_parapet_top_right_corner"
                        ]
                        room_map[j][i] = TileType.WALL
                    elif i == self.map_width_in_tiles - 1:
                        tile_map[j][i] = self.tile_surfs["wall_parapet_top_left_corner"]
                        room_map[j][i] = TileType.WALL
                    else:
                        tile_map[j][i] = self.tile_surfs["wall_parapet_top"]
                        room_map[j][i] = TileType.WALL

                elif i == 0:
                    tile_map[j][i] = self.tile_surfs["wall_left"]
                    room_map[j][i] = TileType.WALL
                elif i == self.map_width_in_tiles - 1:
                    tile_map[j][i] = self.tile_surfs["wall_right"]
                    room_map[j][i] = TileType.WALL

        # Render exits
        horizontal_exit_left_i = self.map_width_in_tiles // 2 - 1
        tile_map[1][horizontal_exit_left_i] = self.tile_surfs["corridor_left"]
        tile_map[1][horizontal_exit_left_i + 1] = self.tile_surfs["corridor_right"]

        vertical_exit_top_j = self.map_height_in_tiles // 2 - 2
        tile_map[vertical_exit_top_j][0] = self.tile_surfs["wall_parapet_bottom_right"]
        tile_map[vertical_exit_top_j + 1][0] = self.tile_surfs["wall_front"]
        tile_map[vertical_exit_top_j + 2][0] = self.tile_surfs["floor"]
        room_map[vertical_exit_top_j + 2][0] = TileType.FLOOR
        tile_map[vertical_exit_top_j + 3][0] = self.tile_surfs["wall_parapet_top_right"]

        tile_map[vertical_exit_top_j][self.map_width_in_tiles - 1] = self.tile_surfs[
            "wall_parapet_bottom_left"
        ]
        tile_map[vertical_exit_top_j + 1][self.map_width_in_tiles - 1] = (
            self.tile_surfs["wall_front"]
        )
        tile_map[vertical_exit_top_j + 2][self.map_width_in_tiles - 1] = (
            self.tile_surfs["floor"]
        )
        room_map[vertical_exit_top_j + 2][self.map_width_in_tiles - 1] = TileType.FLOOR
        tile_map[vertical_exit_top_j + 3][self.map_width_in_tiles - 1] = (
            self.tile_surfs["wall_parapet_top_left"]
        )

        tile_map[self.map_height_in_tiles - 1][horizontal_exit_left_i - 1] = (
            self.tile_surfs["wall_parapet_top_right"]
        )
        tile_map[self.map_height_in_tiles - 1][horizontal_exit_left_i] = (
            self.tile_surfs["floor"]
        )
        tile_map[self.map_height_in_tiles - 1][horizontal_exit_left_i + 1] = (
            self.tile_surfs["floor"]
        )
        room_map[self.map_height_in_tiles - 1][horizontal_exit_left_i] = TileType.FLOOR
        room_map[self.map_height_in_tiles - 1][
            horizontal_exit_left_i + 1
        ] = TileType.FLOOR
        tile_map[self.map_height_in_tiles - 1][horizontal_exit_left_i + 2] = (
            self.tile_surfs["wall_parapet_top_left"]
        )

        return tile_map, room_map

    def enter(self) -> None:
        self.game.background_music = pygame.mixer.Sound(MUSIC_PATH / "dungeon-maze.mp3")
        self.game.background_music.play(-1, 0, 5000)
        self.game.background_music.set_volume(0.5)

        self.enemy_walk_event = pygame.USEREVENT
        pygame.time.set_timer(self.enemy_walk_event, 2500)

    def exit(self) -> None:
        if self.game.background_music:
            self.game.background_music.stop()
            self.game.background_music = None

    def read_events(self, events: list[pygame.event.Event]) -> None:
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pressed_buttons = pygame.mouse.get_pressed()
                if pressed_buttons[0]:
                    pressed_tile = tile_idx(pygame.mouse.get_pos())
                    if is_valid_tile(pressed_tile):
                        if enemy := self.__enemy_on_tile(pressed_tile):
                            if not self.fireball:
                                self.__shoot_fireball(enemy)
                        else:
                            self.hero.target_tile_idx = pressed_tile

            if event.type == self.enemy_walk_event:
                for enemy in self.enemies:
                    enemy.target_tile_idx = pygame.Vector2(-1, -1)
                    while not is_valid_tile(enemy.target_tile_idx):
                        enemy.target_tile_idx = enemy.current_tile_idx + pygame.Vector2(
                            random.randint(-5, 5), 0
                        )

        hover_mouse_position = pygame.mouse.get_pos()
        self.mouse_tile_cursor.position = pygame.Vector2(hover_mouse_position)

    def __enemy_on_tile(self, tile_idx: pygame.Vector2) -> Enemy | None:
        for enemy in self.enemies:
            if are_same_tile(enemy.current_tile_idx, tile_idx):
                return enemy
        return None

    def __shoot_fireball(self, enemy: Enemy):
        self.fireball = Fireball()
        self.fireball.direction = (enemy.position - self.hero.position).normalize()
        self.fireball.position = (
            self.hero.position + self.fireball.direction * TILE_RADIUS
        )

    def update(self, time_delta_in_secs) -> None:
        self.__update_game_map()

        self.hero.update(time_delta_in_secs)
        for enemy in self.enemies:
            enemy.update(time_delta_in_secs)

        if self.fireball:
            if not is_valid_position(self.fireball.position):
                self.fireball = None
            if hit_enemy := self.__fireball_collision():
                hit_enemy.life_points -= 1
                self.fireball = None

        self.enemies = [enemy for enemy in self.enemies if enemy.life_points > 0]

    def __update_game_map(self) -> None:
        self.game.map = [
            [
                (
                    GameObjectType.FLOOR
                    if tile == TileType.FLOOR
                    else GameObjectType.OBSTACLE
                )
                for tile in tile_row
            ]
            for tile_row in self.room_map
        ]

        self.game.map[int(self.hero.current_tile_idx.y)][
            int(self.hero.current_tile_idx.x)
        ] = GameObjectType.HERO

        for enemy in self.enemies:
            self.game.map[int(enemy.current_tile_idx.y)][
                int(enemy.current_tile_idx.x)
            ] = GameObjectType.ENEMY

    def __fireball_collision(self) -> Enemy | None:
        if self.fireball:
            for enemy in self.enemies:
                if enemy.collision_box.colliderect(self.fireball.collision_box):
                    return enemy
        return None

    def animate(self, time_delta_in_secs: float) -> None:
        self.hero.animate(time_delta_in_secs)
        for enemy in self.enemies:
            enemy.animate(time_delta_in_secs)
        if self.fireball:
            self.fireball.animate(time_delta_in_secs)
        self.mouse_tile_cursor.animate()

    def render(self) -> None:
        self.__render_tile_map()

        for enemy in self.enemies:
            enemy.render()

        self.hero.render()

        if self.fireball:
            self.fireball.render()

        self.mouse_tile_cursor.render()

    def __render_tile_map(self) -> None:
        screen = pygame.display.get_surface()

        for j, tile_row in enumerate(self.tile_map):
            for i, tile_surf in enumerate(tile_row):
                if tile_surf:
                    tile_rect = tile_surf.get_rect(topleft=tile_top_left((i, j)))
                    screen.blit(tile_surf, tile_rect)

                if DEBUG_RENDER_TILE_BORDERS:
                    pygame.draw.rect(screen, "black", tile_rect, 1)
