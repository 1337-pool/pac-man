import sys
import os
from src.config.loader import load_config, ParsingError
from src.config.schema import apply_defaults
from src.gameplay.game import Game
from src.utils.paths import app_dir


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python3 pac-man.py config.json")
        sys.exit(1)

    config_arg = sys.argv[1]
    if not os.path.isabs(config_arg):
        config_arg = os.path.join(app_dir(), config_arg)

    try:
        raw_config = load_config(config_arg)
        config = apply_defaults(raw_config)
    except ParsingError as e:
        print(f"Config Error: {e}")
        sys.exit(1)

    try:
        game = Game(config)
        game.run()
    except BaseException as e:
        print(f"Error {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
