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
    available_partition_html, branch_card_html,
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


def tab_ingredient_explorer(available_items: list[str] | None = None) -> None:
    st.markdown('<div class="section-title">Ingredient Explorer</div>',
                unsafe_allow_html=True)
    trees = query.tree_ingredients(CONN)
    col1, col2 = st.columns([1, 1])
    with col1:
        ingredient = st.selectbox("Ingredient", trees, key="explorer_ing",
                                  index=trees.index("cabbage") if "cabbage" in trees else 0)
    with col2:
        mode = st.radio("Mode", ["Best branches", "Choose technique"],
                        horizontal=True, key="explorer_mode")

    avail = available_items or None
    techs = query.techniques_for_ingredient(CONN, ingredient)
    if mode == "Choose technique":
        tech = st.selectbox("Technique", techs, key="explorer_tech")
        card = query.branch_card(CONN, ingredient, tech)
        if card:
            part = (query.available_filter(CONN, card["transformation_id"], avail)
                    if avail else None)
            _md(branch_card_html(card, available=part))
            export_buttons(export.render_branch_markdown(card, part), "branch.md")
        else:
            st.write(f"No transformation for {ingredient}/{tech}.")
    else:
        cards = query.all_branch_cards(CONN, ingredient)
        shown = cards[:5]
        st.markdown(
            f'<div class="eyebrow">Showing top {len(shown)} of {len(cards)} branches · '
            f'ranked cooking-before-preservation</div>', unsafe_allow_html=True)
        md_parts = []
        for c in shown:
            part = (query.available_filter(CONN, c["transformation_id"], avail)
                    if avail else None)
            _md(branch_card_html(c, available=part))
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
    st.markdown('<div class="section-title">Component Explorer</div>',
                unsafe_allow_html=True)
    comps = query.components_list(CONN)
    default = "roasted_tomato_component" if "roasted_tomato_component" in comps else comps[0]
    comp = st.selectbox("Component", comps, index=comps.index(default),
                        key="component_explorer_comp")
    d = query.component_card(CONN, comp)
    if not d:
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

    _md(f"""
    <div class="card info">
      <div class="card-head"><span class="card-tech">{_esc(d["name"])}</span>
        <span class="card-comp">{_esc(d.get("kind") or "")}</span></div>
      <div class="card-shift">came from: <b>{_esc(prod_str)}</b></div>
      <div class="row"><span class="lbl">Storage</span><div class="val">
        keeps {_esc(d.get("keeps_well") or "—")} ·
        freezes: {"yes" if d.get("freezes_well") else "no"} ·
        batch: {_esc(d.get("batch_prep_value") or "—")}</div></div>
      <div class="row"><span class="lbl">Tags</span><div class="chips">{tag_chips or '<span class="chip" style="color:var(--ink-5)">—</span>'}</div></div>
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
        st.markdown(
            f'<div class="section-title">Flavour Routes <span class="count">'
            f'{len(routes)} direction{"s" if len(routes) != 1 else ""} from this state</span></div>',
            unsafe_allow_html=True)
        for r in routes:
            _md(route_card_html(r))

    st.markdown(
        '<div class="hint">A component is an <b>after-state</b>. You do not always '
        'start from raw cabbage/tomato/potato — pick the component you already have.</div>',
        unsafe_allow_html=True)


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
    h_cls = "k-warn" if r["leans_heavy"] else "k-ok"
    _md(f"""
    <div class="kpis">
      <div class="kpi"><div class="lbl">Items</div><div class="val">{len(r['items'])}</div><div class="foot">on the plate</div></div>
      <div class="kpi k-risk"><div class="lbl">Hard gaps</div><div class="val">{gap_n}</div><div class="foot">target roles missing</div></div>
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
    st.markdown('<div class="section-title">Filler Profiles <span class="count">the PIM tab</span></div>',
                unsafe_allow_html=True)
    ings = query.ingredients_list(CONN)
    default = "lemon" if "lemon" in ings else ings[0]
    name = st.selectbox("Filler", ings, index=ings.index(default),
                        key="filler_profile_name")
    d = query.filler_profile_detail(CONN, name)
    if not d["found"]:
        st.write(d["mode"])
        return
    mode_cls = {"cook": "cook", "scout": "scout", "both": "info", "none": "muted"}[d["mode_kind"]]
    kind_label = {"full": "full ingredient (has a technique tree)",
                  "both": "both (technique tree + filler)",
                  "filler": "filler"}.get(d["kind"], d["kind"])
    pair_rows = []
    for p in d["pairings"][:8]:
        tgt = f"{p['target']} {p['technique']}" if p.get("target") else "(general)"
        pair_rows.append(
            f'<div class="row"><span class="lbl">{_esc(p["role"])}</span><div class="val">'
            f'{_esc(tgt)} <span class="chip {p["conf"]}">{_esc(p["conf"])}</span></div></div>'
        )
    _md(f"""
    <div class="card {mode_cls}">
      <div class="card-head"><span class="card-tech">{_esc(d["name"])}</span>
        <span class="card-comp">{_esc(kind_label)}</span></div>
      <div class="row"><span class="lbl">Roles</span><div class="chips">{chips(d["roles"])}</div></div>
      <div class="row"><span class="lbl">Repairs</span><div class="chips">{chips(d["repairs"])}</div></div>
      <div class="row"><span class="lbl">Avoid when</span><div class="chips">{chips(d["avoid_when"])}</div></div>
      <div class="row"><span class="lbl">FI shop</span><div class="val">{_esc(d["availability"])}</div></div>
      <div class="row"><span class="lbl">Mode</span><div class="val">{_esc(d["mode"])}</div></div>
      {"".join(pair_rows) if pair_rows else '<div class="row"><span class="lbl">Pairings</span><div class="val" style="color:var(--ink-5)">none yet</div></div>'}
      {debug_block("Show data rows", d)}
    </div>
    """)
    if d["kind"] == "full":
        st.markdown(
            f'<div class="hint">{_esc(d["name"])} has a technique tree — see it in the '
            '<b>Ingredient Explorer</b> tab.</div>', unsafe_allow_html=True)


def tab_scout() -> None:
    st.markdown('<div class="section-title">Scout <span class="count">'
                'generated hypotheses from analogy rules</span></div>',
                unsafe_allow_html=True)
    _md("""
    <div class="disclaimer">
      <span class="eyebrow">Scout mode</span>
      Hypotheses are generated from reusable analogy rules applied to transformed
      states. They are <b>not classics</b> — they are role-compatible but uncommon
      ideas. Taste a small amount before serving. Each hypothesis shows its
      compatibility evidence, novelty status (if checked), and a test protocol.
    </div>
    """)

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
    comp = st.selectbox("Transformed state", state_comps,
                        index=state_comps.index(default),
                        key="tab_scout_component_select")

    hypotheses = query.generate_scout_hypotheses(CONN, comp)
    if not hypotheses:
        st.markdown(
            f'<div class="hint">No generated hypotheses for <b>{_esc(comp)}</b>.</div>',
            unsafe_allow_html=True)
        return

    candidates = [h for h in hypotheses if h["candidate_class"] != "rejected"]
    rejected = [h for h in hypotheses if h["candidate_class"] == "rejected"]

    st.markdown(
        f'<div class="eyebrow">{len(candidates)} candidate{"s" if len(candidates) != 1 else ""} · '
        f'{len(rejected)} rejected</div>', unsafe_allow_html=True)

    for h in candidates:
        _md(hypothesis_card_html(h))

    if rejected:
        with st.expander(f"Show {len(rejected)} rejected hypotheses", expanded=False):
            for h in rejected:
                _md(hypothesis_card_html(h))


def tab_taste_circle() -> None:
    """Taste Circle tab — interactive flavour wheel builder."""
    st.markdown('<div class="section-title">Taste Circle <span class="count">'
                'build a balanced dish by filling flavour dimensions</span></div>',
                unsafe_allow_html=True)
    st.markdown(
        '<div class="hint">Select a component, then choose items to fill each flavour '
        'dimension (salty, sour, sweet, etc.). Once a dimension is filled, it locks '
        'and you move to the next. Build a complete flavour profile!</div>',
        unsafe_allow_html=True)

    # Initialize session state for the taste circle
    if "taste_circle_locked" not in st.session_state:
        st.session_state.taste_circle_locked = set()
    if "taste_circle_selections" not in st.session_state:
        st.session_state.taste_circle_selections = {}

    # Component selector
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
    component = st.selectbox(
        "Select a component to build around:",
        state_comps,
        index=state_comps.index(default),
        key="taste_circle_component",
    )

    # Reset button
    if st.button("🔄 Reset Taste Circle"):
        st.session_state.taste_circle_locked = set()
        st.session_state.taste_circle_selections = {}
        st.rerun()

    # Get the component's state profile
    profile = query.component_state_profile(CONN, component)
    if profile is None:
        st.warning("This component has no state profile. Cannot build taste circle.")
        return

    # Display what the component already provides
    st.markdown("### Component provides:")
    provided_tags = profile.get("flavour_tags", [])
    if provided_tags:
        st.markdown(", ".join(f"`{tag}`" for tag in provided_tags))
    else:
        st.markdown("_No flavour tags provided_")

    # Get fillers grouped by dimension
    fillers_by_dim = query.taste_circle_fillers(
        CONN,
        component,
        locked_dimensions=st.session_state.taste_circle_locked,
    )

    # Display the taste circle
    st.markdown("### Taste Circle")

    # Define the flavour dimensions to show
    dimensions = [
        ("salty", "🧂 Salty"),
        ("sour", "🍋 Sour"),
        ("sweet", "🍯 Sweet"),
        ("bitter", "🌿 Bitter"),
        ("umami", "🍄 Umami"),
        ("pungent", "🌶️ Pungent"),
        ("aromatic", "🌸 Aromatic"),
        ("nutty_toasted", "🥜 Nutty/Toasted"),
        ("fresh_green", "🥬 Fresh/Green"),
        ("fermented_funky", "🧀 Fermented/Funky"),
        ("rich_fatty", "🧈 Rich/Fatty"),
    ]

    # Create a grid layout for the taste circle
    cols = st.columns(3)

    for i, (dim_key, dim_label) in enumerate(dimensions):
        col = cols[i % 3]

        with col:
            # Check if this dimension is provided or locked
            is_provided = dim_key in provided_tags
            is_locked = dim_key in st.session_state.taste_circle_locked

            if is_provided:
                st.markdown(f"**{dim_label}** ✅ _(provided)_")
            elif is_locked:
                selection = st.session_state.taste_circle_selections.get(dim_key)
                st.markdown(f"**{dim_label}** 🔒 `{selection}`")
            elif dim_key in fillers_by_dim:
                st.markdown(f"**{dim_label}**")
                fillers = fillers_by_dim[dim_key]
                filler_names = [f["filler"] for f in fillers]

                selected = st.selectbox(
                    f"Choose for {dim_label}",
                    ["(none)"] + filler_names,
                    key=f"taste_circle_{dim_key}",
                )

                if selected != "(none)":
                    if st.button(f"Lock {dim_label}", key=f"lock_{dim_key}"):
                        st.session_state.taste_circle_locked.add(dim_key)
                        st.session_state.taste_circle_selections[dim_key] = selected
                        st.rerun()
            else:
                st.markdown(f"**{dim_label}** ⚪ _(no fillers available)_")

    # Display the final dish
    st.markdown("### Your Dish")
    if st.session_state.taste_circle_selections:
        dish_components = [component]
        for dim, filler in st.session_state.taste_circle_selections.items():
            dish_components.append(filler)

        st.markdown("**Components:**")
        st.markdown(", ".join(f"`{c}`" for c in dish_components))

        # Generate a dish name
        dish_name = generate_dish_name(component, st.session_state.taste_circle_selections)
        st.markdown(f"**Dish name:** {dish_name}")
    else:
        st.info("Select items to fill the flavour dimensions and build your dish.")


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


def tab_taste_circle_map() -> None:
    """Taste Circle Map tab — click-driven circular flavour builder.

    The whole interaction happens on the circle itself (custom component):
    click a dimension to expand its fillers, click a filler to lock it in,
    click a locked dimension to change it, click blank canvas to close.
    """
    st.markdown('<div class="section-title">Taste Circle Map <span class="count">'
                'click the circle to build a balanced dish</span></div>',
                unsafe_allow_html=True)
    st.markdown(
        '<div class="hint">Browse components with ◀ ▶ · click a flavour dimension '
        'to see what can fill it · click an ingredient to lock it in · '
        'click a 🔒 dimension to change it · or press 🎲 for a random dish.</div>',
        unsafe_allow_html=True)

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
        # Swallow the last graph click so it isn't re-processed afterwards.
        st.session_state.tcm_last_click = st.session_state.get("tcm_graph")

    # Browse components with ◀ ▶ instead of a dropdown.
    if st.session_state.tcm_component not in state_comps:
        st.session_state.tcm_component = (
            "roasted_broccoli_component"
            if "roasted_broccoli_component" in state_comps
            else state_comps[0]
        )
    idx = state_comps.index(st.session_state.tcm_component)

    nav_prev, nav_name, nav_next = st.columns([1, 8, 1])
    with nav_prev:
        if st.button("◀", key="tcm_prev", help="Previous component"):
            idx = (idx - 1) % len(state_comps)
    # The name sits between the arrows but must show the post-click component,
    # so reserve the slot now and fill it once both buttons have been read.
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

    locked: set[str] = st.session_state.tcm_locked
    selections: dict[str, str] = st.session_state.tcm_selections

    # Pre-click state — also used to validate incoming clicks and random picks.
    profile = query.component_state_profile(CONN, component)
    provided = set(profile["flavour_tags"]) if profile else set()
    fillers_by_dim = query.taste_circle_fillers(CONN, component, locked)

    act_reset, act_random, _spacer = st.columns([1, 1.6, 6])
    with act_reset:
        if st.button("🔄 Reset", key="tcm_reset"):
            _reset()
    with act_random:
        if st.button("🎲 Surprise me", key="tcm_random",
                     help="Fill every open dimension with a random valid pick"):
            for dim, filler in random_dish_selections(fillers_by_dim, selections).items():
                locked.add(dim)
                selections[dim] = filler
            st.session_state.tcm_expanded = None

    # Handle a pending click from the graph BEFORE redrawing, so the new
    # state is reflected in this same rerun.
    click = st.session_state.get("tcm_graph")
    if click and click != st.session_state.tcm_last_click:
        st.session_state.tcm_last_click = click
        click_id = click.get("id")
        if click_id is None:
            # Blank canvas click closes the pop-up.
            st.session_state.tcm_expanded = None
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
        elif click_id.startswith("filler:"):
            _prefix, dim, filler = click_id.split(":", 2)
            valid = any(f["filler"] == filler for f in fillers_by_dim.get(dim, []))
            if valid and filler not in selections.values():
                locked.add(dim)
                selections[dim] = filler
                st.session_state.tcm_expanded = None

    # Recompute after click handling: the graph queries its own fresh data,
    # but the progress line below must reflect the post-click state too.
    fillers_by_dim = query.taste_circle_fillers(CONN, component, locked)

    # Draw the circle — it is both the state display and the click target.
    data = taste_circle_graph_data(
        CONN,
        component,
        locked_dimensions=locked,
        selections=selections,
        expanded_dimension=st.session_state.tcm_expanded,
    )
    taste_circle_map(nodes=data["nodes"], edges=data["edges"], height=640,
                     key="tcm_graph")

    # Progress + dish summary
    fillable = [
        dim for dim, _icon, _name, _color in TASTE_DIMENSIONS
        if dim not in provided and (fillers_by_dim.get(dim) or dim in locked)
    ]
    st.caption(f"{len(locked)} of {len(fillable)} open dimensions filled")

    st.markdown("### Your Dish")
    if selections:
        dish_components = [component, *selections.values()]
        st.markdown("**Components:**")
        st.markdown(", ".join(f"`{c}`" for c in dish_components))

        dish_name = generate_dish_name(component, selections)
        st.markdown(f"**Dish name:** {dish_name}")
    else:
        st.info("Click a dimension on the circle, then click an ingredient "
                "to start building your dish.")


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
}


def _persist_widget_state() -> None:
    """Keep widget values alive across tab switches.

    ``st.tabs`` rendered all ten tabs every run, so every widget stayed
    instantiated. The pill rail renders only the active tab, and Streamlit
    garbage-collects the state of any widget it did not draw — a selection
    would be lost the moment you looked at another tab. Re-assigning each key
    to itself marks it as set and survives the sweep. Button and component
    keys reject assignment; they are transient by nature, so skip them.
    """
    for key in list(st.session_state.keys()):
        try:
            st.session_state[key] = st.session_state[key]
        except Exception:
            pass


def tab_rail() -> str:
    """The ten tabs as a wrapping row of pills; returns the active label.

    A radio, not ``st.pills``: pills cannot be deselected back to a valid
    state, and AppTest cannot serialize a single-select pill group (it walks
    the value string character by character), which would cost us the smoke
    tests. CSS turns the radio into the handoff's pill row.
    """
    with st.container(key="tab_rail"):
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
