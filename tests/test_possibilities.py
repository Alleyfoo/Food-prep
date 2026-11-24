"""The possibility generator: ideas come from part properties, techniques and
acid mechanisms; RecipeNLG counts only label them."""

from __future__ import annotations

import dataclasses
import re

import pytest

from foodprep import pair_counts as pc
from foodprep import part_evidence as pe
from foodprep import possibilities as po
from foodprep.cli import main


@pytest.fixture(scope="module")
def t():
    return po.load_tables()


def ideas_for(t, ing, part, tech, source):
    return [i for i in po.acid_ideas(t, ing, part, tech) if i.source == source]


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


def test_sources_have_valid_forms_and_patterns(t):
    allowed = po.WET_FORMS | {"powder", "raw_shred", "raw_leaf"}
    for name, s in t.sources.items():
        assert set(s["forms"]) <= allowed, name
        re.compile(s["corpus"])


def test_mechanism_timings_are_known(t):
    for name, m in t.mechanisms.items():
        assert m["timing"] in {"finish", "dress", "marinate"}, name


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


# ---- acid mechanisms -------------------------------------------------------------

def test_an_acid_part_gets_no_more_acid(t):
    for tech in po.techniques_for(t, "tomato", "seeds_and_gel"):
        assert po.acid_ideas(t, "tomato", "seeds_and_gel", tech) == []


def test_avocado_raw_lemon_slows_browning_and_cuts_fat(t):
    [i] = ideas_for(t, "avocado", "flesh", "raw", "lemon")
    assert {"slow_browning", "cut_fat"} <= set(i.mechanisms)
    assert not any("olive" in r for r in i.risks)


def test_a_dry_acid_cannot_coat_against_browning(t):
    [i] = ideas_for(t, "avocado", "flesh", "raw", "sumac")
    assert "slow_browning" not in i.mechanisms
    assert "cut_fat" in i.mechanisms


def test_quick_pickle_needs_a_strong_liquid_acid(t):
    [ling] = ideas_for(t, "broccoli", "stems", "raw", "lingonberry")
    assert "quick_pickle" in ling.mechanisms and ling.form == "juice"
    assert ling.safety
    assert ideas_for(t, "broccoli", "stems", "raw", "sumac") == []


def test_lingonberry_on_roasted_stems_gets_its_reasons_and_risks(t):
    [i] = ideas_for(t, "broccoli", "stems", "roast", "lingonberry")
    assert i.mechanisms == ["brighten_browned"]
    assert any("astringency" in r for r in i.reasons)
    assert any("olive" in r for r in i.risks)


def test_bitter_acid_on_bitter_leaves_is_a_risk(t):
    [i] = ideas_for(t, "broccoli", "leaves", "massage", "lingonberry")
    assert any("stacks the bitterness" in r for r in i.risks)


def test_sorrel_warns_about_heat(t):
    [i] = ideas_for(t, "broccoli", "stems", "roast", "sorrel")
    assert any("khaki" in r for r in i.risks)


def test_tomato_gel_is_an_acid_for_other_parts_not_for_itself(t):
    [i] = ideas_for(t, "tomato", "flesh", "roast", "tomato_gel")
    assert po.label(t, i).label == "own_part"
    assert ideas_for(t, "tomato", "seeds_and_gel", "raw", "tomato_gel") == []
    [b] = ideas_for(t, "broccoli", "stems", "roast", "tomato_gel")
    assert po.label(t, b).label == "part_acid" and b.scout


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
    i = po.Idea("broccoli", "stems", "roast", source="lingonberry", form="juice",
                mechanisms=["brighten_browned"])
    po.label(tables, i)
    assert i.label == want
    assert i.scout is (want not in ("seen", "common"))


def test_without_counts_everything_is_untested(t):
    tables = dataclasses.replace(t, counts={})
    i = po.label(tables, po.Idea("broccoli", "stems", "roast", source="lemon"))
    assert i.label == "untested"


def test_scout_rank_puts_a_loud_absence_first():
    loud = po.Idea("a", "p", "raw", source="x", label="not_seen", observed=0, expected=40)
    quiet = po.Idea("a", "p", "raw", source="y", label="not_seen", observed=0, expected=6)
    rare = po.Idea("a", "p", "raw", source="z", label="rare", observed=1, expected=40)
    assert sorted([rare, quiet, loud], key=po.scout_rank) == [loud, quiet, rare]


# ---- counting -----------------------------------------------------------------

def test_count_row_counts_pairs_and_techniques():
    sources = pc.source_patterns()
    targets = {name: ing.listed for name, ing in pe.INGREDIENTS.items()}
    any_s = re.compile("|".join(f"(?:{r.pattern})" for r in sources.values()), re.I)
    c = pc.Counts(targets, sources)
    pc.count_row(c, '["1 head broccoli", "1/2 c. lingonberries"]', '["Roast the broccoli."]',
                 targets, sources, any_s)
    pc.count_row(c, '["2 avocados", "1 tsp lemon pepper"]', '["Mash."]', targets, sources, any_s)
    pc.count_row(c, '["1 c. dried cranberries"]', '["Mix."]', targets, sources, any_s)
    rec = c.to_record()
    assert rec["recipes"] == 3
    assert rec["pairs"]["broccoli"]["lingonberry"] == 1
    assert rec["triples"]["broccoli"]["roast"] == {"lingonberry": 1}
    assert rec["sources"]["lemon"] == 0 and rec["sources"]["cranberry"] == 0
    assert rec["targets"]["avocado"] == 1


# ---- output -------------------------------------------------------------------

def test_render_avocado_shows_flesh_ideas_and_not_food_parts():
    out = po.render("avocado", show_all=True, limit=50)
    assert "Skin: not food." in out and "Stone: not food." in out
    assert "+ lemon (juice)" in out


def test_render_says_acid_parts_need_no_acid():
    assert "Already acid" in po.render("tomato", part="seeds_and_gel")


def test_cli_possible(capsys):
    assert main(["possible", "broccoli", "--part", "stems", "--limit", "2"]) == 0
    assert "Stems." in capsys.readouterr().out
    assert main(["possible", "kale"]) == 1
