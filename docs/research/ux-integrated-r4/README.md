# R4: integrated data-exploration workspace

**Question.** Can people explore, compare and trace Food-prep's data without repeatedly changing screens or mentally reconstructing relationships, once R3's separate layouts work as one workspace with a shared context?

**Scope.**
- Desktop only, as a research prototype outside the product app. Nothing in `src/` changed.
- The R3 prototype is kept unchanged as the baseline: `docs/research/ux-data-layouts-r3/`, port 8540.
- **Out of scope:**
  - mobile and responsive layout;
  - animation;
  - visual polish and branding;
  - taste testing;
  - recommendation logic;
  - new data;
  - another accessibility audit.

**Answer, in short.** See [recommendations.md](recommendations.md).
- **Proceed with the integrated structure, with revisions.**
- One workspace answered all seven R3 tasks:
  - an overview that is always visible;
  - one right-hand pane for detail, compare or trace;
  - one URL-held context.
- No task needed a screen change or a reselection.
- Against the original cards, five tasks went from partial or unsupported to direct.
- Against R3's best separate layouts, K2–K6 improved and nothing got worse.
- The gains came from two changes:
  - the **shared context**;
  - **splitting R3's single status into independent dimensions**.
- They did not come from the graph. It is useful only for small foci.
- **Not tested with people.**

| Document | Contents |
| --- | --- |
| [presentation-model.md](presentation-model.md) | The seven dimensions, stable ids, linking records without merging them |
| [workspace-design.md](workspace-design.md) | Layout; global, shared and local selection; verified interaction paths |
| [traceability.md](traceability.md) | What provenance the database records, and the ingredient → role → pairing → source → scope path |
| [comparison.md](comparison.md) | K1–K7 in R4 against R3's layouts and the original cards; the three datasets; counts |
| [readability.md](readability.md) | Table vs matrix, table vs sheet, graph vs table, status presentation, the E3 panel |
| [recommendations.md](recommendations.md) | Accept, revise or reject; what is permanent, redundant or open |

**Run the prototype**

```powershell
py -3.11 -m streamlit run docs/research/ux-integrated-r4/prototype/app.py --server.port 8541
```

All state is in the URL. For example, the K3 state:

`http://localhost:8541/?ingredient=broccoli&have=yogurt,lemon,garlic&rec=roasted_broccoli_component&trace=ingredient:lemon&pane=trace&depth=2`

**Re-capture** (with the prototype running)

```powershell
py -3.11 docs/research/ux-integrated-r4/evidence/capture_workspace.py
```

The script writes:
- `screenshots/<dataset>/<view>.png` (first screen) and `-full.png` (whole content);
- `screenshots/tasks/K*.png`;
- `screenshots/metrics.json`;
- `evidence/capture-output.txt`.

**Prototype files**

| File | Role |
| --- | --- |
| `prototype/r4_model.py` | Presentation model: records with independent dimensions, id links, gaps |
| `prototype/r4_state.py` | URL state: global, selection and local scopes; filters; pinning; reconciling after an ingredient change |
| `prototype/r4_views.py` | The four representations as pure functions of (model, state) |
| `prototype/app.py` | Streamlit shell: filter bar, context bar, overview and right-hand pane |

**Tests:** `tests/test_r4_workspace.py`, 28 tests. They cover:
- data preservation across the four representations;
- stable ids;
- independent dimensions;
- links made by ids only;
- source traceability;
- required vs optional route elements;
- missing-data semantics;
- compare alignment;
- URL round-trips;
- navigation that keeps the selection;
- graph and table edges agreeing;
- trace steps;
- filters in every pane;
- availability coming only from user input.

The tests show correctness, not that people can understand the layout.
