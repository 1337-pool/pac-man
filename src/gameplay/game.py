from __future__ import annotations

import pygame
import random
import time
import enum

from src.ui.theme import (
    BLACK, WHITE, YELLOW, SCREEN_WIDTH, SCREEN_HEIGHT,
    body_font, display_font, draw_text
)
from src.ui.maze_renderer import draw_maze
from src.ui import HomeScreen, HighscoreScreen, InstructionsScreen

from src.gameplay.level import Level
from src.gameplay.cheat import CheatManager
from src.score_handler.highscore import load_highscores, save_highscores, ScoreFileError


class GameState(enum.Enum):
    HOME = 1
    HIGHSCORES = 2
    INSTRUCTIONS = 3
    PLAYING = 4
    PAUSED = 5
    GAME_OVER = 6
    VICTORY = 7


class Game:
    def __init__(self, config: dict) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Pac-Man khaliha 3ala lah")
        self.clock = pygame.time.Clock()
        self.running = True
        self.config = config
        self.highscore_filename = config.get("highscore_filename")
        self.home_screen = HomeScreen(self.highscore_filename)
        self.highscore_screen = HighscoreScreen(self.highscore_filename)
        self.instructions_screen = InstructionsScreen()

        self.state = GameState.HOME
        self.level: Level | None = None
        self.current_level_index = 0
        self.next_dir: str | None = None

        self.level_start_time = 0.0
        self.elapsed_time = 0.0
        self.level_max_time = config.get("level_max_time", 90)
        self.default_lives = config.get("lives", 3)

        # Cheat state
        self.cheats = CheatManager()
        self.default_move_frames = 15

        # Highscore entry state
        self.player_name = ""
        self.name_entry_active = False

    def run(self) -> None:
        while self.running:
            self._handle_events()
            self._update()
            self._draw()
            self.clock.tick(60)
        pygame.quit()

    def _start_level(self, index: int) -> None:
        levels = self.config.get("levels", [])
        if index >= len(levels):
            self.state = GameState.VICTORY
            self.name_entry_active = True
            self.player_name = ""
            return

        level_data = levels[index]
        width = level_data.get("width", 21)
        height = level_data.get("height", 21)
        
        # First level uses config seed, subsequent levels are random
        seed = self.config.get("seed", 42) if index == 0 else random.randint(0, 10000)

        # Carry over score and lives if we already have a player
        old_score = self.level.player.score if self.level else 0
        old_lives = self.level.player.lives if self.level else self.default_lives

        self.level = Level(
            width=width,
            height=height,
            seed=seed,
            lives=old_lives,
            img="pacman",
            cheat_manager=self.cheats,
            points_per_ghost=self.config.get("points_per_ghost", 200),
            points_per_pacgum=self.config.get("points_per_pacgum", 10),
            points_per_super_pacgum=self.config.get("points_per_super_pacgum", 50),
        )
        
        # Restore carried-over score
        self.level.player.score = old_score
        
        # Apply speed boost immediately if cheat is already active
        if self.cheats.speed_boost:
            self.level.player.move_frames = max(12, self.default_move_frames - 2)
            
        self.level_start_time = time.time()
        self.elapsed_time = 0.0
        self.next_dir = "east"  # Give player initial momentum
        self.state = GameState.PLAYING

    def _handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                continue

            if self.state == GameState.HOME:
                action = self.home_screen.handle_event(event)
                if action == "start":
                    self.current_level_index = 0
                    self._start_level(0)
                elif action == "highscores":
                    self.state = GameState.HIGHSCORES
                elif action == "instructions":
                    self.state = GameState.INSTRUCTIONS
                elif action == "exit":
                    self.running = False

            elif self.state == GameState.HIGHSCORES:
                if self.highscore_screen.handle_event(event) == "back":
                    self.state = GameState.HOME

            elif self.state == GameState.INSTRUCTIONS:
                if self.instructions_screen.handle_event(event) == "back":
                    self.state = GameState.HOME

            elif self.state == GameState.PLAYING:
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_UP, pygame.K_w):
                        self.next_dir = "north"
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        self.next_dir = "south"
                    elif event.key in (pygame.K_LEFT, pygame.K_a):
                        self.next_dir = "west"
                    elif event.key in (pygame.K_RIGHT, pygame.K_d):
                        self.next_dir = "east"
                    elif event.key in (pygame.K_ESCAPE, pygame.K_SPACE):
                        self.state = GameState.PAUSED
                        
                    # --- TOGGLE ALL CHEATS ---
                    elif event.key == pygame.K_F1:
                        self.cheats.toggle_all_cheats()
                        if self.cheats.speed_boost:
                            self.level.player.move_frames = max(12, self.default_move_frames - 2)
                        else:
                            self.level.player.move_frames = self.default_move_frames

            elif self.state == GameState.PAUSED:
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_ESCAPE, pygame.K_SPACE):
                        # Adjust start time to account for pause duration
                        self.level_start_time = time.time() - self.elapsed_time
                        self.state = GameState.PLAYING
                    elif event.key == pygame.K_q:
                        self.state = GameState.HOME

            elif self.state in (GameState.GAME_OVER, GameState.VICTORY):
                if self.name_entry_active:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            self._save_score()
                            self.name_entry_active = False
                            self.state = GameState.HOME
                        elif event.key == pygame.K_BACKSPACE:
                            self.player_name = self.player_name[:-1]
                        else:
                            # Subject V.5: max 10 chars, alphanumeric/space only
                            char = event.unicode
                            if char.isalnum() or char.isspace():
                                if len(self.player_name) < 10:
                                    self.player_name += char
                else:
                    if event.type == pygame.KEYDOWN:
                        self.state = GameState.HOME
    def _update(self) -> None:
        if self.state != GameState.PLAYING or self.level is None:
            return

        # Attempt continuous movement
        if not self.level.player.is_moving:
            moved = False
            
            # 1. Try to apply the new requested direction (next_dir)
            if self.next_dir:
                moved = self.level.player.move(self.level.maze, self.next_dir)
            
            # 2. If the new direction was blocked (hit a wall), 
            # continue in the current direction so momentum doesn't stop!
            if not moved and self.level.player.direction:
                self.level.player.move(self.level.maze, self.level.player.direction)

        self.level.update()

        # --- TIMER FREEZE LOGIC ---
        if not self.cheats.freeze_timer:
            self.elapsed_time = time.time() - self.level_start_time
        else:
            # Keep syncing the start time so elapsed_time doesn't jump when unfrozen
            self.level_start_time = time.time() - self.elapsed_time
        # --------------------------

        # Check level time limit
        if self.elapsed_time > self.level_max_time:
            self.state = GameState.GAME_OVER
            self.name_entry_active = True
            self.player_name = ""
            return

        # Check player death
        if not self.level.player.is_alive():
            self.state = GameState.GAME_OVER
            self.name_entry_active = True
            self.player_name = ""
            return

        # Check level completion
        if self.level.is_level_complete():
            self.current_level_index += 1
            self._start_level(self.current_level_index)

    def _draw(self) -> None:
        self.screen.fill(BLACK)

        if self.state == GameState.HOME:
            self.home_screen.draw(self.screen)
        elif self.state == GameState.HIGHSCORES:
            self.highscore_screen.draw(self.screen)
        elif self.state == GameState.INSTRUCTIONS:
            self.instructions_screen.draw(self.screen)
        elif self.state in (GameState.PLAYING, GameState.PAUSED, GameState.GAME_OVER, GameState.VICTORY):
            self._draw_game()
            
            if self.state == GameState.PAUSED:
                self._draw_overlay("PAUSED", "ESC/SPACE to RESUME | Q to QUIT")
            elif self.state in (GameState.GAME_OVER, GameState.VICTORY):
                self._draw_end_screen()

        pygame.display.flip()

    def _draw_game(self) -> None:
        if self.level is None:
            return

        # Calculate board dimensions
        board_area_w = SCREEN_WIDTH - 100
        board_area_h = SCREEN_HEIGHT - 200
        cell_size = min(board_area_w // self.level.width, board_area_h // self.level.height)
        cell_size = max(8, cell_size)  # Prevent 0 or negative size
        
        board_w = self.level.width * cell_size
        board_h = self.level.height * cell_size
        board_x = (SCREEN_WIDTH - board_w) // 2
        board_y = ((SCREEN_HEIGHT - board_h) // 2) + 40  # Push down for HUD

        # Draw HUD
        self._draw_hud()

        # Draw Maze
        draw_maze(self.screen, self.level.maze, board_x, board_y, cell_size)

        # Draw Pacgums
        for px, py in self.level.pacgums:
            cx = board_x + px * cell_size + cell_size // 2
            cy = board_y + py * cell_size + cell_size // 2
            pygame.draw.circle(self.screen, YELLOW, (cx, cy), max(1, cell_size // 6))

        # Draw Super-Pacgums
        for px, py in self.level.super_pacgums:
            cx = board_x + px * cell_size + cell_size // 2
            cy = board_y + py * cell_size + cell_size // 2
            pygame.draw.circle(self.screen, YELLOW, (cx, cy), max(3, cell_size // 4))

        # Draw Entities
        self.level.player.draw(self.screen, board_x, board_y, cell_size)
        for ghost in self.level.ghosts:
            ghost.draw(self.screen, board_x, board_y, cell_size)

    def _draw_hud(self) -> None:
        if self.level is None:
            return

        score = self.level.player.score
        lives = self.level.player.lives
        level = self.current_level_index + 1
        time_left = max(0, int(self.level_max_time - self.elapsed_time))

        # Top Bar
        draw_text(self.screen, f"SCORE: {score}", body_font(20), WHITE, topleft=(40, 30))
        draw_text(self.screen, f"LEVEL: {level}", body_font(20), WHITE, topleft=(SCREEN_WIDTH // 2 - 40, 30))
        
        timer_surf = body_font(20).render(f"TIME: {time_left}", True, YELLOW)
        timer_rect = timer_surf.get_rect(topright=(SCREEN_WIDTH - 40, 30))
        self.screen.blit(timer_surf, timer_rect)

        # Lives (draw small circles)
        for i in range(lives):
            pygame.draw.circle(self.screen, YELLOW, (50 + i * 25, SCREEN_HEIGHT - 40), 8)
            
        # Cheat Indicator
        if self.cheats.all_active:
            draw_text(self.screen, "[F1] CHEAT MODE ACTIVE", body_font(14), (255, 0, 0), topleft=(40, 60))

    def _draw_overlay(self, title: str, subtitle: str) -> None:
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        draw_text(self.screen, title, display_font(60), YELLOW, center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))
        draw_text(self.screen, subtitle, body_font(20), WHITE, center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))

    def _draw_end_screen(self) -> None:
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, (0, 0))

        title = "GAME OVER" if self.state == GameState.GAME_OVER else "YOU WIN!"
        color = (255, 50, 50) if self.state == GameState.GAME_OVER else YELLOW
        
        draw_text(self.screen, title, display_font(60), color, center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80))
        draw_text(self.screen, f"Final Score: {self.level.player.score if self.level else 0}", body_font(24), WHITE, center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))

        if self.name_entry_active:
            draw_text(self.screen, "ENTER YOUR NAME:", body_font(20), WHITE, center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
            
            # Draw input box
            input_rect = pygame.Rect(0, 0, 300, 50)
            input_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 90)
            pygame.draw.rect(self.screen, BLACK, input_rect)
            pygame.draw.rect(self.screen, YELLOW, input_rect, width=2)
            
            draw_text(self.screen, self.player_name + "_", body_font(24), YELLOW, center=input_rect.center)
            draw_text(self.screen, "PRESS ENTER TO SAVE", body_font(14), WHITE, center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 140))
        else:
            draw_text(self.screen, "PRESS ANY KEY TO RETURN TO MENU", body_font(16), WHITE, center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))
    def _save_score(self) -> None:
        if self.level is None:
            return
            
        name = self.player_name.strip() or "ANON"
        new_score = self.level.player.score
        
        try:
            scores = load_highscores(self.highscore_filename)
        except ScoreFileError:
            scores = []
            
        # --- CHECK FOR DUPLICATE NAME ---
        found_existing = False
        for entry in scores:
            if entry["name"] == name:
                # Name exists: override the score only if the new one is higher
                if new_score > entry["score"]:
                    entry["score"] = new_score
                found_existing = True
                break
                
        # If the name was not found in the list, add it as a new entry
        if not found_existing:
            scores.append({
                "name": name,
                "score": new_score
            })
        # --------------------------------
        
        try:
            save_highscores(self.highscore_filename, scores)
        except ScoreFileError:
            pass  # Fail silently to avoid crashes (subject III.1)