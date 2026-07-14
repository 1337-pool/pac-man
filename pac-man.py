from src.config.loader import load_config, ParsingError
from src.config.schema import apply_defaults
from mazegenerator import MazeGenerator
from src.maze.adapter import MazeGenerationError, build_level_maze
from src.persistence.highscore import ScoreFileError, load_highscores, save_highscores
import sys



try:
    highsroces = load_highscores("highscore.json")
    save_highscores("highscore.json", highsroces)
except ScoreFileError as e:
    print(e)
    exit()
print(highsroces)

