"""The possibility generator: ideas come from part properties, techniques and
family mechanisms; RecipeNLG counts only label them."""

from __future__ import annotations

import dataclasses
import re

import pytest

from foodprep import pair_counts as pc
from foodprep import part_evidence as pe
from foodprep import possibilities as po
from foodprep.cli import main

FORMS = {"juice", "vinegar", "liquid", "crushed_raw", "puree", "cooked_sauce", "jelly",
         "paste", "oil", "solid_fat", "cream", "crystal", "powder", "crumble",
         "raw_shred", "raw_leaf", "whole"}


@pytest.fixture(scope="module")
def t():
    return po.load_tables()


def ideas_for(t, family, ing, part, tech, member):
    return [i for i in po.family_ideas(t, family, ing, part, tech) if i.member == member]


# ---- tables -------------------------------------------------------------------

def test_every_part_with_properties_is_a_modelled_part(t):
    modelled = po._edibility()
    for ing, parts in t.parts.items():
        for part in parts:
            assert (ing, part) in modelled, f"{ing}.{part} not in tomato.yaml parts"


def test_technique_corpus_keys_exist_in_part_evidence(t):
    keys = {k for k, _ in pe.TECHNIQUES}
    for name, rule in t.techniques.items():
        assert rule["corpus"] in keys, name


def test_families_are_ontology_roles(t):
    data = pc.load_yaml(po.DATA / "tomato.yaml")
    roles = {r["name"] for r in data["roles"]}
    used = {r for i in data["ingredients"] for r in (i.get("base_roles") or "").split("\n")}
    for fam in t.families:
        assert fam in roles | used, fam


def test_members_carry_their_ontology_roles(t):
    """A member's tomato.yaml base_roles that are families appear in its families."""
    data = pc.load_yaml(po.DATA / "tomato.yaml")
    roles = {i["canonical_name"]: set((i.get("base_roles") or "").split("\n"))
             for i in data["ingredients"]}
    for name, m in t.members.items():
        if "ingredient" not in m:
            continue
        assert m["ingredient"] in roles, f"{name}: no ingredient {m['ingredient']}"
        missing = (roles[m["ingredient"]] & set(t.families)) - set(m["families"])
        assert not missing, f"{name} lacks {missing}"


def test_members_have_valid_levels_forms_and_patterns(t):
    for name, m in t.members.items():
        assert m["families"] and set(m["families"]) <= set(t.families), name
        assert all(v in po.LEVELS for v in m["families"].values()), name
        assert set(m["forms"]) <= FORMS, name
        re.compile(m["corpus"])


def test_every_family_has_members_and_mechanisms(t):
    for fam, spec in t.families.items():
        assert po.members_of(t, fam), fam
        assert spec["mechanisms"], fam
        assert spec["kind"] in {"modifier", "partner"}
        for name, m in spec["mechanisms"].items():
            assert m["timing"] in {"finish", "dress", "marinate", "cook", "serve"}, name
            for form in m.get("member_needs", {}).get("forms_any", []):
                assert form in FORMS, (name, form)


@pytest.mark.parametrize("cond, ok", [
    ({"water": "<=medium"}, True),
    ({"water": ">=high"}, False),
    ({"fibre": "high"}, True),
    ({"thin": False}, True),
    ({"raw_ok": True}, True),
    ({"liquid": True}, False),
])
def test_holds(cond, ok):
    stems = {"water": "medium", "fibre": "high", "raw_ok": True}
    assert po.holds(stems, cond) is ok


# ---- techniques -----------------------------------------------------------------

def test_parts_that_are_not_food_get_no_techniques(t):
    assert po.techniques_for(t, "avocado", "skin") == []
    assert po.techniques_for(t, "avocado", "stone") == []


def test_conditional_core_is_only_simmered(t):
    assert po.techniques_for(t, "tomato", "core") == ["simmer"]


def test_technique_rules_follow_properties(t):
    leaves = po.techniques_for(t, "broccoli", "leaves")
    assert "massage" in leaves and "dry" in leaves
    assert "massage" not in po.techniques_for(t, "broccoli", "florets")
    gel = po.techniques_for(t, "tomato", "seeds_and_gel")
    assert "roast" not in gel and "fry" not in gel
    assert "fry" not in po.techniques_for(t, "tomato", "flesh")   # too wet


def test_except_list_removes_a_technique(t):
    assert "steam" not in po.techniques_for(t, "tomato", "skin")
    assert "simmer" not in po.techniques_for(t, "avocado", "flesh")


# ---- a part that already has a family gets none of it ----------------------------

@pytest.mark.parametrize("ing, part, family", [
    ("tomato", "seeds_and_gel", "acid"),
    ("avocado", "flesh", "fat"),
    ("tomato", "skin", "umami"),
])
def test_a_part_gets_nothing_from_a_family_it_already_has(t, ing, part, family):
    assert po.already_has(t, t.parts[ing][part], family)
    for tech in po.techniques_for(t, ing, part):
        assert po.family_ideas(t, family, ing, part, tech) == []


# ---- acid ---------------------------------------------------------------------

def test_avocado_raw_lemon_slows_browning_and_cuts_fat(t):
    [i] = ideas_for(t, "acid", "avocado", "flesh", "raw", "lemon")
    assert {"slow_browning", "cut_fat"} <= set(i.mechanisms)
    assert not any("olive" in r for r in i.risks)


def test_a_dry_acid_cannot_coat_against_browning(t):
    [i] = ideas_for(t, "acid", "avocado", "flesh", "raw", "sumac")
    assert "slow_browning" not in i.mechanisms and "cut_fat" in i.mechanisms


def test_quick_pickle_needs_a_strong_liquid_acid(t):
    [ling] = ideas_for(t, "acid", "broccoli", "stems", "raw", "lingonberry")
    assert "quick_pickle" in ling.mechanisms and ling.form == "juice" and ling.safety
    assert ideas_for(t, "acid", "broccoli", "stems", "raw", "sumac") == []


def test_lingonberry_on_roasted_stems_gets_its_reasons_and_risks(t):
    [i] = ideas_for(t, "acid", "broccoli", "stems", "roast", "lingonberry")
    assert i.mechanisms == ["brighten_browned"]
    assert any("astringency" in r for r in i.reasons)
    assert any("olive" in r for r in i.risks)


def test_bitter_member_on_bitter_leaves_is_a_risk(t):
    [i] = ideas_for(t, "acid", "broccoli", "leaves", "massage", "lingonberry")
    assert any("stacks the bitterness" in r for r in i.risks)


def test_sorrel_warns_about_heat(t):
    [i] = ideas_for(t, "acid", "broccoli", "stems", "roast", "sorrel")
    assert any("khaki" in r for r in i.risks)


def test_tomato_gel_is_an_acid_for_other_parts_not_for_itself(t):
    [i] = ideas_for(t, "acid", "tomato", "flesh", "roast", "tomato_gel")
    assert po.label(t, i).label == "own_part"
    [b] = ideas_for(t, "acid", "broccoli", "stems", "roast", "tomato_gel")
    assert po.label(t, b).label == "part_acid" and b.scout


# ---- other families ------------------------------------------------------------

def test_fat_browns_roasted_stems_and_rounds_bitter_leaves(t):
    [oil] = ideas_for(t, "fat", "broccoli", "stems", "roast", "olive_oil")
    assert "brown_in_fat" in oil.mechanisms
    [walnut] = ideas_for(t, "fat", "broccoli", "leaves", "raw", "walnut")
    assert walnut.mechanisms == ["round_bitter"]          # a crumble cannot coat


def test_salt_draws_water_from_raw_tomato_flesh(t):
    [s] = ideas_for(t, "salt", "tomato", "flesh", "raw", "sea_salt")
    assert "draw_water" in s.mechanisms
    assert ideas_for(t, "salt", "tomato", "flesh", "raw", "soy_sauce") == []


def test_a_salty_member_in_another_family_warns_about_salt(t):
    [miso] = ideas_for(t, "umami", "broccoli", "stems", "roast", "miso")
    assert any("salty too" in r for r in miso.risks)


def test_sweet_balances_the_acid_tomato_gel(t):
    [h] = ideas_for(t, "sweet", "tomato", "seeds_and_gel", "raw", "honey")
    assert h.mechanisms == ["balance_acid"]


def test_sweet_acid_in_the_acid_family_reads_as_dessert(t):
    [b] = ideas_for(t, "acid", "broccoli", "stems", "roast", "balsamic_vinegar")
    assert any("dessert" in r for r in b.risks)


def test_protein_partners_follow_the_state(t):
    [egg] = ideas_for(t, "protein", "broccoli", "stems", "roast", "eggs")
    assert "yolk_as_sauce" in egg.mechanisms
    [goat] = ideas_for(t, "protein", "broccoli", "stems", "roast", "goat_cheese")
    assert goat.mechanisms == ["creamy_against_crisp"]
    [tofu] = ideas_for(t, "protein", "broccoli", "stems", "stir_fry", "tofu")
    assert tofu.mechanisms == ["same_pan"]


def test_carb_soaks_tomato_juice(t):
    [bread] = ideas_for(t, "carb", "tomato", "flesh", "raw", "bread")
    assert bread.mechanisms == ["soak_juice"]
    assert ideas_for(t, "carb", "broccoli", "stems", "raw", "bread") == []


# ---- labels -------------------------------------------------------------------

def counts(pair, n_t=50_000, n_s=1_000, n=2_000_000):
    return {"recipes": n, "targets": {"broccoli": n_t}, "sources": {"lingonberry": n_s},
            "pairs": {"broccoli": {"lingonberry": pair}},
            "triples": {"broccoli": {"roast": {"lingonberry": min(pair, 3)}}}}


@pytest.mark.parametrize("pair, n_s, want", [
    (0, 1_000, "not_seen"),     # chance predicts 25
    (0, 100, "untested"),       # chance predicts 2.5
    (3, 1_000, "rare"),
    (20, 1_000, "seen"),
    (400, 10_000, "common"),
])
def test_labels(t, pair, n_s, want):
    tables = dataclasses.replace(t, counts=counts(pair, n_s=n_s))
    i = po.Idea("broccoli", "stems", "roast", family="acid", member="lingonberry",
                form="juice", mechanisms=["brighten_browned"])
    po.label(tables, i)
    assert i.label == want
    assert i.scout is (want not in ("seen", "common"))


def test_without_counts_everything_is_untested(t):
    tables = dataclasses.replace(t, counts={})
    i = po.label(tables, po.Idea("broccoli", "stems", "roast", family="acid", member="lemon"))
    assert i.label == "untested"


def test_scout_rank_puts_a_loud_absence_first():
    loud = po.Idea("a", "p", "raw", member="x", label="not_seen", observed=0, expected=40)
    quiet = po.Idea("a", "p", "raw", member="y", label="not_seen", observed=0, expected=6)
    rare = po.Idea("a", "p", "raw", member="z", label="rare", observed=1, expected=40)
    assert sorted([rare, quiet, loud], key=po.scout_rank) == [loud, quiet, rare]


def test_committed_counts_cover_every_member(t):
    if not t.counts:
        pytest.skip("pair_counts.yaml not generated")
    assert set(t.counts["sources"]) == set(t.members)


# ---- counting -----------------------------------------------------------------

def test_count_row_counts_pairs_and_techniques():
    sources = pc.source_patterns()
    targets = {name: ing.listed for name, ing in pe.INGREDIENTS.items()}
    any_s = re.compile("|".join(f"(?:{r.pattern})" for r in sources.values()), re.I)
    c = pc.Counts(targets, sources)
    pc.count_row(c, '["1 head broccoli", "1/2 c. lingonberries"]', '["Roast the broccoli."]',
                 targets, sources, any_s)
    pc.count_row(c, '["2 avocados", "1 tsp lemon pepper"]', '["Mash."]', targets, sources, any_s)
    pc.count_row(c, '["1 c. dried cranberries", "1 can butter beans"]', '["Mix."]',
                 targets, sources, any_s)
    rec = c.to_record()
    assert rec["recipes"] == 3
    assert rec["pairs"]["broccoli"]["lingonberry"] == 1
    assert rec["triples"]["broccoli"]["roast"] == {"lingonberry": 1}
    assert rec["sources"]["lemon"] == 0 and rec["sources"]["cranberry"] == 0
    assert rec["sources"]["butter"] == 0
    assert rec["targets"]["avocado"] == 1


# ---- output -------------------------------------------------------------------

def test_render_groups_by_family():
    out = po.render("broccoli", part="stems")
    for fam in ("Acid", "Fat", "Salt", "Umami", "Protein"):
        assert f"  {fam} (" in out


def test_render_avocado_says_it_already_has_fat():
    out = po.render("avocado", show_all=True, limit=50)
    assert "Skin: not food." in out and "Stone: not food." in out
    assert "Fat: already has it" in out
    assert "+ lemon (juice)" in out


def test_render_one_family():
    out = po.render("tomato", part="seeds_and_gel", family="sweet", show_all=True)
    assert "Sweet (" in out and "Acid (" not in out


def test_render_families_lists_members_with_their_other_families():
    out = po.render_families("salt")
    assert out.startswith("Salt (modifier")
    assert "soy sauce" in out and "also umami" in out


def test_cli(capsys):
    assert main(["possible", "broccoli", "--part", "stems", "--family", "protein"]) == 0
    assert "Protein (" in capsys.readouterr().out
    assert main(["possible", "kale"]) == 1
    assert main(["possible", "broccoli", "--family", "nope"]) == 1
    assert main(["families", "carb"]) == 0
    assert "Carb (partner" in capsys.readouterr().out


# ---- evidence scope and governance (PR #4 review) --------------------------------

def test_label_scope_is_stated_wherever_labels_are_shown():
    out = po.render("broccoli", part="stems", family="acid", limit=1)
    assert po.LABEL_SCOPE in out
    assert "anywhere" in out


def test_label_ignores_the_technique():
    """The label is set by the ingredient-member pair, not by the technique;
    the scope text says so. Same pair, two techniques, same label."""
    t = po.load_tables()
    [roast] = ideas_for(t, "acid", "broccoli", "stems", "roast", "lemon")
    [steam] = ideas_for(t, "acid", "broccoli", "stems", "steam", "lemon")
    assert po.label(t, roast).label == po.label(t, steam).label


def test_families_checksum_ignores_formatting(tmp_path):
    a, b = tmp_path / "a.yaml", tmp_path / "b.yaml"
    a.write_text("families: {acid: {kind: modifier}}\nmembers: {}\n", encoding="utf-8")
    b.write_text("# comment\nmembers: {}\nfamilies:\n  acid:\n    kind: modifier\n",
                 encoding="utf-8")
    assert pc.families_checksum(a) == pc.families_checksum(b)
    b.write_text("families: {acid: {kind: partner}}\nmembers: {}\n", encoding="utf-8")
    assert pc.families_checksum(a) != pc.families_checksum(b)


def test_stale_warning(tmp_path):
    f = tmp_path / "f.yaml"
    f.write_text("families: {}\nmembers: {}\n", encoding="utf-8")
    good = {"corpus": {"families_sha256": pc.families_checksum(f)}}
    assert pc.stale_warning(good, f) is None
    assert "different family definitions" in pc.stale_warning(
        {"corpus": {"families_sha256": "0" * 64}}, f)
    assert "no checksum" in pc.stale_warning({"corpus": {}}, f)
    assert pc.stale_warning({}, f) is None


def test_committed_counts_match_the_current_family_definitions():
    """Editing families.yaml makes the committed counts stale: rerun
    scripts/count_family_pairs.py (~28 min) and commit both outputs."""
    from foodprep import family_profiles as fp
    for record in (pc.load_counts(), fp.load_profiles()):
        if not record:
            pytest.skip("counts not generated")
        assert pc.stale_warning(record) is None
