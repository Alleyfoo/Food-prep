# Recommendations — E3 Answer First

## Verdict: **revise, then test with people.** Do not merge yet.

The prototype does what it was built to do, and it does it mechanically and
verifiably:
- The answer moved from 1.6 screens down, behind 40 chips, to the first
  desktop screen with nothing before it.
- The emphasis now matches the subject in 4 of 4 scenarios (before: 0 of 4).
- Incomplete knowledge is stated rather than papered over.
- No information was removed. One card that A hid is now reachable (T3).

Whether people *read and understand* the panel is unknown. No participant
has seen it. That is the reason for "revise and test" rather than "accept".

## The completion questions

1. **Does answer-first make the useful recommendation easier to locate?**
   - Mechanically, yes. T1 desktop went from 1.63 screens / 40 chips to
     0.52 / 0, and T1 phone from 3.23 / 38 to 1.13 / 0.
   - T2–T4 show the same pattern ([comparison.md](comparison.md)).
   - Whether it is easier *for a person* is untested.
2. **Does the answer clearly match the selected prepared state?**
   - Yes, by construction and by test. The answer, the bordered card, the
     picker and the strip all read the one shared context.
   - The answer's route, items and roles are the card's own data
     (`test_route_answer_matches_the_cards_route_row`,
     `…lists_every_role_the_card_lists`).
3. **Can users still understand why a recommendation was made?**
   - The *Why* line uses the route's own description and fit reason, and
     risks are always shown.
   - Single-pairing answers say they are single pairings.
   - Understanding is for the human session.
4. **Can the hierarchy handle incomplete knowledge honestly?**
   - Yes. T3 (nothing recorded) says "Nothing here is a recommendation".
   - Roasted cabbage says no route is written.
   - No preparation chosen means none is picked.
   - Nothing matching says "not that it clashes".
5. **Does it work without removing exploratory functionality?**
   - Yes. All preparation cards remain, in their existing rank.
   - The expander makes cards beyond four *more* reachable than A did.
   - *Choose technique* is replaced by the Prepared ingredient picker,
     which sets the shared subject.
6. **Is the benefit large enough to extend the pattern to other screens?**
   - **Not yet.** Measured placement gains are large, but the unknowns are
     about reading and trust.
   - Extending before the human session would multiply an untested pattern.
   - If the session confirms it, Component Explorer is the natural next
     candidate, and Plate Balance the second (its KPIs came before the
     answer in R2). Taste Circle and Scout already lead with the answer.

## Revisions before or alongside the human test

1. **Headline wording.** "Try roasted broccoli: creamy and acidic" is
   derived from the route name and reads slightly mechanical. Test it as is
   first. If participants stumble, consider "Try roasted broccoli with a
   creamy, acidic dressing". That wording needs a per-route noun, which the
   data does not hold, so it would be new curated text and must not be
   invented.
2. **Phone first screen.** The answer starts about 0.1 screen below the
   fold, because the shared chrome (header, on-hand box, two rails, strip)
   takes about 610 px. That chrome is not E3's to change. If the human test
   shows people don't scroll, it is the next thing to look at, app-wide.
3. **"Other ways to use what you have"** uses in-page links. People may
   expect them to *switch* the subject rather than scroll. Watch for it in
   the session.
4. **Streamlit 1.67:** run the new tests there before any merge.

## Keep regardless of the A/B outcome

These are independent of the hierarchy question and low-risk:
- **Taste Circle arrows** (`dc286fa`): named targets and the status line.
  They make an already-existing global effect visible.
- **Tasting form** (`98fea65`): no default verdict and a plain confirmation.
  Correctness and clarity, with all safety guards intact.
- **One name for a prepared ingredient** (`2e17a1a`), unless the human test
  shows the term itself confuses.

## Known limitations

- No human testing. All findings are mechanical placement or expert review.
- The phone's first screen is dominated by shared chrome (see above).
- B's answer shows only the *first* qualifying route. Others appear on the
  card and in "Other ways…".
- In-page anchors add `#card-…` to the URL. That is harmless, but a reload
  scrolls to that card.
- Pre-existing and unchanged:
  - the selectbox Tab-out display bug;
  - Escape clears the on-hand list;
  - graphs aren't keyboard-operable;
  - no back/forward history.
- Not run on Streamlit 1.67.

## Reverting

Each change is one commit (see [implementation.md](implementation.md)).
- To compare without reverting: `FOODPREP_EXPLORER_VARIANT=A`.
- To drop the prototype but keep the repairs: revert `2351ed5`, `22c69b3`,
  `feb187c` and `440c315`.
