"""Home / main menu screen.

Displays the game title, a preview of the top highscores, and the
main navigation buttons (Start, Highscores, Instructions, Exit), as
required by subject section VI.8 ("Main Menu").
"""

import pygame

from src.score_handler.highscore import ScoreFileError, load_highscores
from src.ui.button import Button
from src.ui.theme import (
    BLACK,
    CARD,
    GHOST_COLORS,
    MUTED,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    WHITE,
    YELLOW,
    body_font,
    display_font,
    load_sprite,
    draw_text,
)

_PREVIEW_COUNT = 4


class HomeScreen:
    """The main menu screen shown when the game launches.

    Usage:
        screen = HomeScreen(highscore_filename="highscore.json")
        ...
        action = screen.handle_event(event)  # "start" | "highscores" |
                                            # "instructions" | "exit" | None
        screen.draw(surface)
    """

    def __init__(self, highscore_filename: str = "highscore.json") -> None:
        self.highscore_filename = highscore_filename

        center_x = SCREEN_WIDTH // 2
        self.start_button = Button(
            "START GAME", (center_x, 480), width=320, height=60, primary=True,
        )
        self.highscores_button = Button(
            "HIGHSCORES", (center_x, 552), width=320, height=48,
        )
        self.instructions_button = Button(
            "INSTRUCTIONS", (center_x, 612), width=320, height=48,
        )
        self.exit_button = Button(
            "EXIT", (center_x, 672), width=320, height=48,
        )

    def _load_preview_scores(self) -> list[dict]:
        """Return up to the top 4 highscores, or an empty list on error.

        Never raises: a missing/corrupt highscore file must not crash
        the main menu (subject section III.1 — no crashes allowed).
        """
        try:
            scores = load_highscores(self.highscore_filename)
        except ScoreFileError:
            return []
        scores = sorted(scores, key=lambda s: s["score"], reverse=True)
        return scores[:_PREVIEW_COUNT]

    def handle_event(self, event: "pygame.event.Event") -> str | None:
        """Translate a pygame event into a menu action, if any."""
        if self.start_button.is_clicked(event):
            return "start"
        if self.highscores_button.is_clicked(event):
            return "highscores"
        if self.instructions_button.is_clicked(event):
            return "instructions"
        if self.exit_button.is_clicked(event):
            return "exit"
        return None

    def draw(self, surface: "pygame.Surface") -> None:
        """Render the full home screen onto the given surface."""
        surface.fill(BLACK)
        center_x = SCREEN_WIDTH // 2

        draw_text(
            surface, "PAC-MAN", display_font(72), YELLOW,
            center=(center_x, 130),
        )

        dot_radius = 14
        dot_gap = 48
        colors = (YELLOW, *GHOST_COLORS)
        start_x = center_x - (len(colors) - 1) * dot_gap // 2
        sprite_names = ["pacman", "ghost_red", "ghost_pink", "ghost_blue", "ghost_orange"]

        for i, name in enumerate(sprite_names):
            sprite = load_sprite(name, dot_radius * 2)
            x = start_x + i * dot_gap
            if sprite is not None:
                rect = sprite.get_rect(center=(x, 190))
                surface.blit(sprite, rect)
            else:
                pygame.draw.circle(surface, colors[i], (x, 190), dot_radius)

        self._draw_highscore_preview(surface, center_x, 250)

        self.start_button.draw(surface)
        self.highscores_button.draw(surface)
        self.instructions_button.draw(surface)
        self.exit_button.draw(surface)

        draw_text(
            surface, "© 1980 NAMCO LTD.", body_font(14), MUTED,
            center=(center_x, SCREEN_HEIGHT - 40),
        )

    def _draw_highscore_preview(
        self, surface: "pygame.Surface", center_x: int, top: int,
    ) -> None:
        panel = pygame.Rect(0, 0, 420, 170)
        panel.centerx = center_x
        panel.top = top
        pygame.draw.rect(surface, CARD, panel)
        pygame.draw.rect(surface, YELLOW, panel, width=2)

        draw_text(
            surface, "HIGH SCORES", body_font(18), YELLOW,
            topleft=(panel.left + 20, panel.top + 16),
        )

        scores = self._load_preview_scores()
        row_font = body_font(16)
        if not scores:
            draw_text(
                surface, "NO SCORES YET", row_font, MUTED,
                topleft=(panel.left + 20, panel.top + 60),
            )
            return

        for i, entry in enumerate(scores):
            row_y = panel.top + 56 + i * 26
            draw_text(
                surface, f"{i + 1}. {entry['name']}", row_font, WHITE,
                topleft=(panel.left + 20, row_y),
            )
            draw_text(
                surface, f"{entry['score']:,}", row_font, YELLOW,
                topleft=(panel.right - 140, row_y),
            )
