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
    
    try:
        game = Game(config)
        game.run()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()