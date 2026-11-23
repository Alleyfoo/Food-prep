"""R4.2 palette: derived from one seed, every text pair passes WCAG AA.

Method from dembrandt-skills (algorithmic-color-palette, wcag-accessibility,
surface-separation); see docs/research/ux-layout-variants-r4-2/prototype/r42_palette.py.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
R4 = ROOT / "docs/research/ux-integrated-r4/prototype"
R42 = ROOT / "docs/research/ux-layout-variants-r4-2/prototype"
for p in (R4, R42):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import r42_circle as C  # noqa: E402
import r42_palette as P  # noqa: E402
import r42_views as V  # noqa: E402

HEX = re.compile(r"#[0-9a-fA-F]{6}\b|#[0-9a-fA-F]{3}\b")


@pytest.mark.parametrize("name,fg,bg", P.TEXT_PAIRS)
def test_every_text_pair_passes_aa(name, fg, bg):
    assert P.contrast(fg, bg) >= 4.5, name


@pytest.mark.parametrize("name,fg,bg", P.MARK_PAIRS)
def test_marks_that_carry_meaning_pass_3_to_1(name, fg, bg):
    assert P.contrast(fg, bg) >= 3.0, name


def test_no_pure_black_on_pure_white():
    assert P.INK != "#000000" and P.SURFACE != "#ffffff" and P.PAGE != "#ffffff"


def test_no_grey_every_neutral_is_a_tone_of_the_seed():
    """User request: no grey. Every neutral, the page, the surface and the
    secondary text carry the seed hue at a saturation that does not read grey."""
    tones = [P.N[step] for step, _s, _l in P.NEUTRAL_STEPS] + [P.PAGE, P.SURFACE, P.SECONDARY, P.INK]
    for t in tones:
        h, s, _l = P.hex_to_hsl(t)
        assert s >= P.NEUTRAL_MIN_SAT, t
        assert abs(h - P.H) < 8, t


def test_no_grey_left_in_the_workspace_tokens():
    for name, t in P.TOKENS.items():
        _h, s, _l = P.hex_to_hsl(t)
        assert s >= P.NEUTRAL_MIN_SAT, name


def test_every_concept_takes_the_seeds_weight():
    for k, d in P.C.items():
        _h, s, l = P.hex_to_hsl(d["base"])
        assert abs(s - P.S) < 2 and abs(l - P.L) < 2, k


def test_workspace_css_uses_only_tokens():
    body = V.CSS.split("</style>")[0]
    body = body.replace(P.css_vars(), "")
    assert not HEX.findall(body)
    assert not HEX.findall(C.CSS)
    assert not re.search(r"rgba\(", body + C.CSS)     # no translucent tints
    used = set(re.findall(r"var\(--([a-z0-9-]+)\)", body + C.CSS))
    assert used and used <= set(P.TOKENS)


def test_the_trace_graph_reads_the_palette():
    src = (R42 / "r42_views.py").read_text(encoding="utf-8")
    dot_src = src[src.index("def trace_dot"):src.index("def trace_head_html")]
    assert not HEX.findall(dot_src)
    for tok in re.findall(r"@([a-z0-9-]+)@", dot_src):
        assert tok in P.TOKENS, tok


def test_circle_tab_is_not_the_on_hand_green():
    assert "var(--have" not in C.CSS.split(".k-circle")[1].split("}")[0]
