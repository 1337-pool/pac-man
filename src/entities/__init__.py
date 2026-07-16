"""Game entities: player, ghosts, and base entity class."""

from src.entities.entity import Entity
from src.entities.ghost import Ghost, GHOST_NAMES
from src.entities.player import Player

__all__ = ["Entity", "Ghost", "GHOST_NAMES", "Player"]
