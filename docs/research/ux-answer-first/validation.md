# Validation

## Automated

| Run | Result | Evidence |
| --- | --- | --- |
| Full suite, Streamlit 1.50, branch head | **372 passed** (336 before E3, plus 36 new) | [`evidence/pytest-full.txt`](evidence/pytest-full.txt) |
| Streamlit 1.67 | **not run** this round | — |

`tests/test_answer_first.py` covers the answer rule and the app:

| Required coverage | Tests |
| --- | --- |
| Answer matches the subject | `test_broccoli_scenario_answers_about_roasted_broccoli`, `test_answer_never_names_another_preparation_as_the_subject`, `test_app_answer_and_lead_card_name_the_same_preparation` |
| Summary and card agree | `test_route_answer_matches_the_cards_route_row`, `test_pairing_answer_matches_available_now`, `test_needs_answer_lists_every_role_the_card_lists`, `test_card_anchor_links_resolve_to_rendered_cards` |
| Available-ingredient filtering | `test_other_preparations_use_what_you_have`, `test_nothing_matching_is_said_honestly`, `test_no_items_on_hand_asks_for_them`, `test_pairing_answer_says_whether_any_route_exists` |
| Missing data | `test_limited_knowledge_makes_no_recommendation`, `test_state_without_routes_lists_single_pairings`, `test_no_state_chosen_does_not_pick_one`, `test_app_ingredient_without_state_asks_for_one`, `test_app_state_beyond_the_top_five_is_still_shown` |
| Shared subject updates | `test_app_answer_follows_a_subject_picked_in_the_explorer`, `test_app_subject_change_elsewhere_updates_the_answer`, `test_subject_change_to_cabbage_leaves_no_broccoli` |
| Taste Circle feedback | `test_taste_circle_arrows_name_their_target`, `test_taste_circle_feedback_is_shown_once` |
| Terminology | `test_one_name_for_a_prepared_ingredient` (all 8 views) |
| Safety and escaping | `test_risks_are_always_shown`, `test_answer_is_escaped` |
| A unchanged | `test_variant_a_is_unchanged` |

`tests/test_shared_context.py` (E3 additions) covers the tasting form, always
on an isolated `FOODPREP_TASTINGS_PATH` copy whose fixture asserts the real
file is untouched:

| Required coverage | Tests |
| --- | --- |
| Explicit verdict | `test_no_verdict_is_preselected_and_none_blocks_review`, `test_chosen_verdict_is_reviewed_and_saved` |
| Save confirmation | `test_save_confirmation_is_plain_language` (no "commit", no path, no ".yaml") |
| Duplicate protection | `test_a_second_save_of_the_same_entry_is_refused_plainly`, plus the existing `test_confirm_writes_exactly_once` (replayed token) |

The existing T5 and E1 tasting tests were updated to choose a verdict
explicitly. Before E3 they relied on the "Works" default.

The real `src/foodprep/data/tastings.yaml` SHA-256 is
`1db89151…dad2` before and after every capture and test run.

## Browser (Chromium)

| Check | Result |
| --- | --- |
| B, T1 at 1400 px: answer, bordered subject card, links | pass (`screenshots/B/T1-*`) |
| Answer link → card scroll (in-page anchor, no rerun) | pass: clicking "stir fried broccoli" scrolled to its card |
| Card ids survive Streamlit's HTML sanitising | pass (5 ids present) |
| Roasted cabbage (no routes) and smashed roasted potato (nothing recorded) | pass: honest answers, no invented "Try" |
| Taste Circle arrows → status line, strip and URL update | pass (`screenshots/repairs/taste-circle-*`) |
| Tasting: no verdict → "Choose a verdict."; save → plain message, history updated | pass (`screenshots/repairs/tasting-*`), isolated copy |
| 375 px: disc hidden, no horizontal scroll | pass |
| Keyboard: Tab from the Prepared ingredient picker reaches "See the full … card ↓" with a 3 px ring | pass |
| A/B captures in a fresh server per scenario | done (`screenshots/{baseline,A,B}`) |
| Console | only connection-refused errors while servers restarted |

**Tested with subjects other than broccoli:** tomato, potato, cabbage.

## Human testing — **not done**

No participants have seen A or B. Nothing in these documents is a user
result, and E3 must not be described as a proven usability improvement.

### Prepared session (3 people new to the app, about 25 minutes each)

This reuses the R2 pack (`research/ux-clarity-r2:docs/research/ux-clarity-r2/usability-test-pack.md`)
for setup, the neutral introduction, hesitation capture and consent.
Only the differences are listed here.

**Setup.** Run two servers side by side, each with its own isolated
tastings copy:

```powershell
$env:FOODPREP_EXPLORER_VARIANT = "A"; py -3.11 -m streamlit run app.py --server.port 8510
```

```powershell
$env:FOODPREP_EXPLORER_VARIANT = "B"; py -3.11 -m streamlit run app.py --server.port 8511
```

**Order.** Counterbalance which variant each participant sees first:

| Participant | First | Second |
| --- | --- | --- |
| P1 | A | B |
| P2 | B | A |
| P3 | A | B |

Use a different subject in each variant, so the second run is not a memory
test:
- **Run 1:** T1 as written (broccoli; yogurt, lemon, garlic).
- **Run 2:** "You have cabbage, lemon and garlic. Find something to make
  with the cabbage." Open the second variant at
  `/?ingredient=cabbage&state=roasted_cabbage_component`.

**Prompts** (read exactly; never point at the panel or the cards):
1. "Use the app to find something to make with the [broccoli / cabbage],
   using what you have." *(type the items in yourself only if they ask how)*
2. "What would you need to buy or add?"
3. "Why does the app suggest that?"
4. Phone width (390 px; desktop browser with device emulation is enough):
   repeat prompt 1 in the variant they saw second.
5. After both: "Which of the two screens would you rather use, and why?"

**Record per run:**
- first action;
- hesitations (R2 definition) and wrong turns;
- whether they **name the suggested preparation** (roasted broccoli /
  roasted cabbage);
- whether their account of what they have and what is missing is
  **correct**;
- whether they open or read the detailed card, and whether it **helped** or
  **distracted** (their words);
- time to first correct answer;
- stated preference and reasons.

**Results template:**

```
Participant  Order  Run  Variant  First action  Hesitations  Named prep?  Have/missing correct?  Read card? helped/distracted  Time  Notes
P1           A→B    1    A
P1           A→B    2    B
…
Preference (P1): A / B / none — reasons (verbatim):
```

**Reporting.** Counts only ("2 of 3"). One participant is a lead, not a
finding.
