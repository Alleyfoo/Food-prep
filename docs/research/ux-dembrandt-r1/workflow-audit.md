# Workflow audit — the five investigations

Executed on `main` (`7bd7b01`) in Chromium and through an AppTest probe. **A
walkthrough, not user testing.** Each important finding: **Observation →
Evidence → User impact → Dembrandt principle → Possible remedy → Confidence.**
"Known" marks findings already in earlier research; see
[`comparison.md`](comparison.md).

---

## A · Navigation — finding the right tool without the internal vocabulary

**Audit for drift (information-architecture's own procedure):** every
navigation target and label, sorted:

| Label | Level | Target | Grouping basis |
| --- | --- | --- | --- |
| Cook / Explore / Experiment | 1 | sections | user activity ✔ one principle |
| Ingredient Explorer | 2 | branches by ingredient | object (*ingredient*) |
| Component Explorer | 2 | one cooked state | object (*component*) |
| Plate Balance | 2 | plate gaps | task |
| Taste Circle | 2 | dish builder | coined metaphor |
| Map | 2 | graph | representation |
| Journeys | 2 | cook paths | content type |
| Filler Profiles | 2 | filler facts | object (*filler*) |
| Scout | 2 | hypotheses | coined mode |
| Map › *Scout ideas* | 3 | hypotheses as graph | **same content as Scout** |

**D6 · Level 2 mixes five grouping principles and coined names**
- **Observation:** the eight tabs are named by object, task, metaphor,
  representation and content type. On screen there are **22 distinct coined or
  domain terms** (component, state, filler, route, destination, journey, role,
  branch, hard gap, target role, plate profile, cook mode, scout, hypothesis,
  novelty, compatibility, corpus, analogy, dimension, taste circle, medium,
  preparation; the last two borderline).
- **Evidence:** [probe output](screenshots/evidence/dembrandt-probe-output.txt), table above.
- **User impact:** to pick a tab, a newcomer must already know what a
  "component" and a "filler" are; nothing on screen explains either.
  *(Hypothesis about severity; the vocabulary load itself is verified.)*
- **Principle:** information-architecture *One grouping principle per level*;
  *Introduce as few new terms as possible: a hard ceiling of ~10*; *Naming
  is design*; nielsen #2, #10.
- **Remedy:** name tabs by what the cook gets ("What can it become?",
  "I already cooked it"…) or add one-line descriptions under the rail; retire
  terms that appear on one screen only.
- **Confidence:** Verified (count, mixture); Hypothesis (how much it slows
  people).

**D11 · Hypotheses live in two places**
- **Observation:** Scout hypotheses appear in Experiment › Scout and in
  Explore › Map › *Scout ideas*.
- **Evidence:** table above; `streamlit_app.py` `tab_map` / `tab_scout`.
- **User impact:** a reader may take them for two different things, and the
  graph version sits under "Explore", outside the Experiment boundary.
- **Principle:** information-architecture *One destination, one place* ("A
  second route belongs in page content, not in the navigation").
- **Remedy:** keep the graph as a link from Scout ("see as graph"), not as a
  separate navigation entry.
- **Confidence:** Supported. It's arguably a *representation* rather than a
  destination; see the conflicts in comparison.md.

**D5 · Three stacked pill rails**
- **Observation:** section › tab › view/mode on Ingredient Explorer, Taste
  Circle and Map; all three use the same pill style.
- **Evidence:** probe ("3 levels ['active_section','active_tab','explorer_mode']" etc.).
- **User impact:** scope is ambiguous: does *Cards* belong to Taste Circle, or
  to Cook?
- **Principle:** tab-navigation *Nested tabs*: "One level of tabs maximum in
  the primary content area"; *Pill / Button Tabs*: pills suit "secondary
  content switches within a section (not page-level)".
- **Remedy:** give the in-panel view switch a visibly different, smaller
  control (segmented control) placed inside the panel header.
- **Confidence:** Verified (structure); Hypothesis (confusion).

**Unnecessary transitions:** a section switch resets to the first tab, and
the subject is re-picked per view. Both **Known** (R1 A1, A3), now also
supported by tab-navigation *State persistence*.

---

## B · Selection continuity — roasted broccoli across views

Re-run of R1's probe logic, now judged by the Dembrandt checklists.

| Check | Result |
| --- | --- |
| Subject carries between views | **No**: six independent pickers (**Known**, R1 A1) |
| On-hand filter carries | Yes, but hidden on Explore while applied (**Known**, R1 A2) |
| Survives a page reload | **No**: reload returns to Cook › Ingredient Explorer with an empty on-hand list (verified in browser) |
| Addressable by URL / back button | **No**: the URL never changes (verified) |

**D2 · Nothing survives a reload, and nothing is linkable**
- **Observation:** a browser reload resets section, tab, subject, on-hand list
  and any built dish; the URL is always `/`.
- **Evidence:** browser check: after switching to Explore, reload →
  `afterReload: ["Cook"]`; `location.href` unchanged after navigation.
- **User impact:** an accidental reload, or a returning visit, rebuilds the
  investigation from scratch; nothing can be bookmarked or shared.
- **Principle:** tab-navigation *State persistence* ("URL fragment or query
  param… supports deep linking and browser back/forward");
  operational-expert-tool-ui *Persistent state*; nielsen #6 ("Does a
  returning user need to remember anything to pick up where they left off?").
- **Remedy:** write section, tab and subject to query parameters; read them on
  load.
- **Confidence:** Verified.

**D20 · The working filter disappears from view**: **Known** (R1 A2), now
with a sharper principle: operational-expert-tool-ui *Workflow-state filters
vs. search filters*: a scope filter is "always visible". Supported.

---

## C · Coordinated data views — Map, Journeys, Component Explorer

Applying coordinated-data-views' **"When to use"** test first: the Map (for
relationships) and the cards (for reading one state) serve different tasks,
so the pattern applies, *if* people move between them. That condition is
unverified; the skill itself warns "if users only ever look at the table and
ignore the visual view, it adds complexity without benefit."

Checklist results:

| Item | Food-prep |
| --- | --- |
| Single shared selection store | ✗ (each view owns its picker) **Known** |
| Click in visual → highlight in list, and back | ✗ (Map clicks are not reported) **Known** |
| Scroll-into-view | n/a (no paired list) |
| Colours identical across views, one source | **✗, new: D12** |
| One shared legend | ✗ (Map has none) **Known**; Taste Circle ✔ |
| Visual-only controls in the visual panel | ✔ (*Cook paths / Scout ideas* sits above the graph) |
| Analysis beside the data, non-modal | ✔ (Scout's claim cards beside the hypothesis) |
| Hover vs selection distinct | ✔ (vis-network default) |
| Mobile: one view at a time | ✔ (only one view exists per tab) |

**D12 · One hue, different meanings in different views**
- **Observation:** green marks *ingredient nodes* on the Map but *provided /
  have it* in chips and the Taste Circle; amber marks *filler and route nodes*
  on the Map but the *primary / selected* state of rails and buttons; purple
  marks both *component* and *hypothesis* nodes.
- **Evidence:** `graph.py:29-38` (`_COLORS`); `design.css:168-180` ("green
  carries 'provided / have it'… Amber carries the primary"); Map and Taste
  Circle screenshots.
- **User impact:** someone who enters lemon and garlic, then opens the Map,
  sees green nodes and may read them as "things I have". The Map doesn't mark
  on-hand items at all. *(Hypothesis.)*
- **Principle:** coordinated-data-views *Consistent colour coding*: "Colour
  meaning must be identical in both views"; "colour encodes state, the label
  encodes identity".
- **Remedy:** either give the Map's node types colours that carry no state
  meaning elsewhere, or move the Map to the Taste Circle's convention (type by
  shape and label, colour for state such as on hand or explored), with a legend.
- **Confidence:** Verified (the mapping); Hypothesis (misreading).
- **Tension:** the five-hue node palette was a deliberate decision
  (`design-handoff-reply.md`, "Our palette"). The finding is about *cross-view
  meaning*, not the palette.

**D13 / D14** (no coordinated selection, no legend) are **Known** (R1 B2–B4).
Journeys and Map still describe the same route and destination nodes with no
link (R1 B3).

---

## D · Visual comprehension

**D3 · Keyboard focus is invisible on the navigation rails**
- **Observation:** tabbing onto a rail pill shows no ring, outline or change
  at all; the focused pill looks exactly like an unfocused one.
- **Evidence:** [`keyboard-focus-on-tab-rail-not-visible.jpg`](screenshots/evidence/keyboard-focus-on-tab-rail-not-visible.jpg);
  DOM check: focused element = the "Ingredient Explorer" radio; its label's
  `outline-style: none`, no `box-shadow`. Likely cause: the pill CSS hides the
  radio dot (`design.css`, "hide the radio dot… display: none"), where
  Streamlit draws its radio styling. Not confirmed against an unstyled radio,
  since every radio in the app is pill-styled.
- **User impact:** keyboard users can't see where they are in navigation.
  Arrow keys do work (they switch sections immediately), so focus is live but
  invisible.
- **Principle:** tab-navigation *States*: Focus: "Visible focus ring (outline:
  2px solid…)"; checklist "Do hover and focus states meet contrast
  requirements?"
- **Remedy:** a `:has(input:focus-visible)` outline on the pill.
- **Confidence:** Verified.

**D22 · Rails wrap at phone width and the two levels merge**
- **Observation:** at 375 px the section rail wraps to two lines and the tab
  rail to three, stacked with no separation.
- **Evidence:** [`mobile-375-rails-wrap-and-stale-hint.jpg`](screenshots/evidence/mobile-375-rails-wrap-and-stale-hint.jpg).
- **User impact:** "Experiment" sits directly on top of "Ingredient Explorer";
  the hierarchy is lost.
- **Principle:** tab-navigation *Tab overflow*: "do not wrap tabs onto
  multiple lines; it destroys the strip metaphor"; *select fallback* preferred.
- **Remedy:** a select fallback for the tab level below a breakpoint.
- **Confidence:** Verified (layout); Supported (impact).

**Also checked, not findings:**
- Typography: cards keep the 14 px floor; Caprasimo is used only for headings.
  The unusual display face is an aesthetic choice, not a defect.
- ARIA: rails are `radiogroup`, not `tablist`. Accessible names are correct,
  arrow keys work, and the semantics are honest for a radio. Recorded as
  **D4**, low.
- Map label size (≈6.6 px): **Known** (R1).

---

## E · Error and uncertainty communication

| Situation | What the user sees | Assessment |
| --- | --- | --- |
| Not on hand | "Missing but useful" | ✔ clear |
| No recorded pairing | "Not paired here yet" (but the hint says "no match": **D8**) | ✔ honest wording, inconsistent label |
| Experimental idea | Scout only, with disclaimer | ✔ boundary kept; not hinted in Cook (**Known**, R1 C2) |
| Unsuitable | Filler Profiles "Avoid when"; `unsuitable_provided` unused | partial (**Known**) |
| Rejected idea | hidden (dead code) | ✗ (**Known**, R1 C3) |
| No journeys / no hypotheses | "No complete journeys modelled for butter yet." / "No generated hypotheses for ghee." | honest, no next step (**D16**) |
| Form error | "Safety_confirmed is required before recording a trial." | raw field name (**D9**) |

**D9 · A raw field name in an error message**: see screen-audit (Scout).
nielsen #2 and #9. **Verified.**

**D10 · Saving a tasting is permanent, with no preview or confirmation**
- **Observation:** *Save tasting* appends straight to `tastings.yaml`. The
  record is append-only by design, so a mistyped verdict or note becomes
  permanent; it can only be followed by a correcting trial.
- **Evidence:** `streamlit_app._tasting_save` →
  `tasting.append_trial_yaml`; no confirm step in the form.
- **User impact:** one mis-click on the verdict is a lasting false record in
  the project's most important evidence.
- **Principle:** nielsen #5 *Error prevention* ("For every destructive or
  irreversible action, is there a confirmation step or an undo path?");
  information-architecture *Confirm dialogs*: "Irreversible state change…
  Yes if no undo".
- **Remedy:** a review step showing the exact entry before it is appended,
  which keeps the record append-only (unlike an undo).
- **Confidence:** Verified (behaviour); Supported (risk).

**D16 · Empty states that stop rather than guide**: see screen-audit
(Journeys, Scout). nielsen #10 ("Empty states are an opportunity for
contextual help"). **Verified.**
