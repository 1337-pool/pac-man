from __future__ import annotations
import pygame
from src.entities.entity import Entity
from src.ui.theme import YELLOW, load_sprite

ANIM_SPEED = 8


class Player(Entity):
    """The player-controlled Pac-Man character."""

    def __init__(
        self,
        x: int,
        y: int,
        lives: int,
        move_frames: int = 15,
    ) -> None:
        """Initialize the Player."""
        super().__init__(x, y, move_frames)
        self.lives: int = lives
        self.score: int = 0
        self._anim_counter: int = 0
        self._mouth_open: bool = True

    def respawn(self, x: int, y: int) -> None:
        """Teleport the player to a new position and reset animation state."""
        self.teleport(x, y)
        self.direction = "east"
        self._anim_counter = 0
        self._mouth_open = True

    def is_alive(self) -> bool:
        """Check if the player has lives remaining."""
        return self.lives > 0

    def add_score(self, points: int) -> None:
        """Add points to the player's current score."""
        self.score += points

    def lose_life(self, middle: tuple[int, int]) -> None:
        """Decrement lives by 1 and respawn at
        the specified middle coordinate."""
        if self.lives >= 1:
            self.lives -= 1
            self.respawn(middle[0], middle[1])

    def draw(
        self,
        surface: pygame.Surface,
        board_x: int,
        board_y: int,
        cell_size: int
    ) -> None:
        """Draw the player, alternating between sprite and closed circle."""
        cx = board_x + self.render_x * cell_size + cell_size // 2
        cy = board_y + self.render_y * cell_size + cell_size // 2
        radius = cell_size // 2 - 1

        self._anim_counter += 1
        if self._anim_counter >= ANIM_SPEED:
            self._mouth_open = not self._mouth_open
            self._anim_counter = 0

        if self._mouth_open:
            sprite = load_sprite("pacman", cell_size)
            angle = 0
            if self.direction == "north":
                angle = 90
            elif self.direction == "west":
                angle = 180
            elif self.direction == "south":
                angle = 270

            rotated_sprite = pygame.transform.rotate(sprite, angle)
            rect = rotated_sprite.get_rect(center=(int(cx), int(cy)))
            surface.blit(rotated_sprite, rect)

        else:
            pygame.draw.circle(surface, YELLOW, (int(cx), int(cy)), radius)
