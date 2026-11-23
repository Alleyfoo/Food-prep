# Fact sheet and comparison: R4 against R4.1

**Method.** An expert walkthrough of both running prototypes at 1440 × 900, on the same URLs. Text counts come from rendering both versions' HTML on the same model (`evidence/text_counts.py`, output in `evidence/text-counts-output.txt`). Screen measurements come from `evidence/capture_compare.py`. There are no participants and no scores.

## Fact sheet

### What a reader gets before scrolling

| | R4 | R4.1 |
| --- | --- | --- |
| Section headings in the first pane screen (`sections_first_screen`) | complete 3, incomplete 3, sparse 4 | complete 3, incomplete 3, sparse 2: the index and band labels take about 90 px. **All eight are one click away** through the pinned index |
| Size of each section, before opening it | not shown | in the index: "3 Roles (6) · 4 Pairings (9) · 5 Routes (2) · 6 Evidence (2 sources) · 7 Ideas and tastings (6 ideas · 1 tasted) · 8 Not recorded (0)" |
| Which kind of information a section holds | numbered headings only | four bands: *Attributes* (1–2), *Relationships* (3–5), *Evidence and testing* (6–7), *Gaps* (8) |
| Reaching section 7 on a complete record | scroll 2,009 px in a 596 px pane, 3.4 pane heights (`section_offsets`, roasted broccoli) | 1 click. Scrolling instead takes 2,231 px, because the sheet is longer. The index stays at the top of the pane while you scroll |
| Whole sheet, in pane heights (`pane_screens`) | complete 4.48, incomplete 3.74, sparse 1.93 | complete 5.56, incomplete 4.89, sparse 2.70 |

The index entries double as a summary. "8 Not recorded (0)" answers *is anything missing?* for roasted broccoli without opening section 8. "(3)" does the same for smashed roasted potato.

### Repetition

Counts are on the rendered text of the whole sheet.

| Measure | Roasted broccoli (R4 → R4.1) | Roasted cabbage | Smashed roasted potato |
| --- | --- | --- | --- |
| "scope: not recorded" | **8 → 1** | **7 → 1** | 0 → 0 |
| Legend-dependent marks (●◐○◇✓≠☐☑⇄) | 5 → 0 | 1 → 0 | 0 → 0 |
| Role name repeated on every pairing row | 9 rows → 6 role rows | 8 → 6 | none |
| Source-title mentions | 12 → 14 | 10 → 12 | 1 → 1 |
| "not on hand" | 17 → 19 | 13 → 13 | 1 → 0 |
| Words in the sheet | 782 → 948 | 622 → 794 | 316 → 429 |

How to read it:
- **The repetition R4.1 targeted went away:**
  - the per-link "scope: not recorded";
  - the role column in the pairings table;
  - the glyphs.
- **The sheet still got longer** (+21 to +36% in words). The added text is:
  - the index and the band labels;
  - the section 8 split, which adds the *Not on hand* list;
  - the tasting table, with its column headings;
  - the role group rows;
  - the "rule:" sublines.
- **Source titles went up by 2** because the citation disclosure in section 6 names each source again next to its own description. The disclosure is collapsed, so on screen the count is the same as R4's.
- **"not on hand" went up for broccoli** (17 → 19), because section 8 now lists missing ingredients explicitly. When nothing is entered, R4.1 removes the availability columns instead: potato goes from 1 to 0.

**Finding.** R4.1 does not make the sheet shorter, and the brief did not ask for that. It moves the repeated *status noise* into single statements and adds *navigation*. Whether 948 words with an index reads faster than 782 words without one is a question for people, not for counts.

### Attributes, relationships and evidence

- **Bands make the three kinds of information visible.** In R4 the reader had to know that sections 3–5 are relationships. Now *Relationships* is a band label over them.
- **Sources are still in two places, deliberately:**
  - in section 4, the title only, so that K4 is answered on the pairing row;
  - in section 6, everything about each source (type, the pairings it backs, claim scope, its self-description).

  R4 had the same split. The difference is that section 4 no longer repeats the claim scope.

### Pairing tables

R4's pairings table had 7 columns: Role, Ingredient, Knowledge, Confidence, Application, Availability, Source · claim scope. The role was repeated on every row, and "scope: not recorded" under every source.

R4.1 has 5 or 6 columns:
- Ingredient, Knowledge, Confidence, Application, (Availability, only when something is on hand), and Source;
- the rows sit under role group rows such as "fat · needed · priority high";
- pairings in a role that is not a listed need sit under "mild base · not a listed need", after the needed roles.

The linked-idea note now says what the link found, "also a Scout idea for the same pair, tasted: works — see 7", instead of "also a Scout idea (same ids) — see 7".

### Missing knowledge against missing ingredients

R4's section 8 listed only knowledge gaps. Missing ingredients were spread through the availability columns.

R4.1's section 8 has two boxes.

| Record | Not recorded in the database (knowledge) | Not on hand (your ingredients) |
| --- | --- | --- |
| roasted broccoli (yogurt, lemon, garlic) | Nothing: every section above has recorded data. | Sour and toasted nut: required walnut not on hand. salt: no curated pairing on hand (recorded: sea salt). fat: no curated pairing on hand (recorded: garlic confit, ghee, olive oil). … |
| roasted cabbage (lemon) | (only the shared "no flavour route") | per role, the curated pairings that are not on hand |
| smashed roasted potato (nothing entered) | no curated pairing for acid, herb, fat; no flavour route (each with a link to its section) | "Nothing is entered as on hand, so availability is not assessed. This is not a gap in the data." |

The overview follows the same split:
- *Curated pairings* says "on hand: lemon (acid)" or "none on hand";
- *Flavour routes* says "not on hand: walnut";
- *Not recorded* holds knowledge gaps only.

A test checks that a missing ingredient never appears in the knowledge-gap box.

### Hypotheses and tasting results

**R4 put three different kinds of claim in one table:**
- experimental pairings, which R4 also showed in section 4;
- Scout ideas;
- tasting trials, with the trial conditions in a muted line under the table.

**R4.1's section 7 has three groups, in order:**
1. **Recorded tasting results.** One row per trial: date, idea tasted (and what it replaced), verdict, conditions. For roasted broccoli: 2026-08-12, brown butter replacing olive oil, *works*, "cooked and eaten as a normal meal… ratio not measured; temperature not measured".
2. **Experimental pairings.** Editor-recorded and ungraded. The ingredient name and role, with "full record in 4".
3. **Scout ideas.** "(6: 1 tasted, 5 not tasted)", tasted first. The rule name moved under the candidate, and the *Inference strength* column heading replaces the per-cell "(inference strength)".

K5 ("is brown butter recorded, experimental or tested?") was direct in R4, but it needed reading one row in section 4 and one row in section 7 and connecting them. In R4.1 the answer sits in three labelled places, each pointing to the others:
- the overview row: "experimental pairing: brown butter (fat)" and "tasted: brown butter, works";
- section 4: "also a Scout idea for the same pair, tasted: works";
- section 7: the tasting table, then the experimental pairing, then the idea.

### Progressive disclosure

**One thing was put behind a disclosure:** the sources' descriptions of themselves (`citation_text`), about 30 words for roasted broccoli. R4 showed them in a muted column. They are not claims about the record. R4 needed a separate note to say so, and the disclosure's label now says it.

**Considered, but not disclosed:**

| Candidate | Why it stays visible |
| --- | --- |
| Trial conditions | They qualify the verdict ("normal meal, ratio not measured"). Hiding them would make "works" read stronger than the record supports |
| The corpus-count note | It explains why recipe frequency is not shown. It is short |
| Route elements | Optionality is the fact that prevents the "also needs dill" misreading |
| The full pairing table | It is the K4 answer |

The rule followed: **disclose only text that is not itself a fact about this record.**

## Comparison

### Making the compared records unmistakable

| Where | R4 | R4.1 |
| --- | --- | --- |
| Overview row | blue left edge + ☑ | blue left edge + **compare A** tag + "remove from compare" |
| Compare header | record name + ✕ | **A** tag + record name + "remove" |
| Context bar | "Compare roasted broccoli ✕ steamed broccoli ✕" | "Compare **A · roasted broccoli** ✕ **B · steamed broccoli** ✕", in blue chips |
| Compare tab | "Compare (2)" | "Compare (2): A roasted broccoli, B steamed broccoli" |
| Detail of a compared record | nothing | "compare A" tag next to the title |

A test checks that the same letter names the same record in the overview, context bar, tab and compare header.

### Cells and differences

| | R4 | R4.1 |
| --- | --- | --- |
| Difference marker | ≠ in its own column | the same column holds the word **differs** (red tag) or **same** (grey) |
| Identical rows | greyed | greyed and labelled "same". *Show only the rows that differ* says "6 identical rows hidden" |
| Role cells | matrix glyphs (`◇ brown butter ✓`, `● lemon`) and the six-mark legend above the table | one pairing per line: "brown butter experimental", "lemon on hand". No legend |
| Missing | hatched "needed · no curated pairing" | hatched "needed, no curated pairing recorded" |
| Not applicable | **—** | **not a listed need** (grey words). In compare an empty cell would read as missing data, so it is written out here, unlike in the matrix |
| Tasting on a linked idea | ✓ inside the fat cell | its own row, *Scout ideas*: "brown butter tasted: works". A new *Experimental pairings* row sits beside it, in the *Hypotheses and testing* group |
| Rows | 19 (roasted vs steamed) | 20: the *Experimental pairings* row is new |
| Pane height (`pane_screens`), K2 | 1.64 | 2.09. Differences only: 1.19 → 1.60 |
| Legend-dependent marks | 24 (broccoli), 19 (cabbage), 19 (potato) | 0, 0, 0 |

**Finding.**
- **Identical values can be de-emphasised without hiding them.** The grey text plus "same" works, and *show only the rows that differ* hides them on request.
- **Missing and not applicable stay distinguishable in words.** No symbol has to be decoded.
- **The cost is a taller comparison:** 2.09 pane heights against 1.64, because of the extra row and one pairing per line. The first screen shows fewer role rows than R4.

### Is the compare set visible throughout the workspace?

Yes, through the tag on each compared row, the chips in the context bar and the Compare tab label. From inside Detail or Trace, the set is still named in the context bar and the tab, so leaving the Compare pane does not hide which records are being compared. R4 showed this only as a blue edge in the overview and "Compare (2)".
