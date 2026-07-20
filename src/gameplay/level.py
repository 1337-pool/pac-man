from ..maze.adapter import build_level_maze
from ..entities.player import Player
from ..entities.ghost import Ghost
from ..entities.ghost_behaviors import _build_scatter_corners
from ..gameplay.cheat import CheatManager


_GHOST_SPRITES: list[str] = [
    "ghost_red",
    "ghost_pink",
    "ghost_blue",
    "ghost_orange",
]


class Level:
    def __init__(
        self,
        width: int,
        height: int,
        seed: int,
        lives: int,
        cheat_manager: CheatManager,
        points_per_ghost: int = 200,
        points_per_pacgum: int = 10,
        points_per_super_pacgum: int = 50,
    ) -> None:
        self.width: int = width
        self.height: int = height
        self.points_per_ghost: int = points_per_ghost
        self.points_per_pacgum: int = points_per_pacgum
        self.points_per_super_pacgum: int = points_per_super_pacgum
        self.cheat_manager = cheat_manager
        self.maze: list[
            list[
                dict[str, bool]]] = build_level_maze(width, height, seed)

        shape_w, shape_h = 7, 5
        start_x_42 = int((width - shape_w) / 2)
        start_y_42 = int((height - shape_h) / 2)
        self.middle: tuple[int, int] = (start_x_42 + 3, start_y_42 + 2)

        ghost_corners = _build_scatter_corners(width, height)
        self.corners: tuple[
            tuple[
                int, int], ...] = tuple(ghost_corners.values())

        self.player: Player = Player(
            x=self.middle[0], y=self.middle[1], lives=lives
        )

        self.ghosts: list[Ghost] = [
            Ghost(
                x=ghost_corners[i][0],
                y=ghost_corners[i][1],
                home=ghost_corners[i],
                name=_GHOST_SPRITES[i],
                ID=i,
            )
            for i in range(4)
        ]

        self.pacgums: set[tuple[int, int]] = set()
        self.super_pacgums: set[tuple[int, int]] = set()

        ft_small = [
            [1, 0, 0, 0, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 0, 1, 1, 1],
            [0, 0, 1, 0, 1, 0, 0],
            [0, 0, 1, 0, 1, 1, 1]
        ]
        shape_h = len(ft_small)
        shape_w = len(ft_small[0])

        shape_42_blocks: set[tuple[int, int]] = set()
        if width >= shape_w * 2 and height >= shape_h * 2:
            start_y = int((height - shape_h) / 2)
            start_x = int((width - shape_w) / 2)
            for y in range(shape_h):
                for x in range(shape_w):
                    if ft_small[y][x] == 1:
                        shape_42_blocks.add((start_x + x, start_y + y))

        for x in range(width):
            for y in range(height):
                pos = (x, y)

                if pos in shape_42_blocks:  # skip 42
                    continue

                if pos in self.corners:  # supergum
                    self.super_pacgums.add(pos)

                else:
                    self.pacgums.add(pos)

    def _blinky_position(self) -> tuple[int, int]:
        """Return Blinky's (id=0) current cell, needed by Inky's AI."""
        blinky = self.ghosts[0]
        return (blinky.x, blinky.y)

    def update(self) -> None:
        """Advance one game tick: AI, movement interpolation, collisions.

        Call this once per frame from the main game loop.
        """
        self.player.update_render()

        blinky_x, blinky_y = self._blinky_position()

        if not self.cheat_manager.all_active:
            for ghost in self.ghosts:
                ghost.update()
                if not ghost.is_moving:
                    ghost.think(
                        self.maze,
                        self.player.x,
                        self.player.y,
                        self.player.direction or "east",
                        blinky_x,
                        blinky_y,
                    )
                    ghost.act(self.maze)
                ghost.update_render()

        self._check_collisions()
        self._check_pacgums()

    def _check_collisions(self) -> None:
        """Handle player/ghost collisions"""
        for ghost in self.ghosts:
            if (ghost.x, ghost.y) != (self.player.x, self.player.y):
                continue

            if ghost.is_edible():
                self.player.add_score(self.points_per_ghost)
                ghost.get_eaten()
            elif ghost.is_chasing():
                if not self.cheat_manager.all_active:
                    self.player.lose_life(self.middle)

    def _check_pacgums(self) -> None:
        """Check if the player's current cell overlaps with any pacgums."""
        pos = (self.player.x, self.player.y)

        if pos in self.pacgums:
            self.pacgums.remove(pos)
            self.player.add_score(self.points_per_pacgum)

        if pos in self.super_pacgums:
            self.super_pacgums.remove(pos)
            self.player.add_score(self.points_per_super_pacgum)
            for ghost in self.ghosts:
                ghost.make_edible()

    def is_level_complete(self) -> bool:
        """Return True if all pacgums and super-pacgums have been eaten."""
        return not self.pacgums and not self.super_pacgums
