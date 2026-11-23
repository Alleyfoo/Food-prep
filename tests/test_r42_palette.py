"""R4.2 colour worlds: one job per colour, readable in every world.

See docs/research/ux-layout-variants-r4-2/prototype/r42_palette.py and
palette.md. Method from dembrandt-skills (algorithmic-color-palette,
status-colors-and-errors, surface-separation, wcag-accessibility).
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
import r42_state as S  # noqa: E402
import r42_views as V  # noqa: E402

HEX = re.compile(r"#[0-9a-fA-F]{6}\b|#[0-9a-fA-F]{3}\b")
NEW = ["white", "cool"]
TEXT = [(w, *pair) for w in P.WORLDS for pair in P.text_pairs(w)]
MARKS = [(w, *pair) for w in P.WORLDS for pair in P.mark_pairs(w)]


@pytest.mark.parametrize("world,name,fg,bg", TEXT)
def test_every_text_pair_passes_aa(world, name, fg, bg):
    assert P.contrast(fg, bg) >= 4.5, (world, name)


@pytest.mark.parametrize("world,name,fg,bg", MARKS)
def test_marks_that_carry_meaning_pass_3_to_1(world, name, fg, bg):
    assert P.contrast(fg, bg) >= 3.0, (world, name)


@pytest.mark.parametrize("world", P.WORLDS)
def test_no_pure_black_text(world):
    assert P.world(world)["ink"] != "#000000"


@pytest.mark.parametrize("world", NEW)
def test_structure_carries_no_food_tint(world):
    """The redesign's point: page, fills, lines and text are cool neutrals,
    never the peach / amber seed hue."""
    w = P.world(world)
    peach_hue = P.hex_to_hsl(P.SEED)[0]
    for key in ("ink", "ink2", "secondary", "fill", "fill2", "fill_soft", "line", "line_strong"):
        h, s, _l = P.hex_to_hsl(w[key])
        assert abs(h - peach_hue) > 90, (world, key)
        assert s < 50, (world, key)                       # structure stays quiet


@pytest.mark.parametrize("world", NEW)
def test_one_job_per_hue(world):
    """selection, compare, trace and on hand each have their own hue, far
    enough apart to tell apart; hypotheses carry no hue at all."""
    t = P.tokens(world)
    hues = {job: P.hex_to_hsl(t[f"{job}-base"])[0] for job in ("sel", "cmp", "trace", "have")}
    names = list(hues)
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            d = abs(hues[a] - hues[b]) % 360
            assert min(d, 360 - d) >= 40, (world, a, b)
    for k in ("hyp-text", "hyp-deep", "hyp-border", "hyp-line"):
        assert P.hex_to_hsl(t[k])[1] < 35, (world, k)        # no hue: shape carries it
    assert t["diff-base"] == t["cmp-base"]                   # differs belongs to compare
    assert t["link"] == t["sel-base"]                        # links: "where you act"


@pytest.mark.parametrize("world", NEW)
def test_selected_row_stands_out_from_the_page(world):
    t = P.tokens(world)
    assert P.contrast(t["sel-subtle"], t["page"]) >= 1.15


def test_peach_reference_is_unchanged_and_has_no_grey():
    t = P.tokens("peach")
    assert t["sel-base"] == "#6f4102" and t["page"] == "#f9f3ec"
    for name, col in t.items():
        assert P.hex_to_hsl(col)[1] >= P.NEUTRAL_MIN_SAT, name


def test_workspace_css_uses_only_tokens():
    body = V.CSS.split("</style>")[0]
    assert not HEX.findall(body)
    assert not HEX.findall(C.CSS)
    assert not re.search(r"rgba\(", body + C.CSS)          # no translucent tints
    used = set(re.findall(r"var\(--([a-z0-9-]+)\)", body + C.CSS))
    for world in P.WORLDS:
        assert used and used <= set(P.tokens(world)), (world, used - set(P.tokens(world)))


@pytest.mark.parametrize("world", P.WORLDS)
def test_css_carries_the_worlds_tokens(world):
    css = V.css(world)
    assert P.css_vars(world) in css and css.endswith(V.CSS)


def test_the_trace_graph_reads_the_world():
    src = (R42 / "r42_views.py").read_text(encoding="utf-8")
    dot_src = src[src.index("def trace_dot"):src.index("def trace_head_html")]
    assert not HEX.findall(dot_src)
    for tok in re.findall(r"@([a-z0-9-]+)@", dot_src):
        assert tok in P.TOKENS, tok


def test_the_colour_world_is_a_url_condition_that_survives_links():
    st = S.parse({"ingredient": "broccoli", "pal": "cool"})
    assert st["pal"] == "cool" and S.to_params(st)["pal"] == "cool"
    assert "pal" not in S.to_params(S.parse({"ingredient": "broccoli"}))     # white is the default
    assert S.parse({"ingredient": "broccoli", "pal": "neon"})["pal"] == "white"
    assert "pal=cool" in S.href(st, rec="x")


def test_circle_tab_is_not_the_on_hand_green():
    assert "var(--have" not in C.CSS.split(".k-circle")[1].split("}")[0]
