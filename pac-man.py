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
