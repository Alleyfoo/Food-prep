"""R5: documented processing conditions (docs/research/r5-processing-conditions/).

The data records what documented practice says a step needs (conditions, time
as elapsed and active work, how you know it is done or failed), step by step
through whole documented routes. These tests say the data is well formed and
cited, that every worth-cooking R4 transfer is recorded raw to plate with
readiness and doneness kept apart, that nothing is derived or ranked, that the
"from this state" query reuses R1's state equivalence, and that reading the R3
and R4 data changes nothing in it. They do not say any time is right: that is
the kitchen's job."""

from __future__ import annotations

import copy
import importlib.util
from pathlib import Path

import pytest

from foodprep import conditions as k
from foodprep import constructions as c
from foodprep import operations as o
from foodprep import transfers as t
from foodprep.cli import main

ROOT = Path(__file__).resolve().parent.parent
R5 = ROOT / "docs/research/r5-processing-conditions"
WORTH_COOKING = ["rutabaga_gratin", "onion_vessel", "napa_cabbage_rolls", "pea_falafel",
                 "broccoli_stem_patties"]
KITCHEN_TEST_BASES = ["gratin_dauphinois/raw_long_bake", "zucchine_ripiene/blanched_flesh",
                      "kaalikaaryleet/trimmed_rib", "falafel/raw_soaked", "carrot_patties/crumbs"]
AUTHORITIES = ("ruokavirasto.fi", "livsmedelsverket.se", "mattilsynet.no", "gov.uk",
               "foodstandards.gov.scot", "nhs.uk", "bfr.bund.de", "fsai.ie",
               "extension.colostate.edu", "ndsu.edu")


# ---- the data -------------------------------------------------------------------------

def test_data_is_well_formed_and_every_source_resolves():
    assert k.evidence_index() is not None, "the research documents are next to the package"
    assert k.errors() == []


def test_between_15_and_25_pairs_each_on_a_documented_step():
    pairs = k.load()["pairs"]
    assert 15 <= len(pairs) <= 25
    for pid, p in pairs.items():
        assert p["steps"], pid
        for addr in p["steps"]:
            assert k.resolve_step(addr) is not None, (pid, addr)


def test_r5_sources_were_read():
    idx = k.evidence_index()
    cited = {s for s in k._source_ids(k.load()) if s.startswith("Q")}
    assert len(cited) >= 100
    assert cited <= set(idx)
    for sid in cited:
        assert idx[sid].startswith("http"), sid


def test_no_scoring_ranking_or_prediction_anywhere():
    def walk(obj, where="data"):
        if isinstance(obj, dict):
            assert not k.FORBIDDEN & {str(x) for x in obj}, where
            for key, v in obj.items():
                walk(v, f"{where}.{key}")
        elif isinstance(obj, list):
            for i, v in enumerate(obj):
                walk(v, f"{where}[{i}]")
    walk(k.load())


def test_every_time_and_endpoint_is_cited():
    """Nothing is derived: a time, a check or a keeping time always has sources
    (errors() enforces it; this says it once, plainly)."""
    def walk(obj):
        if isinstance(obj, dict):
            if "check" in obj or ("unit" in obj and ("min" in obj or "max" in obj)):
                assert obj.get("sources"), obj
            for v in obj.values():
                walk(v)
        elif isinstance(obj, list):
            for v in obj:
                walk(v)
    walk(k.load())


def test_conflicts_are_kept_as_versions_not_averaged():
    n = 0
    for pid, p in k.load()["pairs"].items():
        for cf in p.get("conflicts") or []:
            n += 1
            assert len(cf["versions"]) >= 2, pid
            says = [v["says"] for v in cf["versions"]]
            assert len(set(says)) == len(says), pid
    assert n >= 20


def test_active_work_is_a_kind_apart_from_elapsed_time():
    soak = k.for_step("transfer:pea_falafel/pea/1")[0]["fields"]
    assert soak["active"]["kind"] == "none"
    assert any(e.get("label") == "overnight" or e.get("unit") == "h" for e in soak["elapsed"])
    fry = k.for_step("falafel/raw_soaked/paste/3")[0]["fields"]
    assert fry["active"]["kind"] == "regular"
    assert all(e.get("unit") != "h" for e in fry["elapsed"])


def test_a_step_s_fields_replace_the_pair_default_at_that_step():
    rice = k.step_fields("transfer:napa_cabbage_rolls/rice/1")
    assert "al dente" in rice["completion"][0]["check"]
    arancini = k.step_fields("arancini/arancini/rice/1")
    assert "overcooking" in arancini["completion"][0]["check"]


# ---- sequences: whole routes ------------------------------------------------------------

def test_every_worth_cooking_transfer_is_a_whole_sequence():
    seqs = k.load()["sequences"]
    worth = [tid for tid, x in t.load()["candidates"].items() if x["verdict"] == "worth_cooking"]
    assert sorted(worth) == sorted(WORTH_COOKING)
    for tid in WORTH_COOKING + KITCHEN_TEST_BASES:
        key = tid if "/" in tid else f"transfer:{tid}"
        assert key in seqs, key
        steps = seqs[key]["steps"]
        assert {p.address for p in k.routes()[key].points} == set(steps), key


def test_every_step_says_readiness_or_doneness_and_something_reaches_the_plate():
    for key, seq in k.load()["sequences"].items():
        kinds = [s["endpoint"]["kind"] for s in seq["steps"].values()]
        assert set(kinds) <= {"readiness", "doneness"}, key
        assert "doneness" in kinds, key
        last = k.routes()[key].points[-1]
        assert seq["steps"][last.address]["endpoint"]["kind"] == "doneness", key


def test_blanched_rutabaga_is_readiness_and_the_bake_is_doneness():
    assert k.endpoint_kind("transfer:rutabaga_gratin/rutabaga/3") == "readiness"
    assert k.endpoint_kind("transfer:rutabaga_gratin/gratin/1") == "doneness"
    hist = {h.member: h for h in k.histories("transfer:rutabaga_gratin")}
    ops = [p.op for p, *_ in hist["rutabaga"].lines]
    assert ops == ["eplucher", "emincer", "blanchir", "cuire_four"], \
        "the rutabaga is blanched AND baked before the plate"
    *_, mine = hist["rutabaga"].lines[-1]
    assert mine["completion"] and mine["failure"]


def test_every_member_has_an_endpoint_after_the_join():
    cat = o.load()
    for key, seq in k.load()["sequences"].items():
        r = k.routes()[key]
        mats = r.spec.get("materials") or {}
        for p in r.points:
            if p.kind == "assembly" and k._is_heat(p.op, cat):
                got = seq["members"][p.address]
                for m in k.subtree(r, p.owner):
                    if m in mats:
                        assert m in got, (key, p.address, m)


def test_documented_dependencies_point_forward():
    deps = k.load()["sequences"]["transfer:rutabaga_gratin"]["depends"]
    assert any(d["step"].endswith("rutabaga/3") and d["because"].endswith("gratin/1")
               for d in deps)
    for key, seq in k.load()["sequences"].items():
        for d in seq.get("depends") or []:
            assert k._feeds(k.routes()[key], d["step"], d["because"]), (key, d)


def test_skipped_and_overdone_stages_have_failures():
    misses = {(m["step"], m["when"]) for s in k.load()["sequences"].values()
              for m in s.get("misses") or []}
    assert ("transfer:rutabaga_gratin/rutabaga/3", "skipped") in misses
    assert ("transfer:onion_vessel/vessel/2", "overdone") in misses
    assert ("falafel/raw_soaked/chickpea/1", "overdone") in misses


def test_alternative_sequences_are_kept_apart():
    alts = k.load()["sequences"]["transfer:rutabaga_gratin"]["alternatives"]
    assert len(alts) >= 3
    assert any(a.get("route") == "transfer:rutabaga_gratin_raw" for a in alts)


# ---- intermediate states ---------------------------------------------------------------

def test_from_soaked_peas_the_rest_of_the_falafel():
    res = k.from_state("dried_peas.dried_seed", ["tremper"])
    assert [m.route for m in res.matches] == ["transfer:pea_falafel"]
    mt = res.matches[0]
    assert mt.kind == "readiness"
    assert [p.op for p in mt.remaining] == ["broyer", "reposer", "faconner", "frire"]


def test_from_blanched_rutabaga_the_bake_remains_and_it_is_not_ready_to_eat():
    res = k.from_state("rutabaga.root", ["eplucher", "emincer", "blanchir"])
    mt = res.matches[0]
    assert mt.route == "transfer:rutabaga_gratin" and mt.kind == "readiness"
    assert [p.op for p in mt.remaining] == ["cuire_four"]
    assert res.keeps
    out = k.render_from("rutabaga.root", ["eplucher", "emincer", "blanchir"])
    assert "not ready to eat" in out and "rutabaga inside" in out


def test_equivalence_is_r1_material_key():
    """Grated and salted courgette meets kolokythokeftedes; grated and squeezed
    without salt (mucver) is a different material."""
    salted = k.from_state("courgette.fruit", ["raper", "degorger"])
    assert "kolokythokeftedes/baked" in {m.route for m in salted.matches}
    assert "mucver/squeezed" not in {m.route for m in salted.matches}
    assert salted.state.key() == o.apply("degorger", o.apply(
        "raper", o.start_materials("courgette", "fruit")[0])[0])[0].key()


def test_state_flags_and_step_addresses():
    res = k.from_state("chickpea.dried_seed", ["soaked"])
    assert res.matches and res.matches[0].at == 1
    paste = k.from_state("falafel/raw_soaked/paste/1")
    assert [p.op for p in paste.matches[0].remaining] == ["faconner", "frire"]
    assert any(iid == "rested_falafel_paste" for iid, _ in paste.keeps)
    assert k.from_state("nothing.here").problems


def test_food_safety_keeping_times_come_from_public_bodies():
    idx = k.evidence_index()
    n = 0
    for iid, it in k.load()["intermediates"].items():
        for kp in it.get("keeps") or []:
            if kp["basis"] == "food_safety":
                n += 1
                for sid in kp["sources"]:
                    assert any(d in idx[sid] for d in AUTHORITIES), (iid, sid, idx[sid])
    assert n >= 10


# ---- nothing frozen changes ---------------------------------------------------------------

def test_reading_routes_changes_no_r3_or_r4_data():
    before_c = copy.deepcopy(c.load())
    before_t = copy.deepcopy(t.load())
    k.routes.cache_clear()
    k.routes()
    for key in k.load()["sequences"]:
        k.render_sequence(key)
    assert c.load() == before_c
    assert t.load() == before_t


def test_r3_and_r4_code_and_data_are_not_touched_by_this_module():
    src = (ROOT / "src/foodprep/conditions.py").read_text(encoding="utf-8")
    for name in ("write_text", "open(", "yaml.dump", "safe_dump"):
        assert name not in src


# ---- generated documents and CLI -----------------------------------------------------------

def test_generated_tables_are_current():
    spec = importlib.util.spec_from_file_location("r5run", R5 / "run.py")
    run = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(run)
    assert (R5 / "sources.md").read_text(encoding="utf-8") == run.write_sources()
    assert (R5 / "condition-tables.md").read_text(encoding="utf-8") == run.write_tables()
    assert (R5 / "intermediate-tables.md").read_text(encoding="utf-8") == \
        run.write_intermediates()
    assert (R5 / "sequence-tables.md").read_text(encoding="utf-8") == run.write_sequences()


@pytest.mark.parametrize("argv, expect", [
    (["conditions"], "soak_dried_peas"),
    (["conditions", "blanch_rutabaga"], "crisp-tender"),
    (["conditions", "transfer:rutabaga_gratin"], "raw to plate"),
    (["conditions", "dried_peas"], "Soaking dried peas"),
    (["conditions", "transfer:pea_falafel/pea/1"], "soak_dried_peas"),
    (["from", "dried_peas.dried_seed", "tremper"], "not ready to eat"),
    (["from", "falafel/raw_soaked/paste/1"], "deep-fry"),
])
def test_cli(capsys, argv, expect):
    assert main(argv) == 0
    assert expect in capsys.readouterr().out


def test_cli_unknown(capsys):
    assert main(["conditions", "no_such_thing"]) == 1
    assert main(["from", "nothing.here"]) == 1
