"""R4.1 integrated workspace: R4 with refined data readability. Research only,
desktop only. The R4 baseline stays runnable on port 8541.

    py -3.11 -m streamlit run docs/research/ux-integrated-r4-1/prototype/app.py --server.port 8542

Same URL keys as R4, plus the local key `graph=1` (show a collapsed graph).

The whole investigation context lives in the URL (see state.py), e.g.
?ingredient=broccoli&have=yogurt,lemon,garlic&rec=roasted_broccoli_component
&cmp=roasted_broccoli_component,steamed_broccoli_component&trace=ingredient:lemon&pane=trace
"""
from __future__ import annotations

import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
R4 = ROOT / "docs/research/ux-integrated-r4/prototype"   # r4_model: unchanged
sys.path[:0] = [str(HERE), str(R4), str(ROOT / "src")]

import streamlit as st  # noqa: E402

from foodprep import loader, query  # noqa: E402
import r4_model as M  # noqa: E402
import r41_state as S  # noqa: E402
import r41_views as V  # noqa: E402

st.set_page_config(page_title="R4.1 integrated workspace", layout="wide",
                   initial_sidebar_state="collapsed")
st.markdown("<style>[data-testid=stSidebar], [data-testid=stSidebarCollapsedControl] {display:none}"
            " .block-container {padding-top:3.2rem; padding-left:1.5rem; padding-right:1.5rem;"
            " padding-bottom:0.5rem}</style>",
            unsafe_allow_html=True)


@st.cache_resource
def conn() -> sqlite3.Connection:
    c = sqlite3.connect(":memory:", check_same_thread=False)
    c.row_factory = sqlite3.Row
    loader.build(c)
    return c


c = conn()
url = S.parse(st.query_params.to_dict())
ctx = dict(url)

# --- GLOBAL context: a filter bar across the top, written back to the URL --
ings = query.tree_ingredients(c)
all_ing = query.ingredients_list(c)
g1, g2, g3, g4, g5, g6 = st.columns([1.1, 2.2, 1.6, 1.6, 1.6, 1.2])
ctx["ingredient"] = g1.selectbox(
    "Ingredient", ings, index=ings.index(url["ingredient"]) if url["ingredient"] in ings else 0)
ctx["have"] = g2.multiselect("On hand · applies everywhere", all_ing, format_func=M.pretty,
                             default=[h for h in url["have"] if h in all_ing])
m = M.build(c, ctx["ingredient"], ctx["have"])
opts = S.filter_options(m)
ctx["has"] = g3.multiselect("Filter · has", opts["has"], format_func=S.HAS.get,
                            default=[x for x in url["has"] if x in opts["has"]])
ctx["paired"] = g4.multiselect("Filter · paired with", opts["paired"], format_func=M.pretty,
                               default=[x for x in url["paired"] if x in opts["paired"]])
ctx["gap"] = g5.multiselect("Filter · has a gap", opts["gap"], format_func=S.GAP.get,
                            default=[x for x in url["gap"] if x in opts["gap"]])
ctx["hide"] = g6.checkbox("Hide excluded rows", value=url["hide"])
ctx["answer"] = g6.checkbox("E3 summary (eval.)", value=url["answer"],
                            help="Off by default; shown only to evaluate whether it adds anything.")

ctx = S.reconcile(ctx, m)
if S.to_params(ctx) != S.to_params(url):
    st.query_params.from_dict(S.to_params(ctx))

st.html(V.CSS + '<div class="r4">' + V.context_bar(m, ctx) + "</div>")

if ctx["answer"] and ctx["rec"]:
    from foodprep.ui import answer as E3
    card = next(x for x in query.all_branch_cards(c, ctx["ingredient"])
                if x["component"] == ctx["rec"])
    routes = query.flavour_routes_for_component(c, ctx["rec"], ctx["have"])
    part = query.available_filter(c, card["transformation_id"], ctx["have"]) if ctx["have"] else None
    st.html(E3.answer_html(E3.explorer_answer(ctx["ingredient"], card, routes, part, ctx["have"])))

wide = ctx["cols"] == "matrix"
left, right = st.columns([7, 5] if wide else [1, 1], gap="medium")
full = st.query_params.get("full") == "1"   # captures only: no inner scrolling
H = "content" if full else 640
with left.container(height=H, border=False):
    st.html(V.CSS + '<div class="r4">' + V.overview_html(m, ctx) + "</div>")
with right:
    pane = S.pane(ctx)
    st.html(V.CSS + V.tabs_html(m, ctx, pane))
right = right.container(height="content" if full else H - 44, border=False)
with right:
    if pane == "compare":
        st.html(V.CSS + V.compare_html(m, ctx))
    elif pane == "trace":
        # The relationship table is the reading surface. A small graph (at most
        # V.GRAPH_LIMIT relationships) sits above it; a larger one is collapsed
        # and, when revealed, drawn under the table.
        place = V.graph_placement(m, ctx)
        st.html(V.CSS + V.trace_head_html(m, ctx) + V.graph_note_html(m, ctx))
        if place == "shown":
            st.graphviz_chart(V.trace_dot(m, ctx), use_container_width=False)
        st.html(V.CSS + V.trace_table_html(m, ctx))
        if place == "below":
            st.graphviz_chart(V.trace_dot(m, ctx), use_container_width=False)
    else:
        if ctx["rec"]:
            st.html(V.CSS + V.detail_html(m, ctx, ctx["rec"]))
        else:
            st.html(V.CSS + '<div class="r4 muted">Click a prepared ingredient in the overview '
                    "to open its fact sheet. “add to compare” puts rows side by side; "
                    "“trace” follows their relationships.</div>")
