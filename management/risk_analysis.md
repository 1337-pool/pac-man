# Risk Analysis

## Technical Risks

### 1. External Package Dependency (`mazegenerator`)
* **Risk:** The assigned third-party maze generator could crash, have undocumented behavior, or lack type hints, breaking our game or failing `mypy`.
* **Mitigation:** Created an Adapter pattern (`src/maze/adapter.py`). This is the *only* file that imports the external library. It translates the raw bitmask integers into safe Python dictionaries. We also added `# type: ignore` and `ignore_missing_imports = true` in `mypy` config for external stubs.

### 2. Maze "42" Easter Egg Spawn Trap
* **Risk:** The external generator carves a "42" shape in the center of the maze using integer division. If the maze had an even width/height, the player's default spawn point `(width//2, height//2)` fell directly inside a solid wall, trapping the player instantly.
* **Mitigation:** Reverse-engineered the exact coordinate math used by the generator. Hardcoded the player spawn to the guaranteed empty gap between the '4' and the '2'.

### 3. Configuration Edge Cases
* **Risk:** Malformed `config.json` (e.g., comments inside strings, booleans instead of ints) could crash the game via `json.JSONDecodeError` or silent type coercion.
* **Mitigation:** Wrote a custom `strip_comments` parser that tracks string literals. Added strict type checking in `schema.py` that explicitly rejects `bool` when `int` is expected, falling back to safe defaults with printed warnings instead of tracebacks.

### 4. Platform Packaging Rejection
* **Risk:** Choosing Steam for packaging would result in failure to meet the deadline due to the $100 fee and 30-day mandatory wait period.
* **Mitigation:** Verified platform requirements before starting packaging work. Switched to Itch.io, which supports free, unlisted uploads and Python executables.
