# R4.1: data readability and workspace refinement

**Question.** Can someone inspect, compare and trace Food-prep's existing data without having to decode the interface itself?

**Scope.**
- Presentation only, on R4's architecture, on desktop, as a research prototype.
- R4 stays runnable as the baseline (port 8541).
- R4's model (`../ux-integrated-r4/prototype/r4_model.py`) is imported unchanged.
- Nothing in `src/` changed.

**Answer, in short.** See [recommendations.md](recommendations.md).
- **The status layer no longer needs decoding:**
  - legend-dependent marks: R4 39–83 per state, R4.1 0 in all 22 captured states;
  - words broken mid-word: up to 57 per state, now 0;
  - every status in words, every selection named, one colour per concept.
- **The cost is length.** Fewer overview rows in the first screen (potato 6 of 10 vs 10 of 10), a sheet 21–36% longer in words, and a taller comparison.
- **The gain is in large traces.** The relationship table now starts at 195 px instead of 709 px.
- **Verdict (revised): ready for focused data-layout validation, not the final layout.** The structure is settled; the balance between scanning quickly and understanding accurately is not. Validated next on this same workspace, without the cards: see [R4.2](../ux-layout-variants-r4-2/README.md).
- **Not tested with people.**

| Document | Contents |
| --- | --- |
| [baseline.md](baseline.md) | R4 as delivered: what is hard to read, with counts |
| [layout-changes.md](layout-changes.md) | Every R4 → R4.1 change, by phase, and what was not changed |
| [overview-evaluation.md](overview-evaluation.md) | Explicit text against symbols and counts; the matrix |
| [detail-and-compare.md](detail-and-compare.md) | Fact sheet (index, repetition, the two kinds of absence, tastings, disclosure) and comparison |
| [trace-evaluation.md](trace-evaluation.md) | Graph collapse, where the table starts, reading the table |
| [comparison.md](comparison.md) | K1–K7 on both versions; the eight criteria; per-state numbers; how to reproduce |
| [recommendations.md](recommendations.md) | Verdict, keep / revise / drop, the usability session |

**Run both**

```powershell
py -3.11 -m streamlit run docs/research/ux-integrated-r4/prototype/app.py --server.port 8541
```

```powershell
py -3.11 -m streamlit run docs/research/ux-integrated-r4-1/prototype/app.py --server.port 8542
```

Both read the same URL keys. R4.1 adds one local key, `graph=1`. For example:

`http://localhost:8542/?ingredient=broccoli&have=yogurt,lemon,garlic&rec=roasted_broccoli_component&cmp=roasted_broccoli_component,steamed_broccoli_component&trace=ingredient:lemon`

**Evidence**

| File | What it produces |
| --- | --- |
| `evidence/capture_compare.py` | `screenshots/r4/`, `screenshots/r41/`, `screenshots/side-by-side/` (R4 left, R4.1 right), `screenshots/metrics.json`, `evidence/capture-output.txt` |
| `evidence/text_counts.py` | `evidence/text-counts-output.txt`: glyphs, words, repetition, trace sizes, from both versions' HTML on the same model |

**Tests.** `tests/test_r41_workspace.py`, 36 tests. They cover:
- R4's guarantees carried into the new renderers: every pairing in all four representations, graph and table edges agreeing, confidence scales named, filters in every pane, URL round-trip;
- no coded glyphs in any view or dataset;
- the overview in words, and its column count;
- the section index;
- claim scope stated once;
- missing knowledge apart from missing ingredients;
- grouped tastings;
- compare: not-a-need vs not-recorded, differs and same, and letters that match everywhere;
- graph collapse, reveal, and the reveal being local;
- trace names kept whole;
- the trace colour;
- selection markers;
- local controls never changing the subject;
- the matrix lines and its sticky legend.

The full suite passes: 446 tests on Streamlit 1.50.
