"""Tests for the Taste Circle Map graph-data builder (pure, Streamlit-free)."""

import math

import pytest

from foodprep import query
from foodprep.ui.graph import (
    TASTE_DIMENSIONS, _DIM_RADIUS, _FILLER_RADIUS, _MAX_FILLER_NODES,
    taste_circle_graph_data,
)

COMPONENT = "roasted_broccoli_component"


def _by_id(data):
    return {n["id"]: n for n in data["nodes"]}


def test_center_and_dimensions_on_a_true_circle(conn):
    data = taste_circle_graph_data(conn, COMPONENT)
    nodes = _by_id(data)

    center = nodes[f"comp:{COMPONENT}"]
    assert center["x"] == 0.0 and center["y"] == 0.0
    assert center["clickable"] is False

    dim_nodes = [n for n in data["nodes"] if n["id"].startswith("dim:")]
    assert len(dim_nodes) == len(TASTE_DIMENSIONS) == 11
    for n in dim_nodes:
        assert n["fixed"] is True
        assert math.hypot(n["x"], n["y"]) == pytest.approx(_DIM_RADIUS)

    # one edge from the centre to each dimension, nothing else
    assert len(data["edges"]) == 11
    assert all(e["from"] == f"comp:{COMPONENT}" for e in data["edges"])


def test_provided_dimensions_are_visual_only(conn):
    # roasted broccoli provides nutty_toasted, sweet, umami
    data = taste_circle_graph_data(conn, COMPONENT)
    nodes = _by_id(data)
    for dim in ("nutty_toasted", "sweet", "umami"):
        node = nodes[f"dim:{dim}"]
        assert "provided" in node["label"]
        assert node["clickable"] is False

    sour = nodes["dim:sour"]
    assert sour["clickable"] is True
    assert "options" in sour["label"]


def test_no_filler_nodes_without_expansion(conn):
    data = taste_circle_graph_data(conn, COMPONENT)
    assert not any(n["id"].startswith("filler:") for n in data["nodes"])


def test_expanded_dimension_shows_filler_fan(conn):
    data = taste_circle_graph_data(conn, COMPONENT, expanded_dimension="sour")
    nodes = _by_id(data)

    fillers = [n for n in data["nodes"] if n["id"].startswith("filler:sour:")]
    assert 1 <= len(fillers) <= _MAX_FILLER_NODES
    for n in fillers:
        assert math.hypot(n["x"], n["y"]) == pytest.approx(_FILLER_RADIUS)
        assert n["clickable"] is True
        # id routing format: filler:<dimension>:<name>
        assert n["id"].split(":", 2)[1] == "sour"

    fan_edges = [e for e in data["edges"]
                 if e["from"] == "dim:sour" and e["to"].startswith("filler:sour:")]
    assert len(fan_edges) == len(fillers)

    # expanded label reports "shown of total"
    assert "of" in nodes["dim:sour"]["label"]


def test_fan_excludes_fillers_already_chosen(conn):
    # lemon locked under salty must not reappear as an option in sour's fan
    data = taste_circle_graph_data(
        conn, COMPONENT,
        locked_dimensions={"salty"},
        selections={"salty": "lemon"},
        expanded_dimension="sour",
    )
    assert "filler:sour:lemon" not in _by_id(data)


def test_locked_dimension_shows_choice_and_is_reopenable(conn):
    data = taste_circle_graph_data(
        conn, COMPONENT,
        locked_dimensions={"salty"},
        selections={"salty": "soy_sauce"},
    )
    node = _by_id(data)["dim:salty"]
    assert "🔒" in node["label"]
    assert "soy sauce" in node["label"]
    # stays clickable so the user can click to unlock/change
    assert node["clickable"] is True
    assert not any(n["id"].startswith("filler:salty:") for n in data["nodes"])


def test_locked_dimension_leaves_filler_pool(conn):
    open_pool = query.taste_circle_fillers(conn, COMPONENT)
    assert "salty" in open_pool
    locked_pool = query.taste_circle_fillers(conn, COMPONENT, {"salty"})
    assert "salty" not in locked_pool
