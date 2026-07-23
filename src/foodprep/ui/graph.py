"""Build interactive ingredient mindmaps using pyvis (vis.js).

Generates a force-directed graph for one ingredient showing:
  ingredient → techniques → components → fillers / routes / destinations

Rendered as self-contained HTML and embedded in Streamlit via
``st.components.v1.html()``.
"""

from __future__ import annotations

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


def graph_to_html(net: Network) -> str:
    """Serialize a pyvis Network to self-contained HTML."""
    return net.generate_html(notebook=False)
