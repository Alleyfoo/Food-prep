"""R4 integrated workspace: four coordinated representations, one context.

    Overview  associative table (prepared ingredients x a chosen column set)
    Detail    structured fact sheet for the selected record (8 fixed sections)
    Compare   2-3 pinned records as aligned columns
    Trace     relationship graph + the same edges as a table

Every renderer is a pure function of (model, state), so captures and tests are
deterministic. Dimensions are shown as separate labelled columns in tables;
only the dense matrix uses a compact glyph code (see LEGEND).
"""
from __future__ import annotations

from html import escape as esc
from typing import Any

import r4_state as S
from r4_model import (CONFIDENCE_FIELD_LABEL, KNOWLEDGE_LABEL, gaps, linked, of,
                   pretty, route_ids, shared_gaps, state_by)

CSS = """
<style>
.r4 {font-size:14px; line-height:1.4; color:#1f2328}
.r4 a {color:#1a4f8b; text-decoration:none} .r4 a:hover {text-decoration:underline}
.r4 table {border-collapse:collapse; width:100%; margin:4px 0 12px}
.r4 th {text-align:left; font-weight:600; background:#f3f1ec; border-bottom:2px solid #d8d4cb;
        padding:4px 7px; white-space:nowrap; font-size:13px}
.r4 td {border-bottom:1px solid #e6e2da; padding:4px 7px; vertical-align:top; overflow-wrap:anywhere}
.r4 tr.excluded td {color:#9a958c; background:#f7f6f3}
.r4 tr.excluded td a {color:#7f8ea3}
.r4 tr.sel td {background:#fff4d1}
.r4 tr.pinned td:first-child {box-shadow:inset 3px 0 0 #1a4f8b}
.r4 tr.same td {color:#77726a}
.r4 .why {font-size:12px; color:#8a6d3b}
.r4 .muted {color:#6b665d; font-size:12px}
.r4 .nr {background:repeating-linear-gradient(45deg,#faf9f6,#faf9f6 4px,#efece5 4px,#efece5 8px);
         color:#6b665d; font-size:12px}
.r4 tr.sel td.nr {background:repeating-linear-gradient(45deg,#fff4d1,#fff4d1 4px,#efe3bf 4px,#efe3bf 8px)}
.r4 .na {color:#b8b3aa}
.r4 .exp {font-style:italic; color:#7a5510}
.r4 .gen {font-style:italic; color:#7a5510; border-bottom:1px dashed #b07d1a}
.r4 .have {color:#1f6b35; font-weight:600}
.r4 .tested {color:#5c3f08; font-weight:600}
.r4 .ctx {background:#f6f4ef; border:1px solid #e1ddd3; border-radius:6px; padding:6px 10px;
          margin:0 0 8px; font-size:13px}
.r4 .ctx b {font-weight:600; color:#4a463f}
.r4 .chip {display:inline-block; border:1px solid #cfc9bd; border-radius:10px; padding:0 7px;
           margin:1px 3px 1px 0; background:#fff; white-space:nowrap}
.r4 .chip a {color:#8a3b3b; margin-left:4px}
.r4 .tabs a, .r4 .tabs span {display:inline-block; padding:3px 12px; margin-right:4px;
          border:1px solid #d8d4cb; border-bottom:none; border-radius:6px 6px 0 0; background:#f3f1ec}
.r4 .tabs span.on {background:#fff; font-weight:600}
.r4 .tabs {border-bottom:1px solid #d8d4cb; margin:0 0 8px}
.r4 h3 {margin:2px 0 6px; font-size:18px}
.r4 h4 {clear:both; margin:12px 0 3px; font-size:14px; color:#3b3833}
.r4 h4 .n {color:#8d877c; font-weight:400; margin-right:4px}
.r4 dl {margin:0; display:grid; grid-template-columns:160px 1fr; gap:2px 10px}
.r4 dt {font-weight:600; color:#4a463f} .r4 dd {margin:0}
.r4 .scroll {overflow-x:auto; max-width:100%}
.r4 .sub {font-size:12px; color:#6b665d}
.r4 .ideas {border:1px dashed #b07d1a; border-radius:6px; padding:4px 10px; background:#fffdf7}
.r4 .gapbox {border:1px solid #d8d4cb; border-radius:6px; padding:4px 10px;
             background:repeating-linear-gradient(45deg,#fbfaf7,#fbfaf7 6px,#f3f0ea 6px,#f3f0ea 12px)}
.r4 .banner {background:#fbf6e9; border:1px solid #e8d9ad; border-radius:6px; padding:4px 10px;
             margin:0 0 6px; font-size:13px}
.r4 .legend {font-size:12px; color:#555; margin:2px 0 6px}
.r4 .dots {letter-spacing:1px; font-size:13px}
.r4 .num {text-align:right; font-variant-numeric:tabular-nums}
.r4 .diff {color:#8a3b3b; font-weight:700}
</style>
"""

LEGEND = ('<div class="legend">Matrix code: name = curated pairing · '
          '<span class="have">● name</span> = on hand · '
          '<span class="exp">◇ name</span> = experimental pairing · '
          '<span class="tested">✓</span> = a linked Scout idea was tasted · '
          '<span class="nr">&nbsp;hatched&nbsp;</span> = needed, no curated pairing recorded · '
          '<span class="na">—</span> = not a recorded need</div>')


NA = '<span class="na">n/a</span>'


def a(href: str, text: str, title: str | None = None) -> str:
    t = f' title="{esc(title)}"' if title else ""
    return f'<a href="{esc(href)}" target="_self"{t}>{text}</a>'


# --- dimension formatters (one per dimension, used in every pane) ----------

def knowledge_txt(r: dict) -> str:
    cls = {"experimental": "exp", "generated": "gen"}.get(r["knowledge"], "")
    lab = KNOWLEDGE_LABEL[r["knowledge"]]
    return f'<span class="{cls}">{esc(lab)}</span>' if cls else esc(lab)


def conf_txt(r: dict, with_field: bool = False) -> str:
    c = r.get("confidence")
    if not c:
        return NA
    if r.get("knowledge") == "experimental":
        return '<span class="na">not graded</span> <span class="muted">(recorded as “experimental”)</span>'
    val = esc(pretty(c["value"]) or "not recorded")
    if with_field or c["field"] != "confidence":
        return f'{val} <span class="muted">({CONFIDENCE_FIELD_LABEL[c["field"]]})</span>'
    return val


def avail_txt(r: dict) -> str:
    v = r.get("availability")
    if v is None:
        return NA
    return '<span class="have">● on hand</span>' if v == "on hand" else \
        '<span class="muted">not on hand</span>'


def sources_txt(st: dict, r: dict, scope: bool = True) -> str:
    ev = r["evidence"]
    if ev["coverage"] == "not applicable":
        return NA
    if not ev["sources"]:
        return f'<span class="nr">&nbsp;{esc(ev["coverage"])}&nbsp;</span>'
    out = []
    for s in ev["sources"]:
        link = a(S.href(st, trace=f"source:{s['source_id']}", pane="trace"),
                 esc(s["title"]), "Trace what this source backs")
        bit = f'{link} <span class="muted">{esc(s["type"] or "type not recorded")}</span>'
        if scope:
            bit += ('<br><span class="muted">scope: </span>' + esc(s["claim_scope"])
                    if s["claim_scope"] else
                    '<br><span class="muted">scope: not recorded</span>')
        out.append(bit)
    return "<br>".join(out)


def testing_txt(r: dict) -> str:
    t = r.get("testing")
    if not t:
        return NA
    if t["status"] == "untested":
        return '<span class="muted">untested</span>'
    return "<br>".join(f'<span class="tested">✓ {esc(x["verdict"])}</span> '
                       f'<span class="muted">{esc(x["tested_at"])}</span>'
                       for x in t["trials"])


def opt_txt(r: dict) -> str:
    o = r.get("optionality")
    if not o:
        return NA
    return f"<b>{esc(o)}</b>" if o == "required" else esc(o)


def ing_link(st: dict, name: str, text: str | None = None) -> str:
    return a(S.href(st, trace=f"ingredient:{name}", pane="trace"),
             esc(text or pretty(name)), f"Trace {pretty(name)}")


def state_link(st: dict, comp: str, text: str | None = None) -> str:
    return a(S.href(st, rec=comp, pane="detail"), esc(text or pretty(comp)),
             "Open its fact sheet")


def route_link(st: dict, rid: str, name: str) -> str:
    return a(S.href(st, trace=f"route:{rid}", pane="trace"), esc(name), "Trace this route")


def _linked_tested(m: dict, rec: dict) -> bool:
    return any(x["kind"] == "idea" and x["testing"]["status"] == "tested"
               for x in linked(m, rec))


def matrix_cell(m: dict, st: dict, comp: str, role: str, sel: bool = False) -> str:
    need = next((r for r in of(m, comp, "need") if r["role"] == role), None)
    pairs = [p for p in of(m, comp, "pairing") if p["role"] == role]
    if need is None and not pairs:
        return '<td class="na">—</td>'
    bits = []
    for p in pairs:
        nm = pretty(p["ingredient"])
        mark = " ✓" if _linked_tested(m, p) else ""
        if p["knowledge"] == "experimental":
            txt = f'<span class="exp">◇ {esc(nm)}{mark}</span>'
        elif p["availability"] == "on hand":
            txt = f'<span class="have">● {esc(nm)}</span>'
        else:
            txt = esc(nm)
        bits.append(a(S.href(st, trace=f"ingredient:{p['ingredient']}", pane="trace"),
                      txt, f"Trace {nm}"))
    cook = need and need["coverage"] == "recorded"
    if need is not None and not cook:
        extra = ("needed · no curated pairing" +
                 (" (only experimental)" if pairs else ""))
        body = (", ".join(bits) + "<br>" if bits else "") + esc(extra)
        return f'<td class="nr">{body}</td>'
    return "<td>" + ", ".join(bits) + "</td>"


# ---------------------------------------------------------------------------
# context bar: the whole investigation context, each part removable
# ---------------------------------------------------------------------------

def context_bar(m: dict, st: dict) -> str:
    def chip(label: str, remove: str | None) -> str:
        x = a(remove, "✕", "Remove") if remove else ""
        return f'<span class="chip">{label}{x}</span>'

    parts = [f"<b>Ingredient</b> {chip(esc(pretty(m['ingredient'])), None)}"]
    parts.append("<b>On hand</b> " + ("".join(
        chip(esc(pretty(h)), S.href(st, have=[x for x in st["have"] if x != h]))
        for h in st["have"]) or '<span class="muted">nothing entered</span>'))
    flt = S.active_filters(st)
    if flt:
        parts.append("<b>Filters</b> " + "".join(
            chip(esc(lab), S.href(st, **{k: [x for x in st[k] if x != v]}))
            for k, v, lab in flt) + a(S.href(st, has=[], paired=[], gap=[]), "clear filters"))
    sel = []
    if st["rec"]:
        sel.append("<b>Selected</b> " + chip(esc(pretty(st["rec"])), S.href(st, rec="")))
    if st["cmp"]:
        sel.append("<b>Compare</b> " + "".join(
            chip(esc(pretty(c)), S.href(st, cmp=[x for x in st["cmp"] if x != c]))
            for c in st["cmp"]))
    f = S.trace_focus(st)
    if f:
        sel.append("<b>Trace</b> " + chip(esc(_focus_label(m, f)), S.href(st, trace="")))
    reset = a(S.href({**S.DEFAULTS, "ingredient": m["ingredient"]}), "reset all")
    return ('<div class="ctx">' + " &nbsp; ".join(parts + sel) +
            f' &nbsp; <span class="muted">· {reset} · browser Back restores the previous '
            'context</span></div>')


def _focus_label(m: dict, f: tuple[str, str]) -> str:
    kind, name = f
    if kind == "source":
        s = m["sources"].get(int(name)) if name.isdigit() else None
        return f"source {s['title']}" if s else f"source #{name}"
    if kind == "route":
        r = next((r for r in of(m, kind="route_fit") if r["route_id"] == name), None)
        return f"route {r['attrs']['name']}" if r else f"route {pretty(name)}"
    return pretty(name)


# ---------------------------------------------------------------------------
# A. Overview
# ---------------------------------------------------------------------------

def _needs_dots(m: dict, comp: str) -> tuple[str, str]:
    needs = of(m, comp, "need")
    pairs = of(m, comp, "pairing")
    dots, tip = [], []
    for n in needs:
        cook = [p for p in pairs if p["role"] == n["role"] and p["knowledge"] == "curated"]
        if any(p["availability"] == "on hand" for p in cook):
            dots.append("●"); tip.append(f"{n['role']}: on hand")
        elif cook:
            dots.append("◐"); tip.append(f"{n['role']}: curated pairing recorded")
        else:
            dots.append("○"); tip.append(f"{n['role']}: no curated pairing")
    rec = sum(1 for n in needs if n["coverage"] == "recorded")
    return "".join(dots), f"{rec} of {len(needs)} paired · " + "; ".join(tip)


def overview_html(m: dict, st: dict) -> str:
    cols = st["cols"]
    common = shared_gaps(m)
    head = '<div class="tabs">' + "".join(
        f'<span class="on">{esc(lab)}</span>' if k == cols else
        a(S.href(st, cols=k), esc(lab)) for k, lab in S.COLS.items()) + "</div>"
    rows, n_match = [], 0
    for s in m["states"]:
        comp = s["component"]
        why = S.exclusion(m, comp, st)
        n_match += not why
        if why and st["hide"]:
            continue
        cls = " ".join(c for c in ("excluded" if why else "",
                                   "sel" if comp == st["rec"] else "",
                                   "pinned" if comp in st["cmp"] else "") if c)
        change = S.pin(st, comp)
        tip = ("Remove from compare" if comp in st["cmp"] else
               f"Compare with {pretty(st['rec'])}" if len(change["cmp"]) == 2 and not st["cmp"]
               else "Add to compare (max 3)")
        pin = a(S.href(st, **change), "☑" if comp in st["cmp"] else "☐", tip)
        name = state_link(st, comp) + (
            f'<div class="sub">{esc(s["from_label"])} → {esc(s["technique"])} · '
            f'{esc(pretty(s["confidence"]))}</div>' if cols == "summary" else "") + (
            f'<div class="why">excluded: {esc("; ".join(why))}</div>' if why else "")
        cells = [f"<td>{pin}</td>", f"<td>{name}</td>"]
        cells += _overview_cells(m, st, s, cols, common, comp == st["rec"])
        cells.append("<td>" + a(S.href(st, trace=f"state:{comp}", pane="trace"), "⇄",
                                "Trace its relationships") + "</td>")
        rows.append(f'<tr class="{cls}">' + "".join(cells) + "</tr>")
    hdr = ["", "Prepared ingredient"] + _overview_headers(m, cols) + [""]
    flt = S.active_filters(st)
    count = (f'<div class="muted">{n_match} of {len(m["states"])} match the filters'
             + (" · " + a(S.href(st, hide=not st["hide"]),
                          "show excluded" if st["hide"] else "hide excluded")
                if n_match < len(m["states"]) else "") + "</div>") if flt else ""
    banner = (f'<div class="banner">For every {esc(pretty(m["ingredient"]))} preparation: '
              + esc("; ".join(common)) + ". Not repeated in the rows.</div>") if common else ""
    legend = LEGEND if cols == "matrix" else (
        '<div class="legend">Needs: ● curated pairing on hand · ◐ curated pairing recorded · '
        '○ no curated pairing. ☐ adds to compare · ⇄ traces.</div>' if cols == "summary" else "")
    return (head + banner + count + legend + '<div class="scroll"><table><tr>' +
            "".join(f"<th>{esc(h)}</th>" for h in hdr) + "</tr>" + "".join(rows) +
            "</table></div>")


def _overview_headers(m: dict, cols: str) -> list[str]:
    if cols == "sensory":
        return ["Flavour shift", "Texture shift", "Risks", "Keeps · freezes · batch"]
    if cols == "matrix":
        return list(m["roles"])
    if cols == "evidence":
        return ["Step sources (scope)", "Pairing sources", "Pairings without source",
                "Pairing claim scope"]
    return ["Needs", "Flavour routes", "Ideas", "Not recorded"]


def _overview_cells(m, st, s, cols, common, sel) -> list[str]:
    comp = s["component"]
    pairs = of(m, comp, "pairing")
    curated = [p for p in pairs if p["knowledge"] == "curated"]
    step = of(m, comp, "transformation")[0]
    if cols == "sensory":
        kfb = " · ".join([f"keeps {s['keeps_well'] or '?'}",
                          "freezes" if s["freezes_well"] else "doesn't freeze",
                          f"batch {s['batch_prep_value'] or '?'}"])
        return [f"<td>{esc(s['flavour_shift'] or '')}</td>",
                f"<td>{esc(s['texture_shift'] or '')}</td>",
                f"<td>{esc(', '.join(s['risks'])) or '<span class=muted>none recorded</span>'}</td>",
                f"<td>{esc(kfb)}</td>"]
    if cols == "matrix":
        return [matrix_cell(m, st, comp, role, sel) for role in m["roles"]]
    if cols == "evidence":
        stepsrc = "<br>".join(
            esc(x["title"]) + (" ✓" if x["claim_scope"] else " <span class=muted>(no scope)</span>")
            for x in step["evidence"]["sources"]) or '<span class="nr">&nbsp;none&nbsp;</span>'
        tally: dict[str, int] = {}
        for p in curated:
            for x in p["evidence"]["sources"]:
                tally[x["title"]] = tally.get(x["title"], 0) + 1
        psrc = ", ".join(f"{esc(t)} ×{n}" for t, n in sorted(tally.items())) or \
            '<span class="nr">&nbsp;none&nbsp;</span>'
        nos = [p for p in pairs if not p["evidence"]["sources"]]
        nos_txt = ", ".join(
            f'<span class="{"exp" if p["knowledge"] == "experimental" else ""}">'
            f'{esc(pretty(p["ingredient"]))}</span>' for p in nos) or "—"
        scoped = sum(1 for p in pairs for x in p["evidence"]["sources"] if x["claim_scope"])
        links = sum(len(p["evidence"]["sources"]) for p in pairs)
        scope = (f"{scoped} of {links} links" if scoped else
                 f'<span class="nr">&nbsp;not recorded on {links} links&nbsp;</span>')
        return [f"<td>{stepsrc}</td>", f"<td>{psrc}</td>", f"<td>{nos_txt}</td>",
                f"<td>{scope}</td>"]
    dots, tip = _needs_dots(m, comp)
    nrec = sum(1 for n in of(m, comp, "need") if n["coverage"] == "recorded")
    needs = (f'<span class="dots" title="{esc(tip)}">{dots}</span> '
             f'<span class="muted">{nrec}/{len(of(m, comp, "need"))}</span>'
             if dots else '<span class="muted">none recorded</span>')
    routes = []
    for r in of(m, comp, "route_fit"):
        got, need = r["attrs"]["required_on_hand"]
        extra = f' <span class="muted">{got}/{need} req. on hand</span>' if m["have"] else ""
        routes.append(route_link(st, r["route_id"], r["attrs"]["name"]) + extra)
    ideas = of(m, comp, "idea")
    tested = sum(1 for i in ideas if i["testing"]["status"] == "tested")
    ideas_txt = (f"{len(ideas)}" + (f' · <span class="tested">{tested} tasted</span>'
                                    if tested else "")) if ideas else "—"
    row_gaps = [g for g in gaps(m, comp) if g not in common]
    gtxt = (f'<td class="nr">{esc("; ".join(row_gaps))}</td>' if row_gaps else "<td></td>")
    route_cell = ("<td>" + "<br>".join(routes) + "</td>") if routes else (
        '<td class="na">—</td>')
    return [f"<td>{needs}</td>", route_cell, f"<td>{ideas_txt}</td>", gtxt]


# ---------------------------------------------------------------------------
# B. Detail: the fact sheet
# ---------------------------------------------------------------------------

def _h(n: int, title: str, extra: str = "") -> str:
    return f'<h4><span class="n">{n}</span>{esc(title)}{extra}</h4>'


def detail_html(m: dict, st: dict, comp: str) -> str:
    s = state_by(m, comp)
    if s is None:
        return '<div class="muted">Select a prepared ingredient in the overview.</div>'
    out = [f"<h3>{esc(s['label'])}</h3>"]
    why = S.exclusion(m, comp, st)
    if why:
        out.append(f'<div class="banner">Excluded by the active filters: {esc("; ".join(why))}. '
                   "Shown because it is selected.</div>")
    step = of(m, comp, "transformation")[0]
    frm = (state_link(st, s["from"], s["from_label"]) + " (an earlier preparation)"
           if s["from"] else esc(s["from_label"]))
    # 1 identity
    out.append(_h(1, "Identity and transformation"))
    out.append(f"<dl><dt>From</dt><dd>{frm}</dd>"
               f"<dt>Technique</dt><dd>{esc(s['technique'])}</dd>"
               f"<dt>Step confidence</dt><dd>{conf_txt(step)}</dd>"
               f"<dt>Knowledge</dt><dd>{knowledge_txt(step)}</dd></dl>")
    # 2 sensory
    p = s["profile"]
    out.append(_h(2, "Sensory attributes and risks"))
    prof = (f"<dt>Flavour tags</dt><dd>{esc(', '.join(pretty(x) for x in p['flavour_tags']))}</dd>"
            f"<dt>Texture tags</dt><dd>{esc(', '.join(pretty(x) for x in p['texture_tags']))}</dd>"
            f"<dt>Provides</dt><dd>{esc(', '.join(p['provides_roles']))}</dd>"
            f"<dt>Profile note</dt><dd>{esc(p['notes'] or '')}</dd>") if p else \
        '<dt>Sensory profile</dt><dd class="nr">&nbsp;not recorded&nbsp;</dd>'
    out.append(f"<dl><dt>Flavour shift</dt><dd>{esc(s['flavour_shift'] or '')}</dd>"
               f"<dt>Texture shift</dt><dd>{esc(s['texture_shift'] or '')}</dd>{prof}"
               f"<dt>Risks</dt><dd>{esc(', '.join(s['risks'])) or 'none recorded'}</dd>"
               f"<dt>Keeps · freezes · batch</dt><dd>{esc(str(s['keeps_well']))} · "
               f"{'yes' if s['freezes_well'] else 'no'} · {esc(str(s['batch_prep_value']))}</dd></dl>")
    # 3 needed roles
    needs = of(m, comp, "need")
    out.append(_h(3, "Needed culinary roles", f' <span class="muted">({len(needs)})</span>'))
    if needs:
        rows = []
        for n in needs:
            cook, exp = n["attrs"]["curated_pairings"], n["attrs"]["experimental_pairings"]
            cov = (f"{cook} curated" + (f", {exp} experimental" if exp else "")
                   if cook else
                   "no curated pairing recorded" + (f" ({exp} experimental)" if exp else ""))
            td = "<td>" if cook else '<td class="nr">'
            rows.append(f"<tr><td>{esc(n['role'])}</td><td>{esc(n['attrs']['priority'] or '')}</td>"
                        f"<td>{esc(n['attrs']['note'] or '')}</td>{td}{esc(cov)}</td></tr>")
        out.append("<table><tr><th>Role</th><th>Priority</th><th>Note</th>"
                   "<th>Pairings recorded</th></tr>" + "".join(rows) + "</table>")
    else:
        out.append('<div class="nr">&nbsp;no needed roles recorded&nbsp;</div>')
    # 4 pairings
    pairs = of(m, comp, "pairing")
    out.append(_h(4, "Recorded pairings", f' <span class="muted">({len(pairs)})</span>'))
    if pairs:
        rows = []
        for pr in pairs:
            lk = linked(m, pr)
            note = ""
            if lk:
                note = '<div class="muted">also a Scout idea (same ids) — see 7</div>'
            role = esc(pr["role"]) + ("" if pr["attrs"]["role_is_needed"]
                                      else ' <span class="muted">(not a listed need)</span>')
            rows.append(f"<tr><td>{role}</td><td>{ing_link(st, pr['ingredient'])}{note}</td>"
                        f"<td>{knowledge_txt(pr)}</td><td>{conf_txt(pr)}</td>"
                        f"<td>{esc(pr['attrs']['application'] or '')}</td>"
                        f"<td>{avail_txt(pr)}</td><td>{sources_txt(st, pr)}</td></tr>")
        out.append("<table><tr><th>Role</th><th>Ingredient</th><th>Knowledge</th>"
                   "<th>Confidence</th><th>Application</th><th>Availability</th>"
                   "<th>Source · claim scope</th></tr>" + "".join(rows) + "</table>")
    else:
        out.append('<div class="nr">&nbsp;no pairing recorded for this preparation&nbsp;</div>')
    # 5 routes
    routes = of(m, comp, "route_fit")
    out.append(_h(5, "Flavour routes and their elements"))
    if routes:
        for r in routes:
            els = [e for e in of(m, comp, "route_element") if e["route_id"] == r["route_id"]]
            got, need = r["attrs"]["required_on_hand"]
            have = (f" · required elements on hand: {got} of {need}" if m["have"] else "")
            out.append(f"<div><b>{route_link(st, r['route_id'], r['attrs']['name'])}</b> · "
                       f"{conf_txt(r)}{esc(have)}<br><span class='muted'>Why it fits: "
                       f"{esc(r['attrs']['fit_reason'] or 'not recorded')}</span></div>")
            out.append("<table><tr><th>Element</th><th>Optionality</th><th>Contribution</th>"
                       "<th>Availability</th></tr>" + "".join(
                           f"<tr><td>{ing_link(st, e['ingredient'])}</td><td>{opt_txt(e)}</td>"
                           f"<td>{esc(e['attrs']['contribution'])}</td><td>{avail_txt(e)}</td></tr>"
                           for e in els) + "</table>")
        out.append('<div class="muted">Only “required” elements are needed for the route; '
                   "supporting and finish elements are optional. Routes carry an attestation "
                   "(how common the structure is), not sources.</div>")
    else:
        out.append('<div class="nr">&nbsp;no flavour route recorded for this preparation&nbsp;</div>')
    # 6 evidence
    out.append(_h(6, "Evidence and provenance"))
    out.append(_evidence_html(m, st, comp, step, pairs))
    # 7 ideas
    ideas = of(m, comp, "idea")
    out.append(_h(7, "Experimental ideas and tasting results"))
    if ideas:
        rows = []
        for i in ideas:
            lk = [x for x in linked(m, i) if x["kind"] == "pairing"]
            lks = "; ".join(f"experimental pairing for {x['role']}" if x["knowledge"] == "experimental"
                            else f"curated pairing for {x['role']}" for x in lk) or "—"
            rows.append(f"<tr><td>{ing_link(st, i['ingredient'])}</td>"
                        f"<td>{esc(pretty(i['attrs']['replaces']))}</td>"
                        f"<td>{esc(pretty(i['attrs']['analogy_id']))}</td>"
                        f"<td>{conf_txt(i)}</td>"
                        f"<td>{esc(pretty(i['attrs']['novelty']) or 'not observed')}</td>"
                        f"<td>{avail_txt(i)}</td><td>{testing_txt(i)}</td><td>{esc(lks)}</td></tr>")
        out.append('<div class="ideas"><div class="muted">Generated by Scout from analogy rules. '
                   "Ideas, not recommendations. Inference strength rates the analogy’s "
                   "reasoning, not the food; novelty is a recipe-corpus search class.</div>"
                   "<table><tr><th>Candidate</th><th>Replaces</th><th>Analogy</th>"
                   "<th>Strength</th><th>Novelty</th><th>Availability</th><th>Tasting</th>"
                   "<th>Also recorded as</th></tr>" + "".join(rows) + "</table>"
                   + _trial_notes(ideas) + "</div>")
    else:
        out.append('<div class="nr">&nbsp;no Scout idea generated for this preparation&nbsp;</div>')
    # 8 missing
    g = gaps(m, comp)
    out.append(_h(8, "Missing or incomplete knowledge"))
    if g:
        out.append('<div class="gapbox">' + "<br>".join(esc(x) for x in g) +
                   '<div class="muted">Not recorded means nobody wrote it down. '
                   "It does not mean “not needed” or “doesn’t work”.</div></div>")
    else:
        out.append('<div class="muted">Every section above has recorded data.</div>')
    return '<div class="r4">' + "".join(out) + "</div>"


def _trial_notes(ideas: list[dict]) -> str:
    out = []
    for i in ideas:
        for t in (i["testing"] or {}).get("trials", []):
            out.append(f'<div class="muted"><b>Tasting {esc(t["tested_at"])}</b> '
                       f'({esc(pretty(i["ingredient"]))}): verdict “{esc(t["verdict"])}”; '
                       f'ratio {esc(t["ratio"])}; temperature {esc(t["temperature"])}; '
                       f'preparation: {esc(t["preparation"])}</div>')
    return "".join(out)


def _evidence_html(m, st, comp, step, pairs) -> str:
    rows = ""
    for x in step["evidence"]["sources"]:
        link = a(S.href(st, trace=f"source:{x['source_id']}", pane="trace"), esc(x["title"]))
        rows += (f"<tr><td>{link}</td><td>{esc(x['type'] or '')}</td>"
                 f"<td>{esc(x['claim_scope'] or 'not recorded')}</td></tr>")
    out = ["<div><b>Sources for the preparation step</b> (transformation)</div>",
           ("<table><tr><th>Source</th><th>Type</th><th>Recorded claim scope</th></tr>"
            + rows + "</table>") if rows else
           '<div class="nr">&nbsp;no source recorded for the step&nbsp;</div>']
    by_src: dict[int, list[dict]] = {}
    for p in pairs:
        for x in p["evidence"]["sources"]:
            by_src.setdefault(x["source_id"], []).append((p, x))
    out.append("<div><b>Sources for the pairings</b></div>")
    if by_src:
        prow = []
        for sid, lst in by_src.items():
            src = m["sources"][sid]
            scopes = {x["claim_scope"] for _, x in lst}
            scope = ("not recorded for these links" if scopes == {None}
                     else "; ".join(sorted(s for s in scopes if s)))
            prow.append(
                f"<tr><td>{a(S.href(st, trace=f'source:{sid}', pane='trace'), esc(src['title']))}</td>"
                f"<td>{esc(src['type'] or '')}</td>"
                f"<td>{', '.join(esc(p['role'] + ': ' + pretty(p['ingredient'])) for p, _ in lst)}</td>"
                f"<td>{esc(scope)}</td>"
                f"<td class='muted'>{esc(src['citation'] or '')}</td></tr>")
        out.append("<table><tr><th>Source</th><th>Type</th><th>Linked pairings</th>"
                   "<th>Claim scope</th><th>The source describes itself as</th></tr>"
                   + "".join(prow) + "</table>")
        out.append('<div class="muted">The last column is the source’s own description, not a '
                   "claim about these pairings. No claim scope is recorded on any pairing link, "
                   "so the link says only that the source was cited for the pairing.</div>")
    nos = [p for p in pairs if not p["evidence"]["sources"]]
    if nos:
        out.append('<div class="nr">&nbsp;no source recorded for: ' + ", ".join(
            esc(pretty(p["ingredient"])) + (" (experimental)" if p["knowledge"] == "experimental" else "")
            for p in nos) + "&nbsp;</div>")
    if not m["corpus_populated"]:
        out.append('<div class="muted">Recipe co-occurrence counts are 0 for every pairing in '
                   "the database: the column has not been backfilled. 0 does not mean the "
                   "pairing never occurs, so it is not shown as evidence.</div>")
    return "".join(out)


# ---------------------------------------------------------------------------
# C. Compare
# ---------------------------------------------------------------------------

def compare_rows(m: dict, st: dict, comps: list[str]) -> list[tuple[str, str, list[str], list[str]]]:
    """(group, label, html cells, plain keys for 'differs') per aligned row."""
    rows = []

    def add(group, label, cells, keys=None):
        rows.append((group, label, cells, keys if keys is not None else cells))

    S_ = [state_by(m, c) for c in comps]
    add("Identity", "From", [esc(s["from_label"]) for s in S_])
    add("Identity", "Technique", [esc(s["technique"]) for s in S_])
    add("Identity", "Step confidence", [esc(pretty(s["confidence"])) for s in S_])
    add("Sensory", "Flavour shift", [esc(s["flavour_shift"] or "") for s in S_])
    add("Sensory", "Texture shift", [esc(s["texture_shift"] or "") for s in S_])
    add("Sensory", "Risks", [esc(", ".join(s["risks"])) or "none recorded" for s in S_])
    add("Sensory", "Keeps · freezes · batch",
        [esc(f"{s['keeps_well']} · {'yes' if s['freezes_well'] else 'no'} · {s['batch_prep_value']}")
         for s in S_])
    roles = [r for r in m["roles"] if any(
        x["role"] == r for c in comps for x in of(m, c, ("need", "pairing")))]
    for role in roles:
        cells, keys = [], []
        for c in comps:
            td = matrix_cell(m, st, c, role)
            cells.append(td)
            keys.append(",".join(sorted(p["ingredient"] + p["knowledge"]
                                        for p in of(m, c, "pairing") if p["role"] == role))
                        + ("|need" if any(n["role"] == role for n in of(m, c, "need")) else ""))
        add("Needs and pairings", role, cells, keys)
    rcells, rkeys = [], []
    for c in comps:
        rs = of(m, c, "route_fit")
        rkeys.append(",".join(r["route_id"] for r in rs))
        rcells.append("<br>".join(route_link(st, r["route_id"], r["attrs"]["name"])
                                  + (f' <span class="muted">{r["attrs"]["required_on_hand"][0]}/'
                                     f'{r["attrs"]["required_on_hand"][1]} req. on hand</span>'
                                     if m["have"] else "") for r in rs)
                      or '<span class="nr">&nbsp;no route recorded&nbsp;</span>')
    add("Routes", "Flavour routes", rcells, rkeys)
    icells, ikeys = [], []
    for c in comps:
        ideas = of(m, c, "idea")
        ikeys.append(",".join(sorted(i["ingredient"] for i in ideas)))
        icells.append(", ".join(
            f'<span class="gen">{esc(pretty(i["ingredient"]))}</span>'
            + (' <span class="tested">✓ tasted</span>' if i["testing"]["status"] == "tested" else "")
            for i in ideas) or '<span class="nr">&nbsp;none generated&nbsp;</span>')
    add("Ideas", "Scout ideas", icells, ikeys)
    add("Evidence", "Step sources", [
        ", ".join(esc(x["title"]) for x in of(m, c, "transformation")[0]["evidence"]["sources"])
        or '<span class="nr">&nbsp;none&nbsp;</span>' for c in comps])
    pcells = []
    for c in comps:
        cur = [p for p in of(m, c, "pairing") if p["knowledge"] == "curated"]
        n = sum(1 for p in cur if p["evidence"]["sources"])
        titles = sorted({x["title"] for p in cur for x in p["evidence"]["sources"]})
        pcells.append(f"{n} of {len(cur)} curated pairings sourced"
                      + (f'<br><span class="muted">{esc(", ".join(titles))}</span>' if titles else ""))
    add("Evidence", "Pairing sources", pcells)
    add("Not recorded", "Gaps", [
        f'<span class="nr">&nbsp;{esc("; ".join(gaps(m, c)))}&nbsp;</span>' if gaps(m, c) else "—"
        for c in comps])
    return rows


def compare_html(m: dict, st: dict) -> str:
    comps = [c for c in st["cmp"] if state_by(m, c)]
    if len(comps) < 2:
        return ('<div class="r4"><div class="muted">Pin two or three rows with ☐ in the overview '
                f"to compare them. Pinned now: {len(comps)}.</div></div>")
    rows = compare_rows(m, st, comps)
    head = "".join(f"<th>{state_link(st, c)} " +
                   a(S.href(st, cmp=[x for x in st["cmp"] if x != c]), "✕", "Unpin") + "</th>"
                   for c in comps)
    body, last, n_diff = [], None, 0
    for group, label, cells, keys in rows:
        differs = len(set(keys)) > 1
        n_diff += differs
        if st["diff"] and not differs:
            continue
        if group != last:
            body.append(f'<tr><td colspan="{len(comps) + 2}" style="background:#faf8f4">'
                        f"<b>{esc(group)}</b></td></tr>")
            last = group
        tds = "".join(c if c.startswith("<td") else f"<td>{c}</td>" for c in cells)
        mark = '<td class="diff" title="values differ">≠</td>' if differs else "<td></td>"
        body.append(f'<tr class="{"" if differs else "same"}">{mark}<td>{esc(label)}</td>{tds}</tr>')
    toggle = a(S.href(st, diff=not st["diff"]),
               "show all rows" if st["diff"] else "show only differences")
    excl = [f"{pretty(c)} ({'; '.join(S.exclusion(m, c, st))})" for c in comps
            if S.exclusion(m, c, st)]
    ban = (f'<div class="banner">Excluded by the active filters: {esc(", ".join(excl))}. '
           "Kept because they are pinned.</div>") if excl else ""
    return (f'<div class="r4">{ban}<div class="muted">{n_diff} of {len(rows)} rows differ · '
            f'{toggle} · ≠ marks a difference</div>' + LEGEND +
            f'<table><tr><th></th><th></th>{head}</tr>' + "".join(body) + "</table></div>")


# ---------------------------------------------------------------------------
# D. Trace: one edge list drives both the graph and the table
# ---------------------------------------------------------------------------

TRACE_LEVELS = {1: "direct relationships", 2: "+ routes, ideas, experimental",
                3: "+ sources"}


def _node(kind: str, name: str) -> str:
    return f"{kind}:{name}"


def trace_edges(m: dict, st: dict) -> tuple[list[dict], dict[str, dict]]:
    """Edges {src, dst, relation, records: [rec], label} and nodes
    {id: {kind, name, label}} for the current trace focus and depth.

    One node per real entity: an ingredient appears once however many
    records (pairing, idea, route element) point at it."""
    f = S.trace_focus(st)
    edges: list[dict] = []
    nodes: dict[str, dict] = {}
    if not f:
        return edges, nodes
    kind, name = f
    depth = st["depth"]

    def node(k, n, label=None):
        nid = _node(k, n)
        if nid not in nodes:
            nodes[nid] = {"kind": k, "name": n, "label": label or pretty(n)}
        return nid

    def edge(a_, b_, relation, rec=None, label=""):
        key = (a_, b_, relation, rec["id"] if rec else "")
        if any((e["src"], e["dst"], e["relation"], e["key"]) == key for e in edges):
            return
        edges.append({"src": a_, "dst": b_, "relation": relation,
                      "records": [rec] if rec else [], "label": label, "key": key[3]})

    def state_out(comp):
        sid = node("state", comp)
        step = of(m, comp, "transformation")[0]
        if kind == "state":
            src = step["attrs"]["from"]
            edge(node("state" if step["attrs"]["chained"] else "ingredient", src), sid,
                 "becomes", step, state_by(m, comp)["technique"])
        for n in of(m, comp, "need"):
            rid = node("role", f"{comp}|{n['role']}", n["role"])
            edge(sid, rid, "needs", n, f"priority {n['attrs']['priority']}")
            pairs = [p for p in of(m, comp, "pairing") if p["role"] == n["role"]
                     and (p["knowledge"] == "curated" or depth >= 2)]
            for p in pairs:
                edge(rid, node("ingredient", p["ingredient"]), "filled by", p,
                     pretty(p["confidence"]["value"]))
            if n["coverage"] == "not recorded" and not pairs:
                edge(rid, node("gap", f"{comp}|{n['role']}", "(no curated pairing)"),
                     "not recorded", n)
        needed = {n["role"] for n in of(m, comp, "need")}
        for p in of(m, comp, "pairing"):        # pairings for a role not listed as a need
            if p["role"] in needed or (p["knowledge"] != "curated" and depth < 2):
                continue
            rid = node("role", f"{comp}|{p['role']}", f"{p['role']}\\n(not a listed need)")
            edge(sid, rid, "has pairing for", None, "")
            edge(rid, node("ingredient", p["ingredient"]), "filled by", p,
                 pretty(p["confidence"]["value"]))
        if depth >= 2:
            for r in of(m, comp, "route_fit"):
                rnode = node("route", r["route_id"], r["attrs"]["name"])
                edge(sid, rnode, "fits route", r, pretty(r["confidence"]["value"]))
                for e in of(m, comp, "route_element"):
                    if e["route_id"] == r["route_id"]:
                        edge(rnode, node("ingredient", e["ingredient"]), "uses", e,
                             e["optionality"])
            for i in of(m, comp, "idea"):
                edge(sid, node("ingredient", i["ingredient"]), "Scout idea", i,
                     pretty(i["confidence"]["value"]))
        if depth >= 3:
            for x in step["evidence"]["sources"]:
                edge(sid, node("source", str(x["source_id"]), x["title"]), "step backed by", step)
            for p in of(m, comp, "pairing"):
                for x in p["evidence"]["sources"]:
                    edge(node("ingredient", p["ingredient"]),
                         node("source", str(x["source_id"]), x["title"]),
                         "pairing backed by", p, pretty(comp))

    if kind == "state" and state_by(m, name):
        state_out(name)
    elif kind == "ingredient":
        iid = node("ingredient", name)
        for p in of(m, kind="pairing"):
            if p["ingredient"] == name and (p["knowledge"] == "curated" or depth >= 2):
                edge(node("state", p["state"]), iid, "paired (" + p["role"] + ")", p,
                     p["role"] + " · " + pretty(p["confidence"]["value"]))
        if depth >= 2:
            for e in of(m, kind="route_element"):
                if e["ingredient"] == name:
                    rnode = node("route", e["route_id"], e["attrs"]["route"])
                    edge(rnode, iid, "uses", e, e["optionality"])
                    fit = next(r for r in of(m, e["state"], "route_fit")
                               if r["route_id"] == e["route_id"])
                    edge(node("state", e["state"]), rnode, "fits route", fit)
            for i in of(m, kind="idea"):
                if i["ingredient"] == name:
                    edge(node("state", i["state"]), iid, "Scout idea", i,
                         pretty(i["confidence"]["value"]))
                elif i["attrs"]["replaces"] == name:
                    edge(node("state", i["state"]), iid, "idea replaces", i,
                         pretty(i["ingredient"]))
        if depth >= 3:
            for p in of(m, kind="pairing"):
                if p["ingredient"] == name:
                    for x in p["evidence"]["sources"]:
                        edge(node("state", p["state"]),
                             node("source", str(x["source_id"]), x["title"]),
                             "pairing backed by", p, p["role"])
    elif kind == "route":
        rnode = None
        for r in of(m, kind="route_fit"):
            if r["route_id"] == name:
                rnode = node("route", name, r["attrs"]["name"])
                edge(node("state", r["state"]), rnode, "fits route", r,
                     pretty(r["confidence"]["value"]))
        for e in of(m, kind="route_element"):
            if e["route_id"] == name:
                edge(rnode, node("ingredient", e["ingredient"]), "uses", e, e["optionality"])
        if depth >= 2 and rnode:
            els = {e["ingredient"] for e in of(m, kind="route_element") if e["route_id"] == name}
            fits = {r["state"] for r in of(m, kind="route_fit") if r["route_id"] == name}
            for p in of(m, kind="pairing"):
                if p["state"] in fits and p["ingredient"] in els:
                    edge(node("state", p["state"]), node("ingredient", p["ingredient"]),
                         "paired (" + p["role"] + ")", p, "separate pairing record")
    elif kind == "source" and name.isdigit():
        sid = int(name)
        src = m["sources"].get(sid)
        snode = node("source", name, src["title"] if src else f"source #{name}")
        for r in of(m, kind=("transformation", "pairing")):
            for x in r["evidence"]["sources"]:
                if x["source_id"] != sid:
                    continue
                if r["kind"] == "transformation":
                    edge(snode, node("state", r["state"]), "backs step", r,
                         x["claim_scope"] or "scope not recorded")
                else:
                    pn = node("pairing", r["id"], f"{pretty(r['state'])} · {r['role']} · "
                              f"{pretty(r['ingredient'])}")
                    edge(snode, pn, "backs pairing", r, x["claim_scope"] or "scope not recorded")
    return edges, nodes


def _node_label(m: dict, n: dict, recs: list[dict]) -> str:
    """An ingredient node's tags come ONLY from the records on the edges drawn
    to it in this trace, never from other preparations' records."""
    if n["kind"] != "ingredient":
        return n["label"]
    tags = []
    if any(r["knowledge"] == "experimental" for r in recs):
        tags.append("experimental")
    if any(r["kind"] == "idea" for r in recs):
        tags.append("idea")
    if any(r["kind"] == "idea" and r["testing"]["status"] == "tested" for r in recs):
        tags.append("tasted")
    if n["name"] in m["have"]:
        tags.insert(0, "on hand")
    return n["label"] + ("\\n" + " · ".join(tags) if tags else "")


def trace_dot(m: dict, st: dict) -> str:
    edges, nodes = trace_edges(m, st)
    f = S.trace_focus(st)
    focus_id = _node(*f) if f else ""
    if f and f[0] == "source":
        focus_id = _node("source", f[1])
    lines = ['digraph G {', 'rankdir=LR; bgcolor="transparent"; nodesep=0.12; ranksep=0.35; size="7.2,6";',
             'node [shape=box, style="rounded,filled", fillcolor="#ffffff", color="#9aa5b4", '
             'fontname="Helvetica", fontsize=11, margin="0.08,0.03"];',
             'edge [color="#7d8796", fontname="Helvetica", fontsize=9, fontcolor="#5b5f66"];']
    shapes = {"state": 'fillcolor="#eef2f7"', "role": 'shape=ellipse, fillcolor="#f6f4ef"',
              "route": 'shape=hexagon, fillcolor="#f1f6ee"', "source": 'shape=note, fillcolor="#f4f0fa"',
              "gap": 'style="rounded,dashed", color="#b8b3aa", fontcolor="#6b665d"',
              "pairing": 'fillcolor="#f4f0fa"'}
    for nid, n in nodes.items():
        recs = [r for e in edges if nid in (e["src"], e["dst"]) for r in e["records"]
                if r.get("ingredient") == n["name"]]
        attrs = [f'label="{_node_label(m, n, recs)}"', shapes.get(n["kind"], "")]
        if n["kind"] == "ingredient" and n["name"] in m["have"]:
            attrs.append('color="#2f8a4b", penwidth=2')
        if n["kind"] == "state" and S.exclusion(m, n["name"], st):
            attrs.append('fontcolor="#9a958c", color="#cfcac0"')
            attrs[0] = f'label="{n["label"]}\\n(excluded by filter)"'
        if nid == focus_id:
            attrs.append('penwidth=2.5, color="#1a4f8b"')
        if n["kind"] == "state":
            attrs.append(f'URL="{S.href(st, rec=n["name"], pane="detail")}", target="_self"')
        elif n["kind"] == "ingredient":
            attrs.append(f'URL="{S.href(st, trace="ingredient:" + n["name"])}", target="_self"')
        lines.append(f'"{nid}" [{", ".join(x for x in attrs if x)}];')
    for e in edges:
        r = e["records"][0] if e["records"] else {}
        style = []
        if r.get("knowledge") == "experimental":
            style.append('style=dashed, color="#b07d1a"')
        elif r.get("knowledge") == "generated":
            style.append('style=dashed, color="#b07d1a"')
            if r["testing"]["status"] == "tested":
                style.append('penwidth=2')
        elif e["relation"].endswith("backed by") or e["relation"].startswith("backs"):
            style.append('style=dotted, color="#8a78b0"')
        elif e["relation"] == "not recorded":
            style.append('style=dashed, color="#b8b3aa"')
        if r.get("optionality") in ("supporting", "finish"):
            style.append("style=dashed")
        lab = e["label"]
        if r.get("kind") == "idea" and r["testing"]["status"] == "tested":
            lab += " · tasted: " + r["testing"]["trials"][0]["verdict"]
        lines.append(f'"{e["src"]}" -> "{e["dst"]}" [label="{lab}", {", ".join(style)}];')
    lines.append("}")
    return "\n".join(lines)


def trace_table_html(m: dict, st: dict) -> str:
    edges, nodes = trace_edges(m, st)
    f = S.trace_focus(st)
    if not f:
        return ('<div class="r4 muted">Choose something to trace: ⇄ on an overview row, or any '
                "ingredient, route or source name in the fact sheet.</div>")
    lvl = '<div class="tabs">' + "".join(
        f'<span class="on">{i} {esc(t)}</span>' if i == st["depth"] else
        a(S.href(st, depth=i), f"{i} {esc(t)}") for i, t in TRACE_LEVELS.items()) + "</div>"

    def label(nid):
        n = nodes[nid]
        if n["kind"] == "state":
            return state_link(st, n["name"])
        if n["kind"] == "ingredient":
            return ing_link(st, n["name"])
        if n["kind"] == "route":
            return route_link(st, n["name"], n["label"])
        if n["kind"] == "source":
            return a(S.href(st, trace=f"source:{n['name']}"), esc(n["label"]))
        if n["kind"] == "pairing":
            r = next(x for x in m["records"] if x["id"] == n["name"])
            return state_link(st, r["state"]) + " · " + esc(r["role"]) + " · " + \
                ing_link(st, r["ingredient"])
        return esc(n["label"])

    rows = []
    for e in edges:
        r = e["records"][0] if e["records"] else None
        note = ""
        if r is not None:
            lk = linked(m, r)
            if lk:
                note = "linked by ids to: " + "; ".join(
                    ("Scout idea" if x["kind"] == "idea" else f"{x['knowledge']} pairing ({x['role']})")
                    for x in lk)
            if r["kind"] == "route_element":
                note = r["attrs"]["contribution"]
            if r["kind"] == "route_fit":
                note = r["attrs"]["fit_reason"] or ""
        ex = ""
        for nid in (e["src"], e["dst"]):
            n = nodes[nid]
            if n["kind"] == "state" and S.exclusion(m, n["name"], st):
                ex = f'<div class="why">{esc(pretty(n["name"]))} excluded by filter</div>'
        dims = ([knowledge_txt(r), conf_txt(r), avail_txt(r), sources_txt(st, r, scope=False),
                 testing_txt(r), opt_txt(r)] if r else [NA] * 6)
        rows.append([f"<td>{label(e['src'])}</td>", f"<td>{esc(e['relation'])}</td>",
                     f"<td>{label(e['dst'])}{ex}</td>"] + [f"<td>{d}</td>" for d in dims]
                    + [f'<td class="muted">{esc(note)}</td>' if note else f"<td>{NA}</td>"])
    # A dimension that is n/a on every row of this table is dropped: the
    # table then carries only the dimensions that apply to this focus.
    heads = ["From", "Relation", "To", "Knowledge", "Confidence", "Availability", "Sources",
             "Testing", "Optionality", "Note"]
    keep = [i for i in range(len(heads))
            if i < 3 or any(row[i] != f"<td>{NA}</td>" for row in rows)]
    dropped = [heads[i] for i in range(len(heads)) if i not in keep]
    title = f"<h3>Trace: {esc(_focus_label(m, f))}</h3>"
    back = ""
    if st["rec"]:
        back = (" · " + a(S.href(st, pane="detail"), f"back to {esc(pretty(st['rec']))}"))
    summary = (f'<div class="muted">{len(edges)} relationships · {len(nodes)} entities, '
               f'each shown once{back}</div>')
    if not edges:
        return ('<div class="r4">' + title + lvl +
                '<div class="nr">&nbsp;nothing recorded for this focus within '
                f'{esc(pretty(m["ingredient"]))} at this step&nbsp;</div></div>')
    note = (f'<div class="muted">Not applicable to any row here: {esc(", ".join(dropped))}.</div>'
            if dropped else "")
    return ('<div class="r4">' + title + lvl + summary + note +
            "<table><tr>" + "".join(f"<th>{heads[i]}</th>" for i in keep) + "</tr>" +
            "".join("<tr>" + "".join(row[i] for i in keep) + "</tr>" for row in rows) +
            "</table></div>")


def tabs_html(m: dict, st: dict, current: str) -> str:
    labels = {"detail": "Detail" + (f": {pretty(st['rec'])}" if st["rec"] else ""),
              "compare": f"Compare ({len(st['cmp'])})",
              "trace": "Trace" + (f": {_focus_label(m, S.trace_focus(st))}"
                                  if S.trace_focus(st) else "")}
    return '<div class="r4"><div class="tabs">' + "".join(
        f'<span class="on">{esc(t)}</span>' if k == current else a(S.href(st, pane=k), esc(t))
        for k, t in labels.items()) + "</div></div>"
