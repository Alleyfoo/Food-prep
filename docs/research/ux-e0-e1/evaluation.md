# Evaluation — before / after

Same scenarios on `main` (`7bd7b01`, before) and this branch (after). **These
are automated walkthroughs, not user testing.** Counts are programmatic
interactions: a lower bound on what a person does.

Evidence: [`evidence/trace-before.txt`](evidence/trace-before.txt),
[`evidence/trace-after.txt`](evidence/trace-after.txt) (same script,
[`trace_probe.py`](evidence/trace_probe.py)), [`evidence/testE-output.txt`](evidence/testE-output.txt),
and screenshots in `screenshots/before/` and `screenshots/after/`.

## Metrics

| Metric | Before | After |
| --- | --- | --- |
| **Repeated selections**, Test A (roasted cabbage, 6 views) | 5 re-picks | 0 |
| **Repeated selections**, Test B (switch to roasted tomato) | 5 re-picks | 0 |
| **Navigation steps** after the first selection, Test A | 13 | 6 (navigation only) |
| **Views showing the wrong subject** after one selection | 5 of 6 (broccoli or the previous subject) | 0 of 6 |
| **Context loss** returning to the start view | subject kept; position lost | subject and on-hand list kept |
| **State recovery** after reload | nothing (Cook, default subject, empty on-hand list) | subject, on-hand list and tab restored from the URL |
| **Keyboard focus** on rails, buttons, expander | none visible on rails | 3 px ring, verified by Tab in the browser |
| **Error prevention**, tasting | one click wrote permanently | review step; Back to edit keeps text; a rapid double click wrote exactly one entry |
| **Explanation consistency** (unrecorded pairing, Test E) | "Not paired here yet" (cards) vs "no match" (hint) | same words everywhere; no negative claim on any screen |

## Tests A–E

- **A, roasted cabbage:** every view follows it. Map shows cabbage with roasted
  cabbage ringed; Journeys shows the new catalogue-gap empty state; reload
  restores everything. Screenshots `after/testA-1…5`, baseline
  `before/testA-1…2` (Taste Circle fell back to roasted broccoli).
- **B, change subject:** choosing roasted tomato in Scout moved every view. A
  state without a flavour profile (canned tomato base) is **explained, not
  substituted**, in Taste Circle and Scout (`after/testB-1`).
- **C, keyboard:** Tab order is logical (picker → candidate buttons → Next →
  Record a tasting); every button and pill showed the ring; arrow keys switch
  sections. Two pre-existing Streamlit problems were found; see limitations.
- **D, tasting, isolated file:** plain-language validation; review showed the
  exact entry; Back to edit kept the text (after fix `a973110`); the edited
  text was saved; two rapid clicks appended exactly one entry. The real
  `tastings.yaml` was unchanged (checksum).
- **E, unknown relationship:** mango with roasted cabbage reads "Not paired
  here yet" in both explorers and "No pairings are recorded… missing catalogue
  knowledge" in Filler Profiles. Scout is silent. No screen says "incompatible".

## What this does not show
Whether people *want* the subject to follow them (E1b) or would prefer E1a, and
whether the strip is noticed. Run the task scripts with real users.
