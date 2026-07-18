import sqlite3

from foodprep import query
from foodprep.cli import build_parser


EXPECTED = {
    "stir_fried_stems": {
        "preparation": "sliced",
        "destination": "noodles",
        "phrases": ("surface area", "vinegar", "fibrous"),
    },
    "roasted_florets": {
        "preparation": "separated",
        "destination": "side_dish",
        "phrases": ("dry heat", "toasted", "scorched"),
    },
    "steamed_cold_side": {
        "preparation": "separated",
        "destination": "salad",
        "phrases": ("rapid cooling", "tender-crisp", "over-steaming"),
    },
    "crushed_roasted_broccoli": {
        "preparation": "crushed",
        "destination": "sauce_or_base",
        "phrases": ("spoonable", "leftover", "over-processing"),
    },
}


def test_broccoli_has_four_complete_journeys(conn):
    journeys = query.ingredient_journeys(conn, "broccoli")

    assert {j["slug"] for j in journeys} == set(EXPECTED)
    for journey in journeys:
        assert journey["why_choose"]
        assert journey["sensory_change"]
        assert journey["flavour_direction"]
        assert journey["becomes_possible"]
        assert journey["risks"]
        assert journey["transitions"]
        assert journey["useful_additions"]


def test_each_broccoli_journey_is_causal_and_destination_aware(conn):
    for slug, expected in EXPECTED.items():
        journey = query.ingredient_journey(conn, "broccoli", slug)

        assert journey is not None
        assert journey["preparation_id"] == expected["preparation"]
        assert expected["destination"] in journey["destinations"]
        rendered = query.render_journey(journey).lower()
        for phrase in expected["phrases"]:
            assert phrase in rendered
        assert "why choose it:" in rendered
        assert "what changes:" in rendered
        assert "what becomes possible:" in rendered
        assert "watch for:" in rendered


def test_crushed_route_is_an_explicit_secondary_transition(conn):
    journey = query.ingredient_journey(conn, "broccoli", "crushed_roasted_broccoli")

    assert journey["primary_transformation"] == "roast"
    assert journey["primary_component"] == "roasted_broccoli_component"
    assert journey["transitions"][0]["from_state"] == "browned roasted broccoli florets"
    assert journey["transitions"][0]["move"] == "crush while warm"
    assert journey["output_state"] == "coarse roasted broccoli paste"


def test_journey_references_existing_transformations(conn):
    orphan_count = conn.execute(
        "SELECT count(*) FROM journeys j LEFT JOIN transformations t "
        "ON t.transformation_id = j.primary_transformation_id "
        "WHERE t.transformation_id IS NULL"
    ).fetchone()[0]

    assert orphan_count == 0
    assert conn.execute("SELECT count(*) FROM transformations").fetchone()[0] == 46


def test_journey_cli_parser_supports_all_or_one_path():
    parser = build_parser()

    all_paths = parser.parse_args(["journey", "broccoli"])
    one_path = parser.parse_args(["journey", "broccoli", "steamed_cold_side"])
    assert all_paths.ingredient == "broccoli"
    assert all_paths.slug is None
    assert one_path.slug == "steamed_cold_side"


def test_unknown_journey_is_reported_honestly(conn):
    assert query.ingredient_journey(conn, "broccoli", "deep_fried") is None
    assert query.render_ingredient_journeys(conn, "broccoli", "deep_fried") == (
        "No journey named 'deep_fried' for 'broccoli'."
    )
