class Entity:
    def __init__(
        self,
        x: int,
        y: int,
        move_frames: int = 15,
    ) -> None:
        self.x: int = x
        self.y: int = y
        self.direction: str | None = None
        self.move_frames: int = move_frames
        self._move_timer: int = 0
        self.render_x: float = float(x)
        self.render_y: float = float(y)

    def can_move(self, maze: list[
            list[dict[str, bool]]], direction: str) -> bool:
        return not maze[self.y][self.x][direction]

    def move(self, maze: list[list[dict[str, bool]]], direction: str) -> bool:

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

        self._move_timer = self.move_frames
        self.direction = direction
        return True

    @property
    def is_moving(self) -> bool:
        return self._move_timer > 0

    def update_render(self) -> None:
        """Advance the render position one step toward the target cell."""
        if self._move_timer > 0:
            self._move_timer -= 1
            t = 1.0 - (self._move_timer / self.move_frames)
            self.render_x = float(self._from_x) + (self.x - self._from_x) * t
            self.render_y = float(self._from_y) + (self.y - self._from_y) * t
        else:
            self.render_x = float(self.x)
            self.render_y = float(self.y)

    def teleport(self, x: int, y: int) -> None:
        """instantly move to (x, y)"""
        self.x = x
        self.y = y
        self._move_timer = 0
