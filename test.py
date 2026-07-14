"""Standalone preview for the Home, Highscores, and Instructions screens.

This is a lightweight manual test harness, not part of the graded
game loop. Run it with:

    python3 ui_preview.py

Click the on-screen buttons (or press ESC on the sub-screens) to
navigate between Home -> Highscores / Instructions -> back to Home.
Close the window or press Ctrl+C to quit.
"""

import sys

import pygame

from src.ui import HighscoreScreen, HomeScreen, InstructionsScreen
from src.ui.theme import SCREEN_HEIGHT, SCREEN_WIDTH

HIGHSCORE_FILENAME = "highscore.json"


def main() -> None:
    """Run the preview window's event loop."""
    pygame.init()
    try:
        surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Pac-Man - bilal kamel")
        clock = pygame.time.Clock()

        home = HomeScreen(HIGHSCORE_FILENAME)
        highscores = HighscoreScreen(HIGHSCORE_FILENAME)
        instructions = InstructionsScreen()

        current = "home"
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    continue

                if current == "home":
                    action = home.handle_event(event)
                    if action == "start":
                        print("[preview] START GAME pressed (not wired up yet)")
                    elif action == "highscores":
                        current = "highscores"
                    elif action == "instructions":
                        current = "instructions"
                    elif action == "exit":
                        running = False
                elif current == "highscores":
                    if highscores.handle_event(event) == "back":
                        current = "home"
                elif current == "instructions":
                    if instructions.handle_event(event) == "back":
                        current = "home"

            if current == "home":
                home.draw(surface)
            elif current == "highscores":
                highscores.draw(surface)
            elif current == "instructions":
                instructions.draw(surface)

            pygame.display.flip()
            clock.tick(60)
    finally:
        pygame.quit()


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # pragma: no cover - manual preview only
        print(f"Preview crashed: {exc}")
        sys.exit(1)
