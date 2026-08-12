"""Tests for the Taste Circle Map graph-data builder (pure, Streamlit-free)."""

import math
import random

import pytest

from foodprep import query
from foodprep.ui.graph import (
    TASTE_DIMENSIONS, _DIM_RADIUS, _FADED_FONT, _FILLER_RADIUS,
    _MAX_FILLER_NODES, random_dish_selections, taste_circle_graph_data,
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


# ---- fade-out on expansion -------------------------------------------------

def test_expanded_dimension_fades_everything_else(conn):
    data = taste_circle_graph_data(conn, COMPONENT, expanded_dimension="sour")
    nodes = _by_id(data)

    # centre and expanded dimension stay vivid
    assert nodes[f"comp:{COMPONENT}"]["font"]["color"] != _FADED_FONT
    assert nodes["dim:sour"]["font"]["color"] != _FADED_FONT

    # every other dimension is faded
    for dim_key, _icon, _name, _color in TASTE_DIMENSIONS:
        if dim_key != "sour":
            assert nodes[f"dim:{dim_key}"]["font"]["color"] == _FADED_FONT

    # filler fan nodes stay vivid
    fan = [n for n in data["nodes"] if n["id"].startswith("filler:sour:")]
    assert fan
    for n in fan:
        assert n["font"]["color"] != _FADED_FONT


def test_faded_dimensions_stay_clickable(conn):
    data = taste_circle_graph_data(conn, COMPONENT, expanded_dimension="sour")
    nodes = _by_id(data)
    # available dims remain clickable so focus can move to them
    assert nodes["dim:salty"]["clickable"] is True
    # provided dims were never clickable and stay that way
    assert nodes["dim:umami"]["clickable"] is False


def test_no_expansion_no_fade(conn):
    data = taste_circle_graph_data(conn, COMPONENT)
    for n in data["nodes"]:
        assert (n.get("font") or {}).get("color") != _FADED_FONT


# ---- random dish -----------------------------------------------------------

def test_random_dish_picks_one_per_open_dimension(conn):
    pool = query.taste_circle_fillers(conn, COMPONENT)
    picks = random_dish_selections(pool, rng=random.Random(42))
    assert set(picks) == set(pool)  # every open dimension filled
    for dim, filler in picks.items():
        valid = [f["filler"] for f in pool[dim]]
        assert filler in valid
    # no filler used twice
    assert len(set(picks.values())) == len(picks)


def test_random_dish_skips_locked_dimensions(conn):
    pool = query.taste_circle_fillers(conn, COMPONENT, {"salty"})
    picks = random_dish_selections(pool, {"salty": "soy_sauce"},
                                   rng=random.Random(7))
    assert "salty" not in picks
    assert "soy_sauce" not in picks.values()


def test_random_dish_picks_from_most_common_slice(conn):
    pool = query.taste_circle_fillers(conn, COMPONENT)
    picks = random_dish_selections(pool, top_n=3, rng=random.Random(1))
    for dim, filler in picks.items():
        top = [f["filler"] for f in pool[dim][:3]]
        assert filler in top


def test_random_dish_never_reuses_a_contested_filler(conn):
    pool = {
        "sour": [{"filler": "lemon"}, {"filler": "vinegar"}],
        "aromatic": [{"filler": "lemon"}, {"filler": "dill"}],
    }
    picks = random_dish_selections(pool, rng=random.Random(3))
    assert set(picks) == {"sour", "aromatic"}
    assert len(set(picks.values())) == 2
