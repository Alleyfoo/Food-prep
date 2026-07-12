import pytest

from foodprep import query
from foodprep.cli import build_parser


def test_complete_plate_preserves_legacy_target(conn):
    result = query.plate_balance_detail(conn, "mashed potatoes")

    assert result["destination_id"] == "complete_savoury_plate"
    assert result["destination"]["required"] == query.TARGET_ROLES
    assert result["target_gap"] == ["acid", "herb", "crunch", "protein"]


def test_side_dish_does_not_require_carb_or_protein(conn):
    result = query.plate_balance_detail(
        conn, "broccoli", destination_id="side_dish"
    )

    assert result["target_gap"] == ["salt"]
    assert "acid" in result["useful_gap"]
    assert "fat" in result["useful_gap"]
    assert "carb" not in result["target_gap"]
    assert "protein" not in result["target_gap"]


def test_soup_requires_hydration_seasoning_and_body(conn):
    result = query.plate_balance_detail(
        conn, "onion", destination_id="soup"
    )

    assert result["destination"]["required"] == ["hydration", "salt", "body"]
    assert result["target_gap"] == ["hydration", "salt", "body"]
    assert "crunch" not in result["target_gap"]
    assert "protein" not in result["target_gap"]


def test_destination_output_explains_contextual_gap(conn):
    output = query.plate_balance(conn, "broccoli", "side_dish")

    assert "Destination: Side dish" in output
    assert "required for this destination: salt" in output
    assert "useful but not required here:" in output


def test_unknown_destination_is_rejected(conn):
    with pytest.raises(ValueError, match="unknown or unmodelled destination"):
        query.plate_balance_detail(conn, "broccoli", destination_id="banquet")


def test_plate_cli_accepts_destination():
    args = build_parser().parse_args(
        ["plate", "--destination", "side_dish", "broccoli"]
    )

    assert args.destination == "side_dish"
    assert args.prompt == ["broccoli"]
