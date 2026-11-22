# Recommendations

**Research only. Nothing here is implemented.** Ranked by *evidence ×
benefit ÷ cost*. Each preserves the Cook/Scout boundary, the visual identity
and the append-only tasting record.

## Priority 1: verified defects with small remedies

| # | Finding | Remedy | Principle | Cost |
| --- | --- | --- | --- | --- |
| 1 | **D3** Keyboard focus invisible on rails | visible outline on `:has(input:focus-visible)` pills | tab-navigation *Focus* | tiny (CSS) |
| 2 | **D8** "no match" hint vs "Not paired here yet" | align the hint with the card labels | nielsen #4 | tiny (copy) |
| 3 | **D9** "Safety_confirmed is required…" | map field ids to plain labels in form errors ("Tick the safety confirmation to save") | nielsen #2, #9 | small |
| 4 | **D10** Permanent save, no review | a review step showing the exact entry before appending (keeps append-only) | nielsen #5; IA *Confirm dialogs* | small |
| 5 | **D16** Dead-end empty states | one line of next step: "Ingredient Explorer has butter's branches"; "Scout rules don't cover cooking fats" | nielsen #10 | small |
| 6 | **D7** Header counts | remove from the header | nielsen #2, #8 | tiny |

## Priority 2: structural, needs a decision

| # | Finding | Option to evaluate | Principle | Note |
| --- | --- | --- | --- | --- |
| 7 | **D2** No reload persistence, no deep link | section, tab and subject in query parameters | tab-navigation *State persistence* | pairs naturally with R1's E1 (shared subject): the subject becomes one URL parameter |
| 8 | **D12** One hue, several meanings | keep type colours but stop reusing green and amber for state, or move the Map to Taste Circle's "colour = state" convention plus a legend | coordinated-data-views *Consistent colour coding* | touches the palette decision; designer input needed |
| 9 | **D6** 22 coined terms, mixed tab grouping | first remove one-screen terms (branch, hard gap, target role, plate profile, cook mode); then consider goal-named tabs | IA *~10 terms*, *one grouping principle* | renaming tabs spends learned names; test before changing |
| 10 | **D22** Rails wrap on phones | select fallback for the tab level | tab-navigation *Tab overflow* | only if phone use matters |

## Priority 3: test before acting

- **D5:** a smaller in-panel control for view toggles (*Circle / Cards*,
  *Cook paths / Scout ideas*, *Best branches / Choose technique*), so they
  stop reading as a third navigation level.
- **D11:** fold Map › *Scout ideas* into a "see as graph" link from Scout.

Both depend on observing real people. Add a question for each to the next
round of task scripts.

## Rejected

| Suggestion | Reason |
| --- | --- |
| Dense, compact operational layout (28–36 px rows, inline secondary data) | wrong audience; conflicts with the 14 px floor and spacious card design |
| Accordion tables | data is a state graph, not a hierarchy |
| Keyboard shortcuts | no frequent repetitive task |
| Undo for tastings | violates append-only; the review step (4) achieves the safety |
| Logo as home link; underline-only tab indicator | no demonstrated benefit; aesthetic |
| `tablist` semantics | radios are accessible today; revisit only with screen-reader feedback |

## Relationship to earlier plans
- R1's E1 (shared subject) and E2 (show rejection reasons) stand; Dembrandt
  independently supports both.
- Items 1–3 and 6 are small enough to batch with E2 as one polish change.
- Item 7 (URL state) should be designed together with E1, since they share
  a mechanism.

---

## Evaluation of Dembrandt itself

**1. Did it find anything important that earlier research missed?** Yes:
ten new findings. Four are concrete defects (**D3** invisible keyboard focus,
**D8** inconsistent label, **D9** raw field name in an error, **D10**
irreversible save with no review). Three are structural (**D2** no reload or
URL persistence, **D12** colour meaning differs across views, **D6** 22
coined terms). The most valuable were D3 and D10. Neither earlier pass
tested with a keyboard, and both treated append-only as a data rule rather
than a UX risk.

**2. Which skills were genuinely useful?**
- **tab-navigation: most productive.** Its concrete checks (focus state,
  persistence, overflow, nesting) turned directly into browser tests and three
  new findings.
- **nielsen-usability-heuristics: useful as a sweep.** The review questions
  caught the error wording, the irreversible save and the empty states.
- **information-architecture: useful.** The "audit for drift" procedure and
  the ~10-term ceiling gave a *measurable* version of a vague worry about
  jargon.
- **coordinated-data-views: useful, narrowly.** It mostly re-derived R1's
  graph findings, but its colour rule produced D12.
- **operational-expert-tool-ui: least useful here.** Its audience test rules
  most of it out; its one transferable idea (keep the scope filter always
  visible) was already known.

**3. Did any recommendations misunderstand the application?** Only
operational-expert-tool-ui, and only if applied past its own stated scope:
density over whitespace, compact rows, accordions, shortcuts. The
coordinated-data-views colour rule touches a deliberate palette decision; the
finding was narrowed to cross-view meaning to respect it.

**4. Does it improve our ability to evaluate complex information interfaces?**
Moderately. It adds **checklists with specific, testable items** and a
**vocabulary of named principles** that makes findings easier to argue. It
doesn't replace task-based or comparative research: the biggest problem
(subject continuity) was found first by R1's scenario testing, and no skill
asks "can the user complete their task?". It found breadth (many small, real
defects) where R1 found depth.

**5. Should Micro-scope UX research adopt it?** **Yes, selectively, as a
checklist pass after task-based testing, not instead of it.** Use
tab-navigation, nielsen-usability-heuristics and information-architecture by
default. Use coordinated-data-views when a screen shows the same data two
ways. Use operational-expert-tool-ui only for tools whose users are trained
daily operators. Keep reading the `SKILL.md` files directly; nothing in this
round needed the package or its install scripts.
