# Regressions — automated and browser results

## Automated
| Run | Result | Evidence |
| --- | --- | --- |
| Full suite, Streamlit 1.50 | **336 passed** | [`evidence/pytest-full.txt`](evidence/pytest-full.txt) |
| App-level tests, Streamlit 1.67 (scratch venv) | **49 passed** | [`evidence/pytest-streamlit-1.67-app-tests.txt`](evidence/pytest-streamlit-1.67-app-tests.txt) |
| New tests on the old code (`src/` stashed) | 21 of 22 fail, as they should | run log in this session |

New file `tests/test_shared_context.py` (22 tests) covers:
- **mapping:** every component → ingredient; the by-product; plate items → `None`; profiled states;
- **shared subject:** consistency across views; changing it anywhere; no broccoli fallback; an ingredient change drops a foreign state; explain-not-substitute; view state kept;
- **availability:** persistence, and display on Explore; the context strip;
- **URL:** write; reload restore; ingredient-only links; unknown ids ignored;
- **tasting:** review writes nothing; back to edit keeps the text and the panel open; confirm writes once, including a replayed stale confirm; navigating away writes nothing;
- **copy:** E0 wording; empty states.

The T5 tests in `tests/test_usability_tasks.py` were updated to the review
flow. `tests/test_ui_state.py` (widget-state preservation) passes with the new
`tc_state_pick` key.

## Browser (Chromium, 1400×900; 375×812; 1400×1700 for the tasting form)
| Check | Result |
| --- | --- |
| Test A walk plus reload | pass (screenshots `after/testA-*`) |
| Test B plus unrepresentable state | pass (`after/testB-1`) |
| Keyboard Tab order and rings | pass, with two pre-existing Streamlit issues (see limitations) |
| Tasting review / edit / confirm / double click | pass after fix `a973110`; one stale frame after a rapid double click |
| 375 px | strip wraps cleanly; no horizontal scroll |
| Console | only connection-refused errors during server restarts |

Not browser-checked on Streamlit 1.67 in this round.
