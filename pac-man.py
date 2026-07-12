from src.config.loader import load_config, ParsingError
from mazegenerator import MazeGenerator




try:
    config_dic: dict = load_config("config.json")

except ParsingError as e:
    print(e)
    exit()

print(config_dic)

# maze = MazeGenerator(seed=42)
# print(maze.maze)