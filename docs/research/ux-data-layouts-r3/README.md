# R3: data presentation first

**Question.** Are cards and chips the right way to show Food-prep's data, or
do other structures support the data tasks better?

**Scope.**
- Desktop only.
- Out of scope:
  - mobile and responsive layout;
  - typography and spacing polish;
  - animation;
  - another accessibility audit;
  - recommendation logic;
  - new data;
  - refining the existing cards.
- The prototype is outside the product app. Nothing in `src/` changed.

**Answer, in short.**
- Yes, there are better structures, and the best one depends on the task:
  - tables and matrices for scanning, filtering and comparing;
  - a pivot for comparing two or three;
  - a graph with a neighbour list for tracing;
  - a fact sheet for explaining one record and telling facts from ideas.
- An explicit status (curated · on hand · source · idea · tested · not
  recorded) helped in every layout.
- Not tested with people.

| Document | Contents |
| --- | --- |
| [reference-systems.md](reference-systems.md) | How Qlik, Celonis, ARIS, UiPath and ThoughtSpot organize data, with sources and evidence levels |
| [information-structures.md](information-structures.md) | Food-prep's entities, relations, transformations, alternatives, uncertainty and evidence, with counts |
| [layouts.md](layouts.md) | The three layouts and the reference cards |
| [comparison.md](comparison.md) | Complete, incomplete and sparse records in every layout; mechanical counts |
| [readability.md](readability.md) | Seven data tasks × four representations |
| [recommendations.md](recommendations.md) | The proposed combination, issues found, open questions, next step |

**Run the prototype**

```powershell
py -3.11 -m streamlit run docs/research/ux-data-layouts-r3/prototype/app.py --server.port 8540
```

**Re-capture** (with the prototype running)

```powershell
py -3.11 docs/research/ux-data-layouts-r3/evidence/capture_layouts.py
```

**Tests:** `tests/test_r3_layouts.py`.
- Every layout shows every recorded pairing.
- Filters grey rather than remove.
- Brown butter is shown as an idea and tested, never as curated.
- The sparse record states its gaps.
- On hand comes only from user input.
- Focusing a filler finds every preparation it is paired with.
