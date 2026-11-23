# Baseline — Ingredient Explorer before E3

**Build:** `experimental/ux-shared-context` at `f4ba729` (E0 + E1), captured
before any E3 change on `experimental/ux-answer-first`.
**Captures:** `screenshots/baseline/`. Each scenario has a first-screen crop
(`*-desktop.png` 1400×900, `*-phone.png` 390×844) and a tall capture
(`*-full.png`), produced with
[`evidence/capture_ab.py`](evidence/capture_ab.py) `baseline`.
**Accessible copy:**
[`evidence/baseline-T1-visible-text.txt`](evidence/baseline-T1-visible-text.txt)
is the full visible text of the T1 scenario, in reading order (from R2's
walkthrough of the same build).
**Measurements:** [`screenshots/baseline/metrics.json`](screenshots/baseline/metrics.json).

## Scenario: broccoli, with yogurt, lemon and garlic on hand

**Navigation** from a fresh load:
1. The app opens on Cook › Ingredient Explorer, with broccoli / roasted
   broccoli preselected (the app default).
2. Enter yogurt, lemon and garlic in "What do I have right now?" (three
   picks).
3. Scroll and read.

No tab change is needed, because the default subject happens to be broccoli.

**Visible hierarchy, top to bottom** (desktop):

| Order | What | Emphasis |
| --- | --- | --- |
| 1 | Header, on-hand box, Cook / Explore / Experiment, tab rail | — |
| 2 | Strip: "INVESTIGATING Roasted broccoli · from broccoli · AVAILABLE yogurt, lemon, garlic" | small grey |
| 3 | Left: "Ingredient: broccoli", the B disc, "5 ways to transform it, ranked cooking before preservation", Mode pills | — |
| 4 | "SHOWING TOP 5 OF 5 BRANCHES · RANKED COOKING-BEFORE-PRESERVATION" | eyebrow |
| 5 | **Raw Assemble** (raw broccoli): tags, risks, missing, available now (lemon), missing but useful, not paired here yet (garlic, yogurt), use in | **accent border** (rank 1) |
| 6 | "● The dish you are investigating" | eyebrow |
| 7 | **Roast** (roasted broccoli): 11 rows. Row 9 is "Routes with what you have: **Creamy and acidic** — yogurt, lemon · also needs dill" | none |
| 8 | Steam, Stir Fry, Soup | none |

**Steps to locate the suggestion:**
1. Pass the whole of card 1, which is the bordered, wrong preparation.
2. Find the marker.
3. Read 8 rows of card 2.

**Measured:**
- The first "Creamy and acidic" sits **1,464 px** down at 1400 px (1.63
  first screens), with **40 chips** drawn above it.
- On a phone it is **2,724 px** down (3.23 screens), with 38 chips above.
- The bordered card is **raw broccoli**. The subject is roasted broccoli.

## The other scenarios (same build)

| Scenario | Bordered card | Investigated card position | Chips above the target |
| --- | --- | --- | --- |
| T2 roasted tomato (deep link) | charred tomato | target "basil" (a next move on the roasted tomato card) at 1.21 screens desktop / 2.85 phone | 32 / 34 |
| T3 smashed roasted potato | baked potato | **not shown**. It ranks below the top five; a hint points to *Choose technique* | — |
| T4 switch to roasted cabbage (via Component Explorer) | braised cabbage | 2.81 screens desktop / 5.21 phone (card 5 of 8) | 92 |
| default (no on-hand) | raw broccoli | the marker on card 2 | — |

In **every** scenario the accent border is on a card that is *not* the
prepared ingredient being investigated. In T3 the investigated card is not
on the screen at all.

## Before images of the two repairs
- `screenshots/baseline/taste-circle-arrows-before.png`: bare ◀ ▶, a
  "40 / 56" counter, and a tooltip "Next component" (from R2).
- `screenshots/baseline/tasting-saved-before.png`: "Saved to C:\…\tastings.yaml.
  Commit that file to keep the record…" (from R2's T5).
- The verdict defaulted to "Works" (`_tasting_reset`, R2 finding N11).
