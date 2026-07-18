"""Rutabaga — the sixth full ingredient and first Lidl-catalogue expansion.

Rutabaga stresses the dense-storage-root states the model lacked: a no-cook
grated slaw, a long hot roast, a boiled-and-dried mash, and a secondary baked
casserole journey. The brassica guardrail applies: raw pungency and old-root
bitterness are risks and tags, never missing roles.
"""

from foodprep import query


EXPECTED = {
    "winter_slaw": {
        "preparation": "grated",
        "destination": "salad",
        "phrases": ("waxy skin", "pungency", "woody"),
    },
    "roasted_cubes": {
        "preparation": "chopped",
        "destination": "side_dish",
        "phrases": ("caramelise", "dense centre", "crowding"),
    },
    "buttery_mash": {
        "preparation": "chopped",
        "destination": "complete_savoury_plate",
        "phrases": ("completely tender", "dry the", "watery"),
    },
    "baked_rutabaga_casserole": {
        "preparation": "crushed",
        "destination": "batch_prepared_ingredient",
        "phrases": ("lanttulaatikko", "browned top", "never sets"),
    },
}


def test_rutabaga_has_four_complete_journeys(conn):
    journeys = query.ingredient_journeys(conn, "rutabaga")

    assert {j["slug"] for j in journeys} == set(EXPECTED)
    for journey in journeys:
        assert journey["why_choose"]
        assert journey["sensory_change"]
        assert journey["flavour_direction"]
        assert journey["becomes_possible"]
        assert journey["risks"]
        assert journey["transitions"]
        assert journey["useful_additions"]


def test_each_rutabaga_journey_is_causal_and_destination_aware(conn):
    for slug, expected in EXPECTED.items():
        journey = query.ingredient_journey(conn, "rutabaga", slug)

        assert journey is not None
        assert journey["preparation_id"] == expected["preparation"]
        assert expected["destination"] in journey["destinations"]
        rendered = query.render_journey(journey).lower()
        for phrase in expected["phrases"]:
            assert phrase in rendered


def test_casserole_is_a_secondary_transition_from_mash(conn):
    journey = query.ingredient_journey(conn, "rutabaga", "baked_rutabaga_casserole")

    assert journey["primary_transformation"] == "mash"
    assert journey["primary_component"] == "mashed_rutabaga_component"
    assert journey["transitions"][0]["from_state"] == "buttery rutabaga mash"
    assert journey["output_state"] == "browned baked rutabaga casserole"


def test_rutabaga_states_join_existing_flavour_routes(conn):
    routes = {
        row[0] for row in conn.execute(
            """SELECT fr.route_id FROM flavour_route_states frs
               JOIN flavour_routes fr ON fr.route_id = frs.route_id
               JOIN components c ON c.component_id = frs.component_id
               WHERE c.name IN ('roasted_rutabaga_component',
                                'raw_rutabaga_slaw_component')"""
        )
    }
    assert routes == {"sour_and_toasted_nut", "creamy_and_acidic"}


def test_mash_generates_the_apricot_scout_hypothesis(conn):
    hypotheses = {
        h["candidate"]: h
        for h in query.generate_scout_hypotheses(conn, "mashed_rutabaga_component")
    }

    apricot = hypotheses["apricot"]
    assert apricot["candidate_class"] == "scout_candidate"
    assert set(apricot["matched_dimensions"]) == {"sweet", "rich_fatty"}
    assert apricot["protocol"]["starting_ratio"].startswith("1 tablespoon")
    assert "not preservation guidance" in apricot["protocol"]["safety_note"]


def test_roasted_rutabaga_inherits_existing_analogy_rules(conn):
    """The toasted-state rules written for broccoli fire for the new root too:
    the analogy engine generalises by state dimensions, not by ingredient."""
    candidates = {
        h["candidate"] for h in
        query.generate_scout_hypotheses(conn, "roasted_rutabaga_component")
    }
    assert "brown_butter" in candidates
    assert "lingonberry_vinegar" in candidates
