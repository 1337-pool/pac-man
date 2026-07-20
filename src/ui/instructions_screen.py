"""Instructions screen (a.k.a. the "cheat sheet").

Shows controls, objective, scoring, ghost behavior, and lives/level
rules in one place, as required by subject section VI.8 ("Main Menu
-> Instructions").
"""

from __future__ import annotations

import pygame

from src.ui.button import Button
from src.ui.theme import (
    BLACK,
    CARD,
    GHOST_COLORS,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    WHITE,
    YELLOW,
    body_font,
    display_font,
    draw_text,
)

_GHOST_LINES = (
    ("RED (BLINKY) - CHASES YOU", GHOST_COLORS[0]),
    ("PINK (PINKY) - AMBUSH", GHOST_COLORS[1]),
    ("CYAN (INKY) - UNPREDICTABLE", GHOST_COLORS[2]),
    ("ORANGE (CLYDE) - RANDOM", GHOST_COLORS[3]),
)

_SECTIONS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("CONTROLS", (
        "ARROW KEYS OR WASD TO MOVE",
        "SPACE / ESC - PAUSE GAME",
    )),
    ("OBJECTIVE", (
        "COLLECT ALL PACGUMS WHILE AVOIDING",
        "THE FOUR GHOSTS TO CLEAR THE LEVEL.",
    )),
    ("SCORING", (
        "PACGUM = 10 POINTS",
        "SUPER PACGUM = 50 POINTS",
        "EDIBLE GHOST = 200 POINTS",
    )),
    ("CHEAT MODE (F1)", (
        "TOGGLES INVINCIBILITY, GHOST FREEZE,",
        "SPEED BOOST, AND TIMER FREEZE.",
    )),
)


class InstructionsScreen:
    """Controls/rules reference screen with a Back button.

    Usage:
        screen = InstructionsScreen()
        ...
        action = screen.handle_event(event)  # "back" | None
        screen.draw(surface)
    """

    def __init__(self) -> None:
        center_x = SCREEN_WIDTH // 2
        self.back_button = Button(
            "BACK TO MENU", (center_x, SCREEN_HEIGHT - 90),
            width=360, height=56, primary=True,
        )

    def handle_event(self, event: pygame.event.Event) -> str | None:
        """Translate a pygame event into an action, if any."""
        if self.back_button.is_clicked(event):
            return "back"
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return "back"
        return None

    def draw(self, surface: pygame.Surface) -> None:
        """Render the full instructions screen onto the given surface."""
        surface.fill(BLACK)
        center_x = SCREEN_WIDTH // 2

        panel = pygame.Rect(0, 0, 760, 660)
        panel.centerx = center_x
        panel.top = 60
        pygame.draw.rect(surface, CARD, panel)
        pygame.draw.rect(surface, YELLOW, panel, width=4)

        draw_text(
            surface, "HOW TO PLAY", display_font(30), YELLOW,
            center=(panel.centerx, panel.top + 44),
        )

        heading_font = body_font(15)
        line_font = body_font(13)
        y = panel.top + 96
        left = panel.left + 40

        for title, lines in _SECTIONS:
            draw_text(
                surface, title, heading_font, YELLOW, topleft=(left, y),
            )
            y += 26
            for line in lines:
                draw_text(
                    surface, line, line_font, WHITE, topleft=(left, y)
                )
                y += 20
            y += 16

        draw_text(
            surface, "THE GHOSTS", heading_font, YELLOW, topleft=(left, y)
        )
        y += 30
        for label, color in _GHOST_LINES:
            pygame.draw.circle(surface, color, (left + 6, y + 7), 6)
            draw_text(
                surface, label, line_font, WHITE, topleft=(left + 20, y)
            )
            y += 22

        self.back_button.draw(surface)
