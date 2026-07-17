# from src.config.loader import load_config, ParsingError
# from src.config.schema import apply_defaults
# from mazegenerator import MazeGenerator
# from src.maze.adapter import MazeGenerationError, build_level_maze
# from src.persistence.highscore import ScoreFileError, load_highscores, save_highscores
# from src.gameplay.level import Level
# import sys

# load_config("config.json")

# try:
#     highsroces = load_highscores("highscore.json")
#     save_highscores("highscore.json", highsroces)
# except ScoreFileError as e:
#     print(e)
#     exit()
# print(highsroces)

# level = Level(width=21, height=21, seed=42, lives=3, img="pacman")
# for _ in range(100):
#     level.update()
# print(level.player.x, level.player.y, [(g.name, g.x, g.y, g.state) for g in level.ghosts])


import sys
from src.config.loader import load_config, ParsingError
from src.config.schema import apply_defaults
from src.gameplay.game import Game

def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python3 pac-man.py config.json")
        sys.exit(1)

    try:
        raw_config = load_config(sys.argv[1])
        config = apply_defaults(raw_config)
    except ParsingError as e:
        print(f"Config Error: {e}")
        sys.exit(1)

    game = Game(config)
    game.run()

if __name__ == "__main__":
    main()