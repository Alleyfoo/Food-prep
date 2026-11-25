# R7 known limitations

## Untested with the user

Every view was checked in the browser against the real data, but no one has
cooked from it. The IE checks (`ie-checks.md`) are the evaluation. Nothing in
R7 shows that it helps yet.

## Data the views can only report as missing

- **Most R3 dishes have no R5 sequence.** 10 of 64 routes have one. The
  others open with "endpoint not recorded" on every step, and "not found" for
  members after a join. Their outcome entries say the one condition is not
  recorded.
- **Pea soup is not in R3**, so it is not a familiar use of dried peas. It
  is visible only in the soaking record's conflict (see README, item 1).
- **Availability is empty** until the user records shelf checks. lidl.fi is
  deliberately not used.
- **"The one condition"** is derived from R5 `misses`: the skipped stage
  first, otherwise the first recorded one. It is close to R4's hand-written
  conditions but not identical. Pea falafel shows "do not over-grind: dense
  falafel (P4)", while R4's README says "grind coarse, keep the onion and
  herbs" and names dryness (P15). The dryness is shown under quality risk.

## Alignment

Rows are aligned by identity (the same member through the same operation).
This is not the R6 step-correspondence model. Consequences:
- a step that does another's job in a different way (the long covered bake
  in place of the blanch) is not shown as corresponding; it shows as "none"
  in one row and a longer time in the bake row;
- routes whose members have different names (the base gratin's materials
  against a transfer's) do not share rows;
- the gratin's columns are the transfer and its R5 alternatives. The base
  `gratin_dauphinois` routes are reached from "Open the base dish".

## Interface

- **Shared context.** The Dinner picker covers 18 ingredients, some of which
  the older catalogue that drives Cook and Explore does not hold (dried peas,
  napa cabbage, rice, chickpea...). Picking one of those keeps it in Dinner
  and leaves the shared context alone, because the Cook views cannot draw an
  ingredient they do not know. A link with `?ingredient=dried_peas` falls
  back to the default.
- **No deep link** to a dish or a held state. The dish picker remembers the
  last choice within a session.
- The app opens on Cook, not Dinner (see README, "Left out").
- **Long steps.** The bake step of a gratin merges the fields of several R5
  processing records, so its failed-if list is long. That is the data
  (`conditions.step_fields`), shown as is.
- **First load after a server restart.** Once, with two browser sessions
  reconnecting at the same moment, the first run raised an import error.
  Reloading the page cleared it. This looks like a Streamlit cold-start
  race, not R7 code, but it was seen once while verifying.
- **The record form was not submitted in the browser**, so that no invented
  record entered the user's files. Writing, validation, duplicate refusal and
  display beside the documented values are covered by
  `tests/test_kitchen_records.py`.

## Safety

The views add no safety knowledge:
- keeping times are shown with their authority;
- FS1-FS8 stay open;
- the pea-falafel safety gap is shown in words, not resolved.
