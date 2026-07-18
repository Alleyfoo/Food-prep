"""The Lidl-available base catalogue.

The product focus is a small set of items the user can actually buy at the
local Lidl, turned into components and balanced food ideas. These tests pin
that every catalogue item exists in the ontology with FI availability and at
least one culinary role, so the available_* filter can work against the real
shopping list.
"""

LIDL_CATALOGUE = [
    "broccoli", "rutabaga", "greens", "corn", "tomato", "avocado",
    "kale", "cucumber", "mango", "apricot", "peach",
]


def test_lidl_catalogue_items_exist_with_fi_availability(conn):
    for name in LIDL_CATALOGUE:
        row = conn.execute(
            "SELECT ingredient_id, base_roles FROM ingredients "
            "WHERE canonical_name = ?", (name,),
        ).fetchone()
        assert row is not None, f"catalogue item missing from ontology: {name}"
        assert row["base_roles"], f"catalogue item has no culinary role: {name}"
        availability = conn.execute(
            "SELECT availability_class FROM availability "
            "WHERE ingredient_id = ? AND region_code = 'FI'",
            (row["ingredient_id"],),
        ).fetchone()
        assert availability is not None, f"no FI availability row: {name}"


def test_salad_is_an_alias_of_greens(conn):
    aliases = conn.execute(
        "SELECT aliases FROM ingredients WHERE canonical_name = 'greens'"
    ).fetchone()[0]
    assert "salad" in aliases.split("\n")
