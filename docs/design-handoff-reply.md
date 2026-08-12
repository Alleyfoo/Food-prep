# Reply to the Ingredient Foundry handoff

Thanks — this is a genuinely useful document. The layout system, the card anatomy and the
copy are all things we want. Before we build, we need to settle five points, and two of the
handoff's core assumptions need to change.

## Two things we're keeping as they are

### 1. Our palette, not Organic's

Not a taste objection — a capacity one. Organic is a two-accent system (terracotta + sage
+ neutrals). Our graphs encode meaning in **five hues**:

| Hue | Meaning |
| --- | --- |
| `#0E7C5A` green | ingredient nodes, "sweet / aromatic / fresh-green" dimensions |
| `#1F6FC4` blue | technique nodes, "salty" dimension |
| `#6B4C8A` purple | component nodes, scout hypotheses, "umami / fermented" |
| `#A5640A` amber | fillers, routes, "sour / nutty / rich-fatty" |
| `#B23B2E` red | destinations, "bitter / pungent" |

Six node types in the pyvis graphs and eleven taste dimensions are drawn from that set.
Collapsing to accent/accent-2 makes a technique node and a component node the same colour,
which is the one thing those screens exist to distinguish.

The good news: our ground is `#F4F2EC` against Organic's `#f5ead8` — practically the same
warm cream. So the composition, spacing, rounding and card system port onto our tokens with
very little change in feel. **What we'd like from you: the component rules re-specced
against our token names** (`--bg`, `--surface`, `--ink`…`--ink-5`, `--line`…`--line-3`,
`--green/--red/--amber/--blue/--purple` each with a `-soft` and `-tint` step). We can send
the current `design.css` `:root` block.

Open question back to you: the tonal ramps are the part of Organic we're missing. Do you
want to generate 100–900 ramps for our five hues on the same perceptual scale, or should we
keep using our existing two-step `-soft` / `-tint` pattern?

### 2. pyvis stays

Map, Scout Map and the Taste Circle Map all stay graph-rendered. Three reasons:

- These graphs get large — broccoli's map is 40 nodes, tomato's Scout Map is 115. Zoom, pan
  and drag are load-bearing, and the prototype's absolutely-positioned divs give up all three.
- The circle map's fixed ellipse coordinate table can't coexist with "disc diameter encodes
  option count" — the discs would collide at the top and bottom of the ellipse once the
  large ones appear.
- It already ships and works, with no build step.

Node **shapes and states** from your spec we can apply directly to the graph builders
(pills, diamonds for scout candidates, size-encodes-count, the provided/open/thin states).
It's only the drawing engine that stays.

## Five things that need a decision

**1. The Taste Circle Map interaction contradicts a change we shipped last week.**
The brief for that change was explicitly "fade everything else so more options fit on
screen". We now fade the unfocused dimensions and fan **14 fillers** onto the canvas around
the expanded one. Your rail shows four chips and "+ 15 more" — four visible options where
we currently have fourteen, and the fade concept disappears entirely. We think this is
information you didn't have. Can you re-spec the rail around the existing on-canvas fan?

**2. Eleven dimensions, not ten.** §9 says eleven and draws eleven; §10 lists ten and its
36° stepping assumes ten. The missing one is Fermented / funky, which §9 marks "No fillers
yet" — that's incorrect for our data. It has exactly one filler (`sauerkraut`) for every
component we checked, which makes it your own **"thin — one option only"** state, not an
empty one. Eleven nodes needs a new coordinate table (or a formula).

**3. The circle-map click contract can't be kept as written.** §10 says keep the existing
`dim:` / `filler:` ids, but your design has no filler nodes on the canvas — fillers are rail
chips. In Streamlit a clickable chip has to be a button widget, so the `filler:` half of the
contract is dead under this design. Which do you want: fillers on the canvas (keeps the
contract) or in the rail (needs a new one)?

**4. The type scale contradicts the stylesheet.** The README says body 16px, small 14px,
"nothing below 14px except the tracked labels". Shipped `styles.css` has `.card-body` 13px,
`.tag` 11px, `.card-kicker` 10px, `.card-meta` / `figcaption` / `.table th` 11px. Which is
authoritative? We'd rather follow the README floor.

**5. Fonts.** Caprasimo is specified for button labels at 14px — a heavy display face at
small sizes. Is that intended, or should buttons use the body face? (Separately: we haven't
decided whether we're adopting Caprasimo/Figtree at all, since we're keeping our own colour
system. Happy to hear the argument for it.)

## Photography

There's no fallback specced for the empty state, and we need one. Four screens
(Ingredient Explorer, Component Explorer, Filler Profiles, Scout) lead with a 200px circular
photo, and the honest scope is:

- **10 full ingredients** — broccoli, cabbage, cucumber, kale, mango, apricot, onion,
  potato, rutabaga, tomato. Tractable.
- **53 components** — this is the hard one. Components are *states*, not ingredients:
  roasted broccoli, steamed broccoli and broccoli soup are three different photos. An
  ingredient photo can't stand in without misrepresenting the state, which is the whole
  subject of the app.
- **Fillers** — 80+ mapped, on the Filler Profiles screen.

Our proposal, unless you disagree: **spec a typographic fallback disc** (in our palette,
using the dimension/ingredient glyph we already carry) that any slot without a photo uses.
Then photos become progressive enhancement — we can start with the 10 ingredients and add
component states over time, rather than blocking the build on ~65 shots.

If you do supply photos: square crops, subject centred, consistent lighting, named to match
our data keys (`broccoli.jpg`, `roasted_broccoli_component.jpg`) so they wire up
automatically.

## What we're taking, unchanged

So this doesn't read as a rejection — the following are all adopted as specced: the two-
column `300px 1fr` grid and its inversion for canvas screens; the card anatomy
(kicker / title / body / 130px label grid); the chip vocabulary and its semantics (tags,
outline for missing roles, sage " — have it" for on-hand fillers); risks as risk chips,
never missing roles; the KPI row on Plate Balance; the topbar and availability-strip
structure; the Scout screen's separation of Compatibility and Novelty into two claims;
the tab rail as pills; and the copy throughout.
