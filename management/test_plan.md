# Acceptance Test Plan

Manual test cases run against each completed module. Not submitted/graded
per the subject (III.3), kept here as evidence of verification.

## config/loader.py

| Test | Expected result | Status |
|---|---|---|
| Valid JSON, no comments | Returns parsed dict | ✅ Pass |
| JSON with `#` line comments | Comments stripped, parses correctly | ✅ Pass |
| JSON with `//` line comments | Comments stripped, parses correctly | ✅ Pass |
| JSON with `/* */` block comments | Comments stripped, parses correctly | ✅ Pass |
| Block comment containing a lone `*` before the real terminator | Only stops at actual `*/` pair | ✅ Pass (bug found & fixed) |
| String value containing `#` (e.g. `"name": "a#b"`) | Preserved untouched, not treated as a comment | ✅ Pass (bug found & fixed) |
| Escaped quote inside a string | String boundary detection not fooled | ✅ Pass |
| Missing file | Raises `ParsingError` with clear message, no traceback | ✅ Pass |
| Wrong file extension (not `.json`) | Raises `ParsingError` | ✅ Pass |
| Malformed JSON | Raises `ParsingError`, no traceback | ✅ Pass |

## config/schema.py

| Test | Expected result | Status |
|---|---|---|
| Empty config `{}` | All defaults applied | ✅ Pass |
| Partial config (some keys present) | Missing keys defaulted, present keys kept | ✅ Pass |
| Wrong type value (e.g. `"lives": "oops"`) | Falls back to default | ✅ Pass |
| Boolean passed where int expected (e.g. `"lives": true`) | Rejected, falls back to default (not silently accepted as `1`) | ✅ Pass (gotcha caught & fixed) |
| `levels` not a list | Falls back to full default level list | ✅ Pass |
| `levels` entry missing `width`/`height` | That entry defaulted individually | ✅ Pass |
| `levels` with fewer than 10 entries | Padded with default entries to reach 10 | ✅ Pass |
| Negative `seed` / `lives` / `level_max_time` | Clamped to default | ✅ Pass |

## maze/adapter.py

| Test | Expected result | Status |
|---|---|---|
| `generate_maze` with valid width/height/seed | Returns a `MazeGenerator` instance, `perfect=False` enforced | ✅ Pass |
| `generate_maze` with negative width/height | Raises `MazeGenerationError` before ever calling the library | ✅ Pass |
| Same seed twice | Produces identical mazes (reproducibility) | ✅ Pass |
| Different seeds | Produce different mazes | ✅ Pass (bug found: seed was hardcoded, fixed) |
| `decode_cell` on known bitmask values (0, 15, 5, ...) | Correct wall dict per bit | ✅ Pass |
| `decode_maze` on a real generated grid | Shape matches input, every cell decoded | ✅ Pass |
| `build_level_maze` end-to-end | Combines generation + decoding correctly, reuses `generate_maze` (not a duplicate raw call) | ✅ Pass (bug found: was bypassing `generate_maze`, fixed) |

## entities/entity.py + player.py

| Test | Expected result | Status |
|---|---|---|
| `can_move` against a real decoded maze | Returns `True` only when no wall in that direction | ✅ Pass (bug found: was inverted, fixed) |
| `move` in each of the 4 directions | Correctly updates `x`/`y` per standard convention | ✅ Pass (coordinate convention flipped for clarity) |
| `move` blocked by a wall | Position unchanged | ✅ Pass |
| `Player.lose_life` at 1 life remaining | Decrements to 0, respawns | ✅ Pass |
| `Player.lose_life` at 0 lives | No further decrement (never goes negative) | ✅ Pass |
| `Player.is_alive` | Correctly reflects `lives > 0` | ✅ Pass |
| `Player.add_score` | Score accumulates correctly | ✅ Pass |

## entities/ghost.py

| Test | Expected result | Status |
|---|---|---|
| `make_edible` while chasing | State becomes `edible` | ✅ Pass |
| `make_edible` while already eaten | State remains `eaten` (not overridden) | ✅ Pass |
| `get_eaten` | State becomes `eaten`, `eaten_at` timestamp recorded, no blocking sleep | ✅ Pass (bug found: `time.sleep()` would have frozen the whole game, fixed) |
| `update()` before delay elapsed | Ghost remains `eaten` | ✅ Pass |
| `update()` after delay elapsed | Ghost respawns to home corner, state resets to `chasing` | ✅ Pass |

## persistence/highscore.py

| Test | Expected result | Status |
|---|---|---|
| Missing file | Returns empty list, not an error | ✅ Pass |
| Empty file | Returns empty list | ✅ Pass |
| Genuinely malformed JSON (not just empty) | Raises `ScoreFileError` | ✅ Pass (bug found: was misclassified as "empty," fixed) |
| Valid file with 10 valid entries | Loads correctly | ✅ Pass |
| Entry with name > 10 characters | Raises `ScoreFileError` | ✅ Pass |
| Entry with non-alphanumeric/space character in name | Raises `ScoreFileError` | ✅ Pass |
| Entry with score of exactly `0` | Accepted (not rejected as falsy) | ✅ Pass (bug found: `not player.get("score")` rejected legitimate 0 scores, fixed) |
| Entry with negative score | Raises `ScoreFileError` | ✅ Pass |
| `save_highscores` with valid entries | Sorted descending, truncated to top 10, written to disk | ✅ Pass |
| `save_highscores` does not mutate caller's list | Caller's original list order unchanged | ✅ Pass |
| `save_highscores` with an invalid entry | Raises before writing anything to disk | ✅ Pass |
| Write failure (e.g. unwritable path) | Raises `ScoreFileError`, no raw traceback | ✅ Pass |

## Remaining / not yet tested

Level assembly, full game loop, cheat mode, and UI have not been built yet as
of this document — test cases for those will be added as each is completed.
