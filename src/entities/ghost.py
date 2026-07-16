"""Ghost entity with AI-driven movement and sprite rendering.

Each ghost has a personality (id 0-3) that determines its chase
target via ghost_behaviors.choose_direction().  The ghost decides
a direction each tick (think) then moves one cell (act).

Movement is smoothly interpolated between grid cells by the base
Entity class.  Rendering uses the theme's sprite loader; when a
sprite can't be loaded, a coloured circle is drawn as a fallback.
"""

from __future__ import annotations

import time
from typing import Literal

import pygame

from src.entities.entity import Entity
from src.entities.ghost_behaviors import choose_direction
from src.ui.theme import GHOST_COLORS, GHOST_EDIBLE, load_sprite

GhostState = Literal["chasing", "edible", "eaten"]

GHOST_NAMES: dict[int, str] = {
    0: "Blinky",
    1: "Pinky",
    2: "Inky",
    3: "Clyde",
}


class Ghost(Entity):
    def __init__(
        self,
        name: str,
        x: int,
        y: int,
        home: tuple[int, int],
        img: str,
        ID: int,
        move_frames: int = 8,
    ) -> None:
        super().__init__(x, y, move_frames)
        self.name: str = name
        self.id: int = ID
        self.home: tuple[int, int] = home
        self.state: GhostState = "chasing"
        self.eaten_at: float = 0.0
        self.img = img
        self._frightened_timer: float = 0.0

    # -- state transitions ---------------------------------------------------

    def make_edible(self, duration: float = 8.0) -> None:
        if self.state != "eaten":
            self.state = "edible"
            self._frightened_timer = time.time() + duration

    def get_eaten(self) -> None:
        self.state = "eaten"
        self.eaten_at = time.time()

    def update(self, respawn_delay: float = 5.0) -> None:
        if self.state == "edible" and time.time() >= self._frightened_timer:
            self.state = "chasing"
        if self.state == "eaten" and time.time() - self.eaten_at >= respawn_delay:
            self.respawn()

    def respawn(self) -> None:
        self.teleport(self.home[0], self.home[1])
        self.state = "chasing"
        self.direction = None

    # -- queries -------------------------------------------------------------

    def is_edible(self) -> bool:
        return self.state == "edible"

    def is_eaten(self) -> bool:
        return self.state == "eaten"

    def is_chasing(self) -> bool:
        return self.state == "chasing"

    # -- AI ------------------------------------------------------------------

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

    def act(self, maze: list[list[dict[str, bool]]]) -> bool:
        """Move one cell in the current direction if possible and not busy."""
        if self.direction is not None:
            return self.move(maze, self.direction)
        return False

    # -- rendering -----------------------------------------------------------

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
        radius = cell_size // 2

        if self.state == "eaten":
            self._draw_eyes(surface, cx, cy, radius)
            return

        sprite_name = self.img
        if self.state == "edible":
            sprite_name = "ghost_blue"

        sprite = load_sprite(sprite_name, cell_size)
        if sprite is not None:
            rect = sprite.get_rect(center=(cx, cy))
            surface.blit(sprite, rect)
        else:
            color = GHOST_COLORS[self.id % len(GHOST_COLORS)]
            if self.state == "edible":
                color = GHOST_EDIBLE
            pygame.draw.circle(surface, color, (cx, cy), radius)

    def _draw_eyes(
        self,
        surface: "pygame.Surface",
        cx: float,
        cy: float,
        radius: int,
    ) -> None:
        eye_r = max(2, radius // 3)
        pupil_r = max(1, eye_r // 2)
        spread = max(2, radius // 3)

        for side in (-1, 1):
            ex = cx + side * spread
            ey = cy - radius // 6
            pygame.draw.circle(surface, (255, 255, 255), (int(ex), int(ey)), eye_r)
            px, py = 0.0, 0.0
            if self.direction == "north":
                py = -pupil_r
            elif self.direction == "south":
                py = pupil_r
            elif self.direction == "east":
                px = pupil_r
            elif self.direction == "west":
                px = -pupil_r
            pygame.draw.circle(
                surface, (33, 33, 222),
                (int(ex + px), int(ey + py)), pupil_r,
            )
