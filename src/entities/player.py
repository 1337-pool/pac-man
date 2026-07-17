"""Player entity with smooth movement and classic Pac-Man rendering.

Drawn as a bright yellow circle with a black pie-wedge mouth that
opens and closes while moving — faithful to the original 1980 arcade
character.  The mouth is rendered by drawing a full yellow circle
then overlaying a black filled wedge.
"""

from __future__ import annotations

import math

import pygame

from src.entities.entity import Entity
from src.ui.theme import BLACK, YELLOW

MOUTH_SPEED = 0.28
MOUTH_MAX = 0.38
MOUTH_MIN = 0.01

_DIR_RAD = {
    "east": 0.0,
    "north": math.pi / 2,
    "west": math.pi,
    "south": 3 * math.pi / 2,
}

_ARC_STEPS = 32


class Player(Entity):
    def __init__(
        self,
        x: int,
        y: int,
        lives: int,
        img: str,
        move_frames: int = 15,
    ) -> None:
        super().__init__(x, y, move_frames)
        self.lives: int = lives
        self.score: int = 0
        self.img: str = img
        self._mouth: float = MOUTH_MAX
        self._mouth_dir: int = -1

    def respawn(self, x: int, y: int) -> None:
        self.teleport(x, y)
        self.direction = "east"
        self._mouth = MOUTH_MAX
        self._mouth_dir = -1

    def is_alive(self) -> bool:
        return self.lives > 0

    def add_score(self, points: int) -> None:
        self.score += points

    def lose_life(self, middle: tuple[int, int]) -> None:
        if self.lives >= 1:
            self.lives -= 1
            self.respawn(middle[0], middle[1])

    # -- animation -----------------------------------------------------------

    def _tick_mouth(self) -> None:
        self._mouth += MOUTH_SPEED * self._mouth_dir
        if self._mouth >= MOUTH_MAX:
            self._mouth = MOUTH_MAX
            self._mouth_dir = -1
        elif self._mouth <= MOUTH_MIN:
            self._mouth = MOUTH_MIN
            self._mouth_dir = 1

    # -- rendering -----------------------------------------------------------

    def draw(
        self,
        surface: "pygame.Surface",
        board_x: int,
        board_y: int,
        cell_size: int,
    ) -> None:
        cx = board_x + self.render_x * cell_size + cell_size // 2
        cy = board_y + self.render_y * cell_size + cell_size // 2
        radius = cell_size // 2 - 1

        if self.is_moving:
            self._tick_mouth()
        else:
            self._mouth = 0.28

        mouth = self._mouth
        base = _DIR_RAD.get(self.direction or "east", 0.0)

        # Draw full yellow circle
        pygame.draw.circle(surface, YELLOW, (int(cx), int(cy)), radius)

        # Draw black wedge for mouth
        if mouth > 0.03:
            a_start = base - mouth
            a_end = base + mouth
            verts = [(cx, cy)]
            for i in range(_ARC_STEPS + 1):
                a = a_start + (a_end - a_start) * i / _ARC_STEPS
                verts.append((
                    cx + (radius + 1) * math.cos(a),
                    cy - (radius + 1) * math.sin(a),
                ))
            pygame.draw.polygon(surface, BLACK, verts)
