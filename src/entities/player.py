from .entity import Entity

class Player(Entity):
    def __init__(self, x: int, y: int, lives: int, img: str) -> None:
        super().__init__(x, y)
        self.lives: int = lives
        self.score: int = 0
        self.img: str = img

    def respawn(self, x: int, y: int) -> None:

        self.x = x
        self.y = y

    def is_alive(self) -> bool:
        return self.lives > 0

def add_score(self, points: int) -> None:
    self.score += points

def lose_life(self, middle: tuple[int, int]) -> None:
    if self.lives >= 1:
        self.lives -= 1
        self.respawn(middle[0], middle[1])
