"""The pyvis graphs must actually wear the design system.

These pin two pyvis 0.3.2 behaviours that silently swallowed our styling:

  * ``Network.add_node`` drops the ``color`` argument entirely for any node
    that carries a ``group``, falling back to vis.js's default palette.
  * ``Network(font_color=...)`` replaces each node's whole ``font`` dict with
    ``{"color": font_color}``, losing the face and size.

Both failed silently — the graphs rendered, just in the wrong colours and
in Arial — so they are worth a test rather than a comment.
"""

import pytest

from foodprep.ui.graph import (
    _COLORS, _EDGE_COLORS, _FONT_FACE, build_ingredient_graph,
    build_scout_graph, graph_to_html,
)

#: vis.js's own group palette — the tell that our colours were dropped.
VIS_DEFAULTS = {"#97C2FC", "#FFFF00", "#FB7E81", "#7BE141", "#EB7DF4", "#AD85E4"}


@pytest.fixture(params=["broccoli", "tomato"])
def net(conn, request):
    return build_ingredient_graph(conn, request.param)


def test_every_node_uses_our_palette(net):
    palette = set(_COLORS.values())
    for node in net.nodes:
        assert node["color"] in palette, f"{node['id']} has stray colour {node['color']}"
        assert node["color"] not in VIS_DEFAULTS


def test_group_is_not_forwarded_to_pyvis(net):
    # pyvis discards `color` for grouped nodes, so `group` must not reach it.
    for node in net.nodes:
        assert "group" not in node, f"{node['id']} forwards group and loses its colour"


def test_node_font_survives(net):
    for node in net.nodes:
        assert node["font"]["face"] == _FONT_FACE
        assert node["font"]["size"] >= 14
        assert node["font"]["color"] == "#1A1B16"


def test_edges_use_our_palette(net):
    allowed = set(_EDGE_COLORS.values()) | {"#D2CDBE"}
    for edge in net.edges:
        assert edge["color"] in allowed, f"stray edge colour {edge['color']}"


def test_scout_graph_is_styled_too(conn):
    scout = build_scout_graph(conn, "broccoli")
    palette = set(_COLORS.values()) | {"#75796E"}
    for node in scout.nodes:
        assert "group" not in node
        assert node["color"] in palette
        assert node["font"]["face"] == _FONT_FACE


def test_graph_html_carries_the_font(conn):
    # The graph renders in its own iframe, beyond the app stylesheet's reach.
    html = graph_to_html(build_ingredient_graph(conn, "broccoli"))
    assert "Figtree" in html
    assert html.count("fonts.googleapis.com") >= 1
