# Risk Analysis

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Assigned `mazegenerator` package has an undocumented or unstable interface | Medium | High — blocks all maze-dependent work | Inspected the package's public interface (`help()`, `dir()`, and its actual source) before writing any adapter code, rather than assuming its shape. Isolated all direct imports of it inside `src/maze/adapter.py`, so if the package changes or misbehaves, only one file needs to change. |
| Reusing the same seed for every level produces identical mazes | Medium | Medium — breaks game variety, easy to miss since nothing crashes | Caught during code review by explicitly tracing through what value was passed to the generator across levels; fixed by deriving a fresh seed per level after level 1. |
| Config parser silently corrupts values containing `#` inside strings (e.g. a highscore name with a `#`) | Medium | Medium — corrupts JSON, hard to notice since only certain input triggers it | Added explicit string-literal tracking (`in_string` flag) to the comment-stripping logic, with dedicated test cases for this exact scenario. |
| A single malformed entry in the highscore file wipes out all other valid scores | Low-Medium | Medium — player-visible data loss | Deliberately chosen trade-off: the loader raises on any invalid entry rather than silently dropping it, so corruption is surfaced immediately instead of silently losing scores over time. Documented as an explicit design decision, not an oversight. |
| Python's `bool` being a subclass of `int` silently passes invalid config values (e.g. `"lives": true`) as valid integers | Low | Medium — silent, incorrect game behavior | Config validation explicitly checks `isinstance(value, bool)` and rejects it before the `isinstance(value, int)` check, with a dedicated test case. |
| Steam packaging requirements ($100 fee, 30-day mandatory waiting period, native executable requirement) are incompatible with a free, unlisted, short-deadline school submission | High (if Steam were chosen) | High — could block delivery of a graded requirement entirely | Verified Steam's actual requirements before committing to a platform; switched to Itch.io, which the subject explicitly permits and has no fee, no waiting period, and native unlisted-link support. |
| Two-person team working on overlapping areas (UI depends on game logic not yet finished) | Medium | Medium — idle time / merge conflicts | Split work along a dependency-aware boundary: backend/game-logic issues (config, maze, entities, persistence) assigned to berrabia first, since UI cannot be meaningfully built or tested without them; UI/design work (Figma, then implementation) assigned to mjaber, sequenced to start once core entities existed. |
| Ghost AI (`ghost_behaviors.py`) and level assembly (`level.py`) are mutually dependent, risking a stall | Medium | Medium | Deliberately deferred both together rather than half-building one against a moving target; will be tackled as a single connected work session once picked back up. |
| Blocking cheat-mode / packaging work on an unfinished game loop | Low | Low | Correctly sequenced last on the board (M3), so no idle blocked time is expected — by the time we reach them, their dependencies will already be satisfied. |

## Summary

Most risks so far were caught through deliberate code review and testing
rather than surfacing as runtime crashes — several (seed reuse, the string-
comment bug, the bool/int gotcha) would have shipped silently broken if not
specifically traced through with concrete test inputs. Going forward, the
same discipline (trace edge cases by hand before considering a function
"done") is being applied to the remaining gameplay and UI work.
