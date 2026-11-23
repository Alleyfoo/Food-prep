# A/B comparison — Ingredient Explorer

**A:** existing hierarchy (`FOODPREP_EXPLORER_VARIANT=A`). **B:** answer
first (the default). Both run on the same build (`440c315`) with the same
data, queries and on-hand selections. A's measurements equal the untouched
baseline exactly (`screenshots/baseline/metrics.json` vs `A/metrics.json`),
so the switch did not alter A.

**Method.** Each scenario was run by [`evidence/capture_ab.py`](evidence/capture_ab.py),
with a fresh server and page per run, at 1400 px (first screen 900 px) and
390 px (first screen 844 px).

**These are mechanical placements, not usability scores.** They show where
the answer is and what must be scanned past to reach it. They do not show
whether a person notices or understands it.

The metric columns below mean:
- **screens:** the target's distance from the top of the page, divided by
  the first-screen height. Below 1.0 is visible without scrolling.
- **chips above:** the number of chips (tags, fillers, roles) drawn before
  the target.
- **bordered card:** the card with the accent border.

## T1 · What can I cook? (broccoli; yogurt, lemon, garlic)

| | A | B |
| --- | --- | --- |
| Target ("Creamy and acidic") | row 9 of card 2 | **answer headline** |
| Desktop: screens / chips above | 1.63 / 40 | **0.52 / 0** |
| Phone: screens / chips above | 3.23 / 38 | 1.13 / 0 |
| Bordered card | raw broccoli | **roasted broccoli** (the subject) |
| What is on hand vs missing | spread over 4 rows × 5 cards | *You have: yogurt, lemon* · *Still needed: nothing else* · *Optional: dill (fresh aromatic finish)* |
| Why | the card route row has no reason | *Why:* the route description + "Cool yogurt contrasts hot browned edges." |
| Next action | none | link to the full card; links to steamed broccoli (creamy and acidic) and stir-fried broccoli (soy and garlic) |

Shots: `A/T1-broccoli-on-hand-{desktop,phone}.png`, `B/…`, plus the `-full` captures.

## T2 · Already prepared (roasted tomatoes)

| | A | B |
| --- | --- | --- |
| Target (a next move, "basil") | in the Try rows of the roasted tomato card | in the answer's *Add* line |
| Desktop / phone screens | 1.21 / 2.85 | **0.57** / 1.19 |
| Chips above | 32 / 34 | **0 / 0** |
| Bordered card | charred tomato | **roasted tomato** |
| Irrelevant transformations before it | charred tomato, and fresh tomato on phone | none: the roasted tomato card comes first, and the other 11 follow under "Other ways to prepare tomato" |

B's answer: "What roasted tomato usually needs. Add: salt: sea salt; acid:
lemon; herb: basil; carb: pasta; protein: eggs. Note: No flavour route is
written for roasted tomato yet; these are single pairings." It lists every
missing role the card lists (test `test_needs_answer_lists_every_role_the_card_lists`).

## T3 · Limited knowledge (smashed roasted potato)

| | A | B |
| --- | --- | --- |
| Investigated card on screen? | **No.** It ranks below the top five; a hint points to *Choose technique* | **Yes**, first, bordered |
| Desktop / phone screens | — | 0.52 / 1.08 |
| What it says | (only the hint) | "Little is recorded for smashed roasted potato yet. Known: It tends to lack acid, herb, fat, but no pairing or flavour route has been written for it. Nothing here is a recommendation." |
| Invented confidence? | no | **no**: no "Try…", no filler named |

## T4 · Change subject (roasted broccoli → roasted cabbage, picked in Component Explorer, back to Ingredient Explorer)

| | A | B |
| --- | --- | --- |
| Roasted cabbage card position (desktop / phone) | card 5 of 8: 2.81 / 5.21 screens, 92 chips above | first: 0.52 / 1.13 screens, 0 chips above |
| Bordered card | braised cabbage | **roasted cabbage** |
| Answer | — | "Add lemon to roasted cabbage. You have lemon (acid). Still missing: salt, fat, herb, protein, carb (with examples). Why: single pairings recorded… No flavour route is written for it yet." |
| Stale "broccoli" in the main area | 0 | **0** |

The answer updated with the subject. No text from the previous
investigation remained.

## T5 · Narrow screen (390 px)

| | A | B |
| --- | --- | --- |
| T1 answer position | 3.23 screens, behind card 1 (raw) | **1.13 screens**, just below the first screen, nothing to scan past |
| What fills the phone's first screen | header, on-hand box, rails, strip, ingredient picker, disc | the same, minus the disc (hidden ≤ 640 px in B) |
| Emphasis | bordered raw card | the answer panel, then the bordered subject card |

**Limitation:** on a 390×844 phone, the shared chrome above the view takes
about 610 px. B's answer therefore starts one short scroll down. E3 did not
change the chrome.

## Phase 6 criteria (qualitative)

| Criterion | A | B | Evidence |
| --- | --- | --- | --- |
| First impression: purpose apparent? | "5 ways to transform it" + 5 cards: a catalogue | "Suggested next step" + headline: a recommendation for *this* preparation | first-screen crops |
| Answer visibility | below the fold, behind the wrong card | in the first desktop screen in all four scenarios | metrics |
| Next action | none on screen | named (headline), with links to the card and alternatives | B shots |
| Explanation | rows of chips; route reason only on Component Explorer | *Why* line from the route's own text | T1 |
| Context: does the answer match the subject? | the border never matched (4 of 4 scenarios) | matched in 4 of 4; enforced by tests | metrics `lead` |
| Cognitive effort (things to scan past) | 32–92 chips | 0 chips | metrics |
| Exploration still possible? | yes | yes: all cards remain; ones beyond four are in an expander, which is *more* reachable than A's hidden ones (T3) | B full captures |
| Mobile clarity | 3–5 screens | about 1.1 screens | phone metrics |

**What this does not show:**
- whether people read the panel or skip it as a banner;
- whether "Try roasted broccoli: creamy and acidic" is understood as an
  action;
- whether the extra panel feels like clutter to someone who wanted to
  browse;
- whether A's catalogue view is preferred for exploring.

Those questions are for the human session ([validation.md](validation.md)).
