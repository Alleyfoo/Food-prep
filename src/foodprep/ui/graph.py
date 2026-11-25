"""Build interactive ingredient mindmaps using pyvis (vis.js).

Generates a force-directed graph for one ingredient showing:
  ingredient → techniques → components → fillers / routes / destinations

Rendered as self-contained HTML and embedded in Streamlit via
``st.components.v1.html()``.

Also holds ``taste_circle_graph_data`` — the pure (Streamlit-free) data
builder for the Taste Circle Map custom component, whose nodes/edges are
rendered by ``ui/taste_circle_component/index.html``.
"""

from __future__ import annotations

import json
import math
import random
import sqlite3
from typing import Any

from pyvis.network import Network

from foodprep import query


#: Node fills — the 500 step of each categorical ramp in design.css. Our five
#: hues at one shared lightness/chroma, so no node type shouts over another.
#: Keep in step with :root there; regenerate both via scripts/gen_palette.py.
_COLORS = {
    "ingredient": "#3F9A6F",
    "technique":  "#5E86C8",
    "component":  "#A56FAD",
    "filler":     "#A77F2C",
    "route":      "#A77F2C",
    "destination": "#BE6879",
    "hypothesis": "#A56FAD",
    "dimension":  "#5E86C8",
}

#: Edges sit one step darker than their node so they read on the oat ground.
_EDGE_COLORS = {
    "ingredient": "#1C7B53",
    "technique":  "#4368A6",
    "component":  "#86528D",
    "filler":     "#876105",
    "destination": "#9C4C5D",
}

#: Structure, from design.css (pantry palette): oat page, sage ink and lines.
_BG = "#F5F5EB"          # --bg; faded circle nodes blend toward it
_INK = "#24291D"         # --ink
_SECONDARY = "#5D634B"   # --ink-4: unclassified nodes, edge labels
_LINE = "#CDD2BA"        # --line-2: plain edges

_FONT_FACE = "Figtree, system-ui, sans-serif"

_UNIVERSAL_FILLERS = {
    "sea_salt", "olive_oil", "lemon", "black_pepper",
}


def _add_node(net: Network, node_id: str, label: str, group: str,
              size: int = 20, title: str = "", color: str | None = None,
              shape: str | None = None) -> None:
    """Add one node, styled from the categorical ramps.

    ``group`` stays a Python-level concept and is deliberately NOT forwarded
    to pyvis: ``Network.add_node`` drops the ``color`` argument outright for
    any node carrying a group (see pyvis 0.3.2), which silently handed these
    graphs vis.js's default palette instead of ours.
    """
    node_color = color if color is not None else _COLORS.get(group, _SECONDARY)
    node_shape = shape if shape is not None else {"technique": "diamond", "route": "square",
              "destination": "triangle"}.get(group, "dot")
    net.add_node(
        node_id, label=label, color=node_color, size=size, shape=node_shape,
        title=title or label,
        font={"color": _INK, "size": 14, "face": _FONT_FACE},
    )


def _add_edge(net: Network, src: str, dst: str, label: str = "",
              color: str = _LINE, dashes: bool = False) -> None:
    net.add_edge(src, dst, label=label, color=color, dashes=dashes,
                 font={"color": _SECONDARY, "size": 12, "face": _FONT_FACE,
                        "align": "middle"},
                 width=2)


def build_ingredient_graph(conn: sqlite3.Connection,
                           ingredient: str) -> Network:
    """Build a pyvis Network for one ingredient's transformation tree + connections."""
    # font_color must stay falsy: pyvis replaces each node's whole `font`
    # dict with {"color": font_color} when it is set, losing face and size.
    net = Network(height="600px", width="100%", bgcolor=_BG,
                  font_color=False, directed=True)
    net.barnes_hut(gravity=-3000, central_gravity=0.3, spring_length=120,
                   spring_strength=0.05, damping=0.09, overlap=0)

    _add_node(net, f"ing:{ingredient}", ingredient, "ingredient", size=35,
              title=f"Ingredient: {ingredient}")

    techs = query.techniques_for_ingredient(conn, ingredient)
    for tech in techs:
        tech_id = f"tech:{tech}"
        _add_node(net, tech_id, tech.replace("_", " "), "technique", size=18,
                  title=f"Technique: {tech}")
        _add_edge(net, f"ing:{ingredient}", tech_id, "via", color=_EDGE_COLORS["ingredient"])

        tr = query.transformation_by_technique(conn, tech, ingredient)
        if not tr:
            continue
        comp_name = tr.get("output_component") or tr.get("component")
        if not comp_name:
            continue

        comp_id = f"comp:{comp_name}"
        if comp_id not in [n["id"] for n in net.nodes]:
            _add_node(net, comp_id, query.state_label(comp_name), "component",
                      size=22, title=f"Component: {comp_name}")
        _add_edge(net, tech_id, comp_id, "produces", color=_EDGE_COLORS["technique"])

        # A step that starts from another state rather than the raw
        # ingredient (boiled potato -> smashed and roasted). Drawing the input
        # is what makes a chain read as a chain instead of a second technique
        # hanging off the root.
        input_name = tr.get("input_component")
        if input_name:
            input_id = f"comp:{input_name}"
            if input_id not in [n["id"] for n in net.nodes]:
                _add_node(net, input_id, query.state_label(input_name),
                          "component", size=22, title=f"Component: {input_name}")
            _add_edge(net, input_id, tech_id, "then",
                      color=_EDGE_COLORS["component"])

        # Everything else the step yields, which is usually also food.
        for by in query.byproducts_for_transformation(conn, tr["transformation_id"]):
            by_id = f"comp:{by['component']}"
            if by_id not in [n["id"] for n in net.nodes]:
                _add_node(net, by_id, query.state_label(by["component"]),
                          "component", size=18,
                          title=by.get("note") or f"Component: {by['component']}")
            _add_edge(net, tech_id, by_id, "also yields",
                      color=_EDGE_COLORS["technique"], dashes=True)
            for use in query.dish_contexts_for_component(conn, by["component"]):
                use_id = f"dest:{use}"
                if use_id not in [n["id"] for n in net.nodes]:
                    _add_node(net, use_id, use.replace("_", " "), "destination",
                              size=12, title=f"Eaten as: {use.replace('_', ' ')}")
                _add_edge(net, by_id, use_id, "used in",
                          color=_EDGE_COLORS["destination"], dashes=True)

        card = query.branch_card(conn, ingredient, tech)
        if card:
            seen_fillers: set[str] = set()
            for role, fillers in (card.get("fillers_by_role") or {}).items():
                for f in fillers[:3]:
                    fname = f["filler"]
                    if fname in seen_fillers or fname in _UNIVERSAL_FILLERS:
                        continue
                    seen_fillers.add(fname)
                    filler_id = f"fill:{fname}"
                    if filler_id not in [n["id"] for n in net.nodes]:
                        _add_node(net, filler_id, fname.replace("_", " "),
                                  "filler", size=10,
                                  title=f"Filler: {fname} ({role})")
                    _add_edge(net, comp_id, filler_id, role,
                              color=_EDGE_COLORS["filler"], dashes=True)

        # Where this state actually gets eaten. Only route destinations were
        # drawn before, so a state with no route — raw broccoli, which lists
        # bowl/dip/salad/sandwich — appeared to lead nowhere.
        for use in (card.get("uses") if card else []) or []:
            use_id = f"dest:{use}"
            if use_id not in [n["id"] for n in net.nodes]:
                _add_node(net, use_id, use.replace("_", " "), "destination",
                          size=12, title=f"Eaten as: {use.replace('_', ' ')}")
            _add_edge(net, comp_id, use_id, "used in",
                      color=_EDGE_COLORS["destination"], dashes=True)

        routes = query.flavour_routes_for_component(conn, comp_name)
        for route in routes:
            route_id = f"route:{route['route_id']}"
            if route_id not in [n["id"] for n in net.nodes]:
                _add_node(net, route_id, route["name"].replace("_", " "),
                          "route", size=14,
                          title=f"Route: {route['name']}")
            _add_edge(net, comp_id, route_id, "route", color=_EDGE_COLORS["filler"])

            for dest in (route.get("destinations") or []):
                dest_id = f"dest:{dest}"
                if dest_id not in [n["id"] for n in net.nodes]:
                    _add_node(net, dest_id, dest.replace("_", " "),
                              "destination", size=12,
                              title=f"Destination: {dest}")
                _add_edge(net, route_id, dest_id, "", color=_EDGE_COLORS["destination"])

    # Journey destinations, joined to the state the journey produces. These
    # used to be added as free-floating nodes with no edges at all.
    for j in query.ingredient_journeys(conn, ingredient):
        tr = query.transformation_by_technique(
            conn, j["primary_transformation"], ingredient)
        comp_name = (tr or {}).get("output_component") or (tr or {}).get("component")
        if not comp_name:
            continue
        comp_id = f"comp:{comp_name}"
        for dest in (j.get("destinations") or []):
            dest_id = f"dest:{dest}"
            if dest_id not in [n["id"] for n in net.nodes]:
                _add_node(net, dest_id, dest.replace("_", " "),
                          "destination", size=12,
                          title=f"Destination: {dest.replace('_', ' ')}")
            if comp_id in [n["id"] for n in net.nodes]:
                _add_edge(net, comp_id, dest_id, "becomes",
                          color=_EDGE_COLORS["destination"], dashes=True)

    net.show_buttons(filter_=["physics"])
    return net


def build_scout_graph(conn: sqlite3.Connection,
                      ingredient: str) -> Network:
    """Build a pyvis Network showing Scout hypotheses for an ingredient's components.

    Shows: ingredient → techniques → components → Scout hypotheses (candidates)
    Hypotheses are color-coded by candidate_class and show analogy/trial status.
    """
    # font_color must stay falsy: pyvis replaces each node's whole `font`
    # dict with {"color": font_color} when it is set, losing face and size.
    net = Network(height="600px", width="100%", bgcolor=_BG,
                  font_color=False, directed=True)
    net.barnes_hut(gravity=-3000, central_gravity=0.3, spring_length=120,
                   spring_strength=0.05, damping=0.09, overlap=0)

    _add_node(net, f"ing:{ingredient}", ingredient, "ingredient", size=35,
              title=f"Ingredient: {ingredient}")

    techs = query.techniques_for_ingredient(conn, ingredient)
    for tech in techs:
        tech_id = f"tech:{tech}"
        _add_node(net, tech_id, tech.replace("_", " "), "technique", size=18,
                  title=f"Technique: {tech}")
        _add_edge(net, f"ing:{ingredient}", tech_id, "via", color=_EDGE_COLORS["ingredient"])

        tr = query.transformation_by_technique(conn, tech, ingredient)
        if not tr:
            continue
        comp_name = tr.get("output_component") or tr.get("component")
        if not comp_name:
            continue

        comp_id = f"comp:{comp_name}"
        if comp_id not in [n["id"] for n in net.nodes]:
            _add_node(net, comp_id, query.state_label(comp_name), "component",
                      size=22, title=f"Component: {comp_name}")
        _add_edge(net, tech_id, comp_id, "produces", color=_EDGE_COLORS["technique"])

        hypotheses = query.generate_scout_hypotheses(conn, comp_name)
        for hyp in hypotheses:
            if hyp["candidate_class"] == "rejected":
                continue

            candidate = hyp["candidate"]
            hyp_id = f"hyp:{comp_name}:{candidate}"

            if hyp_id in [n["id"] for n in net.nodes]:
                continue

            candidate_class = hyp["candidate_class"]
            color = _COLORS["component"] if candidate_class == "scout_candidate" else _SECONDARY
            size = 14 if candidate_class == "scout_candidate" else 10

            analogy = hyp.get("analogy", "")
            mechanism = hyp.get("mechanism", "").replace("_", " ")
            risk = hyp.get("risk", "")
            trials = hyp.get("trials", [])
            trial_count = len(trials)

            title_parts = [
                f"Candidate: {candidate}",
                f"Class: {candidate_class}",
                f"Analogy: {analogy}",
                f"Mechanism: {mechanism}",
                f"Risk: {risk}",
                f"Trials: {trial_count}",
            ]
            title = "\n".join(title_parts)

            _add_node(net, hyp_id, candidate.replace("_", " "), "hypothesis",
                      size=size, color=color, title=title,
                      shape="diamond" if candidate_class == "scout_candidate" else "dot")

            edge_label = f"analogy: {analogy}" if analogy else "hypothesis"
            _add_edge(net, comp_id, hyp_id, edge_label, color=_EDGE_COLORS["component"], dashes=True)

    net.show_buttons(filter_=["physics"])
    return net


# ---------------------------------------------------------------------------
# Taste Circle Map (custom click-driven component)
# ---------------------------------------------------------------------------

# (key, icon, display name, colour) — the 11 flavour dimensions of the circle.
TASTE_DIMENSIONS: list[tuple[str, str, str, str]] = [
    ("salty", "🧂", "Salty", "#1F6FC4"),
    ("sour", "🍋", "Sour", "#A5640A"),
    ("sweet", "🍯", "Sweet", "#0E7C5A"),
    ("bitter", "🌿", "Bitter", "#B23B2E"),
    ("umami", "🍄", "Umami", "#6B4C8A"),
    ("pungent", "🌶️", "Pungent", "#B23B2E"),
    ("aromatic", "🌸", "Aromatic", "#0E7C5A"),
    ("nutty_toasted", "🥜", "Nutty/Toasted", "#A5640A"),
    ("fresh_green", "🥬", "Fresh/Green", "#0E7C5A"),
    ("fermented_funky", "🧀", "Fermented/Funky", "#6B4C8A"),
    ("rich_fatty", "🧈", "Rich/Fatty", "#A5640A"),
]

# ---- Taste Circle Map geometry and states (design addendum 2) --------------
#
# Colour here encodes STATE, not dimension: the eleven dimensions are one hue
# (the primary) in provided / open / expanded / locked / thin states. Size
# encodes how many options fit. See ADDENDUM-2-taste-circle-map.md.

_MAX_FILLER_NODES = 14   # hard cap on one fan page; usually fit decides first
_DIM_RX = 257.0          # dimension ellipse, horizontal radius
_DIM_RY = 215.0          # dimension ellipse, vertical radius
_FAN_RADIUS_MIN = 110.0  # fan arc radius from the dimension node's centre
_FAN_RADIUS_MAX = 240.0  # beyond this the whole graph zooms out illegibly
_FAN_SPREAD = math.radians(120)  # ±60° around the ray through the dimension
_MORE_SUFFIX = "__more"  # filler:<dim>:__more pages the fan

_PILL_PAD = 26.0     # horizontal padding inside a filler pill
_PILL_CHAR = 7.1     # ~14px Figtree, per character
_PILL_GAP = 12.0     # clear space between neighbouring pills on the arc
_PILL_RADIUS = 14.0  # corner radius == half the pill height

_DISC_MIN = 40.0   # one option
_DISC_MAX = 64.0   # twenty or more
_DISC_CAP = 20

# Circle roles, pantry palette (design.css; docs/research/ux-layout-variants-r4-2/
# palette.md). The outline says focus, the fill says status:
#   mustard seed  the dimension you opened, its fan lines and option outlines
#   pale sage     a dimension still to fill (clickable, like the filters)
#   yogurt        a dimension the state already provides, with a sage outline:
#                 quieter, but a real node, since it explains the preparation
#   red cabbage   a dimension locked into your dish
#   parsley       an option you have on hand (its fill)
#   muted sage    a dimension with no fillers recorded
_CIRCLE = {
    "open_fill": "#E9ECD9", "open_edge": "#515A43",
    "prov_fill": "#FFFDF5", "prov_edge": "#8A916E", "prov_calm": "#A6AC91",
    "prov_label": "#515A43",
    "lock_fill": "#ECDFF0", "lock_edge": "#633F68",
    "focus_fill": "#F1E5AE", "focus_edge": "#674C14",
    "have_fill": "#DCEBDF", "option_fill": "#FFFDF5", "more_fill": "#E9ECD9",
    "gap_fill": "#EBEDE4", "gap_label": "#535C4A",
    "line": "#CDD2BA", "line_faint": "#E1E4D2",
}
_FADED_FONT = "#9AA088"  # label colour for faded nodes (sage, toward the page)
_FADE_T = 0.55           # 45% opacity over the ground == 55% blend into it


def _blend(hex_color: str, toward: str, t: float) -> str:
    """Linear RGB blend of two '#RRGGBB' colours; t=1 gives `toward`."""
    c1 = tuple(int(hex_color[i:i + 2], 16) for i in (1, 3, 5))
    c2 = tuple(int(toward[i:i + 2], 16) for i in (1, 3, 5))
    mixed = tuple(round(a + (b - a) * t) for a, b in zip(c1, c2))
    return "#{:02X}{:02X}{:02X}".format(*mixed)


def _disc_size(options: int) -> float:
    """vis node radius. Disc DIAMETER encodes option count: 40px → 64px."""
    t = min(1.0, max(0.0, (options - 1) / (_DISC_CAP - 1)))
    return (_DISC_MIN + (_DISC_MAX - _DISC_MIN) * t) / 2


def _pill_extent(text: str) -> float:
    """Arc length one filler pill occupies, gap included."""
    return len(text) * _PILL_CHAR + _PILL_PAD + _PILL_GAP


def _fan_page(names: list[str], start: int) -> int:
    """How many fillers fit on one arc-page starting at *start*.

    The addendum fixes the arc at 110px and the page at fourteen, but those
    two cannot both hold: fourteen labelled pills need roughly ten times the
    arc 110px provides, and letting the radius grow that far zooms the whole
    graph to a fifth of its size — the labels become unreadable, which is a
    worse failure than paging. The addendum's own priority settles it
    ("a fan that overlaps its neighbours is worse than paging"), so the arc
    is capped at a legible radius and the page is whatever fits on it.
    """
    budget = _FAN_RADIUS_MAX * _FAN_SPREAD
    used = 0.0
    count = 0
    for name in names[start:start + _MAX_FILLER_NODES]:
        extent = _pill_extent(name)
        if count and used + extent > budget:
            break
        used += extent
        count += 1
    return max(1, count)


def _fan_radius(labels: list[str]) -> float:
    """Arc radius that seats this page's pills without self-overlap."""
    if len(labels) < 2:
        return _FAN_RADIUS_MIN
    extent = sum(_pill_extent(text) for text in labels)
    return min(_FAN_RADIUS_MAX,
               max(_FAN_RADIUS_MIN, extent / _FAN_SPREAD))


def _fade_node(node: dict[str, Any], edge: dict[str, Any] | None,
               border: str | None = None) -> None:
    """Drop an unfocused dimension to 45% opacity over the ground.

    Keeps the node's ``clickable`` flag untouched: a faded-but-available
    dimension can still be clicked to move the focus to it.
    """
    color = node["color"]
    faded_bg = _blend(color["background"], _BG, _FADE_T)
    faded_border = border or _blend(color["border"], _BG, _FADE_T)
    node["color"] = {
        "background": faded_bg, "border": faded_border,
        "hover": {"background": faded_bg, "border": faded_border},
        "highlight": {"background": faded_bg, "border": faded_border},
    }
    node["borderWidth"] = 1
    node["font"] = {**node.get("font", {}), "color": _FADED_FONT}
    if edge is not None:
        edge["color"] = {"color": _CIRCLE["line_faint"]}
        edge["width"] = 1


def _node_color(color: str, border: str | None = None) -> dict[str, Any]:
    border = border or color
    return {
        "background": color,
        "border": border,
        "hover": {"background": color, "border": _INK},
        "highlight": {"background": color, "border": _INK},
    }


def taste_circle_graph_data(
    conn: sqlite3.Connection,
    component_name: str,
    locked_dimensions: set[str] | None = None,
    selections: dict[str, str] | None = None,
    expanded_dimension: str | None = None,
    available: set[str] | None = None,
    page: int = 0,
) -> dict[str, list[dict[str, Any]]]:
    """Build node/edge data for the click-driven Taste Circle component.

    Layout (physics off, fixed positions): the component sits at the centre,
    the 11 flavour dimensions form a circle around it, and the expanded
    dimension's fillers fan out on an outer arc next to it.

    Node ``id`` schemes (click routing happens in the Streamlit tab):
      ``comp:<component>`` · ``dim:<dimension>`` · ``filler:<dimension>:<name>``

    Nodes carry a ``clickable`` flag — provided/empty dimensions and the
    centre node are purely visual and report no clicks.
    """
    locked = set(locked_dimensions or set())
    selections = dict(selections or {})
    chosen_fillers = set(selections.values())

    profile = query.component_state_profile(conn, component_name)
    provided = set(profile["flavour_tags"]) if profile else set()
    fillers_by_dim = query.taste_circle_fillers(conn, component_name, locked)

    nodes: list[dict[str, Any]] = []
    edges: list[dict[str, Any]] = []

    on_hand = set(available or set())

    comp_id = f"comp:{component_name}"
    nodes.append({
        "id": comp_id,
        "label": query.state_label(component_name),
        "x": 0.0, "y": 0.0, "fixed": True,
        "shape": "circle", "widthConstraint": {"minimum": 108},
        "color": _node_color(_CIRCLE["prov_fill"], _INK),
        "borderWidth": 2,
        "font": {"size": 19, "color": _INK},
        "title": "Base component",
        "clickable": False,
    })

    count = len(TASTE_DIMENSIONS)
    for i, (dim_key, icon, dim_name, _hue) in enumerate(TASTE_DIMENSIONS):
        # Computed, never hand-placed, so a twelfth dimension just works.
        angle = -math.pi / 2 + i * (2 * math.pi / count)  # start at top, clockwise
        x = _DIM_RX * math.cos(angle)
        y = _DIM_RY * math.sin(angle)
        ray = math.atan2(y, x)  # ellipse: the ray differs from the parameter
        dim_id = f"dim:{dim_key}"
        title_name = f"{icon} {dim_name}"
        edge: dict[str, Any] = {"from": comp_id, "to": dim_id, "width": 1.5}

        node: dict[str, Any] = {"id": dim_id, "x": x, "y": y, "fixed": True}

        if dim_key in provided:
            node.update({
                "label": f"{title_name}\nprovided",
                "shape": "dot", "size": _disc_size(1),
                "color": _node_color(_CIRCLE["prov_fill"], _CIRCLE["prov_edge"]),
                "borderWidth": 1.5,
                "font": {"size": 14, "color": _CIRCLE["prov_label"]},
                "title": f"{title_name} — already in the component",
                "clickable": False,
            })
            edge.update({"color": {"color": _CIRCLE["prov_edge"]}, "width": 1.5})
        elif dim_key in locked:
            filler = selections.get(dim_key, "")
            node.update({
                "label": f"{title_name}\n🔒 {filler.replace('_', ' ')}",
                "shape": "dot", "size": _disc_size(6),
                "color": _node_color(_CIRCLE["lock_fill"], _CIRCLE["lock_edge"]),
                "borderWidth": 2.5,
                "font": {"size": 14, "color": _INK},
                "title": f"{title_name}: {filler.replace('_', ' ')} — click to change",
                "clickable": True,
            })
            edge.update({"color": {"color": _CIRCLE["lock_edge"]}, "width": 3})
        elif dim_key in fillers_by_dim and fillers_by_dim[dim_key]:
            fillers = [f for f in fillers_by_dim[dim_key]
                       if f["filler"] not in chosen_fillers]
            total = len(fillers)
            if dim_key == expanded_dimension and total:
                # Pages vary in size — each holds whatever fits the arc — so
                # walk them rather than assuming a fixed stride.
                names = [f["filler"].replace("_", " ") for f in fillers]
                offsets: list[int] = []
                cursor = 0
                while cursor < total:
                    offsets.append(cursor)
                    cursor += _fan_page(names, cursor)
                page = page % len(offsets)
                start = offsets[page]
                shown = fillers[start:start + _fan_page(names, start)]
                remaining = total - (start + len(shown))

                node.update({
                    "label": f"{title_name}\n{len(shown)} of {total}",
                    "shape": "dot", "size": _disc_size(total),
                    "color": _node_color(_CIRCLE["focus_fill"], _CIRCLE["focus_edge"]),
                    "borderWidth": 3,
                    "font": {"size": 14, "color": _INK},
                    "title": f"{title_name} — click again to close",
                    "clickable": True,
                })
                edge.update({"color": {"color": _CIRCLE["focus_edge"]}, "width": 3})

                labels = [f["filler"].replace("_", " ") for f in shown]
                if remaining > 0:
                    labels.append(f"+ {remaining} more")
                radius = _fan_radius(labels)
                k = len(labels)
                for j, text in enumerate(labels):
                    a = (ray if k == 1
                         else ray - _FAN_SPREAD / 2 + j * _FAN_SPREAD / (k - 1))
                    is_more = remaining > 0 and j == k - 1
                    fname = _MORE_SUFFIX if is_more else shown[j]["filler"]
                    fid = f"filler:{dim_key}:{fname}"
                    border = _CIRCLE["focus_edge"]   # every option in the fan: focus
                    if is_more:
                        fill = _CIRCLE["more_fill"]
                        title = f"Show the next {min(remaining, _MAX_FILLER_NODES)}"
                    elif fname in on_hand:
                        # "available now" has to read at a glance
                        fill = _CIRCLE["have_fill"]
                        title = f"{text} — in your kitchen. Click to choose it."
                    else:
                        fill = _CIRCLE["option_fill"]
                        title = f"Click to choose {text}"
                    nodes.append({
                        "id": fid,
                        "label": text,
                        "x": x + radius * math.cos(a),
                        "y": y + radius * math.sin(a),
                        "fixed": True,
                        "shape": "box",
                        # Half the pill's height gives a true pill. NOT 999:
                        # vis folds the corner radius into the node's bounding
                        # box, so a CSS-style "very large" value reports a
                        # ~2000px node and fit() zooms the graph to a fifth.
                        "shapeProperties": {"borderRadius": _PILL_RADIUS},
                        "margin": {"top": 5, "bottom": 5, "left": 13, "right": 13},
                        "color": _node_color(fill, border),
                        "borderWidth": 1,
                        "font": {"size": 14, "color": _INK},
                        "title": title,
                        "clickable": True,
                    })
                    edges.append({
                        "from": dim_id, "to": fid,
                        "width": 1.5, "color": {"color": _CIRCLE["focus_edge"]},
                    })
            else:
                plural = "option" if total == 1 else "options"
                node.update({
                    "label": f"{title_name}\n{total} {plural}",
                    "shape": "dot", "size": _disc_size(total),
                    "color": _node_color(_CIRCLE["open_fill"], _CIRCLE["open_edge"]),
                    "borderWidth": 1.5,
                    "font": {"size": 14, "color": _INK},
                    "title": f"{title_name} — click to see options",
                    "clickable": True,
                })
                edge.update({"color": {"color": _CIRCLE["line"]}})
        else:
            # Keep the node: "we have nothing here" is information the
            # curator needs to see, so it is never hidden.
            node.update({
                "label": f"{title_name}\nno fillers yet",
                "shape": "dot", "size": _disc_size(1),
                "color": _node_color(_CIRCLE["gap_fill"], _CIRCLE["line"]),
                "borderWidth": 1,
                "font": {"size": 14, "color": _CIRCLE["gap_label"]},
                "title": f"{title_name} — no fillers in the catalogue",
                "clickable": False,
            })
            edge.update({"color": {"color": _CIRCLE["line"]}, "dashes": True})

        # While a dimension is expanded, every other one drops to 45% so the
        # fan is unambiguously the active region. Faded dimensions stay
        # clickable — clicking one moves the focus there.
        if expanded_dimension and dim_key != expanded_dimension:
            _fade_node(node, edge, _CIRCLE["prov_calm"] if dim_key in provided else None)

        nodes.append(node)
        edges.append(edge)

    return {"nodes": nodes, "edges": edges}


def random_dish_selections(
    fillers_by_dim: dict[str, list[dict[str, Any]]],
    selections: dict[str, str] | None = None,
    *,
    top_n: int = _MAX_FILLER_NODES,
    rng: random.Random | None = None,
) -> dict[str, str]:
    """Pick one random valid filler per open flavour dimension.

    Dimensions already locked (present in *selections*) are skipped, and a
    filler already chosen — locked or freshly picked — is never reused.
    Candidates come from the ``top_n`` most common options of each
    dimension (the same slice the fan shows).
    """
    chooser = rng or random
    chosen = set((selections or {}).values())
    dims = [d for d in fillers_by_dim if not (selections and d in selections)]
    chooser.shuffle(dims)
    picks: dict[str, str] = {}
    for dim in dims:
        candidates = [f["filler"] for f in fillers_by_dim[dim][:top_n]
                      if f["filler"] not in chosen]
        if candidates:
            pick = chooser.choice(candidates)
            picks[dim] = pick
            chosen.add(pick)
    return picks


def graph_data(net: Network) -> dict[str, Any]:
    """A pyvis Network as plain data for the vis-network component.

    pyvis stays the builder (its node/edge API is what the map code speaks),
    but its HTML template is no longer used: the map renders through the same
    no-build custom component as the Taste Circle, instead of
    ``components.html``, and the component's page already links the font.
    """
    options = json.loads(net.options.to_json())
    # pyvis turns on vis's physics-configurator panel; the map never shows it.
    options.pop("configure", None)
    return {"nodes": list(net.nodes), "edges": list(net.edges), "options": options}


def build_outcome_graph(ingredient: str, edges: list[tuple[str, str, str]],
                        labels: dict[str, str] | None = None) -> Network:
    """R7: the mindmap with outcomes as its second ring.

    ``edges`` come from ``foodprep.dinner.outcome_edges``: the ingredient to each
    documented dish (familiar use) or transfer (less usual use), then each of those
    to the other raw ingredients it needs. Techniques live inside the dish view,
    not here. Above about 20 edges the app shows the table instead (R4.1).
    """
    labels = labels or {}
    net = Network(height="600px", width="100%", bgcolor=_BG,
                  font_color=False, directed=True)
    net.barnes_hut(gravity=-3000, central_gravity=0.3, spring_length=140,
                   spring_strength=0.05, damping=0.09, overlap=0)
    root = f"ing:{ingredient}"
    _add_node(net, root, ingredient.replace("_", " "), "ingredient", size=35,
              title=f"Ingredient: {ingredient}")
    seen = {root}
    for src, dst, label in edges:
        for node in (src, dst):
            if node in seen:
                continue
            seen.add(node)
            kind, _, rest = node.partition(":")
            name = labels.get(node) or rest.replace("_", " ")
            if kind == "out":
                familiar = any(e[1] == node and e[2] == "familiar use" for e in edges)
                _add_node(net, node, name, "component" if familiar else "route", size=22,
                          title=("A documented dish" if familiar else
                                 "A documented dish carried over (R4 transfer)") + f": {name}")
            else:
                _add_node(net, node, name, "ingredient", size=14,
                          title=f"Ingredient: {name}")
        color = _EDGE_COLORS["component"] if label == "familiar use" else \
            _EDGE_COLORS["filler"] if label == "less usual use" else _LINE
        _add_edge(net, src, dst, label, color=color, dashes=label == "also needs")
    return net
