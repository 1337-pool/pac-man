"""Ghost AI movement strategies and BFS pathfinding.

Each ghost has a unique personality that determines its target tile:

- Blinky (red, id=0): Direct chase — targets the player's current cell.
- Pinky  (pink, id=1): Ambush — targets 4 tiles ahead of the player.
- Inky   (cyan, id=2): Unpredictable — uses Blinky's position to
  compute a doubled vector offset from the player.
- Clyde  (orange, id=3): Random — chases when far (>= 8 tiles),
  scatters to its corner when close.

When a ghost is in scatter mode it heads toward one of the four map
corners.  When frightened (edible) it picks a random valid direction.
When eaten it uses BFS to take the shortest path back to its home
cell, then resumes chasing.

All pathfinding uses BFS over the wall-dict grid so it is always
optimal and never gets stuck.
"""

from __future__ import annotations
import random
from collections import deque
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from src.entities.ghost import Ghost

DIRECTIONS: list[Any] = ["north", "east", "south", "west"]
OPPOSITE: dict[str, str] = {
    "north": "south",
    "south": "north",
    "east": "west",
    "west": "east",
}


def _build_scatter_corners(
        width: int,
        height: int) -> dict[int, tuple[int, int]]:
    """Return scatter corner tiles adjusted for the maze dimensions."""
    return {
        0: (width - 1, 0),
        1: (0, 0),
        2: (width - 1, height - 1),
        3: (0, height - 1),
    }


def _neighbors(
    x: int, y: int, maze: list[list[dict[str, bool]]],
) -> list[tuple[int, int]]:
    """Return reachable neighbor cells (no wall blocking)."""
    h = len(maze)
    w = len(maze[0]) if h else 0
    result: list[tuple[int, int]] = []
    for direction in DIRECTIONS:
        if not maze[y][x][direction]:
            nx, ny = x, y
            if direction == "north":
                ny -= 1
            elif direction == "south":
                ny += 1
            elif direction == "east":
                nx += 1
            elif direction == "west":
                nx -= 1
            if 0 <= nx < w and 0 <= ny < h:
                result.append((nx, ny))
    return result


def bfs_path(
    maze: list[list[dict[str, bool]]],
    start: tuple[int, int],
    goal: tuple[int, int],
) -> Any:
    """BFS shortest path from *start* to *goal* on the maze grid.

    Returns a list of (x, y) cells from start to goal inclusive,
    or an empty list if no path exists.
    """
    if start == goal:
        return [start]
    visited: set[tuple[int, int]] = {start}
    queue: Any = deque()
    queue.append((start, [start]))
    while queue:
        (cx, cy), path = queue.popleft()
        for nx, ny in _neighbors(cx, cy, maze):
            if (nx, ny) in visited:
                continue
            new_path = path + [(nx, ny)]
            if (nx, ny) == goal:
                return new_path
            visited.add((nx, ny))
            queue.append(((nx, ny), new_path))
    return []


def bfs_direction(
    maze: list[list[dict[str, bool]]],
    start: tuple[int, int],
    goal: tuple[int, int],
) -> str | None:
    """Return the first move direction from *start* toward *goal* via BFS."""
    path = bfs_path(maze, start, goal)
    if len(path) < 2:
        return None
    sx, sy = path[0]
    nx, ny = path[1]
    dx = nx - sx
    dy = ny - sy
    if dy == -1:
        return "north"
    if dy == 1:
        return "south"
    if dx == 1:
        return "east"
    if dx == -1:
        return "west"
    return None


def _manhattan(a: tuple[int, int], b: tuple[int, int]) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def _target_tile(
    ghost: "Ghost",
    player_x: int,
    player_y: int,
    player_dir: str,
    blinky_x: int,
    blinky_y: int,
    maze_w: int,
    maze_h: int,
) -> tuple[int, int]:
    """Compute the ghost's target tile based on its personality id."""
    corners = _build_scatter_corners(maze_w, maze_h)

    if ghost.id == 0:
        return (player_x, player_y)

    if ghost.id == 1:
        tx, ty = player_x, player_y
        for _ in range(4):
            if player_dir == "north":
                ty -= 1
            elif player_dir == "south":
                ty += 1
            elif player_dir == "east":
                tx += 1
            elif player_dir == "west":
                tx -= 1
        return (tx, ty)

    if ghost.id == 2:
        ax, ay = player_x, player_y
        if player_dir == "north":
            ay -= 2
        elif player_dir == "south":
            ay += 2
        elif player_dir == "east":
            ax += 2
        elif player_dir == "west":
            ax -= 2
        vx = ax - blinky_x
        vy = ay - blinky_y
        return (ax + vx, ay + vy)

    dist = _manhattan((ghost.x, ghost.y), (player_x, player_y))
    if dist >= 8:
        return (player_x, player_y)
    return corners[3]


def choose_direction(
    ghost: "Ghost",
    maze: list[list[dict[str, bool]]],
    player_x: int,
    player_y: int,
    player_dir: str,
    blinky_x: int = 0,
    blinky_y: int = 0,
    scatter: bool = False,
) -> str | None:
    """Pick the best direction for *ghost* to move this tick.

    Returns a direction string ("north", "east", "south", "west") or
    None if the ghost cannot move at all.
    """
    maze_h = len(maze)
    maze_w = len(maze[0]) if maze_h else 0
    corners = _build_scatter_corners(maze_w, maze_h)

    x, y = ghost.x, ghost.y
    current_dir = getattr(ghost, "direction", None)
    back = OPPOSITE[current_dir] if current_dir else None

    valid: list[tuple[str, int, int]] = []
    for d in DIRECTIONS:
        if d == back:
            continue
        if not maze[y][x][d]:
            nx, ny = x, y
            if d == "north":
                ny -= 1
            elif d == "south":
                ny += 1
            elif d == "east":
                nx += 1
            elif d == "west":
                nx -= 1
            if 0 <= nx < maze_w and 0 <= ny < maze_h:
                valid.append((d, nx, ny))

    if not valid:
        for d in DIRECTIONS:
            if not maze[y][x][d]:
                nx, ny = x, y
                if d == "north":
                    ny -= 1
                elif d == "south":
                    ny += 1
                elif d == "east":
                    nx += 1
                elif d == "west":
                    nx -= 1
                if 0 <= nx < maze_w and 0 <= ny < maze_h:
                    valid.append((d, nx, ny))

    if not valid:
        return None

    if ghost.is_edible():
        return random.choice(valid)[0]

    if ghost.is_eaten():
        d = bfs_direction(maze, (x, y), ghost.home)
        if d and any(vd == d for vd, _, _ in valid):
            return d
        valid.sort(key=lambda v: _manhattan((v[1], v[2]), ghost.home))
        return valid[0][0]

    if scatter:
        target = corners.get(ghost.id, (0, 0))
    else:
        target = _target_tile(
            ghost, player_x, player_y, player_dir,
            blinky_x, blinky_y, maze_w, maze_h,
        )

    valid.sort(key=lambda v: _manhattan((v[1], v[2]), target))
    return valid[0][0]
