# Palette: colours and tint derived, not picked

> **Revised: no grey (2026-11-23).** On review, the skill's neutrals (3–12% saturation) still read as grey. Every neutral is now a clearly coloured tone of the seed hue, at 24–50% saturation:
> - the page is warm paper, `#f9f3ec`;
> - fills are cream, `#f2eade`;
> - lines are sand, `#dccfbc`;
> - text is roasted brown: body `#221b11`, secondary `#6d5a40`.
>
> Two more changes:
> - Concept fills are a step stronger, so a selected row still stands out on the cream page.
> - The circle's own greys are recoloured in the prototype's copy of the graph data. Its open-dimension labels went from about 2:1 to at least 4.5:1.
>
> Streamlit's own labels, placeholders and icons take the palette through `prototype/run.py`, which starts the app with theme flags. A test checks that no workspace token, and no circle colour, is below 20% saturation.
>
> The tables below are updated to the revised palette.

**Why.** The workspace had grown about 60 hand-picked colours: near-duplicate warm greys, an amber "in detail" highlight, five greys that fail WCAG AA as text, and a green used for both "on hand" and the Taste circle tab.

**Method.** Three skills from [dembrandt-skills](https://github.com/dembrandt/dembrandt-skills), read as guidance; nothing from the repository is installed or run:
- `algorithmic-color-palette`: derive every colour from the brand seed.
- `wcag-accessibility`: 4.5:1 for text, 3:1 for marks that carry meaning.
- `surface-separation`: tints are solid tokens, not transparency.

The code is in `prototype/r42_palette.py`. `py -3.11 prototype/r42_palette.py` prints every token and every contrast pair.

## What it derives

**The seed** is the product's own primary, `--filler-700` `#6F4102` in `src/foodprep/ui/design.css`, which is hsl(35, 96%, 22%).

| Role | How | Result |
| --- | --- | --- |
| **Page tint** | Seed hue, 50% saturation, 95% lightness | `#f9f3ec`, warm paper behind every pane |
| **Surfaces** (chips, tags) | Cream, not pure white | `#fdf9f4` |
| **Text** | Seed hue, 35% saturation, 10% lightness: near-black brown, not `#000` | `#221b11` |
| **Neutrals** (borders, headers, hatches) | Seed hue at 24–50% saturation, more towards the light end so nothing washes out to grey (the skill's steps lose saturation as they lighten; overridden on review) | 9 tones instead of about 30 ad-hoc greys |
| **Secondary text** | The lightest seed-tinted grey that passes 4.5:1 on every fill it sits on | `#6d5a40` |
| **Concept colours** | Each concept keeps its hue and takes the seed's saturation and lightness, so none reads louder than another | |

Each concept colour comes in five variants: base (text), deep (emphasised), mid and border (outlines), subtle (selected row, chips, tags) and faint (large boxes).

| Concept | Hue | Base |
| --- | --- | --- |
| In detail; experimental and tasted (text only) | seed, 35 | `#6f4102` |
| Compare | 215 | `#022f6f` |
| Trace | 268 | `#35026f` |
| On hand | 145 | `#026f2f` |
| Differs | 4 | `#6f0902` |
| Links | 215, lighter, using the skill's "high-visibility blue" option | `#1750a1` |

## What changed on screen

- **The page is tinted.** It is no longer pure white with ad-hoc warm greys on top.
- **The selected row** is a pale tint of the seed (`#f6ecdf`) instead of saturated cream `#fff4d1`. The skill reserves amber-yellow for warnings.
- **Compare, trace and differs tags** have pale fills and outlines in their own hue, with dark text in the same hue.
- **On-hand chips in the filter bar** use the on-hand green, so "on hand" is one green everywhere. Streamlit's theme green is overridden here only. The repo's `.streamlit/config.toml` is shared with the product and is unchanged.
- **The Taste circle tab** uses a neutral top edge, because green means "on hand".
- **The trace graph** (Graphviz) reads the same tokens.

## Contrast, before and after

The rendered page was checked too: on the broccoli state with compare and trace active, the lowest text contrast is **5.10:1** across 144 text elements. Hatched fills are checked in code instead.

| Text | Before | After |
| --- | --- | --- |
| Repeated names in the trace table | 2.47 | 6.29 |
| Excluded (greyed) rows | 2.76 | 5.52 |
| n/a | 2.98 | 6.29 |
| Identical rows in compare, section numbers | 3.57 | 6.29 |
| Secondary text on the darkest hatch (selected row) | 5.34 | 4.68 |
| All 22 text pairs, lowest | 2.47 | **4.68** |

**The trade-off.** De-emphasised text (excluded rows, identical rows, repeated names) used to be faint grey, and faint grey fails AA. It now uses the passing secondary grey. Its de-emphasis is carried by the row fill and the words already on screen ("excluded: …", "same"), not by colour alone.

## Departures from the skill

- **The skill's subtle fill** (saturation × 0.3, 94% lightness) is almost the page colour, so a selected row would not stand out. Fills follow the skill's *selection* rule instead: 90%+ lightness, moderate saturation.
- **The skill's neutrals lose saturation as they lighten,** down to 3%. On review that read as grey, so the neutrals keep 24–50%.
- **The skill's grey-500 step** (50% lightness) is listed for secondary text but fails 4.5:1. Secondary text is darkened until it passes everywhere.
- **The embedded Taste circle** keeps the product's component and its background (`#F4F2EC`, already warm). Only its grey node, edge and label colours are recoloured, in the prototype's copy of the data.

## Not changed

- **Layout:** sizes, spacing and the measurements in evaluation.md. The colour change does not move anything.
- **The product app and `src/`.**
