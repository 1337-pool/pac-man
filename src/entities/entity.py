
class Entity:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def can_move(self, maze: list, direction: str) -> bool:
        return not maze[self.y][self.x][direction]

    def move(self, maze: list, direction: str) -> None:
        if self.can_move(maze, direction):
            if direction == "north":
                self.y -= 1
            elif direction == "east":
                self.x += 1
            elif direction == "west":
                self.x -= 1
            elif direction == "south":
                self.y += 1
