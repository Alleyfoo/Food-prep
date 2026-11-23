"""R4.1 research prototype: R4 with refined data readability.

R4's model is reused unchanged. These tests cover (a) R4's correctness
guarantees carried into the new renderers and (b) the interaction and
presentation behaviour R4.1 changed: no coded glyphs in the default views,
graph collapse above GRAPH_LIMIT, the fact-sheet index, missing knowledge vs
missing ingredients, grouped tastings, and one marker vocabulary for the
shared selection. They say nothing about whether people understand it.
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
for p in (R4, R41):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from foodprep import loader  # noqa: E402
import r4_model as M  # noqa: E402
import r41_state as S  # noqa: E402
import r41_views as V  # noqa: E402

BROCCOLI = ("broccoli", ["yogurt", "lemon", "garlic"])
RB = "roasted_broccoli_component"
SB = "steamed_broccoli_component"
SRP = "smashed_roasted_potato_component"
RP = "roasted_potato_component"
GLYPHS = "●◐○◇✓≠☐☑⇄"          # R4's coded marks that needed a legend


@pytest.fixture(scope="module")
def conn(tmp_path_factory):
    tmp = tmp_path_factory.mktemp("r41") / "tastings.yaml"
    shutil.copy(ROOT / "src/foodprep/data/tastings.yaml", tmp)
    c = sqlite3.connect(":memory:")
    c.row_factory = sqlite3.Row
    loader.build(c, tastings_path=tmp)
    return c


def _text(html: str) -> str:
    return re.sub(r"\s+", " ", unescape(re.sub(r"<[^>]+>", " ", html)))


def _st(ing="broccoli", have=(), **kw):
    st = S.parse({"ingredient": ing, "have": ",".join(have)})
    st.update(kw)
    return st


def _follow(href: str) -> dict:
    return S.parse(dict(p.split("=", 1) for p in unescape(href)[1:].split("&") if "=" in p))


DATASETS = [BROCCOLI, ("cabbage", ["lemon"]), ("potato", []), ("tomato", [])]


# --- R4 guarantees carried over --------------------------------------------

@pytest.mark.parametrize("ing,have", DATASETS)
def test_every_pairing_appears_in_all_four_representations(conn, ing, have):
    m = M.build(conn, ing, have)
    matrix = V.overview_html(m, _st(ing, have, cols="matrix"))
    for s in m["states"]:
        comp = s["component"]
        sheet = _text(V.detail_html(m, _st(ing, have, rec=comp), comp))
        trace = V.trace_table_html(m, _st(ing, have, trace=f"state:{comp}", depth=2))
        other = next(x["component"] for x in m["states"] if x["component"] != comp)
        cmp_ = V.compare_html(m, _st(ing, have, cmp=[comp, other]))
        for p in M.of(m, comp, "pairing"):
            assert f"ingredient:{p['ingredient']}" in matrix, (comp, p["ingredient"])
            assert M.pretty(p["ingredient"]) in sheet, (comp, p["ingredient"])
            assert f"ingredient:{p['ingredient']}" in trace, (comp, p["ingredient"])
            assert f"ingredient:{p['ingredient']}" in cmp_, (comp, p["ingredient"])


def test_graph_and_table_show_the_same_edges(conn):
    for ing, have in DATASETS[:3]:
        m = M.build(conn, ing, have)
        for s in m["states"]:
            for d in (1, 2, 3):
                st = _st(ing, have, trace=f"state:{s['component']}", depth=d)
                edges, nodes = V.trace_edges(m, st)
                assert V.trace_dot(m, st).count(" -> ") == len(edges)
                table = V.trace_table_html(m, st)
                assert table.count('<tr class="edge">') == len(edges)


def test_confidence_scales_stay_named(conn):
    m = M.build(conn, "broccoli", [])
    sheet = _text(V.detail_html(m, _st(rec=RB), RB))
    assert "(attestation)" in sheet and "Inference strength" in sheet
    assert "not graded (recorded as “experimental”)" in sheet


def test_filters_grey_rows_with_reason_in_every_pane(conn):
    m = M.build(conn, "cabbage", ["lemon"])
    st = _st("cabbage", ["lemon"], paired=["lemon"])
    full = V.overview_html(m, _st("cabbage", ["lemon"]))
    filt = V.overview_html(m, st)
    assert full.count("<tr") == filt.count("<tr")
    assert "excluded: no pairing with lemon" in filt
    excluded = [s["component"] for s in m["states"] if S.exclusion(m, s["component"], st)]
    hidden = V.overview_html(m, dict(st, hide=True))
    assert hidden.count("<tr") == full.count("<tr") - len(excluded)
    ex = excluded[0]
    assert "Excluded by the active filters" in V.detail_html(m, dict(st, rec=ex), ex)
    keep = next(s["component"] for s in m["states"] if s["component"] not in excluded)
    assert "Excluded by the active filters" in V.compare_html(m, dict(st, cmp=[ex, keep]))
    assert "excluded by filter" in V.trace_table_html(m, dict(st, trace=f"state:{ex}"))
    assert f"{len(excluded)} of {len(m['states'])} rows excluded" in V.context_bar(m, st)


def test_url_state_round_trips_including_graph(conn):
    st = _st(*BROCCOLI, rec=RB, cmp=[RB, SB], trace="ingredient:lemon", pane="trace",
             depth=2, paired=["lemon"], diff=True, graph=True)
    back = _follow(S.href(st))
    for k in S.GLOBAL + S.SELECTION + S.LOCAL:
        assert back[k] == st[k], k


# --- Phase 2: overview without a decoding step ------------------------------

@pytest.mark.parametrize("ing,have", DATASETS)
def test_default_overview_matrix_and_compare_use_no_coded_glyphs(conn, ing, have):
    m = M.build(conn, ing, have)
    comps = [s["component"] for s in m["states"]]
    st = _st(ing, have, rec=comps[0], cmp=comps[:2], trace=f"state:{comps[0]}")
    for html in (V.overview_html(m, st), V.overview_html(m, dict(st, cols="matrix")),
                 V.overview_html(m, dict(st, cols="evidence")), V.compare_html(m, st),
                 V.detail_html(m, st, comps[0]), V.trace_table_html(m, st)):
        assert not set(_text(html)) & set(GLYPHS)


def test_overview_states_coverage_and_on_hand_in_words(conn):
    m = M.build(conn, *BROCCOLI)
    ov = _text(V.overview_html(m, _st(*BROCCOLI)))
    assert "all 6 needed roles covered" in ov
    assert "on hand: lemon (acid)" in ov
    assert "not on hand: walnut" in ov and "all required on hand" in ov
    assert "experimental pairing: brown butter (fat)" in ov
    assert "tasted: brown butter, works" in ov
    p = M.build(conn, "potato", [])
    ovp = _text(V.overview_html(p, _st("potato")))
    assert "0 of 3 needed roles covered" in ovp
    assert "on hand" not in ovp            # nothing entered: availability is not shown


def test_overview_keeps_the_column_count(conn):
    m = M.build(conn, *BROCCOLI)
    head = re.search(r"<thead>.*?</thead>", V.overview_html(m, _st(*BROCCOLI)), re.S).group(0)
    assert head.count("<th>") == 5          # R4: 7 (incl. pin and trace columns)
    p = M.build(conn, "potato", [])          # no route anywhere: banner, no empty column
    ov = V.overview_html(p, _st("potato"))
    head = re.search(r"<thead>.*?</thead>", ov, re.S).group(0)
    assert head.count("<th>") == 4 and "Flavour routes" not in head
    assert "For every potato preparation: no flavour route" in _text(ov)


# --- Phase 3: fact sheet ----------------------------------------------------

def test_section_index_links_to_every_section(conn):
    m = M.build(conn, *BROCCOLI)
    sheet = V.detail_html(m, _st(*BROCCOLI, rec=RB), RB)
    for n in range(1, 9):
        anchor = V._anchor(RB, n)
        assert f'href="#{anchor}"' in sheet and f'id="{anchor}"' in sheet
    txt = _text(sheet)
    for band in ("Attributes", "Relationships", "Evidence and testing", "Gaps"):
        assert band in txt


def test_uniformly_missing_claim_scope_is_stated_once_per_table(conn):
    m = M.build(conn, *BROCCOLI)
    sheet = _text(V.detail_html(m, _st(*BROCCOLI, rec=RB), RB))
    pairings = sheet.split("4 Recorded pairings")[1].split("5 Flavour routes")[0]
    assert "claim scope: not recorded" not in pairings
    assert pairings.count("Claim scope: not recorded on any of the") == 1


def test_missing_knowledge_is_kept_apart_from_missing_ingredients(conn):
    m = M.build(conn, *BROCCOLI)
    s8 = _text(V.detail_html(m, _st(*BROCCOLI, rec=RB), RB)).split("8 Missing or incomplete")[1]
    know, stock = s8.split("Not on hand (your ingredients)")
    assert "walnut" not in know
    assert "Sour and toasted nut: required walnut not on hand" in stock
    p = M.build(conn, "potato", [])
    s8p = _text(V.detail_html(p, _st("potato", rec=SRP), SRP)).split("8 Missing or incomplete")[1]
    assert "no curated pairing for acid, herb, fat" in s8p
    assert "availability is not assessed. This is not a gap in the data" in s8p


def test_tastings_are_grouped_apart_from_untested_ideas(conn):
    m = M.build(conn, "broccoli", [])
    s7 = _text(V.detail_html(m, _st(rec=RB), RB)).split("7 Experimental ideas")[1]
    s7 = s7.split("8 Missing")[0]
    i_tast = s7.index("Recorded tasting results")
    i_exp = s7.index("Experimental pairings", i_tast)
    i_scout = s7.index("Scout ideas (6: 1 tasted")
    assert i_tast < i_exp < i_scout
    assert "2026-08-12" in s7[i_tast:i_exp] and "works" in s7[i_tast:i_exp]


# --- Phase 4: compare -------------------------------------------------------

def test_compare_distinguishes_not_a_need_from_not_recorded_in_words(conn):
    m = M.build(conn, *BROCCOLI)
    html = V.compare_html(m, _st(*BROCCOLI, cmp=[RB, SB]))
    assert "not a listed need" in html                      # steamed: herb
    p = M.build(conn, "potato", [])
    hp = V.compare_html(p, _st("potato", cmp=[RP, SRP]))
    assert "needed, no curated pairing recorded" in hp and "no route recorded" in hp
    assert V.matrix_cell(m, _st(*BROCCOLI), SB, "herb").startswith('<td class="na"')


def test_compare_marks_identical_rows_and_counts_differences(conn):
    m = M.build(conn, *BROCCOLI)
    st = _st(*BROCCOLI, cmp=[RB, SB])
    html = V.compare_html(m, st)
    rows = V.compare_rows(m, st, [RB, SB])
    n_diff = sum(len(set(k)) > 1 for *_, k in rows)
    assert f"{n_diff} of {len(rows)} rows differ" in _text(html)
    assert html.count('class="tag t-diff"') == n_diff
    assert html.count('<tr class="same">') == len(rows) - n_diff
    only = V.compare_html(m, dict(st, diff=True))
    assert '<tr class="same">' not in only
    assert f"{len(rows) - n_diff} identical rows hidden" in _text(only)


def test_compare_letters_are_the_same_in_every_place(conn):
    m = M.build(conn, *BROCCOLI)
    st = _st(*BROCCOLI, rec=RB, cmp=[RB, SB])
    ov = _text(V.overview_html(m, st))
    assert "compare A" in ov and "compare B" in ov
    assert "A · Roasted broccoli" in _text(V.context_bar(m, st)) or \
        "A · roasted broccoli" in _text(V.context_bar(m, st))
    assert "A roasted broccoli, B steamed broccoli" in _text(V.tabs_html(m, st, "compare"))
    head = _text(V.compare_html(m, st)).split("Identity")[0]
    assert head.index("A") < head.index("roasted broccoli") < head.index("B")


# --- Phase 5: trace ---------------------------------------------------------

def test_large_graph_is_collapsed_and_the_table_keeps_every_edge(conn):
    m = M.build(conn, *BROCCOLI)
    st = _st(*BROCCOLI, rec=RB, trace=f"state:{RB}", depth=2)
    edges, nodes = V.trace_edges(m, st)
    assert len(edges) > V.GRAPH_LIMIT
    assert V.graph_placement(m, st) == "collapsed"
    note = _text(V.graph_note_html(m, st))
    assert f"{len(edges)} relationships" in note and "Show the complete graph" in note
    assert V.trace_table_html(m, st).count('<tr class="edge">') == len(edges)
    shown = dict(st, graph=True)
    assert V.graph_placement(m, shown) == "below"
    assert V.trace_table_html(m, shown).count('<tr class="edge">') == len(edges)


def test_small_graph_is_shown(conn):
    m = M.build(conn, *BROCCOLI)
    st = _st(*BROCCOLI, trace="ingredient:lemon", depth=1)
    assert 0 < len(V.trace_edges(m, st)[0]) <= V.GRAPH_LIMIT
    assert V.graph_placement(m, st) == "shown" and V.graph_note_html(m, st) == ""
    assert V.graph_placement(m, _st(*BROCCOLI)) == "none"


def test_revealing_the_graph_is_local(conn):
    m = M.build(conn, *BROCCOLI)
    st = _st(*BROCCOLI, rec=RB, cmp=[RB, SB], trace=f"state:{RB}", depth=2, paired=["lemon"])
    href = re.search(r'href="([^"]*graph=1[^"]*)"', V.graph_note_html(m, st)).group(1)
    nxt = _follow(href)
    for k in S.GLOBAL + S.SELECTION + ("pane", "depth"):
        assert nxt[k] == st[k], k
    assert nxt["graph"] is True


def test_trace_table_keeps_names_whole_and_sources_with_scope(conn):
    m = M.build(conn, *BROCCOLI)
    st = _st(*BROCCOLI, trace=f"state:{RB}", depth=2)
    css = V.CSS
    assert "overflow-wrap:anywhere" not in css
    assert "table.trace td a {white-space:nowrap}" in css.replace(".r4 .nm, .r4 ", ".r4 ")
    table = _text(V.trace_table_html(m, st))
    assert "roast_culinary" in table and "claim scope" in table


def test_trace_focus_is_violet_not_compare_blue(conn):
    m = M.build(conn, *BROCCOLI)
    dot = V.trace_dot(m, _st(*BROCCOLI, trace="ingredient:lemon"))
    line = next(x for x in dot.splitlines() if x.startswith('"ingredient:lemon"'))
    assert "#6b4fa0" in line and "#1a4f8b" not in line


# --- Phase 6: coordinated selections ----------------------------------------

def test_overview_marks_detail_compare_and_trace_separately(conn):
    m = M.build(conn, *BROCCOLI)
    st = _st(*BROCCOLI, rec=RB, cmp=[RB, SB], trace="ingredient:lemon")
    ov = V.overview_html(m, st)
    rows = {s["component"]: r for s, r in zip(m["states"], re.findall(r"<tr class.*?</tr>", ov, re.S))}
    assert "in detail" in rows[RB] and "compare A" in rows[RB]
    assert "compare B" in rows[SB] and "in detail" not in rows[SB]
    lemon_states = {p["state"] for p in M.of(m, kind="pairing") if p["ingredient"] == "lemon"}
    for comp, row in rows.items():
        assert ("in trace" in row) == (comp in lemon_states), comp
    st2 = dict(st, trace=f"state:{SB}")
    ov2 = V.overview_html(m, st2)
    assert ov2.count(">traced<") == 1


def test_each_concept_has_its_own_colour(conn):
    css = V.CSS
    assert "#fff4d1" in re.search(r"\.t-sel \{[^}]*\}", css).group(0)
    assert "#1a4f8b" in re.search(r"\.t-cmp \{[^}]*\}", css).group(0)
    assert "#6b4fa0" in re.search(r"\.t-trace \{[^}]*\}", css).group(0)
    assert "#1a4f8b" not in re.search(r"\.t-trace \{[^}]*\}", css).group(0)


@pytest.mark.parametrize("local", [{"cols": "matrix"}, {"depth": 3}, {"diff": True},
                                   {"graph": True}, {"pane": "compare"}])
def test_local_controls_never_change_the_investigation_subject(conn, local):
    st = _st(*BROCCOLI, rec=RB, cmp=[RB, SB], trace="ingredient:lemon", paired=["lemon"])
    nxt = _follow(S.href(st, **local))
    for k in S.GLOBAL + S.SELECTION:
        assert nxt[k] == st[k], k


def test_overview_row_actions_are_words_and_keep_the_selection(conn):
    m = M.build(conn, *BROCCOLI)
    st = _st(*BROCCOLI, rec=RB)
    ov = V.overview_html(m, st)
    assert "compare with roasted broccoli" in ov and ">trace<" in ov
    href = re.search(r'href="([^"]*)"[^>]*>compare with roasted broccoli', ov).group(1)
    nxt = _follow(href)
    assert nxt["cmp"][0] == RB and nxt["rec"] == RB and nxt["pane"] == "compare"


# --- Phase 7: matrix --------------------------------------------------------

def test_matrix_lists_one_pairing_per_line_with_status_words(conn):
    m = M.build(conn, *BROCCOLI)
    fat = V.matrix_cell(m, _st(*BROCCOLI), RB, "fat")
    assert fat.count("<br>") == 3 and "experimental" in fat
    acid = V.matrix_cell(m, _st(*BROCCOLI), RB, "acid")
    assert "on hand" in acid
    p = M.build(conn, "potato", [])
    assert "needed, no curated pairing recorded" in V.matrix_cell(p, _st("potato"), SRP, "acid")


def test_matrix_legend_is_in_the_sticky_header(conn):
    m = M.build(conn, *BROCCOLI)
    ov = V.overview_html(m, _st(*BROCCOLI, cols="matrix"))
    head = re.search(r"<thead>.*?</thead>", ov, re.S).group(0)
    assert 'class="legendrow"' in head and "Hatched" in head
    assert "thead {position:sticky" in V.CSS
