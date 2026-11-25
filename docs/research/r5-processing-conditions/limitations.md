# R5 limitations

What could not be found, and what the model deliberately does not do.

## What the evidence did not give

**Inside assemblies.** Six of the 28 member entries after a join have no
endpoint of their own:
- the onion in both falafels;
- the cream in the rutabaga gratin;
- the sweated onion flesh in the onion vessel;
- the filling of the courgette vessel;
- the napa rib minced into the filling.

Others rest on one source, or on a related dish:
- the pork-filling core temperature (Q313, white-cabbage golabki);
- the carrot "tender inside" (Q431).

No source gives:
- a filling doneness test for vegetable farcis (egg set, temperature);
- a check that a grated stem or carrot inside a patty is cooked;
- a rice check after a cabbage-roll bake.

**Peas.** No observable "soaked enough" test, no over-soak failure and no
"cooked through" check for a pea falafel. No Finnish or Swedish pea-falafel
recipe was found. The only quality evidence is still one thesis (P15).

**Finnish sources where the dish is not Finnish.** No Finnish or Swedish
lanttu-potato gratin was found. No Finnish source blanches rutabaga slices for
a gratin. No Finnish napa roll exists. No Finnish courgette-patty recipe was
found on a major site. Finnish cabbage-roll sources state no covering and no
scorch failure.

**Packets.** No Lidl Finland packet text was readable. The lidl.fi rice and
pea pages from R4 are now 404, and search shows only current offers.
S-kaupat and K-Ruoka product pages are truncated before the instructions.
Other brands' packets that were read are marked "not Lidl" (Q337, Q338,
Q543, Q545, Q547, Q549).

**Keeping times.** None found for:
- soaked uncooked pulses;
- blanched but unfrozen vegetables or leaves;
- salted grated courgette;
- a peeled stem;
- moi moi;
- boiled potatoes, from an authority.

Ruokavirasto gives cooling rules (+6 °C within 4 h, reheat above +70 °C) and
temperatures, but no day counts on any page read. Day counts come from Martat
(a home-economics association, `basis: home_economics`), BfR, the UK bodies,
and cooks. Two of the ten food-safety sources are US university extensions
(Colorado State, NDSU), used where no national body covered soaking; they
conflict with each other.

**Food safety of raw-soaked pulse paste.** Ruokavirasto: beans must never be
eaten only soaked (Q505). The pea and chickpea packets say not to eat them
untreated (Q102, Q543). No body read says whether deep-frying a raw soaked
pulse paste counts as that treatment. Falafel's centuries of practice are the
evidence that it does; no authority confirms it. The gap is recorded in the
pea-falafel sequence.

**Over-doing.** Over-blanched rutabaga, over-squeezed courgette and
over-simmered gratin slices: no failure stated by any source.

**Blanching times for freezing** (Martat, Q510) are a different role from
blanching before a bake. They are recorded only as a freezing route for an
intermediate, never as a cooking endpoint. The rutabaga row is ambiguous on the
page (2-3 min, or "cooked through and mashed"); the spot check confirmed the
ambiguity.

## What the model does not do, by design

- **No prediction.** No time or endpoint is computed from properties, slice
  thickness or oven. A shift such as "thicker slices need longer" is recorded
  as a source's statement, not applied.
- **No simulation.** Member states inside an assembly are recorded endpoints,
  not computed. R3's gap (an assembly takes its carrier's state) is now covered
  by documented data, not by a heat model. `constructions.py` is unchanged.
- **No reconciliation.** Conflicts stay as versions; sequences that split the
  work differently stay as alternatives. Nothing reports a "typical" time.
- **No scoring or ranking.** The validator refuses score, rank, rating,
  priority, weight, predicted and estimate fields anywhere in the data.
- **Equivalence is R1's, and only for materials.**
  - `from` matches a part plus operations by `Material.key()`. Two states
    that a cook would call the same but R1 does not (for example julienne
    against grated courgette) do not match.
  - An assembly state (a rested paste, a baked gratin) is reached only by its
    step address.
- **Alternative sequences that are not R3 routes** (raw rutabaga with a
  90-min covered bake, baked falafel, braised cabbage rolls) are recorded as
  text with sources. They are not walked step by step, because they are not
  represented as routes.
- **R3-only pairs** (urad dal, black-eyed beans, moi moi steaming, salted
  courgette, rosti potato) have step data but their routes are not recorded
  as whole sequences. The claim "documented end to end" covers the ten
  sequences only.
- **Endpoint kinds from route order.** 9 of 54 steps have their kind from the
  route's order alone (`by: route_order`, mostly peeling), with no source
  saying "ready for the next step".

## Method limits

- Every page was read through WebFetch (a summarising fetch) or, for five
  PDFs, as raw text with pdftotext. The raw-text spot check covered 12 pages
  and confirmed all 12 paraphrases (`evaluation.md`). It is a sample, not a
  re-read of all 187 pages.
- One agent fetched one URL it had constructed itself (a guessed kwestiasmaku
  path). It returned 404, nothing from it was used, it is listed as failed,
  and the real page was then found by search (Q314).
- Search was mostly through a US-index search tool. Chefkoch.de is blocked
  for the fetch tool. Some Finnish retail pages render instructions with
  JavaScript and were truncated.
- Nothing was cooked.
