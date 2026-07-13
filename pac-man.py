from src.config.loader import load_config, ParsingError
from src.config.schema import apply_defaults
from mazegenerator import MazeGenerator
from src.maze.adapter import MazeGenerationError, build_level_maze
import sys



config = load_config(sys.argv[1])
config = apply_defaults(config)

print(config)

for lvl in config["levels"]:
    print(build_level_maze(lvl["width"], lvl["height"], config['seed']))


from src.maze.adapter import build_level_maze
from src.entities.entity import Entity

maze = build_level_maze(15, 15, 42)
e = Entity(x=7, y=7)
print(e.can_move(maze, "north"))  # should reflect the real wall state at that cell
e.move(maze, "north")
print(e.x, e.y)  # y should have decreased by 1 if move succeeded, unchanged if blocked