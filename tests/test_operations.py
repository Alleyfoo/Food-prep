"""Culinary Operations R1: the operation catalogue, applicability, outputs and
bounded sequences. Passing these tests says the model is consistent; it says
nothing about whether a generated preparation tastes good."""

from __future__ import annotations

import re

import pytest

from foodprep import operations as o
from foodprep import pair_counts as pc
from foodprep import possibilities as po
from foodprep.cli import main


@pytest.fixture(scope="module")
def cat():
    return o.load()


def start(ing, part, cat):
    [m] = o.start_materials(ing, part, cat)
    return m


def out(op, m, name=None):
    outs = o.apply(op, m)
    return outs if name is None else next(x for x in outs if x.path[-1].output == name)


# ---- the catalogue ------------------------------------------------------------

def test_operation_ids_are_unique_and_canonical(cat):
    text = (o.DATA / "operations.yaml").read_text(encoding="utf-8")
    ids = re.findall(r"^  ([a-z_]+):\n    fr:", text, re.M)
    assert len(ids) == len(set(ids)) == len(cat.operations)
    assert all(re.fullmatch(r"[a-z_]+", i) for i in ids)


def test_catalogue_covers_the_briefs_operations(cat):
    for op in ["julienne", "brunoise", "batonnet", "macedoine", "paysanne", "chiffonade",
               "tourner", "rondelles", "emincer", "hacher", "ciseler", "concasser", "raper",
               "rubans", "quartiers", "troncons", "inciser", "eplucher", "peler", "monder",
               "parer", "epepiner", "evider", "equeuter", "ecosser", "denoyauter", "zester",
               "lever_supremes", "detailler_bouquets", "effeuiller", "egrainer", "presser",
               "filtrer", "tamiser", "passer_chinois", "fouler", "degorger", "egoutter",
               "clarifier", "ecumer", "decanter", "infuser", "decocter", "ecraser",
               "reduire_puree", "mixer", "broyer", "piler", "emietter", "moudre", "abaisser",
               "laminer", "malaxer", "fouetter", "foisonner", "emulsionner", "blanchir",
               "cuire_vapeur", "pocher", "etuver", "suer", "sauter", "rissoler", "rotir",
               "griller", "frire", "braiser", "glacer", "gratiner", "confire", "reduire",
               "dessecher", "deshydrater", "torrefier", "caramelliser", "fumer", "mariner",
               "macerer", "saumurer", "fermenter", "acidifier", "gelifier", "lier",
               "monter_beurre", "enrober", "paner", "deglacer"]:
        assert op in cat.operations, op


def test_every_operation_has_the_model_fields(cat):
    for name, op in cat.operations.items():
        for f in ("fr", "en", "categories", "requires", "evidence", "confidence"):
            assert f in op, (name, f)
        assert set(op["categories"]) <= {"geometry", "separation", "extraction",
                                         "mechanical", "thermal", "chemical"}, name
        if op.get("generator", True) is False:
            assert op.get("not_generated_because"), name
        else:
            assert op.get("outputs"), name


def test_evidence_ids_are_listed_in_sources(cat):
    sources = (o.DATA.parent.parent.parent / "docs/research/r1-culinary-operations/sources.md")
    text = sources.read_text(encoding="utf-8")
    listed = set(re.findall(r"^\| `([a-z0-9_]+)` \|", text, re.M))
    used = {e for op in cat.operations.values() for e in op["evidence"]}
    assert used <= listed, used - listed


def test_operations_link_to_existing_techniques_and_preparations(cat):
    data = pc.load_yaml(o.DATA / "tomato.yaml")
    techs = {t["name"] for t in data["techniques"]}
    preps = {p["id"] for p in pc.load_yaml(o.DATA / "vocabularies.yaml")["preparations"]}
    linked = set()
    for name, op in cat.operations.items():
        if op.get("technique"):
            assert op["technique"] in techs, name
            linked.add(op["technique"])
        if op.get("preparation"):
            assert op["preparation"] in preps, name
    unlinked = pc.load_yaml(o.DATA / "operations.yaml")["unlinked_techniques"]
    assert techs <= linked | set(unlinked), techs - linked - set(unlinked)


def test_requirements_name_known_properties(cat):
    known = set()
    for ps in cat.parts.values():
        for p in ps.values():
            known |= set(p)
            for layer in ("outer_layer", "seed_core"):
                known |= set(p.get(layer) or {})
    known |= set(cat.default_false) | {"outer_layer_toughness", "piece", "shape", "form",
                                       "concentrated", "cut"}
    for name, op in cat.operations.items():
        for key in (op.get("requires") or {}):
            assert key in known, (name, key)


def test_family_generator_output_is_unchanged_by_the_move():
    """The family generator read technique_rules.yaml before R1 and reads the
    family states of operations.yaml now. For the three ingredients it knew,
    its output must be identical (fingerprint taken from the pre-R1 output:
    2,236 ideas). If a deliberate change breaks this, update the fingerprint
    and say why in the commit."""
    import hashlib
    import json
    old = [[i.ingredient, i.part, i.technique, i.family, i.member, i.form,
            list(i.mechanisms), i.label]
           for i in po.generate() if i.ingredient in ("broccoli", "tomato", "avocado")]
    assert len(old) == 2236
    assert hashlib.sha256(json.dumps(old).encode()).hexdigest() == \
        "2021d4a0f70725d5039ff7cb0b095d3492964400af43e4db1023884d57526e16"


def test_family_generator_reads_the_same_rules(cat):
    fam = po.family_techniques()
    data = pc.load_yaml(o.DATA / "operations.yaml")
    assert list(fam) == data["family_states"]
    assert not (o.DATA / "technique_rules.yaml").exists()


# ---- applicability --------------------------------------------------------------

def test_julienne_on_carrot_is_applicable_and_explained(cat):
    a = o.assess("julienne", start("carrot", "root", cat))
    assert a.status == "applicable"
    assert "firm enough to hold a narrow strip" in a.explain()


def test_chiffonade_needs_a_rollable_leaf(cat):
    assert o.assess("chiffonade", start("broccoli", "florets", cat)).status == "inapplicable"
    assert o.assess("chiffonade", start("broccoli", "leaves", cat)).status == "applicable"
    feathery = o.assess("chiffonade", start("carrot", "greens", cat))
    assert feathery.status == "inapplicable"
    assert "continuous sheet" in feathery.explain()


def test_tough_peel_makes_cutting_conditional(cat):
    a = o.assess("julienne", start("broccoli", "stems", cat))
    assert a.status == "conditional" and "peel first" in a.explain()


def test_unknown_property_is_not_false(cat):
    bare = o.Material("x", "y", {"liquid": False})          # firmness, shape, piece unknown
    a = o.assess("julienne", bare)
    assert a.status == "unknown"
    assert {"firmness", "shape", "piece"} <= set(a.unknown)
    assert o.holds(bare, {"firmness": ">=low"}) is None


def test_recorded_only_when_true_flags_default_to_false(cat):
    bare = o.Material("x", "y", {})
    assert o.value(bare, "leafy") == (True, False)
    assert o.value(bare, "firmness") == (False, None)


def test_parts_that_are_not_food(cat):
    stone = start("avocado", "stone", cat)
    skin = start("avocado", "skin", cat)
    assert {o.assess(k, stone).status for k in cat.operations} == {"unsafe"}
    assert {o.assess(k, skin).status for k in cat.operations} == {"inapplicable"}


def test_unsafe_when_blocks_drying_fat_rich_flesh(cat):
    a = o.assess("deshydrater", out("emincer", start("avocado", "flesh", cat))[0])
    assert a.status == "unsafe" and "rancid" in a.explain()


def test_long_heat_is_inapplicable_to_avocado(cat):
    av = start("avocado", "flesh", cat)
    assert o.assess("braiser", av).status == "inapplicable"
    assert o.assess("griller", av).status == "applicable"


def test_seed_core_condition_makes_hollowing_conditional(cat):
    a = o.assess("evider", start("courgette", "fruit", cat))
    assert a.status == "conditional" and "large courgettes" in a.explain()


def test_curated_only_techniques_are_honoured(cat):
    core = start("tomato", "core", cat)
    ok = {k for k in cat.operations if o.assess(k, core).status in o.TAKEN}
    assert ok == {"mijoter", "decocter"}


def test_curated_exception(cat):
    a = o.assess("cuire_vapeur", start("tomato", "skin", cat))
    assert a.status == "inapplicable" and "curated exception" in a.explain()


# ---- outputs and property propagation ----------------------------------------------

def test_peeling_gives_two_materials(cat):
    stems = start("broccoli", "stems", cat)
    inner, peel = o.apply("eplucher", stems)
    assert inner.fraction is None and peel.fraction == "stem_peel"
    assert peel.kind == "fraction" and peel.props["usually_discarded"] is True
    assert inner.props["toughness"] == "low"                 # inner_changes applied
    assert "outer_layer" not in inner.props and "outer_layer" not in peel.props
    assert inner.path[-1].siblings == ("peel",)


def test_cut_names_a_preparation_and_changes_geometry(cat):
    [j] = o.apply("julienne", start("carrot", "root", cat))
    assert j.kind == "geometry" and j.props["form"] == "julienne"
    assert j.props["piece"] == "small" and j.props["thin"] is True


def test_pressing_gives_juice_and_pulp(cat):
    grated = out("raper", start("carrot", "root", cat))[0]
    juice, pulp = o.apply("presser", grated)
    assert juice.props["liquid"] is True and juice.props["fibre"] == "none"
    assert pulp.props["binder"] is True and pulp.props["fibre"] == "high"
    assert "binder" in o.functions(pulp)


def test_drying_then_grinding_makes_a_seasoning_powder(cat):
    dried = out("deshydrater", start("tomato", "skin", cat))[0]
    assert dried.props["water"] == "none" and dried.props["crisp"] is True
    [powder] = o.apply("moudre", dried)
    assert powder.props["piece"] == "powder"
    assert "seasoning_powder" in o.functions(powder)


def test_salting_courgette_gives_vegetable_water(cat):
    grated = out("raper", start("courgette", "fruit", cat))[0]
    drained = out("degorger", grated, "drained")
    water = out("degorger", grated, "vegetable_water")
    assert drained.props["water"] == "high" and drained.props["salted"] is True
    assert water.props["liquid"] is True and "broth_base" in o.functions(water)
    assert "salt" in drained.adds


def test_when_set_crisps_thin_pieces_in_the_oven(cat):
    thin = out("emincer", start("carrot", "root", cat))[0]
    assert out("rotir", thin)[0].props["crisp"] is True
    whole = out("troncons", start("carrot", "root", cat))[0]
    assert not out("rotir", whole)[0].props.get("crisp")


# ---- sequences ---------------------------------------------------------------

@pytest.fixture(scope="module")
def broccoli():
    return o.explore("broccoli")


def test_depth_is_bounded(broccoli):
    assert max(len(r.path) for r in broccoli.results) == o.MAX_DEPTH
    with pytest.raises(ValueError):
        o.explore("broccoli", depth=4)


def test_no_operation_twice_and_one_cut_and_one_cooking(broccoli, cat):
    cuts = {k for k, op in cat.operations.items() if "geometry" in op["categories"]
            and any("one cut per sequence" in str(v) for v in op["requires"].values())}
    cooks = {k for k, op in cat.operations.items()
             if any("one primary cooking" in str(v) for v in op["requires"].values())}
    for r in broccoli.results:
        ops = [s.operation for s in r.path]
        assert len(ops) == len(set(ops))
        assert sum(1 for x in ops if x in cuts) <= 2           # brunoise may refine julienne
        assert sum(1 for x in ops if x in cooks) <= 1


def test_steps_are_applicable_or_conditional_and_change_something(broccoli):
    for r in broccoli.results[:500]:
        assert all(s.status in o.TAKEN for s in r.path)


def test_equivalent_materials_merge(broccoli):
    keys = [r.material.key() for r in broccoli.results]
    assert len(keys) == len(set(keys))
    assert broccoli.stats["merged: equivalent material"] > 0


def test_generation_is_deterministic():
    a = [r.material.key() for r in o.explore("tomato", "skin").results]
    b = [r.material.key() for r in o.explore("tomato", "skin").results]
    assert a == b


def test_exhausted_outputs_end_a_path(broccoli):
    for r in broccoli.results:
        for s in r.path[:-1]:
            assert not s.terminal


def test_branches_continue_independently(cat):
    ex = o.explore("broccoli", "stems", depth=2)
    paths = {tuple(f"{s.operation}:{s.output}" for s in r.path) for r in ex.results}
    paths |= {tuple(f"{s.operation}:{s.output}" for s in p) for r in ex.results for p in r.alternates}
    assert ("eplucher:inner", "julienne:main") in paths
    assert ("eplucher:peel", "deshydrater:main") in paths


def test_peeling_comes_before_cutting(cat):
    cut = out("julienne", start("carrot", "root", cat))[0]
    assert o.assess("eplucher", cut).status == "inapplicable"


def test_a_fraction_keeps_its_parents_processing_state(cat):
    """Regression: a peel separated from cooked material was 'raw' again and
    could be cooked a second time."""
    blanched = out("blanchir", start("broccoli", "stems", cat))[0]
    peel = out("eplucher", blanched, "peel")
    assert peel.props.get("blanched") is True
    assert o.assess("eplucher", out("sauter_wok", start("broccoli", "stems", cat))[0]).status \
        == "inapplicable"


def test_coating_comes_before_cooking(cat):
    fried = out("frire", start("avocado", "flesh", cat))[0]
    assert o.assess("paner", fried).status == "inapplicable"


# ---- ranking and evidence --------------------------------------------------------

def test_ranking_needs_a_function_and_a_reason_for_each_step(cat):
    rs, ex = o.ranked("tomato", "skin")
    assert rs and len(rs) < len(ex.results)
    for x in rs:
        assert x.functions and "waste_reduction" not in x.functions
        assert not x.result.path[-1].terminal
    assert rs == sorted(rs, key=lambda x: (-x.score, len(x.result.path),
                                           o.describe_path(x.result.material)))


def test_evidence_types_stay_apart(cat):
    rs, _ = o.ranked("tomato", "skin")
    evidences = {x.evidence for x in rs}
    assert evidences <= {"established path", "mechanistic inference"}
    powder = next(x for x in rs if [s.operation for s in x.result.path] == ["deshydrater", "moudre"])
    assert powder.evidence == "established path"      # both steps documented on tomato skin


def test_tastings_stay_separate():
    """Generated sequences never write to the ontology or the tasting record."""
    before = (o.DATA / "tastings.yaml").read_text(encoding="utf-8")
    o.explore("tomato", "skin")
    assert (o.DATA / "tastings.yaml").read_text(encoding="utf-8") == before


def test_usefulness_counts_groups_not_overlapping_functions(cat):
    assert o.usefulness(["broth_base", "aromatic_infusion", "colouring"]) == pytest.approx(2.5 / 3)
    assert o.usefulness(["crisp_component"]) == pytest.approx(1 / 3)


# ---- output ---------------------------------------------------------------------

def test_cli(capsys):
    assert main(["applicability", "carrot", "--part", "greens"]) == 0
    assert "chiffonnade" in capsys.readouterr().out
    assert main(["explore", "tomato", "--part", "skin", "--top", "3"]) == 0
    assert "hypotheses, not recipes" in capsys.readouterr().out
    assert main(["explore", "kale"]) == 1
