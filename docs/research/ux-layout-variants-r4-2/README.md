# R4.2: data-layout validation, one workspace and three encodings

**Question.** With functionality, data and tasks held fixed, which visual encoding gives the best balance between **scanning quickly** and **understanding accurately**?

**Why this round.** Comparing the workspace with the old cards mixed functionality with layout. R4.2 compares layouts only. All conditions run in one prototype, R4.1's workspace, with only the encoding switched by the URL.

**Scope.**
- Desktop research prototype.
- Imports R4's model unchanged.
- R4 (8541) and R4.1 (8542) stay runnable.
- Nothing in `src/` changed.

| Condition | What changes |
| --- | --- |
| `ov=a` | Overview in R4's compact code (dots, bare counts, legend, names in tooltips) |
| `ov=b` | Overview in R4.1's labelled summary (default) |
| `ov=c` | Overview with one named token per needed role and its status |
| `sheet=dense` | Fact sheet with the same facts, tighter (default `full` = R4.1) |
| `pal=pantry\|white\|cool\|peach` | Colour world (default pantry, the user's chosen palette; white and cool are the alternatives; peach is the previous palette, for reference) |
| `pane=circle` | Not a condition: the product's **Taste Circle** builder as a fourth pane, around the record in detail |

**What the counts already say** ([evaluation.md](evaluation.md)):
- **C** is 21–31% shorter than B in words, needs no legend, and names every uncovered role in the cell.
- **A** is the shortest, but needs a 47-word legend and hides 10–14 names per screen in tooltips.
- **The visible-row difference between the variants is only 0–1 rows.** The name cell sets a 63 px floor under every row, so trimming it is worth about as much as switching encodings.
- **Dense** cuts the sheet by 20–25% with no lost facts.
- **Which variant people actually read better is untested.** That is what [session-plan.md](session-plan.md) is for.

**The Taste Circle is back in the workspace.** R4 to R4.2 had left out the product's 11 taste dimensions. The fourth pane, *Taste circle*, embeds the product's own builder unchanged (its component and graph data). It builds around the record in detail, so it shares the workspace's subject.
- Clicks follow the product's rules: open a dimension, lock in a filler, click a locked dimension to change it.
- The dish is held in the address (`tc`, `tcx`, `tcp`, `tcb`), so Back, sharing and captures work as in every other pane. Opening another record starts a fresh circle.
- Above the circle, a read-out states in words what the circle shows in colour and size: dimensions provided by the state, locked, open (with the number of options and which are on hand), and with no options recorded.
- Records without a sensory profile (raw broccoli, broccoli soup base) cannot anchor a circle, and the pane says so.
- The overview encodings are unchanged, so the measurements in evaluation.md still hold.

**Colour by job, not by food** ([palette.md](palette.md)). The first palette was seeded from the product's food colours, and peach ended up doing six jobs at once. The redesign gives each colour one job:
- blue: selection and links;
- violet: compare;
- magenta: trace;
- green: on hand;
- no hue for hypotheses, which are marked by outline and weight instead;
- cool, quiet neutrals for structure.

The default is **pantry**, the user's palette: oat, yogurt, sage, olive, parsley, red cabbage and mustard seed, one food per job (chosen 2026-11-23). The alternatives stay comparable with `pal=white`, `pal=cool` or `pal=peach` (the previous palette). The circle follows the same roles. Every text pair passes WCAG AA in every world.

**One correction to R4 and R4.1 found on the way.** The tasting record's *observation* ("works… garlic confit on the same state was clearly better, so brown butter is a real option here but not the best one") was never shown, so the sheet said only "works". R4.2 shows it in every condition. A test covers it.

| Document | Contents |
| --- | --- |
| [variants.md](variants.md) | The three overview encodings and the two sheet densities, side by side, and what was held fixed |
| [evaluation.md](evaluation.md) | Mechanical comparison: rows in view, row height, words, legend, tooltip-only names, sheet length |
| [session-plan.md](session-plan.md) | Three-person session: Latin square, scan and understand tasks, sheet tasks, record sheet, decision rules |
| [palette.md](palette.md) | Colour worlds: one job per colour, the three worlds, checks |
| [answer-key.md](answer-key.md) | Ground truth for the scan and understand tasks, generated from the model |

**Run** (the launcher passes the palette to Streamlit's theme; plain `streamlit run …/app.py` also works, with Streamlit's default control colours)

```powershell
py -3.11 docs/research/ux-layout-variants-r4-2/prototype/run.py
```

For example: `http://localhost:8543/?ingredient=potato&have=dill,olive_oil&ov=c&sheet=dense`

**Evidence**

| File | What it produces |
| --- | --- |
| `evidence/capture_variants.py` | `screenshots/<state>/<condition>.png`, `screenshots/side-by-side/`, `screenshots/metrics.json`, `evidence/capture-output.txt` |
| `evidence/answer_key.py` | `answer-key.md` |
| `evidence/capture_worlds.py` | `screenshots/worlds/`: detail, compare, trace and circle in each colour world, side by side |
| `evidence/capture_circle.py` | `screenshots/circle/`: the circle pane empty, with Sour open, with a dish, cabbage, and a record with no profile |

**Tests.** `tests/test_r42_variants.py` (18), `tests/test_r42_circle.py` (10) and `tests/test_r42_palette.py` (33). They cover:
- the default condition equals R4.1, apart from the observation line;
- every variant carries the same facts in every row;
- only A uses glyphs and a legend;
- C names each role once;
- the condition survives every link and *reset all*;
- unknown conditions fall back to R4.1;
- the dense sheet keeps every fact and link;
- the tasting observation is shown in both sheets;
- the circle pane: the product's click rules, the URL-held dish and its round trip, a fresh circle for a new subject, every dimension named in the read-out, links keeping the condition, and records with no profile;
- the colour worlds: every text pair at least 4.5:1 and marks at least 3:1 in every world; no food tint in the new worlds' structure; one hue per job; circle colours from the world's tokens only; no hex or translucent colours in the CSS; `pal` survives links.
