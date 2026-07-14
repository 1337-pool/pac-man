# Team Organization

## Members and roles

| Member | Role | Areas owned |
|---|---|---|
| berrabia | Backend / game logic / project management | `config/`, `maze/adapter.py`, `entities/`, `persistence/highscore.py`, GitHub Projects board, milestones, this documentation |
| mjaber | Design / UI | Figma mockups, `ui/` implementation (main menu, HUD, pause menu, end screens) |

## How decisions were made

Work was split along a dependency boundary rather than evenly by file count:
backend/game-logic modules (config, maze, entities, persistence) have no
dependency on visuals and were built first, so that UI work has real,
working data structures to render against instead of guessing at interfaces
that might change. Design work (Figma) started in parallel, since visual
direction doesn't depend on backend internals — only the eventual UI
*implementation* does.

Each backend module went through the same process before being considered
done: implement the smallest working piece, test it against concrete edge
cases (missing files, malformed input, boundary values), fix what breaks,
then move to the next layer. This caught several real bugs before they
reached integration (see `risk_analysis.md`).

## Issue tracking

All work is tracked as GitHub issues attached to one of three milestones
(`M1: Foundations`, `M2: Full loop`, `M3: Polish`) and visualized on a Kanban
board (Todo / In Progress / Done). See `timeline.md` for the current board
state and Gantt view.

## Communication / issue handling

Blocking questions (e.g. how to interpret an ambiguous subject requirement,
which library method to trust) were resolved by directly inspecting the
relevant source — the assigned `mazegenerator` package's actual code, not
assumptions — before writing dependent code. Design trade-offs with more than
one reasonable answer (e.g. how strictly to validate the highscore file, how
to represent `x`/`y` coordinates consistently across all entities) were
made explicitly and documented in code comments and this README, rather than
left as accidental defaults.

## Blocking points encountered

- Coordinate convention ambiguity: an early version of `entity.py` used `x`
  for the row axis and `y` for the column axis (reversed from the usual
  convention). Caught early, before it spread to other files, and flipped to
  the standard convention.
- Steam vs. Itch.io for packaging: initially assumed Steam without checking
  its actual requirements; verified cost/timeline constraints made it
  infeasible for this project and switched to Itch.io before any packaging
  work was started.
