# The variants

All variants run on one prototype. The model, the panes, the interactions, the trace, compare and filters are fixed. Only the **encoding** of the same facts changes.

The facilitator sets the condition in the URL. Every link keeps it, and so does *reset all*. It is shown only in the browser tab title ("R4.2 · C · full"), not on the page.

A test checks that every variant carries the same facts in every overview row:
- the uncovered roles;
- the curated pairings on hand;
- the experimental pairings;
- the tasted ideas;
- the route names.

A second test checks that the default condition (`ov=b`, `sheet=full`) renders exactly the same text as R4.1.

## Overview encodings (`ov`)

These apply to the default *Summary* column set. The name column (name, step subline, *in detail* / *compare* / *trace* markers, row actions) is identical in all three, at the same minimum width.

| | A: compact code | B: labelled summary | C: named roles |
| --- | --- | --- | --- |
| **Origin** | R4's encoding | R4.1 (default) | new hybrid |
| **Needed roles** | `●◐○○ 3/4`, one dot per needed role. ● curated pairing on hand, ◐ recorded, ○ none. Names are in a tooltip | "7 pairings · 3 of 4 needed roles covered", then "on hand: lemon (acid)" or "none on hand" | one token per needed role: `salt` (curated pairing recorded), green `acid: lemon` (on hand), hatched `herb: not recorded` |
| **Flavour routes** | route name + `1/2` (required elements on hand). Missing names in a tooltip | route name, then "all required on hand" or "not on hand: walnut" | route name + "all on hand" or "walnut not on hand", inline |
| **Hypotheses** | `◇1 · 6 · ✓1` (experimental · Scout ideas · tasted). Names in a tooltip | "experimental pairing: brown butter (fat)", "6 Scout ideas", "tasted: brown butter, works" | tokens: `experimental: brown butter`, `6 ideas`, `tasted: brown butter, works` |
| **Not recorded** | knowledge gaps, hatched | the same | the same, without "no curated pairing for …", because the role tokens already show it |
| **Legend** | one sticky row, 47 words | none | none |
| **Column headers** | Needs · Flavour routes · Hypotheses · Not recorded | Curated pairings · Flavour routes · Hypotheses and tastings · Not recorded | Needed roles · Flavour routes · Hypotheses and tastings · Not recorded |

**What each variant bets on:**
- **A:** a learned code scans fastest once known. Names are one hover away.
- **B:** the meaning is in the sentence, so nothing has to be learned.
- **C:** naming each role with its status gives B's meaning at nearly A's density. It answers "which role?" without a hover, which neither A nor B does in one glance.

## Fact-sheet density (`sheet`)

| | full (R4.1) | dense |
| --- | --- | --- |
| Type, padding | 14 px, R4.1 spacing | 13 px, tighter cells and headings |
| Sections 1–2 | one attribute per line | a four-column grid. Long values (flavour shift, texture shift, profile note) span the row |
| Section 5, routes | heading, fit reason and element table per route | one table, with a group row per route carrying attestation, availability and fit reason |
| Section 7, intro | three-clause explanation | one line with the same distinctions |
| Everything else | — | identical: the index, the bands, the eight sections, every table row and every link (tested) |

## What was not varied

- **The name column.** It was held fixed to isolate the encoding. The capture showed that it sets the row-height floor (see [evaluation.md](evaluation.md)).
- **Compare, trace and the matrix.** They are R4.1's in every condition.
