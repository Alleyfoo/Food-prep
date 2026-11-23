"""The workspace palette, derived from one seed instead of picked by hand.

Method: dembrandt-skills `algorithmic-color-palette`, checked against
`wcag-accessibility` and `status-colors-and-errors`
(https://github.com/dembrandt/dembrandt-skills).

- Seed: the product's primary, --filler-700 #6F4102 in src/foodprep/ui/design.css.
- Neutrals: the seed hue, desaturated, saturation falling as lightness rises
  (steps 900 ... 50). No generic greys, no pure black on pure white.
- Concept colours: each concept keeps its hue (selection = the seed, compare
  blue, trace violet, on hand green, differs red) and takes the seed's
  saturation and lightness, so none reads louder than another. Each concept
  gets base (text), border (the skill's tint, L + 40) and subtle (fill:
  S x 0.3, L 94) variants.
- One meaning per colour: the circle pane's tab, which used green, moves to
  a neutral, because green means "on hand".
- Contrast: every text colour is checked against every fill it sits on
  (pairs below, test in tests/test_r42_palette.py). Where the skill's
  neutral step fails 4.5:1, the step is darkened until it passes; that is
  the only departure from the skill's numbers.
"""
from __future__ import annotations

import colorsys

SEED = "#6F4102"


def hex_to_hsl(h: str) -> tuple[float, float, float]:
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (1, 3, 5))
    hh, ll, ss = colorsys.rgb_to_hls(r, g, b)
    return hh * 360, ss * 100, ll * 100


def hsl(h: float, s: float, l: float) -> str:
    r, g, b = colorsys.hls_to_rgb((h % 360) / 360, max(0, min(l, 100)) / 100,
                                  max(0, min(s, 100)) / 100)
    return "#{:02x}{:02x}{:02x}".format(*(round(x * 255) for x in (r, g, b)))


def luminance(h: str) -> float:
    def ch(v: float) -> float:
        return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = (ch(int(h[i:i + 2], 16) / 255) for i in (1, 3, 5))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a: str, b: str) -> float:
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


H, S, L = hex_to_hsl(SEED)

# brand-tinted neutrals: (step, saturation, lightness) from the skill
# No grey (user request, 2026-11-23): the skill's neutrals (3-12% saturation)
# read as grey, so every neutral is a clearly coloured tone of the seed hue:
# warm paper for fills, sand for lines, roasted brown for text. Saturation
# rises towards the light end, where a low value would wash out to grey.
NEUTRAL_STEPS = [(900, 35, 10), (700, 28, 27), (600, 26, 36), (500, 24, 46), (300, 28, 68),
                 (200, 32, 80), (150, 36, 86), (100, 42, 91), (50, 50, 95)]
NEUTRAL_MIN_SAT = 20         # below this a tone starts to read as grey
N = {step: hsl(H, s, l) for step, s, l in NEUTRAL_STEPS}

CONCEPT_HUES = {"sel": H, "cmp": 215, "trace": 268, "have": 145, "diff": 4}


def concept(hue: float) -> dict[str, str]:
    return {"base": hsl(hue, S, L),            # text, rules, focus edge
            "deep": hsl(hue, S, L - 6),         # emphasised text (tested)
            "mid": hsl(hue, S * 0.75, L + 18),  # dashed / secondary borders
            "border": hsl(hue, S * 0.6, L + 40),
            # fills. The skill's "subtle" (S x 0.3, L 94) is too close to the
            # page to mark a selected row, so fills follow its "selection"
            # rule instead: L 90+, moderate saturation.
            # (on the cream page a fill needs more colour to stand out)
            "subtle": hsl(hue, S * 0.8, 88),    # selected row, chips, tags
            "subtle2": hsl(hue, S * 0.65, 82),  # second stripe of a hatched fill
            "faint": hsl(hue, S * 0.4, 97)}     # large calm fills (idea box)


C = {k: concept(h) for k, h in CONCEPT_HUES.items()}
INK = N[900]                 # near-black body text
SURFACE = hsl(H, 70, 97.5)    # cards, chips: a cream, not pure #fff
PAGE = N[50]                 # the page behind the panes
# The skill allows "primary or a dedicated high-visibility blue" for links.
# At the seed's lightness (22%) blue reads as black, so links are lighter.
LINK = hsl(215, 75, 36)


def _passing(bgs: list[str], start: float, target: float = 4.5, s: float = 26) -> str:
    """Lightest seed-tinted grey at or below *start* lightness that reaches
    *target* on every fill in *bgs*."""
    l = start
    while min(contrast(hsl(H, s, l), bg) for bg in bgs) < target and l > 0:
        l -= 1
    return hsl(H, s, l)


# Secondary text must pass 4.5:1 on the darkest fills it sits on (the
# hatches). De-emphasised text (excluded rows, "same" rows, repeated names)
# is still data, not a disabled control, so it gets the same grey; the
# de-emphasis is carried by the row fill and the words ("excluded", "same").
SECONDARY = _passing([C["sel"]["subtle2"], N[100]], 40)

TOKENS: dict[str, str] = {
    "ink": INK, "ink-2": N[700], "ink-3": SECONDARY,
    "page": PAGE, "surface": SURFACE, "fill": N[100], "fill-2": N[150], "fill-soft": N[50],
    "line": N[200], "line-strong": N[300], "link": LINK,
    **{f"{k}-{v}": c for k, d in C.items() for v, c in d.items()},
}


def css_vars() -> str:
    return ":root {" + "; ".join(f"--{k}:{v}" for k, v in TOKENS.items()) + "}"


# text colour -> the fills it is drawn on in the workspace
TEXT_PAIRS: list[tuple[str, str, str]] = [
    ("body text", INK, SURFACE), ("body text on page", INK, PAGE),
    ("body text, selected row", INK, C["sel"]["subtle"]),
    ("secondary text", SECONDARY, SURFACE),
    ("secondary text, header", SECONDARY, N[100]),
    ("secondary text, selected row hatch", SECONDARY, C["sel"]["subtle2"]),
    ("secondary text, not-recorded hatch", SECONDARY, N[100]),
    ("link", LINK, SURFACE), ("link, header", LINK, N[100]), ("link, selected row", LINK, C["sel"]["subtle"]),
    ("link, compare chip", LINK, C["cmp"]["subtle"]),
    ("experimental", C["sel"]["base"], SURFACE),
    ("experimental chip", C["sel"]["base"], C["sel"]["faint"]),
    ("tested", C["sel"]["deep"], C["sel"]["faint"]),
    ("in-detail tag", C["sel"]["base"], C["sel"]["subtle"]),
    ("compare tag", C["cmp"]["base"], C["cmp"]["subtle"]),
    ("trace tag", C["trace"]["base"], C["trace"]["subtle"]),
    ("differs tag", C["diff"]["base"], C["diff"]["subtle"]),
    ("on hand", C["have"]["base"], SURFACE),
    ("on hand chip", C["have"]["base"], C["have"]["subtle"]),
    ("on hand, selected row", C["have"]["base"], C["sel"]["subtle"]),
    ("remove link in chip", C["diff"]["base"], SURFACE),
]
# UI marks that carry meaning alone need 3:1 against the surface
MARK_PAIRS: list[tuple[str, str, str]] = [
    ("compare pin bar", C["cmp"]["base"], C["sel"]["subtle"]),
    ("tab top, detail", C["sel"]["mid"], SURFACE), ("tab top, compare", C["cmp"]["base"], SURFACE),
    ("tab top, trace", C["trace"]["base"], SURFACE), ("tab top, circle", N[700], SURFACE),
]

if __name__ == "__main__":
    print(f"seed {SEED} = hsl({H:.0f}, {S:.0f}%, {L:.0f}%)")
    for k, v in TOKENS.items():
        print(f"  --{k:16} {v}")
    for name, fg, bg in TEXT_PAIRS + MARK_PAIRS:
        print(f"{contrast(fg, bg):5.2f}  {name}")
