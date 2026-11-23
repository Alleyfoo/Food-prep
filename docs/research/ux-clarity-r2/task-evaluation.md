# Task evaluation — T1–T5 on the E1 interface

> **Classification: expert-review hypotheses, not user tests.** A reviewer who
> knows the app followed the path they judged most likely for a first-time
> cook, scripted in Playwright. This shows that a path exists and records
> what the screen says along it. It cannot show whether a newcomer would
> **find** that path. Every "would hesitate" below is a prediction for the
> test pack ([usability-test-pack.md](usability-test-pack.md)) to confirm or
> reject.

## Fresh documented state

- **Server:** a new Streamlit server **per task** (port 8523) and a new
  browser page, so no session state carries over.
- **Viewport:** Chromium 1400×1700, headless.
- **Default state:** Cook › Ingredient Explorer, broccoli / roasted broccoli,
  nothing on hand, and the example plate (mashed potatoes, chickpea patty) in
  Plate Balance.
- **T5 safety:** `FOODPREP_TASTINGS_PATH` was pointed at a temp copy. The
  real `src/foodprep/data/tastings.yaml` SHA-256 was the same before and
  after (`1db89151…dad2`); see
  [`evidence/task-logs/T5-scratch-diff.txt`](evidence/task-logs/T5-scratch-diff.txt).
- **Reproduce:** `py -3.11 docs/research/ux-clarity-r2/evidence/run_tasks.py`
  ([script](evidence/run_tasks.py)). The script saves screenshots to
  `screenshots/tasks/` and the visible text at each step to `evidence/task-logs/`.

## Summary

| Task | Path exists? | Steps (reviewer) | Predicted difficulty for a newcomer | Main risk |
| --- | --- | --- | --- | --- |
| T1 dinner from what I have | yes | 3 picks | **high** | The answer is buried in row 9–11 of card 2. The top card is the *worst* match. |
| T2 heavy plate | yes | 1 tab | low–medium | Example plate not marked as an example. KPIs before the answer. |
| T3 leftover roasted tomatoes | yes | 1 tab + 1 pick | medium | Choosing between Ingredient and Component Explorer, and the "component" term. |
| T4 unusual pairing for roasted cabbage | yes | 1 section + 1 pick | low–medium | Finding "Experiment" and the analogy explanation. |
| T5 record a tasting | yes | expander + 4 fields + 2 buttons | low | Confirmation worded for a developer ("Commit that file"). |

---

## T1 · What's for dinner from what I have?
Shots: `tasks/T1-1-arrival`, `T1-2-after-on-hand`, `T1-3-scrolled`; text: `evidence/task-logs/T1-*.txt`.

**Path:**
1. Arrival on Ingredient Explorer (broccoli already chosen; this is a
   coincidence of the default, since the task also starts from broccoli).
2. Type yogurt, lemon and garlic into "What do I have right now?" (click the
   box before each pick, to avoid the known focus loss).
3. Tab out (Escape would clear the list, a known limitation).

**What the screen then says (observed):**
- The strip shows "AVAILABLE yogurt, lemon, garlic". The feedback is correct.
- Each of the 5 cards gains rows: AVAILABLE NOW ("lemon — have it · acid"),
  MISSING BUT USEFUL, NOT PAIRED HERE YET, and ROUTES WITH WHAT YOU HAVE.
- The **answer** is on the *second* card (Roast), row 9 of 11:
  "Creamy and acidic — yogurt, lemon · also needs dill". Steam has the same
  routes. Stir Fry offers "Soy and garlic — garlic · also needs soy sauce,
  vinegar".
- The **first, accent-bordered card is Raw Assemble**, which uses only lemon
  and lists garlic and yogurt as "not paired here yet". The ranking does not
  react to what you have.
- Roast says "NOT PAIRED HERE YET: garlic" and, two rows above, "MISSING BUT
  USEFUL — FAT: garlic confit". A cook holding garlic is told garlic isn't
  paired, but garlic confit is wanted.

**Predicted confusion:** "Which card is the suggestion?", "Why is the one
with a border the one that uses the least?", "What do I do with yogurt?" (the
answer is in a route row on card 2, not near the top).

**Completion criteria (from the script):** name a preparation plus one owned
item, found by telling the app what you have. **Reachable.** Findability is
predicted poor.

## T2 · My plate feels heavy
Shot: `tasks/T2-1-plate-balance`.

**Path:** Cook › Plate Balance. The task plate is already loaded, because the
example *is* the task plate.

**Observed:** HARD GAPS 3, MAY WANT MORE 0, HEAVINESS 3.5 / 5 rich. "Missing —
hard gaps" lists acid (vinegar, lemon, lime, mustard), herb and crunch.
"Avoid adding more of: more fat / cream". Both halves of the answer are on
one screen.

**Predicted confusion:**
- Because the example matches the task, the task passes without the user
  entering anything. A real user with a different plate must first notice
  that this is an example and clear it. Nothing says so.
- The KPI tiles ("3", "0", "3.5") come before the plain answer. "Hard
  gaps / soft flags / target roles" need explanation.
- The strip says "This view works on plate items or fillers, not on the
  current dish", which is correct but invites "then why does it show roasted
  broccoli?".

**Note for the test pack:** change T2's plate so that the preloaded example
does not answer it. The test pack uses potato gratin with a fried egg
(available plate items; result heavy, avoid more richness).

## T3 · Leftovers from yesterday (roasted tomatoes)
Shots: `tasks/T3-1-component-explorer`, `T3-2-roasted-tomato`, `T3-3-…routes`.

**Path:** Cook › Component Explorer → pick "roasted tomato". The alternative
path (Ingredient Explorer → tomato → Roast card) was not scripted.

**Observed:**
- Next moves: PROTEIN eggs / soft cheese, CARB pasta, SALT sea salt, HERB
  basil / fresh herbs / parsley, ACID lemon.
- USE IN: bowl, pasta, pizza, soup, toast.
- Flavour routes: "No routes modelled from this state yet. Routes are
  hand-curated — absence here means nobody has written one, not that the
  state leads nowhere." This is honest absence, and well worded.

**Predicted confusion:** the tab label "Component Explorer" does not say
"leftovers". Only the eyebrow inside it ("Something you already cooked")
does, and that is visible only once the user is on the tab. The task is
**complete on arrival** once the right tab is found.

## T4 · Something new to try (roasted cabbage)
Shots: `tasks/T4-1-scout-arrival`, `T4-2-roasted-cabbage`.

**Path:** Experiment (Scout) → Transformed state = roasted cabbage.

**Observed:**
- "Roasted Cabbage + Brown Butter"; Compatibility "Plausible", Novelty "Too
  rare to tell".
- Smallest test: "1 small piece of roasted cabbage : 1/4 teaspoon brown
  butter", with success, likely failure, correction and safety.
- Trial history: "No tastings recorded yet."
- The hypothesis says "Reasoned from a known pairing: roasted broccoli with
  olive oil".

**Predicted confusion:**
- "Experiment" must be recognised as the place for "something unusual".
  This is likely: it's the only plausible word.
- The explanation of brown butter on cabbage via *broccoli with olive oil*
  may read as an error, since the analogy chain is not shown.
- "Other candidates" look like plain text.
- Compatibility and Novelty are worded as claims, not scores (good).
  "Strength of this argument: medium high" re-introduces a score-like
  phrase.

## T5 · I tried it — keep a record
Shots: `tasks/T5-1…5`.

**Path:**
1. Experiment (roasted broccoli + brown butter is the first hypothesis by
   default).
2. Open "Record a tasting".
3. Fill in the form: Verdict Works (the default), what you did, ratio,
   temperature, what you tasted, and the safety tick.
4. Review tasting, then Save permanently.

**Observed:**
- The intro says "One observation per attempt. The record is append-only…".
- The review panel reads "CHECK BEFORE SAVING — THIS CANNOT BE CHANGED
  AFTERWARDS" and shows the exact entry.
- After saving: a green message, then the history shows "2 recorded" with
  the new line.
- The confirmation reads: "Saved to C:\Users\…\tastings.yaml. **Commit that
  file to keep the record** — it is the one the app rebuilds from."

**Predicted confusion:**
- "append-only" in the intro.
- "Commit that file" asks a cook to use git. Does the record persist if they
  don't? (It does on this machine; it isn't *shared* until committed.) The
  message mixes a success with an unexplained chore.
- The Verdict defaults to "Works" (`_tasting_reset`), so a hurried user
  records a success they didn't choose. The review step shows the verdict,
  which mitigates this.
- The ratio is prefilled from the smallest test, which is good. The script
  overwrote it, so the screenshot shows the typed value.

---

## Confusing labels met along the paths

| Label | Where | Why it confuses (prediction) |
| --- | --- | --- |
| Raw Assemble | T1 card 1 | It's a technique name, but it reads like an instruction. |
| HIGH / MEDIUM HIGH | T1 cards | High what? (confidence of the transformation data) |
| not paired here yet / missing but useful | T1 | Garlic "not paired" while garlic confit is "useful". |
| ROUTES WITH WHAT YOU HAVE | T1 | This is the answer, labelled as a sub-row. |
| hard gaps / soft flags / target roles | T2 | Three coined terms in one KPI row. |
| Component Explorer | T3 | The tab name doesn't match the task ("leftovers"). |
| Transformed state | T4, T5 | A different name from Cook's "Something you already cooked". |
| analogy rules, corpus | T4 | Researcher vocabulary in the first banner. |
| append-only, commit that file | T5 | Developer vocabulary. |

## Misleading feedback

1. **T1:** the accent border marks rank 1, not the best match for the on-hand
   items, so emphasis points away from the answer.
2. **Taste Circle ▶** (seen while checking first impressions) silently
   changes the subject in every view.
3. **View switch:** the previous view can linger, faded, for several seconds
   (Taste Circle capture). It may be read as the new view.
4. **T5:** "Commit that file" makes the save sound incomplete.
