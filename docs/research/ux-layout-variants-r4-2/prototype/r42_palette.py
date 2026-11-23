"""Workspace colour worlds: one job per colour.

Method: dembrandt-skills `algorithmic-color-palette`, `status-colors-and-errors`,
`surface-separation` and `wcag-accessibility`
(https://github.com/dembrandt/dembrandt-skills), read as guidance.

Why worlds. The first palette took the product's food colours (design.css
ramps named ingredient, filler, component ...) and seeded everything from
the filler amber. On review (2026-11-23) that was the wrong foundation:
peach did six jobs at once (page tint, every neutral, the selected row,
hypotheses, the idea box, open circle dimensions) and cast one tint over
the whole screen. The redesign assigns colours by JOB, not by food:

  structure    ink, lines, fills         neutral; carries no meaning
  selection    the record in detail      blue  (also links and focus:
                                                one job, "where you act")
  compare      pinned records, differs   violet
  trace        the traced entity         magenta
  on hand      what is in your kitchen   green
  hypothesis   experimental, tasted      no hue: dashed / solid outline,
                                         italic / bold. Shape, not colour
  gap          not recorded              neutral hatch

Worlds differ only in the structure layer, so they can be compared on
identical screens (URL key `pal`):

  peach   the previous palette, kept as the reference
  white   white page and surfaces; structure by thin cool lines; colour
          appears only where it means something
  cool    a faint blue-white page and fills, tied to the selection blue
  pantry  (default) the user's proposal (2026-11-23): food references again, but one
          job per food - oat page, yogurt panels, pale sage filters, green
          olive selection, parsley on hand, red cabbage locked, mustard
          seed open dimensions, muted sage gaps. Jobs the proposal left
          open take the same family: blueberry compare, beetroot trace,
          olive links, sage lines and secondary text, no hue for hypotheses

Every world: every text pair >= 4.5:1, every meaningful mark >= 3:1
(tests/test_r42_palette.py), no translucent tints.
"""
from __future__ import annotations

import colorsys
from functools import lru_cache

SEED = "#6F4102"          # the product's --filler-700; seed of the peach world only
WORLDS = ("peach", "white", "cool", "pantry")
DEFAULT_WORLD = "pantry"     # chosen by the user, 2026-11-23
NEUTRAL_MIN_SAT = 20      # peach world: below this a tone reads as grey


# ---------------------------------------------------------------- colour maths

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


def passing(hue: float, sat: float, bgs: list[str], start: float, target: float = 4.5) -> str:
    """Lightest tone of (hue, sat) at or below *start* lightness that reaches
    *target* on every fill in *bgs*."""
    l = start
    while min(contrast(hsl(hue, sat, l), bg) for bg in bgs) < target and l > 0:
        l -= 1
    return hsl(hue, sat, l)


def ramp(hue: float, s: float, l: float, *, fill_s: float, fill_l: float = 92) -> dict[str, str]:
    """base (text), deep (emphasis), mid and border (outlines), subtle,
    subtle2 and faint (fills, from strongest to calmest)."""
    return {"base": hsl(hue, s, l), "deep": hsl(hue, s, l - 7),
            "mid": hsl(hue, s * 0.8, l + 16), "border": hsl(hue, s * 0.7, l + 36),
            "subtle": hsl(hue, fill_s, fill_l), "subtle2": hsl(hue, fill_s * 0.85, fill_l - 6),
            "faint": hsl(hue, fill_s * 0.8, 97.5)}


# ---------------------------------------------------------------- the worlds

def _peach() -> dict:
    """The previous palette, unchanged: every neutral a tone of the seed."""
    H, S, L = hex_to_hsl(SEED)
    steps = [(900, 35, 10), (700, 28, 27), (600, 26, 36), (500, 24, 46), (300, 28, 68),
             (200, 32, 80), (150, 36, 86), (100, 42, 91), (50, 50, 95)]
    N = {k: hsl(H, s, l) for k, s, l in steps}

    def concept(hue: float) -> dict[str, str]:
        return {"base": hsl(hue, S, L), "deep": hsl(hue, S, L - 6),
                "mid": hsl(hue, S * 0.75, L + 18), "border": hsl(hue, S * 0.6, L + 40),
                "subtle": hsl(hue, S * 0.8, 88), "subtle2": hsl(hue, S * 0.65, 82),
                "faint": hsl(hue, S * 0.4, 97)}
    C = {k: concept(h) for k, h in {"sel": H, "cmp": 215, "trace": 268, "have": 145, "diff": 4}.items()}
    secondary = passing(H, 26, [C["sel"]["subtle2"], N[100]], 40)
    hyp = {"text": C["sel"]["base"], "deep": C["sel"]["deep"], "border": C["sel"]["border"],
           "line": C["sel"]["mid"], "fill": C["sel"]["faint"]}
    return {"name": "peach", "hue": H, "ink": N[900], "ink2": N[700], "secondary": secondary,
            "page": N[50], "surface": hsl(H, 70, 97.5), "fill": N[100], "fill2": N[150],
            "fill_soft": N[50], "line": N[200], "line_strong": N[300], "link": hsl(215, 75, 36),
            "C": C, "hyp": hyp, "note": {"fill": C["sel"]["faint"], "line": C["sel"]["border"]},
            "node": {"state": C["cmp"]["faint"], "route": C["have"]["faint"],
                     "source": C["sel"]["faint"], "pairing": C["sel"]["faint"]},
            "circle_tab": N[700], "primary": SEED, "steps": steps, "N": N}


def _jobs(name: str, *, page: str, fill: str, fill2: str, fill_soft: str,
          line: str, line_strong: str) -> dict:
    """A role-based world: neutral structure (hue 220, cool) plus one hue per job."""
    nh = 220                                            # structure hue: cool, not food
    ink, ink2 = hsl(nh, 28, 12), hsl(nh, 18, 30)
    surface = "#ffffff"
    C = {"sel": ramp(218, 72, 40, fill_s=85),
         "cmp": ramp(265, 55, 42, fill_s=70),
         "trace": ramp(322, 62, 38, fill_s=72),
         "have": ramp(150, 70, 27, fill_s=55)}
    C["diff"] = C["cmp"]                                # differs is part of comparing
    secondary = passing(nh, 16, [fill, fill2, C["sel"]["subtle2"], C["sel"]["subtle"]], 46)
    hyp = {"text": ink2, "deep": ink, "border": secondary, "line": ink2, "fill": surface}
    return {"name": name, "hue": nh, "ink": ink, "ink2": ink2, "secondary": secondary,
            "page": page, "surface": surface, "fill": fill, "fill2": fill2, "fill_soft": fill_soft,
            "line": line, "line_strong": line_strong, "link": C["sel"]["base"], "C": C, "hyp": hyp,
            "note": {"fill": fill_soft, "line": line},
            "node": {"state": surface, "route": surface, "source": fill_soft, "pairing": surface},
            "circle_tab": ink2, "primary": C["sel"]["base"]}


def _extras(w: dict) -> dict:
    """Panel, gap, selected-row edge and circle roles, derived for worlds
    that do not set them (the jobs worlds and peach)."""
    C = w["C"]
    w.setdefault("panel", w["page"])
    w.setdefault("gap", {"fill": w["fill_soft"], "fill2": w["fill"], "text": w["secondary"]})
    w.setdefault("sel_edge", C["sel"]["subtle"])        # no edge: the fill carries it
    w.setdefault("circle", {
        "canvas": w["page"],
        "open-fill": w["surface"], "open-edge": w["line_strong"], "open-label": w["ink2"],
        "prov-fill": w["fill2"], "prov-edge": w["secondary"], "prov-label": w["secondary"],
        "lock-fill": C["sel"]["subtle"], "lock-edge": C["sel"]["base"], "lock-calm": C["sel"]["border"],
        "lock-label": C["sel"]["deep"],
        "exp-fill": C["sel"]["base"], "exp-edge": C["sel"]["deep"], "exp-label": C["sel"]["deep"],
    })
    return w


def _pantry() -> dict:
    """The user's proposal, exactly where it gives a colour; the rest from
    the same family (see the module docstring)."""
    ink, ink2 = "#24291D", "#515A43"
    page, panel, fill = "#F5F5EB", "#FFFDF5", "#E9ECD9"
    fill2, line = hsl(70, 24, 84), hsl(70, 20, 80)
    sel = ramp(66, 41, 29, fill_s=54, fill_l=85)
    sel.update({"subtle": "#E9EDC2", "base": "#5F692C", "subtle2": hsl(66, 45, 79)})
    have = ramp(150, 34, 25, fill_s=27, fill_l=89)
    have.update({"subtle": "#DCEBDF", "base": "#29543E"})
    C = {"sel": sel, "have": have,
         "cmp": ramp(218, 42, 36, fill_s=40, fill_l=91),       # blueberry
         "trace": ramp(345, 48, 36, fill_s=42, fill_l=91)}     # beetroot
    C["diff"] = C["cmp"]
    secondary = passing(75, 14, [fill, fill2, sel["subtle2"], sel["subtle"], "#EBEDE4", hsl(72, 16, 87)], 46)
    gap = {"fill": "#EBEDE4", "fill2": hsl(72, 16, 87), "text": "#535C4A"}
    return {"name": "pantry", "hue": 70, "ink": ink, "ink2": ink2, "secondary": secondary,
            "page": page, "surface": panel, "panel": panel, "fill": fill, "fill2": fill2,
            "fill_soft": page, "line": line, "line_strong": hsl(72, 14, 50),
            "link": sel["base"], "C": C,
            "hyp": {"text": ink2, "deep": ink, "border": secondary, "line": ink2, "fill": panel},
            "note": {"fill": page, "line": line},
            "node": {"state": panel, "route": panel, "source": fill, "pairing": panel},
            "circle_tab": ink2, "primary": sel["base"], "gap": gap, "sel_edge": "#5F692C",
            "circle": {"canvas": panel,
                       "open-fill": "#F1E5AE", "open-edge": "#674C14", "open-label": "#674C14",
                       "prov-fill": fill, "prov-edge": ink2, "prov-label": ink2,
                       "lock-fill": "#ECDFF0", "lock-edge": "#633F68", "lock-calm": hsl(288, 22, 70),
                       "lock-label": "#633F68",
                       "exp-fill": "#674C14", "exp-edge": hsl(40, 67, 16), "exp-label": "#674C14"}}


def _white() -> dict:
    return _jobs("white", page="#ffffff", fill=hsl(220, 22, 96.5), fill2=hsl(220, 18, 92),
                 fill_soft=hsl(220, 25, 98), line=hsl(220, 16, 87), line_strong=hsl(220, 12, 62))


def _cool() -> dict:
    return _jobs("cool", page=hsl(218, 45, 97), fill=hsl(218, 38, 94), fill2=hsl(218, 30, 89),
                 fill_soft=hsl(218, 45, 97.5), line=hsl(218, 26, 84), line_strong=hsl(218, 18, 60))


@lru_cache(maxsize=None)
def world(name: str = DEFAULT_WORLD) -> dict:
    return _extras({"peach": _peach, "white": _white, "cool": _cool,
                    "pantry": _pantry}.get(name, _pantry)())


@lru_cache(maxsize=None)
def tokens(name: str = DEFAULT_WORLD) -> dict[str, str]:
    w = world(name)
    t = {"ink": w["ink"], "ink-2": w["ink2"], "ink-3": w["secondary"], "page": w["page"],
         "surface": w["surface"], "fill": w["fill"], "fill-2": w["fill2"], "fill-soft": w["fill_soft"],
         "line": w["line"], "line-strong": w["line_strong"], "link": w["link"],
         "circle-tab": w["circle_tab"], "panel": w["panel"], "sel-edge": w["sel_edge"]}
    for k, d in w["C"].items():
        t.update({f"{k}-{v}": c for v, c in d.items()})
    t.update({f"hyp-{k}": v for k, v in w["hyp"].items()})
    t.update({f"note-{k}": v for k, v in w["note"].items()})
    t.update({f"node-{k}": v for k, v in w["node"].items()})
    t.update({f"gap-{k}": v for k, v in w["gap"].items()})
    t.update({f"circle-{k}": v for k, v in w["circle"].items()})
    return t


def css_vars(name: str = DEFAULT_WORLD) -> str:
    return ":root {" + "; ".join(f"--{k}:{v}" for k, v in tokens(name).items()) + "}"


def text_pairs(name: str = DEFAULT_WORLD) -> list[tuple[str, str, str]]:
    """Text colour -> the fills it is drawn on in the workspace."""
    t = tokens(name)
    pairs = [("body text", "ink", "surface"), ("body text on page", "ink", "page"),
             ("body text, selected row", "ink", "sel-subtle"),
             ("secondary text", "ink-3", "surface"), ("secondary text, header", "ink-3", "fill"),
             ("secondary text, selected row hatch", "ink-3", "sel-subtle2"),
             ("secondary text, not-recorded hatch", "ink-3", "fill-2"),
             ("link", "link", "surface"), ("link, header", "link", "fill"),
             ("link, selected row", "link", "sel-subtle"), ("link, compare chip", "link", "cmp-subtle"),
             ("experimental", "hyp-text", "surface"), ("experimental chip", "hyp-text", "hyp-fill"),
             ("tested", "hyp-deep", "hyp-fill"), ("experimental, selected row", "hyp-text", "sel-subtle"),
             ("in-detail tag", "sel-base", "sel-subtle"), ("compare tag", "cmp-base", "cmp-subtle"),
             ("trace tag", "trace-base", "trace-subtle"), ("differs tag", "diff-base", "diff-subtle"),
             ("on hand", "have-base", "surface"), ("on hand chip", "have-base", "have-subtle"),
             ("on hand, selected row", "have-base", "sel-subtle"),
             ("remove link in chip", "diff-base", "surface"), ("note banner", "ink", "note-fill"),
             ("not recorded", "gap-text", "gap-fill"), ("not recorded, hatch", "gap-text", "gap-fill2"),
             ("body text on panel", "ink", "panel"), ("secondary text on panel", "ink-3", "panel"),
             ("circle label, open", "circle-open-label", "circle-canvas"),
             ("circle label, provided", "circle-prov-label", "circle-canvas"),
             ("circle label, locked", "circle-lock-label", "circle-canvas"),
             ("circle label, expanded", "circle-exp-label", "circle-canvas")]
    return [(n, t[f], t[b]) for n, f, b in pairs]


def mark_pairs(name: str = DEFAULT_WORLD) -> list[tuple[str, str, str]]:
    """UI marks that carry meaning alone need 3:1 against what is around them."""
    t = tokens(name)
    pairs = [("compare pin bar", "cmp-base", "sel-subtle"), ("tab top, detail", "sel-mid", "surface"),
             ("tab top, compare", "cmp-base", "surface"), ("tab top, trace", "trace-base", "surface"),
             ("tab top, circle", "circle-tab", "surface")]
    if name != "peach":          # the reference world is kept as it was
        pairs.append(("experimental outline", "hyp-border", "surface"))
    return [(n, t[f], t[b]) for n, f, b in pairs]


def theme(name: str = DEFAULT_WORLD) -> dict[str, str]:
    """Streamlit's own theme for this world (run.py)."""
    w = world(name)
    return {"theme.base": "light", "theme.primaryColor": w["primary"],
            "theme.backgroundColor": w["page"], "theme.secondaryBackgroundColor": w["fill"],
            "theme.textColor": w["ink"]}


# -- names the rest of the prototype reads: the default world ------------------
_W = world(DEFAULT_WORLD)
TOKENS = tokens(DEFAULT_WORLD)
INK, PAGE, SURFACE, SECONDARY = _W["ink"], _W["page"], _W["surface"], _W["secondary"]

if __name__ == "__main__":
    import sys
    for name in sys.argv[1:] or WORLDS:
        print(f"== {name}")
        for k, v in tokens(name).items():
            print(f"  --{k:16} {v}")
        for n, fg, bg in text_pairs(name) + mark_pairs(name):
            print(f"{contrast(fg, bg):5.2f}  {n}")
