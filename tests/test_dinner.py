"""R7: the Dinner views over the documented R3-R5 records (foodprep.dinner).

Each test pins a behaviour the R7 recommendation asks for
(docs/research/r6-academic-foundations/r7-recommendation.md) against the real
data: outcome first, component branches, aligned routes, swaps, start from a
held state, the mindmap's outcome ring, and what the views must never do.
"""

from __future__ import annotations

from html import escape as html_escape

import pytest

from foodprep import conditions as cd
from foodprep import dinner as d
from foodprep import kitchen_records as kr
from foodprep.ui import dinner_render as dnr


@pytest.fixture(autouse=True)
def _private_records(tmp_path, monkeypatch):
    """The views read the user's records; tests never see the real ones."""
    monkeypatch.setenv(kr.CONTROL_ENV, str(tmp_path / "control.yaml"))
    monkeypatch.setenv(kr.SHELF_ENV, str(tmp_path / "shelf.yaml"))


def _steps(ov: d.Overview) -> list:
    return [s for b in ov.branches for s in b.steps] + [s for j in ov.joins for s in j.steps]


# ---- 1. what can I make with this ------------------------------------------------

def test_dried_peas_less_usual_use_is_pea_falafel():
    res = d.outcomes("dried_peas")
    assert [o.key for o in res.less_usual] == ["transfer:pea_falafel"]
    assert res.familiar == []        # R3 holds no pea dish: said, not invented
    oc = res.less_usual[0]
    assert oc.group == "less_usual"
    assert "worth cooking" in oc.verdict
    assert oc.swapped == "pea instead of chickpea"


def test_pea_soup_appears_only_as_the_soaking_record_says_it():
    res = d.outcomes("dried_peas.dried_seed")
    says = [v.text for p in res.part_records for cf in p.conflicts for v in cf.versions]
    assert any("soup" in x for x in says)
    assert not any("soup" in o.name.lower() for o in res.familiar + res.less_usual)


def test_pea_falafel_shows_the_safety_gap_in_words():
    oc = d.outcomes("dried_peas").less_usual[0]
    notes = " ".join(n for _, n in oc.keeping) + " ".join(oc.gaps)
    assert "Q505" in notes                     # FS1: never eaten only soaked
    assert "treatment" in notes                # whether frying counts is open
    assert any("dry and hard" in r.text for r in oc.risks)


def test_outcome_condition_and_cooked_and_availability():
    oc = next(o for o in d.outcomes("rutabaga").less_usual
              if o.key == "transfer:rutabaga_gratin")
    assert oc.condition is not None
    assert oc.condition.text.startswith("Do not skip: blanch (rutabaga)")
    assert oc.condition.sources == ["G20", "G21"]
    assert oc.cooked == []
    assert ("rutabaga", "no shelf check of yours recorded") in oc.availability


def test_availability_comes_only_from_the_users_shelf_checks():
    kr.record_shelf_check("rutabaga", checked_on="2026-11-25", seen=True, note="1 kg")
    oc = next(o for o in d.outcomes("rutabaga").less_usual
              if o.key == "transfer:rutabaga_gratin")
    words = dict(oc.availability)["rutabaga"]
    assert words == "seen at Lidl on 2026-11-25 (1 kg)"
    # the lidl.fi text in transfers.yaml is never shown as availability
    assert all("lidl.fi" not in w and "L1" not in w for _, w in oc.availability)


def test_refused_swap_stays_visible_with_its_reasons():
    oc = next(o for o in d.outcomes("kale").less_usual if o.key == "transfer:kale_rolls")
    assert oc.refused and oc.reasons
    assert oc.replaced_by == "napa_cabbage_rolls"
    rejected = next(o for o in d.outcomes("rutabaga").less_usual
                    if o.key == "transfer:rutabaga_gratin_raw")
    assert rejected.refused and "documented to fail" in rejected.verdict


def test_outcomes_keep_recorded_order_and_carry_no_score():
    keys = [o.key for o in d.outcomes("potato").familiar]
    order = [k for k in cd.routes() if k.split("/")[0] in {x.split("/")[0] for x in keys}]
    dishes = list(dict.fromkeys(k.split("/")[0] for k in order))
    assert [k.split("/")[0] for k in keys] == dishes
    for o in d.outcomes("potato").familiar:
        assert not {"score", "rank", "rating"} & set(vars(o))


# ---- 2. the component-branch overview --------------------------------------------

def test_gratin_overview_branches_join_and_member_lines():
    ov = d.overview("transfer:rutabaga_gratin")
    assert [b.member for b in ov.branches] == ["potato", "rutabaga"]
    assert [j.aid for j in ov.joins] == ["gratin"]
    blanch = ov.branches[1].steps[2]
    assert blanch.name == "blanch" and blanch.endpoint_words == "ready for the next step"
    assert blanch.because and "dense root" in blanch.because[0].text
    assert blanch.active is not None and blanch.active.sources
    bake = ov.joins[0].steps[0]
    assert bake.endpoint_words == "ready to eat"
    lines = {m.member: m for m in bake.members}
    assert set(lines) == {"potato", "rutabaga"}
    rut = [x.text for x in lines["rutabaga"].done_when]
    assert any("some give" in x for x in rut) and any("no resistance" in x for x in rut)


def test_not_found_member_endpoint_is_shown_as_itself():
    ov = d.overview("transfer:pea_falafel")
    fry = ov.joins[0].steps[-1]
    onion = next(m for m in fry.members if m.member == "onion")
    assert not onion.found
    assert "no source" in onion.note
    assert "not found" in dnr.step_html(fry)


def test_route_without_sequence_says_endpoint_not_recorded():
    ov = d.overview("latkes/settled_starch")
    assert not ov.has_sequence
    assert all(s.endpoint is None for s in _steps(ov))
    assert "endpoint not recorded" in dnr.overview_html(ov)


def test_conflicting_times_stay_separate_versions():
    blanch = d.overview("transfer:rutabaga_gratin").branches[1].steps[2]
    assert len(blanch.times) > 1                       # never one merged number
    cf = next(c for c in blanch.conflicts if "how long" in c.topic)
    assert len(cf.versions) == 2
    assert " · or " in dnr._choices(cf.versions)


def test_overview_lists_documented_alternatives_as_cited_text():
    ov = d.overview("transfer:rutabaga_gratin")
    assert len(ov.alternatives) == 5
    assert ov.alternatives[0].text.startswith("raw slices and a long covered bake:")
    assert "Other documented ways" in dnr.overview_html(ov)


def test_done_when_is_never_called_a_safety_limit():
    html = dnr.overview_html(d.overview("transfer:rutabaga_gratin"))
    assert html_escape(d.NOT_A_SAFETY_LIMIT) in html


# ---- 3. aligned columns ----------------------------------------------------------

def test_gratin_aligned_routes_include_the_rejected_route_with_none():
    al = d.aligned("transfer:rutabaga_gratin")
    kinds = {c.name: c.kind for c in al.columns}
    rejected = next(c for c in al.columns if c.kind == "rejected")
    assert rejected.key == "transfer:rutabaga_gratin_raw"
    assert "rutabaga:blanchir" not in rejected.cells           # "none" in that row
    assert "rutabaga:blanchir" in al.columns[0].cells
    assert any(k == "alternative" for k in kinds.values())     # cited text columns
    html = dnr.aligned_html(al)
    assert ">none<" in html and "not recorded step by step" in html


def test_aligned_never_adds_a_column_nobody_documented():
    al = d.aligned("transfer:rutabaga_gratin")
    seq = cd.sequence("transfer:rutabaga_gratin")
    documented = {a["name"] for a in seq["alternatives"]} | {d.route_label(al.key)}
    for col in al.columns:
        assert col.key in cd.routes() or col.name in documented
    # every whole-route column is a real route, built by the validator's walk
    assert all(col.key is None or col.key in cd.routes() for col in al.columns)


def test_dish_with_several_r3_routes_gets_each_as_a_column():
    al = d.aligned("gratin_dauphinois/raw_long_bake")
    keys = [c.key for c in al.columns if c.key]
    assert keys[:2] == ["gratin_dauphinois/raw_long_bake",
                        "gratin_dauphinois/simmered_then_baked"]


# ---- 4. a swap is a changed branch -------------------------------------------------

def test_napa_swap_marks_the_changed_branch_and_its_repairs():
    ov = d.overview("transfer:napa_cabbage_rolls")
    assert ov.swaps == {"cabbage": "napa"} and ov.base == "kaalikaaryleet/trimmed_rib"
    napa = next(b for b in ov.branches if b.member == "napa")
    assert napa.changed and napa.replaces == "cabbage"
    assert any("rib" in s.says for s in napa.steps)          # the repair, on the branch
    rice = next(b for b in ov.branches if b.member == "rice")
    assert not rice.changed


def test_added_member_is_named_in_the_swap():
    ov = d.overview("transfer:rutabaga_gratin")
    assert ov.added == ["rutabaga"]
    assert "adds rutabaga" in dnr.overview_html(ov)


def test_refused_kale_swap_overview_shows_its_reasons():
    ov = d.overview("transfer:kale_rolls")
    assert ov.refused and ov.reasons and ov.replaced_by == "napa_cabbage_rolls"
    html = dnr.overview_html(ov)
    assert "not worth it" in html and "Replaced by" in html


# ---- 5. start from what I have ---------------------------------------------------

def test_soaked_peas_start_from_marks_the_soak_done():
    sf = d.start_from("soaked_dried_peas")
    assert [h.route for h in sf.routes] == ["transfer:pea_falafel"]
    h = sf.routes[0]
    pea = next(b for b in h.overview.branches if b.member == "pea")
    assert pea.held_upto == 1 and pea.steps[0].done and not pea.steps[1].done
    assert sf.not_ready_to_eat and h.by_state
    html = dnr.start_from_html(sf)
    assert "Not ready to eat" in html and "History not considered" in html
    assert "Q505" in html
    pea_html = dnr.overview_html(h.overview, hide_done=True)
    assert "Done, you have this: soak (step 1)" in pea_html


def test_blanched_rutabaga_start_from():
    sf = d.start_from("blanched_rutabaga_slices")
    h = sf.routes[0]
    assert (h.route, h.owner, h.at, h.readiness) == ("transfer:rutabaga_gratin", "rutabaga", 3, True)
    assert any("home-economics" in k.text for k in sf.keeping)   # the authority, in words
    body = dnr.overview_html(h.overview, hide_done=True)
    # the whole rutabaga branch is held: it collapses to one line, the join remains
    assert "rutabaga: done, you have it." in body
    assert "blanch" not in body.split("dn-join")[0]
    assert "potato" in body


def test_state_after_a_step_is_matched_exactly_not_by_state():
    sf = d.start_from("rested_pea_paste")
    assert sf.routes and not any(h.by_state for h in sf.routes)
    assert d.HISTORY_NOT_CONSIDERED not in dnr.start_from_html(sf)


def test_every_held_state_opens():
    for iid, _ in d.held_states():
        assert d.start_from(iid) is not None


# ---- 6. the mindmap's outcome ring -----------------------------------------------

def test_outcome_edges_put_outcomes_in_the_second_ring():
    edges = d.outcome_edges("dried_peas")
    assert edges[0] == ("ing:dried_peas", "out:transfer:pea_falafel", "less usual use")
    assert all(a.startswith("out:") for a, _, lbl in edges if lbl == "also needs")


def test_map_table_is_default_above_about_twenty_edges():
    assert d.map_default_view(20) == "graph"
    assert d.map_default_view(21) == "table"
    assert d.map_default_view(len(d.outcome_edges("potato"))) == "table"


# ---- everything is a view: every route renders -----------------------------------

@pytest.mark.parametrize("key", list(cd.routes()))
def test_every_route_renders_both_views(key):
    assert dnr.overview_html(d.overview(key))
    assert dnr.aligned_html(d.aligned(key))


def test_unknown_route_is_not_found():
    assert d.overview("nope/nope") is None and d.aligned("nope/nope") is None
    assert d.start_from("nope") is None
