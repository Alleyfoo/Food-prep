"""Food-prep — ingredient transformation graph UI (Streamlit).

Round 7: handles on the engine, no new ontology. Five tabs map 1:1 to the
existing query API:
  Tab 1 Ingredient Explorer  — branch_card / all_branch_cards
  Tab 2 Component Explorer  — component_card
  Tab 3 Plate Balance        — plate_balance_detail
  Tab 4 Filler Profiles      — filler_profile_detail
  Tab 5 Scout                — scout_rows

Run:  streamlit run app.py
       streamlit run src/foodprep/ui/streamlit_app.py
"""

from __future__ import annotations

import html
import json
from pathlib import Path

import streamlit as st

from foodprep.db import connect
from foodprep.loader import build
from foodprep import export, query

# ---------------------------------------------------------------------------
# page config + design system
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="food-prep",
    page_icon="🍅",
    layout="wide",
    initial_sidebar_state="collapsed",
)

_CSS_PATH = Path(__file__).with_name("design.css")
if _CSS_PATH.exists():
    st.markdown(f"<style>{_CSS_PATH.read_text(encoding='utf-8')}</style>",
                unsafe_allow_html=True)


def _md(markup: str) -> None:
    """Render HTML markup with leading per-line whitespace stripped (so the
    indented source stays readable without becoming a code block)."""
    cleaned = "\n".join(line.lstrip() for line in markup.splitlines())
    st.markdown(cleaned.strip(), unsafe_allow_html=True)


def _esc(s) -> str:
    return html.escape(str(s) if s is not None else "")


# ---------------------------------------------------------------------------
# connection (built once from YAML, cached for the session)
# ---------------------------------------------------------------------------

@st.cache_resource
def get_conn():
    conn = connect(":memory:")
    build(conn)
    return conn


CONN = get_conn()


# ---------------------------------------------------------------------------
# small render primitives
# ---------------------------------------------------------------------------

def chip(value, cls: str = "") -> str:
    return f'<span class="chip {cls}">{_esc(value)}</span>'


def chips(values, cls: str = "") -> str:
    if not values:
        return f'<span class="chip" style="color:var(--ink-5)">—</span>'
    return " ".join(chip(v, cls) for v in values)


def conf_pill(conf: str) -> str:
    return f'<span class="card-conf {conf}">{_esc(conf)}</span>'


def debug_block(title: str, payload) -> str:
    body = json.dumps(payload, indent=2, default=str, ensure_ascii=False)
    return (f'<details class="debug"><summary>{_esc(title)}</summary>'
            f'<pre>{_esc(body)}</pre></details>')


def tag_class(family: str) -> str:
    return {"flavour": "flavour", "texture": "texture", "state": "state"}.get(family, "")


def export_buttons(md: str, filename: str) -> None:
    """Copy-Markdown (a code block with Streamlit's copy icon) + Download .md.
    Renders from the same computed dict the card above renders from — no
    recompute, no new query. No-op when md is empty."""
    if not md:
        return
    st.download_button("Download .md", md, file_name=filename,
                       mime="text/markdown", key=f"dl_{filename}")
    with st.expander("Markdown", expanded=False):
        st.code(md, language="markdown")


# ---------------------------------------------------------------------------
# branch card (Tabs 1 + 2 share it)
# ---------------------------------------------------------------------------

def available_partition_html(part: dict) -> str:
    """Round 11 — render the 'what do I have' partition (Available now /
    Missing but useful / No match) as card rows. Returns '' if empty."""
    rows = []
    if part.get("available_now"):
        groups = []
        for g in part["available_now"]:
            roles = " ".join(chip(r, "missing") for r in g["roles"])
            groups.append(
                f'<div class="chip-group"><span class="gl have">{_esc(g["filler"])}</span>{roles}</div>'
            )
        rows.append(f'<div class="row"><span class="lbl">Available now</span>'
                    f'<div>{"".join(groups)}</div></div>')
    if part.get("missing_but_useful"):
        groups = []
        for m in part["missing_but_useful"]:
            if m["fillers"]:
                fch = " ".join(chip(f, "filler") for f in m["fillers"])
            else:
                fch = '<span class="none">(no curated filler)</span>'
            groups.append(
                f'<div class="chip-group"><span class="gl">{_esc(m["role"])}</span>{fch}</div>'
            )
        rows.append(f'<div class="row"><span class="lbl">Missing but useful</span>'
                    f'<div>{"".join(groups)}</div></div>')
    no_match = list(part.get("unknown_items") or []) + list(part.get("no_match_known") or [])
    if no_match:
        rows.append(f'<div class="row"><span class="lbl">No match here</span>'
                    f'<div class="chips">{"".join(chip(n, "muted") for n in no_match)}</div></div>')
    return "".join(rows)


def branch_card_html(d: dict, with_debug: bool = True,
                     available: dict | None = None) -> str:
    conf = d.get("confidence") or ""
    card_cls = "scout" if conf == "experimental" else "cook"
    tags = d.get("tags") or []
    tag_chips = " ".join(
        chip(t["value"], tag_class(t.get("family", ""))) for t in tags
    ) or '<span class="chip" style="color:var(--ink-5)">—</span>'
    risks = d.get("risks") or []
    risk_chips = " ".join(chip(r, "risk") for r in risks)
    missing = [m["role_name"] for m in (d.get("missing") or [])]
    miss_chips = " ".join(chip(r, "missing") for r in missing)
    # "Try:" groups fillers by the role they fill
    try_groups = []
    for role, fillers in (d.get("fillers_by_role") or {}).items():
        names = [f["filler"] for f in fillers[:3]] or ["(no curated filler)"]
        try_groups.append(
            f'<div class="chip-group"><span class="gl">{_esc(role)}</span>'
            + " ".join(chip(n, "filler") for n in names) + "</div>"
        )
    try_html = "".join(try_groups) or '<span class="chip" style="color:var(--ink-5)">—</span>'
    # Round 11: when a 'what do I have' partition is supplied, replace the
    # plain Try row with Available now / Missing but useful / No match.
    partition_html = available_partition_html(available) if available else ""
    uses = d.get("uses") or []

    shift = ""
    if d.get("flavour_shift") or d.get("texture_shift"):
        shift = f'<div class="card-shift">{_esc(d.get("flavour_shift") or "—")} · {_esc(d.get("texture_shift") or "—")}</div>'

    parts = [f'<div class="card {card_cls}">']
    parts.append(
        f'<div class="card-head"><span class="card-tech">{_esc(d["technique"])}</span>'
        f'<span class="card-comp">{_esc(d.get("component") or "")}</span>'
        f'{conf_pill(conf)}</div>'
    )
    parts.append(shift)
    parts.append(f'<div class="row"><span class="lbl">Tags</span><div class="chips">{tag_chips}</div></div>')
    if risks:
        parts.append(f'<div class="row"><span class="lbl">Risks</span><div class="chips">{risk_chips}</div></div>')
    if missing:
        parts.append(f'<div class="row"><span class="lbl">Missing</span><div class="chips">{miss_chips}</div></div>')
    if partition_html:
        parts.append(partition_html)
    else:
        parts.append(f'<div class="row"><span class="lbl">Try</span><div>{try_html}</div></div>')
    if uses:
        parts.append(f'<div class="row"><span class="lbl">Use in</span><div class="chips">{chips(uses)}</div></div>')
    if with_debug:
        parts.append(debug_block("Show data rows", d))
    parts.append("</div>")
    return "".join(parts)


# ---------------------------------------------------------------------------
# top bar
# ---------------------------------------------------------------------------

def topbar() -> None:
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
      <div class="topbar-pill">{len(query.tree_ingredients(CONN))} full ingredients</div>
      <div class="topbar-pill">{len(query.components_list(CONN))} components</div>
      <div class="topbar-pill">{len(query.profiles_list(CONN))} plate profiles</div>
    </div>
    """)


# ---------------------------------------------------------------------------
# Tab 1 — Ingredient Explorer
# ---------------------------------------------------------------------------

def tab_ingredient_explorer(available_items: list[str] | None = None) -> None:
    st.markdown('<div class="section-title">Ingredient Explorer</div>',
                unsafe_allow_html=True)
    trees = query.tree_ingredients(CONN)
    col1, col2 = st.columns([1, 1])
    with col1:
        ingredient = st.selectbox("Ingredient", trees, index=trees.index("cabbage") if "cabbage" in trees else 0)
    with col2:
        mode = st.radio("Mode", ["Best branches", "Choose technique"], horizontal=True)

    avail = available_items or None  # [] -> current Try view (no partition)
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


# ---------------------------------------------------------------------------
# Tab 2 — Component Explorer
# ---------------------------------------------------------------------------

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
    # Round 11: the component's next-moves come from its first producing
    # transformation; partition those against what the user has on hand.
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
    st.markdown(
        '<div class="hint">A component is an <b>after-state</b>. You do not always '
        'start from raw cabbage/tomato/potato — pick the component you already have.</div>',
        unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Tab 3 — Plate Balance
# ---------------------------------------------------------------------------

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
    avail = available_items or None  # [] -> current behaviour (no partition)
    r = query.plate_balance_detail(CONN, text, available_items=avail)
    has_part = "available_now" in r  # partition computed only when avail passed

    # ---- summary KPIs ----
    gap_n = len(r["target_gap"])
    more_n = len(r["flagged_more"])
    unk_n = len(r["unknown"])
    h_cls = "k-warn" if r["leans_heavy"] else "k-ok"
    d_cls = "k-warn" if r["leans_dry"] else "k-ok"
    _md(f"""
    <div class="kpis">
      <div class="kpi"><div class="lbl">Items</div><div class="val">{len(r['items'])}</div><div class="foot">on the plate</div></div>
      <div class="kpi k-risk"><div class="lbl">Hard gaps</div><div class="val">{gap_n}</div><div class="foot">target roles missing</div></div>
      <div class="kpi k-warn"><div class="lbl">May want more</div><div class="val">{more_n}</div><div class="foot">soft flags</div></div>
      <div class="kpi {h_cls}"><div class="lbl">Heaviness</div><div class="val">{r['plate_heaviness'] if r['plate_heaviness'] is not None else '—'}</div><div class="foot">{r['heaviness_label'] or 'unknown'}</div></div>
    </div>
    """)

    # ---- already provides ----
    _md(f'<div class="balance-section have"><h4>Already provides</h4><div class="chips">{chips(r["provided"])}</div></div>')

    # ---- gaps + suggested fillers (or the 'what do I have' partition) ----
    if has_part:
        # Round 11: partition on-hand fillers into Available now / Missing but
        # useful / No match, instead of the plain per-role suggested lists.
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
        # current behaviour: plain per-role suggested fillers
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

        # ---- may want more ----
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

    # ---- risks / avoid ----
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

    # ---- unknown / no-profile ----
    if r["no_profile"]:
        items = [it["name"] for it in r["no_profile"]]
        _md(f'<div class="balance-section muted"><h4>No balance profile for</h4><div class="chips">{chips(items)}</div>'
            '<div class="filler-line none">add component_profiles entries for heaviness/dryness/missing-risk data.</div></div>')

    export_buttons(export.render_plate_markdown(r), "plate.md")

    with st.expander("Debug — raw plate_balance_detail", expanded=False):
        st.json(r)


# ---------------------------------------------------------------------------
# Tab 4 — Filler Profiles
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# Tab 5 — Scout
# ---------------------------------------------------------------------------

def tab_scout() -> None:
    st.markdown('<div class="section-title">Scout <span class="count">experimental pairings — NOT classic</span></div>',
                unsafe_allow_html=True)
    trees = query.tree_ingredients(CONN)
    opts = ["all ingredients"] + trees
    sel = st.selectbox("Filter by ingredient", opts, index=0)
    ingredient = None if sel == "all ingredients" else sel
    rows = query.scout_rows(CONN, ingredient=ingredient)
    _md("""
    <div class="disclaimer">
      <span class="eyebrow">Scout mode</span>
      Scout shows role-compatible but uncommon ideas. They are <b>not classics</b>.
      Taste a small amount before serving — a tiny spoon first, before any culinary
      heroism. These are speculative, labelled so no one pretends they are tradition.
    </div>
    """)
    if not rows:
        st.markdown('<div class="hint">No experimental pairings curated yet for this filter.</div>',
                    unsafe_allow_html=True)
        return
    for r in rows:
        subj = r["technique"] or r["target"] or "(general)"
        note = r["notes"] or f"{r['filler']} ({r['role']})"
        _md(f"""
        <div class="card scout">
          <div class="card-head"><span class="card-tech">{_esc(r["filler"])}</span>
            <span class="card-comp">+ {_esc(subj)}</span>
            {conf_pill("experimental")}</div>
          <div class="card-shift">{_esc(note)}</div>
          <div class="row"><span class="lbl">Role</span><div class="val">{chip(r["role"], "role")}</div></div>
          <div class="row"><span class="lbl">FI shop</span><div class="val">{_esc(r.get("availability") or "—")}</div></div>
          {debug_block("Show data rows", dict(r))}
        </div>
        """)


# ---------------------------------------------------------------------------
# 'What do I have right now?' — shared selector (Round 11)
# ---------------------------------------------------------------------------

def available_selector() -> list[str]:
    """A single 'available ingredients' multiselect above the tabs. Empty
    selection = current behaviour; non-empty filters Tab 1/2/3 suggestions into
    Available now / Missing but useful / No match. Not a pantry system, not
    inventory, not shopping — just 'what's in the kitchen right now?'."""
    ings = query.ingredients_list(CONN)
    st.markdown('<div class="avail-strip"><span class="avail-label">'
                'What do I have right now?</span>'
                '<span class="avail-hint">filters Ingredient / Component / Plate '
                'suggestions into Available now · Missing but useful · No match</span>'
                '</div>', unsafe_allow_html=True)
    return st.multiselect("Available ingredients", ings, placeholder="e.g. lemon, yogurt, pickles, bread, eggs, beans",
                          help="Pick what's in your kitchen. Empty = show all curated fillers (current behaviour).")


# ---------------------------------------------------------------------------
# layout
# ---------------------------------------------------------------------------

topbar()
available_items = available_selector()
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Ingredient Explorer", "Component Explorer", "Plate Balance",
    "Filler Profiles", "Scout",
])
with tab1:
    tab_ingredient_explorer(available_items)
with tab2:
    tab_component_explorer(available_items)
with tab3:
    tab_plate_balance(available_items)
with tab4:
    tab_filler_profiles()
with tab5:
    tab_scout()