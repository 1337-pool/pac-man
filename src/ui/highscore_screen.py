"""Highscores screen.

Displays the top 10 highscores in full (subject section V.5), backed
by the same load_highscores() used by the rest of the game so this
screen never disagrees with what actually gets saved.
"""

import pygame

from src.score_handler.highscore import ScoreFileError, load_highscores
from src.ui.button import Button
from src.ui.theme import (
    BLACK,
    BORDER,
    CARD,
    MUTED,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    WHITE,
    YELLOW,
    body_font,
    display_font,
    draw_text,
)

_MAX_ROWS = 10


class HighscoreScreen:
    """Full top-10 leaderboard screen with a Back button.

    Usage:
        screen = HighscoreScreen(highscore_filename="highscore.json")
        ...
        action = screen.handle_event(event)  # "back" | None
        screen.draw(surface)
    """

    def __init__(self, highscore_filename: str = "highscore.json") -> None:
        self.highscore_filename = highscore_filename
        center_x = SCREEN_WIDTH // 2
        self.back_button = Button(
            "BACK", (center_x, SCREEN_HEIGHT - 90),
            width=320, height=56, primary=True,
        )

    def _load_scores(self) -> list[dict]:
        """Return up to the top 10 highscores, or [] if unreadable.

        Never raises: a missing/corrupt file must not crash the
        screen (subject section III.1 — no crashes allowed).
        """
        try:
            scores = load_highscores(self.highscore_filename)
        except ScoreFileError:
            return []
        scores = sorted(scores, key=lambda s: s["score"], reverse=True)
        return scores[:_MAX_ROWS]

    def handle_event(self, event: "pygame.event.Event") -> str | None:
        """Translate a pygame event into an action, if any."""
        if self.back_button.is_clicked(event):
            return "back"
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return "back"
        return None

    def draw(self, surface: "pygame.Surface") -> None:
        """Render the full highscores screen onto the given surface."""
        surface.fill(BLACK)
        center_x = SCREEN_WIDTH // 2

        panel = pygame.Rect(0, 0, 480, 620)
        panel.centerx = center_x
        panel.top = 90
        pygame.draw.rect(surface, CARD, panel)
        pygame.draw.rect(surface, YELLOW, panel, width=4)

        draw_text(
            surface, "HIGHSCORES", display_font(34), YELLOW,
            center=(panel.centerx, panel.top + 40),
        )
        draw_text(
            surface, "TOP 10 PLAYERS", body_font(13), MUTED,
            center=(panel.centerx, panel.top + 76),
        )

        scores = self._load_scores()
        row_font = body_font(16)
        list_top = panel.top + 110

        if not scores:
            draw_text(
                surface, "NO SCORES YET", row_font, MUTED,
                center=(panel.centerx, list_top + 40),
            )
        else:
            for i, entry in enumerate(scores):
                row_y = list_top + i * 40
                row_rect = pygame.Rect(
                    panel.left + 24, row_y, panel.width - 48, 34,
                )
                pygame.draw.line(
                    surface, BORDER,
                    (row_rect.left, row_rect.bottom),
                    (row_rect.right, row_rect.bottom),
                )
                draw_text(
                    surface, f"{i + 1}.", row_font, YELLOW,
                    topleft=(row_rect.left, row_rect.top + 6),
                )
                draw_text(
                    surface, str(entry["name"]), row_font, WHITE,
                    topleft=(row_rect.left + 40, row_rect.top + 6),
                )
                score_label = f"{entry['score']:,}"
                score_surf = row_font.render(score_label, True, YELLOW)
                score_rect = score_surf.get_rect()
                score_rect.topright = (row_rect.right, row_rect.top + 6)
                surface.blit(score_surf, score_rect)

        self.back_button.draw(surface)

        draw_text(
            surface, "PRESS ESC OR CLICK BACK TO RETURN", body_font(13),
            MUTED, center=(center_x, SCREEN_HEIGHT - 30),
        )
