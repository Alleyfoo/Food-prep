"""R4.2: the product's Taste Circle embedded as a workspace pane.

The circle is the product's own component and graph data; these tests cover
the glue: it builds around the record in detail, its dish is URL-held, clicks
follow the product's rules, and the read-out states every dimension in words.
"""
from __future__ import annotations

import random
import re
import shutil
import sqlite3
import sys
from html import unescape
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
R4 = ROOT / "docs/research/ux-integrated-r4/prototype"
R42 = ROOT / "docs/research/ux-layout-variants-r4-2/prototype"
for p in (R4, R42):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from foodprep import loader, query  # noqa: E402
import r4_model as M  # noqa: E402
import r42_circle as C  # noqa: E402
import r42_state as S  # noqa: E402
import r42_views as V  # noqa: E402

REC = "roasted_broccoli_component"


@pytest.fixture(scope="module")
def conn(tmp_path_factory):
    tmp = tmp_path_factory.mktemp("r42c") / "tastings.yaml"
    shutil.copy(ROOT / "src/foodprep/data/tastings.yaml", tmp)
    c = sqlite3.connect(":memory:")
    c.row_factory = sqlite3.Row
    loader.build(c, tastings_path=tmp)
    return c


def _st(**kw):
    st = S.parse({"ingredient": "broccoli", "have": "yogurt,lemon,garlic"})
    st.update(rec=REC, pane="circle", tcb=REC)
    st.update(kw)
    return st


def _text(html: str) -> str:
    return re.sub(r"\s+", " ", unescape(re.sub(r"<[^>]+>", " ", html)))


def _parse_href(h: str) -> dict:
    from urllib.parse import parse_qsl
    return S.parse(dict(parse_qsl(unescape(h)[1:])))


def test_the_circle_is_a_fourth_pane_named_after_the_record(conn):
    m = M.build(conn, "broccoli", ["lemon"])
    tabs = V.tabs_html(m, _st(pane="detail"), "detail")
    assert "Taste circle: roasted broccoli" in _text(tabs)
    href = re.search(r'href="([^"]*)"[^>]*>Taste circle', tabs).group(1)
    assert _parse_href(href)["pane"] == "circle"


def test_clicks_follow_the_product_rules(conn):
    st = _st()
    st.update(C.apply_click(conn, st, "dim:sour"))                  # fan out
    assert st["tcx"] == "sour" and st["tc"] == []
    st.update(C.apply_click(conn, st, "filler:sour:lemon"))         # lock in
    assert C.selections(st) == {"sour": "lemon"} and st["tcx"] == ""
    st.update(C.apply_click(conn, st, "dim:salty"))
    st.update(C.apply_click(conn, st, None))                        # blank canvas closes
    assert st["tcx"] == "" and C.selections(st) == {"sour": "lemon"}
    st.update(C.apply_click(conn, st, "dim:sour"))                  # locked: unlock
    assert C.selections(st) == {}


def test_invalid_or_reused_fillers_are_ignored(conn):
    st = _st(tc=["sour:lemon"])
    assert C.selections({**st, **C.apply_click(conn, st, "filler:sour:not_an_ingredient")}) \
        == {"sour": "lemon"}
    aromatic = {f["filler"] for f in query.taste_circle_fillers(conn, REC, {"sour"})["aromatic"]}
    assert "lemon" not in aromatic or C.selections(
        {**st, **C.apply_click(conn, st, "filler:aromatic:lemon")}) == {"sour": "lemon"}
    # provided dimensions never open
    assert C.apply_click(conn, _st(), "dim:umami")["tcx"] == ""


def test_the_more_node_pages_the_fan(conn):
    st = _st(tcx="sour")
    assert C.apply_click(conn, st, "filler:sour:__more")["tcp"] == 1


def test_the_dish_is_url_held_and_round_trips(conn):
    st = _st(tc=["sour:lemon", "pungent:garlic"], tcx="salty", tcp=1)
    back = S.parse(S.to_params(st))
    assert (back["tc"], back["tcx"], back["tcp"], back["tcb"]) == \
        (["sour:lemon", "pungent:garlic"], "salty", 1, REC)
    assert list(C.selections(back)) == ["sour", "pungent"]      # order kept


def test_a_new_subject_starts_a_fresh_circle(conn):
    m = M.build(conn, "broccoli", [])
    same = S.reconcile(_st(tc=["sour:lemon"]), m)
    assert same["tc"] == ["sour:lemon"]
    moved = S.reconcile(_st(tc=["sour:lemon"], tcx="salty", rec="steamed_broccoli_component"), m)
    assert (moved["tc"], moved["tcx"], moved["tcb"]) == ([], "", "")


def test_the_readout_states_every_dimension_in_words(conn):
    st = _st(tc=["sour:lemon"])
    txt = _text(C.readout_html(conn, st, rng=random.Random(1)))
    for name in C.NAMES.values():
        assert txt.count(name) >= 1, name
    assert "Sour: lemon" in txt                                   # locked
    assert "Sweet, Umami, Nutty/Toasted" in txt                   # provided, in circle order
    assert "on hand: garlic" in txt                               # on-hand fillers named


def test_the_graph_is_the_products_own(conn):
    data = C.graph_data(conn, _st(tc=["sour:lemon"], tcx="salty"))
    ids = {n["id"] for n in data["nodes"]}
    assert {f"dim:{d}" for d in C.ORDER} <= ids
    assert f"comp:{REC}" in ids
    assert any(i.startswith("filler:salty:") for i in ids)


def test_random_fill_and_remove_links_keep_the_condition(conn):
    st = _st(tc=["sour:lemon"], ov="a", sheet="dense")
    html = C.readout_html(conn, st, rng=random.Random(3)) + C.dish_html(conn, st)
    hrefs = re.findall(r'href="(\?[^"]*)"', html)
    assert hrefs
    for h in hrefs:
        nxt = _parse_href(h)
        assert (nxt["ov"], nxt["sheet"], nxt["pane"], nxt["tcb"]) == ("a", "dense", "circle", REC)
    filled = C.selections(_parse_href(hrefs[0]))
    assert filled["sour"] == "lemon" and len(filled) > 1
    for d, f in filled.items():
        if d != "sour":
            locked = set(filled) - {d}
            assert f in {x["filler"] for x in query.taste_circle_fillers(conn, REC, locked)[d]}
    removed = [_parse_href(h) for h in hrefs if "tc=" not in unescape(h)]
    assert removed, "remove link clears the only locked filler"


def test_a_record_without_a_profile_says_why(conn):
    assert not C.can_anchor(conn, "raw_broccoli_component")
    txt = _text(C.unavailable_html(conn, _st(rec="raw_broccoli_component")))
    assert "no sensory profile" in txt
    assert "Open a prepared ingredient" in _text(C.unavailable_html(conn, _st(rec="")))


def _colours(v, text=False):
    if isinstance(v, dict):
        for k, x in v.items():
            yield from _colours(x, text or k == "font")
    elif isinstance(v, list):
        for x in v:
            yield from _colours(x, text)
    elif isinstance(v, str) and len(v) == 7 and v.startswith("#"):
        yield v.lower(), text


@pytest.mark.parametrize("pal", ["peach", "white", "cool", "pantry"])
def test_circle_labels_are_readable_on_the_page_in_every_world(conn, pal):
    import r42_palette as P
    page = P.tokens(pal)["page"]
    data = C.graph_data(conn, _st(tc=["sour:lemon"], tcx="aromatic", pal=pal))
    page = P.tokens(pal)["circle-canvas"]
    labels = [col for col, is_text in _colours(data) if is_text]
    assert labels
    for col in labels:
        assert P.contrast(col, page) >= 4.5, (pal, col)


@pytest.mark.parametrize("pal", ["white", "cool", "pantry"])
def test_circle_uses_only_the_worlds_role_colours(conn, pal):
    """No product food colour survives in the new worlds."""
    import r42_palette as P
    allowed = {v.lower() for v in P.tokens(pal).values()}
    for st in (_st(pal=pal), _st(tc=["sour:lemon"], tcx="aromatic", pal=pal)):
        cols = {col for col, _t in _colours(C.graph_data(conn, st))}
        assert cols and cols <= allowed, cols - allowed


def test_circle_roles(conn):
    import r42_palette as P
    T = P.tokens("white")
    st = _st(tc=["sour:lemon"], tcx="aromatic", pal="white")
    nodes = {n["id"]: n for n in C.graph_data(conn, st)["nodes"]}
    assert nodes["dim:sour"]["color"]["border"] == T["sel-border"]         # locked, stepped back
    calm = {n["id"]: n for n in C.graph_data(conn, _st(tc=["sour:lemon"], pal="white"))["nodes"]}
    assert calm["dim:sour"]["color"]["border"] == T["sel-base"]            # locked: selection blue
    assert nodes["dim:aromatic"]["color"]["background"] == T["sel-base"]   # expanded: solid blue
    assert nodes["dim:umami"]["color"]["background"] == T["fill-2"]        # provided: neutral fill
    assert nodes["filler:aromatic:garlic"]["color"]["background"] == T["have-subtle"]   # on hand


def test_peach_reference_keeps_no_grey(conn):
    import r42_palette as P
    data = C.graph_data(conn, _st(tc=["sour:lemon"], tcx="aromatic", pal="peach"))
    for col, is_text in _colours(data):
        if not is_text:
            assert P.hex_to_hsl(col)[1] >= P.NEUTRAL_MIN_SAT, col


def test_pantry_circle_roles(conn):
    import r42_palette as P
    T = P.tokens("pantry")
    calm = {n["id"]: n for n in C.graph_data(conn, _st(tc=["sour:lemon"], pal="pantry"))["nodes"]}
    assert calm["dim:sour"]["color"]["background"] == T["circle-lock-fill"]     # red cabbage
    assert calm["dim:salty"]["color"]["background"] == T["fill"]                # still to fill: pale sage
    assert calm["dim:umami"]["color"]["background"] == T["panel"]               # provided: yogurt
    mustard = {"#f1e5ae", "#674c14"}
    assert not mustard & {c for c, _t in _colours(C.graph_data(conn, _st(tc=["sour:lemon"], pal="pantry")))}


def test_pantry_mustard_marks_only_the_opened_dimension_and_its_fan(conn):
    """Outline = focus, fill = status: Sour open is mustard, the rest stay
    pale sage; lemon in the fan keeps its parsley fill with a mustard
    outline, and turns red cabbage once locked in."""
    import r42_palette as P
    T = P.tokens("pantry")
    d = C.graph_data(conn, _st(tcx="sour", pal="pantry"))
    nodes = {n["id"]: n for n in d["nodes"]}
    assert nodes["dim:sour"]["color"]["background"] == "#F1E5AE"
    assert nodes["dim:sour"]["color"]["border"] == "#674C14"
    others = [n for k, n in nodes.items() if k.startswith("dim:") and k != "dim:sour"
              and C.node_state(_st(tcx="sour", pal="pantry"), k[4:], set()) == "open"
              and n["color"]["background"] != T["panel"]]
    assert others and all(n["color"]["background"] == T["fill"] for n in others)
    lemon = nodes["filler:sour:lemon"]["color"]
    assert (lemon["background"], lemon["border"]) == (T["have-subtle"], "#674C14")
    fan = [e for e in d["edges"] if e["to"].startswith("filler:sour:")]
    assert fan and all(e["color"]["color"] == "#674C14" for e in fan)
    locked = {n["id"]: n for n in C.graph_data(conn, _st(tc=["sour:lemon"], pal="pantry"))["nodes"]}
    assert locked["dim:sour"]["color"]["background"] == "#ECDFF0"
