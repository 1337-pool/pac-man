"""Shared visual theme for the Pac-Man pygame UI.

Centralizes colors, fonts, and layout constants so every screen looks
consistent. Matches the arcade look already used in the project's
web mockups: black background, yellow primary accent, and the four
classic ghost colors.
"""

from typing import Any
import pygame

from src.utils.paths import resource_path

BLACK: tuple[int, int, int] = (10, 10, 10)
CARD: tuple[int, int, int] = (26, 26, 26)
WHITE: tuple[int, int, int] = (255, 255, 255)
YELLOW: tuple[int, int, int] = (255, 255, 0)
MUTED: tuple[int, int, int] = (136, 136, 136)
BORDER: tuple[int, int, int] = (51, 51, 51)

MAZE_BLUE: tuple[int, int, int] = (33, 33, 255)
MAZE_BLUE_DIM: tuple[int, int, int] = (20, 20, 160)
GHOST_RED: tuple[int, int, int] = (255, 0, 0)
GHOST_PINK: tuple[int, int, int] = (255, 184, 232)
GHOST_CYAN: tuple[int, int, int] = (0, 255, 255)
GHOST_ORANGE: tuple[int, int, int] = (255, 163, 71)
GHOST_EDIBLE: tuple[int, int, int] = (33, 33, 222)
GHOST_COLORS: tuple[tuple[int, int, int], ...] = (
    GHOST_RED, GHOST_PINK, GHOST_CYAN, GHOST_ORANGE,
)

SCREEN_WIDTH: int = 1280
SCREEN_HEIGHT: int = 832

_display_font_cache: dict[int, "pygame.font.Font"] = {}
_body_font_cache: dict[int, "pygame.font.Font"] = {}


def display_font(size: int) -> "pygame.font.Font":
    """Return (and cache) the heading/display font at the given size.

    Falls back to the default pygame font if no monospace/bold system
    font is available, so this never raises even on a bare-bones
    environment.
    """
    if size not in _display_font_cache:
        try:
            font = pygame.font.SysFont("couriernew", size, bold=True)
        except Exception:
            font = pygame.font.Font(None, size)
        _display_font_cache[size] = font
    return _display_font_cache[size]


def body_font(size: int) -> "pygame.font.Font":
    """Return (and cache) the body/UI font at the given size."""
    if size not in _body_font_cache:
        try:
            font = pygame.font.SysFont("arial", size, bold=True)
        except Exception:
            font = pygame.font.Font(None, size)
        _body_font_cache[size] = font
    return _body_font_cache[size]


_sprite_cache: dict[tuple[str, int], "pygame.Surface | None"] = {}


def load_sprite(name: str, height: int) -> Any:
    """Load  a sprite PNG from assets/images, scaled to a height."""

    surface: "Any"
    try:
        path = resource_path(f"assets/images/{name}.png")
        raw = pygame.image.load(str(path)).convert_alpha()
        scale = height / raw.get_height()
        new_size = (max(1, round(raw.get_width() * scale)), height)
        surface = pygame.transform.smoothscale(raw, new_size)
    except (FileNotFoundError, OSError, pygame.error):
        raise Exception(f"ghosts image not found for {name} ghost")

    return surface


def draw_text(
    surface: "pygame.Surface",
    text: str,
    font: "pygame.font.Font",
    color: tuple[int, int, int],
    center: tuple[int, int] | None = None,
    topleft: tuple[int, int] | None = None,
) -> "Any":
    """Render text onto a surface, anchored by center or topleft.

    Exactly one of center/topleft must be given. Returns the rect the
    text was blitted to, useful for click-detection.
    """
    label = font.render(text, True, color)
    rect = label.get_rect()
    if center is not None:
        rect.center = center
    elif topleft is not None:
        rect.topleft = topleft
    surface.blit(label, rect)
    return rect
