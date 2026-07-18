"""Mango — the ninth full ingredient; stone fruit modelled separately.

The user's call: each stone fruit is its own culinary object. Mango's state
axis is ripeness, not heat — firm green mango is a crunchy sour vegetable
(slaw), ripe mango is a silky sweet fruit (chile-salt, salsa, lassi). blend
is the genuinely new state: a drinkable destination. Dessert drift is the
recurring risk; salt, chile and acid are the standing corrections.
"""

from foodprep import query


EXPECTED = {
    "chili_salt_mango": {
        "preparation": "sliced",
        "destination": "salad",
        "phrases": ("ripeness", "chile", "dessert"),
    },
    "green_mango_slaw": {
        "preparation": "shredded",
        "destination": "side_dish",
        "phrases": ("underripe", "sour vegetable", "mush"),
    },
    "mango_salsa": {
        "preparation": "chopped",
        "destination": "condiment",
        "phrases": ("pico de gallo", "weeps", "jam"),
    },
    "mango_lassi": {
        "preparation": "chopped",
        "destination": "drink",
        "phrases": ("salted", "cloying", "yogurt"),
    },
}


def test_mango_has_four_complete_journeys(conn):
    journeys = query.ingredient_journeys(conn, "mango")

    assert {j["slug"] for j in journeys} == set(EXPECTED)
    for journey in journeys:
        assert journey["why_choose"]
        assert journey["sensory_change"]
        assert journey["flavour_direction"]
        assert journey["becomes_possible"]
        assert journey["risks"]
        assert journey["transitions"]
        assert journey["useful_additions"]


def test_each_mango_journey_is_causal_and_destination_aware(conn):
    for slug, expected in EXPECTED.items():
        journey = query.ingredient_journey(conn, "mango", slug)

        assert journey is not None
        assert journey["preparation_id"] == expected["preparation"]
        assert expected["destination"] in journey["destinations"]
        rendered = query.render_journey(journey).lower()
        for phrase in expected["phrases"]:
            assert phrase in rendered


def test_ripeness_is_the_state_axis(conn):
    """The same fruit is two culinary objects: firm green mango is a sour
    crunchy vegetable, ripe mango is a silky sweet fruit."""
    green = query.component_state_profile(conn, "green_mango_slaw_component")
    ripe = query.component_state_profile(conn, "ripe_mango_component")

    assert "sour" in green["flavour_tags"]
    assert "fresh_green" in green["flavour_tags"]
    assert "crunchy" in green["texture_tags"]
    assert "aromatic" in ripe["flavour_tags"]
    assert "silky" in ripe["texture_tags"]
    assert "fresh_green" not in ripe["flavour_tags"]


def test_lassi_reaches_the_new_drink_destination(conn):
    row = conn.execute(
        "SELECT is_modifier, heat_type FROM techniques WHERE name = 'blend'"
    ).fetchone()
    assert row["is_modifier"] == 0
    assert row["heat_type"] == "none"

    journey = query.ingredient_journey(conn, "mango", "mango_lassi")
    assert journey["destinations"] == ["drink"]


def test_mango_states_join_existing_flavour_routes(conn):
    routes = {
        row[0] for row in conn.execute(
            """SELECT fr.route_id FROM flavour_route_states frs
               JOIN flavour_routes fr ON fr.route_id = frs.route_id
               JOIN components c ON c.component_id = frs.component_id
               WHERE c.name IN ('green_mango_slaw_component',
                                'mango_lassi_base')"""
        )
    }
    assert routes == {"sour_and_toasted_nut", "creamy_and_acidic"}


def test_green_slaw_generates_the_lingonberry_scout_hypothesis(conn):
    hypotheses = {
        h["candidate"]: h
        for h in query.generate_scout_hypotheses(conn, "green_mango_slaw_component")
    }

    lingonberry = hypotheses["lingonberry_vinegar"]
    assert lingonberry["candidate_class"] == "scout_candidate"
    assert set(lingonberry["matched_dimensions"]) == {"sour", "fresh_green"}
    assert lingonberry["source"] == "lime"
    assert "not preservation guidance" in lingonberry["protocol"]["safety_note"]


def test_ripe_state_does_not_fire_the_sour_slaw_rule(conn):
    """Ripeness trades fresh_green away: the ripe state must not satisfy the
    sour-slaw analogy written for the firm green state."""
    candidates = {
        h["candidate"] for h in
        query.generate_scout_hypotheses(conn, "ripe_mango_component")
    }
    assert "lingonberry_vinegar" not in candidates
