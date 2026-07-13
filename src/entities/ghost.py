from typing import Literal
import time
from .entity import Entity

GhostState = Literal["chasing", "edible", "eaten"]


class Ghost(Entity):
    def __init__(self, x: int, y: int, home: tuple[int, int]) -> None:
        super().__init__(x, y)
        self.home: tuple[int, int] = home
        self.state: GhostState = "chasing"
        self.eaten_at: float = 0.0

    def make_edible(self) -> None:
        if self.state != "eaten":
            self.state = "edible"

    def get_eaten(self) -> None:
        self.state = "eaten"
        self.eaten_at = time.time()

    def update(self, respawn_delay: float = 10.0) -> None:
        if self.state == "eaten" and time.time() - self.eaten_at >= respawn_delay:
            self.respawn()

    def respawn(self) -> None:
        self.x = self.home[0]
        self.y = self.home[1]
        self.state = "chasing"

    def is_edible(self) -> bool:
        return self.state == "edible"

    def is_eaten(self) -> bool:
        return self.state == "eaten"