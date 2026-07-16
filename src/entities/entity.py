"""Base Entity with grid position and smooth pixel interpolation.

Every entity lives on an integer grid (x, y) but is rendered at a
smoothly interpolated pixel position (render_x, render_y) that glides
from one cell to the next over *move_frames* ticks.  While the entity
is mid-move it is "busy" and cannot start a second move until it
arrives.
"""


class Entity:
    def __init__(
        self,
        x: int,
        y: int,
        move_frames: int = 8,
    ) -> None:
        self.x: int = x
        self.y: int = y
        self.direction: str | None = None

        # Smooth movement state
        self.move_frames: int = move_frames
        self._move_timer: int = 0
        self._from_x: float = float(x)
        self._from_y: float = float(y)
        self._to_x: float = float(x)
        self._to_y: float = float(y)
        self.render_x: float = float(x)
        self.render_y: float = float(y)

    # -- grid helpers --------------------------------------------------------

    def can_move(self, maze: list, direction: str) -> bool:
        return not maze[self.y][self.x][direction]

    def move(self, maze: list, direction: str) -> bool:
        """Start a move in *direction* if possible and not already moving.

        Returns True if the move was started.
        """
        if self._move_timer > 0:
            return False
        if not self.can_move(maze, direction):
            return False

        self._from_x = float(self.x)
        self._from_y = float(self.y)

        if direction == "north":
            self.y -= 1
        elif direction == "east":
            self.x += 1
        elif direction == "west":
            self.x -= 1
        elif direction == "south":
            self.y += 1

        self._to_x = float(self.x)
        self._to_y = float(self.y)
        self._move_timer = self.move_frames
        self.direction = direction
        return True

    # -- smooth interpolation ------------------------------------------------

    @property
    def is_moving(self) -> bool:
        return self._move_timer > 0

    def update_render(self) -> None:
        """Advance the render position one step toward the target cell."""
        if self._move_timer > 0:
            self._move_timer -= 1
            t = 1.0 - (self._move_timer / self.move_frames)
            self.render_x = self._from_x + (self._to_x - self._from_x) * t
            self.render_y = self._from_y + (self._to_y - self._from_y) * t
        else:
            self.render_x = float(self.x)
            self.render_y = float(self.y)

    def teleport(self, x: int, y: int) -> None:
        """Instantly move to (x, y) with no interpolation."""
        self.x = x
        self.y = y
        self._move_timer = 0
        self._from_x = float(x)
        self._from_y = float(y)
        self._to_x = float(x)
        self._to_y = float(y)
        self.render_x = float(x)
        self.render_y = float(y)
