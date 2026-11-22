# State model — shared investigation context

## The three concepts

| Concept | Session key | Example | Identifier |
| --- | --- | --- | --- |
| **Ingredient** | `ctx_ingredient` | tomato | `ingredients.canonical_name` of a tree ingredient (`query.tree_ingredients`) |
| **Prepared state** | `ctx_state` | roasted_tomato_component | `components.name`, or `None` |
| **Available ingredients** | `available_items` | lemon, garlic | `ingredients.canonical_name` list (the existing multiselect key) |

They are never merged. A state implies an ingredient; an ingredient does not
imply a state; the available list is independent of both.

## Invariant and mappings

**Invariant:** if `ctx_state` is set, then
`ctx_ingredient == query.ingredient_for_component(ctx_state)`.

| Mapping | Function | Rule |
| --- | --- | --- |
| state → ingredient | `query.ingredient_for_component(conn, comp)` | the ingredient of the transformation that outputs the state. Every component has exactly one (verified across all 62). The one exception, `tomato_water_component`, is a by-product and maps through `transformation_byproducts` to tomato. Plate items and unknown names return `None`. |
| ingredient → states | `query.states_for_ingredient(conn, ing, profiled_only=False)` | outputs of that ingredient's transformations, in transformation order; `profiled_only` keeps states with a flavour profile (what Taste Circle and Scout can use) |

**Transitions:**

| Event | Effect |
| --- | --- |
| `set_ctx_state(s)` | `ctx_state = s`; `ctx_ingredient` = its ingredient |
| `set_ctx_ingredient(i)` | `ctx_ingredient = i`; if `ctx_state` belongs to another ingredient, `ctx_state = None` (never guessed) |
| a view can't show `ctx_state` | the context is unchanged; the view explains and offers options in an empty picker |
| first load, no URL | `CTX_DEFAULT = ("broccoli", "roasted_broccoli_component")`, the single app-wide default |

## Which view reads what

| View | Reads | Writes on change | If the subject can't be shown |
| --- | --- | --- | --- |
| Ingredient Explorer | ingredient; marks the state's branch | ingredient | if the state's branch is below the top 5, says where to find it |
| Component Explorer | state | state | no state → empty picker plus the ingredient's states |
| Taste Circle (Circle arrows, Cards picker) | state (`tcm_component` follows) | state | no flavour profile / no state → explanation plus picker; the context is not changed |
| Map | ingredient; rings the state node | ingredient | says the state is not drawn in this view |
| Journeys | ingredient; marks journeys whose `primary_component` is the state | ingredient | says none is built on the state |
| Scout | state | state | as Taste Circle |
| Plate Balance, Filler Profiles | — | Filler Profiles' jump button sets ingredient | strip notes these views do not follow the dish |

**Picker mechanics:** before a picker draws, `_sync_picker(key, options,
value)` sets its session value to the context value, or `None` if the view
can't show it (an empty picker with a placeholder). Its `on_change` writes the
context. Passing no `index=` avoids Streamlit's "default value also set via
Session State" warning (see the earlier `_seed` note).

**View-specific state is separate:** `tcm_locked` / `tcm_selections` (the
dish), `tcm_expanded`, `scout_index`, the Map's selected node and all tasting
form keys. The dish resets only when the state really changes, as before.

## Persistence

| Layer | Holds | Lifetime |
| --- | --- | --- |
| Session state | everything above | browser tab session |
| URL query | `ingredient`, `state` (if any), `have` (comma list, if any), `tab` (slug) | survives reload; shareable |

Example: `/?ingredient=cabbage&tab=taste-circle&state=roasted_cabbage_component&have=lemon%2Cgarlic`

**Rules:**
- **Read once per session** (`_ctx_loaded`), before any widget draws. A
  `state` wins over `ingredient`; an `ingredient` alone means no state.
- **Unknown ids are ignored,** never guessed: an unknown state, ingredient or
  tab falls back to the app default for that part; unknown `have` items are
  dropped and known ones kept. Covered by tests.
- **Written after each render, only when different.** Streamlit replaces the
  address rather than adding a history entry.
- **Not serialised:** graph layout, hover or selection, Taste Circle dish,
  expanded dimension, Scout position, form drafts.

**Browser back/forward:** no history entries are created, so Back leaves the
app (or goes to the page before it) instead of stepping through investigation
states. That avoids contradictory states; it doesn't provide undo. See
[limitations.md](limitations.md).
