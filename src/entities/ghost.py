from __future__ import annotations
import time
from typing import Literal
from src.entities.entity import Entity
from src.entities.ghost_behaviors import choose_direction
from src.ui.theme import load_sprite
import pygame

GhostState = Literal["chasing", "edible", "eaten"]


class Ghost(Entity):
    def __init__(
        self,
        x: int,
        y: int,
        home: tuple[int, int],
        name: str,
        ID: int,
        move_frames: int = 15,
    ) -> None:
        super().__init__(x, y, move_frames)
        self.id: int = ID
        self.home: tuple[int, int] = home
        self.state: GhostState = "chasing"
        self.eaten_at: float = 0.0
        self.name: str = name
        self._frightened_timer: float = 0.0

    def make_edible(self, duration: float = 8.0) -> None:
        if self.state != "eaten":
            self.state = "edible"
            self._frightened_timer = time.time() + duration

    def get_eaten(self) -> None:
        self.state = "eaten"
        self.teleport(self.home[0], self.home[1])
        self.eaten_at = time.time()

    def update(self, respawn_delay: float = 5.0) -> None:
        if self.state == "edible" and time.time() >= self._frightened_timer:
            self.state = "chasing"
        if (self.state == "eaten" and
                time.time() - self.eaten_at >= respawn_delay):
            self.respawn()

    def respawn(self) -> None:
        self.teleport(self.home[0], self.home[1])
        self.state = "chasing"
        self.direction = None

    def is_edible(self) -> bool:
        return self.state == "edible"

    def is_eaten(self) -> bool:
        return self.state == "eaten"

    def is_chasing(self) -> bool:
        return self.state == "chasing"

    def act(self, maze: list[list[dict[str, bool]]]) -> bool:
        """Move one cell in the current direction if possible and not busy."""
        if self.direction is not None:
            return self.move(maze, self.direction)
        return False

    def draw(
        self,
        surface: "pygame.Surface",
        board_x: int,
        board_y: int,
        cell_size: int,
    ) -> None:
        """Draw the ghost at its smoothly interpolated pixel position."""
        cx = board_x + self.render_x * cell_size + cell_size // 2
        cy = board_y + self.render_y * cell_size + cell_size // 2

        if self.state == "eaten":
            self.update()
            return

        sprite_name = self.name
        if self.state == "edible":
            sprite_name = "ghost_blue"

        sprite = load_sprite(sprite_name, cell_size)
        rect = sprite.get_rect(center=(cx, cy))
        surface.blit(sprite, rect)

    def think(
        self,
        maze: list[list[dict[str, bool]]],
        player_x: int,
        player_y: int,
        player_dir: str,
        blinky_x: int = 0,
        blinky_y: int = 0,
        scatter: bool = False,
    ) -> None:
        d = choose_direction(
            self, maze, player_x, player_y, player_dir,
            blinky_x, blinky_y, scatter,
        )
        if d is not None:
            self.direction = d
