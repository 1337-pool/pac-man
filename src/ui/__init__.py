"""Pygame UI screens for the Pac-Man game.

Exposes the screen classes so other modules can simply do:

    from src.ui import HomeScreen, HighscoreScreen, InstructionsScreen
"""

from src.ui.highscore_screen import HighscoreScreen
from src.ui.home_screen import HomeScreen
from src.ui.instructions_screen import InstructionsScreen

__all__ = ["HomeScreen", "HighscoreScreen", "InstructionsScreen"]
