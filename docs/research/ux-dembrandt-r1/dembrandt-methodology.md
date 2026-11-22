# Dembrandt methodology — what was used and how

**Source:** [`dembrandt/dembrandt-skills`](https://github.com/dembrandt/dembrandt-skills),
`skills/<name>/SKILL.md`, at commit `905b7a54a8` (2026-11-21). The five files
were read in full through the GitHub API (`gh api … contents/…/SKILL.md`,
raw). **Nothing was installed:** no npm package, no install script, no MCP
server, and no new dependency in this repository.

**Food-prep version audited:** `main` at `7bd7b01`, Streamlit 1.50, Chromium
at 1400×900 and 375×812.

## The five skills and their evaluation procedures

Each skill is a set of principles plus a **review checklist**. The checklists
were the procedure: every item was answered for Food-prep, with evidence, or
marked not applicable. Findings cite the skill and the principle by its own
heading.

| Skill | What it evaluates | Procedure applied |
| --- | --- | --- |
| `nielsen-usability-heuristics` | 10 heuristics, each with a review question | Asked each heuristic's review question of every screen; checked the "Heuristic Review Checklist" table |
| `coordinated-data-views` | Two representations of one dataset kept in sync | Its rule, "any selection or highlight made in one view is immediately reflected in the other", applied to Map ↔ Component Explorer ↔ Journeys, plus its 10-item checklist (shared store, two-way selection, consistent colour, one legend, hover vs selection) |
| `information-architecture` | Naming, structure, navigation, confirm dialogs | Naming audit questions; "Audit for drift" (list every navigation target and label, look for duplicates); invented-term ceiling (~10); 19-item checklist |
| `tab-navigation` | When tabs fit, states, overflow, keyboard, ARIA, persistence, nesting | 12-item checklist, tested in the browser: focus ring, arrow keys, ARIA roles, reload persistence, 375 px overflow, nesting depth |
| `operational-expert-tool-ui` | Dense, persistent, keyboard-driven tools for trained daily users | 10-item checklist, applied with its own scope test: it is for "trained domain specialists … as their primary work surface". Food-prep's users are home cooks, so items that assume that audience are recorded as conflicts, not defects |

## How evidence was gathered

| Method | Used for | Where |
| --- | --- | --- |
| Fresh screenshots via the project's `scripts/capture_screenshots.py` (output redirected; committed README images untouched) | screen-by-screen audit | [`screenshots/`](screenshots/) |
| Browser inspection (DOM, computed styles, keyboard) | ARIA roles, focus visibility, arrow keys, reload persistence, logo link, mobile wrap | [`screenshots/evidence/`](screenshots/evidence/) |
| AppTest probe ([script](screenshots/evidence/dembrandt-probe.py), [output](screenshots/evidence/dembrandt-probe-output.txt)) | nested pill levels per screen, coined-term inventory, error wording, empty states | same folder |
| Code reading | colour semantics, state model, confirm paths | cited by file |
| Prior research reused, not re-run | subject continuity, Map size and labels, rejected-hypothesis dead code | [Qlik/Celonis R1](https://github.com/Alleyfoo/Food-prep/tree/research/ux-qlik-celonis-r1/docs/research/ux-qlik-celonis-r1) (branch `research/ux-qlik-celonis-r1`, not merged into `main`), `docs/usability/2026-11-21-findings.md` |

## What this is not
- **Not user testing.** Every finding is a heuristic judgement or a measured
  fact about the interface. "User impact" lines are predictions unless marked
  otherwise.
- **No scores.** Dembrandt's skills contain none, and none were invented.
- Dembrandt contains ~45 skills; only the five requested were applied.
  Issues that belong to other skills (e.g. no `<h1>`, which is
  `semantic-html-and-seo`) are noted as out of scope.

## Finding format

Every important finding in [`screen-audit.md`](screen-audit.md) and
[`workflow-audit.md`](workflow-audit.md) follows:

> **Observation → Evidence → User impact → Dembrandt principle → Possible remedy → Confidence**

Confidence: **Verified** (observed or measured in the running app or code) ·
**Supported** (verified behaviour, predicted impact) · **Hypothesis**
(needs users).
