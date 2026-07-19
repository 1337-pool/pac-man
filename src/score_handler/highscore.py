from pathlib import Path
import json

class ScoreFileError(Exception):
    pass


def _validate_entries(data: list) -> None:
    """Raise ScoreFileError if any entry violates the highscore rules."""
    try:
        for player in data:
            if not isinstance(player.get("name"), str) or not isinstance(player.get("score"), int):
                raise ScoreFileError("file keys error ;)")
            if len(player.get("name")) > 10:
                raise ScoreFileError("player name more than 10 caracters ;)")
            if any(not c.isalnum() and not c.isspace() for c in player.get("name")):
                raise ScoreFileError("player name have invalid caracter (see subject V.5) ;)")
            if player.get("score") < 0:
                raise ScoreFileError("player score negative ;)")
    except AttributeError:
        raise ScoreFileError("score file have to be list of players ;)")

    def load_highscores(path: str) -> list[dict[str, Any]]:
        """Load and validate highscores from a JSON file."""
        if not Path(path).is_file():
            return []

        try:
            with open(path) as f:
                raw = f.read()
        except OSError as e:
            raise ScoreFileError(f"error with the score file: {e}")

        if not raw.strip():
            return []

        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            raise ScoreFileError("error with the score file format")

        _validate_entries(data)

        if len(data) > 10:
            raise ScoreFileError("score file have more than 10 players ;)")

        return data


    def save_highscores(path: str, scores: list[dict[str, Any]]) -> None:
        """Validate, sort, and save highscores to a JSON file."""
        _validate_entries(scores)

        scores = sorted(scores, key=lambda elem: elem["score"], reverse=True)
        scores = scores[:10]

        try:
            with open(path, "w") as f:
                json.dump(scores, f, indent=4)
        except OSError as e:
            raise ScoreFileError(f"scores file error: {e}")
