from mazegenerator import MazeGenerator


class MazeGenerationError(Exception):
    """Raised when the external maze generator fails or
    receives invalid parameters."""
    pass


def generate_maze(width: int, height: int, seed: int) -> MazeGenerator:
    """Create a maze using the external MazeGenerator package."""
    if width <= 0 or height <= 0:
        raise MazeGenerationError("height or width are not valid ;)")
    try:
        maze: MazeGenerator = MazeGenerator(
            size=(width, height), seed=seed, perfect=False)
    except Exception as e:
        raise MazeGenerationError(f"mazegenerator error: {e}")

    return maze


def decode_cell(value: int) -> dict[str, bool]:
    """Decode a bitmask integer into a dictionary of boolean wall flags."""
    result: dict[str, bool] = {
        "north": False,
        "east": False,
        "south": False,
        "west": False
        }

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
    """Convert a 2D array of bitmask integers into a
    2D array of wall dictionaries."""
    result: list[list[dict[str, bool]]] = []

    for x in raw_maze:
        raw_list: list[dict[str, bool]] = []
        for y in x:
            raw_list.append(decode_cell(y))
        result.append(raw_list)

    return result


def build_level_maze(width: int, height: int, seed: int) -> list[
    list[
        dict[
            str, bool]]]:
    """generate and decode a complete playable maze for a game level."""
    maze = generate_maze(width=width, height=height, seed=seed)
    return decode_maze(maze.maze)
