# Navigation comparison — tool-first vs question-first

No prototype was built. The comparison uses only what exists: the current
rails, and the E1 URL parameters (`tab`, `ingredient`, `state`, `have`).
Those parameters already allow a question to open the right tool on the
right subject. This was verified in the browser:
`?tab=scout&state=roasted_cabbage_component` opens Experiment › Scout on
roasted cabbage.

## The current model: tool-first

```
Cook        Ingredient Explorer · Component Explorer · Plate Balance · Taste Circle
Explore     Map · Journeys · Filler Profiles
Experiment  (Scout, no tab row)
```

The user must translate a cooking question into a section, then a tool.

| Task question (T1–T5) | Tool(s) that answer it | Is the tool name a cue for the question? |
| --- | --- | --- |
| T1 What can I make from what I have? | Ingredient Explorer **plus** the on-hand box (and, partly, Component Explorer, Taste Circle) | No. "Explorer" suggests browsing, and the on-hand box is global. |
| T2 My plate feels heavy | Plate Balance | Yes ("balance"). |
| T3 What do I do with leftovers? | Component Explorer (or Ingredient Explorer › Roast card) | No. "Component" is internal vocabulary; the cue is inside the tab. |
| T4 Something new to try | Experiment › Scout | Partly ("Experiment"). |
| T5 Record what I tried | Experiment › Scout › Record a tasting | No. It's three levels down, under a hypothesis. |
| (not in tasks) Build a dish by taste | Taste Circle | Partly. |
| (not in tasks) Show me a worked example | Journeys | Partly. |
| (not in tasks) What goes with this filler? | Filler Profiles | Partly. |
| (not in tasks) How does everything connect? | Map | Yes. |

**Strengths of tool-first:**
- Tools are stable places to return to.
- Expert users can compare two views of one subject (E1 made this cheap).
- Explore vs Cook keeps experimental ideas out of everyday advice (R1
  strength 5).

**Weaknesses (observed and predicted):**
- Two of five tasks start from a tool name that does not name the question
  (T1, T3).
- One task (T5) lives under another task's result.
- Explore / Experiment are near-homonyms.

## The alternative: question-first, using existing functionality only

A question list that sends each question to an existing tool through the
existing URL parameters. Nothing new is computed.

| Question (user words) | Destination (existing) | URL that does it today |
| --- | --- | --- |
| What can I make with what I have? | Ingredient Explorer, with the on-hand box focused | `?tab=ingredient-explorer&have=…` |
| What can I do with something I already cooked? | Component Explorer | `?tab=component-explorer&state=…` |
| My plate feels off — what's missing? | Plate Balance | `?tab=plate-balance` |
| Help me build a dish by taste | Taste Circle | `?tab=taste-circle&state=…` |
| Show me a complete way to cook X | Journeys | `?tab=journeys&ingredient=…` |
| Something new to try | Scout | `?tab=scout&state=…` |
| I tried something — record it | Scout (Record a tasting) | `?tab=scout&state=…` (the expander still has to be opened) |
| What goes with this ingredient? | Filler Profiles | `?tab=filler-profiles` |
| Show me how it all connects | Map | `?tab=map&ingredient=…` |

**What it would gain (hypothesis):**
- It removes the translation step for first-time users in T1 and T3.
- It surfaces "record a tasting" as a goal in its own right.
- Because E1 already carries the subject, a question can open with the
  subject set, which R1 noted was the precondition ("Test only after R1").

**What it would cost (hypothesis):**
- Nine questions is a menu, not a question. The list would itself need a
  hierarchy.
- Several tools answer more than one question, and T1 is answered *across*
  tools (cards, routes, Taste Circle). A single destination per question
  hides the others.
- Returning users lose a stable map of places.
- Map and Filler Profiles answer exploratory questions that a list frames
  poorly.

## Assessment

**Would question-first navigation help?** For **orientation of first-time
users**, probably yes. Evidence: the tool-name cue fails for T1, T3 and T5.
For **repeat use and comparison**, probably not. The tool rails are the
better structure once learned. The evidence supports a *hybrid*: keep the
rails, and add questions as the *entry* and as *descriptions* of tools.
Replacing the rails is not supported.

What would decide it is whether newcomers, given only the questions, land on
the tool that answers their task faster and with fewer wrong clicks than with
the rails. That can be tested **without code**: give the moderator the
question list above as printed or clickable deep links (session B in the test
pack) and compare with the rails alone (session A).

**Confidence:** low. The task-to-tool mismatch is observed; the benefit is
not.
