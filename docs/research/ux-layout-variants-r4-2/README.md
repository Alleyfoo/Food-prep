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

**What the counts already say** ([evaluation.md](evaluation.md)):
- **C** is 21–31% shorter than B in words, needs no legend, and names every uncovered role in the cell.
- **A** is the shortest, but needs a 47-word legend and hides 10–14 names per screen in tooltips.
- **The visible-row difference between the variants is only 0–1 rows.** The name cell sets a 63 px floor under every row, so trimming it is worth about as much as switching encodings.
- **Dense** cuts the sheet by 20–25% with no lost facts.
- **Which variant people actually read better is untested.** That is what [session-plan.md](session-plan.md) is for.

**One correction to R4 and R4.1 found on the way.** The tasting record's *observation* ("works… garlic confit on the same state was clearly better, so brown butter is a real option here but not the best one") was never shown, so the sheet said only "works". R4.2 shows it in every condition. A test covers it.

| Document | Contents |
| --- | --- |
| [variants.md](variants.md) | The three overview encodings and the two sheet densities, side by side, and what was held fixed |
| [evaluation.md](evaluation.md) | Mechanical comparison: rows in view, row height, words, legend, tooltip-only names, sheet length |
| [session-plan.md](session-plan.md) | Three-person session: Latin square, scan and understand tasks, sheet tasks, record sheet, decision rules |
| [answer-key.md](answer-key.md) | Ground truth for the scan and understand tasks, generated from the model |

**Run**

```powershell
py -3.11 -m streamlit run docs/research/ux-layout-variants-r4-2/prototype/app.py --server.port 8543
```

For example: `http://localhost:8543/?ingredient=potato&have=dill,olive_oil&ov=c&sheet=dense`

**Evidence**

| File | What it produces |
| --- | --- |
| `evidence/capture_variants.py` | `screenshots/<state>/<condition>.png`, `screenshots/side-by-side/`, `screenshots/metrics.json`, `evidence/capture-output.txt` |
| `evidence/answer_key.py` | `answer-key.md` |

**Tests.** `tests/test_r42_variants.py`, 18 tests. They cover:
- the default condition equals R4.1, apart from the observation line;
- every variant carries the same facts in every row;
- only A uses glyphs and a legend;
- C names each role once;
- the condition survives every link and *reset all*;
- unknown conditions fall back to R4.1;
- the dense sheet keeps every fact and link;
- the tasting observation is shown in both sheets.
