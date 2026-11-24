"""R3: documented constructions (docs/adr/0003-documented-constructions.md).

These tests say the recorded dishes are consistent with the operation model
and trace to R2's recipes. They say nothing about whether a dish tastes good:
every dish here is documented practice, not a hypothesis."""

from __future__ import annotations

import copy
import re
from pathlib import Path

import pytest

from foodprep import constructions as c
from foodprep import operations as o
from foodprep import pair_counts as pc
from foodprep import possibilities as po
from foodprep.cli import main

ROOT = Path(__file__).resolve().parent.parent
R2 = ROOT / "docs/research/r2-construction-patterns"


@pytest.fixture(scope="module")
def cat():
    return o.load()


@pytest.fixture(scope="module")
def reports(cat):
    return {d: c.validate(d, cat) for d in c.dish_ids()}


# ---- the data loads and is well formed ------------------------------------------

def test_dishes_and_additions_are_well_formed():
    assert c.addition_errors() == []
    for d in c.dish_ids():
        assert c.dish_errors(d) == [], d


def test_no_route_has_structural_errors(reports):
    for d, rep in reports.items():
        for rid, r in rep.routes.items():
            assert r.errors == [], (d, rid, r.errors)
            assert r.result is not None, (d, rid)


def test_design_set_has_about_three_dishes_per_pattern():
    data = c.load()
    design = c.dish_ids("design")
    assert len(design) == 27
    per = {p: set() for p in data["patterns"]}
    for d in design:
        for route in data["dishes"][d]["routes"].values():
            for p in route.get("patterns") or []:
                per[p].add(d)
    assert all(len(ds) >= 3 for ds in per.values()), {p: len(v) for p, v in per.items()}


# ---- expressiveness: pinned verdicts ----------------------------------------------

DESIGN_VERDICTS = {
    "latkes": "fully", "gamja_jeon": "fully", "rosti": "partly", "aloo_tikki": "fully",
    "arancini": "fully", "croquetas": "partly", "falafel": "fully", "medu_vada": "fully",
    "akara": "fully", "mucver": "fully", "carrot_patties": "partly",
    "onion_pakoda": "partly", "raggmunk": "fully", "okonomiyaki": "partly",
    "kakiage": "partly", "tortilla": "fully", "frittata": "partly",
    "porkkanalaatikko": "fully", "zucchine_ripiene": "fully", "kaalikaaryleet": "partly",
    "gemista": "partly", "gratin_dauphinois": "partly", "parmigiana": "partly",
    "kaalilaatikko": "partly", "tempura": "partly", "korokke": "fully", "hobak_jeon": "partly",
}


def test_design_verdicts_are_pinned(reports):
    """A change to the model or the data that moves a verdict must update this
    table and docs/research/r3-construction-modelling/validation.md together."""
    got = {d: reports[d].verdict for d in DESIGN_VERDICTS}
    assert got == DESIGN_VERDICTS


def test_partly_routes_say_why(reports):
    """Every route short of 'fully' carries a failure, an unknown property, an
    unaccounted fraction or a recorded model gap: nothing is partly by silence."""
    for d, rep in reports.items():
        for rid, r in rep.routes.items():
            if r.verdict == "partly":
                assert r.failures or r.unknowns or r.unaccounted or r.model_gaps, (d, rid)


def test_every_step_is_assessed_not_assumed(reports):
    for rep in reports.values():
        for r in rep.routes.values():
            assert r.steps
            for s in r.steps:
                assert s.status in o.STATUSES


# ---- what the representation must express -------------------------------------------

RECOMBINATIONS = {
    ("latkes", "settled_starch"): ("potato", "juice", "settled"),
    ("gamja_jeon", "own_starch"): ("potato", "liquid", "settled"),
    ("onion_pakoda", "own_juice"): ("onion", "vegetable_water", "juice"),
    ("hobak_jeon", "shredded_own_juice"): ("courgette", "vegetable_water", "juice"),
    ("zucchine_ripiene", "cooked_flesh"): ("courgette", "flesh", "flesh"),
    ("zucchine_ripiene", "blanched_flesh"): ("courgette", "flesh", "flesh"),
    ("kaalikaaryleet", "inner_leaves"): ("cabbage", "heart", "heart"),
    ("gemista", "oven_raw_rice"): ("tomato", "flesh", "pulp"),
    ("gemista", "pot_partly_cooked"): ("aubergine", "flesh", "aubergine_flesh"),
}


def test_recombination_is_derived(reports):
    """R2: scooped flesh, inner leaves, settled starch and salt-drawn juice go
    back into the same dish. The validator finds these links from the data."""
    for (d, rid), (src, out, mid) in RECOMBINATIONS.items():
        links = {(s, o_, m) for s, _, o_, m in reports[d].routes[rid].recombinations}
        assert (src, out, mid) in links, (d, rid, links)
    # E12b discards the heart that E12a returns: no recombination there
    assert reports["kaalikaaryleet"].routes["trimmed_rib"].recombinations == []


def test_nesting_and_structural_relations(reports):
    data = c.load()
    arancini = data["dishes"]["arancini"]["routes"]["arancini"]["assemblies"]
    assert arancini["ball"]["op"] == "envelopper" and arancini["ball"]["roles"]["wrapper"] == "rice_mass"
    assert arancini["coated"]["op"] == "revetir" and arancini["coated"]["roles"]["piece"] == "ball"
    relations = {asm["op"] for d in data["dishes"].values() for r in d["routes"].values()
                 for asm in (r.get("assemblies") or {}).values()}
    assert relations == set(c.assembly_ops())     # every join is used by some design dish


def test_moisture_heat_cooling_and_resting_are_recorded(reports):
    ops = {s.op for rep in reports.values() for r in rep.routes.values() for s in r.steps}
    assert {"degorger", "presser", "egoutter", "decanter"} <= ops        # removal
    assert {"tremper", "refroidir", "reposer"} <= ops                    # soak, cool, rest
    assert {"frire", "rissoler", "cuire_four", "cuire_anglaise", "mijoter"} <= ops
    data = c.load()
    waters = {w for d in data["dishes"].values() for r in d["routes"].values()
              for w in r.get("water") or []}
    assert waters == set(data["water_routes"])                           # all nine routes


def test_alternative_routes_to_one_dish(reports):
    for d in ("rosti", "gamja_jeon", "porkkanalaatikko", "kaalilaatikko", "gratin_dauphinois"):
        assert len(reports[d].routes) >= 2, d
    rosti = c.load()["dishes"]["rosti"]["routes"]
    assert rosti["raw"]["patterns"] == ["C1"] and rosti["boiled"]["patterns"] == ["C2"]


def test_claims_are_checked_against_computed_states(reports):
    claims = [x for rep in reports.values() for r in rep.routes.values() for x in r.claims]
    assert len(claims) > 40
    assert all(v is True for _, _, v in claims), [x for x in claims if x[2] is not True]
    # the courgette pulp of mücver is not a binder; the potato starch of latkes is
    mucver = reports["mucver"].routes["squeezed"].states["courgette"]
    latkes = reports["latkes"].routes["settled_starch"].states["settled"]
    assert not mucver.props.get("binder") and latkes.props["binder"] is True


# ---- the vocabulary changes behave as the ADR says -----------------------------------

def test_one_cooking_is_waived_only_for_assembled_materials(cat):
    boiled = o.apply("cuire_anglaise", o.start_materials("potato", "tuber", cat)[0], cat)[0]
    assert o.assess("frire", boiled, cat).status == "inapplicable"
    shaped = o.apply("faconner", boiled, cat)[0]
    assert shaped.props["assembled"] is True
    assert o.assess("rissoler", shaped, cat).status in o.TAKEN


def test_cooling_makes_cooked_starch_cohesive(cat):
    rice = o.start_materials("rice", "grain", cat)[0]
    cooked = o.apply("cuire_anglaise", rice, cat)[0]
    assert cooked.props["water"] == "medium"            # water uptake
    cooled = o.apply("refroidir", cooked, cat)[0]
    assert cooled.props["cooled"] is True and cooled.props["cohesive"] is True
    carrot = o.apply("cuire_anglaise", o.start_materials("carrot", "root", cat)[0], cat)[0]
    assert not o.apply("refroidir", carrot, cat)[0].props.get("cohesive")


def test_raw_pulse_paste_fries_but_a_puree_does_not(cat):
    soaked = o.apply("tremper", o.start_materials("chickpea", "dried_seed", cat)[0], cat)[0]
    paste = o.apply("mixer", soaked, cat)[0]
    assert paste.props["smooth"] is True
    assert o.assess("frire", paste, cat).status in o.TAKEN
    puree = o.apply("mixer", o.start_materials("avocado", "flesh", cat)[0], cat)[0]
    assert o.assess("frire", puree, cat).status == "inapplicable"


def test_construction_operations_stay_outside_the_generator(cat):
    new = ["tremper", "refroidir", "reposer", "creuser", "fendre", "decortiquer",
           "detacher_feuilles", "faconner", *c.assembly_ops(cat)]
    for op in new:
        assert cat.operations[op].get("generator") is False, op
    ex = o.explore("courgette", "fruit", depth=2, cat=cat)
    used = {s.operation for r in ex.results for s in r.path}
    assert not used & set(new)
    for op in ("decanter", "egoutter", "foisonner"):
        assert cat.operations[op].get("generator") is False


def test_staged_parts_are_invisible_to_the_family_generator(cat):
    staged = pc.load_yaml(o.DATA / "part_properties.yaml")["staged_parts"]
    assert set(staged) & set(po.load_tables().parts) == set()
    assert set(staged) <= set(cat.parts)


def test_role_requirements_name_known_properties(cat):
    known = set(cat.default_false) | {"piece", "shape", "cut"}
    for ps in cat.parts.values():
        for p in ps.values():
            known |= set(p)
    for a in c.load()["additions"].values():
        known |= set(a.get("props") or {})
    for name, op in c.assembly_ops(cat).items():
        assert op["assembly"]["carrier"] in op["assembly"]["roles"], name
        for role, spec in op["assembly"]["roles"].items():
            for key in (spec.get("requires") or {}):
                assert key in known, (name, role, key)


# ---- traceability --------------------------------------------------------------------

def _r2_ids() -> tuple[set, set]:
    text = (R2 / "recipes.md").read_text(encoding="utf-8")
    heads = set(re.findall(r"^### ([EMA]\d+[a-z])\.", text, re.M))
    with_url = set()
    same_page = {}
    for m in re.finditer(r"^### ([EMA]\d+[a-z])\..*?(?=^### |\Z)", text, re.M | re.S):
        if "URL:" in m.group(0):
            with_url.add(m.group(1))
        ref = re.search(r"on the .{0,40}page of (\d+[a-z])", m.group(0).splitlines()[0])
        if ref:                     # e.g. M2c is on the page of M1a (stated in its heading)
            same_page[m.group(1)] = m.group(1)[0] + ref.group(1)
    src = (R2 / "sources.md").read_text(encoding="utf-8")
    for region, used in re.findall(r"^\| ([EMA])-\d+ \| https?://\S+ \|[^|]*\|([^|]*)\|", src, re.M):
        for bare in re.findall(r"\d+[a-z]", used):
            with_url.add(region + bare)
    with_url |= {k for k, v in same_page.items() if v in with_url}
    return heads, with_url


def _cited() -> set:
    ids = set()

    def walk(x):
        if isinstance(x, dict):
            for k, v in x.items():
                if k in ("recipes", "documented_in"):
                    ids.update(v or [])
                else:
                    walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)
    walk(c.load()["dishes"])
    walk({k: v.get("documented_in") and {"documented_in": v["documented_in"]}
          for k, v in o.load().operations.items()})
    return ids


def test_every_cited_recipe_exists_in_r2_with_a_url():
    heads, with_url = _r2_ids()
    cited = _cited()
    assert cited, "nothing cited"
    assert cited <= heads, sorted(cited - heads)
    assert cited <= with_url, sorted(cited - with_url)


def test_every_relationship_cites_recipes():
    data = c.load()
    for d, dish in data["dishes"].items():
        for rid, r in dish["routes"].items():
            assert r["recipes"], (d, rid)
            for name, m in (r.get("materials") or {}).items():
                assert m.get("recipes"), (d, rid, name)
            for name, a in (r.get("assemblies") or {}).items():
                assert a.get("recipes"), (d, rid, name)
            assert r["final"].get("recipes"), (d, rid)


def test_held_out_recipes_are_not_cited_by_design_dishes():
    """The held-out dishes' recipe ids (dish-selection.md) appear in no design
    dish and in no operation's documented_in written before the freeze."""
    held = {"E5a", "E5b", "E5c", "M4a", "M4b", "A8a", "M16a", "M16b", "E16a", "E16b",
            "M8a", "M8b", "A12a", "A12b", "A19a", "A19b"}
    data = c.load()
    design_ids = set()
    for d in c.dish_ids("design"):
        for r in data["dishes"][d]["routes"].values():
            design_ids |= set(r["recipes"])
    assert not design_ids & held
    ops_ids = {r for op in o.load().operations.values() for r in op.get("documented_in") or []}
    assert not ops_ids & held


# ---- the validator catches what it should --------------------------------------------

def _mutated(dish: str, route: str, edit) -> c.RouteReport:
    data = copy.deepcopy(c.load())
    edit(data["dishes"][dish]["routes"][route])
    return c.validate_route(dish, route, data=data)


def test_validator_reports_unknown_operations_and_missing_citations():
    r = _mutated("latkes", "settled_starch",
                 lambda rt: rt["materials"]["onion"]["steps"].append("flamber"))
    assert any("unknown operation" in e for e in r.errors) and r.verdict == "not"
    r = _mutated("latkes", "settled_starch", lambda rt: rt["assemblies"]["mass"].pop("recipes"))
    assert any("no recipe ids" in e for e in r.errors)
    r = _mutated("latkes", "settled_starch",
                 lambda rt: rt["assemblies"]["mass"].update(recipes=["E4a", "M17a"]))
    assert any("does not list" in e for e in r.errors)


def test_validator_reports_a_false_claim():
    def edit(rt):
        rt["assemblies"]["mass"]["expects"][1]["state"] = {"cooked": True}
    r = _mutated("latkes", "settled_starch", edit)
    assert r.verdict == "partly" and any("computed state disagrees" in f for f in r.failures)


def test_validator_reports_an_inapplicable_step():
    # hollowing a cut courgette: creuser needs a whole piece or a half
    def edit(rt):
        rt["materials"]["courgette"]["steps"].insert(1, "rondelles")
    r = _mutated("zucchine_ripiene", "cooked_flesh", edit)
    assert any("inapplicable" in f for f in r.failures)


def test_validator_reports_an_unaccounted_fraction():
    def edit(rt):
        rt["materials"]["courgette"]["steps"][1].pop("discard")
    r = _mutated("mucver", "squeezed", edit)
    assert r.unaccounted == ["courgette: presser [juice]"]
    # a fraction the model marks usually_discarded (the clear liquid) is not reported
    def edit2(rt):
        rt["materials"]["settled"]["steps"][0].pop("discard")
    r = _mutated("latkes", "settled_starch", edit2)
    assert r.unaccounted == [] and "settled: decanter [clear]" in r.conventional


def test_validator_reports_a_wrong_role():
    def edit(rt):
        rt["assemblies"]["mass"]["roles"]["coagulant"] = "milk"
    r = _mutated("mucver", "squeezed", edit)
    assert any("milk as coagulant" in f for f in r.failures)
    def edit2(rt):
        rt["assemblies"]["mass"]["roles"]["dry_phase"] = "milk"
    r = _mutated("mucver", "squeezed", edit2)
    assert any("milk as dry_phase: water_uptake unknown" in u for u in r.unknowns)


def test_unknown_fields_are_errors():
    r = _mutated("latkes", "settled_starch",
                 lambda rt: rt["assemblies"]["mass"].update(quantity="4 potatoes"))
    assert any("unknown assembly field" in e for e in r.errors)


# ---- PR #7 review: recombination needs two routes; edibility is checked at joins --------

def test_extraction_alone_is_not_recombination():
    """Potato pressed and only its settled juice used: the potato never enters
    the dish by its own route, so this is extraction, not recombination."""
    def edit(rt):
        mass = rt["assemblies"]["mass"]
        mass["roles"]["body"] = "onion"                          # the pulp no longer enters
        mass["roles"]["flavour"] = ["salt", "spices"]
        mass["expects"] = [e for e in mass["expects"] if e.get("member") != "potato"]
    r = _mutated("latkes", "settled_starch", edit)
    assert r.errors == []
    assert r.recombinations == []


def test_pulp_and_its_own_starch_together_are_recombination():
    r = c.validate_route("latkes", "settled_starch")
    assert [(s, o_, m) for s, _, o_, m in r.recombinations] == [("potato", "juice", "settled")]


def test_recombination_through_an_intermediate_material():
    """potato -> juice (an intermediate that never enters the dish) -> settled
    starch, with the pulp in the mass: the link is found through the
    intermediate, back to the potato."""
    def edit(rt):
        mats = rt["materials"]
        mats["juice"] = {"from": {"material": "potato", "step": "presser", "output": "juice"},
                         "recipes": ["E4a"],
                         "steps": [{"op": "decanter", "keep": "clear"}]}
        mats["settled"] = {"from": {"material": "juice", "step": "decanter", "output": "settled"},
                           "recipes": ["E4a"]}
    r = _mutated("latkes", "settled_starch", edit)
    assert r.errors == []
    assert [(s, m) for s, _, _, m in r.recombinations] == [("potato", "settled")]


def test_a_non_food_member_makes_the_join_inedible():
    """An edible shell must not make a filling with a non-food member look
    edible (avocado stone: R1 says not established as safe, so unsafe)."""
    def edit(rt):
        rt["materials"]["stone"] = {"from": "avocado.stone", "recipes": ["M17a"]}
        rt["assemblies"]["filling"]["roles"]["flavour"].append("stone")
    r = _mutated("zucchine_ripiene", "cooked_flesh", edit)
    assert r.verdict != "fully"
    assert any("stone" in f and "not food" in f for f in r.failures)
    assert r.states["filling"].edible == "no"
    assert r.states["stuffed"].edible == "no"             # the edible shell does not hide it
    bake = [s for s in r.steps if s.owner == "stuffed" and s.op == "cuire_four"][0]
    assert bake.status == "unsafe"


def test_an_inedible_member_makes_the_join_inapplicable():
    def edit(rt):
        rt["materials"]["skin"] = {"from": "avocado.skin", "recipes": ["M17a"]}
        rt["assemblies"]["filling"]["roles"]["flavour"].append("skin")
    r = _mutated("zucchine_ripiene", "cooked_flesh", edit)
    assert any("skin" in f and "not food" in f for f in r.failures)
    bake = [s for s in r.steps if s.owner == "stuffed" and s.op == "cuire_four"][0]
    assert bake.status == "inapplicable"


def test_no_documented_dish_has_a_non_food_member(reports):
    for d, rep in reports.items():
        for rid, r in rep.routes.items():
            assert r.result.edible != "no", (d, rid)
            assert not any("not food" in f for f in r.failures), (d, rid)


# ---- the freeze ------------------------------------------------------------------------

AMENDMENT_KEYS = {"code", "schema", "vocabulary", "catalogue", "operations"}


def _amendments() -> dict:
    return pc.load_yaml(c.FREEZE_PATH.with_name("construction_freeze_amendments.yaml"))


def _effective_freeze() -> dict:
    """The original R3 manifest plus each documented amendment, in order."""
    frozen = copy.deepcopy(pc.load_yaml(c.FREEZE_PATH))
    for a in _amendments()["amendments"]:
        for key in set(a) & AMENDMENT_KEYS:
            frozen[key] = {**frozen[key], **a[key]}
    return frozen


def test_the_original_freeze_manifest_is_preserved():
    """construction_freeze.yaml is the record of the experiment (e8a2e54): its
    bytes must not change. Corrections go into the amendments file."""
    import hashlib
    raw = c.FREEZE_PATH.read_bytes().replace(b"\r\n", b"\n")
    assert hashlib.sha256(raw).hexdigest() == _amendments()["original_manifest_sha256"]


def test_freeze_amendments_are_documented():
    ids = []
    for a in _amendments()["amendments"]:
        assert {"id", "date", "reason", "changed", "effect"} <= set(a), a.get("id")
        assert re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(a["date"])), a["id"]
        assert set(a) - {"id", "date", "reason", "changed", "effect"} <= AMENDMENT_KEYS, a["id"]
        ids.append(a["id"])
    assert len(ids) == len(set(ids))


def test_held_out_dishes_rely_on_nothing_changed_after_the_freeze():
    """The schema was frozen before the held-out dishes were represented
    (construction_freeze.yaml, written by the R3 run script). A held-out dish
    may use only operations whose definition is unchanged since the freeze,
    property keys that existed at the freeze, and the frozen schema and code.
    Adding new parts or additions with existing keys is data, and allowed.

    The original manifest is never rewritten: later corrections are documented
    amendments (construction_freeze_amendments.yaml), applied on top of it."""
    frozen = _effective_freeze()
    now = c.freeze_manifest()
    assert now["schema"] == frozen["schema"]
    assert now["vocabulary"] == frozen["vocabulary"]
    assert now["code"] == frozen["code"],         "constructions.py or operations.py changed after the freeze without a documented amendment"
    assert now["catalogue"] == frozen["catalogue"]
    held = c.dish_ids("held_out")
    assert set(held) == set(frozen["held_out"]), "the held-out set is the one recorded before design"
    for d in held:
        used = c.used_by(d)
        for op in used["operations"]:
            assert op in frozen["operations"], (d, op, "operation added after the freeze")
            assert now["operations"][op] == frozen["operations"][op], (d, op, "changed after the freeze")
        new_keys = set(used["property_keys"]) - set(frozen["property_keys"])
        assert not new_keys, (d, new_keys)


HELD_OUT_VERDICTS = {
    "draniki": "fully", "kolokythokeftedes": "fully", "chawanmushi": "partly",
    "farcis_nicois": "partly", "pierogi_ruskie": "partly", "spanakopita": "partly",
    "zha_qie_he": "partly", "moi_moi": "partly",
}


def test_held_out_verdicts_are_pinned(reports):
    """Step 4 results (generalisation.md). A held-out dish that later fits
    better because the model changed is progress, but it is no longer evidence
    of generalisation: record why when this table changes."""
    assert {d: reports[d].verdict for d in HELD_OUT_VERDICTS} == HELD_OUT_VERDICTS


def test_held_out_failures_point_at_missing_structure(reports):
    """Each held-out failure is a specific operation or role that would need a
    change after the freeze; none is malformed data."""
    fails = {(d, rid): r.failures for d in HELD_OUT_VERDICTS
             for rid, r in reports[d].routes.items() if r.failures}
    assert set(fails) == {("chawanmushi", "steamed_custard"), ("farcis_nicois", "vegetarian"),
                          ("zha_qie_he", "egg_starch_coat"), ("zha_qie_he", "double_fried"),
                          ("moi_moi", "steamed")}
    assert any("cuire_vapeur" in f and "steams a solid" in f
               for f in fails[("chawanmushi", "steamed_custard")])
    assert any("cuire_vapeur" in f and "tender enough" in f for f in fails[("moi_moi", "steamed")])
    assert any("a hollow to fill" in f for f in fails[("zha_qie_he", "double_fried")])


# ---- CLI ---------------------------------------------------------------------------------

def test_cli(capsys):
    assert main(["construction"]) == 0
    assert "zucchine_ripiene" in capsys.readouterr().out
    assert main(["construction", "zucchine_ripiene"]) == 0
    out = capsys.readouterr().out
    assert "recombination: courgette -> creuser [flesh]" in out
    assert main(["construction", "no_such_dish"]) == 1
