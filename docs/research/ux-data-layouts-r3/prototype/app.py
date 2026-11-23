"""R3 data-layout prototype. Research only, desktop only, not part of the app.

    py -3.11 -m streamlit run docs/research/ux-data-layouts-r3/prototype/app.py --server.port 8540

URL params (for captures): ?ingredient=broccoli&have=yogurt,lemon,garlic
&layout=table|explorer|workspace|cards&focus=<component or filler>&level=0..3
&role=..&filler=..&has=..&compare=a,b
"""
from __future__ import annotations

import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path[:0] = [str(HERE), str(ROOT / "src")]

import streamlit as st  # noqa: E402

from foodprep import loader, query  # noqa: E402
from foodprep.ui import render  # noqa: E402
import layouts as L  # noqa: E402
from model import build_model, pretty  # noqa: E402

st.set_page_config(page_title="R3 data layouts", layout="wide")


@st.cache_resource
def conn() -> sqlite3.Connection:
    c = sqlite3.connect(":memory:", check_same_thread=False)
    c.row_factory = sqlite3.Row
    loader.build(c)
    return c


def qp(name, default=""):
    v = st.query_params.get(name, default)
    return v


def qlist(name):
    v = qp(name, "")
    return [x for x in v.split(",") if x]


c = conn()
LAYOUTS = {"table": "L1 Associative table", "explorer": "L2 Relationship explorer",
           "workspace": "L3 Overview / detail", "cards": "Reference: current cards"}

with st.sidebar:
    st.markdown("**R3 prototype** · same data in every layout")
    ings = query.tree_ingredients(c)
    ing = st.selectbox("Ingredient", ings,
                       index=ings.index(qp("ingredient", "broccoli"))
                       if qp("ingredient", "broccoli") in ings else 0)
    have = st.multiselect("On hand", query.ingredients_list(c),
                          default=[h for h in qlist("have") if h in query.ingredients_list(c)],
                          format_func=pretty)
    keys = list(LAYOUTS)
    lay = st.radio("Layout", keys, format_func=LAYOUTS.get,
                   index=keys.index(qp("layout", "table")) if qp("layout", "table") in keys else 0)

m = build_model(c, ing, have)
comps = [s["component"] for s in m["states"]]
st.markdown(f"### {pretty(ing)} · {len(comps)} prepared ingredients"
            + (f" · on hand: {', '.join(pretty(h) for h in have)}" if have else ""))

if lay == "table":
    opts = L.filter_options(m)
    c1, c2, c3 = st.columns(3)
    sel = {
        "role": c1.multiselect("Needs role", opts["role"],
                               default=[x for x in qlist("role") if x in opts["role"]]),
        "filler": c2.multiselect("Paired with", opts["filler"], format_func=pretty,
                                 default=[x for x in qlist("filler") if x in opts["filler"]]),
        "has": c3.multiselect("Has", opts["has"],
                              default=[x for x in qlist("has") if x in opts["has"]]),
    }
    st.html(L.associative_html(m, sel, focus=qp("focus") or None))
    with st.expander("Every relation as rows (sortable)", expanded=qp("rows") == "1"):
        st.dataframe(L.relations_rows(m), hide_index=True, use_container_width=True)

elif lay == "explorer":
    kinds = L.node_kinds(m)
    nodes = comps + sorted(n for n, k in kinds.items() if k == "filler")
    f0 = qp("focus") if qp("focus") in nodes else (comps[1] if len(comps) > 1 else comps[0])
    a, b = st.columns([2, 3])
    focus = a.selectbox("Focus", nodes, index=nodes.index(f0),
                        format_func=lambda n: ("● " if n in comps else "  ") + pretty(n))
    level = b.select_slider("Show", options=list(range(len(L.LEVELS))),
                            value=int(qp("level", "1") or 1),
                            format_func=lambda i: L.LEVELS[i])
    g, t = st.columns([3, 2])
    with g:
        st.graphviz_chart(L.explorer_dot(m, focus, level), use_container_width=True)
        st.html(L.CSS + '<div class="r3">' + L.legend()
                + '<div class="muted">Line: solid = curated · thick green = on hand · '
                  'dashed = idea · thick amber = tasted · dotted = source.</div></div>')
    with t:
        st.html(L.neighbour_table_html(m, focus))

elif lay == "workspace":
    left, right = st.columns([2, 3])
    with left:
        f0 = qp("focus") if qp("focus") in comps else (comps[1] if len(comps) > 1 else comps[0])
        rows = L.overview_rows(m)
        ev = st.dataframe(rows, hide_index=True, use_container_width=True,
                          on_select="rerun", selection_mode="single-row",
                          key="overview")
        picked = ev.selection.rows if ev and ev.selection else []
        focus = comps[picked[0]] if picked else f0
        st.caption("Needs: ● on hand · ◐ pairing recorded · ○ nothing recorded. "
                   "Click a row to open its fact sheet.")
        cmp = st.multiselect("Compare side by side (up to 3)", comps, format_func=pretty,
                             default=[x for x in qlist("compare") if x in comps][:3],
                             max_selections=3)
    with right:
        if cmp:
            st.html(L.compare_html(m, cmp))
        else:
            st.html(L.fact_sheet_html(m, focus))

else:  # reference: the current card layout, same data
    css = (ROOT / "src/foodprep/ui/design.css").read_text(encoding="utf-8")
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    for card in query.all_branch_cards(c, ing):
        part = query.available_filter(c, card["transformation_id"], have) if have else None
        routes = query.flavour_routes_for_component(c, card["component"], have) if have else None
        st.markdown(render.branch_card_html(card, available=part, routes=routes),
                    unsafe_allow_html=True)
