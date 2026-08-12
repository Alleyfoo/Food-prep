"""Food-prep — ingredient transformation graph UI (Streamlit).

Tabs:
  Tab 1  Ingredient Explorer  — branch_card / all_branch_cards
  Tab 2  Map                  — interactive ingredient mindmap (pyvis)
  Tab 3  Scout Map            — Scout hypotheses graph (pyvis)
  Tab 4  Journeys             — ingredient_journeys
  Tab 5  Component Explorer   — component_card + flavour_routes
  Tab 6  Plate Balance        — plate_balance_detail
  Tab 7  Filler Profiles      — filler_profile_detail
  Tab 8  Scout                — generate_scout_hypotheses + trials
  Tab 9  Taste Circle         — flavour wheel builder (buttons)
  Tab 10 Taste Circle Map     — click-driven circular flavour builder

Run:  streamlit run app.py
"""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any

import streamlit as st
import streamlit.components.v1 as components

from foodprep.loader import build
from foodprep import export, query
from foodprep.ui.render import (
    _esc, chip, chips, conf_pill, debug_block, tag_class,
    available_partition_html, branch_card_html, subject_column_html,
    hypothesis_card_html, journey_card_html, route_card_html,
)
from foodprep.ui.graph import (
    TASTE_DIMENSIONS, build_ingredient_graph, build_scout_graph,
    graph_to_html, random_dish_selections, taste_circle_graph_data,
)
from foodprep.ui.taste_circle import taste_circle_map

_CSS_PATH = Path(__file__).with_name("design.css")


def _md(markup: str) -> None:
    cleaned = "\n".join(line.lstrip() for line in markup.splitlines())
    st.markdown(cleaned.strip(), unsafe_allow_html=True)


@st.cache_resource
def get_conn():
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    build(conn)
    return conn


CONN = get_conn()


def export_buttons(md: str, filename: str) -> None:
    if not md:
        return
    st.download_button("Download .md", md, file_name=filename,
                       mime="text/markdown", key=f"dl_{filename}")
    with st.expander("Markdown", expanded=False):
        st.code(md, language="markdown")


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
            label_visibility="collapsed",
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
        ingredient = st.selectbox(
            "Ingredient", trees, key="explorer_ing",
            label_visibility="collapsed",
            index=trees.index("cabbage") if "cabbage" in trees else 0)
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
            tech = st.selectbox("Technique", techs, key="explorer_tech")
            card = query.branch_card(CONN, ingredient, tech)
            if card:
                part = (query.available_filter(CONN, card["transformation_id"], avail)
                        if avail else None)
                _md(branch_card_html(card, available=part, lead=True))
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
                # the top-ranked branch carries the accent border
                _md(branch_card_html(c, available=part, lead=(i == 0)))
                md_parts.append(export.render_branch_markdown(c, part))
            export_buttons("\n\n---\n\n".join(md_parts), "branches.md")


def tab_map() -> None:
    st.markdown('<div class="section-title">Map <span class="count">'
                'interactive ingredient mindmap</span></div>',
                unsafe_allow_html=True)
    st.markdown(
        '<div class="hint">Select an ingredient to see its transformation tree: '
        'how it can be cooked, what components it becomes, what fillers pair with it, '
        'and what flavour routes it opens. Drag nodes to explore.</div>',
        unsafe_allow_html=True)
    trees = query.tree_ingredients(CONN)
    ingredient = st.selectbox("Ingredient", trees, key="map_ing",
                              index=trees.index("broccoli") if "broccoli" in trees else 0)
    net = build_ingredient_graph(CONN, ingredient)
    html = graph_to_html(net)
    components.html(html, height=620, scrolling=False)


def tab_scout_map() -> None:
    st.markdown('<div class="section-title">Scout Map <span class="count">'
                'generated hypotheses from analogy rules</span></div>',
                unsafe_allow_html=True)
    st.markdown(
        '<div class="hint">Select an ingredient to see Scout hypotheses for its '
        'transformed states. Diamond nodes = scout_candidate (3+ compatibility evidence), '
        'dot nodes = weak_hypothesis. Drag nodes to explore.</div>',
        unsafe_allow_html=True)
    trees = query.tree_ingredients(CONN)
    ingredient = st.selectbox("Ingredient", trees, key="scout_map_ing",
                              index=trees.index("broccoli") if "broccoli" in trees else 0)
    net = build_scout_graph(CONN, ingredient)
    html = graph_to_html(net)
    components.html(html, height=620, scrolling=False)


def tab_journeys() -> None:
    st.markdown('<div class="section-title">Journeys <span class="count">'
                'complete Cook paths for an ingredient</span></div>',
                unsafe_allow_html=True)
    trees = query.tree_ingredients(CONN)
    ingredient = st.selectbox("Ingredient", trees, key="journey_ing",
                              index=trees.index("broccoli") if "broccoli" in trees else 0)
    journeys = query.ingredient_journeys(CONN, ingredient)
    if not journeys:
        st.markdown(
            f'<div class="hint">No complete journeys modelled for <b>{_esc(ingredient)}</b> yet.</div>',
            unsafe_allow_html=True)
        return
    st.markdown(
        f'<div class="eyebrow">{len(journeys)} journey{"s" if len(journeys) != 1 else ""}</div>',
        unsafe_allow_html=True)
    for j in journeys:
        _md(journey_card_html(j))


def tab_component_explorer(available_items: list[str] | None = None) -> None:
    comps = query.components_list(CONN)
    default = "roasted_tomato_component" if "roasted_tomato_component" in comps else comps[0]
    subject, answer = st.columns(_SUBJECT_RATIO, gap="large")

    with subject:
        _md('<div class="eyebrow">Component — an after-state</div>')
        comp = st.selectbox("Component", comps, index=comps.index(default),
                            label_visibility="collapsed",
                            key="component_explorer_comp")
    d = query.component_card(CONN, comp)
    if not d:
        with answer:
            st.write("No component named", comp)
        return
    producers = d.get("produced_by") or []
    prod_str = ", ".join(f"{p['ingredient']} + {p['technique']}" for p in producers) or "(no producing transformation)"
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
          {debug_block("Show data rows", d)}
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


def tab_plate_balance(available_items: list[str] | None = None) -> None:
    st.markdown('<div class="section-title">Plate Balance <span class="count">Cook mode — no experimental pairings</span></div>',
                unsafe_allow_html=True)
    profiles = query.profiles_list(CONN)
    picked = st.multiselect("Plate items", profiles, key="plate_items",
                            default=["mashed_potatoes", "chickpea_patty"])
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
    h_cls = "k-warn k-heavy" if r["leans_heavy"] else "k-ok"
    _md(f"""
    <div class="kpis">
      <div class="kpi"><div class="lbl">Items</div><div class="val">{len(r['items'])}</div><div class="foot">on the plate</div></div>
      <div class="kpi {'k-risk' if gap_n else ''}"><div class="lbl">Hard gaps</div><div class="val">{gap_n}</div><div class="foot">target roles missing</div></div>
      <div class="kpi k-warn"><div class="lbl">May want more</div><div class="val">{more_n}</div><div class="foot">soft flags</div></div>
      <div class="kpi {h_cls}"><div class="lbl">Heaviness</div><div class="val">{r['plate_heaviness'] if r['plate_heaviness'] is not None else '—'}</div><div class="foot">{r['heaviness_label'] or 'unknown'}</div></div>
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
    if r["leans_heavy"]:
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

    with st.expander("Debug — raw plate_balance_detail", expanded=False):
        st.json(r)


def tab_filler_profiles() -> None:
    ings = query.ingredients_list(CONN)
    default = "lemon" if "lemon" in ings else ings[0]
    subject, answer = st.columns(_SUBJECT_RATIO, gap="large")

    with subject:
        _md('<div class="eyebrow">Filler</div>')
        name = st.selectbox("Filler", ings, index=ings.index(default),
                            label_visibility="collapsed",
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
            st.button(f"See {name}'s branches", key="filler_to_explorer",
                      on_click=_goto_explorer, args=(name,))

    with answer:
        _md(f"""
        <div class="card">
          <div class="row"><span class="lbl">Roles</span><div class="chips">{chips(d["roles"], "flavour")}</div></div>
          <div class="row"><span class="lbl">Repairs</span><div class="chips">{chips(d["repairs"], "have")}</div></div>
          <div class="row"><span class="lbl">Avoid when</span><div class="chips">{chips(d["avoid_when"], "missing")}</div></div>
          <div class="row"><span class="lbl">FI shop</span><div class="val">{_esc(d["availability"])}</div></div>
          <div class="row"><span class="lbl">Mode</span><div class="val">{_esc(d["mode"])}</div></div>
          {debug_block("Show data rows", d)}
        </div>
        """)
        _md('<div class="eyebrow">Pairings</div>')
        if d["pairings"]:
            rows = "".join(
                f'<tr><td>{_esc(p["role"])}</td>'
                f'<td>{_esc((p["target"] + " " + p["technique"]) if p.get("target") else "(general)")}</td>'
                f'<td>{conf_pill(p["conf"])}</td></tr>'
                for p in d["pairings"][:8])
            _md('<table class="table"><thead><tr><th>Role</th>'
                '<th>Works best with</th><th>Confidence</th></tr></thead>'
                f'<tbody>{rows}</tbody></table>')
        else:
            _md('<div class="hint">No pairings recorded yet.</div>')


def _goto_explorer(name: str) -> None:
    st.session_state["explorer_ing"] = name
    st.session_state["active_tab"] = "Ingredient Explorer"


def tab_scout() -> None:
    st.markdown('<div class="section-title">Scout <span class="count">'
                'generated hypotheses from analogy rules</span></div>',
                unsafe_allow_html=True)
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

    default = "roasted_broccoli_component" if "roasted_broccoli_component" in state_comps else state_comps[0]
    subject, answer = st.columns(_SUBJECT_RATIO, gap="large")

    with subject:
        _md('<div class="eyebrow">Transformed state</div>')
        comp = st.selectbox("Transformed state", state_comps,
                            index=state_comps.index(default),
                            label_visibility="collapsed",
                            key="tab_scout_component_select")
        profile = query.component_state_profile(CONN, comp)
        tags = (profile or {}).get("flavour_tags") or []
        _md(subject_column_html(comp, "state"))
        if tags:
            _md(f'<div class="chips subject-block">'
                f'{chips([t.replace("_", " ") for t in tags], "flavour")}</div>')

    hypotheses = query.generate_scout_hypotheses(CONN, comp)
    candidates = [h for h in hypotheses if h["candidate_class"] != "rejected"]
    rejected = [h for h in hypotheses if h["candidate_class"] == "rejected"]

    with subject:
        if hypotheses:
            _md('<div class="eyebrow subject-block">Other candidates</div>'
                + "".join(
                    f'<div class="subject-note">{_esc(h["candidate"].replace("_", " "))}</div>'
                    for h in candidates[1:])
                + (f'<div class="subject-note" style="color:var(--neutral-700)">'
                   f'{len(rejected)} rejected, with reasons</div>' if rejected else ""))

    with answer:
        _md("""
        <div class="disclaimer">
          <span class="eyebrow">Scout mode</span>
          Hypotheses come from reusable analogy rules applied to transformed
          states. They are <b>not classics</b> — they are role-compatible but
          uncommon. Taste a small amount before serving.
        </div>
        """)
        if not hypotheses:
            _md(f'<div class="hint">No generated hypotheses for '
                f'<b>{_esc(comp)}</b>.</div>')
            return
        _md(f'<div class="eyebrow">{len(candidates)} '
            f'candidate{"s" if len(candidates) != 1 else ""} · '
            f'{len(rejected)} rejected</div>')
        for i, h in enumerate(candidates):
            _md(hypothesis_card_html(h, lead=(i == 0)))
        if rejected:
            with st.expander(f"Show {len(rejected)} rejected hypotheses",
                             expanded=False):
                for h in rejected:
                    _md(hypothesis_card_html(h))


def _tc_lock(dim: str) -> None:
    """Selecting a filler locks its dimension — no separate Lock click."""
    choice = st.session_state.get(f"taste_circle_{dim}")
    if choice and choice != "(none)":
        st.session_state.taste_circle_locked.add(dim)
        st.session_state.taste_circle_selections[dim] = choice


def _tc_unlock(dim: str) -> None:
    st.session_state.taste_circle_locked.discard(dim)
    st.session_state.taste_circle_selections.pop(dim, None)
    st.session_state[f"taste_circle_{dim}"] = "(none)"


def _tc_reset() -> None:
    for dim in list(st.session_state.taste_circle_locked):
        st.session_state[f"taste_circle_{dim}"] = "(none)"
    st.session_state.taste_circle_locked.clear()
    st.session_state.taste_circle_selections.clear()


def _tc_surprise(component: str) -> None:
    locked = st.session_state.taste_circle_locked
    selections = st.session_state.taste_circle_selections
    pool = query.taste_circle_fillers(CONN, component, locked)
    for dim, filler in random_dish_selections(pool, selections).items():
        locked.add(dim)
        selections[dim] = filler


def tab_taste_circle() -> None:
    """Taste Circle — the same builder as the map, read as a card grid.

    Eleven dimension cards in three columns; colour encodes state exactly as
    it does on the circle (provided / locked / open / no fillers yet). The
    right rail carries the dish and the two actions.
    """
    if "taste_circle_locked" not in st.session_state:
        st.session_state.taste_circle_locked = set()
    if "taste_circle_selections" not in st.session_state:
        st.session_state.taste_circle_selections = {}

    comps = query.components_list(CONN)
    state_comps = [c for c in comps
                   if query.component_state_profile(CONN, c) is not None]
    if not state_comps:
        _md('<div class="hint">No components with state profiles found. '
            'Run <code>foodprep build</code> first.</div>')
        return

    default = ("roasted_broccoli_component"
               if "roasted_broccoli_component" in state_comps else state_comps[0])
    grid, rail = st.columns([2.6, 1], gap="large")

    with grid:
        component = st.selectbox(
            "Component", state_comps, index=state_comps.index(default),
            label_visibility="collapsed", key="taste_circle_component")

        profile = query.component_state_profile(CONN, component)
        provided = set((profile or {}).get("flavour_tags") or [])
        locked: set[str] = st.session_state.taste_circle_locked
        selections: dict[str, str] = st.session_state.taste_circle_selections
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
                    _md(f'<div class="dim-card">'
                        f'<div class="card-kicker">{len(options)} '
                        f'option{"" if len(options) == 1 else "s"}</div>'
                        f'<div class="card-title">{_esc(title)}</div>'
                        f'<div class="card-body">{_esc(preview)}</div></div>')
                    st.selectbox(
                        f"Choose for {dim_name}", ["(none)"] + options,
                        key=f"taste_circle_{dim_key}",
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
                      on_click=_tc_surprise, args=(component,))
        with act_reset:
            st.button("Reset", key="tc_reset", on_click=_tc_reset)

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
    """Taste Circle Map tab — click-driven circular flavour builder.

    The interaction happens ON the circle (custom component): click a
    dimension to fan out its fillers, click a filler node to lock it in,
    click a locked dimension to change it, click blank canvas to close.
    The right rail is a read-out, never a picker — that distinction is what
    keeps this tab different from Taste Circle.
    """
    # Session state
    if "tcm_locked" not in st.session_state:
        st.session_state.tcm_locked = set()
    if "tcm_selections" not in st.session_state:
        st.session_state.tcm_selections = {}
    if "tcm_expanded" not in st.session_state:
        st.session_state.tcm_expanded = None
    if "tcm_last_click" not in st.session_state:
        st.session_state.tcm_last_click = None
    if "tcm_component" not in st.session_state:
        st.session_state.tcm_component = None
    if "tcm_page" not in st.session_state:
        st.session_state.tcm_page = 0

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

    if st.session_state.tcm_component not in state_comps:
        st.session_state.tcm_component = (
            "roasted_broccoli_component"
            if "roasted_broccoli_component" in state_comps
            else state_comps[0]
        )

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
        pretty = component.replace("_component", "").replace("_", " ")
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


#: Tab label -> renderer. Order is the handoff's and is unchanged. Renderers
#: taking the availability list are called with it; the rest take nothing.
TABS: dict[str, Any] = {
    "Ingredient Explorer": tab_ingredient_explorer,
    "Map": tab_map,
    "Scout Map": tab_scout_map,
    "Journeys": tab_journeys,
    "Component Explorer": tab_component_explorer,
    "Plate Balance": tab_plate_balance,
    "Filler Profiles": tab_filler_profiles,
    "Scout": tab_scout,
    "Taste Circle": tab_taste_circle,
    "Taste Circle Map": tab_taste_circle_map,
}
_TABS_WITH_AVAILABLE = {
    "Ingredient Explorer", "Component Explorer", "Plate Balance",
    "Taste Circle Map",
}


#: Selector widgets whose value must outlive a trip to another tab. This is an
#: allow-list on purpose: re-assigning a *button* key makes Streamlit refuse to
#: create the button ("cannot be set using st.session_state"), so a blanket
#: sweep breaks the app the second time you open a tab that has one.
#: tests/test_ui_state.py fails if a selector widget is added and not listed.
_STICKY_WIDGETS = frozenset({
    "active_tab",
    "available_items",
    "explorer_ing", "explorer_mode", "explorer_tech",
    "map_ing", "scout_map_ing", "journey_ing",
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


def tab_rail() -> str:
    """The ten tabs as a wrapping row of pills; returns the active label.

    A radio, not ``st.pills``: pills cannot be deselected back to a valid
    state, and AppTest cannot serialize a single-select pill group (it walks
    the value string character by character), which would cost us the smoke
    tests. CSS turns the radio into the handoff's pill row.
    """
    with st.container(key="tab_rail_pills"):
        active = st.radio(
            "Section", list(TABS), horizontal=True,
            label_visibility="collapsed", key="active_tab",
        )
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
    available_items = available_selector()
    active = tab_rail()
    render = TABS[active]
    if active in _TABS_WITH_AVAILABLE:
        render(available_items)
    else:
        render()


if __name__ == "__main__":
    main()
