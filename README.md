*This project has been created as part of the 42 curriculum by berrabia, mjaber.*

# Pac-Man

## Description

A from-scratch recreation of the classic 1980 arcade game Pac-Man, built in Python
with an object-oriented, modular architecture. The game features JSON-based
configuration, procedurally generated mazes (via an externally assigned
`mazegenerator` package), autonomous ghost AI, a persistent highscore system, and
a full graphical UI (main menu, HUD, pause menu, game-over/victory screens).

The goal of this project is to reproduce the core Pac-Man gameplay loop — collect
pacgums, avoid or hunt ghosts using power pellets, progress through at least 10
increasingly randomized levels — while following clean software engineering
practices: type hints, docstrings, no unhandled crashes, and a clear separation
between our code and the third-party maze generator.

## Instructions

```bash
make install     # install dependencies
make run         # launch the game with config.json
make debug       # launch under pdb
make lint        # flake8 + mypy
make lint-strict # flake8 + mypy --strict
make clean       # remove caches
```

Manual launch:
```bash
python3 pac-man.py config.json
```

The program takes exactly one argument: a path to a JSON configuration file.

## Configuration

The config file is standard JSON with comment support. Lines starting with `#`,
`//` line comments, and `/* ... */` block comments are stripped before parsing.
Comment markers inside string values (e.g. `"name": "a#b"`) are preserved
correctly — comment detection is disabled while inside a string literal.

| Key | Type | Default | Description |
|---|---|---|---|
| `highscore_filename` | string | `"highscore.json"` | Path to the persistent highscore file |
| `levels` | list of `{width, height}` | 10 entries, 21×21 each | Maze dimensions per level |
| `lives` | int | `3` | Starting player lives |
| `points_per_pacgum` | int | `10` | Score awarded per pacgum eaten |
| `points_per_super_pacgum` | int | `50` | Score awarded per super-pacgum eaten |
| `points_per_ghost` | int | `200` | Score awarded per edible ghost eaten |
| `seed` | int | `42` | Fixed seed for level 1's maze |
| `level_max_time` | int | `90` | Seconds allowed per level |

**Faulty config handling:** any missing key falls back to its default. Any key
present with the wrong type, or a value outside a sane range (e.g. a maze
dimension below 9 or above 51, a boolean passed where an int is expected), is
clamped to the default with a printed warning — the game never crashes on a bad
config. Unknown/extra keys are silently ignored. The `levels` list is padded
with default entries if it has fewer than 10, and each entry's `width`/`height`
is validated independently.

## Highscore

Highscores are stored as a flat JSON array of `{"name": ..., "score": ...}`
objects, sorted descending by score, capped at the top 10 entries. The file
path is configurable via `highscore_filename`.

**Validation rules enforced on both load and save** (so a corrupt or malicious
file can never silently get further corrupted, and the game can never write a
file it wouldn't later be able to read back):
- `name`: string, max 10 characters, alphanumeric and spaces only.
- `score`: non-negative integer.
- A missing file is treated as "no scores yet" (returns an empty list), not an
  error.
- An empty file is treated the same way.
- A file that exists but contains genuinely malformed JSON, or entries
  violating the rules above, raises a clean `ScoreFileError` — never a raw
  traceback.

## Maze Generation

We were assigned the `mazegenerator` package, used
as-is via `src/maze/adapter.py` — the only file in our codebase that imports it
directly.

**Interface used:**
```python
MazeGenerator(size=(width, height), perfect=False, seed=seed)
```
- `perfect` is always hardcoded to `False`, per the subject requirement (V.4),
  to produce Pac-Man-compatible corridors (loops, not just a spanning tree).
- `.maze` returns a `list[list[int]]` bitmask grid, where each cell's value
  (0–15) encodes which of its 4 walls are present: bit `1`=North, `2`=East,
  `4`=South, `8`=West.

**Our adapter** decodes this bitmask grid into a plain `list[list[dict]]` where
each cell is `{"north": bool, "east": bool, "south": bool, "west": bool}` (a
wall is `True`). Nothing outside `adapter.py` ever touches the raw int grid or
knows the bitmask encoding — the rest of the codebase only speaks in terms of
these wall dictionaries.

We deliberately do not use the library's own `entry_cell`/`exit_cell`/
`shortest_path` concepts — our player spawn point (the gap in the "42" shape carved
by the generator) and ghost pathing are computed independently in 
`gameplay/level.py`, decoupling us from the library's own notion of entry/exit.

Per VI.1: level 1 always uses the fixed seed from config (`seed`); subsequent
levels use freshly randomized seeds, so no two playthroughs beyond level 1 are
identical.

## Implementation

The game is fully implemented and playable end-to-end. The core game loop is
managed by `gameplay/game.py`, which acts as a finite state machine handling
navigation between the Main Menu, Highscores, Instructions, Playing, Paused,
Game Over, and Victory screens. 

`gameplay/level.py` assembles the maze, player, ghosts, and pacgums.

A `CheatManager` class handles peer-review cheats (invisibilty, ghost freeze,
speed boost, and timer freeze) all toggled simultaneously via the `F1` key. The
UI is rendered using Pygame, drawing a classic blue-walled maze, animated 
entities (2-frame sprite animation for the player), and a fully interactive HUD 
and menu system.

## General Software Architecture

```
pac-man.py              entry point: parse argv, load+validate config, launch game
src/
├── config/
│   ├── loader.py        JSON+comments parsing, raises ParsingError cleanly
│   └── schema.py         defaults, type/range validation, clamping
├── maze/
│   └── adapter.py        isolates mazegenerator; decodes bitmask -> wall-dicts
├── entities/
│   ├── entity.py         base class: position, can_move(), move(), smooth interp
│   ├── player.py         lives, score, respawn, 2-frame sprite animation
│   ├── ghost.py           chasing/edible/eaten state machine, teleport-on-eaten
│   └── ghost_behaviors.py  full BFS pathfinding + 4 distinct ghost personalities
├── gameplay/
│   ├── level.py           assembles maze+player+ghosts+pacgums, handles collisions
│   ├── game.py            main loop, state machine, HUD, screen routing
│   └── cheat.py            peer-review cheat toggles (F1)
├── score_handler/
│   └── highscore.py       load/save/validate top-10 JSON highscores
└── ui/                     
    ├── theme.py            colors, fonts, load_sprite()
    ├── button.py           reusable UI button widget
    ├── maze_renderer.py    draws classic blue walls with rounded corners
    ├── home_screen.py      main menu
    ├── highscore_screen.py top 10 leaderboard view
    └── instructions_screen.py controls and rules reference
```


## Project Management

Managed via a GitHub Projects board (Todo / In Progress / Done) with issues
tied to three milestones — `M1: Foundations`, `M2: Full loop`, `M3: Polish` —
and tracked with a Gantt-style timeline view. See [`management/`](./management)
for the timeline, risk analysis, team organization, progress tracking, and
acceptance test plan, including board/timeline screenshots.

Team:
- mjaber (Figma design, UI implementation, ghosts algo, game loop),
- berrabia (config, maze adapter, entities, ghosts, highscore, project
management/board).

## Resources

- https://www.youtube.com/watch?v=9H27CimgPsQ&pp=ygUNcGFjbWFuIHB5dGhvbg%3D%3D
- [Pac-Man (Wikipedia)](https://en.wikipedia.org/wiki/Pac-Man) — original game
  history and ghost AI behavior reference.
- Python official docs: `json`, `pathlib`, `typing`.
- `mazegenerator` package documentation — inspected directly.

**AI usage:**
AI  was used strictly as a mentor and reviewer, not a code generator. AI helped explain design trade-offs, reviewed drafts to catch logic bugs and edge cases, and assisted in scaffolding the repository structure and documentation. No production code in this repository was written directly by AI.