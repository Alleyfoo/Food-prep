# R4 steps 2, 3 and 5: candidates, evidence and verdicts

Five candidates from the brief, plus one replacement (napa cabbage for kale)
and one control (the gratin's documented failure). For each: is the
ingredient at Lidl FI (`catalogue.md`), is the transfer already made
somewhere, how does it turn out, and the verdict. The evidence ids resolve in
`sources.md`; the full notes, search logs (per language) and failed pages are
in the four `evidence-*.md` files. The same verdicts and reasons are data in
`src/foodprep/data/transfers.yaml`; `foodprep transfer <id>` prints them with
the model's check.

**How the evidence was read.** Five research agents searched in each
tradition's own language as well as English (Finnish, Swedish, Norwegian,
Danish, German, Dutch, Polish, French, Italian, Spanish, Portuguese, Turkish,
Greek, Arabic, Hindi and Marathi terms, Chinese, Japanese, Korean, Russian),
and cited only pages they opened, in about 15 languages. Most pages were read
through WebFetch, which returns a model-written summary rather than the page
text; PDFs that failed in it were read in full from the saved files, and Lidl
pages were read in full in a browser unless marked *snippet*. Failed pages are
listed and never cited. Quality evidence (ratings, comments, failure reports,
one sensory study) was sought for every candidate, not only existence.

| Candidate | Lidl FI | Already made? | Evidence on the result | Verdict |
| --- | --- | --- | --- | --- |
| Falafel from dried peas | split peas once, in a campaign; whole peas not found | yes: German, British, Spanish home recipes; a Swedish product; Indian vatana vada | holds with no binder; one controlled study: hardest and driest of ten pulses | **worth cooking**, as a comparison |
| Cabbage rolls with kale | curly kale, small bags, Aug-Oct | yes, but only with large flat kale | no source for curly kale; indirect evidence against | **not worth it** (replaced) |
| ↳ napa-cabbage rolls (replacement) | not confirmed (Lidl recipes name it) | yes: Japan, Germany, Russia, Korea, Norway | liked (4.5/5 from 123); tough rib unless shaved | **worth cooking** |
| Potato and rutabaga gratin | rutabaga in season now; potato, cream, milk regular | yes: UK, Ireland, Germany, Switzerland, North America; not Finland | works if the rutabaga is blanched; raw thin slices stay crunchy | **worth cooking** |
| ↳ raw rutabaga (control) | as above | documented as a failure | stays crunchy (two reports) | **rejected** |
| Broccoli-stem patties | frozen florets only; fresh head not found | yes, narrowly: recent zero-waste recipes | no failures, but only publishers' claims | **worth cooking**, as a use for a part already bought |
| Hollowed onion vessel | onions regular (mixed bag); no large onions seen | yes: Nice, Liguria, Piedmont, Turkey, Greece, Levant | liked; handling and effort are the complaints | **worth cooking**, in the same tray as courgettes |

None of the five is new to cooking. Four are new to the Finnish home table
(pea falafel, rutabaga gratin, stem patties and napa rolls in the Finnish
oven); the onion vessel was already in R2's own evidence (M16a, M17b).

---

## T1. Falafel from Finnish dried peas

*Question: can an inexpensive local staple provide the same structure?*
Base: `falafel/raw_soaked` (C3, raw pulse paste; holds by H4, sets on heat).

- **Lidl.** Golden Sun organic split peas appeared once, in a "green
  choices" campaign (L1); whole dried peas and *hernerouhe* are not on any
  Lidl page. Lidl's regular pulses are canned (L12), and canned pulses cannot
  make a raw-paste falafel (R2). Availability is the first thing to check.
- **Made already.** Soaked raw dried peas ground and fried: two German
  publisher recipes (P2: green or yellow peas, no binder; P3: green split peas
  through a meat grinder), a British pulse seller (P4, no binder), English
  blogs (P1, P5, P6), Spanish (P9). A Swedish yellow-pea falafel, 82 % peas
  with bicarbonate and no binder (P16). The closest traditional relative is
  South Indian and Maharashtrian *pattani / vatana masala vada*: whole dried
  peas soaked overnight, ground coarse and raw, deep-fried (P10-P13).
  Caribbean *phulourie* (P14) is a flour batter, a different structure. No
  Finnish recipe or Finnish pea falafel was found (Fallero is faba, P21).
- **How it turns out.** The structure transfers: binder-free pea pastes fry
  whole (P2, P4, P6, P12, P15). The one controlled study (P15, an SLU MSc
  thesis with texture analysis and 54 consumers) made binder-free falafel from
  ten pulses with one bare recipe: yellow pea took up least water, gave the
  **hardest** falafel, and drew the most "too dry" comments; texture 4.6/9,
  overall 5.4 against chickpea 6.0 (not significant) and lentil 6.6. A second
  pea was dropped for dryness. The thesis used no onion or herbs. Cooks'
  notes: grind coarse, or it is dense (P4); fry in small batches at about
  170 C or the balls may break (P4); press, do not roll (P2). Anecdotes are
  mildly positive ("easier than chickpeas", P5; "lighter and crisper" than dal
  vada, P12). No raw-pea or pea-soup taste reported. Food safety: peas are low
  in lectins (P18); falafel fries raw soaked pulses by tradition, so fry small
  pieces through.
- **Verdict: worth cooking**, as one comparison against chickpea falafel.
  The structure is documented and the mechanism identical; the specific risk
  (dry, hard) is documented too, with levers to try. If it holds up with
  onion and herbs, the cheapest Finnish pulse becomes a weeknight dish; if not,
  record it and stop.

## T2. Cabbage rolls with kale leaves, replaced by napa cabbage

*Question: can another leafy vegetable serve as a wrapper?*
Base: `kaalikaaryleet/trimmed_rib` (C7, wrapper and filling, H7).

### Kale (the brief's candidate)

- **Lidl.** Only "Kotimainen lehtikaali": curly kale in 100-200 g bags of
  loose leaves, on offer August to October (L2, L18). No bunches, no cavolo
  nero, nothing in November.
- **Made already, with other kale.** Turkish Black Sea *karalahana sarması*
  (K1-K5, GI-registered versions) uses a non-heading flat kale; a German
  publisher sells it as *Schwarzkohlröllchen*, rated easy (K6). Brazilian
  *charuto de couve* (K7-K10), US collard and lacinato rolls (K11, K16-K19).
  Several sources say kale is *easier* than cabbage: no head to core (K5,
  K15, K18).
- **Curly kale:** no readable page wraps single curly leaves. A test kitchen
  chose lacinato because curly kale is firmer with tougher stems (K16); one
  recipe asks for non-curly kale (K17); others ask for large leaves (K12) or
  stack several small ones per roll (K13).
- **Verdict: not worth it.** Nothing shows curly kale fails, but the
  documented practice selects large flat leaves, Lidl sells only small curly
  ones and only in autumn, and stacking leaves is more work than the cabbage
  it replaces. Replaced, as the brief allows, by a leafy wrapper of the same
  kind that fits a Finnish shop.

### Napa cabbage (replacement)

- **Why.** Its leaves are large, come off the head raw, and it is a
  year-round Finnish supermarket vegetable. **Lidl:** not confirmed; no
  product page, but a Lidl storage guide and Lidl recipes name *kiinankaali*
  (L24, L25). Pointed cabbage was seen once in an old offer (L19).
- **Made already.** Japanese *ロール白菜* (N1-N4), Korean (N5), German
  *Chinakohlrouladen* (N6-N8), Russian golubtsy in Peking cabbage baked with
  mince and rice, "otherwise identical" to the cabbage dish (N10, N11),
  Norwegian (N13). Not Finnish or Swedish.
- **How it turns out.** N1: 4.5/5 from 123 ratings; reviewers found it easier
  to roll than cabbage and one prefers it. The recurring failure is the thick
  white rib staying tough and stringy (N2: several reviewers; N1, N3), fixed by
  shaving it (N3 minces the shavings into the filling). Pan-fried rolls can
  open (N2); overcooked leaves go mushy (N12). Every baked version bakes in
  liquid or sauce, often covered (N6, N9, N10); **nobody bakes them the
  Finnish dry way with syrup**, so that is untested.
- **Verdict: worth cooking**, with the rib shaved and the dish covered with a
  little liquid for part of the bake.

## T3. Potato and rutabaga gratin

*Question: can another root come in without losing cohesion?*
Base: `gratin_dauphinois/raw_long_bake` (C8, layers held by a thickened
dairy, H10).

- **Lidl.** Rutabaga is Finnish and on offer September to December (L5): in
  season now. Potatoes (L6), milk, cream and butter (L7) are regular.
- **Made already.** UK and Ireland: swede dauphinoise, and a 1:1
  swede-potato gratin by Rory O'Connell (G11); Germany and Switzerland:
  *Kartoffel-Steckrüben-Gratin* (G2, G6, G17); North America (G7 America's
  Test Kitchen, G22). Swedish root gratins use only a little swede (G4, G25);
  Norway has a swede-only gratin (G3). **No Finnish potato-lanttu gratin was
  found**: Finland mashes lanttu into *lanttulaatikko*.
- **How it turns out.** The one failure mode is documented twice: thin raw
  rutabaga stayed crunchy after 45 min (G20) and after over an hour in stock
  (G21). The fix is just as clear: blanch the **rutabaga only** 3-5 min (G1,
  G10, G11, G22), or simmer the slices in the cream (G5, G9), or bake raw
  slices covered for about 90 min (G7, G8). Cohesion: no page reports a
  watery result, but recipes keep potato at least half of the roots or add a
  little flour (G7, G22), and rest it before cutting (G7). Flavour: mild and
  potato-like to slightly bitter or pungent, balanced by cream; mustard, apple
  or bacon are common partners (G7, G10, G12, G22).
- **Verdict: worth cooking.** Documented, cheap, Finnish and in season, and
  the one way it fails is known and avoided by a 4-minute blanch. This is also
  the transfer that exposed the model's limitation (`limitations.md`).
- **Control, raw rutabaga: rejected** (G20, G21). Recorded as data so the
  model's check can be tested against a documented failure.

## T4. Broccoli-stem patties

*Question: can an overlooked ingredient part become useful?*
Base: `carrot_patties/crumbs` (C4, grated firm vegetable held by egg and
crumbs, H5b + H6a).

- **Lidl.** The regular broccoli is frozen florets from Spain (L4): no stems.
  A fresh head was not found on any Lidl page. Carrots (L15) and eggs (L10)
  are regular.
- **Made already, narrowly.** Stem-only fritters, coarsely grated raw (B1,
  Australian public broadcaster; B2 copies it); stems boiled and blended with
  egg and flour (B4, Brazil); stem with carrot, egg and flour (B20, a
  Ukrainian video repost); stem-and-potato latkes (B21, B18). All recent
  zero-waste pieces (2016-2026). Not found as a stem patty in Finnish,
  Swedish, Italian, French, German, Spanish or Korean; there the stem goes into
  whole-broccoli galettes and fritters, salads and stir-fries.
- **How it turns out.** No failure report, but also no independent one: the
  evidence is the publishers' claims (crisp outside, the stem not noticeable)
  and two writer tests of whole-head galettes (B6, B7). Most peel the stem
  (B13, B21); only B21 squeezes it. Flavour: mild, slightly sweet, like
  kohlrabi or asparagus (B9, B13-B15); no source calls it carrot-sweet. Thin
  patties cook the grated stem through (B1).
- **Verdict: worth cooking**, as a use for a part already bought: one stem is
  100-150 g, so it goes in with carrot rather than replacing it. Not a reason
  to buy broccoli, and only possible with a fresh head.

## T5. Hollowed onion as the vessel

*Question: can the construction transfer to a different vegetable?*
Base: `zucchine_ripiene/cooked_flesh` (C7, container and filling, with
recombination).

- **Lidl.** Onions are regular as a 1 kg mixed yellow and red bag (L8); no
  large onions were seen, so the vessel is a half of an ordinary onion.
- **Made already, widely.** The City of Nice's own farcis recipe (O5) treats
  the onion exactly like the courgette: halve across, blanch 10 min, keep two
  outer layers as the shell, chop the rest into the farce, bake 180 C 30 min.
  Ligurian *cipolle ripiene* the same (O1-O3; O3 pools onion and courgette
  pulp into one filling), Piedmontese and German whole cups (O4, O8), Asturian
  braised (O6, O7), and the layer-roll form across Turkey, Greece and the
  Levant (O12-O21). R2 had already met it (M16a, M17b).
- **How it turns out.** Liked where rated: 4.96/5 from 25 for hollowed cups
  (O11), about 4/5 from 16 at America's Test Kitchen (O10). Failures are
  handling: overboiled layers tear or slip (O12, O15), cooked onion cups are
  slippery (O10 switched to ring shells); and effort, for a minority
  ("a bit laborious", O7; two 2-star reviews, O12).
- **Verdict: worth cooking**, as halves in the same tray as courgette halves
  with one filling, which is how Nice and Liguria do it: a sweet second
  vessel for almost no extra work.
