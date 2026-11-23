# Research reconciliation

This document checks R2's findings against the earlier work:

- **R1:** `research/ux-qlik-celonis-r1`. Findings A1–C4, recommendations
  R1–R5.
- **Dembrandt:** `research/ux-dembrandt-r1`. Findings D2–D22.
- **E0/E1:** `docs/research/ux-e0-e1/` on this branch, which covers the
  evaluation and the known limitations.
- **Usability pass 2026-11-21:** `docs/usability/2026-11-21-findings.md`.

The earlier documents were read only after the first-impressions and task
passes were written.

**Categories:**
- **Known, still relevant:** reported before, and still observed in R2.
- **Corrected by E0/E1:** reported before, and no longer observed.
- **New:** first reported here.
- **Suspected, unverified:** plausible, but not confirmed by an observation
  in R2.
- **Design preference:** a judgement about taste or priority, not a defect.

## Known and still relevant

| Earlier finding | R2 observation |
| --- | --- |
| R1 B1 — full graph before the part that matters | Map default view: about 70 nodes, unreadable labels at 1400 px, none at 390 px (`desktop/5-map`, `narrow/5-map`). |
| R1 B4 / Dembrandt D12 — no Map legend; colour carries different meanings across views | No legend on the Map. Taste Circle has one ("already provided / open / thin"), so the two graph views disagree. |
| R1 C2 / R4 — Cook can't tell unknown vs untested idea vs unsuitable | T1: "Not paired here yet" is still the only status. Scout ideas for the same state aren't signposted from Cook. E2 was deliberately not done. |
| R1 C3 / R2 — Scout's rejected reasons hidden | Unchanged (not observed in the UI). |
| Dembrandt D6 — about 22 coined terms | Still the main clarity cost. R2 counts about 20 on first screens, and **four or more names for "a prepared state"** (component, something you already cooked, transformed state, prepared state, dish you are investigating). |
| Dembrandt D5 — view toggles look like navigation | Three look-alike pill levels on four screens. |
| Dembrandt D11 — Map › Scout ideas as a separate view | Still a peer toggle on the Map. |
| Dembrandt D22 — rails wrap on phones | `narrow/1`: the tab row wraps raggedly. |
| E1 limitation — Escape clears "What do I have" | Avoided in scripts by pressing Tab; still present. |
| E1 limitation — graphs not keyboard-operable | Unchanged. |
| E1 limitation — no back/forward history | Unchanged; matters more now that ▶ can move the subject (see N3). |
| Usability 2026-11-21 watch item — is the example plate recognised as an example? | Still unlabelled (`desktop/3`). |
| Usability 2026-11-21 #12 — multiselect loses focus between picks | Scripts click the box before each pick, so not re-observed. Assumed still present. |

## Corrected by E0/E1 (confirmed in R2)

| Earlier finding | R2 evidence |
| --- | --- |
| R1 A1 — re-picking the subject in every view | Strip and pickers agree across the 7 captures, and T3/T4 picks carried over. |
| R1 A2 (partly) — on-hand list invisible on Explore | The strip shows "AVAILABLE …" on Map and Journeys. *Editing* it there is still not possible (the box is hidden). |
| Dembrandt D2 — no URL persistence | `?tab=scout&state=roasted_cabbage_component` opened Scout on roasted cabbage in the browser. |
| Dembrandt D3 — invisible focus on rails | Focus ring visible on the Cook pill after Tab (`tasks/T1-2`). |
| Dembrandt D7 — header counts | Absent. |
| Dembrandt D8 — "no match" vs "Not paired here yet" | Same wording in the helper line and on the cards. |
| Dembrandt D10 — permanent save without review | T5: review panel, Save permanently, Back to edit (`tasks/T5-4`). |
| Dembrandt D16 — dead-end empty states | T3: "No routes modelled from this state yet… absence here means nobody has written one". |
| Usability 2026-11-21 #2 — rich plate never warned | T2: "Avoid adding more of: more fat / cream" at 3.5 / 5. |

## New in R2

| ID | Finding | Evidence | Confidence |
| --- | --- | --- | --- |
| N1 | On the Ingredient Explorer, emphasis (accent border, rank 1) points to Raw Assemble while the subject marker sits on card 2. With on-hand items, rank 1 is the card that uses them *least*, and ranking ignores availability. | `desktop/1`, `tasks/T1-2`, `task-logs/T1-2-after-on-hand.txt` | high (observed) |
| N2 | The T1 answer ("Routes with what you have") is row 9–11 of card 2. Nothing at the top summarises what the on-hand items unlock. | same | high (observed); impact predicted |
| N3 | Taste Circle ◀ ▶ steps through 56 components and **changes the shared subject in every view**, labelled only by a tooltip. | browser check: URL went from `state=roasted_broccoli_component` to `roasted_cabbage_component` | high (observed) |
| N4 | The previous view can linger, faded, for several seconds after a tab switch, looking like the new view. | first `4-taste-circle` capture at 4 s | medium (headless timing; not seen interactively) |
| N5 | The tasting confirmation tells the cook to "Commit that file" and shows a raw temp path. | `tasks/T5-5` | high (observed) |
| N6 | Suggestion chips (Try, Next moves, Use in, fillers) look like tags and are not actionable. The clickable "Other candidates" look like plain text. Affordance is inverted. | `desktop/1,2,3,7` | high (observed); whether users try to click is predicted |
| N7 | "Garlic — not paired here yet" next to "garlic confit — missing but useful" on the same card. | `task-logs/T1-2` | high (observed) |
| N8 | Journeys' "● Built on the dish you are investigating" sits between cards, so the card it refers to is ambiguous. | `desktop/6` | medium |
| N9 | Taste Circle's counts sentence mixes 8 / eleven / "this destination" with no destination chosen; "40 / 56" is unlabelled. | `desktop/4` | high (observed) |
| N10 | Raw id `olive_oil` and Title Case route names ("Sour And Toasted Nut") on the Component Explorer. | `desktop/2` | high (observed). R1 noted raw ids in Map tooltips; this is a second place. |
| N11 | Verdict defaults to "Works". | code `_tasting_reset`, `tasks/T5-4` | high (observed); mitigated by review |
| N12 | Plate Balance KPIs (3 / 0 / 3.5) come before the plain answer. | `desktop/3` | high (observed); impact predicted |

## Suspected, unverified

- **S1:** first-time users will not notice the context strip. It is small and
  grey, below two pill rows. This is untested: E1's evaluation also flagged
  "whether the strip is noticed".
- **S2:** "Explore" and "Experiment" will be confused with each other.
  Untested.
- **S3:** users will try to click suggestion chips (N6). Untested.
- **S4:** the analogy explanation in Scout ("reasoned from roasted broccoli
  with olive oil" on cabbage) reads as an error. The 2026-11-21 pass already
  changed its wording once. Untested with users.
- **S5:** the Map is used for looking around, not for finding things.
  Untested.

## Design preference (not defects)

- The large initial disc (B / RB / RC) costs vertical space without carrying
  information.
- "Download .md" placed between the answer and the routes.
- "Surprise me" as the primary button in Taste Circle.
- Monospace helper captions ("sorts suggestions into…", "Cook mode — no
  experimental pairings").
- Experiment having no tab row, so the layout shifts between sections.
