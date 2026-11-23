"""R4.2 layout variants: one workspace, switchable encodings.

These tests make the variants a fair comparison: every variant carries the
same facts per row, only the encoding differs; the facilitator's condition
survives every link; the default condition is R4.1 unchanged. They say
nothing about which variant people read better.
"""
from __future__ import annotations

import re
import shutil
import sqlite3
import sys
from html import unescape
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
R4 = ROOT / "docs/research/ux-integrated-r4/prototype"
R41 = ROOT / "docs/research/ux-integrated-r4-1/prototype"
R42 = ROOT / "docs/research/ux-layout-variants-r4-2/prototype"
for p in (R4, R41, R42):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from foodprep import loader  # noqa: E402
import r4_model as M  # noqa: E402
import r41_state as S41  # noqa: E402
import r41_views as V41  # noqa: E402
import r42_state as S  # noqa: E402
import r42_views as V  # noqa: E402

GLYPHS = set("●◐○◇✓≠☐☑⇄")
DATASETS = [("broccoli", ["yogurt", "lemon", "garlic"], "roasted_broccoli_component"),
            ("cabbage", ["lemon"], "roasted_cabbage_component"),
            ("potato", [], "smashed_roasted_potato_component")]


@pytest.fixture(scope="module")
def conn(tmp_path_factory):
    tmp = tmp_path_factory.mktemp("r42") / "tastings.yaml"
    shutil.copy(ROOT / "src/foodprep/data/tastings.yaml", tmp)
    c = sqlite3.connect(":memory:")
    c.row_factory = sqlite3.Row
    loader.build(c, tastings_path=tmp)
    return c


def _text(html: str) -> str:
    return re.sub(r"\s+", " ", unescape(re.sub(r"<[^>]+>", " ", html)))


def _text_and_titles(html: str) -> str:
    """Visible text plus tooltips: variant A keeps names in tooltips, as R4 did."""
    return _text(html) + " " + " ".join(unescape(t) for t in re.findall(r'title="([^"]*)"', html))


def _st(mod, ing, have=(), **kw):
    st = mod.parse({"ingredient": ing, "have": ",".join(have)})
    st.update(kw)
    return st


def _rows(html: str) -> list[str]:
    return re.findall(r"<tr class=\"[^\"]*\">.*?</tr>", html.split("<tbody>")[1], re.S)


@pytest.mark.parametrize("ing,have,rec", DATASETS)
def test_default_condition_is_r41_unchanged(conn, ing, have, rec):
    m = M.build(conn, ing, have)
    for cols in ("summary", "matrix", "evidence", "sensory"):
        assert _text(V.overview_html(m, _st(S, ing, have, cols=cols))) == \
            _text(V41.overview_html(m, _st(S41, ing, have, cols=cols))), cols
    assert _text(V.detail_html(m, _st(S, ing, have, rec=rec), rec)) == \
        _text(V41.detail_html(m, _st(S41, ing, have, rec=rec), rec))


@pytest.mark.parametrize("ing,have,rec", DATASETS)
def test_every_variant_carries_the_same_facts_per_row(conn, ing, have, rec):
    m = M.build(conn, ing, have)
    rows = {ov: _rows(V.overview_html(m, _st(S, ing, have, ov=ov))) for ov in "abc"}
    assert len(rows["a"]) == len(rows["b"]) == len(rows["c"]) == len(m["states"])
    for i, s in enumerate(m["states"]):
        comp = s["component"]
        facts = []
        for n in M.of(m, comp, "need"):
            if n["coverage"] == "not recorded":
                facts.append(n["role"])                      # the uncovered role is named
        for p in M.of(m, comp, "pairing"):
            if p["knowledge"] == "curated" and p["availability"] == "on hand":
                facts.append(M.pretty(p["ingredient"]))     # what is on hand is named
            if p["knowledge"] == "experimental":
                facts.append(M.pretty(p["ingredient"]))
        for idea in M.of(m, comp, "idea"):
            if idea["testing"]["status"] == "tested":
                facts.append(M.pretty(idea["ingredient"]))
        for r in M.of(m, comp, "route_fit"):
            facts.append(r["attrs"]["name"])
        for ov in "abc":
            txt = _text_and_titles(rows[ov][i])
            for f in facts:
                assert f in txt, (ov, comp, f)


@pytest.mark.parametrize("ing,have,rec", DATASETS)
def test_only_variant_a_uses_coded_glyphs_and_a_legend(conn, ing, have, rec):
    m = M.build(conn, ing, have)
    a = V.overview_html(m, _st(S, ing, have, ov="a"))
    assert set(_text(a)) & GLYPHS and 'class="legendrow"' in a
    for ov in "bc":
        h = V.overview_html(m, _st(S, ing, have, ov=ov))
        assert not set(_text(h)) & GLYPHS and 'class="legendrow"' not in h


def test_variant_c_names_each_needed_role_once_with_its_status(conn):
    m = M.build(conn, "broccoli", ["yogurt", "lemon", "garlic"])
    cell = V.roles_named(m, "roasted_broccoli_component")
    roles = [n["role"] for n in M.of(m, "roasted_broccoli_component", "need")]
    assert cell.count('class="rc') == len(roles)
    assert "acid: lemon" in _text(cell) and "rc-have" in cell
    p = M.build(conn, "potato", [])
    pc = V.roles_named(p, "smashed_roasted_potato_component")
    assert pc.count("rc-nr") == 3 and "acid: not recorded" in _text(pc)
    ov = V.overview_html(p, _st(S, "potato", ov="c"))
    assert "no curated pairing for acid" not in ov         # not repeated in Not recorded


@pytest.mark.parametrize("ov,sheet", [("a", "dense"), ("c", "full"), ("b", "dense")])
def test_the_condition_survives_every_link_and_reset(conn, ov, sheet):
    m = M.build(conn, "broccoli", ["lemon"])
    rec = "roasted_broccoli_component"
    st = _st(S, "broccoli", ["lemon"], ov=ov, sheet=sheet, rec=rec,
             cmp=[rec, "steamed_broccoli_component"], trace="ingredient:lemon")
    html = (V.overview_html(m, st) + V.detail_html(m, st, rec) + V.compare_html(m, st)
            + V.trace_table_html(m, st) + V.context_bar(m, st) + V.tabs_html(m, st, "detail"))
    hrefs = [unescape(h) for h in re.findall(r'href="(\?[^"]*)"', html)]
    assert hrefs
    for h in hrefs:
        nxt = S.parse(dict(x.split("=", 1) for x in h[1:].split("&") if "=" in x))
        assert (nxt["ov"], nxt["sheet"]) == (ov, sheet), h


def test_unknown_conditions_fall_back_to_r41(conn):
    st = S.parse({"ingredient": "broccoli", "ov": "z", "sheet": "tiny"})
    assert (st["ov"], st["sheet"]) == ("b", "full")
    assert "ov" not in S.to_params(st) and "sheet" not in S.to_params(st)


@pytest.mark.parametrize("ing,have,rec", DATASETS)
def test_dense_sheet_keeps_every_fact_and_link(conn, ing, have, rec):
    m = M.build(conn, ing, have)
    full = V.detail_html(m, _st(S, ing, have, rec=rec), rec)
    dense = V.detail_html(m, _st(S, ing, have, rec=rec, sheet="dense"), rec)
    links = lambda h: sorted(x.replace("&amp;sheet=dense", "")  # noqa: E731
                             for x in re.findall(r'href="([^"]*)"', h))
    assert links(full) == links(dense)
    for n in range(1, 9):
        assert f'id="{V._anchor(rec, n)}"' in dense
    ft = _text(full)
    for r in M.of(m, rec, "route_element"):
        assert r["attrs"]["contribution"] in _text(dense)
    for x in ("Why it fits", "Recorded tasting results", "Not on hand (your ingredients)",
              "Not recorded in the database (knowledge)"):
        assert (x in ft) == (x in _text(dense)), x
    assert 'class="r4 dense"' in dense and "dl4" in dense
