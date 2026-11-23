# Session plan: data-layout validation

**Goal.** For the same data and the same workspace, find which encoding lets people both **scan quickly** (find every matching row) and **understand accurately** (say correctly what a cell means).

**Not compared:** the old cards, R4 against R4.1 as whole systems, or functionality. Everything except the encoding is fixed.

## Set-up

- **Prototype:** `py -3.11 docs/research/ux-layout-variants-r4-2/prototype/run.py`. Desktop, 1440 × 900, one browser window.
- **Conditions** are set by URL only. The tab title shows the condition to the facilitator.
- **The on-hand lists are session input, not culinary data:**
  - broccoli: yogurt, lemon, garlic;
  - cabbage: lemon;
  - potato: dill, olive oil.
- **Three participants.** That is enough to find misreadings, not to rank variants statistically. Treat the results as observations.
- **Timing.** Scan tasks need no clicks, so the page does not reload during them. Note a rough time with a stopwatch, to the nearest 5 s. Understand tasks are not timed.

## Part 1: overview encodings (about 25 min)

Each participant sees **every overview variant once, each on a different ingredient**, so nobody answers the same question twice on the same data:

| | Block 1 | Block 2 | Block 3 |
| --- | --- | --- | --- |
| P1 | A · broccoli | B · cabbage | C · potato |
| P2 | B · potato | C · broccoli | A · cabbage |
| P3 | C · cabbage | A · potato | B · broccoli |

Each ingredient appears once per variant across the three participants, and each variant appears once in each position.

URL for a block, for example C · potato:
`http://localhost:8543/?ingredient=potato&have=dill,olive_oil&ov=c`

**Per block:**

1. **No explanation of the encoding.** In A the legend row is on screen; say nothing about it. Ask the participant to read the table, not to use the filters or the right-hand pane. Filters would answer the scan tasks for them.
2. **Scan tasks.** Ask the participant to name every preparation that:
   - **S1** has a needed role with no curated pairing;
   - **S2** has a curated pairing you have on hand;
   - **S3** has an experimental pairing or a tasted idea;
   - **S4** has a flavour route with every required ingredient on hand.
3. **Understand probes**, on the row given in the answer key (roasted broccoli, roasted cabbage, fried potato). Point at the row and ask:
   - **U1** Which of its needed roles have a curated pairing, and which do not?
   - **U2** What from your on-hand list does it pair with?
   - **U3** What here is a hypothesis rather than a recorded pairing, and has any of it been tasted?
   - **U4** What is missing from the data for this preparation? Is anything missing only because you don't have it?

Answers are in [answer-key.md](answer-key.md), generated from the model by `evidence/answer_key.py`.

**"None" answers are deliberate.** For example, S1 on broccoli and cabbage, and S3 and S4 on potato. A confident "none" is a correct scan, and a false positive is a misreading. Because difficulty varies by ingredient, compare variants across participants, never across ingredients within one person.

## Part 2: fact-sheet density (about 15 min)

Each participant sees **full** and **dense** once each, on two records with the same structure:

| | First | Second |
| --- | --- | --- |
| P1 | full · roasted broccoli | dense · steamed broccoli |
| P2 | dense · roasted broccoli | full · steamed broccoli |
| P3 | full · steamed broccoli | dense · roasted broccoli |

URL, for example dense · roasted broccoli:
`http://localhost:8543/?ingredient=broccoli&have=yogurt,lemon,garlic&rec=roasted_broccoli_component&sheet=dense`

Tasks in the sheet. The index may be used.

| Task | Roasted broccoli | Steamed broccoli |
| --- | --- | --- |
| **D1** Which source backs the acid pairing, and what does it claim? | lemon: roast_culinary. Claim scope not recorded | lemon: recipedb. Claim scope not recorded. Lingonberry vinegar is experimental, with no source |
| **D2** What hypotheses are recorded, and what did tasting show? | experimental: brown butter (fat). Tasted 2026-08-12: *works*, but garlic confit on the same broccoli was clearly better. Normal meal, ratio and temperature not measured | experimental: lingonberry vinegar (acid) and walnut (crunch). No tasting recorded |
| **D3** For *Sour and toasted nut*: is walnut missing from the data, or missing from your kitchen? | from the kitchen (required, not on hand). Not a knowledge gap | the same |
| **D4** In *Creamy and acidic*, which ingredients could you leave out? | dill (finish). Yogurt and lemon are required | the same |

D3 and D4 are the same on both records on purpose. They test the layout of the same facts. D1 and D2 differ, so a participant cannot answer the second from memory of the first.

## Part 3 (optional): the taste circle (about 5 min)

The Taste circle pane is not a layout condition: it is the same in every condition. Use it to check that the workspace still carries the product's main builder. Open:
`http://localhost:8543/?ingredient=broccoli&have=yogurt,lemon,garlic&rec=roasted_broccoli_component&pane=circle`

| Task | Answer |
| --- | --- |
| **T1** Which taste dimensions does roasted broccoli already provide? | Sweet, Umami, Nutty/Toasted |
| **T2** Add something sour that you have on hand. | Lemon or yogurt, from the Sour fan |
| **T3** Change your mind about the sour ingredient. | Click the locked Sour dimension, or *remove* in *Your dish* |

Record: correct · partly · wrong, whether they read the answer from the circle or from the read-out above it, and any click that did something they did not expect.

## What to record

The sheet for each block:

| Field | Values |
| --- | --- |
| participant, block, condition, ingredient or record | |
| per scan task | rows found · rows missed · false positives · rough time · hovers (A only) · scrolled the overview? (y/n) |
| per understand probe | correct · partly · wrong, plus the participant's words when not correct |
| misreadings | any meaning read wrongly, quoted. Watch for: "covered" read as on hand; ◐ or ○ misread; "not on hand" read as a data gap; "experimental" read as tested; a tasted idea read as a recorded pairing |
| per sheet task | correct · partly · wrong · used the index? · rough time |

After both parts, ask:
- Which overview would you want for scanning, and which for checking one preparation? Why?
- Was anything on screen you did not understand?

## How to read the results

- **A variant wins scanning** if it gives the fewest missed rows and false positives, at a comparable time. Count A's hovers as part of its cost.
- **A variant wins understanding** if it gives the fewest wrong or partly-right probes.
- **If one variant wins both,** it becomes the default. If they split, keep the understanding winner as the default (misreading data is the worse failure) and look at whether the scanning winner can be offered as a deliberate *compact* column set.
- **Dense becomes the default sheet** if it costs no accuracy on D1–D4.
- **Do not conclude** from fewer than three participants per variant, and do not report timings as more precise than ±5 s.

## Not in this session

- The old cards.
- Mobile.
- Recommendation tasks ("what should I cook?").
- The E3 answer panel.
- Comparing the circle with the old cards or the product's Cards view.
- Changes to the name cell. It is the next density lever, held fixed here so it does not confound the encodings ([evaluation.md](evaluation.md)).
