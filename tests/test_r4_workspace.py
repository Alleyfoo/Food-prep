"""R4 research prototype: one integrated workspace over one presentation model.

Correctness only: these tests say the four representations show the same
records, keep dimensions apart and keep the shared context coherent. They do
not say the layout is understandable to a person.
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
PROTO = ROOT / "docs/research/ux-integrated-r4/prototype"
sys.path.insert(0, str(PROTO))

from foodprep import loader  # noqa: E402
import r4_model as M  # noqa: E402
import r4_state as S  # noqa: E402
import r4_views as V  # noqa: E402

BROCCOLI = ("broccoli", ["yogurt", "lemon", "garlic"])
RB = "roasted_broccoli_component"
SB = "steamed_broccoli_component"
SRP = "smashed_roasted_potato_component"


@pytest.fixture(scope="module")
def conn(tmp_path_factory):
    # A copy, never the real tastings file (read-only use, but a copy anyway).
    tmp = tmp_path_factory.mktemp("r4") / "tastings.yaml"
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


def _rec(m, **kw):
    return [r for r in m["records"] if all(r.get(k) == v for k, v in kw.items())]


# --- data preservation across all four representations ---------------------

@pytest.mark.parametrize("ing,have", [BROCCOLI, ("cabbage", ["lemon"]), ("potato", []),
                                      ("tomato", [])])
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
            name = M.pretty(p["ingredient"])
            assert f"ingredient:{p['ingredient']}" in matrix, (comp, name)
            assert name in sheet, (comp, name)
            assert f"ingredient:{p['ingredient']}" in trace, (comp, name)
            assert f"ingredient:{p['ingredient']}" in cmp_, (comp, name)


def test_every_record_has_a_stable_unique_id(conn):
    for ing in ("broccoli", "cabbage", "potato", "tomato"):
        m = M.build(conn, ing, [])
        ids = [r["id"] for r in m["records"]]
        assert len(ids) == len(set(ids)), ing
        assert M.build(conn, ing, ["lemon"])["records"][0]["id"] == ids[0]


# --- multi-dimensional status --------------------------------------------

def test_brown_butter_keeps_three_independent_dimensions(conn):
    m = M.build(conn, "broccoli", [])
    pair = _rec(m, state=RB, kind="pairing", ingredient="brown_butter")
    idea = _rec(m, state=RB, kind="idea", ingredient="brown_butter")
    assert len(pair) == 1 and len(idea) == 1
    pair, idea = pair[0], idea[0]
    assert pair["knowledge"] == "experimental" and pair["testing"] is None
    assert idea["knowledge"] == "generated"
    assert idea["confidence"]["field"] == "inference_strength"
    assert idea["testing"]["status"] == "tested"
    assert idea["testing"]["trials"][0]["verdict"] == "works"
    assert pair["availability"] == "not on hand" == idea["availability"]
    # availability changes, knowledge and testing do not
    m2 = M.build(conn, "broccoli", ["brown_butter"])
    p2 = _rec(m2, state=RB, kind="pairing", ingredient="brown_butter")[0]
    i2 = _rec(m2, state=RB, kind="idea", ingredient="brown_butter")[0]
    assert p2["availability"] == "on hand" == i2["availability"]
    assert (p2["knowledge"], i2["testing"]["status"]) == ("experimental", "tested")


def test_confidence_scales_are_never_merged(conn):
    m = M.build(conn, "broccoli", [])
    fields = {(r["kind"], r["confidence"]["field"]) for r in m["records"] if r["confidence"]}
    assert fields <= {("transformation", "confidence"), ("pairing", "confidence"),
                      ("route_fit", "attestation"), ("idea", "inference_strength")}
    sheet = _text(V.detail_html(m, _st(rec=RB), RB))
    assert "(attestation)" in sheet and "(inference strength)" in sheet


def test_links_are_by_ids_and_never_merge_records(conn):
    for ing in ("broccoli", "cabbage", "potato", "tomato"):
        m = M.build(conn, ing, [])
        for g in m["links"]:
            recs = [r for r in m["records"] if r["id"] in g["records"]]
            assert {r["kind"] for r in recs} == {"pairing", "idea"}
            assert {(r["component_id"], r["ingredient_id"]) for r in recs} == \
                {(g["component_id"], g["ingredient_id"])}
            assert g["basis"] == "same component_id and ingredient_id"
        linked_ids = {i for g in m["links"] for i in g["records"]}
        assert not any(r["kind"] == "route_element" and r["id"] in linked_ids
                       for r in m["records"])
    m = M.build(conn, "broccoli", [])
    assert [(g["state"], g["ingredient"]) for g in m["links"]] == [(RB, "brown_butter")]


def test_brown_butter_shows_once_per_representation_with_both_properties(conn):
    m = M.build(conn, "broccoli", [])
    st = _st(trace=f"state:{RB}", depth=2)
    edges, nodes = V.trace_edges(m, st)
    bb = [n for n in nodes if n == "ingredient:brown_butter"]
    assert len(bb) == 1
    assert "experimental · idea · tasted" in V.trace_dot(m, st)
    sheet = _text(V.detail_html(m, _st(rec=RB), RB))
    assert "also a Scout idea (same ids)" in sheet
    assert "experimental pairing for fat" in sheet          # in the ideas table
    row = re.search(r"fat brown butter.*?(?=fat garlic confit)", sheet).group(0)
    assert "curated" not in row


# --- pairing and source traceability -------------------------------------

def test_lemon_on_roasted_broccoli_traces_to_its_named_source(conn):
    m = M.build(conn, *BROCCOLI)
    lemon = _rec(m, state=RB, kind="pairing", ingredient="lemon")[0]
    srcs = lemon["evidence"]["sources"]
    assert [s["title"] for s in srcs] == ["roast_culinary"]
    assert srcs[0]["type"] == "culinary" and srcs[0]["claim_scope"] is None
    sheet = _text(V.detail_html(m, _st(*BROCCOLI, rec=RB), RB))
    assert "roast_culinary culinary scope: not recorded" in sheet
    assert "not a claim about these pairings" in sheet
    sid = srcs[0]["source_id"]
    trace = _text(V.trace_table_html(m, _st(*BROCCOLI, trace=f"source:{sid}")))
    assert "roasted broccoli · acid · lemon" in trace
    assert "backs pairing" in trace


def test_step_and_pairing_sources_are_kept_apart(conn):
    m = M.build(conn, *BROCCOLI)
    step = _rec(m, state=RB, kind="transformation")[0]
    assert all(s["claim_scope"] for s in step["evidence"]["sources"])
    sheet = V.detail_html(m, _st(*BROCCOLI, rec=RB), RB)
    i_step = sheet.index("Sources for the preparation step")
    i_pair = sheet.index("Sources for the pairings")
    assert i_step < i_pair
    for s in step["evidence"]["sources"]:
        assert s["claim_scope"] in unescape(sheet[i_step:i_pair])


def test_experimental_pairings_have_no_invented_source(conn):
    m = M.build(conn, "broccoli", [])
    for p in _rec(m, kind="pairing", knowledge="experimental"):
        assert p["evidence"]["sources"] == []
        assert p["evidence"]["coverage"] == "no source recorded"


def test_zero_corpus_counts_are_never_shown_as_evidence(conn):
    m = M.build(conn, *BROCCOLI)
    assert M.corpus_populated(m) is False
    sheet = _text(V.detail_html(m, _st(*BROCCOLI, rec=RB), RB))
    assert "0 does not mean the pairing never occurs" in sheet
    assert not re.search(r"\b0 recipes?\b", sheet)


# --- required vs optional route elements ---------------------------------

def test_finish_and_supporting_elements_are_not_requirements(conn):
    m = M.build(conn, *BROCCOLI)
    dill = _rec(m, state=RB, kind="route_element", ingredient="dill")[0]
    assert dill["optionality"] == "finish"
    fit = _rec(m, state=RB, kind="route_fit", route_id="creamy_and_acidic")[0]
    assert fit["attrs"]["required_on_hand"] == [2, 2]   # yogurt + lemon; dill not counted
    sheet = _text(V.detail_html(m, _st(*BROCCOLI, rec=RB), RB))
    assert "dill finish" in sheet and "olive oil supporting" in sheet
    assert "also needs" not in sheet.lower()
    assert "required elements on hand: 2 of 2" in sheet


# --- missing-data semantics ----------------------------------------------

def test_sparse_record_states_gaps_without_instructions(conn):
    m = M.build(conn, "potato", [])
    g = M.gaps(m, SRP)
    assert any(x.startswith("no curated pairing for") for x in g)
    sheet = _text(V.detail_html(m, _st("potato", rec=SRP), SRP))
    assert "no pairing recorded for this preparation" in sheet
    assert "nobody wrote it down" in sheet
    for bad in ("add ", "try ", "you should"):
        assert bad not in sheet.lower(), bad
    # "not needed" appears only inside the disclaimer that says gaps aren't that
    assert sheet.lower().count("not needed") == 1
    assert "does not mean “not needed”" in sheet


def test_gap_shared_by_every_row_is_stated_once(conn):
    m = M.build(conn, "potato", [])
    assert M.shared_gaps(m) == ["no flavour route"]
    html = V.overview_html(m, _st("potato"))
    assert html.count("no flavour route") == 1
    assert "For every potato preparation: no flavour route" in _text(html)


def test_not_a_need_differs_from_not_recorded(conn):
    m = M.build(conn, *BROCCOLI)
    steamed_herb = V.matrix_cell(m, _st(*BROCCOLI), SB, "herb")
    assert steamed_herb == '<td class="na">—</td>'
    p = M.build(conn, "potato", [])
    acid = V.matrix_cell(p, _st("potato"), SRP, "acid")
    assert 'class="nr"' in acid and "no curated pairing" in acid


# --- comparison alignment ------------------------------------------------

def test_compare_rows_are_aligned_and_flag_differences(conn):
    m = M.build(conn, *BROCCOLI)
    st = _st(*BROCCOLI, cmp=[RB, SB])
    rows = V.compare_rows(m, st, [RB, SB])
    assert all(len(cells) == 2 == len(keys) for _, _, cells, keys in rows)
    by = {lab: keys for _, lab, _, keys in rows}
    assert len(set(by["Technique"])) == 2
    assert len(set(by["From"])) == 1
    roles = {lab for g, lab, _, _ in rows if g == "Needs and pairings"}
    needed = {n["role"] for c in (RB, SB) for n in M.of(m, c, ("need", "pairing"))}
    assert roles == needed
    full = V.compare_html(m, st)
    only = V.compare_html(m, dict(st, diff=True))
    assert only.count("<tr") < full.count("<tr")
    assert "From" not in _text(only).split("Technique")[0]


def test_sparse_vs_complete_compare_shows_missing_explicitly(conn):
    m = M.build(conn, "potato", [])
    st = _st("potato", cmp=["roasted_potato_component", SRP])
    html = V.compare_html(m, st)
    assert "no curated pairing" in html and "no route recorded" in html


# --- shared selection and navigation ------------------------------------

def test_url_state_round_trips(conn):
    st = _st(*BROCCOLI, rec=RB, cmp=[RB, SB], trace="ingredient:lemon", pane="trace",
             depth=2, paired=["lemon"], diff=True)
    back = S.parse(dict(p.split("=", 1) for p in S.href(st)[1:].split("&")))
    for k in S.GLOBAL + S.SELECTION + S.LOCAL:
        assert back[k] == st[k], k


def test_opening_a_pane_never_clears_the_shared_selection(conn):
    m = M.build(conn, *BROCCOLI)
    st = _st(*BROCCOLI, rec=RB, cmp=[RB, SB])
    sheet = V.detail_html(m, st, RB)
    href = re.search(r'href="([^"]*trace=ingredient:lemon[^"]*)"', sheet).group(1)
    nxt = S.parse(dict(p.split("=", 1) for p in unescape(href)[1:].split("&")))
    assert (nxt["rec"], nxt["cmp"], nxt["pane"]) == (RB, [RB, SB], "trace")
    # trace -> detail: a connected prepared ingredient opens its own sheet
    table = V.trace_table_html(m, nxt)
    href = re.search(r'href="([^"]*rec=steamed_broccoli_component[^"]*)"', table).group(1)
    nxt2 = S.parse(dict(p.split("=", 1) for p in unescape(href)[1:].split("&")))
    assert (nxt2["rec"], nxt2["pane"], nxt2["trace"]) == (SB, "detail", "ingredient:lemon")
    assert nxt2["cmp"] == [RB, SB]


def test_pinning_compares_with_the_selected_record(conn):
    st = _st(*BROCCOLI, rec=RB)
    ch = S.pin(st, SB)
    assert ch == {"cmp": [RB, SB], "pane": "compare"}
    st2 = dict(st, **ch)
    assert S.pin(st2, SB) == {"cmp": [RB], "pane": "detail"}
    assert S.pin(_st(*BROCCOLI), SB) == {"cmp": [SB], "pane": ""}


def test_ingredient_change_drops_foreign_selection_but_keeps_ingredient_trace(conn):
    st = _st("broccoli", rec=RB, cmp=[RB, SB], trace="ingredient:lemon")
    st2 = S.reconcile(dict(st, ingredient="cabbage"), M.build(conn, "cabbage", []))
    assert (st2["rec"], st2["cmp"], st2["trace"]) == ("", [], "ingredient:lemon")
    st3 = S.reconcile(dict(st, ingredient="cabbage", trace=f"state:{RB}"),
                      M.build(conn, "cabbage", []))
    assert st3["trace"] == ""


def test_graph_and_table_show_the_same_edges_with_unique_nodes(conn):
    for ing, have in (BROCCOLI, ("cabbage", ["lemon"]), ("potato", [])):
        m = M.build(conn, ing, have)
        for s in m["states"]:
            for d in (1, 2, 3):
                st = _st(ing, have, trace=f"state:{s['component']}", depth=d)
                edges, nodes = V.trace_edges(m, st)
                dot = V.trace_dot(m, st)
                assert dot.count(" -> ") == len(edges)
                table = V.trace_table_html(m, st)
                assert table.count("<tr>") - 1 == len(edges)
                declared = re.findall(r'^"([^"]+)" \[', dot, re.M)
                assert len(declared) == len(set(declared)) == len(nodes)


def test_trace_starts_limited_and_reveals_deliberately(conn):
    m = M.build(conn, *BROCCOLI)
    n = [len(V.trace_edges(m, _st(*BROCCOLI, trace=f"state:{RB}", depth=d))[0])
         for d in (1, 2, 3)]
    assert n[0] < n[1] < n[2]
    d1 = V.trace_edges(m, _st(*BROCCOLI, trace=f"state:{RB}", depth=1))[0]
    assert not any(e["records"] and e["records"][0]["knowledge"] in ("experimental", "generated")
                   for e in d1)


# --- filter behaviour ----------------------------------------------------

def test_filters_grey_rows_with_reason_in_every_pane(conn):
    m = M.build(conn, "cabbage", ["lemon"])
    st = _st("cabbage", ["lemon"], paired=["lemon"])
    full = V.overview_html(m, _st("cabbage", ["lemon"]))
    filt = V.overview_html(m, st)
    assert full.count("<tr") == filt.count("<tr")
    assert "excluded: no pairing with lemon" in filt
    hidden = V.overview_html(m, dict(st, hide=True))
    excluded = [s["component"] for s in m["states"] if S.exclusion(m, s["component"], st)]
    assert excluded and hidden.count("<tr") == full.count("<tr") - len(excluded)
    ex = excluded[0]
    assert "Excluded by the active filters" in V.detail_html(m, dict(st, rec=ex), ex)
    keep = next(s["component"] for s in m["states"] if s["component"] not in excluded)
    assert "Excluded by the active filters" in V.compare_html(m, dict(st, cmp=[ex, keep]))
    tr = V.trace_table_html(m, dict(st, trace=f"state:{ex}"))
    assert "excluded by filter" in tr


def test_k7_cabbage_preparations_paired_with_lemon(conn):
    m = M.build(conn, "cabbage", ["lemon"])
    st = _st("cabbage", ["lemon"], paired=["lemon"])
    match = [s["component"] for s in m["states"] if not S.exclusion(m, s["component"], st)]
    expected = sorted({p["state"] for p in M.of(m, kind="pairing") if p["ingredient"] == "lemon"})
    assert sorted(match) == expected and match
    assert f"{len(match)} of {len(m['states'])} match" in V.overview_html(m, st)


def test_availability_comes_only_from_user_input(conn):
    m = M.build(conn, "broccoli", [])
    assert not any(r["availability"] == "on hand" for r in m["records"])
    m2 = M.build(conn, *BROCCOLI)
    on = {r["ingredient"] for r in m2["records"] if r["availability"] == "on hand"}
    assert on <= set(BROCCOLI[1])


def test_graph_node_tags_come_only_from_edges_in_this_trace(conn):
    # lingonberry vinegar is an experimental pairing on steamed broccoli, but on
    # roasted broccoli it is only a Scout idea: the node must not say "experimental".
    m = M.build(conn, *BROCCOLI)
    dot = V.trace_dot(m, _st(*BROCCOLI, trace=f"state:{RB}", depth=2))
    line = next(x for x in dot.splitlines() if x.startswith('"ingredient:lingonberry_vinegar"'))
    assert "idea" in line and "experimental" not in line
    bb = next(x for x in dot.splitlines() if x.startswith('"ingredient:brown_butter"'))
    assert "experimental · idea · tasted" in bb
