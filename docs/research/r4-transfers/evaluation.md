# R4 evaluation: what the round shows, what it cost, what it changed

## Did the round answer its question?

*Can the system help us find something useful to cook?* **Partly, and not in
the way the roadmap assumed.**

- **Useful things to cook were found: five.** A potato and rutabaga gratin,
  onion halves as vessels beside courgettes, napa-cabbage rolls, a pea
  falafel to compare with chickpea, and broccoli stems with carrot in patties.
  Each is made and liked somewhere, has one known way to go wrong, and fits a
  Finnish home kitchen. One candidate was turned down (curly kale as a
  wrapper) and replaced by a better one of the same kind.
- **The search found them, not the model.** Every fact that makes these
  dishes work (blanch only the rutabaga, shave the napa rib, grind peas
  coarse, halve the onion and cook it in the same tray) came from documented
  practice, read in about 15 languages. None of the five is new to cooking;
  four are new to the Finnish table.
- **The model helped in three narrower ways.**
  1. It turned each transfer into an explicit list of what the substitute
     must do (bend and be large enough to wrap; supply starch to the dairy;
     stand as a large blanched half; set on heat when raw), which made the
     search targeted: the questions sent to the research agents came from the
     base routes' requirements.
  2. It caught nothing the evidence missed, but where it disagreed with the
     evidence (raw rutabaga), the disagreement pointed at a real, small gap
     that could be fixed with data alone.
  3. It now records a transfer so that the kitchen test can falsify a stated
     property (A2's layer requirement, the peas' `sets_on_heat`, the kale
     leaf size).
- **What the model cannot do is the deciding part.** In every transfer worth
  cooking, the open question is quality (dry, sharp, stringy, noticeable),
  and the model has no quality. That is consistent with the project's rule of
  no scoring; it means the model's job at the stove is a checklist and a
  record, and the kitchen test is the judge.

## Against the brief's criteria

| Criterion | Result |
| --- | --- |
| Lidl FI catalogue as the boundary, with sources and dates | done, but lidl.fi publishes offers only; 26 Lidl page ids with dates; regular, seasonal, campaign and not-found recorded per item (`catalogue.md`) |
| Five candidates evaluated; unpromising ones replaced and why | five evaluated; kale replaced by napa cabbage (Lidl sells only small curly kale, every documented roll uses large flat kale) |
| Multilingual search for existing practice and its quality | 158 cited pages and Lidl ids (`sources.md`), failed pages listed, summarising tool disclosed; quality sought in ratings, comments, failure reports and one sensory study |
| Model explanation per transfer, as data through the validator | seven transfer routes in `transfers.yaml`, validated with R3's code unchanged; agreement with the evidence per transfer (`model.md`) |
| Verdict and kitchen test per candidate | four worth cooking plus the replacement, one not worth it, one control rejected; five kitchen tests with taste and a stop condition |
| Extend the model only where a worth-cooking transfer needs it | one data-only extension (A2) for the gratin; seven other limitations recorded, not fixed (`limitations.md`) |
| No new ranking or scoring; no massive ingredient expansion | none; two ingredients and four staged parts added |
| R3 freeze strict; behaviour otherwise unchanged | A2 is a documented amendment with zero effect on R3 (57 routes compared); R3 tables untouched; family generator fingerprint unchanged |

## Behaviour changes, all deliberate

- `foodprep explore kale` (and rutabaga, dried_peas, napa_cabbage) now lists
  operations, because these ingredients have staged parts. The CLI test that
  used kale as its example of an ingredient without parts now uses mango.
- New CLI command `foodprep transfer [id]`.
- Two catalogue ingredients (`dried_peas`, `napa_cabbage`) and Lidl notes on
  rutabaga, kale and broccoli availability. No availability class changed.
- Amendment A2: a property and one role requirement in `operations.yaml`;
  zero effect on every documented dish.
- Nothing else: `constructions.py` and `operations.py` are byte-for-byte as
  R3 left them (their freeze hashes are unchanged); the family generator does
  not read staged parts or assembly operations.

## Cost

Five research agents (about 1.0 million tokens in total, 526 tool calls),
then data, a 280-line module, a run script and 21 tests. The Lidl check alone
took 166 tool calls, mostly to establish that the website cannot answer the
question. A shelf visit would have taken ten minutes.

## Limits

- **Nothing was cooked.** Every verdict is a reading of documented practice.
- Most pages were read through WebFetch, which summarises; no raw-text spot
  check was done this round (R2 did one: 9 of 12 exact, none badly wrong).
- Quality evidence is thin where it matters most: small rating samples, one
  thesis for the falafel, publishers' own claims for the stems, no Finnish-style
  bake for napa rolls.
- Lidl availability of dried peas, fresh broccoli and napa cabbage is
  unconfirmed (not absent).
- Two model agreements (peas, curly kale) rest on a property this round set
  from the same evidence; the documents say so where it matters.

## What R5 should take from this

- The practical value is in **pairing a documented construction with what is
  in season and in the shop**, and in carrying each dish's one known failure
  with it (blanch the rutabaga, shave the rib). That is what an interface
  could show: "rutabaga is in season; it goes into gratin if you blanch it
  first; here is why".
- The Lidl catalogue should come from the user's own shelf checks or receipts,
  not the website.
- The kitchen tests are the cheapest next evidence; their results belong in
  `transfers.yaml` (`evidence_says`, `verdict`) and in the tasting record.
