"""Three desktop data layouts over the same model (R3 prototype).

L1  Associative table      - rows x attributes and rows x roles, filters grey
                             out rather than remove (Qlik's selection states).
L2  Relationship explorer  - one focus node, what it comes from and goes to,
                             a complexity step control (Celonis), refocus on
                             any neighbour (ARIS object-to-object).
L3  Overview / detail      - an overview list with status strips, a fact sheet
                             for one record (ARIS fact sheet), side-by-side
                             compare (ThoughtSpot pivot / UiPath compare).

All rendering is pure functions of the model so captures and tests are
deterministic. Status is shown the same way in all three (STATUS_STYLE).
"""
from __future__ import annotations

from html import escape as esc
from typing import Any

from model import pretty, state_gaps

# One visual code for epistemic status, shared by every layout.
STATUS_STYLE = {
    "curated":      ("Curated",     "st-cur"),
    "on_hand":      ("On hand",     "st-have"),
    "evidence":     ("Source",      "st-ev"),
    "hypothesis":   ("Idea",        "st-hyp"),
    "tested":       ("Tested",      "st-test"),
    "not_recorded": ("Not recorded", "st-nr"),
}

CSS = """
<style>
.r3 {font-size:14px; line-height:1.4; color:#1f2328}
.r3 table {border-collapse:collapse; width:100%; margin:6px 0 14px}
.r3 th {text-align:left; font-weight:600; background:#f3f1ec; border-bottom:2px solid #d8d4cb;
        padding:5px 8px; position:sticky; top:0; white-space:nowrap}
.r3 td {border-bottom:1px solid #e6e2da; padding:5px 8px; vertical-align:top; overflow-wrap:anywhere}
.r3 tr.excluded td {color:#9a958c; background:#f7f6f3}
.r3 tr.excluded td .badge {opacity:.55}
.r3 tr.focus td {background:#fff8e6}
.r3 .num {text-align:right; font-variant-numeric:tabular-nums}
.r3 .badge {display:inline-block; font-size:11px; padding:0 6px; border-radius:9px; margin:1px 2px 1px 0;
            border:1px solid transparent; white-space:nowrap}
.r3 .st-cur  {background:#eef2f7; border-color:#c9d3e0}
.r3 .st-have {background:#dff3e4; border-color:#7cc08f; font-weight:600}
.r3 .st-ev   {background:#f1ecf9; border-color:#cbbde6}
.r3 .st-hyp  {background:#fff; border:1px dashed #b07d1a; color:#7a5510}
.r3 .st-test {background:#fff3d6; border:1px solid #b07d1a; color:#5c3f08}
.r3 .st-nr   {background:repeating-linear-gradient(45deg,#f4f2ee,#f4f2ee 4px,#e9e5dd 4px,#e9e5dd 8px);
              color:#6b665d; border-color:#d8d4cb}
.r3 .cell-nr {background:repeating-linear-gradient(45deg,#faf9f6,#faf9f6 4px,#efece5 4px,#efece5 8px);
              color:#6b665d; font-size:12px}
.r3 .cell-none {color:#b8b3aa}
.r3 .legend {font-size:12px; color:#555; margin:2px 0 8px}
.r3 .muted {color:#6b665d; font-size:12px}
.r3 .why {font-size:12px; color:#6b665d}
.r3 .strip span {display:inline-block; width:9px; height:12px; margin-right:1px; border-radius:2px}
.r3 .strip .f {background:#7cc08f} .r3 .strip .c {background:#c9d3e0} .r3 .strip .n {background:#e3dfd6}
.r3 h4 {margin:14px 0 4px; font-size:15px}
.r3 .sheet dt {font-weight:600; float:left; width:150px; clear:left}
.r3 .sheet dd {margin:0 0 4px 160px}
.r3 .ideas {border:1px dashed #b07d1a; border-radius:6px; padding:6px 10px; background:#fffdf7}
.r3 .gaps {border:1px solid #d8d4cb; border-radius:6px; padding:6px 10px;
           background:repeating-linear-gradient(45deg,#fbfaf7,#fbfaf7 6px,#f3f0ea 6px,#f3f0ea 12px)}
.r3 .nb-list td:first-child {white-space:nowrap}
</style>
"""


def badge(status: str, text: str | None = None) -> str:
    label, cls = STATUS_STYLE[status]
    return f'<span class="badge {cls}">{esc(text or label)}</span>'


def legend() -> str:
    return ('<div class="legend">Status: ' + " ".join(
        badge(k) for k in STATUS_STYLE) +
        ' · a hatched cell means nothing is written there, not "no".</div>')


def _filler_cell(r: dict) -> str:
    if not r["fillers"]:
        return '<td class="cell-nr">needed · nothing recorded</td>'
    bits = []
    for p in r["fillers"]:
        if p["confidence"] == "experimental":
            bits.append(badge("hypothesis", pretty(p["filler"])))
        elif p["filler"] in r["on_hand"]:
            bits.append(badge("on_hand", "● " + pretty(p["filler"])))
        else:
            bits.append(badge("curated", pretty(p["filler"])))
    pr = f'<div class="muted">priority {esc(r["priority"] or "?")}</div>'
    return "<td>" + "".join(bits) + pr + "</td>"


# ---------------------------------------------------------------------------
# L1  Associative table
# ---------------------------------------------------------------------------

def filter_options(m: dict) -> dict[str, list[str]]:
    roles = list(m["roles"])
    fillers = sorted({p["filler"] for s in m["states"] for r in s["roles"].values()
                      for p in r["fillers"]})
    return {"role": roles, "filler": fillers,
            "has": ["flavour route", "Scout idea", "tasting", "cited source",
                    "something on hand"]}


def matches(s: dict, sel: dict[str, list[str]]) -> tuple[bool, list[str]]:
    """Does state *s* satisfy every active filter? Returns (ok, reasons it
    is excluded) - the reasons are shown, like Qlik's grey states."""
    why = []
    for role in sel.get("role", []):
        if role not in s["roles"]:
            why.append(f"does not need {role}")
    for f in sel.get("filler", []):
        if not any(p["filler"] == f for r in s["roles"].values() for p in r["fillers"]):
            why.append(f"no pairing with {pretty(f)}")
    tests = {"flavour route": bool(s["routes"]),
             "Scout idea": bool(s["hypotheses"]),
             "tasting": bool(s["trials"]),
             "cited source": bool(s["sources"]),
             "something on hand": any(r["on_hand"] for r in s["roles"].values())
             or any(rt["available_elements"] for rt in s["routes"])}
    for h in sel.get("has", []):
        if not tests[h]:
            why.append(f"no {h}")
    return (not why), why


def associative_html(m: dict, sel: dict[str, list[str]],
                     focus: str | None = None) -> str:
    states = m["states"]
    res = [(s, *matches(s, sel)) for s in states]
    n_in = sum(1 for _, ok, _ in res if ok)
    active = any(sel.values())
    out = [CSS, '<div class="r3">', legend()]
    if active:
        out.append(f'<div class="muted"><b>{n_in}</b> of {len(states)} prepared '
                   f'ingredients match · the other {len(states) - n_in} stay in '
                   'place, greyed, with the reason.</div>')

    # Table A: attributes
    out.append("<h4>Prepared ingredients × attributes</h4><table><tr>"
               "<th>Prepared ingredient</th><th>From</th><th>Technique</th>"
               "<th>Confidence</th><th>Flavour shift</th><th>Keeps · freezes · batch</th>"
               "<th>Routes</th><th>Ideas</th><th>Sources</th><th>Not recorded</th>"
               "</tr>")
    for s, ok, why in res:
        cls = "focus" if s["component"] == focus else ("" if ok or not active else "excluded")
        routes = ("".join(badge("on_hand" if rt["available_elements"] else "curated",
                                rt["name"]) for rt in s["routes"])
                  or '<span class="cell-none">—</span>')
        tested = sum(1 for h in s["hypotheses"] if h.get("trials"))
        ideas = (badge("hypothesis", str(len(s["hypotheses"])))
                 + (badge("tested", f"{tested} tested") if tested else "")
                 if s["hypotheses"] else '<span class="cell-none">—</span>')
        gaps = ", ".join(state_gaps(s)) or "—"
        excl = (f'<div class="why">excluded: {esc("; ".join(why))}</div>'
                if active and not ok else "")
        out.append(
            f'<tr class="{cls}"><td><b>{esc(s["label"])}</b>{excl}</td>'
            f'<td>{esc(s["from"])}</td><td>{esc(s["technique"])}</td>'
            f'<td>{badge("curated", s["confidence"].replace("_", " "))}</td>'
            f'<td>{esc(s["flavour_shift"] or "")}</td>'
            f'<td>{esc(s["keeps_well"] or "?")} · {"yes" if s["freezes_well"] else "no"}'
            f' · {esc(s["batch_prep_value"] or "?")}</td>'
            f'<td>{routes}</td><td>{ideas}</td>'
            f'<td class="num">{len(s["sources"]) or "—"}</td>'
            f'<td class="muted">{esc(gaps)}</td></tr>')
    out.append("</table>")

    # Table B: states x roles matrix
    roles = m["roles"]
    out.append("<h4>Prepared ingredients × what they still need</h4>"
               '<div class="muted">Each cell lists the recorded pairings for that '
               "role. Blank (—) means the role is not a recorded need for that "
               "preparation.</div><table><tr><th>Prepared ingredient</th>"
               + "".join(f"<th>{esc(r)}</th>" for r in roles) + "</tr>")
    for s, ok, why in res:
        cls = "focus" if s["component"] == focus else ("" if ok or not active else "excluded")
        cells = []
        for r in roles:
            if r in s["roles"]:
                cells.append(_filler_cell(s["roles"][r]))
            else:
                cells.append('<td class="cell-none">—</td>')
        out.append(f'<tr class="{cls}"><td><b>{esc(s["label"])}</b></td>'
                   + "".join(cells) + "</tr>")
    out.append("</table></div>")
    return "".join(out)


def relations_rows(m: dict) -> list[dict]:
    """The long form: every relation as a sortable row (the 'table box')."""
    rows = []
    for r in m["relations"]:
        extra = {k: v for k, v in r.items()
                 if k not in ("source", "kind", "target", "status") and v not in (None, "")}
        rows.append({"from": pretty(r["source"]), "relation": r["kind"],
                     "to": pretty(r["target"]),
                     "status": STATUS_STYLE[r["status"]][0],
                     "details": "; ".join(f"{k}: {pretty(str(v)) if k == 'state' else v}"
                                          for k, v in extra.items())})
    return rows


# ---------------------------------------------------------------------------
# L2  Relationship explorer
# ---------------------------------------------------------------------------

LEVELS = ["needs and routes", "+ pairings", "+ ideas and sources", "+ where it is used"]

_EDGE = {"curated": 'color="#5a6b82"', "on_hand": 'color="#2e8b4e" penwidth=2.4',
         "evidence": 'color="#8a72b8" style=dotted',
         "hypothesis": 'color="#b07d1a" style=dashed',
         "tested": 'color="#b07d1a" penwidth=2.2',
         "not_recorded": 'color="#b8b3aa" style=dashed'}
_NODE = {"state": 'shape=box style="rounded,filled" fillcolor="#fff8e6" color="#b07d1a"',
         "ingredient": 'shape=box style="rounded,filled" fillcolor="#f3f1ec" color="#9a958c"',
         "role": 'shape=ellipse style=filled fillcolor="#eef2f7" color="#c9d3e0"',
         "filler": 'shape=box style="rounded" color="#c9d3e0"',
         "have": 'shape=box style="rounded,filled" fillcolor="#dff3e4" color="#2e8b4e"',
         "route": 'shape=box style="rounded,filled" fillcolor="#eef2f7" color="#5a6b82"',
         "idea": 'shape=box style="rounded,dashed" color="#b07d1a"',
         "tested": 'shape=box style="rounded,filled" fillcolor="#fff3d6" color="#b07d1a"',
         "source": 'shape=note color="#8a72b8"',
         "gap": 'shape=box style="rounded,dashed,filled" fillcolor="#f4f2ee" color="#b8b3aa" fontcolor="#6b665d"',
         "use": 'shape=plaintext fontcolor="#6b665d"'}


def node_kinds(m: dict) -> dict[str, str]:
    """Every node id in the model and what it is, for the focus picker."""
    k: dict[str, str] = {m["ingredient"]: "ingredient"}
    for s in m["states"]:
        k[s["component"]] = "state"
    for r in m["relations"]:
        if r["kind"] == "needs":
            k.setdefault(r["target"], "role")
        elif r["kind"] in ("filled by", "uses"):
            k.setdefault(r["target"], "filler")
        elif r["kind"] == "route":
            k.setdefault(r["target"], "route")
        elif r["kind"] == "idea":
            k.setdefault(r["target"], "filler")
    return k


def neighbours(m: dict, focus: str) -> dict[str, list[dict]]:
    """Celonis-style 'comes from' / 'goes to' for any node."""
    comes = [r for r in m["relations"] if r["target"] == focus]
    goes = [r for r in m["relations"] if r["source"] == focus]
    return {"comes from": comes, "goes to": goes}


def _q(s: str) -> str:
    return '"' + s.replace('"', "'") + '"'


def explorer_dot(m: dict, focus: str, level: int) -> str:
    """Layered left-to-right graph around *focus* (a prepared ingredient or a
    filler). Edge style = status, so the graph and the tables agree."""
    lines = ['digraph G {', 'rankdir=LR; nodesep=0.18; ranksep=0.45;',
             'node [fontname="Helvetica" fontsize=11 margin="0.08,0.03"];',
             'edge [fontname="Helvetica" fontsize=9 arrowsize=0.6];']
    kinds = node_kinds(m)
    have = set(m["have"])
    seen = set()

    def node(nid, kind, label=None):
        if nid in seen:
            return
        seen.add(nid)
        lines.append(f'{_q(nid)} [label={_q(label or pretty(nid))} {_NODE[kind]}];')

    edges = set()

    def edge(a, b, status, label=""):
        if (a, b, label) in edges:
            return
        edges.add((a, b, label))
        lab = f' label={_q(label)}' if label else ""
        lines.append(f'{_q(a)} -> {_q(b)} [{_EDGE[status]}{lab}];')

    state = next((s for s in m["states"] if s["component"] == focus), None)
    if state:
        node(focus, "state", state["label"])
        src = m["ingredient"]
        node(src, "ingredient", state["from"])
        edge(src, focus, "curated", state["technique"])
        for role, r in state["roles"].items():
            rid = f"{focus}:{role}"
            if not r["fillers"]:
                node(rid, "gap", f"{role}\n(nothing recorded)")
                edge(focus, rid, "not_recorded", f"needs · {r['priority']}")
                continue
            node(rid, "role", role)
            edge(focus, rid, "curated", f"needs · {r['priority']}")
            if level >= 1:
                for p in r["fillers"]:
                    fid = f"{focus}:{role}:{p['filler']}"
                    exp = p["confidence"] == "experimental"
                    kind = "idea" if exp else "have" if p["filler"] in have else "filler"
                    node(fid, kind, pretty(p["filler"]))
                    edge(rid, fid, "hypothesis" if exp else
                         "on_hand" if p["filler"] in have else "curated",
                         p["confidence"].replace("_", " "))
        for rt in state["routes"]:
            rtid = f"route:{rt['route_id']}"
            node(rtid, "route", "route: " + rt["name"])
            edge(focus, rtid, "on_hand" if rt["available_elements"] else "curated",
                 rt["attestation"].replace("_", " "))
            for e in rt["elements"]:
                eid = f"{rtid}:{e['ingredient']}"
                node(eid, "have" if e["ingredient"] in have else "filler",
                     pretty(e["ingredient"]))
                edge(rtid, eid, "on_hand" if e["ingredient"] in have else "curated",
                     e["optionality"])
        if not state["roles"] and not state["routes"]:
            node(f"{focus}:none", "gap", "no needs, pairings or\nroutes recorded")
            edge(focus, f"{focus}:none", "not_recorded")
        if level >= 2:
            for h in state["hypotheses"]:
                hid = f"idea:{h['analogy_id']}"
                tried = h.get("trials") or []
                node(hid, "tested" if tried else "idea",
                     f"idea: {pretty(h['candidate'])}"
                     + (f"\n(tasted: {tried[0]['verdict']})" if tried else ""))
                edge(focus, hid, "tested" if tried else "hypothesis",
                     h["inference_strength"].replace("_", " "))
            for s in state["sources"]:
                sid = f"src:{s['title']}"
                node(sid, "source", s["title"])
                edge(sid, focus, "evidence", s["source_type"])
        if level >= 3:
            for u in state["uses"][:8]:
                uid = f"use:{u}"
                node(uid, "use", pretty(u))
                edge(focus, uid, "curated")
    else:
        # focus is a filler: every preparation it is recorded with
        node(focus, "have" if focus in have else "filler", pretty(focus))
        for r in m["relations"]:
            if r["target"] != focus:
                continue
            if r["kind"] == "filled by":
                sid = r["state"]
                node(sid, "state", pretty(sid))
                edge(sid, focus, r["status"], f"{r['source']} · {r['confidence'].replace('_', ' ')}")
            elif r["kind"] == "uses":
                rtid = f"route:{r['source']}"
                node(rtid, "route", "route: " + pretty(r["source"]))
                edge(rtid, focus, r["status"], r["optionality"])
                for rr in m["relations"]:
                    if rr["kind"] == "route" and rr["target"] == r["source"]:
                        node(rr["source"], "state", pretty(rr["source"]))
                        edge(rr["source"], rtid, "curated")
            elif r["kind"] == "idea" and level >= 2:
                node(r["source"], "state", pretty(r["source"]))
                edge(r["source"], focus, r["status"],
                     "idea · " + r["strength"].replace("_", " "))
    lines.append("}")
    return "\n".join(lines)


def neighbour_table_html(m: dict, focus: str) -> str:
    nb = neighbours(m, focus)
    out = [CSS, '<div class="r3">']
    for title, rows in nb.items():
        out.append(f"<h4>{title.capitalize()} ({len(rows)})</h4>")
        if not rows:
            out.append('<div class="muted">none</div>')
            continue
        out.append('<table class="nb-list"><tr><th>Relation</th><th>Node</th>'
                   "<th>Status</th><th>Details</th></tr>")
        for r in rows:
            other = pretty(r["source"] if title == "comes from" else r["target"])
            if r.get("state") and title == "comes from":
                other = f"{pretty(r['state'])} → {other}"
            det = {k: v for k, v in r.items()
                   if k not in ("source", "kind", "target", "status", "filled") and v not in (None, "")}
            out.append(f"<tr><td>{esc(r['kind'])}</td><td>{esc(other)}</td>"
                       f"<td>{badge(r['status'])}</td><td class='muted'>"
                       + esc("; ".join(f"{k}: {pretty(str(v)) if k == 'state' else v}"
                                       for k, v in det.items())) + "</td></tr>")
        out.append("</table>")
    out.append("</div>")
    return "".join(out)


# ---------------------------------------------------------------------------
# L3  Overview / detail workspace
# ---------------------------------------------------------------------------

def strip(s: dict) -> str:
    """One square per needed role: green = on hand, blue = pairing recorded,
    grey = nothing recorded."""
    sq = []
    for r in s["roles"].values():
        sq.append('<span class="f"></span>' if r["on_hand"] else
                  '<span class="c"></span>' if r["fillers"] else '<span class="n"></span>')
    return '<span class="strip">' + "".join(sq) + "</span>"


def overview_rows(m: dict) -> list[dict]:
    """The overview as plain rows for a selectable table."""
    out = []
    for s in m["states"]:
        dots = "".join("●" if r["on_hand"] else "◐" if r["fillers"] else "○"
                       for r in s["roles"].values())
        out.append({"Prepared ingredient": s["label"], "Needs": dots or "—",
                    "Routes": len(s["routes"]), "Ideas": len(s["hypotheses"]),
                    "Tasted": len(s["trials"]), "Sources": len(s["sources"]),
                    "Confidence": s["confidence"].replace("_", " ")})
    return out


def overview_html(m: dict, focus: str | None, compare: list[str]) -> str:
    out = [CSS, '<div class="r3"><table><tr><th>Prepared ingredient</th>'
           '<th>Needs (■ on hand ■ paired ■ none)</th><th class="num">Routes</th>'
           '<th class="num">Ideas</th><th class="num">Sources</th></tr>']
    for s in m["states"]:
        cls = "focus" if s["component"] == focus else ""
        mark = " ◆" if s["component"] in compare else ""
        out.append(f'<tr class="{cls}"><td><b>{esc(s["label"])}</b>{mark}</td>'
                   f'<td>{strip(s)} <span class="muted">{len(s["roles"])}</span></td>'
                   f'<td class="num">{len(s["routes"]) or "—"}</td>'
                   f'<td class="num">{len(s["hypotheses"]) or "—"}</td>'
                   f'<td class="num">{len(s["sources"]) or "—"}</td></tr>')
    out.append("</table></div>")
    return "".join(out)


def fact_sheet_html(m: dict, comp: str) -> str:
    s = next(x for x in m["states"] if x["component"] == comp)
    out = [CSS, '<div class="r3">', legend()]
    out.append(f'<h3 style="margin:0">{esc(s["label"])}</h3>'
               f'<div class="muted">{esc(s["from"])} → {esc(s["technique"])} → '
               f'{esc(s["label"])} · {badge("curated", "confidence " + s["confidence"].replace("_", " "))}</div>')
    out.append('<h4>Attributes</h4><dl class="sheet">')
    prof = s["profile"] or {}
    for k, v in [("Flavour shift", s["flavour_shift"]), ("Texture shift", s["texture_shift"]),
                 ("Flavour tags", ", ".join(prof.get("flavour_tags", [])) or None),
                 ("Provides", ", ".join(prof.get("provides_roles", [])) or None),
                 ("Keeps", s["keeps_well"]), ("Freezes", "yes" if s["freezes_well"] else "no"),
                 ("Batch value", s["batch_prep_value"]),
                 ("Watch for", ", ".join(s["risks"]) or None)]:
        val = esc(v) if v else '<span class="cell-nr" style="padding:0 6px">not recorded</span>'
        out.append(f"<dt>{k}</dt><dd>{val}</dd>")
    out.append("</dl>")

    out.append("<h4>Needs and recorded pairings</h4>")
    if s["roles"]:
        out.append("<table><tr><th>Role</th><th>Priority</th><th>Pairings</th>"
                   "<th>Note</th></tr>")
        for role, r in s["roles"].items():
            out.append(f"<tr><td>{esc(role)}</td><td>{esc(r['priority'] or '')}</td>"
                       + _filler_cell(r) + f"<td class='muted'>{esc(r['note'] or '')}</td></tr>")
        out.append("</table>")
    else:
        out.append('<div class="cell-nr" style="padding:4px 8px">no needed roles recorded</div>')

    out.append("<h4>Flavour routes</h4>")
    if s["routes"]:
        out.append("<table><tr><th>Route</th><th>Uses</th><th>Why it fits</th>"
                   "<th>Attestation</th></tr>")
        for rt in s["routes"]:
            uses = "".join(badge("on_hand" if e in rt["available_elements"] else "curated",
                                 f"{pretty(e['ingredient'])} ({e['optionality']})")
                           for e in rt["elements"])
            out.append(f"<tr><td><b>{esc(rt['name'])}</b></td><td>{uses}</td>"
                       f"<td>{esc(rt.get('fit_reason') or '')}</td>"
                       f"<td>{esc(rt['attestation'].replace('_', ' '))}</td></tr>")
        out.append("</table>")
    else:
        out.append('<div class="cell-nr" style="padding:4px 8px">no flavour route written</div>')

    out.append("<h4>Evidence</h4>")
    if s["sources"]:
        out.append("<table><tr><th>Source</th><th>Type</th><th>What it supports</th></tr>"
                   + "".join(f"<tr><td>{badge('evidence', x['title'])}</td>"
                             f"<td>{esc(x['source_type'])}</td>"
                             f"<td>{esc(x['claim_scope'] or '')}</td></tr>"
                             for x in s["sources"]) + "</table>")
    else:
        out.append('<div class="cell-nr" style="padding:4px 8px">no cited source</div>')

    out.append('<h4>Ideas (Scout) — not recommendations</h4>')
    if s["hypotheses"]:
        out.append('<div class="ideas"><table><tr><th>Idea</th><th>Instead of</th>'
                   "<th>Reasoning strength</th><th>Seen in recipes</th><th>Tasted</th></tr>")
        for h in s["hypotheses"]:
            tr = h.get("trials") or []
            nov = (h.get("novelty") or {}).get("class") or "not checked"
            out.append(f"<tr><td>{badge('tested' if tr else 'hypothesis', pretty(h['candidate']))}</td>"
                       f"<td>{esc(pretty(h['source']))}</td>"
                       f"<td>{esc(h['inference_strength'].replace('_', ' '))}</td>"
                       f"<td>{esc(nov)}</td>"
                       f"<td>{esc(tr[0]['verdict'] + ' (' + tr[0]['tested_at'] + ')') if tr else '—'}</td></tr>")
        out.append("</table></div>")
    else:
        out.append('<div class="cell-nr" style="padding:4px 8px">no Scout idea</div>')

    gaps = state_gaps(s)
    out.append('<h4>Not recorded</h4><div class="gaps">'
               + (esc("; ".join(gaps)) if gaps else "nothing obvious missing")
               + '</div></div>')
    return "".join(out)


def compare_html(m: dict, comps: list[str]) -> str:
    """Attributes as rows, chosen preparations as columns (a pivot)."""
    ss = [x for x in m["states"] if x["component"] in comps]
    if not ss:
        return ""
    head = "".join(f"<th>{esc(s['label'])}</th>" for s in ss)
    rows: list[tuple[str, list[str]]] = [
        ("From → technique", [esc(f"{s['from']} → {s['technique']}") for s in ss]),
        ("Confidence", [badge("curated", s["confidence"].replace("_", " ")) for s in ss]),
        ("Flavour shift", [esc(s["flavour_shift"] or "") for s in ss]),
        ("Keeps · freezes", [esc(f"{s['keeps_well']} · {'yes' if s['freezes_well'] else 'no'}") for s in ss]),
    ]
    for role in m["roles"]:
        cells = []
        for s in ss:
            r = s["roles"].get(role)
            cells.append(_filler_cell(r)[4:-5] if r and r["fillers"] else
                         ('<span class="badge st-nr">needed · nothing recorded</span>' if r
                          else '<span class="cell-none">—</span>'))
        rows.append((f"needs {role}", cells))
    rows.append(("Routes", ["".join(badge("on_hand" if rt["available_elements"] else "curated",
                                          rt["name"]) for rt in s["routes"]) or
                            '<span class="badge st-nr">none written</span>' for s in ss]))
    rows.append(("Ideas", [", ".join(pretty(h["candidate"]) for h in s["hypotheses"]) or "—"
                           for s in ss]))
    rows.append(("Not recorded", [esc("; ".join(state_gaps(s)) or "nothing listed") for s in ss]))
    body = "".join(f"<tr><th>{esc(k)}</th>" + "".join(f"<td>{c}</td>" for c in v) + "</tr>"
                   for k, v in rows)
    return (CSS + '<div class="r3"><h4>Compare</h4><table><tr><th></th>' + head
            + "</tr>" + body + "</table></div>")
