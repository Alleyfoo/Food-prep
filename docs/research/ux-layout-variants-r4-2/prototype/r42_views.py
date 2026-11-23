"""R4.2 layout variants on the R4.1 workspace (data-layout validation).

R4.1's renderers, plus two facilitator-set encodings that change only how
the same facts are drawn:
    ov=a     overview: compact code (R4 dots, bare counts, legend; names in tooltips)
    ov=b     overview: labelled summary (R4.1, default)
    ov=c     overview: named roles - one token per needed role with its status
    sheet=dense  fact sheet: same facts, tighter type, 4-column attribute grid,
                 routes in one table, shorter ideas note

R4.1 docstring follows.

R4.1 integrated workspace: the same four representations, read more easily.

Forked from R4 (docs/research/ux-integrated-r4/prototype/r4_views.py). The
model (R4's r4_model), the URL context and the pane architecture are R4's.
What changed is presentation only (see ../layout-changes.md):

    Overview  labelled sentences instead of dot codes and bare counts; text row
              actions; facts, hypotheses and gaps in separate columns; sticky
              header; one marker vocabulary for detail / compare / trace
    Detail    section index; bands (attributes, relationships, evidence and
              testing, gaps); pairings grouped by role; claim scope stated once
              when it is uniformly missing; tastings apart from untested ideas;
              missing knowledge apart from missing ingredients
    Compare   lettered records (A, B, C) everywhere; plain-language cells;
              "differs" instead of ≠; not-a-need vs not-recorded in words
    Trace     table first; graph collapsed above GRAPH_LIMIT relationships;
              rows grouped by their From entity; names never broken mid-word
    Matrix    words instead of glyphs; one pairing per line; sticky legend

Every renderer is still a pure function of (model, state).
"""
from __future__ import annotations

from html import escape as esc
from typing import Any

import r42_palette as P
import r42_state as S
from r4_model import (CONFIDENCE_FIELD_LABEL, KNOWLEDGE_LABEL, gaps, linked, of,
                      pretty, shared_gaps, state_by)

GRAPH_LIMIT = 20   # relationships; above this the graph is collapsed by default

# One colour per concept, never reused for another:
#   inspected record  amber background      (Detail)
#   compare set       blue left edge + A/B/C (Compare)
#   trace             violet                 (Trace)
#   filter exclusion  grey text + reason
#   on hand           green text + the words "on hand"
#   experimental/idea brown italic + the word "experimental" / "idea"
#   not recorded      hatched + the words "not recorded"
CSS = """
<style>
.r4 {font-size:14px; line-height:1.4; color:var(--ink)}
.r4 table.ov {font-size:13px}
.r4 a {color:var(--link); text-decoration:none} .r4 a:hover {text-decoration:underline}
.r4 table {border-collapse:collapse; width:100%; margin:4px 0 12px}
.r4 th {text-align:left; font-weight:600; background:var(--fill); border-bottom:2px solid var(--line);
        padding:4px 7px; font-size:13px; vertical-align:bottom}
.r4 td {border-bottom:1px solid var(--fill-2); padding:4px 7px; vertical-align:top;
        overflow-wrap:normal; word-break:normal; hyphens:manual}
.r4 thead {position:sticky; top:0; z-index:3; background:var(--fill); box-shadow:0 1px 0 var(--line)}
.r4 thead th {background:var(--fill)}
.r4 thead tr.legendrow th {font-weight:400; border-bottom:1px solid var(--line); background:var(--fill-soft)}
.r4 .nm, .r4 table.trace td a {white-space:nowrap}
.r4 tr.excluded td {color:var(--ink-3); background:var(--fill)}
.r4 tr.excluded td a {color:var(--link)}
.r4 tr.sel td {background:var(--sel-subtle)}
.r4 tr.pinned td:first-child {box-shadow:inset 4px 0 0 var(--cmp-base)}
.r4 tr.same td {color:var(--ink-3)}
.r4 .why {font-size:12px; color:var(--ink-3)}
.r4 .muted {color:var(--ink-3); font-size:12px}
.r4 .nr {background:repeating-linear-gradient(45deg,var(--fill-soft),var(--fill-soft) 4px,var(--fill) 4px,var(--fill) 8px);
         color:var(--ink-3); font-size:12px}
.r4 tr.sel td.nr {background:repeating-linear-gradient(45deg,var(--sel-subtle),var(--sel-subtle) 4px,var(--sel-subtle2) 4px,var(--sel-subtle2) 8px)}
.r4 .na {color:var(--ink-3); font-size:12px}
.r4 .exp {font-style:italic; color:var(--hyp-text)}
.r4 .gen {font-style:italic; color:var(--hyp-text)}
.r4 .have {color:var(--have-base); font-weight:600}
.r4 .lbl {font-size:11px; color:var(--ink-3); margin-left:3px}
.r4 .lbl.have {color:var(--have-base); font-weight:400}
.r4 .tested {color:var(--hyp-deep); font-weight:600}
.r4 .ctx {background:var(--fill-soft); border:1px solid var(--line); border-radius:6px; padding:6px 10px;
          margin:0 0 8px; font-size:13px}
.r4 .ctx b {font-weight:600; color:var(--ink-2)}
.r4 .chip {display:inline-block; border:1px solid var(--line-strong); border-radius:10px; padding:0 7px;
           margin:1px 3px 1px 0; background:var(--surface); white-space:nowrap}
.r4 .chip a {color:var(--diff-base); margin-left:4px}
.r4 .chip.c-sel {border-color:var(--sel-border); background:var(--sel-subtle)}
.r4 .chip.c-cmp {border-color:var(--cmp-border); background:var(--cmp-subtle)}
.r4 .chip.c-trace {border-color:var(--trace-border); background:var(--trace-subtle)}
.r4 .tag {display:inline-block; font-size:11px; line-height:15px; border-radius:3px; padding:0 4px;
          margin:1px 3px 0 0; white-space:nowrap; border:1px solid}
.r4 .t-sel {background:var(--sel-subtle); border-color:var(--sel-border); color:var(--sel-base)}
.r4 .t-cmp {background:var(--cmp-subtle); border-color:var(--cmp-border); color:var(--cmp-base); font-weight:600}
.r4 .t-trace {background:var(--trace-subtle); border-color:var(--trace-border); color:var(--trace-base)}
.r4 .t-diff {background:var(--diff-subtle); border-color:var(--diff-border); color:var(--diff-base)}
.r4 .acts {font-size:12px; margin-top:2px}
.r4 .acts a {margin-right:8px}
.r4 .tabs a, .r4 .tabs span {display:inline-block; padding:3px 12px; margin-right:4px;
          border:1px solid var(--line); border-bottom:none; border-radius:6px 6px 0 0; background:var(--fill)}
.r4 .tabs span.on {background:var(--surface); font-weight:600}
.r4 .tabs {border-bottom:1px solid var(--line); margin:0 0 8px}
.r4 .tabs .k-detail {border-top:3px solid var(--sel-mid)} .r4 .tabs .k-compare {border-top:3px solid var(--cmp-base)}
.r4 .tabs .k-trace {border-top:3px solid var(--trace-base)}
.r4 h3 {margin:2px 0 6px; font-size:18px}
.r4 h4 {clear:both; margin:12px 0 3px; font-size:14px; color:var(--ink-2); scroll-margin-top:64px}
.r4 h4 .n {color:var(--ink-3); font-weight:400; margin-right:4px}
.r4 h5 {margin:8px 0 2px; font-size:13px; color:var(--ink-2)}
.r4 .band {margin:16px 0 0; padding:2px 0; border-bottom:2px solid var(--line); font-size:12px;
           letter-spacing:.04em; text-transform:uppercase; color:var(--ink-3); font-weight:600}
.r4 .index {position:sticky; top:0; z-index:4; background:var(--surface); border:1px solid var(--line);
            border-radius:6px; padding:4px 8px; margin:0 0 6px; font-size:12px}
.r4 .index b {color:var(--ink-3); font-weight:600; margin-right:4px}
.r4 .index a {margin-right:9px; white-space:nowrap}
.r4 .index .grp {display:inline-block; margin-right:10px}
.r4 dl {margin:0; display:grid; grid-template-columns:170px 1fr; gap:2px 10px}
.r4 dt {font-weight:600; color:var(--ink-2)} .r4 dd {margin:0}
.r4 .sub {font-size:12px; color:var(--ink-3)}
.r4 .ideas {border:1px dashed var(--hyp-line); border-radius:6px; padding:4px 10px; background:var(--hyp-fill)}
.r4 .gapbox {border:1px solid var(--line); border-radius:6px; padding:4px 10px;
             background:repeating-linear-gradient(45deg,var(--fill-soft),var(--fill-soft) 6px,var(--fill) 6px,var(--fill) 12px)}
.r4 .stockbox {border:1px solid var(--have-border); border-radius:6px; padding:4px 10px; background:var(--have-faint)}
.r4 .banner {background:var(--note-fill); border:1px solid var(--note-line); border-radius:6px; padding:4px 10px;
             margin:0 0 6px; font-size:13px}
.r4 .legend {font-size:12px; color:var(--ink-3); margin:2px 0 6px}
.r4 .num {text-align:right; font-variant-numeric:tabular-nums}
.r4 tr.grp td {background:var(--fill-soft); font-weight:600; color:var(--ink-2)}
.r4 tr.grp td .muted {font-weight:400}
.r4 details summary {cursor:pointer; color:var(--link); font-size:12px}
.r4 .tscroll {overflow-x:auto; max-width:100%}
.r4 .tscroll table.trace {width:auto; min-width:100%}
.r4 table.trace td.rep a {color:var(--ink-3)}
.r4 table.trace td.src {min-width:12em}
.r4 .dots {letter-spacing:1px; font-size:13px}
.r4 .rc {display:inline-block; white-space:normal; border:1px solid var(--line); border-radius:3px;
         padding:0 4px; margin:1px 2px 1px 0; font-size:12px; line-height:16px; background:var(--surface)}
.r4 .rc-have {border-color:var(--have-border); color:var(--have-base); background:var(--have-subtle); font-weight:600}
.r4 .rc-nr {background:repeating-linear-gradient(45deg,var(--fill-soft),var(--fill-soft) 4px,var(--fill) 4px,var(--fill) 8px);
            color:var(--ink-3)}
.r4 .rc-exp {border-color:var(--hyp-border); color:var(--hyp-text); font-style:italic; background:var(--hyp-fill)}
.r4 .rc-tested {border-color:var(--hyp-line); color:var(--hyp-deep); font-weight:600; background:var(--hyp-fill)}
.r4.dense {font-size:13px; line-height:1.3}
.r4.dense td, .r4.dense th {padding:2px 5px}
.r4.dense table {margin:2px 0 6px}
.r4.dense h4 {margin:7px 0 2px}
.r4.dense h5 {margin:4px 0 1px}
.r4.dense .band {margin:9px 0 0}
.r4.dense dl.dl4 {grid-template-columns:110px 1fr 110px 1fr; gap:1px 8px}
.r4.dense dl.dl4 dd.w {grid-column:2 / span 3}
.r4.dense dl.dl4 dt.w {grid-column:1}
.r4 table.ov.sum td:first-child {min-width:15em}
.r4 .obs {font-size:12px; color:var(--ink-2); margin-top:2px}
.r4 .graphnote {border:1px solid var(--line); border-radius:6px; background:var(--fill-soft); padding:6px 10px;
                margin:4px 0 8px; font-size:13px}
</style>
"""


def css(pal: str) -> str:
    """The workspace CSS with the colour world's tokens (r42_palette)."""
    return f"<style>{P.css_vars(pal)}</style>" + CSS


NA = '<span class="na">n/a</span>'


def a(href: str, text: str, title: str | None = None) -> str:
    t = f' title="{esc(title)}"' if title else ""
    return f'<a href="{esc(href)}" target="_self"{t}>{text}</a>'


def _names(xs: list[str]) -> str:
    return ", ".join(pretty(x) for x in xs)


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
        return 'not graded <span class="muted">(recorded as “experimental”)</span>'
    val = esc(pretty(c["value"]) or "not recorded")
    if with_field or c["field"] != "confidence":
        return f'{val} <span class="muted">({CONFIDENCE_FIELD_LABEL[c["field"]]})</span>'
    return val


def avail_txt(r: dict) -> str:
    v = r.get("availability")
    if v is None:
        return NA
    return '<span class="have">on hand</span>' if v == "on hand" else \
        '<span class="muted">not on hand</span>'


def _scope_uniform_missing(recs: list[dict]) -> bool:
    links = [x for r in recs for x in r["evidence"]["sources"]]
    return bool(links) and not any(x["claim_scope"] for x in links)


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
            bit += ('<br><span class="muted">claim scope: </span>' + esc(s["claim_scope"])
                    if s["claim_scope"] else
                    '<br><span class="muted">claim scope: not recorded</span>')
        out.append(bit)
    return "<br>".join(out)


def testing_txt(r: dict) -> str:
    t = r.get("testing")
    if not t:
        return NA
    if t["status"] == "untested":
        return '<span class="muted">not tasted</span>'
    return "<br>".join(f'<span class="tested">tasted: {esc(x["verdict"])}</span> '
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


# --- shared selection markers (one vocabulary for every pane) --------------

def traced_states(m: dict, st: dict) -> set[str]:
    """Prepared ingredients that appear in the current trace."""
    if not S.trace_focus(st):
        return set()
    _, nodes = trace_edges(m, st)
    return {n["name"] for n in nodes.values() if n["kind"] == "state"}


def markers(m: dict, st: dict, comp: str, traced: set[str] | None = None) -> list[str]:
    """Tags saying which shared selections a prepared ingredient belongs to."""
    out = []
    if comp == st["rec"]:
        out.append('<span class="tag t-sel" title="Shown in the Detail pane">in detail</span>')
    if comp in st["cmp"]:
        out.append(f'<span class="tag t-cmp" title="In the compare set">compare '
                   f'{S.compare_letter(st, comp)}</span>')
    f = S.trace_focus(st)
    if f and f == ("state", comp):
        out.append('<span class="tag t-trace" title="The traced entity">traced</span>')
    elif traced is not None and comp in traced:
        out.append(f'<span class="tag t-trace" title="Appears in the trace of '
                   f'{esc(_focus_label(m, f))}">in trace</span>')
    return out


# --- the needs x roles matrix cell (plain words, no glyph code) ------------

def matrix_cell(m: dict, st: dict, comp: str, role: str, sel: bool = False) -> str:
    """One cell: each pairing on its own line, its status in words.

    hatched + "needed, no curated pairing recorded"  = a recorded need, nothing curated
    empty (class "na")                               = the role is not a listed need
    """
    need = next((r for r in of(m, comp, "need") if r["role"] == role), None)
    pairs = [p for p in of(m, comp, "pairing") if p["role"] == role]
    if need is None and not pairs:
        return '<td class="na" title="not a listed need for this preparation"></td>'
    lines = []
    for p in pairs:
        nm = esc(pretty(p["ingredient"]))
        if p["knowledge"] == "experimental":
            txt = f'<span class="exp">{nm}</span>'
            lab = '<span class="lbl">experimental</span>'
        else:
            txt = f'<span class="have">{nm}</span>' if p["availability"] == "on hand" else nm
            lab = ""
        if p["availability"] == "on hand":
            lab += '<span class="lbl have">on hand</span>'
        lines.append(a(S.href(st, trace=f"ingredient:{p['ingredient']}", pane="trace"),
                       txt, f"Trace {pretty(p['ingredient'])}") + lab)
    if need is None:
        lines.append('<span class="na">not a listed need</span>')
    elif need["coverage"] != "recorded":
        lines.append("needed, no curated pairing recorded")
        return '<td class="nr">' + "<br>".join(lines) + "</td>"
    return "<td>" + "<br>".join(lines) + "</td>"


def compare_cell(m: dict, st: dict, comp: str, role: str) -> str:
    """Compare uses the matrix cell, but says 'not a listed need' in words,
    because in an aligned comparison an empty cell reads as missing data."""
    td = matrix_cell(m, st, comp, role)
    if td.startswith('<td class="na"'):
        return '<td class="na">not a listed need</td>'
    return td


# ---------------------------------------------------------------------------
# context bar: the whole investigation context, each part removable
# ---------------------------------------------------------------------------

def context_bar(m: dict, st: dict) -> str:
    def chip(label: str, remove: str | None, cls: str = "") -> str:
        x = a(remove, "✕", "Remove") if remove else ""
        return f'<span class="chip {cls}">{label}{x}</span>'

    parts = [f"<b>Ingredient</b> {chip(esc(pretty(m['ingredient'])), None)}"]
    parts.append("<b>On hand</b> " + ("".join(
        chip(esc(pretty(h)), S.href(st, have=[x for x in st["have"] if x != h]))
        for h in st["have"]) or '<span class="muted">nothing entered · availability not '
                                'assessed</span>'))
    flt = S.active_filters(st)
    if flt:
        n_ex = sum(1 for s in m["states"] if S.exclusion(m, s["component"], st))
        parts.append("<b>Filters</b> " + "".join(
            chip(esc(lab), S.href(st, **{k: [x for x in st[k] if x != v]}))
            for k, v, lab in flt) + f'<span class="muted">{n_ex} of {len(m["states"])} rows '
            f'excluded</span> ' + a(S.href(st, has=[], paired=[], gap=[]), "clear filters"))
    sel = []
    if st["rec"]:
        sel.append("<b>In detail</b> " + chip(esc(pretty(st["rec"])), S.href(st, rec=""), "c-sel"))
    if st["cmp"]:
        sel.append("<b>Compare</b> " + "".join(
            chip(f"{S.compare_letter(st, c)} · {esc(pretty(c))}",
                 S.href(st, cmp=[x for x in st["cmp"] if x != c]), "c-cmp")
            for c in st["cmp"]))
    f = S.trace_focus(st)
    if f:
        sel.append("<b>Tracing</b> " + chip(esc(_focus_label(m, f)), S.href(st, trace=""),
                                            "c-trace"))
    reset = a(S.href({**S.DEFAULTS, "ingredient": m["ingredient"],
                      **{k: st[k] for k in S.VARIANT}}), "reset all")   # keeps the condition
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

def roles_summary(m: dict, comp: str) -> str:
    """Recorded culinary knowledge for one row, in words: how many curated
    pairings, how many needed roles they cover, and (only when something is
    entered) which are on hand. The column header says "Curated pairings"."""
    needs = of(m, comp, "need")
    pairs = [p for p in of(m, comp, "pairing") if p["knowledge"] == "curated"]
    n, rec = len(needs), sum(1 for x in needs if x["coverage"] == "recorded")
    cnt = f"{len(pairs)} pairing{'' if len(pairs) == 1 else 's'}" if pairs else "none"
    if not n:
        cov = '<span class="muted">no needed roles recorded</span>'
    elif rec == n:
        cov = f"all {n} needed roles covered"
    else:
        cov = f"{rec} of {n} needed roles covered"
    out = [f"{cnt} · {cov}"]
    if m["have"]:
        on = [p for p in pairs if p["availability"] == "on hand"]
        out.append('<span class="have">on hand: ' + esc(", ".join(
            f"{pretty(p['ingredient'])} ({p['role']})" for p in on)) + "</span>" if on else
            '<span class="muted">none on hand</span>')
    return "<br>".join(out)


def route_summary(m: dict, st: dict, comp: str) -> str:
    out = []
    for r in of(m, comp, "route_fit"):
        line = route_link(st, r["route_id"], r["attrs"]["name"])
        if m["have"]:
            req = [e for e in of(m, comp, "route_element")
                   if e["route_id"] == r["route_id"] and e["optionality"] == "required"]
            miss = [e["ingredient"] for e in req if e["availability"] != "on hand"]
            line += ('<br><span class="lbl have">all required on hand</span>' if not miss else
                     f'<br><span class="lbl">not on hand: {esc(_names(miss))}</span>')
        out.append(line)
    return "<br>".join(out)


def hypotheses_summary(m: dict, comp: str) -> str:
    """Experimental pairings, Scout ideas and tastings: never mixed with the
    curated facts in the roles column."""
    exp = [p for p in of(m, comp, "pairing") if p["knowledge"] == "experimental"]
    ideas = of(m, comp, "idea")
    out = []
    if exp:
        out.append('<span class="exp">experimental pairing: ' + esc(", ".join(
            f"{pretty(p['ingredient'])} ({p['role']})" for p in exp)) + "</span>")
    if ideas:
        tasted = [i for i in ideas if i["testing"]["status"] == "tested"]
        out.append(f"{len(ideas)} Scout idea{'' if len(ideas) == 1 else 's'}"
                   + ("" if tasted else ", none tasted"))
        for i in tasted:
            v = i["testing"]["trials"][0]
            out.append(f'<span class="tested">tasted: {esc(pretty(i["ingredient"]))}, '
                       f'{esc(v["verdict"])}</span>')
    return "<br>".join(out) or '<span class="muted">none recorded</span>'


def overview_html(m: dict, st: dict) -> str:
    cols = st["cols"]
    common = shared_gaps(m)
    traced = traced_states(m, st)
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
        pin_tip = ("remove from compare" if comp in st["cmp"] else
                   f"compare with {pretty(st['rec'])}"
                   if len(change["cmp"]) == 2 and not st["cmp"] else "add to compare")
        # the matrix needs every pixel: short labels there, the full one as a tooltip
        pin_txt = pin_tip if cols != "matrix" else (
            "remove" if comp in st["cmp"] else "compare")
        acts = (f'<div class="acts">{a(S.href(st, **change), esc(pin_txt), pin_tip)}'
                + a(S.href(st, trace=f"state:{comp}", pane="trace"), "trace",
                    "Trace its relationships") + "</div>")
        tags = markers(m, st, comp, traced)
        name = (f'<span class="nm">{state_link(st, comp)}</span>'
                + (f'<div class="sub">{esc(s["from_label"])} → {esc(s["technique"])} · '
                   f'confidence {esc(pretty(s["confidence"]))}</div>'
                   if cols == "summary" else "")
                + (f'<div class="why">excluded: {esc("; ".join(why))}</div>' if why else "")
                + acts.replace('<div class="acts">', '<div class="acts">' + "".join(tags), 1))
        cells = [f"<td>{name}</td>"]
        cells += _overview_cells(m, st, s, cols, common, comp == st["rec"])
        rows.append(f'<tr class="{cls}">' + "".join(cells) + "</tr>")
    hdr = ["Prepared ingredient"] + _overview_headers(m, cols, common, st.get("ov", "b"))
    flt = S.active_filters(st)
    count = (f'<div class="muted">{n_match} of {len(m["states"])} match the filters'
             + (" · " + a(S.href(st, hide=not st["hide"]),
                          "show excluded" if st["hide"] else "hide excluded")
                if n_match < len(m["states"]) else "") + "</div>") if flt else ""
    banner = (f'<div class="banner">For every {esc(pretty(m["ingredient"]))} preparation: '
              + esc("; ".join(common)) + ". Not repeated in the rows.</div>") if common else ""
    legend = _legend(cols, st.get("ov", "b"))
    leg = (f'<tr class="legendrow"><th colspan="{len(hdr)}">{legend}</th></tr>'
           if legend else "")
    sum_cls = " sum" if cols == "summary" else ""   # same name-column width in A, B, C
    return (head + banner + count + f'<table class="ov{sum_cls}"><thead>' + leg + "<tr>" +
            "".join(f"<th>{esc(h)}</th>" for h in hdr) + "</tr></thead><tbody>" +
            "".join(rows) + "</tbody></table>")


def _legend(cols: str, ov: str = "b") -> str:
    if cols == "summary" and ov == "a":
        return ('<span class="legend">Needed roles: ● curated pairing on hand · ◐ curated pairing '
                'recorded · ○ no curated pairing; x/y = needed roles with a curated pairing. '
                'Routes: x/y = required elements on hand. Hypotheses: ◇ experimental pairings · '
                'Scout ideas · ✓ tasted. Hover a cell for names.</span>')
    if cols == "matrix":
        return ('<span class="legend">Each cell lists the pairings recorded for that role, '
                'one per line. <span class="nr">&nbsp;Hatched&nbsp;</span> = the role is needed '
                'but no curated pairing is recorded. Empty = the role is not a listed need for '
                'that preparation.</span>')
    return ""


# ---------------------------------------------------------------------------
# R4.2 overview encodings. Same facts per row in every variant; only the
# encoding differs. B (labelled summary) is R4.1's roles_summary /
# route_summary / hypotheses_summary.
# ---------------------------------------------------------------------------

def _tip(xs: list[str]) -> str:
    return esc("; ".join(xs))


def roles_code(m: dict, comp: str) -> str:
    """A: R4's compact code. One dot per needed role and a bare count; the
    names are only in the tooltip (as in R4)."""
    needs = of(m, comp, "need")
    pairs = [p for p in of(m, comp, "pairing") if p["knowledge"] == "curated"]
    if not needs:
        return '<span class="muted">none recorded</span>'
    dots, tip = [], []
    for n in needs:
        cook = [p for p in pairs if p["role"] == n["role"]]
        on = [p for p in cook if p["availability"] == "on hand"]
        if on:
            dots.append("●"); tip.append(f"{n['role']}: on hand ({_names([p['ingredient'] for p in on])})")
        elif cook:
            dots.append("◐"); tip.append(f"{n['role']}: {_names([p['ingredient'] for p in cook])}")
        else:
            dots.append("○"); tip.append(f"{n['role']}: no curated pairing")
    rec = sum(1 for n in needs if n["coverage"] == "recorded")
    return (f'<span class="dots" title="{_tip(tip)}">{"".join(dots)}</span> '
            f'<span class="muted">{rec}/{len(needs)}</span>')


def route_code(m: dict, st: dict, comp: str) -> str:
    out = []
    for r in of(m, comp, "route_fit"):
        line = route_link(st, r["route_id"], r["attrs"]["name"])
        if m["have"]:
            got, need = r["attrs"]["required_on_hand"]
            miss = [e["ingredient"] for e in of(m, comp, "route_element")
                    if e["route_id"] == r["route_id"] and e["optionality"] == "required"
                    and e["availability"] != "on hand"]
            line += (f' <span class="muted" title="not on hand: {_tip([_names(miss)]) or "none"}">'
                     f"{got}/{need}</span>")
        out.append(line)
    return "<br>".join(out)


def hypotheses_code(m: dict, comp: str) -> str:
    exp = [p for p in of(m, comp, "pairing") if p["knowledge"] == "experimental"]
    ideas = of(m, comp, "idea")
    tasted = [i for i in ideas if i["testing"]["status"] == "tested"]
    if not exp and not ideas:
        return '<span class="muted">—</span>'
    tip = ([f"experimental: {pretty(p['ingredient'])} ({p['role']})" for p in exp]
           + [f"tasted: {pretty(i['ingredient'])}, {i['testing']['trials'][0]['verdict']}"
              for i in tasted])
    bits = []
    if exp:
        bits.append(f'<span class="exp">◇{len(exp)}</span>')
    bits.append(f"{len(ideas)}")
    if tasted:
        bits.append(f'<span class="tested">✓{len(tasted)}</span>')
    return f'<span title="{_tip(tip)}">' + " · ".join(bits) + "</span>"


def _chip(text: str, cls: str = "") -> str:
    return f'<span class="rc {cls}">{text}</span>'


def roles_named(m: dict, comp: str) -> str:
    """C: one short token per needed role, its status in a word or a name:
    'fat' (curated pairing recorded), 'acid: lemon' (on hand, green),
    'herb: not recorded' (hatched)."""
    needs = of(m, comp, "need")
    pairs = [p for p in of(m, comp, "pairing") if p["knowledge"] == "curated"]
    if not needs:
        return '<span class="muted">no needed roles recorded</span>'
    out = []
    for n in needs:
        cook = [p for p in pairs if p["role"] == n["role"]]
        on = [p for p in cook if p["availability"] == "on hand"]
        if on:
            out.append(_chip(f"{esc(n['role'])}: {esc(_names([p['ingredient'] for p in on]))}",
                             "rc-have"))
        elif cook:
            out.append(_chip(esc(n["role"])))
        else:
            out.append(_chip(f"{esc(n['role'])}: not recorded", "rc-nr"))
    return " ".join(out)


def route_named(m: dict, st: dict, comp: str) -> str:
    out = []
    for r in of(m, comp, "route_fit"):
        line = route_link(st, r["route_id"], r["attrs"]["name"])
        if m["have"]:
            miss = [e["ingredient"] for e in of(m, comp, "route_element")
                    if e["route_id"] == r["route_id"] and e["optionality"] == "required"
                    and e["availability"] != "on hand"]
            line += (' <span class="lbl have">all on hand</span>' if not miss else
                     f' <span class="lbl">{esc(_names(miss))} not on hand</span>')
        out.append(line)
    return "<br>".join(out)


def hypotheses_named(m: dict, comp: str) -> str:
    exp = [p for p in of(m, comp, "pairing") if p["knowledge"] == "experimental"]
    ideas = of(m, comp, "idea")
    tasted = [i for i in ideas if i["testing"]["status"] == "tested"]
    out = [_chip(f"experimental: {esc(pretty(p['ingredient']))}", "rc-exp") for p in exp]
    if ideas:
        out.append(_chip(f"{len(ideas)} idea{'' if len(ideas) == 1 else 's'}"))
    out += [_chip(f"tasted: {esc(pretty(i['ingredient']))}, "
                  f"{esc(i['testing']['trials'][0]['verdict'])}", "rc-tested") for i in tasted]
    return " ".join(out) or '<span class="muted">none recorded</span>'


def route_summary_b(m: dict, st: dict, comp: str) -> str:
    return route_summary(m, st, comp)


def _overview_headers(m: dict, cols: str, common: list[str] = (), ov: str = "b") -> list[str]:
    if cols == "sensory":
        return ["Flavour shift", "Texture shift", "Risks", "Keeps · freezes · batch"]
    if cols == "matrix":
        return [r.replace("_", " ") for r in m["roles"]]
    if cols == "evidence":
        return ["Step sources", "Pairing sources", "Pairings without a source",
                "Claim scope on pairing sources"]
    first = {"a": "Needs", "c": "Needed roles"}.get(ov, "Curated pairings")
    hyp = {"a": "Hypotheses"}.get(ov, "Hypotheses and tastings")
    if "no flavour route" in common:      # stated once in the banner; the column would be empty
        return [first, hyp, "Not recorded"]
    return [first, "Flavour routes", hyp, "Not recorded"]


def _overview_cells(m, st, s, cols, common, sel) -> list[str]:
    comp = s["component"]
    pairs = of(m, comp, "pairing")
    curated = [p for p in pairs if p["knowledge"] == "curated"]
    step = of(m, comp, "transformation")[0]
    if cols == "sensory":
        kfb = " · ".join([f"keeps {s['keeps_well'] or 'not recorded'}",
                          "freezes" if s["freezes_well"] else "doesn't freeze",
                          f"batch value {s['batch_prep_value'] or 'not recorded'}"])
        return [f"<td>{esc(s['flavour_shift'] or '')}</td>",
                f"<td>{esc(s['texture_shift'] or '')}</td>",
                f"<td>{esc(', '.join(s['risks'])) or '<span class=muted>none recorded</span>'}</td>",
                f"<td>{esc(kfb)}</td>"]
    if cols == "matrix":
        return [matrix_cell(m, st, comp, role, sel) for role in m["roles"]]
    if cols == "evidence":
        stepsrc = "<br>".join(
            esc(x["title"]) + (' <span class="muted">(claim scope recorded)</span>'
                               if x["claim_scope"] else
                               ' <span class="muted">(no claim scope)</span>')
            for x in step["evidence"]["sources"]) or '<span class="nr">&nbsp;none recorded&nbsp;</span>'
        tally: dict[str, int] = {}
        for p in curated:
            for x in p["evidence"]["sources"]:
                tally[x["title"]] = tally.get(x["title"], 0) + 1
        psrc = "<br>".join(f"{esc(t)} <span class=muted>({n} pairing{'' if n == 1 else 's'})</span>"
                           for t, n in sorted(tally.items())) or \
            '<span class="nr">&nbsp;none recorded&nbsp;</span>'
        nos = [p for p in pairs if not p["evidence"]["sources"]]
        nos_txt = ", ".join(
            f'<span class="{"exp" if p["knowledge"] == "experimental" else ""}">'
            f'{esc(pretty(p["ingredient"]))}'
            + (" (experimental)" if p["knowledge"] == "experimental" else "") + "</span>"
            for p in nos) or '<span class="muted">none</span>'
        scoped = sum(1 for p in pairs for x in p["evidence"]["sources"] if x["claim_scope"])
        links = sum(len(p["evidence"]["sources"]) for p in pairs)
        scope = (f"recorded on {scoped} of {links} links" if scoped else
                 f'<span class="nr">&nbsp;not recorded on any of {links} links&nbsp;</span>'
                 if links else '<span class="muted">no source links</span>')
        return [f"<td>{stepsrc}</td>", f"<td>{psrc}</td>", f'<td class="wrap">{nos_txt}</td>',
                f"<td>{scope}</td>"]
    ov = st.get("ov", "b")
    roles_f, route_f, hyp_f = {"a": (roles_code, route_code, hypotheses_code),
                               "c": (roles_named, route_named, hypotheses_named)}.get(
        ov, (roles_summary, route_summary_b, hypotheses_summary))
    routes = route_f(m, st, comp)
    route_cell = (f"<td>{routes}</td>" if routes else
                  "<td></td>" if "no flavour route" in common else
                  '<td class="nr">no flavour route recorded</td>')
    row_gaps = [g for g in gaps(m, comp) if g not in common and g != "no flavour route"]
    if ov == "c":       # the role tokens already name the uncovered roles
        row_gaps = [g for g in row_gaps if not g.startswith("no curated pairing for")]
    gtxt = (f'<td class="nr">{esc("; ".join(row_gaps))}</td>' if row_gaps else "<td></td>")
    cells = [f"<td>{roles_f(m, comp)}</td>", route_cell,
             f"<td>{hyp_f(m, comp)}</td>", gtxt]
    if "no flavour route" in common:
        del cells[1]
    return cells


# ---------------------------------------------------------------------------
# B. Detail: the fact sheet
# ---------------------------------------------------------------------------

SECTIONS = {1: "Identity and transformation", 2: "Sensory attributes and risks",
            3: "Needed culinary roles", 4: "Recorded pairings",
            5: "Flavour routes and their elements", 6: "Evidence and provenance",
            7: "Experimental ideas and tasting results", 8: "Missing or incomplete knowledge"}
BANDS = {1: "Attributes", 3: "Relationships", 6: "Evidence and testing", 8: "Gaps"}
SHORT = {1: "Identity", 2: "Sensory", 3: "Roles", 4: "Pairings", 5: "Routes",
         6: "Evidence", 7: "Ideas and tastings", 8: "Not recorded"}


def _anchor(comp: str, n: int) -> str:
    return f"r41-{comp}-s{n}"


def _h(comp: str, n: int, extra: str = "") -> str:
    band = f'<div class="band">{BANDS[n]}</div>' if n in BANDS else ""
    return (f'{band}<h4 id="{_anchor(comp, n)}"><span class="n">{n}</span>'
            f'{esc(SECTIONS[n])}{extra}</h4>')


def section_index(m: dict, comp: str) -> str:
    """Contents line with direct links; each entry says how much it holds."""
    needs = of(m, comp, "need")
    pairs = of(m, comp, "pairing")
    ideas = of(m, comp, "idea")
    routes = of(m, comp, "route_fit")
    step = of(m, comp, "transformation")[0]
    srcs = {x["source_id"] for r in [step] + pairs for x in r["evidence"]["sources"]}
    tasted = sum(1 for i in ideas if i["testing"]["status"] == "tested")
    g = gaps(m, comp)
    counts = {3: f"{len(needs)}", 4: f"{len(pairs)}", 5: f"{len(routes)}",
              6: f"{len(srcs)} source{'' if len(srcs) == 1 else 's'}",
              7: f"{len(ideas)} ideas · {tasted} tasted",
              8: f"{len(g)}"}
    grp: dict[str, list[str]] = {}
    band = ""
    for n in SECTIONS:
        band = BANDS.get(n, band)
        c = counts.get(n)
        txt = f"{n} {SHORT[n]}" + (f" ({c})" if c else "")
        grp.setdefault(band, []).append(f'<a href="#{_anchor(comp, n)}" target="_self">'
                                        f"{esc(txt)}</a>")
    return ('<div class="index">' + "".join(
        f'<span class="grp"><b>{esc(b)}</b>{"".join(xs)}</span>' for b, xs in grp.items())
        + "</div>")


def detail_html(m: dict, st: dict, comp: str) -> str:
    s = state_by(m, comp)
    if s is None:
        return '<div class="muted">Select a prepared ingredient in the overview.</div>'
    tags = markers(m, st, comp, traced_states(m, st))
    dense = st.get("sheet") == "dense"
    dl = '<dl class="dl4">' if dense else "<dl>"
    w = ' class="w"'                      # a long value: spans the row in the dense grid
    out = [f"<h3>{esc(s['label'])} {''.join(tags)}</h3>", section_index(m, comp)]
    why = S.exclusion(m, comp, st)
    if why:
        out.append(f'<div class="banner">Excluded by the active filters: {esc("; ".join(why))}. '
                   "Shown because it is selected.</div>")
    step = of(m, comp, "transformation")[0]
    frm = (state_link(st, s["from"], s["from_label"]) + " (an earlier preparation)"
           if s["from"] else esc(s["from_label"]))
    # 1 identity
    out.append(_h(comp, 1))
    out.append(f"{dl}<dt>From</dt><dd>{frm}</dd>"
               f"<dt>Technique</dt><dd>{esc(s['technique'])}</dd>"
               f"<dt>Step confidence</dt><dd>{conf_txt(step)}</dd>"
               f"<dt>Knowledge</dt><dd>{knowledge_txt(step)}</dd></dl>")
    # 2 sensory
    p = s["profile"]
    out.append(_h(comp, 2))
    prof = (f"<dt>Flavour tags</dt><dd>{esc(', '.join(pretty(x) for x in p['flavour_tags']))}</dd>"
            f"<dt>Texture tags</dt><dd>{esc(', '.join(pretty(x) for x in p['texture_tags']))}</dd>"
            f"<dt>Provides</dt><dd>{esc(', '.join(p['provides_roles']))}</dd>"
            f"<dt{w}>Profile note</dt><dd{w}>{esc(p['notes'] or '')}</dd>") if p else \
        '<dt>Sensory profile</dt><dd class="nr">&nbsp;not recorded&nbsp;</dd>'
    out.append(f"{dl}<dt{w}>Flavour shift</dt><dd{w}>{esc(s['flavour_shift'] or '')}</dd>"
               f"<dt{w}>Texture shift</dt><dd{w}>{esc(s['texture_shift'] or '')}</dd>{prof}"
               f"<dt>Risks</dt><dd>{esc(', '.join(s['risks'])) or 'none recorded'}</dd>"
               f"<dt>Keeps well</dt><dd>{esc(str(s['keeps_well'] or 'not recorded'))}</dd>"
               f"<dt>Freezes well</dt><dd>{'yes' if s['freezes_well'] else 'no'}</dd>"
               f"<dt>Batch-prep value</dt><dd>{esc(str(s['batch_prep_value'] or 'not recorded'))}"
               "</dd></dl>")
    # 3 needed roles
    needs = of(m, comp, "need")
    pairs = of(m, comp, "pairing")
    out.append(_h(comp, 3, f' <span class="muted">({len(needs)})</span>'))
    if needs:
        rows = []
        for n in needs:
            cook, exp = n["attrs"]["curated_pairings"], n["attrs"]["experimental_pairings"]
            cov = ((f"{cook} curated" + (f", {exp} experimental" if exp else ""))
                   if cook else "no curated pairing recorded"
                   + (f" ({exp} experimental only)" if exp else ""))
            td = "<td>" if cook else '<td class="nr">'
            rows.append(f"<tr><td class='nm'>{esc(n['role'])}</td>"
                        f"<td>{esc(n['attrs']['priority'] or '')}</td>"
                        f"<td>{esc(n['attrs']['note'] or '')}</td>{td}{esc(cov)}</td></tr>")
        out.append("<table><tr><th>Role</th><th>Priority</th><th>Note</th>"
                   "<th>Pairings recorded (listed in 4)</th></tr>" + "".join(rows) + "</table>")
    else:
        out.append('<div class="nr">&nbsp;no needed roles recorded&nbsp;</div>')
    # 4 pairings, grouped by role
    out.append(_h(comp, 4, f' <span class="muted">({len(pairs)})</span>'))
    out.append(_pairings_html(m, st, comp, pairs, needs))
    # 5 routes
    routes = of(m, comp, "route_fit")
    out.append(_h(comp, 5, f' <span class="muted">({len(routes)})</span>'))
    if routes and dense:
        out.append(_routes_dense(m, st, comp, routes))
    elif routes:
        for r in routes:
            els = [e for e in of(m, comp, "route_element") if e["route_id"] == r["route_id"]]
            miss = [e["ingredient"] for e in els
                    if e["optionality"] == "required" and e["availability"] != "on hand"]
            have = ("" if not m["have"] else
                    ' · <span class="have">every required element on hand</span>' if not miss
                    else f" · required, not on hand: {esc(_names(miss))}")
            out.append(f"<h5>{route_link(st, r['route_id'], r['attrs']['name'])} "
                       f'<span class="muted">· {conf_txt(r)}</span>{have}</h5>'
                       f"<div class='muted'>Why it fits: "
                       f"{esc(r['attrs']['fit_reason'] or 'not recorded')}</div>")
            head = "<th>Element</th><th>Optionality</th><th>Contribution</th>"
            if m["have"]:
                head += "<th>Availability</th>"
            out.append(f"<table><tr>{head}</tr>" + "".join(
                f"<tr><td>{ing_link(st, e['ingredient'])}</td><td>{opt_txt(e)}</td>"
                f"<td>{esc(e['attrs']['contribution'])}</td>"
                + (f"<td>{avail_txt(e)}</td>" if m["have"] else "") + "</tr>"
                for e in els) + "</table>")
        out.append('<div class="muted">Only “required” elements are needed for the route; '
                   "supporting and finish elements are optional. Routes carry an attestation "
                   "(how common the structure is), not sources."
                   + ("" if m["have"] else " Nothing is entered as on hand, so availability "
                      "is not assessed.") + "</div>")
    else:
        out.append('<div class="nr">&nbsp;no flavour route recorded for this preparation&nbsp;</div>')
    # 6 evidence
    out.append(_h(comp, 6))
    out.append(_evidence_html(m, st, comp, step, pairs))
    # 7 ideas and tastings
    ideas = of(m, comp, "idea")
    out.append(_h(comp, 7))
    out.append(_ideas_html(m, st, comp, ideas, pairs, dense))
    # 8 missing
    out.append(_h(comp, 8))
    out.append(_missing_html(m, comp, needs, pairs, routes))
    return f'<div class="r4{" dense" if dense else ""}">' + "".join(out) + "</div>"


def _routes_dense(m, st, comp, routes) -> str:
    """Dense sheet: every route in one table, a group row per route carrying
    its attestation, availability summary and fit reason (the same facts as
    the full sheet's heading + paragraph + table per route)."""
    cols = 4 if m["have"] else 3
    head = "<th>Element</th><th>Optionality</th><th>Contribution</th>" + (
        "<th>Availability</th>" if m["have"] else "")
    rows = []
    for r in routes:
        els = [e for e in of(m, comp, "route_element") if e["route_id"] == r["route_id"]]
        miss = [e["ingredient"] for e in els
                if e["optionality"] == "required" and e["availability"] != "on hand"]
        have = ("" if not m["have"] else
                ' · <span class="have">every required element on hand</span>' if not miss
                else f" · required, not on hand: {esc(_names(miss))}")
        rows.append(f'<tr class="grp"><td colspan="{cols}">'
                    f"{route_link(st, r['route_id'], r['attrs']['name'])} "
                    f'<span class="muted">· {conf_txt(r)}</span>{have}'
                    f'<div class="muted">Why it fits: {esc(r["attrs"]["fit_reason"] or "not recorded")}'
                    "</div></td></tr>")
        rows += [f"<tr><td>{ing_link(st, e['ingredient'])}</td><td>{opt_txt(e)}</td>"
                 f"<td>{esc(e['attrs']['contribution'])}</td>"
                 + (f"<td>{avail_txt(e)}</td>" if m["have"] else "") + "</tr>" for e in els]
    return (f"<table><tr>{head}</tr>" + "".join(rows) + "</table>"
            '<div class="muted">Only “required” elements are needed; supporting and finish are '
            "optional. Routes carry an attestation, not sources."
            + ("" if m["have"] else " Availability not assessed: nothing entered as on hand.")
            + "</div>")


def _pairings_html(m, st, comp, pairs, needs) -> str:
    if not pairs:
        return '<div class="nr">&nbsp;no pairing recorded for this preparation&nbsp;</div>'
    uniform = _scope_uniform_missing(pairs)
    by_role: dict[str, list[dict]] = {}
    for p in pairs:
        by_role.setdefault(p["role"], []).append(p)
    need_by = {n["role"]: n for n in needs}
    cols = ["Ingredient", "Knowledge", "Confidence", "Application"]
    if m["have"]:
        cols.append("Availability")
    cols.append("Source" if uniform else "Source · claim scope")
    rows = []
    order = [n["role"] for n in needs if n["role"] in by_role] + \
        [r for r in by_role if r not in need_by]
    for role in order:
        n = need_by.get(role)
        hint = (f'needed · priority {esc(n["attrs"]["priority"] or "not recorded")}' if n
                else "not a listed need")
        rows.append(f'<tr class="grp"><td colspan="{len(cols)}">{esc(role)} '
                    f'<span class="muted">{hint}</span></td></tr>')
        for pr in by_role[role]:
            lk = [x for x in linked(m, pr) if x["kind"] == "idea"]
            note = ""
            if lk:
                t = lk[0]["testing"]
                note = ('<div class="muted">also a Scout idea for the same pair'
                        + (f", tasted: {esc(t['trials'][0]['verdict'])}" if t["status"] == "tested"
                           else ", not tasted") + " — see 7</div>")
            cells = [f"<td>{ing_link(st, pr['ingredient'])}{note}</td>",
                     f"<td>{knowledge_txt(pr)}</td>", f"<td>{conf_txt(pr)}</td>",
                     f"<td>{esc(pr['attrs']['application'] or '')}</td>"]
            if m["have"]:
                cells.append(f"<td>{avail_txt(pr)}</td>")
            cells.append(f"<td>{sources_txt(st, pr, scope=not uniform)}</td>")
            rows.append("<tr>" + "".join(cells) + "</tr>")
    links = sum(len(p["evidence"]["sources"]) for p in pairs)
    foot = (f'<div class="muted">Claim scope: not recorded on any of the {links} source links '
            "in this table, so each link says only that the source was cited for the "
            "pairing.</div>" if uniform else "")
    if not m["have"]:
        foot += ('<div class="muted">Nothing is entered as on hand, so availability is not '
                 "assessed.</div>")
    return ("<table><tr>" + "".join(f"<th>{c}</th>" for c in cols) + "</tr>"
            + "".join(rows) + "</table>" + foot)


def _ideas_html(m, st, comp, ideas, pairs, dense: bool = False) -> str:
    exp = [p for p in pairs if p["knowledge"] == "experimental"]
    tasted = [i for i in ideas if i["testing"]["status"] == "tested"]
    untested = [i for i in ideas if i["testing"]["status"] != "tested"]
    out = ['<div class="ideas"><div class="muted">' + (
        "Hypotheses, not recommendations. Experimental = editor-recorded, ungraded; Scout "
        "ideas = generated; inference strength rates the reasoning, not the food."
        if dense else
        "Hypotheses, not recommendations. "
        "Experimental pairings are recorded by an editor without a grade; Scout ideas are "
        "generated from analogy rules (inference strength rates the analogy’s reasoning, "
        "not the food; novelty is a recipe-corpus search class).") + "</div>"]
    out.append("<h5>Recorded tasting results</h5>")
    if tasted:
        rows = []
        for i in tasted:
            for t in i["testing"]["trials"]:
                rows.append(f"<tr><td style='white-space:nowrap'>{esc(t['tested_at'])}</td>"
                            f"<td>{ing_link(st, i['ingredient'])} "
                            f"<span class='muted'>replacing {esc(pretty(i['attrs']['replaces']))}"
                            f"</span></td><td class='tested'>{esc(t['verdict'])}</td>"
                            f"<td>{esc(t['preparation'])}; ratio {esc(t['ratio'])}; "
                            f"temperature {esc(t['temperature'])}"
                            # R4.2: the recorded observation qualifies the verdict
                            # (R4 and R4.1 never showed it)
                            + (f'<div class="obs">Observed: {esc(t["observations"])}</div>'
                               if t.get("observations") else "") + "</td></tr>")
        out.append("<table><tr><th>Date</th><th>Idea tasted</th><th>Verdict</th>"
                   "<th>Conditions and observations</th></tr>" + "".join(rows) + "</table>")
    else:
        out.append('<div class="muted">No tasting recorded for this preparation.</div>')
    out.append("<h5>Experimental pairings</h5>")
    out.append('<div>' + ", ".join(
        f'<span class="exp">{ing_link(st, p["ingredient"])}</span> ({esc(p["role"])})'
        for p in exp) + ' <span class="muted">— full record in 4</span></div>' if exp else
        '<div class="muted">None recorded.</div>')
    out.append(f"<h5>Scout ideas ({len(ideas)}: {len(tasted)} tasted, "
               f"{len(untested)} not tasted)</h5>")
    if ideas:
        rows = []
        for i in tasted + untested:
            lk = [x for x in linked(m, i) if x["kind"] == "pairing"]
            lks = "; ".join(f"experimental pairing for {x['role']}" if x["knowledge"] == "experimental"
                            else f"curated pairing for {x['role']}" for x in lk)
            cells = [f"<td>{ing_link(st, i['ingredient'])}<div class='muted'>rule: "
                     f"{esc(pretty(i['attrs']['analogy_id']))}</div></td>",
                     f"<td>{esc(pretty(i['attrs']['replaces']))}</td>",
                     f"<td>{esc(pretty(i['confidence']['value']) or 'not recorded')}</td>",
                     f"<td>{esc(pretty(i['attrs']['novelty']) or 'not observed')}</td>"]
            if m["have"]:
                cells.append(f"<td>{avail_txt(i)}</td>")
            cells += [f"<td>{testing_txt(i)}</td>",
                      f"<td>{esc(lks) if lks else '<span class=muted>not recorded otherwise</span>'}</td>"]
            rows.append("<tr>" + "".join(cells) + "</tr>")
        head = ["Candidate (analogy rule)", "Replaces", "Inference strength", "Novelty"] + \
            (["Availability"] if m["have"] else []) + ["Tasting", "Also recorded as"]
        out.append("<table><tr>" + "".join(f"<th>{h}</th>" for h in head) + "</tr>"
                   + "".join(rows) + "</table>")
    else:
        out.append('<div class="nr">&nbsp;no Scout idea generated for this preparation&nbsp;</div>')
    return "".join(out) + "</div>"


GAP_SECTION = {"no curated pairing for": 3, "no flavour route": 5, "no source for the step": 6,
               "no source for any pairing": 6, "no sensory profile": 2, "no needed roles": 3}


def missing_ingredients(m: dict, comp: str) -> list[str]:
    """What the user does not have, as opposed to what nobody recorded."""
    if not m["have"]:
        return []
    out = []
    for r in of(m, comp, "route_fit"):
        miss = [e["ingredient"] for e in of(m, comp, "route_element")
                if e["route_id"] == r["route_id"] and e["optionality"] == "required"
                and e["availability"] != "on hand"]
        if miss:
            out.append(f"{r['attrs']['name']}: required {_names(miss)} not on hand")
    for n in of(m, comp, "need"):
        cook = [p for p in of(m, comp, "pairing")
                if p["role"] == n["role"] and p["knowledge"] == "curated"]
        if cook and not any(p["availability"] == "on hand" for p in cook):
            out.append(f"{n['role']}: no curated pairing on hand "
                       f"(recorded: {_names([p['ingredient'] for p in cook])})")
    return out


def _missing_html(m, comp, needs, pairs, routes) -> str:
    g = gaps(m, comp)
    out = ["<h5>Not recorded in the database (knowledge)</h5>"]
    if g:
        items = []
        for x in g:
            sec = next((n for k, n in GAP_SECTION.items() if x.startswith(k)), None)
            link = (f' <a href="#{_anchor(comp, sec)}" target="_self" class="muted">'
                    f"section {sec}</a>" if sec else "")
            items.append(esc(x) + link)
        out.append('<div class="gapbox">' + "<br>".join(items) +
                   '<div class="muted">Not recorded means nobody wrote it down. '
                   "It does not mean “not needed” or “doesn’t work”.</div></div>")
    else:
        out.append('<div class="muted">Nothing: every section above has recorded data.</div>')
    out.append("<h5>Not on hand (your ingredients)</h5>")
    if not m["have"]:
        out.append('<div class="muted">Nothing is entered as on hand, so availability is not '
                   "assessed. This is not a gap in the data.</div>")
    else:
        mi = missing_ingredients(m, comp)
        out.append('<div class="stockbox">' + ("<br>".join(esc(x) for x in mi) if mi else
                   "Every route’s required elements and at least one curated pairing per needed "
                   "role are on hand.") +
                   '<div class="muted">This depends only on what you entered; it says nothing '
                   "about the recorded knowledge.</div></div>")
    return "".join(out)


def _evidence_html(m, st, comp, step, pairs) -> str:
    rows = ""
    for x in step["evidence"]["sources"]:
        link = a(S.href(st, trace=f"source:{x['source_id']}", pane="trace"), esc(x["title"]))
        rows += (f"<tr><td>{link}</td><td>{esc(x['type'] or '')}</td>"
                 f"<td>{esc(x['claim_scope'] or 'not recorded')}</td></tr>")
    out = ["<h5>Sources for the preparation step (transformation)</h5>",
           ("<table><tr><th>Source</th><th>Type</th><th>Recorded claim scope</th></tr>"
            + rows + "</table>") if rows else
           '<div class="nr">&nbsp;no source recorded for the step&nbsp;</div>']
    by_src: dict[int, list] = {}
    for p in pairs:
        for x in p["evidence"]["sources"]:
            by_src.setdefault(x["source_id"], []).append((p, x))
    out.append("<h5>Sources for the pairings</h5>")
    if by_src:
        prow, cites = [], []
        for sid, lst in by_src.items():
            src = m["sources"][sid]
            scopes = {x["claim_scope"] for _, x in lst}
            scope = ("not recorded" if scopes == {None}
                     else "; ".join(sorted(s for s in scopes if s)))
            prow.append(
                f"<tr><td>{a(S.href(st, trace=f'source:{sid}', pane='trace'), esc(src['title']))}</td>"
                f"<td>{esc(src['type'] or '')}</td>"
                f"<td class='wrap'>{', '.join(esc(p['role'] + ': ' + pretty(p['ingredient'])) for p, _ in lst)}</td>"
                f"<td>{esc(scope)}</td></tr>")
            if src["citation"]:
                cites.append(f"<div><b>{esc(src['title'])}</b>: {esc(src['citation'])}</div>")
        out.append("<table><tr><th>Source</th><th>Type</th><th>Backs these pairings</th>"
                   "<th>Claim scope</th></tr>" + "".join(prow) + "</table>")
        if cites:
            out.append(f'<details><summary>How each source describes itself ({len(cites)}) — '
                       "the source’s own words, not a claim about these pairings</summary>"
                       f'<div class="muted">{"".join(cites)}</div></details>')
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
        [esc(f"keeps {s['keeps_well']} · {'freezes' if s['freezes_well'] else 'does not freeze'}"
             f" · batch value {s['batch_prep_value']}") for s in S_])
    roles = [r for r in m["roles"] if any(
        x["role"] == r for c in comps for x in of(m, c, ("need", "pairing")))]
    for role in roles:
        cells, keys = [], []
        for c in comps:
            cells.append(compare_cell(m, st, c, role))
            keys.append(",".join(sorted(p["ingredient"] + p["knowledge"]
                                        for p in of(m, c, "pairing") if p["role"] == role))
                        + ("|need" if any(n["role"] == role for n in of(m, c, "need")) else ""))
        add("Needed roles and pairings", role.replace("_", " "), cells, keys)
    rcells, rkeys = [], []
    for c in comps:
        rs = of(m, c, "route_fit")
        rkeys.append(",".join(r["route_id"] for r in rs))
        rcells.append(route_summary(m, st, c)
                      or '<span class="nr">&nbsp;no route recorded&nbsp;</span>')
    add("Flavour routes", "Routes", rcells, rkeys)
    ecells, ekeys = [], []
    for c in comps:
        exp = [p for p in of(m, c, "pairing") if p["knowledge"] == "experimental"]
        ekeys.append(",".join(sorted(p["ingredient"] + p["role"] for p in exp)))
        ecells.append("<br>".join(f'<span class="exp">{esc(pretty(p["ingredient"]))}</span> '
                                  f'<span class="lbl">{esc(p["role"])}</span>' for p in exp)
                      or '<span class="muted">none recorded</span>')
    add("Hypotheses and testing", "Experimental pairings", ecells, ekeys)
    icells, ikeys = [], []
    for c in comps:
        ideas = of(m, c, "idea")
        ikeys.append(",".join(sorted(i["ingredient"] for i in ideas)))
        icells.append("<br>".join(
            f'<span class="gen">{esc(pretty(i["ingredient"]))}</span>'
            + (f' <span class="tested">tasted: {esc(i["testing"]["trials"][0]["verdict"])}</span>'
               if i["testing"]["status"] == "tested" else "")
            for i in ideas) or '<span class="nr">&nbsp;none generated&nbsp;</span>')
    add("Hypotheses and testing", "Scout ideas", icells, ikeys)
    add("Evidence", "Step sources", [
        ", ".join(esc(x["title"]) for x in of(m, c, "transformation")[0]["evidence"]["sources"])
        or '<span class="nr">&nbsp;none recorded&nbsp;</span>' for c in comps])
    pcells = []
    for c in comps:
        cur = [p for p in of(m, c, "pairing") if p["knowledge"] == "curated"]
        n = sum(1 for p in cur if p["evidence"]["sources"])
        titles = sorted({x["title"] for p in cur for x in p["evidence"]["sources"]})
        pcells.append(f"{n} of {len(cur)} curated pairings have a source"
                      + (f'<br><span class="muted">{esc(", ".join(titles))}</span>' if titles else ""))
    add("Evidence", "Pairing sources", pcells)
    add("Not recorded", "Knowledge gaps", [
        f'<span class="nr">&nbsp;{esc("; ".join(gaps(m, c)))}&nbsp;</span>' if gaps(m, c) else
        '<span class="muted">none</span>' for c in comps])
    return rows


def compare_html(m: dict, st: dict) -> str:
    comps = [c for c in st["cmp"] if state_by(m, c)]
    if len(comps) < 2:
        return ('<div class="r4"><div class="muted">Use “add to compare” on two or three rows '
                f"in the overview to compare them. In the compare set now: {len(comps)}.</div></div>")
    rows = compare_rows(m, st, comps)
    head = "".join(f'<th><span class="tag t-cmp">{S.compare_letter(st, c)}</span> '
                   f'{state_link(st, c)}<div class="acts">'
                   + a(S.href(st, cmp=[x for x in st["cmp"] if x != c]), "remove") + "</div></th>"
                   for c in comps)
    body, last, n_diff = [], None, 0
    for group, label, cells, keys in rows:
        differs = len(set(keys)) > 1
        n_diff += differs
        if st["diff"] and not differs:
            continue
        if group != last:
            body.append(f'<tr class="grp"><td colspan="{len(comps) + 2}">{esc(group)}</td></tr>')
            last = group
        tds = "".join(c if c.startswith("<td") else f"<td>{c}</td>" for c in cells)
        mark = ('<span class="tag t-diff">differs</span>' if differs
                else '<span class="na">same</span>')
        body.append(f'<tr class="{"" if differs else "same"}"><td>{mark}</td>'
                    f"<td>{esc(label)}</td>{tds}</tr>")
    toggle = a(S.href(st, diff=not st["diff"]),
               "show all rows" if st["diff"] else "show only the rows that differ")
    excl = [f"{pretty(c)} ({'; '.join(S.exclusion(m, c, st))})" for c in comps
            if S.exclusion(m, c, st)]
    ban = (f'<div class="banner">Excluded by the active filters: {esc(", ".join(excl))}. '
           "Kept because they are in the compare set.</div>") if excl else ""
    hidden = len(rows) - n_diff
    note = (f'{n_diff} of {len(rows)} rows differ'
            + (f" · {hidden} identical rows hidden" if st["diff"] and hidden else
               " · identical rows are greyed") + f" · {toggle}")
    return (f'<div class="r4">{ban}<div class="muted">{note}</div>'
            f'<table><thead><tr><th></th><th></th>{head}</tr></thead>' + "".join(body) + "</table></div>")


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

    Unchanged from R4. One node per real entity: an ingredient appears once
    however many records (pairing, idea, route element) point at it."""
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


def graph_placement(m: dict, st: dict) -> str:
    """'none' (nothing to draw), 'shown' (small enough to read, above the
    table), 'collapsed' (large; the table is the reading surface) or 'below'
    (large, revealed on request, under the table)."""
    edges, _ = trace_edges(m, st)
    if not edges:
        return "none"
    if len(edges) <= GRAPH_LIMIT:
        return "shown"
    return "below" if st.get("graph") else "collapsed"


def graph_note_html(m: dict, st: dict) -> str:
    edges, nodes = trace_edges(m, st)
    place = graph_placement(m, st)
    if place == "collapsed":
        return ('<div class="r4"><div class="graphnote">Graph collapsed: '
                f"<b>{len(edges)} relationships</b> among {len(nodes)} entities are too many to "
                "read as a graph at this width. Every relationship is in the table below. "
                + a(S.href(st, graph=True), "Show the complete graph") + "</div></div>")
    if place == "below":
        return ('<div class="r4"><div class="graphnote">The complete graph '
                f"({len(edges)} relationships) is shown below the table. "
                + a(S.href(st, graph=False), "Collapse the graph") + "</div></div>")
    return ""


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
    lines = ['digraph G {', 'rankdir=LR; bgcolor="transparent"; nodesep=0.12; ranksep=0.35; size="7.2,6";',
             'node [shape=box, style="rounded,filled", fillcolor="@surface@", color="@line-strong@", '
             'fontname="Helvetica", fontsize=11, margin="0.08,0.03"];',
             'edge [color="@ink-3@", fontname="Helvetica", fontsize=9, fontcolor="@ink-3@"];']
    shapes = {"state": 'fillcolor="@node-state@"', "role": 'shape=ellipse, fillcolor="@fill-soft@"',
              "route": 'shape=hexagon, fillcolor="@node-route@"', "source": 'shape=note, fillcolor="@node-source@"',
              "gap": 'style="rounded,dashed", color="@line-strong@", fontcolor="@ink-3@"',
              "pairing": 'fillcolor="@node-pairing@"'}
    for nid, n in nodes.items():
        recs = [r for e in edges if nid in (e["src"], e["dst"]) for r in e["records"]
                if r.get("ingredient") == n["name"]]
        attrs = [f'label="{_node_label(m, n, recs)}"', shapes.get(n["kind"], "")]
        if n["kind"] == "ingredient" and n["name"] in m["have"]:
            attrs.append('color="@have-base@", penwidth=2')
        if n["kind"] == "state" and S.exclusion(m, n["name"], st):
            attrs.append('fontcolor="@ink-3@", color="@line@"')
            attrs[0] = f'label="{n["label"]}\\n(excluded by filter)"'
        if nid == focus_id:                       # violet = trace, as everywhere
            attrs.append('penwidth=2.5, color="@trace-base@", fillcolor="@trace-subtle@"')
        if n["kind"] == "state":
            attrs.append(f'URL="{S.href(st, rec=n["name"], pane="detail")}", target="_self"')
        elif n["kind"] == "ingredient":
            attrs.append(f'URL="{S.href(st, trace="ingredient:" + n["name"])}", target="_self"')
        lines.append(f'"{nid}" [{", ".join(x for x in attrs if x)}];')
    for e in edges:
        r = e["records"][0] if e["records"] else {}
        style = []
        if r.get("knowledge") in ("experimental", "generated"):
            style.append('style=dashed, color="@hyp-line@"')
            if r.get("knowledge") == "generated" and r["testing"]["status"] == "tested":
                style.append('penwidth=2')
        elif e["relation"].endswith("backed by") or e["relation"].startswith("backs"):
            style.append('style=dotted, color="@ink-3@"')
        elif e["relation"] == "not recorded":
            style.append('style=dashed, color="@line-strong@"')
        if r.get("optionality") in ("supporting", "finish"):
            style.append("style=dashed")
        lab = e["label"]
        if r.get("kind") == "idea" and r["testing"]["status"] == "tested":
            lab += " · tasted: " + r["testing"]["trials"][0]["verdict"]
        lines.append(f'"{e["src"]}" -> "{e["dst"]}" [label="{lab}", {", ".join(style)}];')
    lines.append("}")
    # DOT has no CSS variables: fill the at-sign placeholders from the palette
    dot = "\n".join(lines)
    for k, v in P.tokens(st.get("pal", P.DEFAULT_WORLD)).items():
        dot = dot.replace(f"@{k}@", v)
    return dot


def trace_head_html(m: dict, st: dict) -> str:
    f = S.trace_focus(st)
    if not f:
        return ('<div class="r4 muted">Choose something to trace: “trace” on an overview row, or '
                "any ingredient, route or source name in the fact sheet.</div>")
    edges, nodes = trace_edges(m, st)
    lvl = '<div class="tabs">' + "".join(
        f'<span class="on">Step {i}: {esc(t)}</span>' if i == st["depth"] else
        a(S.href(st, depth=i), f"Step {i}: {esc(t)}") for i, t in TRACE_LEVELS.items()) + "</div>"
    back = (" · " + a(S.href(st, pane="detail"), f"back to {esc(pretty(st['rec']))}")
            if st["rec"] else "")
    summary = (f'<div class="muted"><b>{len(edges)} relationships</b> · {len(nodes)} entities, '
               f"each shown once{back}</div>")
    return ('<div class="r4"><h3>Trace: ' + esc(_focus_label(m, f))
            + ' <span class="tag t-trace">traced</span></h3>' + lvl + summary + "</div>")


def trace_table_html(m: dict, st: dict) -> str:
    """The relationship table: every edge, grouped under its From entity, with
    one labelled column per dimension. Columns that are n/a on every row are
    dropped and named."""
    edges, nodes = trace_edges(m, st)
    f = S.trace_focus(st)
    if not f:
        return ""
    if not edges:
        return ('<div class="r4"><div class="nr">&nbsp;nothing recorded for this focus within '
                f'{esc(pretty(m["ingredient"]))} at this step&nbsp;</div></div>')

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
        return f'<span class="nm">{esc(n["label"].replace(chr(92) + "n", " "))}</span>'

    recs = [e["records"][0] for e in edges if e["records"]]
    uniform = _scope_uniform_missing(recs)
    rows: list[tuple[str, list[str]]] = []
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
        ex = {}
        for end in ("src", "dst"):
            n = nodes[e[end]]
            ex[end] = ('<div class="why">excluded by filter</div>'
                       if n["kind"] == "state" and S.exclusion(m, n["name"], st) else "")
        dims = ([knowledge_txt(r), conf_txt(r), avail_txt(r),
                 sources_txt(st, r, scope=not uniform), testing_txt(r), opt_txt(r)]
                if r else [NA] * 6)
        rows.append((e["src"], [f"<td>{label(e['src'])}{ex['src']}</td>",
                                f"<td>{esc(e['relation'])}</td>",
                                f"<td>{label(e['dst'])}{ex['dst']}</td>"]
                     + [f'<td class="src">{d}</td>' if j == 3 and d != NA else f"<td>{d}</td>"
                        for j, d in enumerate(dims)]
                     + [f'<td class="muted">{esc(note)}</td>' if note else f"<td>{NA}</td>"]))
    heads = ["From", "Relation", "To", "Knowledge", "Confidence", "Availability", "Sources",
             "Testing", "Optionality", "Note"]
    keep = [i for i in range(len(heads))
            if i < 3 or any(row[i] != f"<td>{NA}</td>" for _, row in rows)]
    dropped = [heads[i] for i in range(len(heads)) if i not in keep]
    body, last = [], None
    for src, row in rows:
        cells = [row[i] for i in keep]
        if src == last:              # the same From as the row above: greyed, not repeated loudly
            cells[0] = cells[0].replace("<td>", '<td class="rep">', 1)
        last = src
        body.append('<tr class="edge">' + "".join(cells) + "</tr>")
    notes = []
    if dropped:
        notes.append(f"Not applicable to any row here: {', '.join(dropped)}.")
    if uniform:
        notes.append("Claim scope is not recorded on any source link in this table.")
    note = f'<div class="muted">{esc(" ".join(notes))}</div>' if notes else ""
    return ('<div class="r4">' + note + '<div class="tscroll"><table class="trace"><thead><tr>'
            + "".join(f"<th>{heads[i]}</th>" for i in keep) + "</tr></thead>"
            + "".join(body) + "</table></div></div>")


def tabs_html(m: dict, st: dict, current: str) -> str:
    cmp_txt = ", ".join(f"{S.compare_letter(st, c)} {pretty(c)}" for c in st["cmp"])
    labels = {"detail": "Detail" + (f": {pretty(st['rec'])}" if st["rec"] else ""),
              "compare": f"Compare ({len(st['cmp'])})" + (f": {cmp_txt}" if st["cmp"] else ""),
              "trace": "Trace" + (f": {_focus_label(m, S.trace_focus(st))}"
                                  if S.trace_focus(st) else ""),
              "circle": "Taste circle" + (f": {pretty(st['rec'])}" if st["rec"] else "")}
    return '<div class="r4"><div class="tabs">' + "".join(
        f'<span class="on k-{k}">{esc(t)}</span>' if k == current else
        a(S.href(st, pane=k), esc(t)).replace("<a ", f'<a class="k-{k}" ', 1)
        for k, t in labels.items()) + "</div></div>"
