from foodprep import query


def test_three_initial_routes_load_with_structured_fit(conn):
    count = conn.execute("SELECT count(*) FROM flavour_routes").fetchone()[0]
    assert count == 3

    routes = query.flavour_routes_for_component(conn, "roasted_broccoli_component")
    assert {route["route_id"] for route in routes} == {
        "sour_and_toasted_nut", "creamy_and_acidic"
    }
    for route in routes:
        assert route["fit_reason"]
        assert route["risks"]
        assert route["destinations"]
        assert route["elements"]


def test_available_items_rank_and_partially_satisfy_route(conn):
    routes = query.flavour_routes_for_component(
        conn,
        "stir_fried_broccoli_component",
        ["soy_sauce", "garlic", "rice"],
    )

    route = routes[0]
    assert route["route_id"] == "soy_and_garlic"
    assert route["required_coverage"] == (2, 2)
    assert route["missing_required"] == []
    assert {e["ingredient"] for e in route["available_elements"]} == {
        "soy_sauce", "garlic"
    }


def test_missing_route_elements_are_explicit(conn):
    route = next(
        route for route in query.flavour_routes_for_component(
            conn, "steamed_broccoli_component", ["lemon"]
        )
        if route["route_id"] == "sour_and_toasted_nut"
    )

    assert route["route_id"] == "sour_and_toasted_nut"
    assert route["required_coverage"] == (1, 2)
    assert [e["ingredient"] for e in route["missing_required"]] == ["walnut"]


def test_routes_use_existing_ingredients_only(conn):
    orphan_count = conn.execute(
        "SELECT count(*) FROM flavour_route_elements fre LEFT JOIN ingredients i "
        "ON i.ingredient_id = fre.ingredient_id WHERE i.ingredient_id IS NULL"
    ).fetchone()[0]
    assert orphan_count == 0
