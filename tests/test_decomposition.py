"""ADR 0002: ingredient -> decomposition -> processing -> use as food."""
from __future__ import annotations

import sqlite3

import pytest

from foodprep import loader, query
from foodprep.loader import DATA_PATH, LoadError


def _parts(d):
    return {p["name"]: p for p in d["parts"]}


def test_broccoli_splits_into_florets_stems_and_leaves(conn):
    d = query.decomposition(conn, "broccoli")
    parts = _parts(d)
    assert list(parts) == ["florets", "stems", "leaves"]
    assert all(p["edible"] == "yes" and p["separated_by"] == "trim" for p in parts.values())


def test_each_broccoli_part_has_its_own_processing_and_uses(conn):
    parts = _parts(query.decomposition(conn, "broccoli"))
    techs = {name: {x["technique"] for x in p["paths"]} for name, p in parts.items()}
    assert techs["florets"] == {"raw_assemble", "steam", "roast", "stir_fry"}
    assert techs["stems"] == {"raw_slaw", "stir_fry"}
    assert techs["leaves"] == {"saute"}
    stem_slaw = next(x for x in parts["stems"]["paths"] if x["technique"] == "raw_slaw")
    assert "slaw" in stem_slaw["uses"] and "acid" in stem_slaw["missing"]


def test_soup_still_uses_the_whole_broccoli(conn):
    whole = query.decomposition(conn, "broccoli")["whole"]
    assert [x["technique"] for x in whole] == ["soup"]


def test_the_same_technique_on_two_parts_gives_two_states(conn):
    florets = query.transformation_by_technique(conn, "stir_fry", "broccoli", part="florets")
    stems = query.transformation_by_technique(conn, "stir_fry", "broccoli", part="stems")
    assert florets["component"] != stems["component"]
    # Without a part, the lookup is stable: the first authored step.
    assert query.transformation_by_technique(conn, "stir_fry", "broccoli")["part"] == "florets"
    assert query.techniques_for_ingredient(conn, "broccoli").count("stir_fry") == 1


def test_the_stems_journey_follows_the_stems(conn):
    comp = conn.execute(
        "SELECT c.name FROM journeys j JOIN transformations t "
        "ON t.transformation_id = j.primary_transformation_id "
        "JOIN components c ON c.component_id = t.output_component_id "
        "WHERE j.slug = 'stir_fried_stems'").fetchone()[0]
    assert comp == "stir_fried_broccoli_stem_component"


def test_avocado_fat_is_what_the_flesh_provides_and_the_rest_is_not_food(conn):
    parts = _parts(query.decomposition(conn, "avocado"))
    assert "fat" in parts["flesh"]["provides"]
    assert parts["skin"]["edible"] == parts["stone"]["edible"] == "no"
    assert parts["stone"]["not_food_reason"]
    text = query.render_decomposition(query.decomposition(conn, "avocado"))
    assert "Not food." in text


def test_tomato_parts_lead_somewhere_the_whole_tomato_does_not(conn):
    parts = _parts(query.decomposition(conn, "tomato"))
    assert {x["component"] for x in parts["skin"]["paths"]} == {"tomato_skin_powder_component"}
    assert parts["core"]["edible"] == "conditional"
    assert len(query.decomposition(conn, "tomato")["whole"]) == 12


def test_an_ingredient_without_parts_says_so(conn):
    d = query.decomposition(conn, "kale")
    assert d["parts"] == [] and d["whole"]
    assert "Not decomposed" in query.render_decomposition(d)
    assert query.decomposition(conn, "no_such_thing") is None


# ---- the loader's guards -------------------------------------------------

def _build(data):
    c = sqlite3.connect(":memory:")
    c.row_factory = sqlite3.Row
    loader.rebuild(c)
    loader.populate(c, data, loader.load_vocabulary())
    return c


@pytest.fixture(scope="module")
def base():
    return loader.load_yaml(DATA_PATH)


def _with(base, *, parts=None, transformation=None):
    import copy
    data = copy.deepcopy(base)
    data["journeys"] = []
    if parts is not None:
        data["parts"] = parts
    if transformation is not None:
        data["transformations"] = data["transformations"] + [transformation]
    return data


def _tr(**kw):
    return {"technique": "boil", "output_component": "boiled_potato_component",
            "confidence": "high", **kw}


def test_a_part_of_another_ingredient_is_rejected(base):
    with pytest.raises(LoadError, match="has no part 'stems'"):
        _build(_with(base, transformation=_tr(ingredient="tomato", part="stems")))


def test_processing_a_part_that_is_not_food_is_rejected(base):
    with pytest.raises(LoadError, match="'stone' is not food"):
        _build(_with(base, transformation=_tr(ingredient="avocado", part="stone")))


def test_a_part_must_be_separated_by_a_prep_step(base):
    with pytest.raises(LoadError, match="not a prep modifier"):
        _build(_with(base, parts=[{"ingredient": "kale", "name": "ribs",
                                   "separated_by": "roast"}]))


def test_a_part_that_is_not_food_must_say_why(base):
    with pytest.raises(LoadError, match="needs a not_food_reason"):
        _build(_with(base, parts=[{"ingredient": "kale", "name": "ribs", "edible": "no"}]))
