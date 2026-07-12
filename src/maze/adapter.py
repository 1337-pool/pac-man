from mazegenerator import MazeGenerator

class MazeGenerationError(Exception):
    pass

def generate_maze(width: int, height: int, seed: int) -> MazeGenerator:

    if width <= 0 or height <= 0:
        raise MazeGenerationError("height or width are not valid ;)")
    try:
        maze = MazeGenerator(size=(width, height), seed=seed, perfect=False)

    except Exception:
        raise MazeGenerationError("mazegenerator error")

    return maze


def decode_cell(value: int) -> dict[str, bool]:

    result: dict = {"north": False, "east": False, "south": False, "west": False}

    if value & 1:
        result["north"] = True
    if value & 2:
        result["east"] = True
    if value & 4:
        result["south"] = True
    if value & 8:
        result["west"] = True

    return result

def decode_maze(raw_maze: list[list[int]]) -> list[list[dict[str, bool]]]:

    result: list[list[dict[str, bool]]] = []

    for x in raw_maze:
        raw_list: list[dict[str, bool]] = []
        for y in x:
            raw_list.append(decode_cell(y))
        result.append(raw_list)

    return result

def build_level_maze(width: int, height: int, seed: int) -> list[list[dict[str, bool]]]:
    Maze = generate_maze(width=width, height=height, seed=seed)
    return decode_maze(Maze.maze)