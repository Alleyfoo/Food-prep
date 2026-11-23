# Implementation — E3 Answer First

Branch `experimental/ux-answer-first`, from `experimental/ux-shared-context`
(`f4ba729`). **Not merged.** Each change is its own commit, so it can be
evaluated or reverted on its own.

| Commit | Change |
| --- | --- |
| `2351ed5` | Answer-first Ingredient Explorer (variant B); variant A kept behind an env var |
| `2e17a1a` | One user-facing name for a prepared ingredient (see [terminology.md](terminology.md)) |
| `dc286fa` | Taste Circle arrows name their target and confirm the change |
| `98fea65` | Explicit tasting verdict; plain save confirmation |
| `22c69b3` | Phone: the decorative disc is dropped in variant B |
| `feb187c` | The answer lists every missing role the card lists |

## 1 · Answer first (Ingredient Explorer only)

**Files:**
- `src/foodprep/ui/answer.py` (new, pure, no Streamlit).
- `streamlit_app._ingredient_explorer_b`.
- `render.branch_card_html(anchor=…)`.
- CSS `.answer-first`.

### Order on the screen (B)

1. **Suggested next step** panel:
   - a headline;
   - *You have / Still needed / Optional / Why*, or the honest fallback
     lines;
   - *Watch for* (risks);
   - links: "See the full … card ↓" and "Other ways to use what you have: …".
2. "● The prepared ingredient you are investigating", then **its** card,
   with the accent border.
3. "Other ways to prepare broccoli · ranked cooking before preservation": the
   remaining cards in their **existing rank**. The first four are shown and
   any others sit in an expander ("4 more ways to prepare potato"). Nothing
   is hidden behind *Choose technique* any more.
4. The *Download .md* button, as before.

The left column adds a **Prepared ingredient** picker. It reads and writes
the E1 shared context (`ctx_state`), so the answer, the bordered card, the
strip and every other view agree. The *Best branches / Choose technique*
mode pills are not drawn in B: the picker does the job of *Choose technique*,
and the expander does the job of the old "below the top five" hint.

### Presentation rule (deterministic; no new engine)

The answer is **always about the investigated prepared ingredient**.
Nothing is re-ranked. Every word comes from data the cards already draw:
`all_branch_cards`, `flavour_routes_for_component` and `available_filter`.
These are called once, and the same objects feed both the answer and the
card.

| Situation | Answer kind | Content |
| --- | --- | --- |
| No prepared ingredient chosen for this ingredient | `no_state` | "Choose how the cabbage is prepared". **Does not pick one.** |
| Items on hand, and a route from this state uses one | `route` | The first such route in the query's own order (most required elements on hand, then route id). Shows *You have* (on-hand elements), *Still needed* (required, not on hand), *Optional* (finish/supporting, with the route's own contribution text) and *Why* (route description + fit reason). Route risks are added to *Watch for*. |
| Items on hand, no route uses them, single pairings on hand | `pairings` | "Add lemon to roasted cabbage". *Still missing* roles with one example filler. *Why* says they are single pairings and no route uses what you have. |
| Items on hand, nothing paired | `no_match` | "Nothing you have is paired with … yet", the roles it usually needs, and "not that it clashes". |
| Nothing on hand, a route exists | `recorded_route` | "One way with …: …", its required and optional elements, and its fit reason. |
| Nothing on hand, no route, fillers exist | `needs` | "What … usually needs", every missing role with its first curated filler, and "No flavour route is written … yet". |
| Nothing recorded | `limited` | "Little is recorded for … yet … Nothing here is a recommendation." |

Two more rules:
- **Always shown:** the state's risks (and the chosen route's). Safety text
  is never hidden.
- **"Other ways to use what you have":** the other preparations of the same
  ingredient, in card rank, with a route that uses an on-hand item. Each
  links to its card.

### Answer ↔ evidence

- Every card carries `id="card-<component>"`. The answer's links are plain
  in-page anchors, so no rerun happens. In the browser, clicking a link
  scrolled to the card.
- Tests check that every anchor in the answer resolves to a rendered card,
  and that the route, the on-hand items and the missing roles in the answer
  are the same as on the card.

### A/B switch (development only)

`FOODPREP_EXPLORER_VARIANT=A` before starting Streamlit draws the previous
function `_ingredient_explorer_a`, unchanged except for the shared
terminology strings. The default is B. There is **no** in-app selector and
no query parameter, so nothing consumer-facing was added. It is read on
every run, so tests can switch it.

```powershell
$env:FOODPREP_EXPLORER_VARIANT = "A"; py -3.11 -m streamlit run app.py --server.port 8510
```

### Phone

On phones (≤ 640 px) B hides the decorative initial disc. The ingredient
name directly below it carries the same information. The rest of the
phone's first screen is the app's shared chrome (header, on-hand box, two
rails, strip, about 610 px), which E3 deliberately left alone.

## 2 · Terminology
See [terminology.md](terminology.md).

## 3 · Taste Circle navigation

**Before:** `◀` and `▶` with a tooltip, "Next component", and "40 / 56".

**After:**
- The buttons read `◀ roasted broccoli` and `roasted potato ▶`, naming the
  prepared ingredient they will select.
- The tooltip reads "Investigate roasted potato instead, in every view".
- The position reads "prepared ingredient 41 of 56".
- A standing hint says the arrows change the investigated prepared
  ingredient in every view.
- After a step, a one-time status line (`role="status"`) says "Now
  investigating **roasted cabbage** instead of roasted broccoli, in every
  view." It disappears on the next interaction.

The shared-subject behaviour is unchanged (E1), and Taste Circle itself was
not rebuilt.

## 4 · Tasting form

- **Verdict:** no default (`_tasting_reset` sets `None`). The picker shows
  "Choose a verdict". Review is refused with "Choose a verdict." until one is
  chosen.
- **Success message:** "Saved: roasted broccoli + brown butter, “Promising”,
  2026-11-23. It is now in the trial history below." It has no path and no
  "commit". Where the record lives is already in the README.
- **Unchanged and tested:** review before save, Back to edit, the
  single-write token, the append-only duplicate refusal (same pairing, same
  day), and the isolated `FOODPREP_TASTINGS_PATH` in tests.

## Not changed
- The culinary data, the route and filler ordering, the ranking of cards,
  and the graph engine.
- E2 work, other screens' hierarchy, and navigation.
- The *Component Explorer* tab name (see terminology).
