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

import math
import random
import sqlite3
from typing import Any

from pyvis.network import Network

from foodprep import query


_COLORS = {
    "ingredient": "#0E7C5A",
    "technique":  "#1F6FC4",
    "component":  "#6B4C8A",
    "filler":     "#A5640A",
    "route":      "#A5640A",
    "destination": "#B23B2E",
    "hypothesis": "#6B4C8A",
    "dimension":  "#1F6FC4",
}

_UNIVERSAL_FILLERS = {
    "sea_salt", "olive_oil", "lemon", "black_pepper",
}


def _add_node(net: Network, node_id: str, label: str, group: str,
              size: int = 20, title: str = "", color: str | None = None,
              shape: str | None = None) -> None:
    node_color = color if color is not None else _COLORS.get(group, "#75796E")
    node_shape = shape if shape is not None else {"technique": "diamond", "route": "square",
              "destination": "triangle"}.get(group, "dot")
    net.add_node(
        node_id, label=label, color=node_color, size=size, shape=node_shape,
        group=group, title=title or label,
        font={"color": "#1A1B16", "size": 12, "face": "Geist, sans-serif"},
    )


def _add_edge(net: Network, src: str, dst: str, label: str = "",
              color: str = "#D2CDBE", dashes: bool = False) -> None:
    net.add_edge(src, dst, label=label, color=color, dashes=dashes,
                 font={"color": "#75796E", "size": 9, "face": "Geist Mono, monospace",
                        "align": "middle"},
                 width=1.5)


def build_ingredient_graph(conn: sqlite3.Connection,
                           ingredient: str) -> Network:
    """Build a pyvis Network for one ingredient's transformation tree + connections."""
    net = Network(height="600px", width="100%", bgcolor="#F4F2EC",
                  font_color="#1A1B16", directed=True)
    net.barnes_hut(gravity=-3000, central_gravity=0.3, spring_length=120,
                   spring_strength=0.05, damping=0.09, overlap=0)

    _add_node(net, f"ing:{ingredient}", ingredient, "ingredient", size=35,
              title=f"Ingredient: {ingredient}")

    techs = query.techniques_for_ingredient(conn, ingredient)
    for tech in techs:
        tech_id = f"tech:{tech}"
        _add_node(net, tech_id, tech.replace("_", " "), "technique", size=18,
                  title=f"Technique: {tech}")
        _add_edge(net, f"ing:{ingredient}", tech_id, "via", color="#0E7C5A")

        tr = query.transformation_by_technique(conn, tech, ingredient)
        if not tr:
            continue
        comp_name = tr.get("output_component") or tr.get("component")
        if not comp_name:
            continue

        comp_id = f"comp:{comp_name}"
        if comp_id not in [n["id"] for n in net.nodes]:
            _add_node(net, comp_id, comp_name.replace("_", " "), "component",
                      size=22, title=f"Component: {comp_name}")
        _add_edge(net, tech_id, comp_id, "produces", color="#1F6FC4")

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
                              color="#A5640A", dashes=True)

        routes = query.flavour_routes_for_component(conn, comp_name)
        for route in routes:
            route_id = f"route:{route['route_id']}"
            if route_id not in [n["id"] for n in net.nodes]:
                _add_node(net, route_id, route["name"].replace("_", " "),
                          "route", size=14,
                          title=f"Route: {route['name']}")
            _add_edge(net, comp_id, route_id, "route", color="#A5640A")

            for dest in (route.get("destinations") or []):
                dest_id = f"dest:{dest}"
                if dest_id not in [n["id"] for n in net.nodes]:
                    _add_node(net, dest_id, dest.replace("_", " "),
                              "destination", size=12,
                              title=f"Destination: {dest}")
                _add_edge(net, route_id, dest_id, "", color="#B23B2E")

    journeys = query.ingredient_journeys(conn, ingredient)
    for j in journeys:
        for dest in (j.get("destinations") or []):
            dest_id = f"dest:{dest}"
            if dest_id not in [n["id"] for n in net.nodes]:
                _add_node(net, dest_id, dest.replace("_", " "),
                          "destination", size=12,
                          title=f"Destination: {dest}")

    net.show_buttons(filter_=["physics"])
    return net


def build_scout_graph(conn: sqlite3.Connection,
                      ingredient: str) -> Network:
    """Build a pyvis Network showing Scout hypotheses for an ingredient's components.

    Shows: ingredient → techniques → components → Scout hypotheses (candidates)
    Hypotheses are color-coded by candidate_class and show analogy/trial status.
    """
    net = Network(height="600px", width="100%", bgcolor="#F4F2EC",
                  font_color="#1A1B16", directed=True)
    net.barnes_hut(gravity=-3000, central_gravity=0.3, spring_length=120,
                   spring_strength=0.05, damping=0.09, overlap=0)

    _add_node(net, f"ing:{ingredient}", ingredient, "ingredient", size=35,
              title=f"Ingredient: {ingredient}")

    techs = query.techniques_for_ingredient(conn, ingredient)
    for tech in techs:
        tech_id = f"tech:{tech}"
        _add_node(net, tech_id, tech.replace("_", " "), "technique", size=18,
                  title=f"Technique: {tech}")
        _add_edge(net, f"ing:{ingredient}", tech_id, "via", color="#0E7C5A")

        tr = query.transformation_by_technique(conn, tech, ingredient)
        if not tr:
            continue
        comp_name = tr.get("output_component") or tr.get("component")
        if not comp_name:
            continue

        comp_id = f"comp:{comp_name}"
        if comp_id not in [n["id"] for n in net.nodes]:
            _add_node(net, comp_id, comp_name.replace("_", " "), "component",
                      size=22, title=f"Component: {comp_name}")
        _add_edge(net, tech_id, comp_id, "produces", color="#1F6FC4")

        hypotheses = query.generate_scout_hypotheses(conn, comp_name)
        for hyp in hypotheses:
            if hyp["candidate_class"] == "rejected":
                continue

            candidate = hyp["candidate"]
            hyp_id = f"hyp:{comp_name}:{candidate}"

            if hyp_id in [n["id"] for n in net.nodes]:
                continue

            candidate_class = hyp["candidate_class"]
            color = "#6B4C8A" if candidate_class == "scout_candidate" else "#75796E"
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
            _add_edge(net, comp_id, hyp_id, edge_label, color="#6B4C8A", dashes=True)

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

_MAX_FILLER_NODES = 14  # most common fillers shown when a dimension expands
_DIM_RADIUS = 280.0     # circle radius for dimension nodes
_FILLER_RADIUS = 470.0  # radius of the filler fan around the expanded dimension

_BG = "#F4F2EC"         # app background; faded nodes blend toward it
_FADED_FONT = "#B7B3A6"  # label colour for faded nodes
_FADE_T = 0.72          # blend factor toward the background for faded nodes


def _blend(hex_color: str, toward: str, t: float) -> str:
    """Linear RGB blend of two '#RRGGBB' colours; t=1 gives `toward`."""
    c1 = tuple(int(hex_color[i:i + 2], 16) for i in (1, 3, 5))
    c2 = tuple(int(toward[i:i + 2], 16) for i in (1, 3, 5))
    mixed = tuple(round(a + (b - a) * t) for a, b in zip(c1, c2))
    return "#{:02X}{:02X}{:02X}".format(*mixed)


def _fade_node(node: dict[str, Any], edge: dict[str, Any] | None) -> None:
    """Visually fade a node (and its centre edge) into the background.

    Keeps the node's ``clickable`` flag untouched: a faded-but-available
    dimension can still be clicked to move the focus to it.
    """
    color = node["color"]
    faded_bg = _blend(color["background"], _BG, _FADE_T)
    faded_border = _blend(color["border"], _BG, _FADE_T)
    node["color"] = {
        "background": faded_bg, "border": faded_border,
        "hover": {"background": faded_bg, "border": faded_border},
        "highlight": {"background": faded_bg, "border": faded_border},
    }
    node["borderWidth"] = 1
    node["font"] = {**node.get("font", {}), "color": _FADED_FONT}
    if edge is not None:
        base = (edge.get("color") or {}).get("color", "#D8D2C2")
        edge["color"] = {"color": _blend(base, _BG, 0.6), "opacity": 0.5}
        edge["width"] = 1


def _node_color(color: str, border: str | None = None) -> dict[str, Any]:
    border = border or color
    return {
        "background": color,
        "border": border,
        "hover": {"background": color, "border": "#1A1B16"},
        "highlight": {"background": color, "border": "#1A1B16"},
    }


def taste_circle_graph_data(
    conn: sqlite3.Connection,
    component_name: str,
    locked_dimensions: set[str] | None = None,
    selections: dict[str, str] | None = None,
    expanded_dimension: str | None = None,
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

    comp_id = f"comp:{component_name}"
    nodes.append({
        "id": comp_id,
        "label": component_name.replace("_", " "),
        "x": 0.0, "y": 0.0, "fixed": True,
        "shape": "dot", "size": 30,
        "color": _node_color("#6B4C8A", "#54396F"),
        "font": {"size": 15, "color": "#1A1B16"},
        "title": "Base component",
        "clickable": False,
    })

    count = len(TASTE_DIMENSIONS)
    for i, (dim_key, icon, dim_name, color) in enumerate(TASTE_DIMENSIONS):
        angle = -math.pi / 2 + i * (2 * math.pi / count)  # start at top, clockwise
        x = _DIM_RADIUS * math.cos(angle)
        y = _DIM_RADIUS * math.sin(angle)
        dim_id = f"dim:{dim_key}"
        title_name = f"{icon} {dim_name}"
        edge: dict[str, Any] = {"from": comp_id, "to": dim_id, "width": 1.5}

        node: dict[str, Any] = {"id": dim_id, "x": x, "y": y, "fixed": True}

        if dim_key in provided:
            node.update({
                "label": f"{title_name}\n✓ provided",
                "shape": "dot", "size": 20,
                "color": _node_color(color),
                "font": {"size": 12, "color": "#75796E"},
                "title": f"{title_name} — already in the component",
                "clickable": False,
            })
            edge.update({"color": {"color": color, "opacity": 0.8}, "width": 2})
        elif dim_key in locked:
            filler = selections.get(dim_key, "")
            node.update({
                "label": f"{title_name}\n🔒 {filler.replace('_', ' ')}",
                "shape": "dot", "size": 26,
                "color": _node_color(color, "#1A1B16"),
                "borderWidth": 2.5,
                "font": {"size": 13, "color": "#1A1B16"},
                "title": f"{title_name}: {filler.replace('_', ' ')} — click to change",
                "clickable": True,
            })
            edge.update({"color": {"color": color}, "width": 2.5})
        elif dim_key in fillers_by_dim and fillers_by_dim[dim_key]:
            fillers = [f for f in fillers_by_dim[dim_key]
                       if f["filler"] not in chosen_fillers]
            total = len(fillers)
            if dim_key == expanded_dimension and total:
                shown = fillers[:_MAX_FILLER_NODES]
                node.update({
                    "label": f"{title_name}\n{len(shown)} of {total}",
                    "shape": "dot", "size": 28,
                    "color": _node_color(color, "#1A1B16"),
                    "borderWidth": 3,
                    "font": {"size": 13, "color": "#1A1B16"},
                    "title": f"{title_name} — click again to close",
                    "clickable": True,
                })
                edge.update({"color": {"color": color}, "width": 2, "dashes": True})

                k = len(shown)
                spread = math.radians(min(200, 16 * k))
                for j, f in enumerate(shown):
                    a = angle if k == 1 else angle - spread / 2 + j * spread / (k - 1)
                    fname = f["filler"]
                    fid = f"filler:{dim_key}:{fname}"
                    nodes.append({
                        "id": fid,
                        "label": fname.replace("_", " "),
                        "x": _FILLER_RADIUS * math.cos(a),
                        "y": _FILLER_RADIUS * math.sin(a),
                        "fixed": True,
                        "shape": "dot", "size": 12,
                        "color": _node_color("#FFFFFF", color),
                        "font": {"size": 12, "color": "#1A1B16"},
                        "title": f"Click to choose {fname.replace('_', ' ')}",
                        "clickable": True,
                    })
                    edges.append({
                        "from": dim_id, "to": fid,
                        "dashes": True, "width": 1.2,
                        "color": {"color": color, "opacity": 0.55},
                    })
            else:
                node.update({
                    "label": f"{title_name}\n{total} options",
                    "shape": "dot", "size": 24,
                    "color": _node_color(color),
                    "font": {"size": 13, "color": "#1A1B16"},
                    "title": f"{title_name} — click to see options",
                    "clickable": True,
                })
                edge.update({"color": {"color": "#D8D2C2"}})
        else:
            node.update({
                "label": f"{title_name}\n—",
                "shape": "dot", "size": 16,
                "color": _node_color("#C6C2B4", "#B4B0A2"),
                "font": {"size": 12, "color": "#9AA092"},
                "title": f"{title_name} — no fillers in the catalogue",
                "clickable": False,
            })
            edge.update({"color": {"color": "#E2DDD0"}, "dashes": True})

        # When a dimension is expanded, fade everything else into the
        # background so the filler fan owns the screen. Faded dimensions
        # stay clickable — clicking one moves the focus there.
        if expanded_dimension and dim_key != expanded_dimension:
            _fade_node(node, edge)

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


def graph_to_html(net: Network) -> str:
    """Serialize a pyvis Network to self-contained HTML."""
    return net.generate_html(notebook=False)
