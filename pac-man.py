from src.config.loader import load_config, ParsingError
from src.config.schema import apply_defaults
from mazegenerator import MazeGenerator
import sys



config = load_config(sys.argv[1])
config = apply_defaults(config)

print(config)