"""Cucumber — the seventh full ingredient, second Lidl-catalogue expansion.

Cucumber stress-tests the no-cook corner of the model: every state is made
without heat, so water management (salt timing, draining, brine) replaces
heat management. The quick pickle is a flavour state with a not_shelf_stable
risk — never preservation guidance.
"""

from foodprep import query


EXPECTED = {
    "fresh_cucumber_salad": {
        "preparation": "sliced",
        "destination": "salad",
        "phrases": ("dressing late", "weep", "blunt knife"),
    },
    "smashed_cucumber": {
        "preparation": "crushed",
        "destination": "side_dish",
        "phrases": ("ragged", "drain", "over-salting"),
    },
    "quick_pickled_cucumber": {
        "preparation": "sliced",
        "destination": "condiment",
        "phrases": ("brine", "never shelf-stable", "condiment"),
    },
    "chilled_cucumber_soup": {
        "preparation": "grated",
        "destination": "soup",
        "phrases": ("cold flattens", "yogurt", "bendy"),
    },
}


def test_cucumber_has_four_complete_journeys(conn):
    journeys = query.ingredient_journeys(conn, "cucumber")

    assert {j["slug"] for j in journeys} == set(EXPECTED)
    for journey in journeys:
        assert journey["why_choose"]
        assert journey["sensory_change"]
        assert journey["flavour_direction"]
        assert journey["becomes_possible"]
        assert journey["risks"]
        assert journey["transitions"]
        assert journey["useful_additions"]


def test_each_cucumber_journey_is_causal_and_destination_aware(conn):
    for slug, expected in EXPECTED.items():
        journey = query.ingredient_journey(conn, "cucumber", slug)

        assert journey is not None
        assert journey["preparation_id"] == expected["preparation"]
        assert expected["destination"] in journey["destinations"]
        rendered = query.render_journey(journey).lower()
        for phrase in expected["phrases"]:
            assert phrase in rendered


def test_quick_pickle_stays_a_flavour_state_not_preservation(conn):
    row = conn.execute(
        """SELECT t.risks FROM transformations t
           JOIN ingredients i ON i.ingredient_id = t.ingredient_id
           JOIN techniques tech ON tech.technique_id = t.technique_id
           WHERE i.canonical_name = 'cucumber' AND tech.name = 'pickle'"""
    ).fetchone()
    assert row["risks"] == "not_shelf_stable"

    journey = query.ingredient_journey(conn, "cucumber", "quick_pickled_cucumber")
    assert "not preservation" in journey["risks"]


def test_cucumber_states_join_existing_flavour_routes(conn):
    routes = {
        row[0] for row in conn.execute(
            """SELECT fr.route_id FROM flavour_route_states frs
               JOIN flavour_routes fr ON fr.route_id = frs.route_id
               JOIN components c ON c.component_id = frs.component_id
               WHERE c.name IN ('raw_cucumber_component',
                                'salted_cucumber_component')"""
        )
    }
    assert routes == {"creamy_and_acidic", "soy_and_garlic"}


def test_raw_cucumber_generates_the_peach_scout_hypothesis(conn):
    hypotheses = {
        h["candidate"]: h
        for h in query.generate_scout_hypotheses(conn, "raw_cucumber_component")
    }

    peach = hypotheses["peach"]
    assert peach["candidate_class"] == "scout_candidate"
    assert set(peach["matched_dimensions"]) == {"fresh_green", "sweet"}
    assert peach["source"] == "tomato"
    assert "not preservation guidance" in peach["protocol"]["safety_note"]


def test_salted_state_does_not_fire_the_peach_rule(conn):
    """salt_and_drain trades fresh sweetness for concentration: the salted
    state (fresh_green + salty) must not satisfy a rule requiring sweet."""
    candidates = {
        h["candidate"] for h in
        query.generate_scout_hypotheses(conn, "salted_cucumber_component")
    }
    assert "peach" not in candidates
