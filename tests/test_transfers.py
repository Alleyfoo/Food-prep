"""R4: controlled transfers (docs/research/r4-transfers/).

A transfer is a documented R3 route with one ingredient changed. These tests
say the transfer data is well formed, every cited source resolves to a page
that was read, the R3 validator runs on the derived route unchanged, and the
model's verdict on each transfer is the one the R4 documents report. They do
not say a transfer tastes good: that is the kitchen test's job."""

from __future__ import annotations

import copy
import re
from pathlib import Path

import pytest

from foodprep import constructions as c
from foodprep import operations as o
from foodprep import transfers as t
from foodprep.cli import main

ROOT = Path(__file__).resolve().parent.parent
R4 = ROOT / "docs/research/r4-transfers"


@pytest.fixture(scope="module")
def reports():
    return {tid: t.validate(tid) for tid in t.candidate_ids()}


def _sources() -> dict:
    out = {}
    for line in (R4 / "sources.md").read_text(encoding="utf-8").splitlines():
        m = re.match(r"^\| ([A-Z]\d+) \|.*?(https?://\S+)", line)
        if m:
            out[m.group(1)] = m.group(2)
    return out


def _cited(obj) -> set:
    """Every R4 evidence id cited anywhere in a candidate (evidence lists and the
    recipes of replaced specs)."""
    found = set()
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in ("evidence", "recipes") and isinstance(v, list):
                found |= {x for x in v if t.EVIDENCE_ID.match(str(x))}
            else:
                found |= _cited(v)
    elif isinstance(obj, list):
        for x in obj:
            found |= _cited(x)
    return found


# ---- the data -------------------------------------------------------------------------

def test_candidates_are_well_formed():
    for tid in t.candidate_ids():
        assert t.candidate_errors(tid) == [], tid


def test_the_brief_s_five_candidates_and_one_replacement():
    cands = t.load()["candidates"]
    bases = {(x["base"]["dish"], x["base"]["route"]) for x in cands.values()}
    for dish in ("falafel", "kaalikaaryleet", "gratin_dauphinois", "carrot_patties",
                 "zucchine_ripiene"):
        assert any(d == dish for d, _ in bases), dish
    assert cands["kale_rolls"]["replaced_by"] == "napa_cabbage_rolls"


def test_no_ranking_or_scoring():
    for tid, cand in t.load()["candidates"].items():
        assert not {"score", "rank", "rating", "priority"} & set(cand), tid


def test_transfers_are_not_documented_dishes():
    """A transfer is never added to constructions.yaml as a dish (R3 r4-needs)."""
    assert not set(t.candidate_ids()) & set(c.dish_ids())


def test_deriving_leaves_the_documented_dishes_untouched():
    before = copy.deepcopy(c.load()["dishes"])
    for tid in t.candidate_ids():
        t.derive(tid)
    assert c.load()["dishes"] == before


def test_every_cited_source_was_read_and_has_a_url():
    src = _sources()
    assert len(src) > 100
    for tid, cand in t.load()["candidates"].items():
        for sid in _cited(cand):
            assert sid in src, (tid, sid)


def test_the_validator_accepts_r4_ids_and_nothing_else(reports):
    src = _sources()
    for tid, rep in reports.items():
        assert set(rep.evidence_ids) <= set(src), (tid, set(rep.evidence_ids) - set(src))


def test_lidl_availability_is_recorded_per_candidate():
    for tid, cand in t.load()["candidates"].items():
        assert cand.get("lidl"), tid


# ---- the derived routes -----------------------------------------------------------------

def test_derived_routes_have_no_structural_errors(reports):
    for tid, rep in reports.items():
        assert rep.route is not None, tid
        assert rep.route.errors == [], (tid, rep.route.errors)
        assert rep.route.result is not None, tid


# What docs/research/r4-transfers/ reports (model-tables.md, after amendment A2).
MODEL = {
    "pea_falafel": (True, True),
    "kale_rolls": (False, None),           # evidence on curly kale is indirect
    "napa_cabbage_rolls": (True, True),
    "rutabaga_gratin": (True, True),
    "rutabaga_gratin_raw": (False, True),  # the control: fails, as in the kitchen (A2)
    "broccoli_stem_patties": (True, True),
    "onion_vessel": (True, True),
}


def test_model_verdicts_and_agreement_are_pinned(reports):
    assert {tid: (r.model_holds, r.agrees) for tid, r in reports.items()} == MODEL


def test_worth_cooking_means_the_model_holds_and_a_kitchen_test(reports):
    for tid, cand in t.load()["candidates"].items():
        if cand["verdict"] == "worth_cooking":
            assert reports[tid].model_holds, tid
            assert cand["status"] == "documented", tid
            assert cand["kitchen_test"]["stop_if"], tid


def test_pea_paste_holds_without_a_binder_because_it_sets_on_heat(reports):
    r = reports["pea_falafel"].route
    assert not any(s.status in ("inapplicable", "unsafe") for s in r.steps if not s.alternative)
    assert ("assembly paste (pea)", {"soaked": True, "cooked": False}, True) in r.claims
    paste = r.states["paste"]
    assert paste.props.get("sets_on_heat") and paste.props.get("cooked")


def test_curly_kale_fails_on_size_and_flat_kale_would_pass():
    """The model's verdict on Lidl's curly kale rests on one value this round set
    from the evidence (`piece: medium`); with a large flat leaf the same route
    passes. The model restates the evidence here; it does not test it."""
    rep = t.validate("kale_rolls").route
    assert any("kale as wrapper" in f and "large enough" in f for f in rep.failures)
    cat = o.load()
    parts = copy.deepcopy(cat.parts)
    parts["kale"]["leaves"]["piece"] = "large"
    flat = o.Catalogue(cat.operations, cat.scales, cat.default_false, cat.ordinary,
                       cat.functions, parts)
    assert t.validate("kale_rolls", flat).route.failures == []


def test_napa_leaves_come_off_raw_and_the_rib_returns_to_the_filling(reports):
    r = reports["napa_cabbage_rolls"].route
    first = [s for s in r.steps if s.owner == "napa"][0]
    assert first.op == "detacher_feuilles" and first.status == "applicable"
    assert ("napa", "equeuter", "ribs", "rib") in r.recombinations
    # white cabbage needs blanching before its leaves come off; napa does not
    head = o.start_materials("cabbage", "head")[0]
    assert o.assess("detacher_feuilles", head).status == "inapplicable"


def test_a2_rutabaga_must_be_blanched_in_a_gratin(reports):
    raw = reports["rutabaga_gratin_raw"].route
    assert raw.failures == ["assembly gratin: rutabaga as layer: softens more slowly than "
                            "the other layers in the same bake: blanch or cook it first"]
    ok = reports["rutabaga_gratin"].route
    assert ok.failures == []
    assert ("assembly gratin (potato)", {"starch": ">=high"}, True) in ok.claims


def test_a2_changes_no_documented_layer():
    """No R3 part is `cooks_slowly`, so every documented gratin and layered dish
    passes the new layer requirement (amendment A2: effect none)."""
    for d in c.dish_ids():
        for rid, r in c.validate(d).routes.items():
            assert not any("softens more slowly" in f for f in r.failures), (d, rid)
    assert "cooks_slowly" in o.load().default_false


def test_broccoli_stem_is_peeled_then_grated_and_not_squeezed(reports):
    r = reports["broccoli_stem_patties"].route
    ops = [s.op for s in r.steps if s.owner == "stem"]
    assert ops == ["eplucher", "raper"]
    assert r.states["stem"].props.get("water") == "medium"


def test_onion_shell_is_a_vessel_and_its_inside_returns(reports):
    r = reports["onion_vessel"].route
    assert ("vessel", "creuser", "flesh", "flesh") in r.recombinations
    assert ("final", {"cooked": True, "hollow": True, "filled": True}, True) in r.claims


def test_staged_transfer_parts_stay_out_of_the_family_generator():
    from foodprep import possibilities as po
    known = {i.ingredient for i in po.generate()}
    assert not {"dried_peas", "napa_cabbage", "rutabaga", "kale"} & known


# ---- output -------------------------------------------------------------------------------

def test_model_tables_are_current():
    """model-tables.md is generated by run.py; regenerate it after a data change."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("r4run", R4 / "run.py")
    run = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(run)
    current = (R4 / "model-tables.md").read_text(encoding="utf-8").replace("\r\n", "\n")
    assert current == run.write_tables()
    assert (R4 / "sources.md").read_text(encoding="utf-8").replace("\r\n", "\n") == \
        run.write_sources()


def test_cli(capsys):
    assert main(["transfer"]) == 0
    assert "rutabaga_gratin" in capsys.readouterr().out
    assert main(["transfer", "onion_vessel"]) == 0
    out = capsys.readouterr().out
    assert "recombination: vessel -> creuser [flesh] -> flesh" in out
    assert "kitchen test" in out
    assert main(["transfer", "no_such_transfer"]) == 1
