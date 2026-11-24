"""RecipeNLG practice evidence per part: the sentence rules, the tally, the cache.

Every sentence here is written for the test; no corpus text is needed."""
from __future__ import annotations

from collections import Counter

import pytest

from foodprep import part_evidence as pe

R = pe.RULES_BY_KEY


def cls(ingredient, part, sentence, kind="direction", confuser=False):
    return pe.classify(R[(ingredient, part)], sentence, kind, confuser)


@pytest.mark.parametrize("sentence, expected", [
    ("Peel the stalks and cut into 1-inch coins.", "trimmed"),
    ("Cut stems into 1 inch pcs.", "used"),
    ("Cut off the florets; discard the stems.", "removed"),
    ("Save the stalks for another use.", "removed"),
    ("Trim off the tough ends of the stems.", "trimmed"),
    ("Remove from the heat and stir in the stems.", "used"),
    ("The stems are thick.", "unclear"),
])
def test_broccoli_stems(sentence, expected):
    assert cls("broccoli", "stems", sentence) == expected


@pytest.mark.parametrize("sentence, kind, expected", [
    ("2 tomatoes, peeled and chopped", "ingredient", "removed"),
    ("1 (28 oz) can whole peeled tomatoes", "ingredient", "canned"),
    ("Slip off the skins.", "direction", "removed"),
    ("Roast until the skins blister.", "direction", "cue"),
    ("Use unpeeled tomatoes.", "direction", "used"),
    ("Roll the tomato skins into roses for garnish.", "direction", "used"),
    ("Peel the onions and add the tomatoes.", "direction", None),
    ("1 cup tomato sauce", "ingredient", None),
])
def test_tomato_skin(sentence, kind, expected):
    assert cls("tomato", "skin", sentence, kind) == expected


def test_seeded_and_cored_remove_the_part_in_one_word():
    assert cls("tomato", "seeds_and_gel", "4 tomatoes, seeded and diced", "ingredient") == "removed"
    assert cls("tomato", "core", "Core the tomatoes and stuff them.") == "removed"


def test_a_bare_part_word_needs_the_ingredient_when_another_has_that_part():
    # A recipe with parsley: "the stems" may be parsley stems.
    assert cls("broccoli", "stems", "Chop the stems.", confuser=True) is None
    assert cls("broccoli", "stems", "Chop the broccoli stems.", confuser=True) == "used"
    # Bell pepper seeds are not tomato seeds.
    assert cls("tomato", "seeds_and_gel", "Remove the seeds.", confuser=True) is None


# Cases the first hand check got wrong (docs/research/s2-part-counts).
@pytest.mark.parametrize("ingredient, part, sentence, kind, expected", [
    ("tomato", "seeds_and_gel", "Mix the tomatoes, onion, fennel seed and basil.", "direction", None),
    ("tomato", "seeds_and_gel", "Roll up jelly-roll style.", "direction", None),
    ("tomato", "seeds_and_gel", "Wash tomatoes, cut in half and squeeze the seeds out.", "direction", "removed"),
    ("tomato", "seeds_and_gel", "Chop the tomatoes, reserving the seeds and juice.", "direction", "used"),
    ("tomato", "core", "Core tomatoes.", "direction", "removed"),
    ("tomato", "core", "Slice tomatoes in half (cut through the core).", "direction", "used"),
    ("tomato", "core", "2 large tomatoes (8 ounces each), cored", "ingredient", "removed"),
    ("tomato", "skin", "4 large tomatoes, peeled, or 1 can tomatoes", "ingredient", "removed"),
    ("tomato", "skin", "Skin, deseed and chop the tomatoes.", "direction", "removed"),
    ("tomato", "skin", "Pulverize the skins into tomato skin salt.", "direction", "used"),
    ("broccoli", "leaves", "Add bay leaf and broccoli.", "direction", None),
    ("broccoli", "florets", "Cut off broccoli florets.", "direction", "used"),
    ("broccoli", "florets", "Cut florets off; discard the stalks.", "direction", "used"),
    ("broccoli", "florets", "Discard the florets.", "direction", "removed"),
    # Second round.
    ("broccoli", "florets", "1 bunch broccoli, stems discarded and florets cut into pieces", "ingredient", "used"),
    ("broccoli", "leaves", "Trim large leaves from broccoli.", "direction", "removed"),
    ("broccoli", "leaves", "Add Chinese broccoli leaves and stir-fry.", "direction", None),
    ("broccoli", "stems", "Saute the broccoli stems and onion in butter.", "direction", "used"),
    ("broccoli", "stems", "2 stalks broccoli", "ingredient", None),
    ("broccoli", "stems", "1 large stalk fresh broccoli, sliced", "ingredient", None),
    ("broccoli", "stems", "1 lb Broccoli stems", "ingredient", "used"),
    ("broccoli", "stems", "1 bundle broccoli, chopped fine (don't use stalks)", "ingredient", "removed"),
    ("tomato", "core", "Cut the tough cores from the top of the tomatoes.", "direction", "removed"),
    ("tomato", "core", "Add the cored tomatoes and cook until charred.", "direction", "removed"),
    ("tomato", "core", "Cut away the stem area, leaving the core intact.", "direction", "used"),
    ("tomato", "seeds_and_gel", "Dip tomatoes in boiling water, then peel and seed.", "direction", "removed"),
    ("tomato", "seeds_and_gel", "I do NOT seed or juice my tomatoes.", "direction", "used"),
    ("tomato", "seeds_and_gel", "1/8 cup minced tomato (no seeds)", "ingredient", "removed"),
    ("tomato", "skin", "Roast until tomato skins wrinkle and brown.", "direction", "cue"),
    ("tomato", "skin", "Remove the tray and take the skin from the tomato.", "direction", "removed"),
    ("tomato", "skin", "2 roma tomatoes, with skin removed and chopped", "ingredient", "removed"),
    ("tomato", "skin", "Roast a whole unpeeled head of garlic with the tomatoes.", "direction", None),
])
def test_hand_check_regressions(ingredient, part, sentence, kind, expected):
    assert cls(ingredient, part, sentence, kind) == expected


def test_broccoli_rabe_is_not_broccoli():
    _, baselines, _ = pe.tally([_recipe(["1 bunch broccoli rabe"], ["Trim the stems."])])
    assert baselines["broccoli"] == 0


def _recipe(ingredients, directions, source="Gathered"):
    return pe.Recipe(source, ingredients, directions)


def test_a_recipe_counts_once_under_its_strongest_class():
    recipes = [
        # Discards stems, then peels and keeps them: kept wins.
        _recipe(["1 head broccoli"], ["Cut off the florets; discard the stems.",
                                      "Actually peel the stalks and add them too."]),
        _recipe(["1 head broccoli"], ["Cut into florets and discard the stems."]),
        _recipe(["2 cups broccoli florets"], ["Steam the florets."], source="Recipes1M"),
        _recipe(["1 lb potatoes"], ["Boil."]),
    ]
    tallies, baselines, _ = pe.tally(recipes)
    stems = tallies[("broccoli", "stems")]
    assert stems.recipes == Counter({"trimmed": 1, "removed": 1})
    assert baselines["broccoli"] == 3 and baselines["tomato"] == 0
    florets = tallies[("broccoli", "florets")]
    assert florets.by_source["Recipes1M"]["used"] == 1
    assert florets.techniques["steam"] == 1


def test_canned_tomato_is_not_fruit_in_the_baseline():
    _, baselines, _ = pe.tally([
        _recipe(["1 can tomato sauce"], ["Heat."]),
        _recipe(["3 ripe tomatoes"], ["Slice."]),
    ])
    assert baselines["tomato"] == 2 and baselines["tomato:fresh"] == 1


def test_the_hand_check_sample_is_bounded_per_class():
    recipes = [_recipe(["broccoli"], ["Discard the stems."]) for _ in range(50)]
    _, _, samples = pe.tally(recipes, sample_per_class=5)
    assert len([s for s in samples if s.part == "stems"]) == 5


@pytest.mark.parametrize("counts, base, level", [
    ({}, 1000, "not_found"),
    ({"removed": 40, "used": 10}, 1000, "removed"),
    ({"used": 20}, 1000, "rarely_used"),      # under 30 recipes
    ({"used": 50}, 10000, "rarely_used"),     # under 1% of the ingredient
    ({"used": 300, "trimmed": 50, "removed": 200}, 10000, "used"),
])
def test_evidence_level(counts, base, level):
    t = pe.PartTally("broccoli", "stems", recipes=Counter(counts))
    assert pe.evidence_level(t, base) == level


def test_resolve_csv_prefers_the_given_path_and_rejects_a_missing_one(tmp_path):
    f = tmp_path / "full_dataset.csv"
    f.write_text("x", encoding="utf-8")
    assert pe.resolve_csv(f, env={}) == f
    assert pe.resolve_csv(None, env={pe.RECIPENLG_ENV: str(f)}) == f
    with pytest.raises(pe.RecipeNLGNotFound):
        pe.resolve_csv(tmp_path / "nope.csv", env={})


def test_read_recipes_filters_before_parsing(tmp_path):
    f = tmp_path / "full_dataset.csv"
    f.write_text(
        ',title,ingredients,directions,link,source,NER\n'
        '0,A,"[""1 head broccoli""]","[""Steam.""]",x,Gathered,"[]"\n'
        '1,B,"[""2 eggs""]","not json",x,Gathered,"[]"\n',
        encoding="utf-8")
    import re
    got = list(pe.read_recipes(f, re.compile("broccoli")))
    assert [r.directions for r in got] == [["Steam."]]


def test_the_cache_holds_counts_and_no_recipe_text(tmp_path):
    tallies, baselines, _ = pe.tally([_recipe(["1 head broccoli"], ["Discard the stems."])])
    ev = pe.build_evidence(tmp_path / "full_dataset.csv", Counter({"Gathered": 1}),
                           tallies, baselines, search_date="2026-11-24")
    out = tmp_path / "part_evidence.yaml"
    pe.write_evidence(ev, out)
    text = out.read_text(encoding="utf-8")
    assert "Discard the stems" not in text
    loaded = pe.load_evidence(out)
    assert loaded[("broccoli", "stems")]["recipes"]["removed"] == 1
    assert pe.load_evidence(tmp_path / "missing.yaml") == {}


def test_every_rule_names_a_part_the_model_has(conn):
    rows = conn.execute(
        "SELECT i.canonical_name, p.name FROM ingredient_parts p "
        "JOIN ingredients i ON i.ingredient_id = p.ingredient_id").fetchall()
    known = {(r[0], r[1]) for r in rows}
    assert set(R) <= known


def test_a_default_part_is_not_called_rare():
    t = pe.PartTally("tomato", "flesh", recipes=Counter({"used": 10}))
    assert pe.evidence_level(t, 100000, default_part=True) == "default"
    t = pe.PartTally("broccoli", "florets", recipes=Counter({"removed": 9, "used": 1}))
    assert pe.evidence_level(t, 1000, default_part=True) == "removed"


def test_parts_show_practice_from_the_committed_counts(conn):
    from foodprep import query
    d = query.decomposition(conn, "tomato")
    skin = next(p for p in d["parts"] if p["name"] == "skin")
    assert skin["practice"]["evidence_level"] == "removed"
    text = query.render_decomposition(d)
    assert "Cooks mostly remove it (RecipeNLG:" in text
    assert "What recipes mean by the ingredient" in text   # flesh
    # Avocado has parts but no counts yet: no practice line, no error.
    avo = query.decomposition(conn, "avocado")
    assert all(p["practice"] is None for p in avo["parts"])
