"""Reusable arcade-style button widget for pygame screens."""

import pygame

from src.ui.theme import BLACK, YELLOW, body_font


class Button:
    """A clickable rectangular button with a primary/secondary style.

    Attributes:
        rect: The button's screen-space rectangle (also its hitbox).
        label: The text drawn on the button.
        primary: If True, renders filled (yellow bg); otherwise
            renders outlined (transparent bg, yellow border/text).
    """

    def __init__(
        self,
        label: str,
        center: tuple[int, int],
        width: int = 320,
        height: int = 56,
        primary: bool = False,
        font_size: int = 22,
    ) -> None:
        self.label = label
        self.primary = primary
        self.rect = pygame.Rect(0, 0, width, height)
        self.rect.center = center
        self.font = body_font(font_size)

    def draw(self, surface: "pygame.Surface") -> None:
        """Draw the button onto the given surface."""
        if self.primary:
            pygame.draw.rect(surface, YELLOW, self.rect)
            text_color = BLACK
        else:
            pygame.draw.rect(surface, BLACK, self.rect)
            pygame.draw.rect(surface, YELLOW, self.rect, width=2)
            text_color = YELLOW

        label_surf = self.font.render(self.label, True, text_color)
        label_rect = label_surf.get_rect(center=self.rect.center)
        surface.blit(label_surf, label_rect)

    def is_clicked(self, event: "pygame.event.Event") -> bool:
        """Return True if this event is a left-click inside the button."""
        return (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        )
