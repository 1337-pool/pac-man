"""Cheat manager for peer review and testing.

Toggles all cheats (invincibility, ghost freezing, speed boost, timer freeze) simultaneously.
"""

from __future__ import annotations

class CheatManager:
    def __init__(self) -> None:
        self.invincible: bool = False
        self.freeze_ghosts: bool = False
        self.speed_boost: bool = False
        self.freeze_timer: bool = False  # <-- ADDED THIS
        self.all_active: bool = False

    def toggle_all_cheats(self) -> None:
        """Flips all continuous cheats to the opposite state."""
        self.all_active = not self.all_active
        self.invincible = self.all_active
        self.freeze_ghosts = self.all_active
        self.speed_boost = self.all_active
        self.freeze_timer = self.all_active  # <-- ADDED THIS