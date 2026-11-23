# Baseline: the R4 workspace as delivered

R4 is commit `8178afc` on `experimental/ux-integrated-workspace-r4`. It is unchanged on this branch and still runs on port 8541. Every R4.1 comparison uses this build, the same URLs and the same desktop viewport (1440 × 900).

**Sources:**
- the R4 docs (`../ux-integrated-r4/`);
- an expert walkthrough of the running prototype;
- `evidence/capture_compare.py`, columns `r4` in `screenshots/metrics.json`;
- `evidence/text_counts.py`.

Screenshots are in `screenshots/r4/`. The side-by-side versions are in `screenshots/side-by-side/`.

## What R4 already did well (kept as is)

- **The overview never leaves the screen.** Detail, compare and trace share one right-hand pane, and each side scrolls on its own.
- **One URL-held context** (global, shared selection, local), with a context bar and *reset all*. Back undoes the last step.
- **Independent dimensions:** knowledge type, confidence with its field name, availability, evidence with claim scope, testing, coverage, optionality. Records are linked by ids, never merged.
- **Filters grey rows with a reason** instead of removing them.
- **Every K1–K7 task was answered in one workspace,** with no layout switch.

## Where R4 is hard to read

### 1. Information hidden behind symbols

Occurrences of R4's nine legend-dependent marks (●◐○◇✓≠☐☑⇄) in the page text, from `metrics.json`, `coded_glyphs`:

| State | Marks | Kinds |
| --- | --- | --- |
| Complete (broccoli), overview + sheet | 44 | ● ◐ ○ ☐ ⇄ ✓ |
| Incomplete (cabbage), overview + sheet | 58 | ● ◐ ○ ☐ ⇄ |
| Sparse (potato), overview + sheet | 64 | ● ◐ ○ ☐ ⇄ |
| K2 compare (broccoli) | 63 | all nine |
| K6 compare (potato) | 83 | all nine |

What the marks did:
- **Summary overview.** Each row's *Needs* is a dot string (`●◐●◐◐`) plus a bare count (`6/6`).
  - The dots need a three-mark legend.
  - The count does not say what it counts. It is "needed roles with a curated pairing", but it reads just as easily as "on hand".
  - ☐ and ⇄ in every row need the legend too.
- **Matrix.** A six-mark code (name, ● on hand, ◇ experimental, ✓ linked idea tasted, hatched, —). The ✓ mixes two records in one cell: a pairing and the Scout idea for the same pair.
- **Compare.** It reuses the matrix code and prints the whole legend above every comparison, plus ≠ as the difference marker.

### 2. Names broken mid-word

Every table cell had `overflow-wrap:anywhere`. This counts words of three or more letters drawn across two lines (`broken_words`).

| State | Broken words | Examples |
| --- | --- | --- |
| Complete, matrix | 52 | "parmesa / n", "parsl / ey", "past / a", "crouto / ns", "potat / o" |
| Incomplete, matrix | 55 | |
| Complete, trace step 2 | 57 | entity and source names in the trace table |
| K3 trace lemon | 33 | |
| Complete, sheet | 15 | analogy rule names in the ideas table, among others |

### 3. Repeated information

- **"scope: not recorded"** was printed under every pairing source: 8 times in roasted broccoli's sheet, 7 in roasted cabbage's. It is true of all 288 links in the database.
- **The role** was repeated on every pairing row (9 rows, 6 distinct roles for roasted broccoli).
- **Sources** appear in section 4 (title + scope per pairing) and again in section 6 (title, type, linked pairings, scope, self-description).
- **The compare legend** repeats the matrix legend.

### 4. Content spread over a long pane

| Sheet | Pane heights (`pane_screens`) | Section 7 heading starts at |
| --- | --- | --- |
| Roasted broccoli | 4.48 | 2,009 px (3.4 pane heights) |
| Roasted cabbage | 3.74 | 1,613 px |
| Smashed roasted potato | 1.93 | 874 px |

There is no index. Sections are numbered, but the only way to reach 6 or 7 is to scroll.

### 5. A graph that pushes the table off screen

For a preparation at step 2, the graph is drawn first (27–29 nodes, labels around 7 px). The first relationship row starts 709 px into a 596 px pane for roasted broccoli, and 726 px for roasted cabbage. The table, which R4's own readability study called the reliable representation, is never on the first screen for these traces.

### 6. Selections that share or lack markers

| Concept | R4 marker | Problem |
| --- | --- | --- |
| Selected record | yellow row | the context bar calls it "Selected" |
| Compare set | blue left edge + ☑ | the trace focus node in the graph was also blue (`#1a4f8b`) |
| Trace focus | blue graph outline, context bar chip | **no marker in the overview at all**. Tracing lemon gave no sign of which rows the trace reaches |
| Filter exclusion | grey row + reason | fine |

### 7. Mixed kinds of claim in one place

- **Section 7** put Scout ideas and tasting trials in one table, with the trial conditions as a muted line under it.
- **The overview's *Ideas* column** ("6 · 1 tasted") counted Scout ideas and left out experimental pairings, which were visible only in the sheet and the matrix.
- **Missing ingredients** ("not on hand") and **missing knowledge** (hatched) were both spread through the same tables. Section 8 listed only knowledge gaps.

## Baseline numbers used later

The full per-state numbers are in [comparison.md](comparison.md).

| Measure | Complete | Incomplete | Sparse |
| --- | --- | --- | --- |
| Overview rows fully in view, first screen | 5 of 5 | 8 of 8 | 10 of 10 |
| Default overview columns | 7 | 7 | 7 |
| Legend-dependent marks, summary overview | 39 | 57 | 64 |
| Matrix legend | 6 marks, 42 words | | |
| Sheet words | 782 | 622 | 316 |
| "scope: not recorded" in sheet | 8 | 7 | 0 |
| Trace step 2: first relationship row (px into the pane) | 709 | 726 | 362 |
