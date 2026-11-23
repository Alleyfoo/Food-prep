# Recommendations: accept, revise or reject the integrated workspace

## Verdict: **proceed with the integrated structure, revised**

The brief asked: can people explore, compare and trace Food-prep's data without repeatedly changing screens or mentally reconstructing relationships? For the structure, the answer is **yes**.
- **Every K1–K7 task was answered in one workspace**, with no layout switch and no reselection ([comparison.md](comparison.md)).
- **Against the original cards,** five tasks moved from *not supported* or *partial* to *direct*.
- **Against R3's best separate layouts,** K2–K6 improved and nothing got worse.
- **A typical investigation** (compare, then trace, explain, check status, go back) needed 3 layout switches and 2 reselections in R3. In R4 it needed none.

Two changes did most of the work:
1. **One shared context.** It is held in the URL and visible in the context bar. The overview never leaves the screen.
2. **Independent dimensions instead of one status**, with records linked by database ids ([presentation-model.md](presentation-model.md)). Brown butter is now correctly *one* ingredient carrying *three* records. Lemon's provenance can be followed to a named source, and the missing claim scope is stated.

The graph did **not** do much of the work. Two caveats remain:
- **No person has used this workspace.** Every result here is an expert walkthrough plus correctness tests.
- **R4 has more controls than any R3 layout.** Whether people find them is the open question.

## Permanent, redundant, needs investigation

| Representation or element | Decision | Why |
| --- | --- | --- |
| **Overview, Summary column set** (needs dots, routes, ideas, row gaps) | **Permanent**, default entry | Answers K1 and K6, and is the index for choosing rows. It kept getting worse whenever reasons or per-relation detail were added to it |
| **Shared-gap banner** | **Permanent** | Removed R3's "no flavour route" ×10 noise |
| **Filters that grey rows with a reason, across panes** | **Permanent** | K1 and K7 in one step. Rows are never silently removed |
| **Fact sheet, 8 fixed sections** | **Permanent**, replaces the cards | Direct for K4, K5 and K6. Dimensions as columns; optionality explicit; provenance with scope |
| **Compare with ≠ and differences only** | **Permanent** | K2 direct; complete vs sparse side by side |
| **Relationship table in Trace** | **Permanent** | The reliable form of tracing, carrying every dimension. It drops columns that are n/a everywhere |
| **Context bar and URL state** (✕ per part, reset, Back) | **Permanent** | The visible part of the shared context, and the recovery path |
| **Needs × roles matrix** | **Keep as a switchable column set**, not the default | The only "where does X sit across everything" view without a trace, and the best view of relative sparsity. Too dense to be the entry point (six-mark legend) |
| **Sensory and Evidence column sets** | **Keep**, but review | Useful, little used in K1–K7. Evidence might fit better in the sheet only |
| **Graph in Trace** | **Keep for small foci; collapse it automatically above about 20 edges** | Shows convergence, the chain and the generated layer at a glance for an ingredient, route, source or a step-1 preparation. Illegible at steps 2–3 for a preparation, where it duplicates the table |
| **E3 answer-first panel** | **Redundant in the data workspace**; leave it out | Every fact it states is already in the overview and sheet. It adds a "try this" ordering, which is a recommendation task. Re-evaluate only in a cooking-task study |
| **R3 L2 as a standalone layout** | **Redundant** | Replaced by Trace on demand |
| **Cards** | **Redundant for exploration** | The sheet holds the same facts plus routes with optionality, evidence, ideas and gaps |

## Revisions before testing with people

1. **Auto-collapse the graph** above about 20 edges. Show "graph hidden: 30 relationships, read the table, or show anyway".
2. **Put a section index at the top of the fact sheet** (1–8 as links), so sections 6 and 7 are one click away instead of a scroll.
3. **Make the matrix legend sticky**, and consider dropping ✓ from matrix cells. It is the only mark where two records meet in one cell.
4. **Mark the right-pane tabs in the overview.** For example, a small "in compare" or "traced" marker on rows, so the shared selection is visible from both sides.
5. **Update in place instead of reloading** (a production build). The reload is a Streamlit prototype cost, but it would distort timing in a user session.

## Data issues the workspace exposed (outside R4's scope, logged only)

| Issue | Evidence | Why it matters |
| --- | --- | --- |
| `pairing_evidence.claim_scope` is empty on all 288 links | [traceability.md](traceability.md) | K4 cannot be fully answered: a source is named, but what it claims about the pairing is not recorded |
| 8 Scout ideas propose an ingredient that is already a curated pairing for the same state (eggs on fried, mashed, roasted potato, potato hash, roasted cabbage and mashed rutabaga; dill on boiled potato; capers on potato salad) | `links` in the model; listed in presentation-model.md | Scout presents known pairings as ideas. Exposed only once records were linked by id |
| `pairings.confidence = 'experimental'` stores a knowledge type in a confidence field | 16 rows | Displayed as "not graded" to avoid merging scales. A separate column would remove the ambiguity |
| `corpus_cooccurrence_count` is 0 on all 303 pairings | not backfilled | Not shown as evidence. Explained wherever it would have appeared |
| 54 pairings fill a role the preparation does not list as a need | the model | Easy to lose in any role-based layout. R3's graph lost them; R4 shows them everywhere |
| Cards print *finish* route elements as "also needs" | carried over from R3 | Still in the product cards. R4's sheet shows optionality |

## Open questions for a desktop session with people

1. Do people read the dimension columns (knowledge, confidence and its scale, availability, sources, testing), or do they want one combined status back?
2. Do they understand that "scope: not recorded" weakens a source link, without being told?
3. Do they find Trace from an ingredient name, or only from ⇄?
4. Is the shared context understood? When they open an excluded record, or come back to Compare, is the state where they expect it?
5. Do they ever switch to the matrix on their own, and for which task?
6. Does anyone miss the E3 summary when the task is exploration rather than cooking?

A three-person desktop session on K1–K7 would answer these: cards against the R4 workspace, think-aloud, with the steps above recorded. **It has not been run.**

## Next step

- **Do:** apply revisions 1–4 to the prototype, then run the three-person session.
- **Don't:** merge, port the workspace into the product app, or start mobile, visual-polish or recommendation-logic work before that session.
