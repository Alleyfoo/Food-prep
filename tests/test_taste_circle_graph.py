"""Tests for the Taste Circle Map graph-data builder (pure, Streamlit-free)."""

import math
import random

import pytest

from foodprep import query
from foodprep.ui.graph import (
    TASTE_DIMENSIONS, _DIM_RX, _DIM_RY, _FADED_FONT, _FAN_RADIUS_MAX,
    _FAN_RADIUS_MIN, _FAN_SPREAD, _MAX_FILLER_NODES, _MORE_SUFFIX, _POSITIVE,
    _fan_page, _pill_extent, random_dish_selections, taste_circle_graph_data,
)

COMPONENT = "roasted_broccoli_component"


def _by_id(data):
    return {n["id"]: n for n in data["nodes"]}


def test_center_and_eleven_dimensions_on_the_ellipse(conn):
    data = taste_circle_graph_data(conn, COMPONENT)
    nodes = _by_id(data)

    center = nodes[f"comp:{COMPONENT}"]
    assert center["x"] == 0.0 and center["y"] == 0.0
    assert center["clickable"] is False

    dim_nodes = [n for n in data["nodes"] if n["id"].startswith("dim:")]
    # Eleven, not ten: fermented_funky must agree with the Taste Circle grid.
    assert len(dim_nodes) == len(TASTE_DIMENSIONS) == 11
    assert "dim:fermented_funky" in nodes
    for n in dim_nodes:
        assert n["fixed"] is True
        # on the ellipse: (x/rx)^2 + (y/ry)^2 == 1
        assert (n["x"] / _DIM_RX) ** 2 + (n["y"] / _DIM_RY) ** 2 == pytest.approx(1.0)


def test_dimensions_are_evenly_stepped(conn):
    """Computed from 360/11, never hand-placed, so a twelfth just works."""
    data = taste_circle_graph_data(conn, COMPONENT)
    nodes = _by_id(data)
    params = []
    for i, (key, *_rest) in enumerate(TASTE_DIMENSIONS):
        n = nodes[f"dim:{key}"]
        params.append(math.atan2(n["y"] / _DIM_RY, n["x"] / _DIM_RX))
    # first node starts at -90 degrees (top of the circle)
    assert params[0] == pytest.approx(-math.pi / 2)
    step = 2 * math.pi / len(TASTE_DIMENSIONS)
    for i in range(1, len(params)):
        delta = (params[i] - params[i - 1]) % (2 * math.pi)
        assert delta == pytest.approx(step)

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
    assert 1 <= len(fillers) <= _MAX_FILLER_NODES + 1  # +1 for the pager
    dim = nodes["dim:sour"]
    radii = set()
    for n in fillers:
        # the fan arcs around its DIMENSION node, not the circle's centre
        radii.add(round(math.hypot(n["x"] - dim["x"], n["y"] - dim["y"]), 3))
        assert n["clickable"] is True
        assert n["shape"] == "box"  # pill, per the addendum
        # id routing format: filler:<dimension>:<name>
        assert n["id"].split(":", 2)[1] == "sour"
    assert len(radii) == 1, "fan nodes must share one arc radius"
    assert radii.pop() >= _FAN_RADIUS_MIN

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


# ---- addendum 2: pills, availability, paging, thin states ------------------

def test_fan_stays_within_the_specced_spread(conn):
    data = taste_circle_graph_data(conn, COMPONENT, expanded_dimension="sour")
    nodes = _by_id(data)
    dim = nodes["dim:sour"]
    ray = math.atan2(dim["y"], dim["x"])
    for n in data["nodes"]:
        if not n["id"].startswith("filler:sour:"):
            continue
        a = math.atan2(n["y"] - dim["y"], n["x"] - dim["x"])
        offset = (a - ray + math.pi) % (2 * math.pi) - math.pi
        assert abs(offset) <= _FAN_SPREAD / 2 + 1e-6


def test_on_hand_fillers_are_flagged_in_the_fan(conn):
    pool = query.taste_circle_fillers(conn, COMPONENT)
    target = pool["sour"][0]["filler"]
    data = taste_circle_graph_data(conn, COMPONENT, expanded_dimension="sour",
                                   available={target})
    nodes = _by_id(data)
    on_hand = nodes[f"filler:sour:{target}"]
    assert on_hand["color"]["background"] == _POSITIVE[200]
    assert on_hand["color"]["border"] == _POSITIVE[500]
    # and a filler that is not on hand keeps the primary tint
    others = [n for n in data["nodes"]
              if n["id"].startswith("filler:sour:") and n["id"] != on_hand["id"]]
    assert others
    assert all(n["color"]["background"] != _POSITIVE[200] for n in others)


def test_long_pool_pages_instead_of_overflowing(conn):
    pool = query.taste_circle_fillers(conn, COMPONENT)
    names = [f["filler"].replace("_", " ") for f in pool["sour"]]
    total = len(names)
    first_page = _fan_page(names, 0)
    assert first_page < total, "sour should need more than one page"

    first = taste_circle_graph_data(conn, COMPONENT, expanded_dimension="sour")
    ids = [n["id"] for n in first["nodes"] if n["id"].startswith("filler:sour:")]
    assert len(ids) == first_page + 1          # + the pager
    assert ids[-1] == f"filler:sour:{_MORE_SUFFIX}"

    second = taste_circle_graph_data(conn, COMPONENT, expanded_dimension="sour",
                                     page=1)
    ids2 = [n["id"] for n in second["nodes"] if n["id"].startswith("filler:sour:")]
    # a genuinely different page, and never the same filler twice
    assert set(ids) & set(ids2) <= {f"filler:sour:{_MORE_SUFFIX}"}


def test_every_filler_is_reachable_by_paging(conn):
    """Paging must eventually show all of them, with none seen twice."""
    pool = query.taste_circle_fillers(conn, COMPONENT)
    expected = {f["filler"] for f in pool["sour"]}
    seen, page, guard = [], 0, 0
    while len(seen) < len(expected) and guard < 40:
        data = taste_circle_graph_data(conn, COMPONENT,
                                       expanded_dimension="sour", page=page)
        got = [n["id"].split(":", 2)[2] for n in data["nodes"]
               if n["id"].startswith("filler:sour:")]
        seen += [g for g in got if g != _MORE_SUFFIX]
        page += 1
        guard += 1
    assert set(seen) == expected
    assert len(seen) == len(set(seen)), "a filler appeared on two pages"


def test_fan_page_respects_the_arc_budget(conn):
    """No page may ask for more arc than the capped radius provides."""
    pool = query.taste_circle_fillers(conn, COMPONENT)
    for dim, fillers in pool.items():
        names = [f["filler"].replace("_", " ") for f in fillers]
        start = 0
        while start < len(names):
            size = _fan_page(names, start)
            assert 1 <= size <= _MAX_FILLER_NODES
            page = names[start:start + size]
            if size > 1:  # a single over-long label is allowed to bust it
                extent = sum(_pill_extent(n) for n in page)
                assert extent <= _FAN_RADIUS_MAX * _FAN_SPREAD + 1e-6
            start += size


def test_paging_wraps(conn):
    pool = query.taste_circle_fillers(conn, COMPONENT)
    names = [f["filler"].replace("_", " ") for f in pool["sour"]]
    pages, cursor = 0, 0
    while cursor < len(names):
        cursor += _fan_page(names, cursor)
        pages += 1
    a = taste_circle_graph_data(conn, COMPONENT, expanded_dimension="sour", page=0)
    b = taste_circle_graph_data(conn, COMPONENT, expanded_dimension="sour",
                                page=pages)
    ids = lambda d: [n["id"] for n in d["nodes"] if n["id"].startswith("filler:")]
    assert ids(a) == ids(b)


def test_dimension_without_fillers_keeps_its_node(conn):
    """"We have nothing here" is information the curator needs to see."""
    data = taste_circle_graph_data(conn, "roasted_broccoli_component")
    nodes = _by_id(data)
    empty = [n for n in data["nodes"]
             if n["id"].startswith("dim:") and "no fillers yet" in n["label"]]
    for n in empty:
        assert n["clickable"] is False
    # every dimension is present regardless
    assert len([n for n in data["nodes"] if n["id"].startswith("dim:")]) == 11


def test_disc_size_encodes_option_count(conn):
    data = taste_circle_graph_data(conn, COMPONENT)
    nodes = _by_id(data)
    pool = query.taste_circle_fillers(conn, COMPONENT)
    thin = nodes["dim:fermented_funky"]      # exactly one option: sauerkraut
    wide = nodes["dim:sour"]                 # the deepest pool
    assert len(pool["fermented_funky"]) == 1
    assert thin["size"] * 2 == pytest.approx(40)   # diameter floor
    assert wide["size"] > thin["size"]
    assert wide["size"] * 2 <= 64 + 1e-6           # diameter ceiling


def test_pill_corner_radius_does_not_inflate_the_bounding_box(conn):
    """vis folds shapeProperties.borderRadius into a node's bounding box.

    A CSS-style 999 therefore reports a ~2000px-wide node, and the graph's
    own fit() zooms everything to a fifth of its size. Half the pill height
    is what a pill actually needs.
    """
    from foodprep.ui.graph import _PILL_RADIUS
    data = taste_circle_graph_data(conn, COMPONENT, expanded_dimension="sour")
    pills = [n for n in data["nodes"] if n["id"].startswith("filler:")]
    assert pills
    for n in pills:
        assert n["shapeProperties"]["borderRadius"] == _PILL_RADIUS
        assert _PILL_RADIUS <= 20, "a radius this large distorts fit()"
