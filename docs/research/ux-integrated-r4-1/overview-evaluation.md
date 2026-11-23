# Overview: explicit text against symbols and counts

**Question (Phase 2).** Can the overview show the important differences between preparations without asking people to decode symbol sequences, and without adding columns?

**Method.** Three presentations were compared on the same three datasets:
- R4's coded summary;
- an explicit-sentence variant, the first R4.1 render, observed in the browser and not kept as a screenshot;
- the final R4.1 compact sentences.

Counts come from `evidence/text_counts.py` and `screenshots/metrics.json`. There are no participants.

## The six things the overview has to show

| Item | R4 (compact code) | R4.1 (labelled summary) | Meaning apparent without a legend? |
| --- | --- | --- | --- |
| Needed culinary roles | `●◐●◐◐ 6/6` | "8 pairings · all 6 needed roles covered" / "3 of 4 needed roles covered" / "none · 0 of 3 needed roles covered" | **R4: no.** It needs the dot legend, and "6/6" could mean covered or on hand. **R4.1: yes.** The denominator is named ("needed roles") and so is the property ("covered", under the heading *Curated pairings*) |
| Recorded pairings | only in the tooltip and the matrix | count in the same line: "8 pairings" | yes |
| Available ingredients | ● inside the dot string, for a role whose curated pairing is on hand; "2/2 req. on hand" on routes | "on hand: lemon (acid)" or "none on hand". On routes: "all required on hand" or "not on hand: walnut" | **R4: partly.** "1/2 req. on hand" does not say *which*. **R4.1: yes, and it names the missing item** |
| Flavour-route coverage | route names + "x/y req. on hand" | route names + the availability line. When no row has a route, the column is dropped and the banner says so once | yes in both. R4.1 removes a column that was empty on all 10 potato rows |
| Experimental ideas and tastings | "6 · 1 tasted" (Scout ideas only) | "experimental pairing: brown butter (fat)" · "6 Scout ideas" · "tasted: brown butter, works" | **R4: no.** It did not say what the 6 were, and experimental pairings were absent from the overview. **R4.1: yes,** in a column separate from the curated facts |
| Missing information | row-specific gaps, hatched; shared gaps in a banner | the same, with knowledge gaps only. Missing ingredients go in the pairings and routes columns, never here | yes in both. R4.1 keeps the two kinds of absence in different columns |

Row controls: R4 used ☐ ☑ ⇄; R4.1 uses *add to compare*, *compare with roasted broccoli*, *remove from compare* and *trace*.

## The three presentations tried

### 1. Explicit sentences (first R4.1 render, rejected)

An example cell: "all 6 needed roles have a curated pairing / 8 curated pairings recorded / on hand: lemon (acid)", under a header that itself ran four lines ("Culinary roles and curated pairings").

At 10/21 of the width, cells wrapped to 5–7 lines, and only about three of the five broccoli rows fitted on the first screen. It was unambiguous, but the overview stopped working as an index for scanning rows.

### 2. Compact labelled summary (adopted)

The sentence keeps only what changes between rows: count, coverage, and named on-hand items. The shared words move into the column header (*Curated pairings*). This keeps the meaning without a legend, at 2–3 lines per cell.

### 3. Compact structured indicators (R4's dots, considered and not kept)

Dots are the densest form. But a dot string only says "some roles are covered or on hand". It does not say *which* roles, and naming them is what tasks K1, K6 and K7 actually need. A bare count says how many, but not of what.

Mixed forms were also considered and rejected, for example "6/6 covered" or a bar with a label. Once the label is there, the bar adds nothing the number does not already give.

## Measured effect

| Measure | Complete (broccoli) | Incomplete (cabbage) | Sparse (potato) |
| --- | --- | --- | --- |
| Legend-dependent marks, summary overview | 39 → **0** | 57 → **0** | 64 → **0** |
| Kinds of mark needing a legend | 5 (● ◐ ○ ☐ ⇄) → **0** | 5 → 0 | 5 → 0 |
| Summary overview legend | 1 line, 3 dot meanings + 2 control meanings → **none** | | |
| Default columns | 7 → **5** | 7 → 5 | 7 → **4** (route column dropped; banner) |
| Words in the summary overview | 159 → 231 | 167 → 273 | 210 → 310 |
| Overview rows fully in view on the first screen (`overview_rows_visible`) | 5 of 5 → **4 of 5** | 8 of 8 → **6 of 8** | 10 of 10 → **6 of 10** |
| K7, filtered (cabbage, paired with lemon) | 8 of 8 → **5 of 8** | | |

**Finding.**
- **The overview no longer needs a legend,** and it has fewer columns.
- **The price is vertical density.** About 45–63% more words, and on the first screen 1 to 4 fewer rows fully visible.
  - For broccoli (5 rows) this hardly matters.
  - For potato (10 rows) and filtered cabbage (8 rows), the reader now scrolls the overview to see every row, where R4 showed them all at once.
- **This is the main trade-off R4.1 found.** It is presentation, not structure: explicit text needs about one more line per row than a code does.

## Qlik-style filtering and visible exclusions (kept)

- **Unchanged:** filters grey excluded rows with a reason ("excluded: no flavour route"), *hide excluded* removes them, and "3 of 5 match the filters" stays above the table.
- **New:** the context bar adds "2 of 5 rows excluded" next to the filter chips, so the effect of a filter is visible while you are working in the right-hand pane.

K1 (`has=route`) in R4.1 reads, for roasted broccoli:

> Creamy and acidic — all required on hand
> Sour and toasted nut — not on hand: walnut

The two greyed rows say "excluded: no flavour route".

## What the overview still does not show

- **Which roles are covered.** "3 of 4 needed roles covered" names the count. The missing role is named only in *Not recorded* ("no curated pairing for acid"). Naming covered roles too would add a line per row.
- **Confidence of the pairings.** It never was in the overview. It is in the sheet and the trace.
- **Pairings in roles that are not listed as needs.** They were briefly shown as "+1 for a role not listed as a need", and removed to save a line. They stay in the matrix, the sheet (section 4, "not a listed need"), compare and the trace.

## The needs × roles matrix (Phase 7)

The matrix is still an optional column set. R4.1 did not make it the default.

**Are all six R4 marks necessary?** No.

| R4 mark | Needed? | R4.1 |
| --- | --- | --- |
| name = curated pairing | yes, it is the content | name |
| ● = on hand | the fact, yes; the dot, no | green name + the words "on hand" |
| ◇ = experimental pairing | the fact, yes; the diamond, no | italic name + the word "experimental" |
| ✓ = a linked Scout idea was tasted | **no** | dropped. It put a second record's testing inside a pairing cell. The tasting is shown in the sheet (section 7), in compare (*Scout ideas*: "tasted: works"), in the trace, and in the overview's *Hypotheses and tastings* |
| hatched = needed, no curated pairing | yes | hatched + "needed, no curated pairing recorded" |
| — = not a listed need | the distinction, yes; the dash, no | empty cell, with a tooltip. A pairing in an unlisted role carries "not a listed need" under it |

**Missing versus not applicable.**
- **Missing** is hatched and says so in words.
- **Not applicable** is empty.

An empty cell can be read without a legend. The one-sentence legend confirms it. In **compare**, where an empty cell beside a filled one would look like missing data, "not a listed need" is written out.

**A legend visible while scrolling.** The legend is now a row inside the table header, and the header is `position: sticky`. Checked in the browser on potato (10 rows): after scrolling the overview, the legend and the role names stay at the top. The legend is two sentences (36 words) instead of six marks (42 words).

**Alternative pairings in one cell.** R4 separated them with commas, so "garlic confit, ghee, olive oil" wrapped at arbitrary points. R4.1 puts one pairing per line. A test checks that roasted broccoli's fat cell has four lines, one of them marked experimental.

**Measured:**

| | Complete | Incomplete | Sparse |
| --- | --- | --- | --- |
| Legend-dependent marks | 21 → 0 | 23 → 0 | 23 → 0 |
| Words broken mid-word | 52 → 0 | 55 → 0 | 9 → 0 |
| Words in the matrix | 161 → 133 | 209 → 178 | 272 → 236 |
| Overview rows fully in view | 5/5 → 5/5 | 8/8 → 7/8 | 7/10 → 6/10 |

Unlike the summary, the matrix got *shorter* in words, because "—" became an empty cell. It lost at most one visible row, because pairings now stack one per line.

**Still open.**
- Roasted cabbage has 10 role columns plus `mild_base`, a role that appears only on pairings. In the 7:5 split, the last column sits at the edge of the pane, and the overview scrolls sideways.
- The matrix is the only representation that is wider than its pane. Wide matrices may need a frozen first column, or a fold of pairing-only roles.
