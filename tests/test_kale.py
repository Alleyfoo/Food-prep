"""Kale — the eighth full ingredient, third Lidl-catalogue expansion.

Kale is the sturdy leafy green: leaves tough enough to need mechanical or
long-heat breakdown. It earns its place with the massage technique — salt,
oil and acid worked into raw leaves, the no-heat equivalent of cooking —
plus bone-dry chips, fast sauté and silky braise. The brassica guardrail
holds: rawness and bitterness are risks and tags, never missing roles.
"""

from foodprep import query


EXPECTED = {
    "massaged_kale_salad": {
        "preparation": "shredded",
        "destination": "salad",
        "phrases": ("strip", "cell walls", "slimy"),
    },
    "kale_chips": {
        "preparation": "separated",
        "destination": "rice_or_grain_bowl",
        "phrases": ("shatter", "scorched", "soggy"),
    },
    "garlicky_sauteed_kale": {
        "preparation": "chopped",
        "destination": "toast_or_sandwich",
        "phrases": ("wilt", "burnt garlic", "crowding"),
    },
    "braised_kale_and_beans": {
        "preparation": "sliced",
        "destination": "complete_savoury_plate",
        "phrases": ("silky", "squeaky", "muddy"),
    },
}


def test_kale_has_four_complete_journeys(conn):
    journeys = query.ingredient_journeys(conn, "kale")

    assert {j["slug"] for j in journeys} == set(EXPECTED)
    for journey in journeys:
        assert journey["why_choose"]
        assert journey["sensory_change"]
        assert journey["flavour_direction"]
        assert journey["becomes_possible"]
        assert journey["risks"]
        assert journey["transitions"]
        assert journey["useful_additions"]


def test_each_kale_journey_is_causal_and_destination_aware(conn):
    for slug, expected in EXPECTED.items():
        journey = query.ingredient_journey(conn, "kale", slug)

        assert journey is not None
        assert journey["preparation_id"] == expected["preparation"]
        assert expected["destination"] in journey["destinations"]
        rendered = query.render_journey(journey).lower()
        for phrase in expected["phrases"]:
            assert phrase in rendered


def test_massage_is_a_state_change_not_a_modifier(conn):
    row = conn.execute(
        "SELECT is_modifier, heat_type FROM techniques WHERE name = 'massage'"
    ).fetchone()
    assert row["is_modifier"] == 0
    assert row["heat_type"] == "none"

    profile = query.component_state_profile(conn, "massaged_kale_component")
    assert "fresh_green" in profile["flavour_tags"]
    assert "bitter" in profile["flavour_tags"]


def test_kale_states_join_existing_flavour_routes(conn):
    routes = {
        row[0] for row in conn.execute(
            """SELECT fr.route_id FROM flavour_route_states frs
               JOIN flavour_routes fr ON fr.route_id = frs.route_id
               JOIN components c ON c.component_id = frs.component_id
               WHERE c.name IN ('massaged_kale_component',
                                'sauteed_kale_component')"""
        )
    }
    assert routes == {"sour_and_toasted_nut", "soy_and_garlic"}


def test_massaged_kale_generates_the_mango_scout_hypothesis(conn):
    hypotheses = {
        h["candidate"]: h
        for h in query.generate_scout_hypotheses(conn, "massaged_kale_component")
    }

    mango = hypotheses["mango"]
    assert mango["candidate_class"] == "scout_candidate"
    assert set(mango["matched_dimensions"]) == {"fresh_green", "bitter"}
    assert mango["source"] == "apple"
    assert "firm" in mango["protocol"]["smallest_test"]
    assert "not preservation guidance" in mango["protocol"]["safety_note"]


def test_kale_chips_do_not_fire_the_fresh_green_rules(conn):
    """Baking dries away the fresh green dimension: the chips state
    (nutty_toasted + bitter) must not satisfy fresh_green analogies."""
    candidates = {
        h["candidate"] for h in
        query.generate_scout_hypotheses(conn, "crisped_kale_component")
    }
    assert "mango" not in candidates
    assert "peach" not in candidates
