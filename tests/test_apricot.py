"""Apricot — the tenth full ingredient; second stone fruit, modelled separately.

Apricot's state axis is FRESH vs DRIED: fresh is a short summer window for
salads and roasting, dried is the year-round pantry state that cooks INTO
savoury stews (the tagine grammar) rather than being snacked. Dessert drift
stays a risk with salt/heat/acid corrections, per the stone-fruit pattern.
"""

from foodprep import query


EXPECTED = {
    "fresh_apricot_with_cheese": {
        "preparation": "sliced",
        "destination": "salad",
        "phrases": ("floral", "woolly", "dessert"),
    },
    "roasted_apricot_halves": {
        "preparation": "halved",
        "destination": "sauce_or_base",
        "phrases": ("cut side up", "caramelise", "steam instead of browning"),
    },
    "dried_apricot_savoury_stew": {
        "preparation": "whole",
        "destination": "complete_savoury_plate",
        "phrases": ("plump", "tagine", "syrupy"),
    },
    "quick_apricot_compote": {
        "preparation": "chopped",
        "destination": "condiment",
        "phrases": ("skins", "spoonable", "jam"),
    },
}


def test_apricot_has_four_complete_journeys(conn):
    journeys = query.ingredient_journeys(conn, "apricot")

    assert {j["slug"] for j in journeys} == set(EXPECTED)
    for journey in journeys:
        assert journey["why_choose"]
        assert journey["sensory_change"]
        assert journey["flavour_direction"]
        assert journey["becomes_possible"]
        assert journey["risks"]
        assert journey["transitions"]
        assert journey["useful_additions"]


def test_each_apricot_journey_is_causal_and_destination_aware(conn):
    for slug, expected in EXPECTED.items():
        journey = query.ingredient_journey(conn, "apricot", slug)

        assert journey is not None
        assert journey["preparation_id"] == expected["preparation"]
        assert expected["destination"] in journey["destinations"]
        rendered = query.render_journey(journey).lower()
        for phrase in expected["phrases"]:
            assert phrase in rendered


def test_dried_is_a_savoury_ingredient_not_a_snack(conn):
    """The dried state's missing roles point at stew-building (aromatic,
    body, umami, heat) — the model treats it as a cooking ingredient."""
    profile = query.component_state_profile(conn, "dried_apricot_component")
    assert "sweet" in profile["flavour_tags"]
    assert "chewy" in profile["texture_tags"]

    journey = query.ingredient_journey(conn, "apricot", "dried_apricot_savoury_stew")
    assert journey["primary_component"] == "dried_apricot_component"
    assert journey["transitions"][0]["from_state"] == "dried apricots"


def test_apricot_states_join_existing_flavour_routes(conn):
    routes = {
        row[0] for row in conn.execute(
            """SELECT fr.route_id FROM flavour_route_states frs
               JOIN flavour_routes fr ON fr.route_id = frs.route_id
               JOIN components c ON c.component_id = frs.component_id
               WHERE c.name IN ('roasted_apricot_component',
                                'apricot_compote_component')"""
        )
    }
    assert routes == {"sour_and_toasted_nut", "creamy_and_acidic"}


def test_roasted_apricot_generates_the_rye_crumb_hypothesis(conn):
    hypotheses = {
        h["candidate"]: h
        for h in query.generate_scout_hypotheses(conn, "roasted_apricot_component")
    }

    rye = hypotheses["rye_crumbs"]
    assert rye["candidate_class"] == "scout_candidate"
    assert set(rye["matched_dimensions"]) == {"sweet", "nutty_toasted"}
    assert rye["source"] == "walnut"
    assert rye["mechanism"] == "flavour_reinforcement"
    assert "not preservation guidance" in rye["protocol"]["safety_note"]


def test_pantry_fats_pair_with_existing_states(conn):
    """The user's actual pantry (ghee, garlic butter) is wired into the
    catalogue's states as Cook-side pairings, not Scout hypotheses."""
    rows = conn.execute(
        """SELECT i.canonical_name AS filler, ti.canonical_name AS target,
                  p.confidence
           FROM pairings p
           JOIN ingredients i ON i.ingredient_id = p.ingredient_id
           LEFT JOIN transformations t
             ON t.transformation_id = p.works_best_with_transformation_id
           LEFT JOIN ingredients ti ON ti.ingredient_id = t.ingredient_id
           WHERE i.canonical_name IN ('ghee', 'garlic_butter')"""
    ).fetchall()

    pairs = {(r["filler"], r["target"]) for r in rows}
    assert ("ghee", "broccoli") in pairs
    assert ("ghee", "kale") in pairs
    assert ("garlic_butter", "broccoli") in pairs
    assert ("garlic_butter", "rutabaga") in pairs
    assert all(r["confidence"] != "experimental" for r in rows)
