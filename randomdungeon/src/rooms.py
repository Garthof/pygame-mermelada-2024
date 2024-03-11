import enum
import pygame
import random

from pygame.event import Event

from actors import *
from game import *
from globals import *
from utils import *


class TileType(enum.Enum):
    FLOOR = enum.auto()
    WALL = enum.auto()
    CLOSED_DOOR = enum.auto()
    OPEN_DOOR = enum.auto()


class Room:
    def __init__(self, game: Game) -> None:
        self.game = game

    def enter(self) -> None:
        pass

    def exit(self) -> None:
        pass

    def read_events(self, events: list[pygame.event.Event]) -> None:
        pass

    def update(self, time_delta_in_secs: float) -> None:
        pass

    def animate(self, time_delta_in_secs: float) -> None:
        pass

    def render(self) -> None:
        pass


class DungeonRoom(Room):
    def __init__(self, game: Game) -> None:
        super().__init__(game)

        self.are_open_doors = False

        self.tile_surfs: dict[str, pygame.Surface] = {}
        self.__load_tiles()

        self.map_width_in_tiles, self.map_height_in_tiles = window_size_in_tiles()
        self.tile_map, self.room_map = self.__generate_maps()

        self.hero = Hero(self.game)

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

        self.tile_surfs["door_closed_left"] = load_tile("0046")
        self.tile_surfs["door_closed_right"] = load_tile("0047")
        self.tile_surfs["door_open_left"] = load_tile("0034")
        self.tile_surfs["door_open_right"] = load_tile("0035")

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

        # vertical_exit_top_j = self.map_height_in_tiles // 2 - 2
        # tile_map[vertical_exit_top_j][0] = self.tile_surfs["wall_parapet_bottom_right"]
        # tile_map[vertical_exit_top_j + 1][0] = self.tile_surfs["wall_front"]
        # tile_map[vertical_exit_top_j + 2][0] = self.tile_surfs["floor"]
        # room_map[vertical_exit_top_j + 2][0] = TileType.FLOOR
        # tile_map[vertical_exit_top_j + 3][0] = self.tile_surfs["wall_parapet_top_right"]

        # tile_map[vertical_exit_top_j][self.map_width_in_tiles - 1] = self.tile_surfs[
        #     "wall_parapet_bottom_left"
        # ]
        # tile_map[vertical_exit_top_j + 1][self.map_width_in_tiles - 1] = (
        #     self.tile_surfs["wall_front"]
        # )
        # tile_map[vertical_exit_top_j + 2][self.map_width_in_tiles - 1] = (
        #     self.tile_surfs["floor"]
        # )
        # room_map[vertical_exit_top_j + 2][self.map_width_in_tiles - 1] = TileType.FLOOR
        # tile_map[vertical_exit_top_j + 3][self.map_width_in_tiles - 1] = (
        #     self.tile_surfs["wall_parapet_top_left"]
        # )

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
        self.hero.next_tile_idx = self.hero.current_tile_idx
        self.hero.position = tile_center(self.hero.current_tile_idx)
        self.hero.collision_box.center = self.hero.position  # type: ignore

        self.hero_attack_countdown_in_secs = 0.0

    def read_events(self, events: list[pygame.event.Event]) -> None:
        super().read_events(events)
        hover_mouse_position = pygame.mouse.get_pos()
        self.mouse_tile_cursor.position = pygame.Vector2(hover_mouse_position)

    def update(self, time_delta_in_secs: float) -> None:
        super().update(time_delta_in_secs)

        self.__update_doors()
        self._update_game_map()

        self.hero.update(time_delta_in_secs)

        if self.fireball:
            if (
                not is_valid_position(self.fireball.position)
                or self.__fireball_collision_obstacle()
            ):
                self.fireball = None

    def __update_doors(self) -> None:
        if self.are_open_doors:
            door_left_tile_surf = self.tile_surfs["door_open_left"]
            door_right_tile_surf = self.tile_surfs["door_open_right"]
            door_tile_type = TileType.OPEN_DOOR
        else:
            door_left_tile_surf = self.tile_surfs["door_closed_left"]
            door_right_tile_surf = self.tile_surfs["door_closed_right"]
            door_tile_type = TileType.CLOSED_DOOR

        self.tile_map[int(self.game.door_left_tile_idx[1])][
            int(self.game.door_left_tile_idx[0])
        ] = door_left_tile_surf
        self.room_map[int(self.game.door_left_tile_idx[1])][
            int(self.game.door_left_tile_idx[0])
        ] = door_tile_type

        self.tile_map[int(self.game.door_right_tile_idx[1])][
            int(self.game.door_right_tile_idx[0])
        ] = door_right_tile_surf
        self.room_map[int(self.game.door_right_tile_idx[1])][
            int(self.game.door_right_tile_idx[0])
        ] = door_tile_type

    def _update_game_map(self) -> None:
        for j, tile_row in enumerate(self.room_map):
            for i, tile in enumerate(tile_row):
                match tile:
                    case TileType.FLOOR:
                        object_type = GameObjectType.FLOOR
                    case TileType.OPEN_DOOR:
                        object_type = GameObjectType.OPEN_DOOR
                    case _:
                        object_type = GameObjectType.OBSTACLE
                self.game.map[j][i] = object_type

        self.game.map[int(self.hero.current_tile_idx.y)][
            int(self.hero.current_tile_idx.x)
        ] = GameObjectType.HERO

    def __fireball_collision_obstacle(self) -> bool:
        if self.fireball:
            fireball_tile = tile_idx(self.fireball.position)
            return self.game.object_at(fireball_tile) == GameObjectType.OBSTACLE
        return False

    def animate(self, time_delta_in_secs: float) -> None:
        super().animate(time_delta_in_secs)

        self.hero.animate(time_delta_in_secs)
        if self.fireball:
            self.fireball.animate(time_delta_in_secs)
        self.mouse_tile_cursor.animate()

    def render(self) -> None:
        super().render()

        self.__render_tile_map()

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


class MonsterRoom(DungeonRoom):
    def __init__(self, game: Game, num_monsters: int) -> None:
        super().__init__(game)

        self.monsters: list[Monster] = []
        self.__generate_monsters(num_monsters)

        self.lasers: list[Laser] = []
        self.laser_countdown_in_secs = 5.0

    def __generate_monsters(self, num_monsters):
        super()._update_game_map()

        for _ in range(num_monsters):
            monster = MonsterCrab(self.game)
            monster.current_tile_idx = self.__random_empty_floor_tile()
            monster.next_tile_idx = monster.current_tile_idx
            monster.position = tile_center(monster.current_tile_idx)
            monster.collision_box.center = monster.position
            self.monsters.append(monster)

            self.game.map[int(monster.current_tile_idx.y)][
                int(monster.current_tile_idx.x)
            ] = GameObjectType.MONSTER

    def __random_empty_floor_tile(self):
        tile_idx = pygame.Vector2(-1.0, -1.0)
        while not (
            is_valid_tile(tile_idx)
            and self.game.object_at(tile_idx) == GameObjectType.FLOOR
        ):
            tile_idx = pygame.Vector2(
                random.randint(1, 14),
                random.randint(2, 10),
            )
        return tile_idx

    def read_events(self, events: list[pygame.event.Event]) -> None:
        super().read_events(events)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pressed_buttons = pygame.mouse.get_pressed()
                if pressed_buttons[0]:
                    pressed_tile = tile_idx(pygame.mouse.get_pos())
                    if is_valid_tile(pressed_tile):
                        if monster := self.__monster_on_tile(pressed_tile):
                            if not self.fireball:
                                self.__shoot_fireball(monster)
                        else:
                            self.hero.target_tile_idx = pressed_tile

    def __monster_on_tile(self, tile_idx: pygame.Vector2) -> Monster | None:
        for monster in self.monsters:
            if are_same_tile(monster.current_tile_idx, tile_idx):
                return monster
        return None

    def __shoot_fireball(self, monster: Monster):
        self.fireball = Fireball()
        self.fireball.direction = (monster.position - self.hero.position).normalize()
        self.fireball.position = (
            self.hero.position + self.fireball.direction * TILE_RADIUS
        )

    def update(self, time_delta_in_secs: float) -> None:
        super().update(time_delta_in_secs)

        if self.fireball:
            if hit_monster := self.__fireball_collision__monster():
                hit_monster.life_points -= 1
                self.fireball = None

        self.monsters = [
            monster for monster in self.monsters if monster.life_points > 0
        ]
        self.are_open_doors = len(self.monsters) == 0
        for monster in self.monsters:
            monster.update(time_delta_in_secs)
            if (
                monster.state == CharacterState.MOVE
                and self.laser_countdown_in_secs < -0.0
                and random.random() < 0.1
            ):
                self.__shoot_laser(monster)
                self.laser_countdown_in_secs = 5.0 + random.uniform(-2.0, +2.0)

        self.lasers = [
            laser
            for laser in self.lasers
            if is_valid_tile(tile_idx(laser.position))
            and not self.__laser_collision_obstacle(laser)
        ]

        self.laser_countdown_in_secs -= time_delta_in_secs

    def __shoot_laser(self, monster: Monster):
        direction = pygame.Vector2(monster.next_tile_idx) - pygame.Vector2(
            monster.current_tile_idx
        )
        if direction.magnitude_squared() > 0.1:
            laser = Laser()
            laser.direction = direction
            laser.position = monster.position + laser.direction * TILE_RADIUS
            laser.angle = direction.angle_to(pygame.Vector2(0.0, -1.0))

            self.lasers.append(laser)

    def __laser_collision_obstacle(self, laser: Laser) -> bool:
        laser_tile = tile_idx(laser.position)
        return self.game.object_at(laser_tile) == GameObjectType.OBSTACLE

    def _update_game_map(self) -> None:
        super()._update_game_map()

        for monster in self.monsters:
            self.game.map[int(monster.current_tile_idx.y)][
                int(monster.current_tile_idx.x)
            ] = GameObjectType.MONSTER

    def __fireball_collision__monster(self) -> Monster | None:
        if self.fireball:
            for monster in self.monsters:
                if monster.collision_box.colliderect(self.fireball.collision_box):
                    return monster
        return None

    def animate(self, time_delta_in_secs: float) -> None:
        super().animate(time_delta_in_secs)
        for monster in self.monsters:
            monster.animate(time_delta_in_secs)
        for laser in self.lasers:
            laser.animate(time_delta_in_secs)

    def render(self) -> None:
        super().render()
        for monster in self.monsters:
            monster.render()
        for laser in self.lasers:
            laser.render()


class MenuRoom(Room):
    def __init__(self, game: Game) -> None:
        super().__init__(game)

    def read_events(self, events: list[Event]) -> None:
        super().read_events(events)

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.game.state = GameState.START_PLAY

    def render(self) -> None:
        screen = pygame.display.get_surface()
        screen.fill(MENU_COLOR)
        self.__render_centered_text("Random Dungeon", 200, self.game.title_font)
        self.__render_centered_text(
            "Click to start", WINDOW_HEIGHT - 60, self.game.menu_font
        )

    def __render_centered_text(self, text: str, y_pos: int, font: pygame.font.Font):
        text_surf = render_text(text, font, "azure1", MENU_COLOR)
        text_rect = text_surf.get_rect(center=pygame.Vector2(WINDOW_WIDTH // 2, y_pos))
        screen = pygame.display.get_surface()
        screen.blit(text_surf, text_rect)
