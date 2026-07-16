"""Classic Pac-Man maze renderer.

Draws the maze with thick blue wall segments and rounded corners,
matching the look of the original 1980 arcade game.  Walls are drawn
as the borders between open corridor cells and blocked cells, using
thick lines with rounded caps and corner arcs.
"""

from __future__ import annotations

import pygame

from src.ui.theme import MAZE_BLUE, MAZE_BLUE_DIM

WALL_WIDTH = 3


def draw_maze(
    surface: "pygame.Surface",
    maze: list[list[dict[str, bool]]],
    board_x: int,
    board_y: int,
    cell_size: int,
) -> None:
    """Render the maze in classic Pac-Man blue-wall style.

    Each wall segment is a thick blue line drawn along the edge of
    a cell.  Where two wall segments meet at a right angle, a small
    filled circle is drawn to create the rounded-corner look.
    """
    h = len(maze)
    w = len(maze[0]) if h else 0
    hw = WALL_WIDTH // 2

    drawn: set[tuple[int, int, str]] = set()

    for y in range(h):
        for x in range(w):
            cell = maze[y][x]
            px = board_x + x * cell_size
            py = board_y + y * cell_size

            if cell["north"] and (x, y, "north") not in drawn:
                x1 = px
                y1 = py
                x2 = px + cell_size
                y2 = py
                pygame.draw.line(surface, MAZE_BLUE, (x1, y1), (x2, y2), WALL_WIDTH)
                drawn.add((x, y, "north"))

            if cell["south"] and (x, y, "south") not in drawn:
                x1 = px
                y1 = py + cell_size
                x2 = px + cell_size
                y2 = py + cell_size
                pygame.draw.line(surface, MAZE_BLUE, (x1, y1), (x2, y2), WALL_WIDTH)
                drawn.add((x, y, "south"))

            if cell["west"] and (x, y, "west") not in drawn:
                x1 = px
                y1 = py
                x2 = px
                y2 = py + cell_size
                pygame.draw.line(surface, MAZE_BLUE, (x1, y1), (x2, y2), WALL_WIDTH)
                drawn.add((x, y, "west"))

            if cell["east"] and (x, y, "east") not in drawn:
                x1 = px + cell_size
                y1 = py
                x2 = px + cell_size
                y2 = py + cell_size
                pygame.draw.line(surface, MAZE_BLUE, (x1, y1), (x2, y2), WALL_WIDTH)
                drawn.add((x, y, "east"))

    _draw_rounded_corners(surface, maze, board_x, board_y, cell_size)


def _draw_rounded_corners(
    surface: "pygame.Surface",
    maze: list[list[dict[str, bool]]],
    board_x: int,
    board_y: int,
    cell_size: int,
) -> None:
    """Draw small filled circles at wall-segment intersections for rounded look."""
    h = len(maze)
    w = len(maze[0]) if h else 0
    corner_r = WALL_WIDTH // 2 + 1

    for y in range(h):
        for x in range(w):
            cell = maze[y][x]
            px = board_x + x * cell_size
            py = board_y + y * cell_size

            # Top-left corner
            if cell["north"] or cell["west"]:
                if cell["north"] and cell["west"]:
                    pygame.draw.circle(surface, MAZE_BLUE, (px, py), corner_r)

            # Top-right corner
            if cell["north"] or cell["east"]:
                if cell["north"] and cell["east"]:
                    pygame.draw.circle(surface, MAZE_BLUE, (px + cell_size, py), corner_r)

            # Bottom-left corner
            if cell["south"] or cell["west"]:
                if cell["south"] and cell["west"]:
                    pygame.draw.circle(surface, MAZE_BLUE, (px, py + cell_size), corner_r)

            # Bottom-right corner
            if cell["south"] or cell["east"]:
                if cell["south"] and cell["east"]:
                    pygame.draw.circle(
                        surface, MAZE_BLUE,
                        (px + cell_size, py + cell_size), corner_r,
                    )
