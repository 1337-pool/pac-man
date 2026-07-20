"""Cheat manager for peer review and testing.

Toggles all cheats (invincibility, ghost freezing, timer freeze)
simultaneously.
"""

from __future__ import annotations


class CheatManager:
    def __init__(self) -> None:
        self.invisible: bool = False
        self.freeze_ghosts: bool = False
        self.freeze_timer: bool = False
        self.speed_up: bool = False
        self.all_active: bool = False

    def toggle_all_cheats(self) -> None:
        """Flips all continuous cheats to the opposite state."""
        self.all_active = not self.all_active
