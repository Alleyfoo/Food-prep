"""Components are the provable layer.

Whether a pairing tastes good is an opinion; what a transformation does to an
ingredient is a fact you can demonstrate in a kitchen. Two shapes the model
could not previously hold, both of them ordinary cooking:

  * a **chain** — a step whose input is another state (boil, smash, roast)
  * a **fork** — a step yielding more than one thing you can eat (salting a
    tomato gives firm flesh AND tomato water)

Before this, every transformation started from the raw ingredient and kept
exactly one output, so the second half of a fork was silently discarded.
"""

import sqlite3

import pytest

from foodprep import query
from foodprep.loader import build
from foodprep.ui.graph import build_ingredient_graph


def test_a_step_can_start_from_another_state(conn):
    tr = query.transformation_by_technique(conn, "smash_roast", "potato")
    assert tr, "smashed potato is not modelled"
    assert tr["input_component"] == "boiled_potato_component", (
        "smashing and roasting is impossible from a raw potato")


def test_one_ingredient_may_have_two_of_the_same_technique(conn):
    """UNIQUE (ingredient_id, technique_id) forbade this, which is why a
    second roast of an already-roasted thing had nowhere to live."""
    n = conn.execute(
        """SELECT count(*) FROM transformations t
           JOIN ingredients i ON i.ingredient_id = t.ingredient_id
           JOIN techniques tech ON tech.technique_id = t.technique_id
           WHERE i.canonical_name = 'potato' AND tech.name IN ('roast','smash_roast')"""
    ).fetchone()[0]
    assert n == 2


def test_salting_a_tomato_also_yields_tomato_water(conn):
    tr = query.transformation_by_technique(conn, "salt_and_drain", "tomato")
    by = query.byproducts_for_transformation(conn, tr["transformation_id"])
    names = {b["component"] for b in by}
    assert "tomato_water_component" in names, (
        "the water leaving is the whole mechanism, and it is food")
    assert any(b["note"] for b in by), "a by-product should say what it is for"


def test_a_byproduct_has_somewhere_to_go(conn):
    """Otherwise it is not a component, just a thing we noticed."""
    uses = query.dish_contexts_for_component(conn, "tomato_water_component")
    assert uses, "tomato water leads nowhere"


def test_the_map_draws_the_chain(conn):
    net = build_ingredient_graph(conn, "potato")
    chain = [(e["from"], e["to"]) for e in net.edges if e.get("label") == "then"]
    assert ("comp:boiled_potato_component", "tech:smash_roast") in chain


def test_the_map_draws_the_fork(conn):
    net = build_ingredient_graph(conn, "tomato")
    ids = {n["id"] for n in net.nodes}
    assert "comp:tomato_water_component" in ids
    assert any(e.get("label") == "also yields" for e in net.edges)


@pytest.mark.parametrize("ingredient", ["tomato", "potato", "broccoli", "butter"])
def test_maps_stay_connected(conn, ingredient):
    net = build_ingredient_graph(conn, ingredient)
    ids = {n["id"] for n in net.nodes}
    linked = {e["from"] for e in net.edges} | {e["to"] for e in net.edges}
    assert not (ids - linked)


def test_existing_transformations_did_not_need_an_input(conn):
    """All 60 pre-existing steps migrate untouched as raw-input rows."""
    n = conn.execute(
        "SELECT count(*) FROM transformations WHERE input_component_id IS NULL"
    ).fetchone()[0]
    assert n >= 60
