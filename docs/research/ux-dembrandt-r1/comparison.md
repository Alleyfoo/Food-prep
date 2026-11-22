# Comparison with earlier research

Compared against:
- **U1:** `docs/usability/2026-11-21-findings.md` (developer walkthrough of
  five task scripts, 13 findings), on `main`.
- **R1:** Qlik/Celonis research, branch `research/ux-qlik-celonis-r1`
  (`8fe5884`), not merged; read from that branch.

Classes, as requested:
1. **Previously known**: Dembrandt reaches the same conclusion.
2. **New and independently supported**: not in U1 or R1, and verified in the
   app or code.
3. **Useful but unverified**: plausible; its benefit needs users.
4. **Generic, no demonstrated benefit**: true as a rule, but nothing shows
   it matters here.
5. **Conflicts with Food-prep's requirements.**

---

## 1 · Previously known (Dembrandt adds a named principle, not a discovery)

| Finding | Earlier source | Dembrandt principle now attached |
| --- | --- | --- |
| Subject never carries between views | R1 A1 | coordinated-data-views *single shared store*; nielsen #6 |
| Section switch resets the tab | R1 A3 | tab-navigation *State persistence* |
| On-hand list hidden on Explore while applied | R1 A2 | operational *Workflow-state filters always visible* |
| Map: no coordinated selection, no details on click | R1 B2, B3 | coordinated-data-views core rule |
| Map: no legend | R1 B4 | coordinated-data-views *shared legend once* |
| Map labels ≈6.6 px | R1 B1 | nielsen #8 |
| Rejected hypotheses never shown | R1 C3 | nielsen #9 |
| Untested idea vs nothing known look the same in Cook | R1 C2 | nielsen #2 |
| `unsuitable_provided` never shown | R1 | nielsen #1 |
| Colour-only availability on route cards | R1 C4 | operational *status label beside colour* |
| Taste Circle dish wiped on state change | R1 matrix #9 | nielsen #3, #5 |
| "No match" read as "doesn't go with" | U1 #4 (fixed) | IA naming (and see D8: the fix was incomplete) |

**12 of the important findings were already known.** In each case
Dembrandt's checklist would have found them independently, which is a fair
sign the checklists work, but it added no new knowledge.

## 2 · New and independently supported

| Id | Finding | Principle | Evidence | Missed earlier because… |
| --- | --- | --- | --- | --- |
| **D3** | Keyboard focus invisible on the navigation rails | tab-navigation *States: Focus* | browser + screenshot | U1/R1 never used a keyboard |
| **D2** | Reload resets everything; URL never changes; no deep link | tab-navigation *State persistence*; operational *Persistent state* | browser | R1 tested within one session only |
| **D8** | Hint says "no match", cards say "Not paired here yet" | nielsen #4; IA *Naming* | screenshot + source line | the U1 fix renamed the cards, not the hint |
| **D9** | Error shows a raw field name ("Safety_confirmed…") | nielsen #2, #9 | probe | the form shipped after U1; R1 didn't test errors |
| **D10** | Saving a tasting is permanent with no review step | nielsen #5; IA *Confirm dialogs* | code | append-only was treated as a data rule, not a UX risk |
| **D12** | Same hue means different things on the Map and elsewhere | coordinated-data-views *Consistent colour coding* | code + screenshots | R1 noted no legend, not conflicting meanings |
| **D7** | Header counts ("62 components", "29 plate profiles") on every screen | nielsen #2, #8 | probe + screenshots | treated as chrome |
| **D6** | 22 coined terms on screen; tab level mixes five grouping principles | IA *~10 term ceiling*, *one grouping principle per level* | probe + drift table | R1 noted vocabulary, without a measure or a rule |
| **D16** | Empty states (Journeys/butter, Scout/ghee) stop instead of guiding | nielsen #10 | probe | neither pass tried empty cases |
| **D22** | Rails wrap at 375 px and the two levels merge | tab-navigation *Tab overflow* | screenshot | an earlier fix stopped clipping but kept wrapping |

**Ten new findings.** D3, D8, D9 and D10 are concrete defects with small
remedies. D2, D6 and D12 are structural and need decisions.

## 3 · Useful but unverified

| Id | Suggestion | Why unverified |
| --- | --- | --- |
| D5 | Three stacked pill rails read as nested tabs | the section/tab split was a deliberate design; whether people misread scope needs observation |
| D11 | Hypotheses in two places (Scout tab and Map › Scout ideas) | can be read as one destination in two places or as two representations; needs users |
| — | Name tabs by goal ("I already cooked it") rather than object | IA principle; plausible, but changes learned names (IA itself warns: "Do not mess with the structure casually") |
| — | Global search as an escape hatch | IA recommends it beyond 3 navigation levels; Food-prep is at 2 (3 counting view toggles) |

## 4 · Generic, without demonstrated benefit here

| Suggestion | Source | Why it does not earn a place |
| --- | --- | --- |
| Logo links home | IA *Logo as Home* | single page; "home" is one click (Cook) and nothing is lost by not linking |
| Underline only the active tab, no rule under the strip | tab-navigation | aesthetic; the rule under the rail separates navigation from content in the established design |
| Use `role="tablist"` instead of radios | tab-navigation *ARIA* | radios are accessible, named and keyboard-operable; the change matters only if testing with screen-reader users shows confusion (**D4**) |
| Keyboard shortcuts for frequent actions | nielsen #7; operational | no frequent repetitive action exists for a home cook |
| Confirm dialogs for deletion or bulk changes | IA | nothing in the app deletes or bulk-changes; only D10 applies |

## 5 · Conflicts with Food-prep's requirements

| Recommendation | Source | Conflict |
| --- | --- | --- |
| "Information over whitespace"; compact 28–36 px rows; secondary attributes inline | operational-expert-tool-ui *Primary design principles* | written for "trained domain specialists… for the entire working day". Food-prep is for home cooks; the design has a 14 px floor and spacious cards by explicit decision. **Misapplied if followed.** |
| Hierarchical accordion tables instead of drill-down | operational | the data is a graph of states, not order → line hierarchies; the cards already disclose progressively |
| Bulk-operation feedback scaled by count | operational | no bulk operations exist |
| "Colour encodes state, not identity" applied to the Map's node types | coordinated-data-views | the five-hue type palette is a documented decision (`design-handoff-reply.md`). D12 keeps the conflict narrow: fix *cross-view meaning*, not the palette itself |
| Undo for saved tastings | nielsen #3 | the tasting record is append-only by design; Dembrandt's alternative of confirmation (D10) fits, undo does not |
| Show everything in one coordinated layout (table + graph side by side) | coordinated-data-views *Layout* | not a misunderstanding of the skill (it says to use it only if users move between views), but adopting it before knowing whether anyone uses the Map would add complexity |

**Was the application misunderstood?** Only by **operational-expert-tool-ui**,
and only if its advice is applied without its own scope test. Read
carefully, the skill states its audience in the first paragraph, and that
audience is not Food-prep's.
