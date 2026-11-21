"""How Scout candidates find themselves in CulinaryDB.

Before these fixes 187 of 336 novelty observations read "cannot tell",
mostly because the corpus was being read wrong rather than because it lacked
the ingredient. Each test pins one of the misreadings.
"""

import csv

from foodprep import corpus
from foodprep.ui.render import claim_cards_html


def _write(tmp_path, ingredients, links):
    with open(tmp_path / "01_Recipe_Details.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["Recipe ID", "Title", "Source", "Cuisine"])
        for rid in sorted({link[0] for link in links}):
            w.writerow([rid, f"Recipe {rid}", "test", "test"])
    with open(tmp_path / "02_Ingredients.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["Aliased Ingredient Name", "Ingredient Synonyms", "Entity ID", "Category"])
        for name, synonyms, eid in ingredients:
            w.writerow([name, synonyms, eid, "misc"])
    with open(tmp_path / "04_Recipe-Ingredients_Aliases.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["Recipe ID", "Original Ingredient Name", "Aliased Ingredient Name", "Entity ID"])
        for rid, original, aliased, eid in links:
            w.writerow([rid, original, aliased, eid])
    return corpus.load_corpus(tmp_path)


def test_semicolon_synonyms_and_head_first_order(tmp_path):
    _, _, index = _write(
        tmp_path,
        [("Bread", "bread; bun", 2), ("Gruyere Cheese", "cheese-gruyere", 3),
         ("Hazelnut", "hazel=nut", 4)],
        [(1, "bun", "bread", 2)],
    )
    assert index["bun"] == 2                 # was indexed as "bread; bun"
    assert index["gruyere cheese"] == 3      # head-first: cheese-gruyere
    assert index["hazel nut"] == 4


def test_plural_and_identity_names_resolve(tmp_path):
    _, _, index = _write(
        tmp_path,
        [("Egg", "egg", 0), ("Caraway", "caraway", 326)],
        [(1, "egg", "egg", 0), (1, "caraway", "caraway", 326)],
    )
    assert corpus.resolve_novelty_entities("eggs", index) == [0]
    assert corpus.resolve_novelty_entities("caraway_seeds", index) == [326]


def test_broad_family_never_stands_in(tmp_path):
    _, _, index = _write(
        tmp_path,
        [("Butter", "butter", 10), ("Salt", "salt", 11)],
        [(1, "butter", "butter", 10), (1, "salt", "salt", 11)],
    )
    assert corpus.resolve_novelty_entities("brown_butter", index) == []
    assert corpus.resolve_novelty_entities("smoked_salt", index) == []


def test_recipe_links_win_when_the_ingredient_list_disagrees(tmp_path):
    # Real CulinaryDB: anchovy is 720 in the list, 2073 in every recipe.
    recipes, _, index = _write(
        tmp_path,
        [("Anchovy", "#anchovy#", 720)],
        [(1, "anchovy fillets", "anchovy", 2073), (2, "anchovies", "anchovy", 2073)],
    )
    [entity] = corpus.resolve_novelty_entities("anchovy", index)
    assert recipes[entity] == {1, 2}


def test_cooks_wording_measures_a_specific_candidate(tmp_path):
    # CulinaryDB files balsamic under plain vinegar; the original text keeps it.
    recipes, _, index = _write(
        tmp_path,
        [("Vinegar", "vinegar", 322)],
        [(1, "aged balsamic vinegar", "vinegar", 322),
         (2, "balsamic vinegar", "vinegar", 322),
         (3, "white vinegar", "vinegar", 322)],
    )
    entities = corpus.resolve_novelty_entities("balsamic_vinegar", index)
    found = set().union(*(recipes[e] for e in entities))
    assert found == {1, 2}
    # The original wordings must not leak into ordinary lookups.
    assert corpus.resolve_entities("balsamic_vinegar", index) == []


def test_cannot_tell_names_the_missing_ingredient():
    html = claim_cards_html({
        "candidate": "chili_crisp", "state_ingredient": "tomato",
        "candidate_class": "scout_candidate", "shared_function": "x",
        "novelty": {"class": "insufficient_coverage", "corpus_name": "CulinaryDB",
                    "candidate_covered": False, "target_covered": True},
    })
    assert "Chili crisp is not in CulinaryDB" in html
    assert "One side" not in html
