"""Food-prep — ingredient transformation graph UI (Streamlit).

Navigation is two levels — a section, then a tab inside it (see SECTIONS):
  Cook        Ingredient Explorer · Component Explorer · Plate Balance ·
              Taste Circle (Circle | Cards views, one shared dish)
  Explore     Map (Cook paths | Scout ideas) · Journeys · Filler Profiles
  Experiment  Scout

Run:  streamlit run app.py
"""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any

import streamlit as st

from foodprep.loader import build
from foodprep import export, query
from foodprep.ui.render import (
    _esc, _readable, chip, chips, conf_pill, debug_block, tag_class,
    available_partition_html, branch_card_html, subject_column_html,
    claim_cards_html, hypothesis_card_html, journey_card_html,
    route_card_html, smallest_test_html, trial_history_html,
)
from foodprep.ui.graph import (
    TASTE_DIMENSIONS, build_ingredient_graph, build_scout_graph,
    graph_data, random_dish_selections, taste_circle_graph_data,
)
from foodprep.ui.taste_circle import network_graph, taste_circle_map

_CSS_PATH = Path(__file__).with_name("design.css")


def _md(markup: str) -> None:
    cleaned = "\n".join(line.lstrip() for line in markup.splitlines())
    st.markdown(cleaned.strip(), unsafe_allow_html=True)


def _seed(key: str, options: list, preferred) -> None:
    """Give a sticky selector its starting value through session state.

    Passing ``index=``/``default=`` as well as re-assigning the key each run
    (see _persist_widget_state) makes Streamlit warn that the widget "was
    created with a default value but also had its value set via the Session
    State API". So the default goes in once, here, and never as an argument.
    A stored value that is no longer an option is replaced.
    """
    current = st.session_state.get(key)
    if isinstance(preferred, list):
        if current is None or not all(v in options for v in current):
            st.session_state[key] = [v for v in preferred if v in options]
    elif current not in options:
        st.session_state[key] = preferred if preferred in options else options[0]


def _pretty(name: str) -> str:
    """What a cook reads: roasted_broccoli_component -> roasted broccoli."""
    return _readable(name)


@st.cache_resource
def get_conn():
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    build(conn)
    return conn


CONN = get_conn()


def export_buttons(md: str, filename: str) -> None:
    """Getting the data out stays; the inline preview and the raw-row dump
    were scaffolding and are gone."""
    if not md:
        return
    st.download_button("Download .md", md, file_name=filename,
                       mime="text/markdown", key=f"dl_{filename}")


def topbar() -> None:
    trees = query.tree_ingredients(CONN)
    comps = query.components_list(CONN)
    profiles = query.profiles_list(CONN)
    _md(f"""
    <div class="topbar">
      <div class="brand">
        <div class="brand-mark">if</div>
        <div>
          <div class="brand-title">Ingredient Foundry</div>
          <div class="brand-sub">A local cooking map for turning ingredients into useful components, seeing what taste roles are missing, and finding the next sensible move.</div>
        </div>
      </div>
      <div class="topbar-spacer"></div>
      <div class="topbar-pill">{len(trees)} full ingredients</div>
      <div class="topbar-pill">{len(comps)} components</div>
      <div class="topbar-pill">{len(profiles)} plate profiles</div>
    </div>
    """)


def available_selector() -> list[str]:
    ings = query.ingredients_list(CONN)
    # The strip is one surface block with the multiselect inside it, so the
    # container carries the styling (`.st-key-avail_strip`) rather than a
    # wrapper div — Streamlit widgets cannot be nested inside raw markup.
    with st.container(key="avail_strip"):
        _md('<div class="avail-head">'
            '<span class="avail-title">What do I have right now?</span>'
            '<span class="avail-hint">filters suggestions into available now · '
            'missing but useful · no match</span>'
            '</div>')
        return st.multiselect(
            "Available ingredients", ings, key="available_items",
            label_visibility="collapsed", format_func=_pretty,
            placeholder="e.g. lemon, yogurt, pickles, bread, eggs, beans",
            help="Pick what's in your kitchen. Empty = show all curated fillers.")


#: 300px subject column beside a 1fr answer column — the recurring layout.
_SUBJECT_RATIO = [1, 2.6]


def pill_radio(label: str, options: list[str], key: str) -> str:
    """A horizontal radio wearing the design's pill styling."""
    with st.container(key=f"{key}_pills"):
        return st.radio(label, options, horizontal=True,
                        label_visibility="collapsed", key=key)


def tab_ingredient_explorer(available_items: list[str] | None = None) -> None:
    trees = query.tree_ingredients(CONN)
    avail = available_items or None
    subject, answer = st.columns(_SUBJECT_RATIO, gap="large")

    with subject:
        _md('<div class="eyebrow">Ingredient</div>')
        # Broccoli is the pilot and on the shopping list; cabbage is not.
        _seed("explorer_ing", trees, "broccoli")
        ingredient = st.selectbox(
            "Ingredient", trees, key="explorer_ing",
            label_visibility="collapsed", format_func=_pretty)
        techs = query.techniques_for_ingredient(CONN, ingredient)
        _md(subject_column_html(
            ingredient, "ingredient",
            note=f"{len(techs)} ways to transform it, "
                 f"ranked cooking before preservation."))
        _md('<div class="eyebrow subject-block">Mode</div>')
        mode = pill_radio("Mode", ["Best branches", "Choose technique"],
                          "explorer_mode")

    with answer:
        if mode == "Choose technique":
            tech = st.selectbox("Technique", techs, key="explorer_tech",
                                format_func=_pretty)
            card = query.branch_card(CONN, ingredient, tech)
            if card:
                part = (query.available_filter(CONN, card["transformation_id"], avail)
                        if avail else None)
                routes = (query.flavour_routes_for_component(
                    CONN, card["component"], available_items=avail) if avail else None)
                _md(branch_card_html(card, available=part, lead=True, routes=routes))
                export_buttons(export.render_branch_markdown(card, part), "branch.md")
            else:
                st.write(f"No transformation for {ingredient}/{tech}.")
        else:
            cards = query.all_branch_cards(CONN, ingredient)
            shown = cards[:5]
            _md(f'<div class="eyebrow">Showing top {len(shown)} of {len(cards)} '
                f'branches · ranked cooking-before-preservation</div>')
            md_parts = []
            for i, c in enumerate(shown):
                part = (query.available_filter(CONN, c["transformation_id"], avail)
                        if avail else None)
                routes = (query.flavour_routes_for_component(
                    CONN, c["component"], available_items=avail) if avail else None)
                # the top-ranked branch carries the accent border
                _md(branch_card_html(c, available=part, lead=(i == 0), routes=routes))
                md_parts.append(export.render_branch_markdown(c, part))
            export_buttons("\n\n---\n\n".join(md_parts), "branches.md")


def tab_map() -> None:
    """One graph tab, two readings of the same ingredient.

    Cook paths is the transformation tree; Scout ideas is the same tree with
    generated hypotheses hanging off each state. They used to be two tabs with
    two ingredient pickers that drifted apart.
    """
    trees = query.tree_ingredients(CONN)
    pick, view_col = st.columns([1, 1.4], gap="large")
    with pick:
        _seed("map_ing", trees, "broccoli")
        ingredient = st.selectbox(
            "Ingredient", trees, key="map_ing", format_func=_pretty,
            label_visibility="collapsed")
    with view_col:
        view = pill_radio("View", ["Cook paths", "Scout ideas"], "map_view")
    if view == "Scout ideas":
        _md('<div class="hint">Generated hypotheses for each transformed state. '
            'Diamonds have three lines of compatibility evidence; dots are '
            'thinner. Untested — see Scout before cooking any of them.</div>')
        net = build_scout_graph(CONN, ingredient)
    else:
        _md('<div class="hint">How it can be cooked, what each state becomes, '
            'what pairs with it and where it goes. Drag nodes to explore.</div>')
        net = build_ingredient_graph(CONN, ingredient)
    network_graph(graph_data(net), height=620,
                  key=f"map_graph_{view}_{ingredient}")


def tab_journeys() -> None:
    trees = query.tree_ingredients(CONN)
    col, _pad = st.columns([2.4, 1], gap="large")
    with col:
        _seed("journey_ing", trees, "broccoli")
        ingredient = st.selectbox(
            "Ingredient", trees, key="journey_ing", label_visibility="collapsed",
            format_func=_pretty)
        journeys = query.ingredient_journeys(CONN, ingredient)
        if not journeys:
            _md(f'<div class="hint">No complete journeys modelled for '
                f'<b>{_esc(ingredient)}</b> yet.</div>')
            return
        _md(f'<div class="h2">{_esc(ingredient.capitalize())} — '
            f'{len(journeys)} complete cook path'
            f'{"s" if len(journeys) != 1 else ""}</div>'
            f'<div class="hint">Each one reads left to right: preparation → '
            f'transformation → sensory change → flavour route → correction → '
            f'destination.</div>')
        for i, j in enumerate(journeys, start=1):
            _md(journey_card_html(j, index=i))


def tab_component_explorer(available_items: list[str] | None = None) -> None:
    comps = query.components_list(CONN)
    default = "roasted_tomato_component" if "roasted_tomato_component" in comps else comps[0]
    subject, answer = st.columns(_SUBJECT_RATIO, gap="large")

    with subject:
        _md('<div class="eyebrow">Something you already cooked</div>')
        _seed("component_explorer_comp", comps, default)
        comp = st.selectbox("Component", comps,
                            label_visibility="collapsed", format_func=_pretty,
                            key="component_explorer_comp")
    d = query.component_card(CONN, comp)
    if not d:
        with answer:
            st.write("No component named", comp)
        return
    producers = d.get("produced_by") or []
    prod_str = ", ".join(f"{_pretty(p['ingredient'])} + {_pretty(p['technique'])}" for p in producers) or "(no producing transformation)"
    tags = d.get("tags") or []
    tag_chips = " ".join(chip(t["value"], tag_class(t.get("family", ""))) for t in tags)
    risks = d.get("risks") or []
    missing = [m["role_name"] for m in (d.get("missing") or [])]
    avail = available_items or None
    part = None
    if avail and producers:
        part = query.available_filter(CONN, producers[0]["transformation_id"], avail)
    if part:
        moves_html = available_partition_html(part) or '<span class="chip" style="color:var(--ink-5)">—</span>'
    else:
        try_groups = []
        for role, fillers in (d.get("fillers_by_role") or {}).items():
            names = [f["filler"] for f in fillers[:3]] or ["(no curated filler)"]
            try_groups.append(
                f'<div class="chip-group"><span class="gl">{_esc(role)}</span>'
                + " ".join(chip(n, "filler") for n in names) + "</div>"
            )
        moves_html = "".join(try_groups) or '<span class="chip" style="color:var(--ink-5)">—</span>'

    with subject:
        _md(subject_column_html(
            comp, "component",
            note="A component is a state you already have — you do not always "
                 "start from raw. This one came from "
                 f"{prod_str}."))
        _md(f'<div class="eyebrow subject-block">Storage</div>'
            f'<div class="subject-note">keeps {_esc(d.get("keeps_well") or "—")} · '
            f'{"freezes well" if d.get("freezes_well") else "does not freeze"} · '
            f'{_esc(d.get("batch_prep_value") or "—")} batch value</div>')

    with answer:
        _md(f"""
        <div class="card">
          <div class="row"><span class="lbl">Tags</span><div class="chips">{tag_chips or '<span class="chip muted">—</span>'}</div></div>
          {f'<div class="row"><span class="lbl">Risks</span><div class="chips">{"".join(chip(r,"risk") for r in risks)}</div></div>' if risks else ''}
          {f'<div class="row"><span class="lbl">May need</span><div class="chips">{"".join(chip(r,"missing") for r in missing)}</div></div>' if missing else ''}
          <div class="row"><span class="lbl">{"Next moves" if not part else "Next moves · what you have"}</span><div>{moves_html}</div></div>
          <div class="row"><span class="lbl">Use in</span><div class="chips">{chips(d.get("uses") or [])}</div></div>
        </div>
        """)
        export_buttons(export.render_component_markdown(d, part), "component.md")

        routes = query.flavour_routes_for_component(CONN, comp, available_items=avail)
        if routes:
            _md(f'<div class="eyebrow">Flavour routes — '
                f'{len(routes)} direction{"s" if len(routes) != 1 else ""} '
                f'from this state</div>')
            for r in routes:
                _md(route_card_html(r))
        else:
            # Most components have no routes modelled yet, so the section
            # would otherwise vanish without saying why.
            _md('<div class="eyebrow">Flavour routes</div>'
                '<div class="card muted"><div class="card-body">No routes '
                'modelled from this state yet. Routes are hand-curated — '
                'absence here means nobody has written one, not that the '
                'state leads nowhere.</div></div>')


def tab_plate_balance(available_items: list[str] | None = None) -> None:
    st.markdown('<div class="section-title">Plate Balance <span class="count">Cook mode — no experimental pairings</span></div>',
                unsafe_allow_html=True)
    profiles = query.profiles_list(CONN)
    if "plate_items" not in st.session_state:
        _seed("plate_items", profiles, ["mashed_potatoes", "chickpea_patty"])
    picked = st.multiselect("Plate items", profiles, key="plate_items",
                            format_func=_pretty)
    if not picked:
        st.markdown('<div class="hint">Pick one or more plate items to see what the plate '
                    'has, what it lacks, and what to add.</div>', unsafe_allow_html=True)
        return
    text = "I have " + " and ".join(picked) + ". what is missing?"
    avail = available_items or None
    r = query.plate_balance_detail(CONN, text, available_items=avail)
    has_part = "available_now" in r

    gap_n = len(r["target_gap"])
    more_n = len(r["flagged_more"])
    h_cls = ("k-warn k-heavy" if r["leans_heavy"]
             else "k-warn" if r["avoid_more_richness"] else "k-ok")
    _md(f"""
    <div class="kpis">
      <div class="kpi"><div class="lbl">Items</div><div class="val">{len(r['items'])}</div><div class="foot">on the plate</div></div>
      <div class="kpi {'k-risk' if gap_n else ''}"><div class="lbl">Hard gaps</div><div class="val">{gap_n}</div><div class="foot">target roles missing</div></div>
      <div class="kpi k-warn"><div class="lbl">May want more</div><div class="val">{more_n}</div><div class="foot">soft flags</div></div>
      <div class="kpi {h_cls}"><div class="lbl">Heaviness</div><div class="val">{r['heaviness_avg'] if r['heaviness_avg'] is not None else '—'}<span class="kpi-scale"> / 5</span></div><div class="foot">{r['heaviness_label'] or 'unknown'} · average per item</div></div>
    </div>
    """)

    _md(f'<div class="balance-section have"><h4>Already provides</h4><div class="chips">{chips(r["provided"])}</div></div>')

    if has_part:
        if r["available_now"]:
            lines = []
            for g in r["available_now"]:
                lines.append(
                    f'<div class="filler-line"><b>{_esc(g["filler"])}</b> → '
                    + " ".join(chip(role, "missing") for role in g["roles"]) + "</div>")
            _md(f'<div class="balance-section have"><h4>Available now</h4>{"".join(lines)}</div>')
        if r["missing_but_useful"]:
            lines = []
            for m in r["missing_but_useful"]:
                if m["fillers"]:
                    fch = " ".join(chip(f, "filler") for f in m["fillers"])
                else:
                    fch = '<span class="none">(no curated filler)</span>'
                lines.append(f'<div class="filler-line"><span class="role">{_esc(m["role"])}</span>{fch}</div>')
            _md(f'<div class="balance-section more"><h4>Missing but useful</h4>{"".join(lines)}</div>')
        no_match = list(r["unknown_items"]) + list(r["no_match_known"])
        if no_match:
            _md(f'<div class="balance-section muted"><h4>No match from selected items</h4>'
                f'<div class="chips">{"".join(chip(n, "muted") for n in no_match)}</div></div>')
        if r["target_gap"] and not r["available_now"] and not r["missing_but_useful"]:
            _md('<div class="balance-section gap"><h4>Hard gaps</h4>'
                '<div class="filler-line none">none of the on-hand items fill these — see Missing but useful</div></div>')
    else:
        if r["target_gap"]:
            lines = []
            for role in r["target_gap"]:
                fillers = r["suggested_fillers"].get(role, [])
                if fillers:
                    lines.append(f'<div class="filler-line"><span class="role">{_esc(role)}</span>'
                                 + " ".join(chip(f, "filler") for f in fillers) + "</div>")
                else:
                    lines.append(f'<div class="filler-line"><span class="role">{_esc(role)}</span><span class="none">(no curated filler)</span></div>')
            _md(f'<div class="balance-section gap"><h4>Missing — hard gaps</h4>{"".join(lines)}</div>')
        else:
            _md('<div class="balance-section have"><h4>Hard gaps</h4><div class="filler-line">none — all target roles covered</div></div>')

        if r["flagged_more"]:
            lines = []
            for role in r["flagged_more"]:
                fillers = r["suggested_fillers"].get(role, [])
                if fillers:
                    lines.append(f'<div class="filler-line"><span class="role">{_esc(role)}</span>'
                                 + " ".join(chip(f, "filler") for f in fillers) + "</div>")
                else:
                    lines.append(f'<div class="filler-line"><span class="role">{_esc(role)}</span><span class="none">(no curated filler)</span></div>')
            _md(f'<div class="balance-section more"><h4>May want more</h4>{"".join(lines)}</div>')

    warn_lines = []
    if r["leans_heavy"]:
        warn_lines.append('<div class="filler-line">leans heavy — favour acid / herb / crunch.</div>')
    if r["leans_dry"]:
        warn_lines.append('<div class="filler-line">leans dry — favour sauce / hydration / cream.</div>')
    avoid = []
    if r["avoid_more_richness"]:
        avoid.append("more fat / cream")
    if r["leans_dry"]:
        avoid.append("more dry items")
    if warn_lines:
        _md(f'<div class="balance-section warn"><h4>Risks</h4>{"".join(warn_lines)}</div>')
    if avoid:
        _md(f'<div class="balance-section warn"><h4>Avoid adding more of</h4><div class="chips">{chips(avoid)}</div></div>')

    if r["no_profile"]:
        items = [it["name"] for it in r["no_profile"]]
        _md(f'<div class="balance-section muted"><h4>No balance profile for</h4><div class="chips">{chips(items)}</div>'
            '<div class="filler-line none">add component_profiles entries for heaviness/dryness/missing-risk data.</div></div>')

    export_buttons(export.render_plate_markdown(r), "plate.md")


def tab_filler_profiles() -> None:
    ings = query.ingredients_list(CONN)
    default = "lemon" if "lemon" in ings else ings[0]
    subject, answer = st.columns(_SUBJECT_RATIO, gap="large")

    with subject:
        _md('<div class="eyebrow">Filler</div>')
        _seed("filler_profile_name", ings, default)
        name = st.selectbox("Filler", ings,
                            label_visibility="collapsed", format_func=_pretty,
                            key="filler_profile_name")
        d = query.filler_profile_detail(CONN, name)
        if not d["found"]:
            st.write(d["mode"])
            return
        kind_label = {"full": "both a filler and a full ingredient",
                      "both": "both a filler and a full ingredient",
                      "filler": "a filler — no technique tree of its own"}.get(
                          d["kind"], d["kind"])
        _md(subject_column_html(name, "filler", note=kind_label))
        if d["kind"] in ("full", "both"):
            _md('<div class="subject-block"></div>')
            st.button(f"See {_pretty(name)}'s branches", key="filler_to_explorer",
                      on_click=_goto_explorer, args=(name,))

    with answer:
        _md(f"""
        <div class="card">
          <div class="row"><span class="lbl">Roles</span><div class="chips">{chips(d["roles"], "flavour")}</div></div>
          <div class="row"><span class="lbl">Repairs</span><div class="chips">{chips(d["repairs"], "have")}</div></div>
          <div class="row"><span class="lbl">Avoid when</span><div class="chips">{chips(d["avoid_when"], "missing")}</div></div>
          <div class="row"><span class="lbl">FI shop</span><div class="val">{_esc(d["availability"])}</div></div>
          <div class="row"><span class="lbl">Mode</span><div class="val">{_esc(d["mode"])}</div></div>
        </div>
        """)
        _md('<div class="eyebrow">Pairings</div>')
        if d["pairings"]:
            rows = "".join(
                f'<tr><td>{_esc(p["role"])}</td>'
                f'<td>{_esc(_pretty(p["target"] + " " + p["technique"]) if p.get("target") else "(general)")}</td>'
                f'<td>{conf_pill(p["conf"])}</td></tr>'
                for p in d["pairings"][:8])
            _md('<table class="table"><thead><tr><th>Role</th>'
                '<th>Works best with</th><th>Confidence</th></tr></thead>'
                f'<tbody>{rows}</tbody></table>')
        else:
            _md('<div class="hint">No pairings recorded yet.</div>')


def _goto_explorer(name: str) -> None:
    st.session_state["explorer_ing"] = name
    st.session_state["active_section"] = "Cook"
    st.session_state["active_tab"] = "Ingredient Explorer"


def _scout_step(n: int) -> None:
    st.session_state.scout_index = st.session_state.get("scout_index", 0) + n


def _scout_goto(index: int) -> None:
    st.session_state.scout_index = index


def tab_scout(available_items: list[str] | None = None) -> None:
    """Scout — one hypothesis at a time, with its two claims kept separate."""
    on_hand = set(available_items or [])
    comps = query.components_list(CONN)
    state_comps = [c for c in comps
                   if query.component_state_profile(CONN, c) is not None]
    if not state_comps:
        _md('<div class="hint">No components with state profiles found. '
            'Run <code>foodprep build</code> first.</div>')
        return

    default = ("roasted_broccoli_component"
               if "roasted_broccoli_component" in state_comps else state_comps[0])
    subject, answer = st.columns(_SUBJECT_RATIO, gap="large")

    with subject:
        _md('<div class="eyebrow">Transformed state</div>')
        _seed("tab_scout_component_select", state_comps, default)
        comp = st.selectbox("Transformed state", state_comps,
                            label_visibility="collapsed", format_func=_pretty,
                            key="tab_scout_component_select")

    hypotheses = query.generate_scout_hypotheses(CONN, comp)
    candidates = [h for h in hypotheses if h["candidate_class"] != "rejected"]
    rejected = [h for h in hypotheses if h["candidate_class"] == "rejected"]

    # Which hypothesis is on show. Changing state starts again at the first.
    if st.session_state.get("scout_state") != comp:
        st.session_state.scout_state = comp
        st.session_state.scout_index = 0
    idx = st.session_state.get("scout_index", 0) % max(1, len(candidates))
    current = candidates[idx] if candidates else None

    profile = query.component_state_profile(CONN, comp)
    tags = (profile or {}).get("flavour_tags") or []
    pretty = comp.replace("_component", "").replace("_", " ")

    with subject:
        _md(subject_column_html(comp, "state"))
        if tags:
            _md(f'<div class="chips">'
                f'{chips([t.replace("_", " ") for t in tags], "flavour")}</div>')
        # Each other candidate is a button straight to its hypothesis; a plain
        # list meant pressing "Next" blind (usability pass, finding 7).
        others = [(i, h["candidate"]) for i, h in enumerate(candidates)
                  if i != idx]
        if others or rejected:
            _md('<div class="tcm-rule"></div>'
                '<div class="eyebrow">Other candidates</div>')
            with st.container(key="scout_others"):
                for i, name in others:
                    st.button(_pretty(name), key=f"scout_jump_{i}",
                              type="tertiary", on_click=_scout_goto, args=(i,))
            if rejected:
                _md(f'<div class="subject-note" style="color:var(--neutral-700)">'
                    f'{len(rejected)} rejected, with reasons</div>')

    with answer:
        _md('<div class="disclaimer">Hypotheses come from analogy rules applied '
            'to transformed states. They are <b>not classics</b>. Taste a small '
            'amount before serving.</div>')
        if not current:
            _md(f'<div class="hint">No generated hypotheses for '
                f'<b>{_esc(pretty)}</b>.</div>')
            return

        h = dict(current)
        h["pairing_title"] = f"{pretty.capitalize()} + {h['candidate'].replace('_', ' ')}"
        if h["candidate"] in on_hand:
            h["on_hand"] = h["candidate"]
        _md(hypothesis_card_html(h))
        _md(claim_cards_html(h))
        _md(smallest_test_html(h))

        act_record, act_next, _sp = st.columns([1.3, 1.2, 2])
        with act_record:
            # It shows how; it does not record (usability pass, finding 8).
            st.button("How to record a tasting", key="scout_record")
        with act_next:
            st.button("Next hypothesis", key="scout_next",
                      on_click=_scout_step, args=(1,),
                      disabled=len(candidates) < 2)
        if st.session_state.get("scout_record"):
            # Tastings are an append-only record written through the CLI;
            # the UI does not have a write path into the ontology.
            _md('<div class="hint">Tastings are recorded through the CLI so the '
                'append-only record stays the single source of truth. Run this '
                'in a terminal in the project folder, after changing the '
                'quoted parts to what actually happened:</div>')
            # One line: `\` continuations only work in bash, and this user's
            # Windows terminal is PowerShell (usability pass, finding 3).
            ratio = (h.get("protocol") or {}).get("starting_ratio") or "not measured"
            st.code(
                f"foodprep record-tasting {comp} {h['candidate']} "
                f"--verdict works --preparation \"what you did\" "
                f"--ratio \"{ratio}\" --temperature warm "
                f"--observations \"what you tasted\" --safety-confirmed",
                language="bash")
            _md('<div class="hint">Verdicts: works · promising · '
                'works_only_in_this_form · needs_adjustment · dominated · '
                'clashes · texturally_wrong · inconclusive.</div>')
        _md(trial_history_html(h))

        if rejected:
            with st.expander(f"Show {len(rejected)} rejected hypotheses",
                             expanded=False):
                for r in rejected:
                    rr = dict(r)
                    rr["pairing_title"] = (
                        f"{pretty.capitalize()} + {r['candidate'].replace('_', ' ')}")
                    _md(hypothesis_card_html(rr, lead=False))
                    if r.get("rejection_reason"):
                        _md(f'<div class="hint">{_esc(r["rejection_reason"])}</div>')


# The Circle and Cards views of Taste Circle build ONE dish. Both read and
# write the tcm_* state; Cards' per-dimension pickers are only an input.

def _tcm_init(state_comps: list[str]) -> None:
    defaults = {"tcm_locked": set, "tcm_selections": dict}
    for key, factory in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = factory()
    for key in ("tcm_expanded", "tcm_last_click"):
        st.session_state.setdefault(key, None)
    st.session_state.setdefault("tcm_page", 0)
    if st.session_state.get("tcm_component") not in state_comps:
        st.session_state.tcm_component = (
            "roasted_broccoli_component"
            if "roasted_broccoli_component" in state_comps else state_comps[0])


def _tc_lock(dim: str) -> None:
    """Selecting a filler locks its dimension — no separate Lock click."""
    choice = st.session_state.get(f"taste_circle_{dim}")
    if choice and choice != "(none)":
        st.session_state.tcm_locked.add(dim)
        st.session_state.tcm_selections[dim] = choice


def _tc_unlock(dim: str) -> None:
    st.session_state.tcm_locked.discard(dim)
    st.session_state.tcm_selections.pop(dim, None)
    st.session_state[f"taste_circle_{dim}"] = "(none)"


def _tc_component_changed() -> None:
    st.session_state.tcm_component = st.session_state.taste_circle_component
    _tcm_reset_cb()


def tab_taste_circle(available_items: list[str] | None = None) -> None:
    """Taste Circle — one dish, two ways to build it.

    Circle is the click-driven map; Cards is the same dish as a grid of
    eleven dimension cards with a picker each. They used to be two tabs with
    two separate dishes, so a filler chosen in one was missing from the other.
    """
    view = pill_radio("View", ["Circle", "Cards"], "tc_view")
    if view == "Cards":
        _taste_circle_cards()
    else:
        tab_taste_circle_map(available_items)


def _taste_circle_cards() -> None:
    """Eleven dimension cards in three columns; colour encodes state exactly as
    it does on the circle (provided / locked / open / no fillers yet). The
    right rail carries the dish and the two actions.
    """
    comps = query.components_list(CONN)
    state_comps = [c for c in comps
                   if query.component_state_profile(CONN, c) is not None]
    if not state_comps:
        _md('<div class="hint">No components with state profiles found. '
            'Run <code>foodprep build</code> first.</div>')
        return

    _tcm_init(state_comps)
    # Mirror the shared component into this view's picker before it is drawn,
    # so the Circle's arrows and this selectbox always agree.
    st.session_state.taste_circle_component = st.session_state.tcm_component
    grid, rail = st.columns([2.6, 1], gap="large")

    with grid:
        component = st.selectbox(
            "Component", state_comps, format_func=_pretty,
            label_visibility="collapsed", key="taste_circle_component",
            on_change=_tc_component_changed)

        profile = query.component_state_profile(CONN, component)
        provided = set((profile or {}).get("flavour_tags") or [])
        locked: set[str] = st.session_state.tcm_locked
        selections: dict[str, str] = st.session_state.tcm_selections
        fillers_by_dim = query.taste_circle_fillers(CONN, component, locked)

        pretty = component.replace("_component", "").replace("_", " ")
        _md(f'<div class="h2">Taste circle — {_esc(pretty)}</div>'
            f'<div class="hint">Fill a dimension and it locks. '
            f'{len(provided & {d for d, *_ in TASTE_DIMENSIONS})} are already '
            f'provided by the state itself.</div>')

        cols = st.columns(3)
        for i, (dim_key, icon, dim_name, _hue) in enumerate(TASTE_DIMENSIONS):
            with cols[i % 3]:
                title = f"{icon} {dim_name}"
                if dim_key in provided:
                    _md(f'<div class="dim-card provided">'
                        f'<div class="card-kicker">Provided</div>'
                        f'<div class="card-title">{_esc(title)}</div></div>')
                elif dim_key in locked:
                    _md(f'<div class="dim-card locked">'
                        f'<div class="card-kicker">Locked</div>'
                        f'<div class="card-title">{_esc(title)}</div>'
                        f'<div class="card-body">'
                        f'{_esc(selections.get(dim_key, "").replace("_", " "))}'
                        f'</div></div>')
                    st.button("Change", key=f"unlock_{dim_key}",
                              on_click=_tc_unlock, args=(dim_key,))
                elif fillers_by_dim.get(dim_key):
                    options = [f["filler"] for f in fillers_by_dim[dim_key]
                               if f["filler"] not in set(selections.values())]
                    preview = " · ".join(o.replace("_", " ") for o in options[:3])
                    # A dimension unlocked from the Circle view leaves this
                    # picker holding its old choice; clear it before drawing.
                    picker = f"taste_circle_{dim_key}"
                    if st.session_state.get(picker, "(none)") != "(none)":
                        st.session_state[picker] = "(none)"
                    _md(f'<div class="dim-card">'
                        f'<div class="card-kicker">{len(options)} '
                        f'option{"" if len(options) == 1 else "s"}</div>'
                        f'<div class="card-title">{_esc(title)}</div>'
                        f'<div class="card-body">{_esc(preview)}</div></div>')
                    st.selectbox(
                        f"Choose for {dim_name}", ["(none)"] + options,
                        key=f"taste_circle_{dim_key}", format_func=_pretty,
                        label_visibility="collapsed",
                        on_change=_tc_lock, args=(dim_key,))
                else:
                    _md(f'<div class="dim-card empty">'
                        f'<div class="card-kicker">No fillers yet</div>'
                        f'<div class="card-title">{_esc(title)}</div></div>')

    with rail:
        fillable = [d for d, *_ in TASTE_DIMENSIONS
                    if d not in provided and (fillers_by_dim.get(d) or d in locked)]
        rows = [f'<div class="tcm-dish-row"><span>{_esc(pretty)}</span>'
                f'<span class="tcm-dish-dim">base</span></div>']
        names = {k: n for k, _i, n, _c in TASTE_DIMENSIONS}
        for dim, filler in selections.items():
            rows.append(f'<div class="tcm-dish-row">'
                        f'<span>{_esc(filler.replace("_", " "))}</span>'
                        f'<span class="tcm-dish-dim">'
                        f'{_esc(names.get(dim, dim).lower())}</span></div>')
        _md('<div class="rail-card"><div class="card-kicker">Your dish</div>'
            + "".join(rows) + '<div class="tcm-rule"></div>'
            f'<div class="card-body">{len(locked)} of {len(fillable)} open '
            'dimensions filled. A plate does not need all eleven — only the '
            'ones this destination asks for.</div></div>')

        act_random, act_reset = st.columns([1.4, 1])
        with act_random:
            st.button("Surprise me", key="tc_random", type="primary",
                      on_click=_tcm_surprise, args=(component,))
        with act_reset:
            st.button("Reset", key="tc_reset", on_click=_tcm_reset_cb)

        if selections:
            _md('<div class="rail-card"><div class="card-kicker">Dish name</div>'
                f'<div class="tcm-dish-name">'
                f'{_esc(generate_dish_name(component, selections))}</div></div>')


def generate_dish_name(
    component: str, selections: dict[str, str]
) -> str:
    """Generate a dish name from the component and selections."""
    # Simple heuristic: combine component with key selections
    component_short = component.replace("_component", "").replace("_", " ")

    # Get the most interesting selections (prioritize by dimension)
    priority_dims = ["umami", "sour", "aromatic", "pungent"]
    key_selections = []

    for dim in priority_dims:
        if dim in selections:
            key_selections.append(selections[dim].replace("_", " "))
            if len(key_selections) >= 2:
                break

    if key_selections:
        return f"{component_short} with {' and '.join(key_selections)}"
    else:
        return f"Seasoned {component_short}"


#: The paging node's filler slot — mirrors graph.py::_MORE_SUFFIX.
TCM_MORE = "__more"


def tab_taste_circle_map(available_items: list[str] | None = None) -> None:
    """Taste Circle, Circle view — click-driven circular flavour builder.

    The interaction happens ON the circle (custom component): click a
    dimension to fan out its fillers, click a filler node to lock it in,
    click a locked dimension to change it, click blank canvas to close.
    The right rail is a read-out, never a picker — that distinction is what
    keeps this view different from Cards.
    """
    # Component list (only those that can anchor a taste circle)
    comps = query.components_list(CONN)
    state_comps = []
    for c in comps:
        if query.component_state_profile(CONN, c) is not None:
            state_comps.append(c)

    if not state_comps:
        st.markdown('<div class="hint">No components with state profiles found. '
                    'Run <code>foodprep build</code> first.</div>',
                    unsafe_allow_html=True)
        return

    def _reset() -> None:
        # Clear in place: the Reset/random buttons are rendered after `locked`
        # and `selections` are bound below, and those aliases must see it.
        st.session_state.tcm_locked.clear()
        st.session_state.tcm_selections.clear()
        st.session_state.tcm_expanded = None
        st.session_state.tcm_page = 0
        # Swallow the last graph click so it isn't re-processed afterwards.
        st.session_state.tcm_last_click = st.session_state.get("tcm_graph")

    _tcm_init(state_comps)

    on_hand = set(available_items or [])
    canvas, rail = st.columns([2.6, 1], gap="large")

    with canvas:
        idx = state_comps.index(st.session_state.tcm_component)
        nav_prev, nav_name, nav_next = st.columns([1, 8, 1])
        with nav_prev:
            if st.button("◀", key="tcm_prev", help="Previous component"):
                idx = (idx - 1) % len(state_comps)
        # The name sits between the arrows but must show the post-click
        # component, so reserve the slot and fill it once both are read.
        name_slot = nav_name.empty()
        with nav_next:
            if st.button("▶", key="tcm_next", help="Next component"):
                idx = (idx + 1) % len(state_comps)

        component = state_comps[idx]
        pretty = _pretty(component)
        name_slot.markdown(
            f'<div class="tcm-component-name">{pretty}'
            f'<span class="tcm-component-pos">{idx + 1} / {len(state_comps)}</span>'
            f'</div>',
            unsafe_allow_html=True)

        # Switching component starts a fresh circle.
        if st.session_state.tcm_component != component:
            _reset()
            st.session_state.tcm_component = component

        _md('<div class="hint">Click a dimension to see what fills it, '
            'click an ingredient to lock it in.</div>')

        locked: set[str] = st.session_state.tcm_locked
        selections: dict[str, str] = st.session_state.tcm_selections

        # Pre-click state — validates incoming clicks and random picks.
        profile = query.component_state_profile(CONN, component)
        provided = set(profile["flavour_tags"]) if profile else set()
        fillers_by_dim = query.taste_circle_fillers(CONN, component, locked)

        # Handle a pending click BEFORE redrawing, so the new state shows
        # in this same rerun.
        click = st.session_state.get("tcm_graph")
        if click and click != st.session_state.tcm_last_click:
            st.session_state.tcm_last_click = click
            click_id = click.get("id")
            if click_id is None:
                st.session_state.tcm_expanded = None      # blank canvas
            elif click_id.startswith("dim:"):
                dim = click_id[4:]
                if dim in locked:
                    locked.remove(dim)
                    selections.pop(dim, None)
                    st.session_state.tcm_expanded = None
                elif dim == st.session_state.tcm_expanded:
                    st.session_state.tcm_expanded = None
                elif fillers_by_dim.get(dim):
                    st.session_state.tcm_expanded = dim
                    st.session_state.tcm_page = 0
            elif click_id.startswith("filler:"):
                _prefix, dim, filler = click_id.split(":", 2)
                if filler == TCM_MORE:
                    st.session_state.tcm_page += 1        # page the fan
                else:
                    valid = any(f["filler"] == filler
                                for f in fillers_by_dim.get(dim, []))
                    if valid and filler not in selections.values():
                        locked.add(dim)
                        selections[dim] = filler
                        st.session_state.tcm_expanded = None
                        st.session_state.tcm_page = 0

        # Recompute after click handling: the progress line and the rail must
        # both reflect the post-click state.
        fillers_by_dim = query.taste_circle_fillers(CONN, component, locked)
        expanded = st.session_state.tcm_expanded

        data = taste_circle_graph_data(
            CONN, component,
            locked_dimensions=locked,
            selections=selections,
            expanded_dimension=expanded,
            available=on_hand,
            page=st.session_state.tcm_page,
        )
        taste_circle_map(nodes=data["nodes"], edges=data["edges"], height=640,
                         key="tcm_graph")

        _md('<div class="tcm-legend">'
            '<span><i class="sw sw-provided"></i>already provided</span>'
            '<span><i class="sw sw-open"></i>open — size is how many fit</span>'
            '<span><i class="sw sw-thin"></i>thin — one option only</span>'
            '</div>')

    with rail:
        _taste_circle_rail(component, expanded, fillers_by_dim, selections,
                           locked, provided, on_hand)



def _taste_circle_rail(component: str, expanded: str | None,
                       fillers_by_dim: dict, selections: dict[str, str],
                       locked: set[str], provided: set[str],
                       on_hand: set[str]) -> None:
    """The right rail: a read-out of the circle, never a second picker."""
    names = {k: (icon, name) for k, icon, name, _ in TASTE_DIMENSIONS}

    if expanded and fillers_by_dim.get(expanded):
        options = [f["filler"] for f in fillers_by_dim[expanded]
                   if f["filler"] not in set(selections.values())]
        icon, label = names.get(expanded, ("", expanded))
        have = [o.replace("_", " ") for o in options if o in on_hand]
        if have:
            body = (f"{_join_names(have)} "
                    f"{'is' if len(have) == 1 else 'are'} in your kitchen.")
        else:
            body = "None of these are in your kitchen right now."
        _md(f'<div class="rail-card">'
            f'<div class="card-kicker">{icon} {label} — {len(options)} options</div>'
            f'<div class="card-title">What fits here</div>'
            f'<div class="card-body">{_esc(body)} Click a node on the circle '
            f'to lock it in — the circle re-reads, and what is still open '
            f'changes with it.</div></div>')
    else:
        _md('<div class="rail-card rail-idle">'
            '<div class="card-kicker">Nothing expanded</div>'
            '<div class="card-body">Click a dimension on the circle to see '
            'what can fill it.</div></div>')

    # ---- Your dish -------------------------------------------------------
    fillable = [d for d, _i, _n, _c in TASTE_DIMENSIONS
                if d not in provided and (fillers_by_dim.get(d) or d in locked)]
    base = component.replace("_component", "").replace("_", " ")
    rows = [f'<div class="tcm-dish-row"><span>{_esc(base)}'
            f'</span><span class="tcm-dish-dim">base</span></div>']
    for dim, filler in selections.items():
        _icon, label = names.get(dim, ("", dim))
        rows.append(f'<div class="tcm-dish-row"><span>'
                    f'{_esc(filler.replace("_", " "))}</span>'
                    f'<span class="tcm-dish-dim">{_esc(label.lower())}</span></div>')

    _md('<div class="rail-card">'
        '<div class="card-kicker">Your dish</div>'
        + "".join(rows) +
        '<div class="tcm-rule"></div>'
        f'<div class="card-body">{len(locked)} of {len(fillable)} open '
        'dimensions filled. A plate does not need all eleven — only the ones '
        'this destination asks for.</div></div>')

    act_random, act_reset = st.columns([1.4, 1])
    with act_random:
        st.button("Surprise me", key="tcm_random", type="primary",
                  help="Fill every open dimension with a random valid pick",
                  on_click=_tcm_surprise, args=(component,))
    with act_reset:
        st.button("Reset", key="tcm_reset", on_click=_tcm_reset_cb)

    if selections:
        _md(f'<div class="rail-card">'
            f'<div class="card-kicker">Dish name</div>'
            f'<div class="tcm-dish-name">'
            f'{_esc(generate_dish_name(component, selections))}</div></div>')


def _join_names(items: list[str]) -> str:
    if len(items) == 1:
        return items[0]
    return ", ".join(items[:-1]) + " and " + items[-1]


def _tcm_reset_cb() -> None:
    st.session_state.tcm_locked.clear()
    st.session_state.tcm_selections.clear()
    st.session_state.tcm_expanded = None
    st.session_state.tcm_page = 0
    st.session_state.tcm_last_click = st.session_state.get("tcm_graph")


def _tcm_surprise(component: str) -> None:
    locked = st.session_state.tcm_locked
    selections = st.session_state.tcm_selections
    pool = query.taste_circle_fillers(CONN, component, locked)
    for dim, filler in random_dish_selections(pool, selections).items():
        locked.add(dim)
        selections[dim] = filler
    st.session_state.tcm_expanded = None
    st.session_state.tcm_page = 0


#: Tab label -> renderer. Renderers taking the availability list are called
#: with it; the rest take nothing.
TABS: dict[str, Any] = {
    "Ingredient Explorer": tab_ingredient_explorer,
    "Component Explorer": tab_component_explorer,
    "Plate Balance": tab_plate_balance,
    "Taste Circle": tab_taste_circle,
    "Map": tab_map,
    "Journeys": tab_journeys,
    "Filler Profiles": tab_filler_profiles,
    "Scout": tab_scout,
}
#: What a cook is trying to do, then where. Cook answers "what do I make",
#: Explore is reference, Experiment is untested ideas — kept apart on purpose
#: so a Scout hypothesis never sits next to a Cook suggestion.
SECTIONS: dict[str, list[str]] = {
    "Cook": ["Ingredient Explorer", "Component Explorer", "Plate Balance",
             "Taste Circle"],
    "Explore": ["Map", "Journeys", "Filler Profiles"],
    "Experiment": ["Scout"],
}
_TABS_WITH_AVAILABLE = {
    "Ingredient Explorer", "Component Explorer", "Plate Balance",
    "Taste Circle", "Scout",
}


#: Selector widgets whose value must outlive a trip to another tab. This is an
#: allow-list on purpose: re-assigning a *button* key makes Streamlit refuse to
#: create the button ("cannot be set using st.session_state"), so a blanket
#: sweep breaks the app the second time you open a tab that has one.
#: tests/test_ui_state.py fails if a selector widget is added and not listed.
_STICKY_WIDGETS = frozenset({
    "active_tab",
    "available_items",
    "active_section",
    "explorer_ing", "explorer_mode", "explorer_tech",
    "map_ing", "map_view", "journey_ing", "tc_view",
    "component_explorer_comp",
    "plate_items",
    "filler_profile_name",
    "tab_scout_component_select",
    "taste_circle_component",
})

#: Widgets keyed dynamically (one per flavour dimension in Taste Circle)
#: cannot be listed by name, so they are persisted by prefix instead.
#: No button key may start with one of these.
_STICKY_PREFIXES = ("taste_circle_",)


def _persist_widget_state() -> None:
    """Keep selector values alive across tab switches.

    ``st.tabs`` rendered all ten tabs every run, so every widget stayed
    instantiated. The rail renders only the active tab, and Streamlit
    garbage-collects the state of any widget it did not draw — a selection
    would be lost the moment you looked at another tab. Re-assigning a key to
    itself marks it as set and survives the sweep.
    """
    for key in _STICKY_WIDGETS:
        if key in st.session_state:
            st.session_state[key] = st.session_state[key]
    for key in [k for k in st.session_state if k.startswith(_STICKY_PREFIXES)]:
        st.session_state[key] = st.session_state[key]


def _section_changed() -> None:
    """Land on the section's first tab, not on a stale tab from another one."""
    tabs = SECTIONS[st.session_state.active_section]
    if st.session_state.get("active_tab") not in tabs:
        st.session_state.active_tab = tabs[0]


def tab_rail() -> str:
    """Section pills, then the section's tabs; returns the active tab label.

    Radios, not ``st.pills``: pills cannot be deselected back to a valid
    state, and AppTest cannot serialize a single-select pill group (it walks
    the value string character by character), which would cost us the smoke
    tests. CSS turns the radios into the handoff's pill rows.
    """
    # A tab saved from an older layout (e.g. "Scout Map") or set by a
    # jump button decides the section, and must exist before widgets draw.
    if st.session_state.get("active_tab") not in TABS:
        st.session_state.pop("active_tab", None)
    section = st.session_state.get("active_section")
    tab = st.session_state.get("active_tab")
    if tab and (section not in SECTIONS or tab not in SECTIONS[section]):
        st.session_state.active_section = next(
            name for name, tabs in SECTIONS.items() if tab in tabs)
    elif section not in SECTIONS:
        st.session_state.active_section = "Cook"

    with st.container(key="section_rail_pills"):
        section = st.radio(
            "Section", list(SECTIONS), horizontal=True,
            label_visibility="collapsed", key="active_section",
            on_change=_section_changed)
    tabs = SECTIONS[section]
    if st.session_state.get("active_tab") not in tabs:
        st.session_state.active_tab = tabs[0]
    if len(tabs) > 1:
        with st.container(key="tab_rail_pills"):
            active = st.radio(
                "Tab", tabs, horizontal=True,
                label_visibility="collapsed", key="active_tab",
            )
    else:
        active = tabs[0]
    _md('<div class="tab-rule"></div>')
    return active


def main() -> None:
    if not st.session_state.get("_page_configured"):
        st.set_page_config(
            page_title="food-prep",
            page_icon="🍅",
            layout="wide",
            initial_sidebar_state="collapsed",
        )
        st.session_state["_page_configured"] = True
    if _CSS_PATH.exists():
        st.markdown(f"<style>{_CSS_PATH.read_text(encoding='utf-8')}</style>",
                    unsafe_allow_html=True)
    _persist_widget_state()
    topbar()
    # The strip sits above the rail but only belongs on tabs that use it, and
    # which tab is active is known only once the rail has run — so reserve
    # its slot first and fill it afterwards. The selection itself is sticky,
    # so it survives a visit to a tab that hides the strip.
    strip = st.container()
    active = tab_rail()
    render = TABS[active]
    if active in _TABS_WITH_AVAILABLE:
        with strip:
            available_items = available_selector()
        render(available_items)
    else:
        render()


if __name__ == "__main__":
    main()
