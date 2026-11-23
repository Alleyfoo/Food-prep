# R4 against R4.1: tasks K1–K7 and the eight criteria

## Method

- **The same seven tasks as R4** ([R4 comparison](../ux-integrated-r4/comparison.md)), run by the author in both running prototypes. R4 runs on port 8541 and R4.1 on 8542.
- **The same datasets:**
  1. roasted broccoli, complete knowledge (yogurt, lemon, garlic on hand);
  2. roasted cabbage, incomplete knowledge (lemon on hand);
  3. smashed roasted potato, sparse knowledge (nothing on hand).
- **The same start state as R4:** the ingredient chosen and the on-hand items entered.
- **Steps** are clicks before the answer is on screen.
- **Screenshots** are first screens at 1440 × 900, opened on identical URLs: `screenshots/r4/`, `screenshots/r41/`, and `screenshots/side-by-side/` (R4 left, R4.1 right).
- **Counts** come from `evidence/capture_compare.py` (`screenshots/metrics.json`) and `evidence/text_counts.py` (`evidence/text-counts-output.txt`).
- **There are no participants and no usability scores.**

## K1–K7

R4.1 has R4's architecture, so the step counts are the same. What changes is what has to be **decoded** on the way to the answer.

| Task | Steps (R4 = R4.1) | R4: what must be decoded | R4.1: what is read | Side by side |
| --- | --- | --- | --- | --- |
| **K1 Scan.** Which broccoli preparations have flavour routes? | 0 (column) or 1 (*Has: a flavour route*) | the route column itself is plain. "2/2 req. on hand" and "1/2 req. on hand" are fractions without a named item. 41 legend marks on the page | "Creamy and acidic — all required on hand", "Sour and toasted nut — not on hand: walnut". The context bar says "2 of 5 rows excluded". 0 legend marks | `K1-scan-has-route.png` |
| **K2 Compare** roasted vs steamed | 2 (select, then *compare with roasted broccoli*) | ≠, the six-mark matrix code in the role cells (◇ brown butter ✓, ● lemon), "—" vs hatched; the legend above the table. 63 marks | "differs" / "same" column; "brown butter experimental", "lemon on hand"; "not a listed need" vs "needed, no curated pairing recorded"; A/B letters in the overview, header, context bar and tab. 0 marks | `K2-compare-roasted-steamed.png`, `K2-compare-differences-only.png` |
| **K3 Trace** lemon across broccoli | 1 (any *lemon* link) | the graph is readable (12 edges). The table starts 441 px into the pane, and 33 words are broken mid-word | the same graph above the table (12 ≤ 20). The table starts at 474 px. No broken words. The overview marks the three rows lemon reaches with *in trace* | `K3-trace-lemon.png` |
| **K4 Explain** lemon on roasted broccoli | 0 once the sheet is open | section 4 row: *curated · medium · roast_culinary (culinary) · scope: not recorded*. "scope: not recorded" is repeated under 8 sources | section 4, under the role row "acid · needed · priority medium": *curated · medium · roast_culinary culinary*, and once under the table: "Claim scope: not recorded on any of the 8 source links". Section 6 lists the source once with what it backs | `K4-explain-lemon-detail.png`, `K4-explain-source-roast-culinary.png` |
| **K5 Status** of brown butter | 0 (sheet) or 1 (trace) | section 4 row + section 7 row, connected by "also a Scout idea (same ids)". In the matrix: ◇ + ✓. In the overview: "6 · 1 tasted", which does not say what was tasted | overview row: "experimental pairing: brown butter (fat)" and "tasted: brown butter, works". Section 4: "also a Scout idea for the same pair, tasted: works — see 7". Section 7: *Recorded tasting results* first (2026-08-12, works, conditions). Trace: 2-edge graph + table | `K5-brown-butter-trace.png` |
| **K6 Coverage** of smashed roasted potato | 1 (select) | the overview row's ○○○ 0/3 plus hatched "no curated pairing for acid, herb, fat". 64 marks on the page | "none · 0 of 3 needed roles covered" plus the same hatched gap. Section 8: knowledge gaps, each linked to its section, and "nothing entered as on hand, so availability is not assessed. This is not a gap in the data" | `K6-sparse-potato.png`, `K6-compare-complete-vs-sparse.png` |
| **K7 Filter** cabbage paired with lemon | 1 (*paired with: lemon*) | "1 of 8 match"; 7 greyed rows with reasons; in the matrix, ● lemon | the same, plus "7 of 8 rows excluded" in the context bar. In the matrix: "lemon on hand" | `K7-cabbage-paired-with-lemon.png`, `-matrix.png` |

**Summary.** Every task is answered in the same number of steps as in R4.
- **R4.1 changes how much decoding the answer needs.** Before the answer could be read, R4 needed the dot legend (K1, K6), the matrix legend (K2, K5, K7), the ≠ convention (K2) and the per-link scope repetition (K4). R4.1 needs none of them.
- **K5 is the clearest gain.** The overview now answers it.
- **K4 is unchanged in substance.** The data still records no claim scope on pairing links. R4.1 only stops repeating that eight times.

## The eight criteria

| Criterion | R4 | R4.1 | Evidence |
| --- | --- | --- | --- |
| **1. Information visible without extra navigation** | **Overview:** 5/5, 8/8, 10/10 rows fully in view. **Sheet:** 3, 3, 4 section headings on the first pane screen. **Large traces:** the first relationship row is off the first screen (709, 726 px) | **Overview:** 4/5, 6/8, 6/10 rows. **Sheet:** 3, 3, 2 headings, but all 8 one click away through the index, each with its size. **Large traces:** the table at 195, 212 px. **Mixed**: R4.1 shows fewer overview rows and more trace rows | `overview_rows_visible`, `sections_first_screen`, `trace_table_y` |
| **2. Unexplained symbols** | 39–64 legend-dependent marks per summary overview, 21–23 per matrix, 19–24 per comparison; 5–9 kinds | 0 in every state captured (22 states) | `coded_glyphs`, `text_counts.py`; a test for each dataset |
| **3. Repeated information** | "scope: not recorded" ×8 (broccoli), ×7 (cabbage); the role on every pairing row; the matrix legend repeated in compare | ×1 per table; role rows; no legend in compare. Source-title mentions +2 (citation disclosure). The sheet has 21–36% more words | [detail-and-compare.md](detail-and-compare.md#repetition) |
| **4. Required scrolling** | **Sheet** (pane heights): 4.48 / 3.74 / 1.93. Section 7 at 2,009 px. **Trace step 2:** 5.60 / 3.70. **Compare K2:** 1.64 | **Sheet:** 5.56 / 4.89 / 2.70, but section 7 is 1 click. **Trace step 2:** 3.20 / 2.44. **Compare K2:** 2.09. Scrolling grows in the sheet and compare, and shrinks in large traces | `pane_screens`, `section_offsets` |
| **5. Relationship traceability** | the graph first; the table off screen for large traces; 33–57 broken words; claim scope absent from the trace table | the table first above 20 relationships; the graph one click away (below the table); 0 broken words; claim scope per link when any link has one; the trace reach marked in the overview | [trace-evaluation.md](trace-evaluation.md) |
| **6. Comparison readability** | ≠ and matrix glyphs; "—" vs hatched; compared rows marked by a blue edge only | "differs" / "same"; status in words; "not a listed need" vs "needed, no curated pairing recorded"; A/B/C letters in four places. The comparison is longer (2.09 vs 1.64 pane heights) | `K2-*.png`, [detail-and-compare.md](detail-and-compare.md#comparison) |
| **7. Recorded facts vs hypotheses vs testing** | Kept as separate dimensions in tables. But the overview's *Ideas* left out experimental pairings, section 7 mixed ideas and trials, and the matrix ✓ joined two records in one cell | **Overview:** *Curated pairings* (facts) and *Hypotheses and tastings* are separate columns. **Section 7:** tastings, then experimental pairings, then Scout ideas. ✓ is gone from the matrix. Section 8 separates missing knowledge from missing ingredients | tests `test_tastings_are_grouped…`, `test_missing_knowledge_is_kept_apart…` |
| **8. Context preservation** | **Unchanged and good:** URL state, Back, the context bar. But the trace focus was invisible in the overview and shared blue with compare | **The same state model,** plus **in detail / compare A / traced / in trace** markers in the overview and the sheet title, one colour per concept, the compare set named in the tab and the context bar, and "n of N rows excluded". Local controls tested never to change the subject | `markers` (0 in R4; up to 6 in R4.1), `S-all-selections.png`, tests |

## Per-state numbers

Complete metrics are in `screenshots/metrics.json`. A selection, R4 → R4.1:

| State | Legend marks | Broken words | Overview rows in view | Pane heights | Trace table y (px) |
| --- | --- | --- | --- | --- | --- |
| complete, detail | 44 → 0 | 15 → 0 | 5/5 → 4/5 | 4.48 → 5.56 | |
| complete, matrix | 26 → 0 | 52 → 0 | 5/5 → 5/5 | 5.36 → 6.34 | |
| complete, trace step 1 | 40 → 0 | 0 → 0 | 5/5 → 4/5 | 1.83 → 2.32 | 628 → 644 |
| complete, trace step 2 | 44 → 0 | 57 → 0 | 5/5 → 4/5 | 5.60 → 3.20 | 709 → 195 |
| incomplete, detail | 58 → 0 | 21 → 0 | 8/8 → 6/8 | 3.74 → 4.89 | |
| incomplete, matrix | 24 → 0 | 55 → 0 | 8/8 → 7/8 | 4.77 → 5.63 | |
| incomplete, trace step 2 | 58 → 0 | 21 → 0 | 8/8 → 6/8 | 3.70 → 2.44 | 726 → 212 |
| sparse, detail | 64 → 0 | 2 → 0 | 10/10 → 6/10 | 1.93 → 2.70 | |
| sparse, matrix | 23 → 0 | 9 → 0 | 7/10 → 6/10 | 2.07 → 2.80 | |
| sparse, trace step 2 | 64 → 0 | 1 → 0 | 10/10 → 6/10 | 1.31 → 1.33 | 362 → 374 |
| K2 compare | 63 → 0 | 0 → 0 | 5/5 → 4/5 | 1.64 → 2.09 | |
| K6 compare complete vs sparse | 83 → 0 | 0 → 0 | 10/10 → 7/10 | 1.53 → 1.81 | |
| K7 filter | 59 → 0 | 0 → 0 | 8/8 → 5/8 | 1 → 1 | |

The sheet's "pane heights" for R4.1 are measured with the pane scrolled to the top. The index makes any section one click away regardless of length.

## Where R4.1 is worse

- **Overview density.** Explicit sentences cost about one line per row: 1 to 4 fewer rows fully visible on the first screen. This matters for ingredients with 8 or more preparations.
- **Length.** The sheet is 21–36% longer in words and 0.8–1.2 pane heights taller. The comparison is 0.3–0.5 pane heights taller.
- **Two section headings drop below the first pane screen for the sparse record,** because of the index and the band labels.
- **More words overall.** Every symbol that became a word made the page longer. The bet is that words are faster to read than symbols are to decode. That bet is untested.

## Reproduce

```powershell
py -3.11 -m streamlit run docs/research/ux-integrated-r4/prototype/app.py --server.port 8541
```

```powershell
py -3.11 -m streamlit run docs/research/ux-integrated-r4-1/prototype/app.py --server.port 8542
```

```powershell
py -3.11 docs/research/ux-integrated-r4-1/evidence/capture_compare.py
```

```powershell
$env:PYTHONIOENCODING="utf-8"; py -3.11 docs/research/ux-integrated-r4-1/evidence/text_counts.py
```
