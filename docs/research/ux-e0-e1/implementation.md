# Implementation — UX experiment E0 + E1

**Branch:** `experimental/ux-shared-context`, cut from `main` at `7bd7b01`. Not
merged. Commits: `ae7a2da` (E0 + E1), `a973110` (fix found in the browser
check).

**Sources:**
- **E1** is experiment E1 in
  [`research/ux-qlik-celonis-r1` › prototype-plan.md](https://github.com/Alleyfoo/Food-prep/blob/research/ux-qlik-celonis-r1/docs/research/ux-qlik-celonis-r1/prototype-plan.md).
- **E0** is Priority 1 of
  [`research/ux-dembrandt-r1` › recommendations.md](https://github.com/Alleyfoo/Food-prep/blob/research/ux-dembrandt-r1/docs/research/ux-dembrandt-r1/recommendations.md).
- Neither research branch was merged here.

**Files changed:** `src/foodprep/ui/streamlit_app.py`, `src/foodprep/query.py`
(two read-only helpers), `src/foodprep/ui/design.css`, plus tests. **Not
touched:** culinary data, pairing logic, Scout rules, evidence rules, the graph
engine, the Taste Circle component, the navigation hierarchy. No new
dependencies.

---

## E0 — usability repairs

| # | Finding (source) | What changed | Where |
| --- | --- | --- | --- |
| 1 | **D3** keyboard focus invisible on rails | `:focus-visible` ring (3 px ink) on pills, buttons, the expander header, checkboxes. Mouse clicks show no ring. | `design.css` "Keyboard focus" |
| 2a | **D8** hint said "no match", cards say "Not paired here yet" | Hint now reads "sorts suggestions into available now · missing but useful · not paired here yet" | `available_selector` |
| 2b | **D9** "Safety_confirmed is required…" | Fields are checked before review; messages name the form's own labels ("Fill in “What you tasted”.", "Tick “Everything was safely prepared…”"). The duplicate-date refusal is reworded too. | `_tasting_problems`, `_tasting_confirm` |
| 2c | **D6** (one screen) "component" vs "Something you already cooked" | Component Explorer's note now uses the heading's words. Specialist vocabulary elsewhere was left alone, as the brief asks. | `tab_component_explorer` |
| 3 | **D10** permanent save with no review | Two steps: **Review tasting** shows the exact entry ("Check before saving — this cannot be changed afterwards"); **Save permanently** writes it; **Back to edit** returns with all text kept. A one-time token plus pop-before-write means reruns, repeat clicks and stale buttons cannot write twice. Append-only `tastings.yaml` and `append_trial_yaml` are unchanged. | `_tasting_review`, `_tasting_confirm`, `_tasting_edit`, `_tasting_form` |
| 4 | **D16** dead-end empty states | Journeys: "Nobody has written a complete cook path for X yet. That is a gap in the catalogue…" plus an "Open X in Ingredient Explorer" button. Scout: what was checked and why nothing fits ("None of the 51 analogy rules fits ghee: N are written for a different kind of dish…, M need flavours…"), "a limit of the rule set, not evidence that nothing pairs", and states of the same ingredient that do have ideas. Map's Scout view with no hypotheses says the same. Filler Profiles: "missing catalogue knowledge, not a sign it pairs badly". | `tab_journeys`, `_no_hypotheses_html`, `tab_map`, `tab_filler_profiles` |
| 5 | **D7** header catalogue counts | Removed ("11 full ingredients · 62 components · 29 plate profiles"). Brand and subtitle kept. | `topbar` |

Nothing invents a recommendation: the Scout empty-state counts come from the
same generator with rejections included.

## E1 — shared investigation context

Detailed rules are in [state-model.md](state-model.md). In short:
- **One context, three separate things:** `ctx_ingredient`, `ctx_state`,
  `available_items`.
- **Pickers:** every subject picker is filled from the context before it draws
  (`_sync_picker`) and writes back on change (`_picked_state`,
  `_picked_ingredient`). That covers Ingredient Explorer, Component Explorer,
  Taste Circle (arrows and Cards picker), Map, Journeys and Scout. The four
  per-view broccoli defaults are gone; one app default (`CTX_DEFAULT`) remains.
- **State → ingredient** is deterministic: `query.ingredient_for_component`,
  with by-products included. Changing the ingredient drops a state that belongs
  to another ingredient; it never picks a substitute.
- **Views that cannot show the subject explain why** (`_explain_unrepresentable`)
  and offer the real alternatives in an empty picker. Taste Circle and Scout
  need a flavour profile. Map and Journeys are per ingredient, so they show the
  ingredient, ring the investigated state on the Map, and mark journeys built
  on it.
- **Context strip** (`context_strip`): "INVESTIGATING Roasted cabbage · from
  cabbage   AVAILABLE lemon, garlic", on every tab. On Explore it shows the
  on-hand list the box hides; on Plate Balance and Filler Profiles it notes
  that the view does not follow the dish.
- **URL:** `?ingredient=…&state=…&have=…&tab=…`, read once per session
  (`load_context_from_url`), written when it changes (`write_context_to_url`).
- View-specific state stays in its view: a Taste Circle dimension or locked
  filler, the Map's selected node, Scout's current hypothesis.

**Variant chosen:** R1's plan offered E1a (default only) and E1b (linked). The
brief's synchronisation rules describe E1b, so a picker change anywhere moves
the subject everywhere. E1a was not built.

## Found and fixed during the browser check
- "Back to edit" collapsed the tasting expander and hid the form. Fixed in
  `a973110` (`tasting_editing` keeps it open); assertion added.

## Deliberately not done (left for later rounds)
- **E2** (show rejected Scout hypotheses; mark untested ideas in Cook): not
  started, per the brief. The dead "Show rejected" expander is untouched.
- **Dembrandt D2 beyond the subject:** section/tab are in the URL, but the
  browser back button does not step through states (see
  [limitations.md](limitations.md)).
- **D12** (colour meaning across views), **D22** (rails wrap on phones),
  **D5** / **D11**, and Map focus/legend/inspect (R1 R3): untouched.
