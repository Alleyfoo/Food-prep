# Colour worlds: one job per colour

## Why the redesign

**The first palette started from the wrong foundation.** It was seeded from the product's food colours: the `design.css` ramps named ingredient, filler, component and so on, and their amber primary `#6F4102`. After the "no grey" pass, peach was doing at least six jobs:
- the page tint and every neutral;
- the selected row and the "in detail" tag;
- experimental and tasted hypotheses;
- the idea box;
- source nodes in the trace graph;
- open dimensions on the circle.

The whole screen carried one tint, and the tint said nothing. (Review, 2026-11-23.)

**The redesign assigns colour by job, not by food.** Each colour has exactly one job, and structure carries no colour at all.

| Job | What it marks | Colour |
| --- | --- | --- |
| **Structure** | text, lines, fills, headers | cool neutrals (hue 220), quiet |
| **Selection** | the record in detail; also links and focus, the one job "where you act" | blue `#1d52af`, fill `#d9e6fc` |
| **Compare** | pinned records A/B/C, and *differs*, which is part of comparing | violet `#6130a6` |
| **Trace** | the traced entity | magenta `#9d2571` |
| **On hand** | what is in your kitchen | green `#157545` |
| **Hypothesis** | experimental (dashed outline, italic) and tasted (solid outline, bold) | **no hue**: shape and weight carry it |
| **Gap** | not recorded | neutral hatch |

**The circle follows the same jobs.** The product's peach, brown and green states are recoloured by role in the prototype's copy of the data:

| Circle state | Look |
| --- | --- |
| Open dimension | white, with an outline |
| Provided by the state | neutral fill |
| Locked into your dish | selection blue |
| Expanded (fanned out) | solid blue |
| An option you have on hand | green |

When one dimension is fanned out, the other dimensions step back to lighter versions of their roles.

The product component also paints its own warm background (`#F4F2EC`). The prototype serves a generated copy of the component with only that background made transparent (`prototype/r42_circle_component.py`). `src/` is unchanged.

## Three worlds to compare

The worlds differ only in the structure layer. The job colours are the same in white and cool. Pick one in the URL with `pal`:

| `pal` | Page | Fills and lines | Intent |
| --- | --- | --- | --- |
| **white** (default) | `#ffffff` | very light cool fills (`#f4f5f8`) and thin cool lines (`#d9dce3`) | colour appears only where it means something |
| **cool** | faint blue-white `#f4f6fb` | slightly bluer fills (`#eaeef6`) and lines (`#ccd3e1`) | a calmer page, tied to the selection blue |
| **peach** | `#f9f3ec` | the previous palette, unchanged | the reference, for comparison |

**Side by side**, peach, white and cool from left to right: `screenshots/worlds/side-by-side/` covers the detail, compare, trace and circle panes, from `evidence/capture_worlds.py`.

## Checks (`tests/test_r42_palette.py`, `tests/test_r42_circle.py`)

- **Contrast:** every text pair is at least 4.5:1 in every world. That is 24 pairs per world; the lowest is 4.50:1 (secondary text on the selected-row hatch) in white and cool, and 4.68:1 in peach. Every mark that carries meaning is at least 3:1.
- **No food tint in the new worlds:** no structure colour lies within 90° of the peach hue.
- **One job per hue:** selection, compare, trace and on hand are at least 40° apart. Hypotheses carry no hue. *Differs* uses the compare colour, and links use the selection colour.
- **Circle:** in white and cool, every circle colour is one of the world's own tokens. Circle labels are at least 4.5:1 on the page in every world.
- **CSS:** the workspace CSS holds only tokens. There are no hex colours and no translucent tints.
- **URL:** `pal` survives every link and *reset all*. An unknown value falls back to white.

## How it is built

- **`prototype/r42_palette.py`:** the worlds, their tokens, and the contrast pairs. `py -3.11 prototype/r42_palette.py white` prints one world.
- **`r42_views.css(pal)`:** prepends the world's tokens to the workspace CSS. The trace graph reads the same tokens.
- **`prototype/run.py`:** starts Streamlit with the default world as its theme. `app.py` recolours the page and the filter controls for the world in the URL.

## What it does not change

- **Layout.** `metrics.json` is identical before and after.
- **The product app and `src/`.** The product's own palette (`design.css`) still uses the food ramps. Whether the product should follow is a separate decision.
