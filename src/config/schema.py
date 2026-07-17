from typing import Any, Dict, List

DEFAULT_LEVEL_COUNT = 10
DEFAULT_WIDTH = 21
DEFAULT_HEIGHT = 21
MIN_DIMENSION = 9
MAX_DIMENSION = 50

DEFAULTS: Dict[str, Any] = {
    "highscore_filename": "highscore.json",
    "levels": [
        {"width": DEFAULT_WIDTH, "height": DEFAULT_HEIGHT}
        for _ in range(DEFAULT_LEVEL_COUNT)
    ],
    "lives": 3,
    "points_per_pacgum": 10,
    "points_per_super_pacgum": 50,
    "points_per_ghost": 200,
    "seed": 42,
    "level_max_time": 90
}


def _clamp_int(value: Any, default: int, minimum: int = 0) -> int:
    """Return value as a valid int >= minimum, or default if invalid."""
    if not isinstance(value, int) or isinstance(value, bool):
        return default
    if value < minimum:
        return default
    return value


def _clamp_dimension(value: Any, default: int) -> int:
    """Return value as a valid maze dimension, or default if invalid."""
    if not isinstance(value, int):
        return default
    if value < MIN_DIMENSION or value > MAX_DIMENSION:
        return default
    return value


def _validate_levels(raw_levels: Any) -> List[Dict[str, int]]:
    """
    Validate/clamp the levels list, padding to the minimum count.
    """
    if not isinstance(raw_levels, list):
        print("Config warning: 'levels' is not a list, using defaults")
        return DEFAULTS["levels"]

    validated: List[Dict[str, int]] = []
    for i, lvl in enumerate(raw_levels):
        if not isinstance(lvl, dict):
            print(f"Config warning: level {i} is not an object, using default")
            validated.append(
                {"width": DEFAULT_WIDTH, "height": DEFAULT_HEIGHT}
                )
            continue

        width = _clamp_dimension(entry.get("width"), DEFAULT_WIDTH)
        height = _clamp_dimension(entry.get("height"), DEFAULT_HEIGHT)
        validated.append({"width": width, "height": height})

    while len(validated) < DEFAULT_LEVEL_COUNT:
        validated.append({"width": DEFAULT_WIDTH, "height": DEFAULT_HEIGHT})

    return validated


def apply_defaults(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Merge a raw config dict with safe defaults, validating types.
    """
    result: Dict[str, Any] = {}

    result["highscore_filename"] = (
        config.get("highscore_filename")
        if isinstance(config.get("highscore_filename"), str)
        else DEFAULTS["highscore_filename"]
    )

    result["levels"] = _validate_levels(config.get("levels"))

    result["lives"] = _clamp_int(
        config.get("lives"), DEFAULTS["lives"], minimum=1)

    result["points_per_pacgum"] = _clamp_int(
        config.get("points_per_pacgum"), DEFAULTS["points_per_pacgum"]
    )

    result["points_per_super_pacgum"] = _clamp_int(
        config.get(
            "points_per_super_pacgum"), DEFAULTS["points_per_super_pacgum"]
    )

    result["points_per_ghost"] = _clamp_int(
        config.get("points_per_ghost"), DEFAULTS["points_per_ghost"]
    )

    result["seed"] = _clamp_int(
        config.get("seed"), DEFAULTS["seed"])

    result["level_max_time"] = _clamp_int(
        config.get("level_max_time"), DEFAULTS["level_max_time"], minimum=60
    )

    return result
