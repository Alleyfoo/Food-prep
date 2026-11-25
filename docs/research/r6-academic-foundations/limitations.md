# R6 limitations

## Method

- **Seven evidence agents**, one per area, followed one brief
  (`research-brief.md`) written before any source was read. All seven were
  stopped once by a usage limit and resumed with their own context. The
  reading they had done was kept, not repeated. Each wrote one evidence
  file. The synthesis documents are written from those files, plus R6's own
  reading of the Food-prep code and data.
- **How pages were read.** Of 113 entries (110 distinct works):
  - 51 were read as full text;
  - 17 as full text through a summarising fetch tool, so details are less
    certain;
  - 28 in part;
  - 17 as an abstract or landing page only (`sources.md`).

  No conclusion rests on an abstract alone.
- **Spot check against raw text.** Five load-bearing claims were checked
  by extracting the PDF's text with `pdftotext` and searching it. All five
  were confirmed, with one correction:

| Claim | Source | Raw-text result |
| --- | --- | --- |
| 76% of retrieved recipes correct; errors 39% wrong substitution, 27% state, 14% motion, 20% integration; kale and cabbage among similar objects | Y206 | confirmed (abstract; §V; Fig. 7 lists kale and cabbage) |
| 61 sandwich recipes; generalisation and specialisation "enable to generate more than 9 × 10^21 recipes" | Y300 §5 | confirmed |
| primary and secondary substitutions; integrity constraints; a mitigation need not exist | Y402 | confirmed (§1; Proposition 11). No evaluation on real recipes was found in the text |
| overview presentation preferred; no difference to time | Y703 ch. 7 | confirmed. **Correction:** the 24 participants were university students, 8 per condition. The abstract says the overview *reduced* problems arising from recipe content, so "did not change overall error counts" (in `evidence-visualisation.md`) overstates it. The synthesis documents use the thesis's wording |
| human upper bound 79.0; model 72.4 | Y503 | confirmed (Table) |

  The evidence files are kept as the agents wrote them. The correction is
  recorded here and applied in the synthesis.
- **Blocked sites.** Semantic Scholar refused automated access (429), so
  forward citations were followed through the papers' own citing lists and
  readable Google Scholar listings only. Also blocked:
  - ResearchGate, HAL (every French deposit) and core.ac.uk;
  - MDPI, some DFKI pages, and FAO (the Codex text was read from a
    university mirror, Y611);
  - ScienceDirect full texts.
- **Languages.**
  - Read: French (Taaable, Y311; the digital-kitchen ontology, Y111;
    INRAE slides, Y115), Japanese (Y709, Y710; Y219 did not decode),
    Finnish (Ruokavirasto, Y613).
  - German Trier reports: none found online.
  - The Japanese recipe-flow and cooking-support line was read mainly
    through English papers (AR17).
  - No Italian or Spanish academic work on culinary process modelling
    was found.
- **Unread works that might matter**, each in `open-questions.md`:
  - Yamakata et al. 2016, merging the flow graphs of one dish (AR12);
  - Müller's 2018 dissertation and the 2015 adaptation-operators paper
    (AR11);
  - Onto-FP, Buche et al. 2020, Batista et al. 2006 "food state" (AR22);
  - ISA-88 Part 3 clauses 5-8 (AR13);
  - Lütke Entrup 2005 on yoghurt shelf life (AR14);
  - every food-science source on binders and egg replacers (AR9).
- **Mappings are inferences.** Every mapping of K1-K9 into an external
  framework was made on paper in R6. No framework was run, and none was
  implemented.

## What the evidence could not settle

- **Members after assembly.** No approach models them. R6 can say that the
  literature does not solve R3's gap, and that R5's documented endpoints
  go further than anything found. It cannot say how to fill the six
  missing endpoints: only kitchen tests can (KT6).
- **Readiness against doneness** has no counterpart in any area. That may
  be a real gap in the literature, or a search that missed it. Robotics,
  ontologies, workflows, industry and NLP all came up empty.
- **Whether the adopted concepts help a cook.**
  - ISA-88's levels, Y402's repairs and alignment are evaluated in their
    own fields, never with a home cook.
  - The one cook-tested representation (Y703) was tested with students
    cooking set recipes, not deciding what to cook.
- **Substitution ground truth** is weak across the field. R4's kitchen
  tests would be stronger than any published protocol found, once they are
  done.
- **Food safety.** Nothing read settles FS1, the raw-soaked pulse paste.
  R6 added only the general point that history matters to food-service
  safety (Y612), and that critical limits must be validated (Y611).
- **No culinary success is claimed.** Nothing was cooked in R6. Neither the
  user's purchase of rutabaga and dried peas nor anything read here changes
  the status of KT1-KT12 or SA1-SA5.

## Boundaries kept

- No change to `src/`, `tests/`, any schema, any culinary data, or any
  R1-R5 document or frozen file. Verified with
  `git diff origin/main -- src tests docs/research/r1-* ... r5-*`, which is
  empty. The edits outside this folder are `docs/research/roadmap.md`
  (R6 and R7 entries added, earlier entries kept) and `.handoff.md`.
- No prototype, generator, scoring, ML experiment or simulator.
- No preference for a framework because it resembles Food-prep. Where
  Food-prep is called stronger, the reason is given (`representation-comparison.md`).
