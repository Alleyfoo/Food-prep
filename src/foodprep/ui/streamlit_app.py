"""Food-prep — ingredient transformation graph UI (Streamlit).

Seven tabs:
  Tab 1 Ingredient Explorer  — branch_card / all_branch_cards
  Tab 2 Map                  — interactive ingredient mindmap (pyvis)
  Tab 3 Journeys             — ingredient_journeys
  Tab 4 Component Explorer   — component_card + flavour_routes
  Tab 5 Plate Balance        — plate_balance_detail
  Tab 6 Filler Profiles      — filler_profile_detail
  Tab 7 Scout                — generate_scout_hypotheses + trials

Run:  streamlit run app.py
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

from foodprep.loader import build
from foodprep import export, query
from foodprep.ui.render import (
    _esc, chip, chips, conf_pill, debug_block, tag_class,
    available_partition_html, branch_card_html,
    hypothesis_card_html, journey_card_html, route_card_html,
)
from foodprep.ui.graph import build_ingredient_graph, build_scout_graph, graph_to_html

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
          <div class="brand-sub">a local cooking map for turning ingredients into useful components, seeing what taste roles are missing, and finding the next sensible move</div>
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
    st.markdown('<div class="avail-strip"><span class="avail-label">'
                'What do I have right now?</span>'
                '<span class="avail-hint">filters Ingredient / Component / Plate '
                'suggestions into Available now · Missing but useful · No match</span>'
                '</div>', unsafe_allow_html=True)
    return st.multiselect("Available ingredients", ings,
                          placeholder="e.g. lemon, yogurt, pickles, bread, eggs, beans",
                          help="Pick what's in your kitchen. Empty = show all curated fillers.")


def tab_ingredient_explorer(available_items: list[str] | None = None) -> None:
    st.markdown('<div class="section-title">Ingredient Explorer</div>',
                unsafe_allow_html=True)
    trees = query.tree_ingredients(CONN)
    col1, col2 = st.columns([1, 1])
    with col1:
        ingredient = st.selectbox("Ingredient", trees,
                                  index=trees.index("cabbage") if "cabbage" in trees else 0)
    with col2:
        mode = st.radio("Mode", ["Best branches", "Choose technique"], horizontal=True)

    avail = available_items or None
    techs = query.techniques_for_ingredient(CONN, ingredient)
    if mode == "Choose technique":
        tech = st.selectbox("Technique", techs)
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
    comp = st.selectbox("Component", comps, index=comps.index(default))
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
    picked = st.multiselect("Plate items", profiles,
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
    name = st.selectbox("Filler", ings, index=ings.index(default))
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
                        index=state_comps.index(default))

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
    topbar()
    available_items = available_selector()
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
        "Ingredient Explorer", "Map", "Scout Map", "Journeys", "Component Explorer",
        "Plate Balance", "Filler Profiles", "Scout",
    ])
    with tab1:
        tab_ingredient_explorer(available_items)
    with tab2:
        tab_map()
    with tab3:
        tab_scout_map()
    with tab4:
        tab_journeys()
    with tab5:
        tab_component_explorer(available_items)
    with tab6:
        tab_plate_balance(available_items)
    with tab7:
        tab_filler_profiles()
    with tab8:
        tab_scout()


if __name__ == "__main__":
    main()
