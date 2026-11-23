"""The product's Taste Circle builder, embedded as a fourth workspace pane.

The circle itself is the product's own component and graph data, unchanged
(src/foodprep/ui/taste_circle.py, graph.taste_circle_graph_data). What is
new here is only the glue:

- it builds around the record in detail (rec), so it shares the workspace's
  subject instead of keeping its own;
- the dish lives in the URL (tc / tcx / tcp / tcb, see r42_state), so Back,
  sharing and captures work as everywhere else in the workspace;
- the read-out beside the circle states in words what the circle shows in
  colour and size: provided, open with N options, no options yet, locked.

Click routing mirrors the product's tab_taste_circle_map, as a pure function
from (state, clicked node id) to URL changes.
"""
from __future__ import annotations

import random
import sqlite3
from typing import Any, Mapping

from foodprep import query
from foodprep.ui.graph import TASTE_DIMENSIONS, random_dish_selections

import r42_palette as P
import r42_state as S
from r4_model import pretty
from r42_views import a, esc

MORE = "__more"                     # graph.py's paging node: filler:<dim>:__more
NAMES = {k: n for k, _i, n, _h in TASTE_DIMENSIONS}
ORDER = [k for k, *_ in TASTE_DIMENSIONS]


def selections(st: Mapping[str, Any]) -> dict[str, str]:
    """The locked dish, {dimension: filler}, in the order it was chosen."""
    out: dict[str, str] = {}
    for item in st.get("tc", []):
        dim, _, filler = item.partition(":")
        if dim in NAMES and filler and dim not in out and filler not in out.values():
            out[dim] = filler
    return out


def encode(sel: Mapping[str, str]) -> list[str]:
    return [f"{d}:{f}" for d, f in sel.items()]


def can_anchor(c: sqlite3.Connection, comp: str) -> bool:
    """The circle needs a sensory profile: it is what says which dimensions
    the prepared ingredient already provides."""
    return bool(comp) and query.component_state_profile(c, comp) is not None


def provided(c: sqlite3.Connection, comp: str) -> list[str]:
    tags = set((query.component_state_profile(c, comp) or {}).get("flavour_tags") or [])
    return [d for d in ORDER if d in tags]


def _recolour_peach(value: Any, bg: str, *, text: bool = False) -> Any:
    """Peach world (the reference): the product's colours with its greys
    lifted into seed tones, as before the redesign."""
    w = P.world("peach")
    if isinstance(value, dict):
        return {k: _recolour_peach(v, bg, text=text or k == "font") for k, v in value.items()}
    if isinstance(value, list):
        return [_recolour_peach(v, bg, text=text) for v in value]
    if not (isinstance(value, str) and len(value) == 7 and value.startswith("#")):
        return value
    if text and P.contrast(value, bg) < 4.5:
        return w["secondary"]
    hue, sat, light = P.hex_to_hsl(value)
    if sat >= P.NEUTRAL_MIN_SAT:
        return value
    if light > 97:
        return w["surface"]
    if abs(hue - w["hue"]) > 30 and sat >= 15:
        return P.hsl(hue, P.NEUTRAL_MIN_SAT + 10, light)
    tones = [w["ink"]] + [w["N"][k] for k, *_ in w["steps"]]
    return min(tones, key=lambda t: abs(P.hex_to_hsl(t)[2] - light))


def _paint(bg: str, border: str, hover: str) -> dict[str, Any]:
    return {"background": bg, "border": border, "hover": {"background": bg, "border": hover},
            "highlight": {"background": bg, "border": hover}}


def node_state(st: Mapping[str, Any], dim: str, prov: set[str]) -> str:
    """provided / locked / expanded / open: the circle's states as roles."""
    if dim in prov:
        return "provided"
    if dim in selections(st):
        return "locked"
    if dim == st["tcx"]:
        return "expanded"
    return "open"


def style_by_role(data: dict, st: Mapping[str, Any], prov: set[str]) -> dict:
    """Colour every node and edge by its job, from the world's tokens:
    each state takes the world's circle role (white/cool: open = white
    with an outline, provided = neutral fill, locked = the selection blue,
    expanded = solid blue; pantry: open = mustard seed, provided = pale
    sage, locked = red cabbage), and an option you have on hand takes
    the on-hand colour. When one dimension is fanned out, the others step
    back to lighter versions of the same roles."""
    T = P.tokens(st["pal"])
    have = set(st["have"])
    fanned = bool(st["tcx"])
    out_nodes, state_of = [], {}
    for n in data["nodes"]:
        n = dict(n)
        kind = n["id"].split(":", 1)[0]
        if kind == "comp":
            n["color"], n["font"] = _paint(T["circle-canvas"], T["ink"], T["ink"]), {**n.get("font", {}), "color": T["ink"]}
        elif kind == "dim":
            dim = n["id"][4:]
            role = node_state(st, dim, prov)
            back = fanned and role != "expanded"
            state_of[n["id"]] = role
            c = lambda k: T[f"circle-{k}"]  # noqa: E731
            bg, line, label, width = {
                "open": (c("open-fill"), T["line"] if back else c("open-edge"),
                         T["ink-3"] if back else c("open-label"), 1),
                "provided": (c("prov-fill"), c("prov-fill") if back else c("prov-edge"), c("prov-label"), 1),
                "locked": (c("lock-fill"), c("lock-calm") if back else c("lock-edge"), c("lock-label"), 2),
                "expanded": (c("exp-fill"), c("exp-edge"), c("exp-label"), 3),
            }[role]
            n["color"] = _paint(bg, line, T["ink"])
            n["borderWidth"] = width
            n["font"] = {**n.get("font", {}), "color": label}
        elif kind == "filler":
            _p, _dim, filler = n["id"].split(":", 2)
            if filler == MORE:
                n["color"] = _paint(T["fill"], T["line"], T["ink"])
            elif filler in have:
                n["color"] = _paint(T["have-subtle"], T["have-base"], T["ink"])
            else:
                n["color"] = _paint(T["surface"], T["line-strong"], T["ink"])
            n["font"] = {**n.get("font", {}), "color": T["ink"]}
        out_nodes.append(n)
    out_edges = []
    for e in data["edges"]:
        e = dict(e)
        role = state_of.get(e.get("to", ""))
        if role is None:                              # dimension -> option (the fan)
            col, w = T["line-strong"], 1
        else:
            col, w = {"open": (T["line"], 1), "provided": (T["circle-prov-edge"], 1.5),
                      "locked": (T["circle-lock-edge"], 2), "expanded": (T["circle-exp-fill"], 2)}[role]
        e["color"], e["width"] = {"color": col}, w
        out_edges.append(e)
    return {"nodes": out_nodes, "edges": out_edges}


def graph_data(c: sqlite3.Connection, st: Mapping[str, Any]) -> dict[str, list]:
    """The product's graph data for this dish, coloured for the colour world.
    The product's function and data are unchanged; this colours a copy."""
    from foodprep.ui.graph import taste_circle_graph_data
    sel = selections(st)
    data = taste_circle_graph_data(c, st["rec"], locked_dimensions=set(sel), selections=sel,
                                   expanded_dimension=st["tcx"] or None,
                                   available=set(st["have"]), page=st["tcp"])
    if st.get("pal", P.DEFAULT_WORLD) == "peach":
        bg = P.tokens("peach")["page"]
        return {"nodes": _recolour_peach(data["nodes"], bg), "edges": _recolour_peach(data["edges"], bg)}
    return style_by_role(data, st, set(provided(c, st["rec"])))


def apply_click(c: sqlite3.Connection, st: Mapping[str, Any], node: str | None) -> dict[str, Any]:
    """URL changes for one click on the circle (same rules as the product):
    blank canvas closes the fan; an open dimension fans out its fillers, a
    second click closes it; a locked dimension unlocks; a filler locks in;
    the "more" node pages the fan."""
    sel = selections(st)
    fillers = query.taste_circle_fillers(c, st["rec"], set(sel))
    tcx, tcp = st["tcx"], st["tcp"]
    if node is None:
        tcx = ""
    elif node.startswith("dim:"):
        dim = node[4:]
        if dim in sel:
            sel.pop(dim)
            tcx = ""
        elif dim == tcx:
            tcx = ""
        elif fillers.get(dim):
            tcx, tcp = dim, 0
    elif node.startswith("filler:"):
        _p, dim, filler = node.split(":", 2)
        if filler == MORE:
            tcp += 1
        elif (any(f["filler"] == filler for f in fillers.get(dim, []))
              and filler not in sel.values()):
            sel[dim] = filler
            tcx, tcp = "", 0
    return {"tc": encode(sel), "tcx": tcx, "tcp": tcp, "tcb": st["rec"],
            "pane": "circle"}


def dish_name(comp: str, sel: Mapping[str, str]) -> str:
    """The product's heuristic (streamlit_app.generate_dish_name), copied so
    the prototype does not import the whole product app."""
    base = comp.replace("_component", "").replace("_", " ")
    keys = [sel[d].replace("_", " ") for d in ("umami", "sour", "aromatic", "pungent") if d in sel][:2]
    return f"{base} with {' and '.join(keys)}" if keys else f"Seasoned {base}"


def _href(st: Mapping[str, Any], **changes: Any) -> str:
    return S.href(st, pane="circle", tcb=st["rec"], **changes)


def readout_html(c: sqlite3.Connection, st: Mapping[str, Any],
                 rng: random.Random | None = None) -> str:
    """Head (above the circle): the subject, how to use it, and every
    dimension's state in words, so nothing depends on reading colour."""
    comp = st["rec"]
    sel = selections(st)
    have = set(st["have"])
    prov = provided(c, comp)
    fillers = query.taste_circle_fillers(c, comp, set(sel))
    open_ = [d for d in ORDER if d not in prov and d not in sel and fillers.get(d)]
    none_ = [d for d in ORDER if d not in prov and d not in sel and not fillers.get(d)]

    def opt(d: str) -> str:
        n = len([f for f in fillers[d] if f["filler"] not in sel.values()])
        on = [f["filler"] for f in fillers[d] if f["filler"] in have and f["filler"] not in sel.values()]
        txt = f"{esc(NAMES[d])} ({n})"
        return txt + (f' <span class="have">on hand: {esc(", ".join(pretty(x) for x in on))}</span>'
                      if on else "")

    rows = [("Provided by the state", ", ".join(esc(NAMES[d]) for d in prov) or "none"),
            ("Locked in your dish", ", ".join(f"{esc(NAMES[d])}: {esc(pretty(f))}"
                                             for d, f in sel.items()) or "nothing yet"),
            ("Open, options in brackets", "; ".join(opt(d) for d in open_) or "none"),
            ("No options recorded", ", ".join(esc(NAMES[d]) for d in none_) or "none")]
    fan = ""
    if st["tcx"] and fillers.get(st["tcx"]):
        opts = [f["filler"] for f in fillers[st["tcx"]] if f["filler"] not in sel.values()]
        on = [pretty(x) for x in opts if x in have]
        fan = (f'<div class="tc-fan"><b>{esc(NAMES[st["tcx"]])}</b> is open on the circle: '
               f'{len(opts)} options, {"on hand: " + esc(", ".join(on)) if on else "none on hand"}. '
               f'Click one to lock it in.</div>')
    surprise = random_dish_selections(fillers, sel, rng=rng)
    acts = [a(_href(st, tc=encode({**sel, **surprise}), tcx="", tcp=0),
              "fill the open dimensions at random")] if surprise else []
    if sel or st["tcx"]:
        acts.append(a(_href(st, tc=[], tcx="", tcp=0), "start the circle again"))
    return ('<div class="r4 tc">'
            f'<h3>Taste circle around {esc(pretty(comp))}</h3>'
            '<div class="muted">Click a dimension to see what can fill it, click an ingredient '
            'to lock it in, click a locked dimension to change it. The product’s builder, '
            'unchanged; the dish is kept in the address.</div>'
            '<dl class="tc-dl">' + "".join(f"<dt>{k}</dt><dd>{v}</dd>" for k, v in rows) + "</dl>"
            + fan + (f'<div class="acts">{"".join(acts)}</div>' if acts else "") + "</div>")


def dish_html(c: sqlite3.Connection, st: Mapping[str, Any]) -> str:
    """Below the circle: the dish so far, with a remove link per ingredient."""
    comp = st["rec"]
    sel = selections(st)
    prov = provided(c, comp)
    fillers = query.taste_circle_fillers(c, comp, set(sel))
    fillable = [d for d in ORDER if d not in prov and (fillers.get(d) or d in sel)]
    have = set(st["have"])
    rows = [f"<tr><td>{esc(pretty(comp))}</td><td>base</td><td></td><td></td></tr>"]
    for d, f in sel.items():
        rest = {k: v for k, v in sel.items() if k != d}
        rows.append(f"<tr><td>{esc(pretty(f))}</td><td>{esc(NAMES[d].lower())}</td>"
                    f"<td>{'on hand' if f in have else ''}</td>"
                    f"<td>{a(_href(st, tc=encode(rest)), 'remove')}</td></tr>")
    name = f'<div class="tc-name">{esc(dish_name(comp, sel))}</div>' if sel else ""
    return ('<div class="r4 tc"><h4>Your dish</h4>' + name
            + '<table class="tc-dish"><thead><tr><th>Ingredient</th><th>Fills</th>'
              '<th>Availability</th><th></th></tr></thead><tbody>' + "".join(rows)
            + f'</tbody></table><div class="muted">{len(sel)} of {len(fillable)} open dimensions '
              'filled. A plate does not need all eleven.</div></div>')


def unavailable_html(c: sqlite3.Connection, st: Mapping[str, Any]) -> str:
    if not st["rec"]:
        msg = ("Open a prepared ingredient in the overview: the taste circle builds a dish "
               "around the record in detail.")
    else:
        msg = (f"{esc(pretty(st['rec']))} has no sensory profile, so the circle cannot say which "
               "dimensions it already provides. Open another prepared ingredient.")
    return f'<div class="r4 muted">{msg}</div>'


CSS = """<style>
.r4 .tabs .k-circle {border-top:3px solid var(--circle-tab)}
.r4.tc .tc-dl {display:grid; grid-template-columns:max-content 1fr; gap:2px 12px; margin:6px 0}
.r4.tc .tc-dl dt {color:var(--ink-3)} .r4.tc .tc-dl dd {margin:0}
.r4.tc .tc-fan {background:var(--fill-soft); border-left:3px solid var(--ink-2); padding:4px 8px; margin:4px 0}
.r4.tc .tc-name {font-weight:600; margin:2px 0 4px}
.r4.tc table.tc-dish td, .r4.tc table.tc-dish th {padding:2px 10px 2px 0; text-align:left}
</style>"""
