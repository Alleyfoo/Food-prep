"""The product palette (design.css, graph.py): pantry, readable, in step.

The pantry palette was chosen in the R4.2 research
(docs/research/ux-layout-variants-r4-2/palette.md) and ported to the
product on 2026-11-24. scripts/gen_palette.py generates the ramps.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

from foodprep.ui import graph

CSS = (Path(graph.__file__).resolve().parent / "design.css").read_text(encoding="utf-8")
ROOT = CSS[CSS.index(":root {"):]
ROOT = ROOT[:ROOT.index("\n}")]
RAW = dict(re.findall(r"--([a-z0-9-]+):\s*([^;]+);", ROOT))


def tok(name: str) -> str:
    v = RAW[name].strip()
    while v.startswith("var(--"):
        v = RAW[v[6:-1]].strip()
    return v.upper()


def _lum(h: str) -> float:
    def ch(c: float) -> float:
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (ch(int(h[i:i + 2], 16) / 255) for i in (1, 3, 5))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a: str, b: str) -> float:
    la, lb = sorted((_lum(a), _lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def test_pantry_values_are_used_exactly():
    pantry = {"bg": "#F5F5EB", "surface": "#FFFDF5", "bg-2": "#E9ECD9", "ink": "#24291D",
              "neutral-200": "#E9ECD9", "neutral-700": "#515A43",
              "primary": "#5F692C", "primary-tint": "#E9EDC2",
              "ingredient-200": "#DCEBDF", "ingredient-700": "#29543E",
              "component-200": "#ECDFF0", "component-700": "#633F68",
              "filler-200": "#F1E5AE", "filler-700": "#674C14",
              "technique-700": "#355282", "destination-700": "#883046"}
    for k, v in pantry.items():
        assert tok(k) == v, k


# Text colour on the fill it is drawn on, as the rules in design.css pair them.
TEXT_PAIRS = [
    ("ink", "bg"), ("ink", "surface"), ("ink", "bg-2"), ("ink", "neutral-200"),
    ("neutral-700", "bg"), ("neutral-700", "surface"), ("neutral-700", "bg-2"),
    ("neutral-800", "neutral-100"), ("ink-3", "surface-2"), ("ink-3", "bg"),
    ("ink-4", "bg"), ("ink-4", "surface"), ("ink-4", "bg-2"),
    ("primary", "surface"), ("primary", "bg"),
    ("neutral-100", "primary"), ("neutral-100", "primary-deep"),
    ("ingredient-800", "ingredient-100"), ("ingredient-700", "ingredient-200"),
    ("filler-800", "filler-100"), ("filler-700", "filler-200"), ("filler-700", "filler-100"),
    ("component-800", "component-100"), ("component-700", "component-200"),
    ("technique-800", "technique-100"), ("destination-700", "destination-200"),
    ("destination-900", "destination-300"),
    ("green", "green-tint"), ("red", "red-tint"), ("amber", "amber-tint"),
    ("purple", "purple-tint"), ("blue", "surface-2"), ("positive", "surface"),
]


@pytest.mark.parametrize("fg,bg", TEXT_PAIRS)
def test_text_pairs_pass_aa(fg, bg):
    assert contrast(tok(fg), tok(bg)) >= 4.5, (fg, tok(fg), bg, tok(bg))


def test_graph_colours_follow_the_css_ramps():
    for kind in ("ingredient", "technique", "component", "filler", "destination"):
        assert graph._COLORS[kind] == tok(f"{kind}-500"), kind
        assert graph._EDGE_COLORS[kind] == tok(f"{kind}-600"), kind
    assert graph._BG == tok("bg") and graph._INK == tok("ink")
    assert graph._SECONDARY == tok("ink-4") and graph._LINE == tok("line-2")


def test_taste_circle_component_paints_the_page_colour():
    html = (Path(graph.__file__).resolve().parent / "taste_circle_component" / "index.html"
            ).read_text(encoding="utf-8")
    assert f"background: {tok('bg')};" in html


def test_circle_labels_and_outlines_read_on_the_page():
    C, bg = graph._CIRCLE, graph._BG
    for label in (graph._INK, C["prov_label"], C["gap_label"]):
        assert contrast(label, bg) >= 4.5, label
    for edge in (C["prov_edge"], C["open_edge"], C["focus_edge"], C["lock_edge"]):
        assert contrast(edge, bg) >= 3.0, edge
    assert contrast(C["prov_calm"], bg) >= 2.0      # provided stays visible while a fan is open
