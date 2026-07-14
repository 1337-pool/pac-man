# Progress Tracking

Snapshot as of the board/timeline screenshots in this directory.

## Status vs. plan

| Milestone | Planned | Actual status | Notes |
|---|---|---|---|
| M1: Foundations | #2, #3, #4, #5 | ✅ All done | Completed roughly on the original plan; maze adapter took slightly longer than expected due to needing to reverse-engineer the assigned package's bitmask encoding by reading its source directly. |
| M2: Full loop | #6, #7, #8, #9, #10 | 🟡 In progress | #9 (highscore) done. #6 (ghost) split: base state machine done, chase/flee AI behaviors deferred to be tackled together with #7 (level assembly), since they're mutually dependent. #10 (UI) started by mjaber in parallel. |
| M3: Polish | #11, #12 | ⬜ Not started | Correctly not started yet — #12 (packaging) cannot begin until the game runs end-to-end. |
| Docs | #13, #14 | 🟡 In progress | This document and its siblings written now, ahead of full game completion, specifically so documentation isn't rushed at the deadline. |

## Deviations from original plan

- **Ghost AI and level assembly grouped together**, rather than done strictly
  in issue-number order. Reasoning: `ghost_behaviors.py` needs a real maze +
  player position to meaningfully test chase logic against, and `level.py`
  needs ghosts to place in the level — building either in isolation would
  mean testing against fake/mocked data now and rewriting later.
- **Packaging platform changed from an initial assumption of Steam to
  Itch.io** after checking Steam's actual requirements (a $100 fee, a
  mandatory 30-day waiting period between payment and release, and a
  requirement for a native desktop executable) — incompatible with a
  free, unlisted, deadline-bound school submission. Caught before any
  packaging work was started, so no wasted effort.
- **Testing deprioritized for simplicity** partway through: the subject
  explicitly marks automated tests as "not submitted or graded" (III.3), so
  the team chose to rely on manual, documented test cases (see
  `test_plan.md`) instead of maintaining a `tests/` directory, to keep the
  repository smaller and reduce maintenance overhead.

## Blocking points so far

See `risk_analysis.md` and `team_org.md` for the full list; none have
caused an actual schedule slip so far, since each was caught during code
review before being merged/relied upon elsewhere.
