"""Family-level analysis: family shares per ingredient and technique, checked
against the curated missing roles."""

from __future__ import annotations

import re

import pytest

from foodprep import family_profiles as fp
from foodprep import pair_counts as pc
from foodprep import part_evidence as pe
from foodprep.cli import main

FAMS = ["acid", "fat", "salt", "umami", "sweet", "protein", "carb"]


def run(rows):
    """Count fake recipes (ingredient field, directions field)."""
    sources = pc.source_patterns()
    targets = {n: i.listed for n, i in pe.INGREDIENTS.items()}
    any_s = re.compile("|".join(f"(?:{r.pattern})" for r in sources.values()), re.I)
    c, f = pc.Counts(targets, sources), fp.FamilyCounts()
    for ing, dirs in rows:
        f.add(*pc.count_row(c, ing, dirs, targets, sources, any_s))
    return f.to_record()


def test_a_recipe_has_a_family_when_it_lists_any_member():
    rec = run([('["1 lb broccoli", "2 T olive oil", "salt", "juice of 1 lemon"]',
                '["Roast the broccoli."]'),
               ('["1 lb broccoli", "1 T vinegar", "1 tsp lemon juice"]', '["Steam."]')])
    b = rec["targets"]["broccoli"]
    assert b["recipes"] == 2
    assert b["families"]["acid"] == 2            # two acids in one recipe count once
    assert b["techniques"]["roast"]["families"] == {
        "acid": 1, "fat": 1, "salt": 1, "umami": 0, "sweet": 0, "protein": 0, "carb": 0}
    assert b["techniques"]["roast"]["combos"] == {"acid+fat+salt": 1}


def test_a_part_of_the_target_is_not_a_member_for_it():
    rec = run([('["4 tomatoes", "salt"]', '["Slice."]'),
               ('["1 lb broccoli", "2 tomatoes"]', '["Toss."]')])
    assert rec["targets"]["tomato"]["families"]["acid"] == 0     # tomato gel is tomato
    assert rec["targets"]["broccoli"]["families"]["acid"] == 1   # tomato brings acid here


def test_recipes_without_members_are_none():
    rec = run([('["1 avocado"]', '["Eat."]')])
    assert rec["targets"]["avocado"]["combos"] == {"none": 1}
    assert rec["all_recipes"]["acid"] == 0


def test_the_any_recipe_baseline_counts_every_member():
    rec = run([('["2 c. flour", "1 c. butter", "1 c. sugar"]', '["Bake."]')])
    assert rec["recipes"] == 1
    assert rec["all_recipes"]["fat"] == 1 and rec["all_recipes"]["sweet"] == 1


@pytest.mark.parametrize("curated, s, want", [
    ("high", 0.7, "agrees"), ("high", 0.3, "partly"), ("medium", 0.1, "gap"),
    (None, 0.8, "unlisted"), (None, 0.3, ""),
])
def test_verdict(curated, s, want):
    assert fp.verdict(curated, s) == want


def test_curated_states_read_missing_roles():
    states = {(s["technique"], s["part"]): s for s in fp.curated_states("broccoli")}
    roast = states[("roast", "florets")]
    assert {"salt", "fat", "acid", "protein", "carb"} <= set(roast["missing"])


def profile(acid_roast=10, n_roast=100):
    fam = {f: 0 for f in FAMS}
    return {
        "recipes": 1000, "all_recipes": dict(fam),
        "targets": {"broccoli": {
            "recipes": 500, "families": {**fam, "acid": 100, "fat": 400}, "combos": {"fat+salt": 200},
            "techniques": {"roast": {"recipes": n_roast,
                                     "families": {**fam, "acid": acid_roast, "fat": 90, "salt": 80,
                                                  "sweet": 70},
                                     "combos": {}}}}},
    }


def test_check_marks_gaps_agreements_and_unlisted_families():
    rows = {r["family"]: r for r in fp.check("broccoli", profile(), FAMS)
            if r["technique"] == "roast"}
    assert rows["acid"]["verdict"] == "gap"         # curated missing, 10% add it
    assert rows["fat"]["verdict"] == "agrees"       # curated missing, 90% add it
    assert rows["sweet"]["verdict"] == "unlisted"   # not curated, 70% add it
    assert rows["umami"]["verdict"] == ""


def test_render_profile_shows_table_check_and_sets():
    out = fp.render_profile("broccoli", profile())
    assert "roast" in out and "Gap: listed as missing" in out and "acid 10%" in out
    assert "fat + salt" in out


def test_render_without_profiles():
    assert fp.render_profile("broccoli", {}).startswith("No family profiles")


def test_committed_profiles_cover_every_family():
    prof = fp.load_profiles()
    if not prof:
        pytest.skip("family_profiles.yaml not generated")
    fams = list(pc.load_yaml(pc.FAMILIES_PATH)["families"])
    for t in prof["targets"].values():
        assert list(t["families"]) == fams


def test_cli_family_profile(capsys):
    code = main(["family-profile", "broccoli"])
    out = capsys.readouterr().out
    assert code == (1 if out.startswith("No ") else 0)
    assert main(["family-profile", "kale"]) == 1
