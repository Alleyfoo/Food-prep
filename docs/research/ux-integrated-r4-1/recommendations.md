# Recommendations

## The acceptance question

> Can someone inspect, compare and trace Food-prep's existing data without having to decode the interface itself?

**For the status layer, yes.**

| What had to be decoded in R4 | Count in R4 | Count in R4.1 |
| --- | --- | --- |
| Legend-dependent marks | 39–83 per state | 0 in all 22 captured states |
| Words broken mid-word | up to 57 per state | 0 |

These were removed by:
- writing every status in words: on hand, experimental, tasted, needed, not recorded, not a listed need, differs, same;
- naming every selection: in detail, compare A/B/C, traced, in trace, excluded;
- giving each concept one colour.

**For the workspace structure, not shown.** The overview, the three panes, the filters, the trace steps and the column sets are R4's, unchanged. Whether people find and understand them is the open question R4 already named. R4.1 removed the symbol layer on top of that structure. It did not test the structure.

## Verdict: ready for focused data-layout validation, not the final layout

> **Revised after review (2026-11-23).** R4.1 settles the structure and removes the cryptic notation. It is not the final layout. The open question is the balance between scanning quickly and understanding accurately. A comparison with the old cards would mix functionality with layout, so it was dropped. The next round validates layout variants on this same workspace: see [R4.2](../ux-layout-variants-r4-2/README.md).

**No further structural problem was found that should be fixed before testing.** R4.1 found no data relationship that the layout cannot show. Every K1–K7 task is answered in the same steps as R4, with nothing left to decode, and the three datasets behave consistently.

**The problems that remain are trade-offs between density and explicitness.** Only people can settle those. Further expert iteration would mean choosing between two goods without evidence.

| Remaining issue | Why it is not a blocker | What the session should look for |
| --- | --- | --- |
| **Overview density.** 1 to 4 fewer rows fully in view on the first screen (potato 6 of 10 vs 10 of 10) | Rows are still in one scrolling table, with a sticky header. Every row can be scanned | Do people scan the 8–10 row ingredients by scrolling, or do they miss rows below the fold? Do they want the compact code back once they know it? |
| **The fact sheet is longer:** 21–36% more words, up to 5.6 pane heights | The index makes every section one click away and shows each section's size | Do people use the index, or scroll? Do they read the section 8 split (*not recorded* vs *not on hand*) as two different things? |
| **The comparison is taller:** 2.09 vs 1.64 pane heights | *Show only the rows that differ* cuts it to 1.6 | Do people find differences from the "differs" column, or do they read every row? |
| **The matrix is wider than its pane** for cabbage (11 role columns) | It is optional, not the default | Does anyone switch to it, and for which task? This is unchanged from R4's open question 5 |
| **Each click reloads the page** (1–2 s, a Streamlit prototype cost) | Same as R4 | Record it as a prototype cost. Do not time tasks in seconds |

## Keep, revise, drop

| Change | Decision | Basis |
| --- | --- | --- |
| Status in words instead of glyphs (overview, matrix, compare) | **Keep** | 0 legend marks; meaning visible in the cell. Costs vertical space (overview-evaluation.md) |
| Compact labelled summary in the overview | **Keep, and test** against R4's dots | The main trade-off |
| Text row actions (*add to compare*, *compare with X*, *trace*) | **Keep** | They state what pinning does, including the auto-pair with the record in detail |
| One marker vocabulary and one colour per concept | **Keep** | The trace focus is now visible in the overview and no longer blue like compare |
| Fact-sheet index and bands | **Keep** | Section 7 is 1 click instead of 2,000+ px of scrolling |
| Pairings grouped by role; claim scope stated once | **Keep** | Removes 7–8 repeated phrases per sheet |
| Section 7 grouping (tastings, experimental, ideas) | **Keep** | K5 readable in the overview and the sheet |
| Section 8 split (knowledge vs ingredients) | **Keep, and test** whether people read it as two things | Tested in code; not tested with people |
| Graph collapsed above 20 relationships, table first | **Keep** | The large-trace table is on the first screen (195 px vs 709 px). Small traces keep their graph |
| Group rows per From entity in the trace | **Dropped** during the build | One group per edge for preparation traces (trace-evaluation.md) |
| Sentence-length cells (first render) | **Dropped** during the build | About 3 of 5 rows on the first screen |
| Progressive disclosure | **Only for text that is not a fact about the record** (source self-descriptions) | Trial conditions and route optionality stay visible, because hiding them changes the meaning of the facts shown |

## For the validation session

> **Superseded by [R4.2's session plan](../ux-layout-variants-r4-2/session-plan.md).** It compares encodings on this one workspace, with scan and understand tasks, and does not use the cards. The points below carry over.

1. **Do not compare against the cards.** Their functionality differs too much, so a comparison would not isolate the layout. Compare layout variants on the same workspace instead.
2. **Add two probes:**
   - "What does *not on hand* in section 8 mean, compared to *not recorded*?"
   - "Which records are you comparing right now?", asked while the Trace pane is open.
3. **Keep R4's open questions 1–6.** Question 1 (do people read separate dimension columns) is now sharper, because there is no compact code left to fall back on.
4. **Record what is visible without extra navigation, not times.** Each click reloads the page.

## Do not

- Merge into `main`, or port into the product app.
- Start mobile, responsive, animation or branding work.
- Change recommendation logic or culinary data.
- Develop the E3 answer-first panel. It is off by default, unchanged.

## Data issues seen again (logged in R4, not fixed here)

- `pairing_evidence.claim_scope` is empty on all links. R4.1 states it once per table, but K4 still cannot say what a source claims about a pairing.
- Scout ideas that duplicate curated pairings (8 cases). R4.1's "Also recorded as" column and the linked-idea note make them visible, as in R4.
- 54 pairings fill a role that is not a listed need. R4.1 shows them as role group rows ("not a listed need") in the sheet, as cells in the matrix and compare, and in the trace. They are no longer counted in the overview.
