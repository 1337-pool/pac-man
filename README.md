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
make install   # install dependencies
make run       # launch the game with config.json
make debug     # launch under pdb
make lint      # flake8 + mypy
make clean     # remove caches
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
| `highscore_filename` | string | `"highscores.json"` | Path to the persistent highscore file |
| `levels` | list of `{width, height}` | 10 entries, 21×21 each | Maze dimensions per level |
| `lives` | int | `3` | Starting player lives |
| `pacgum` | int | `42` | (reserved for pacgum count tuning) |
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

We chose a flat JSON array (over, say, a database) because the top-10 list is
small, the access pattern is simple (load once at startup, save once at game
end), and it keeps the project dependency-free.

## Maze Generation

We were assigned the `mazegenerator` package (from another 42 group), used
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
`shortest_path` concepts — our player spawn point (middle of the maze) and
ghost pathing are computed independently in `gameplay/level.py`, decoupling us
from the library's own notion of entry/exit.

Per VI.1: level 1 always uses the fixed seed from config (`seed`); subsequent
levels use freshly randomized seeds, so no two playthroughs beyond level 1 are
identical.

## Implementation

TODO: expand once the mandatory part (levels, UI, cheat mode) is fully wired.
Current state: config loading/validation, maze generation/decoding, player and
ghost entities, and highscore persistence are complete and independently
tested. Level assembly, the game loop, cheat mode, and the graphical UI are in
progress.

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
│   ├── entity.py         base class: position, can_move(), move()
│   ├── player.py         lives, score, respawn, lose_life()
│   ├── ghost.py           chasing/edible/eaten state machine, respawn timer
│   └── ghost_behaviors.py  (in progress) chase/flee movement strategies
├── gameplay/
│   ├── level.py           (in progress) assembles maze+player+ghosts+timer
│   ├── game.py            (in progress) main loop, state machine
│   ├── scoring.py         (in progress) point-value wiring
│   └── cheat.py            (in progress) peer-review cheat toggles
├── persistence/
│   └── highscore.py       load/save/validate top-10 JSON highscores
└── ui/                     (in progress) menu, HUD, pause, end screens
```

Design principle followed throughout: each "external boundary" (config file on
disk, the third-party maze package, the highscore file) is wrapped by exactly
one module that owns all the messy validation/error-handling, and exposes a
clean, trusted interface to everything else.

## Project Management

Managed via a GitHub Projects board (Todo / In Progress / Done) with issues
tied to three milestones — `M1: Foundations`, `M2: Full loop`, `M3: Polish` —
and tracked with a Gantt-style timeline view. See [`management/`](./management)
for the timeline, risk analysis, team organization, progress tracking, and
acceptance test plan, including board/timeline screenshots.

Team: berrabia (config, maze adapter, entities, ghosts, highscore, project
management/board), mjaber (Figma design, UI implementation).

## Resources

- [Pac-Man (Wikipedia)](https://en.wikipedia.org/wiki/Pac-Man) — original game
  history and ghost AI behavior reference.
- Python official docs: `json`, `pathlib`, `typing`.
- `mazegenerator` package documentation (assigned peer package) — inspected
  directly via `help()`/`dir()` and source reading rather than external docs.

**AI usage:** Claude (Anthropic) was used throughout this project as a guided
mentor, not a code generator. For every module (`config/loader.py`,
`config/schema.py`, `maze/adapter.py`, `entities/entity.py`,
`entities/player.py`, `entities/ghost.py`, `persistence/highscore.py`), the
workflow was: Claude explained the required behavior and design trade-offs,
one function at a time; the author wrote the code themselves; Claude reviewed
each draft, identified real bugs by tracing through concrete test cases (e.g.
a `for`/`range()` loop that silently failed to skip characters, a seed-reuse
bug that would have made every level identical, a Python `bool`-is-a-subclass-
of-`int` gotcha in config validation, a block-comment terminator that
matched on any `*` instead of the `*/` pair, an unhandled string-literal case
that could corrupt JSON containing `#`), and the author then fixed the code
themselves based on that feedback. Claude also helped scaffold the initial
repository structure, GitHub Projects board/milestones, and this documentation.
No production code in this repository was written directly by AI without the
author writing and understanding it first.
