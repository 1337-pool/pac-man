"""Pac-Man demo — classic maze style with smooth animated movement.

Run with:  uv run ghost_demo.py

Controls:
    Arrow keys / WASD  — hold to move continuously
    TAB                — toggle chase / scatter mode
    ESC                — quit
"""

import os
import sys

os.environ["SDL_VIDEODRIVER"] = "x11"

import pygame

from src.entities.ghost import Ghost, GHOST_NAMES
from src.entities.player import Player
from src.maze.adapter import build_level_maze
from src.ui.maze_renderer import draw_maze
from src.ui.theme import (
    BLACK,
    MUTED,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    WHITE,
    YELLOW,
    body_font,
    display_font,
    draw_text,
)

CELL = 32
COLS, ROWS = 25, 25
BOARD_X = (SCREEN_WIDTH - COLS * CELL) // 2
BOARD_Y = (SCREEN_HEIGHT - ROWS * CELL) // 2 + 20

KEY_DIR = {
    pygame.K_UP: "north",
    pygame.K_w: "north",
    pygame.K_DOWN: "south",
    pygame.K_s: "south",
    pygame.K_LEFT: "west",
    pygame.K_a: "west",
    pygame.K_RIGHT: "east",
    pygame.K_d: "east",
}

KEY_SET = set(KEY_DIR.keys())


def main():
    pygame.init()
    surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pac-Man — Classic Demo")
    clock = pygame.time.Clock()

    maze = build_level_maze(COLS, ROWS, seed=42)

    mid_x, mid_y = COLS // 2, ROWS // 2
    player = Player(mid_x, mid_y, 3, "pacman", move_frames=8)
    player.direction = "east"

    home = (COLS // 2, ROWS // 2)
    corner_spawns = [
        (1, 1),              # Blinky — top-left
        (COLS - 2, 1),       # Pinky — top-right
        (1, ROWS - 2),       # Inky — bottom-left
        (COLS - 2, ROWS - 2),# Clyde — bottom-right
    ]
    ghosts = [
        Ghost("Blinky", corner_spawns[i][0], corner_spawns[i][1],
              home, f"ghost_{name}", i, move_frames=12)
        for i, name in enumerate(["red", "pink", "blue", "orange"])
    ]

    wanted_dir = None
    scatter = False
    tick = 0
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_TAB:
                    scatter = not scatter
                elif event.key in KEY_DIR:
                    wanted_dir = KEY_DIR[event.key]

        if not player.is_moving and wanted_dir:
            if player.can_move(maze, wanted_dir):
                player.move(maze, wanted_dir)
            elif player.direction != wanted_dir:
                if player.can_move(maze, wanted_dir):
                    player.move(maze, wanted_dir)

        player.update_render()

        tick += 1
        ghost_move_interval = 14
        if tick % ghost_move_interval == 0:
            blinky = ghosts[0]
            for g in ghosts:
                if not g.is_moving:
                    g.think(
                        maze, player.x, player.y, player.direction or "east",
                        blinky.x, blinky.y, scatter,
                    )
                    g.act(maze)
                g.update()

        for g in ghosts:
            g.update_render()
            if tick % ghost_move_interval == 0 and not g.is_moving:
                g.update()

        surface.fill(BLACK)
        draw_maze(surface, maze, BOARD_X, BOARD_Y, CELL)

        for g in ghosts:
            g.draw(surface, BOARD_X, BOARD_Y, CELL)

        player.draw(surface, BOARD_X, BOARD_Y, CELL)

        draw_text(
            surface, "PAC-MAN", display_font(22), YELLOW,
            center=(SCREEN_WIDTH // 2, 16),
        )
        mode = "SCATTER" if scatter else "CHASE"
        draw_text(
            surface,
            f"{mode}  |  ARROWS/WASD: hold to move  TAB: toggle  ESC: quit",
            body_font(12), MUTED,
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 14),
        )

        info_y = 44
        for g in ghosts:
            draw_text(
                surface,
                f"{GHOST_NAMES[g.id]}: ({g.x},{g.y}) [{g.state}]",
                body_font(11), WHITE,
                topleft=(20, info_y),
            )
            info_y += 16
        draw_text(
            surface,
            f"Pac-Man: ({player.x},{player.y}) score={player.score}",
            body_font(11), YELLOW,
            topleft=(20, info_y + 4),
        )

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Demo crashed: {e}")
        pygame.quit()
        sys.exit(1)
