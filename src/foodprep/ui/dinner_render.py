"""Pure HTML for the Dinner views (R7). No Streamlit here: every function takes a
view model from `foodprep.dinner` and returns markup, so it is testable.

Words, not codes: a step says "ready for the next step" or "ready to eat"; an
absence says which absence it is (not recorded, not found, none, documented to
fail). Sources sit beside every statement. Nothing is scored or ranked.
"""

from __future__ import annotations

from foodprep import dinner as d
from foodprep.kitchen_records import VERDICTS as RECORD_VERDICTS
from foodprep.ui.render import _esc


def _src(sources) -> str:
    if not sources:
        return ""
    return f' <span class="src">{_esc(", ".join(str(s) for s in sources))}</span>'


def _cited(x: d.Cited) -> str:
    cause = f' <span class="cause">because {_esc(x.cause)}</span>' if x.cause else ""
    return f"{_esc(x.text)}{cause}{_src(x.sources)}"


def _choices(items) -> str:
    """Versions from different sources, kept apart: "a [S1] · or b [S2]"."""
    return '<span class="or"> · or </span>'.join(_cited(x) for x in items)


def _list(items) -> str:
    return "<ul>" + "".join(f"<li>{_cited(x)}</li>" for x in items) + "</ul>"


def _line(label: str, body: str, cls: str = "") -> str:
    return (f'<div class="dn-line {cls}"><span class="dn-lbl">{_esc(label)}</span>'
            f'<span class="dn-val">{body}</span></div>')


def endpoint_badge(kind: str | None) -> str:
    cls = {"readiness": "ready-next", "doneness": "ready-eat"}.get(kind, "unknown")
    return f'<span class="dn-badge {cls}">{_esc(d.ENDPOINT_WORDS.get(kind, d.ENDPOINT_WORDS[None]))}</span>'


# ---- 1. outcomes -----------------------------------------------------------------

def _record_words(rec: dict) -> str:
    v = RECORD_VERDICTS.get(rec.get("verdict"), rec.get("verdict"))
    kt = f'{rec["kitchen_test"]}, ' if rec.get("kitchen_test") else ""
    alt = f' ({_esc(rec["alternative"])})' if rec.get("alternative") else ""
    return f"{_esc(kt)}{_esc(rec.get('cooked_on'))}{alt}: {_esc(v)}"


def outcome_card_html(oc: d.Outcome) -> str:
    kicker = "Familiar use · a documented dish" if oc.group == "familiar" else \
        "Less usual use · a documented dish carried over (R4)"
    cls = "card dn-outcome" + (" risk" if oc.refused else "")
    parts = [f'<div class="{cls}"><div class="card-kicker">{_esc(kicker)}</div>',
             f'<div class="card-head"><span class="card-tech">{_esc(oc.name)}</span></div>',
             _line("Verdict", _esc(oc.verdict))]
    if oc.swapped:
        parts.append(_line("Swap", _esc(oc.swapped)))
    if oc.refused:
        parts.append(_line("Why not", _list([d.Cited(r) for r in oc.reasons])))
        if oc.replaced_by:
            parts.append(_line("Instead", f"replaced by {_esc(d.route_label('transfer:' + oc.replaced_by))}"))
    parts.append(_line("The one condition",
                       _cited(oc.condition) if oc.condition else
                       '<span class="dn-none">not recorded for this route (no R5 sequence)</span>'))
    parts.append(_line("Cooked", "; ".join(_record_words(r) for r in oc.cooked)
                       if oc.cooked else '<span class="dn-none">not cooked yet</span>'))
    parts.append(_line("Your shelf", "; ".join(
        f"{_esc(ing.replace('_', ' '))}: {_esc(words)}" for ing, words in oc.availability)
        + '<span class="dn-quiet"> · lidl.fi lists offers only, so it is not used</span>'))
    if oc.risks:
        parts.append(_line("Quality risk", _list(oc.risks), "dn-risk"))
    if oc.gaps:
        parts.append(_line("Evidence stops", _list([d.Cited(g) for g in oc.gaps]), "dn-gap"))
    for name, note in oc.keeping:
        parts.append(_line(f"{name}", _esc(note), "dn-gap"))
    if oc.other_routes:
        parts.append(_line("Routes", f"{oc.other_routes + 1} documented ways; open to compare them"))
    parts.append("</div>")
    return "".join(parts)


def part_records_html(recs: list) -> str:
    if not recs:
        return ""
    out = ['<div class="section-title">What the processing records say about this '
           'ingredient (R5), including uses not modelled as a dish</div>']
    for p in recs:
        body = []
        for cf in p.conflicts:
            body.append(_line(f"Sources differ: {cf.topic}", _choices(cf.versions)
                              + (f'<div class="dn-quiet">{_esc(cf.note)}</div>' if cf.note else "")))
        for g in p.gaps:
            body.append(_line("Not found", _esc(g), "dn-gap"))
        out.append(f'<div class="card dn-record"><div class="card-kicker">{_esc(p.name)}</div>'
                   + "".join(body) + "</div>")
    return "".join(out)


# ---- 2. overview -----------------------------------------------------------------

def step_html(sv: d.StepView, kind_member: str = "") -> str:
    if sv.done:
        return (f'<div class="dn-step done"><div class="dn-step-head"><span class="dn-n">'
                f'{sv.index}</span> {_esc(sv.name)} <span class="dn-badge held">done: you have this'
                f'</span></div></div>')
    head = (f'<div class="dn-step-head"><span class="dn-n">{sv.index}</span> '
            f'<b>{_esc(sv.name)}</b>' + (' <span class="dn-quiet">(optional)</span>' if sv.optional else "")
            + f' {endpoint_badge(sv.endpoint)}{_src(sv.endpoint_sources)}</div>')
    body = []
    if sv.says:
        body.append(_line("Route says", _esc(sv.says)
                          + (f' · or {_esc(", ".join(sv.or_ops))}' if sv.or_ops else "")))
    body.append(_line("Time", _choices(sv.times) if sv.times else '<span class="dn-none">not recorded</span>'))
    body.append(_line("Work", _cited(sv.active) if sv.active else '<span class="dn-none">not recorded</span>'))
    if sv.done_when:
        body.append(_line("Done when", _list(sv.done_when)))
    if sv.failed_if:
        body.append(_line("Failed if", _list(sv.failed_if), "dn-risk"))
    for b in sv.because:
        body.append(_line("Why", _cited(b), "dn-why"))
    for m in sv.misses:
        body.append(_line("Watch", _cited(m), "dn-risk"))
    for cf in sv.conflicts:
        body.append(_line(f"Sources differ: {cf.topic}", _choices(cf.versions)))
    if sv.medium:
        body.append(_line("With", _choices(sv.medium)))
    if sv.note:
        body.append(_line("Note", _esc(sv.note)))
    for ml in sv.members:
        if ml.found:
            val = ""
            if ml.done_when:
                val += "done when " + _choices(ml.done_when)
            if ml.failed_if:
                val += ('; ' if val else '') + "failed if " + _choices(ml.failed_if)
            body.append(_line(f"{ml.member.replace('_', ' ')} inside", val, "dn-member"))
        else:
            body.append(_line(f"{ml.member.replace('_', ' ')} inside",
                              '<span class="dn-none">not found</span>'
                              + (f' <span class="dn-quiet">{_esc(ml.note)}</span>' if ml.note else ""),
                              "dn-member"))
    for day, took in sv.recorded:
        body.append(_line("Your record", f"{_esc(day)}: {_esc(took)}", "dn-control"))
    return f'<div class="dn-step">{head}{"".join(body)}</div>'


def branch_html(br: d.Branch, hide_done: bool = False) -> str:
    cls = "dn-branch" + (" changed" if br.changed else "") + (" held" if br.held_upto else "")
    swap = ""
    if br.changed:
        swap = ('<div class="dn-swap">changed by the swap'
                + (f": instead of {_esc(br.replaces.replace('_', ' '))}" if br.replaces else "")
                + ' <span class="dn-quiet">(its repairs are in the steps below)</span></div>')
    held = ""
    if br.held_upto:
        done = ", ".join(s.name for s in br.steps if s.done)
        held = (f'<div class="dn-held">Done, you have this: {_esc(done)} '
                f'(step{"s" if br.held_upto > 1 else ""} 1-{br.held_upto}).</div>'
                if br.held_upto > 1 else
                f'<div class="dn-held">Done, you have this: {_esc(done)} (step 1).</div>')
    shown = [s for s in br.steps if not (hide_done and s.done)]
    steps = "".join(step_html(s) for s in shown) or \
        '<div class="dn-none">no steps: used as it is</div>'
    return (f'<div class="{cls}"><div class="dn-branch-head">{_esc(br.member.replace("_", " "))}'
            f'<span class="dn-quiet"> · from {_esc(br.source)}</span></div>{swap}{held}{steps}</div>')


def join_html(j: d.Join) -> str:
    members = ", ".join(
        f'{_esc(m.replace("_", " "))} <span class="dn-quiet">({_esc(role)}'
        + (", added as is" if kind == "added as is" else "") + ")</span>"
        for m, role, kind in j.members)
    swap = '<div class="dn-swap">changed by the swap</div>' if j.changed else ""
    says = _line("Route says", _esc(j.says)) if j.says else ""
    steps = "".join(step_html(s) for s in j.steps) or \
        '<div class="dn-quiet">no step of its own after joining</div>'
    return (f'<div class="dn-join{" changed" if j.changed else ""}"><div class="dn-join-head">'
            f'<span class="dn-arrow">&#x2193;</span> {_esc(j.aid.replace("_", " "))}: '
            f'{_esc(j.name)}</div><div class="dn-join-members">joins {members}</div>'
            f'{swap}{says}{steps}</div>')


def overview_html(ov: d.Overview, hide_done: bool = False) -> str:
    out = ['<div class="dn-overview">']
    if ov.kind == "transfer":
        cls = "disclaimer dn-refused" if ov.refused else "dn-transfer"
        bits = [f"{new.replace('_', ' ')} instead of {old.replace('_', ' ')}"
                for old, new in ov.swaps.items()]
        bits += [f"adds {m.replace('_', ' ')}" for m in ov.added]
        bits += [f"changes how {m.replace('_', ' ')} is prepared" for m in ov.reworked]
        bits += [f"leaves out {m.replace('_', ' ')}" for m in ov.dropped]
        swaps = "; ".join(bits)
        out.append(f'<div class="{cls}"><span class="eyebrow">A swap on '
                   f'{_esc(d.route_label(ov.base))}</span>'
                   f'{_esc(swaps) or "the base dish, re-specified"}. Verdict: <b>{_esc(ov.verdict)}</b>'
                   f'; {_esc(ov.status)}; {_esc(ov.evidence)}.')
        if ov.refused:
            out.append(_list([d.Cited(r) for r in ov.reasons]))
            if ov.replaced_by:
                out.append(f'<div>Replaced by <b>{_esc(d.route_label("transfer:" + ov.replaced_by))}</b>.</div>')
        out.append("</div>")
    if not ov.has_sequence:
        out.append('<div class="hint">No whole R5 sequence is recorded for this route: '
                   'endpoints are "not recorded" and members after a join "not found" '
                   'unless a processing record covers the step.</div>')
    branches = [b for b in ov.branches if not (hide_done and b.held_upto and not b.remaining)]
    out.append('<div class="dn-branches">' + "".join(branch_html(b, hide_done) for b in branches)
               + "</div>")
    held_done = [b for b in ov.branches if hide_done and b.held_upto and not b.remaining]
    for b in held_done:
        out.append(f'<div class="dn-held">{_esc(b.member.replace("_", " "))}: done, you have it.</div>')
    for j in ov.joins:
        out.append(join_html(j))
    for stage, times, done, note in ov.finish:
        body = _line("Time", _choices(times)) if times else ""
        if done:
            body += _line("Done when", _list(done))
        if note:
            body += _line("Note", _esc(note))
        out.append(f'<div class="dn-join"><div class="dn-join-head"><span class="dn-arrow">'
                   f'&#x2193;</span> then: {_esc(stage)}</div>{body}</div>')
    if ov.alternatives:
        out.append('<div class="dn-footer">' + _line(
            "Other documented ways", _list(ov.alternatives)
            + '<div class="dn-quiet">Each is its own documented route: compare them under '
              'Routes side by side. Mixing their steps is not documented.</div>') + "</div>")
    if ov.gaps:
        out.append('<div class="dn-footer">' + _line("Evidence stops", _list([d.Cited(g) for g in ov.gaps]), "dn-gap") + "</div>")
    for name, lines, note in ov.keeping:
        body = _list(lines) if lines else '<span class="dn-none">not known</span>'
        out.append('<div class="dn-footer">' + _line(f"Keeping: {name}", body
                   + (f'<div class="dn-quiet">{_esc(note)}</div>' if note else "")) + "</div>")
    out.append(f'<div class="hint">{_esc(d.NOT_A_SAFETY_LIMIT)}</div>')
    if ov.records:
        out.append(records_html(ov.records))
    out.append("</div>")
    return "".join(out)


def records_html(records: list) -> str:
    """Control records, beside the documented values and visibly not part of them."""
    rows = []
    for rec in records:
        bits = [_record_words(rec)]
        for addr, took in (rec.get("step_times") or {}).items():
            bits.append(f'{_esc(addr.rsplit("/", 2)[-2])} {_esc(addr.rsplit("/", 1)[-1])}: {_esc(took)}')
        for m, reached in (rec.get("endpoints") or {}).items():
            bits.append(f"{_esc(m.replace('_', ' '))} reached: {_esc(reached)}")
        if rec.get("notes"):
            bits.append(_esc(rec["notes"]))
        rows.append("<li>" + " · ".join(bits) + "</li>")
    return ('<div class="card dn-control-card"><div class="card-kicker">Your kitchen '
            'records (control records): what happened when you cooked it. Kept apart from '
            'the documented values above.</div><ul>' + "".join(rows) + "</ul></div>")


# ---- 3. aligned columns ----------------------------------------------------------

_KIND_WORDS = {
    "route": "a documented route",
    "alternative": "a documented alternative, as cited text",
    "rejected": "documented to fail",
}


def _cell(sv: d.StepView) -> str:
    bits = [endpoint_badge(sv.endpoint)]
    if sv.says:
        bits.append(f'<div class="dn-quiet">{_esc(sv.says)}</div>')
    if sv.times:
        bits.append(f"<div>{_choices(sv.times)}</div>")
    for cf in sv.conflicts:
        bits.append(f'<div><span class="dn-lbl">Sources differ: {_esc(cf.topic)}</span> '
                    f'{_choices(cf.versions)}</div>')
    if sv.done_when:
        bits.append(f'<div><span class="dn-lbl">Done when</span> {_choices(sv.done_when)}</div>')
    for m in sv.misses:
        bits.append(f'<div class="dn-risk">{_cited(m)}</div>')
    return "".join(bits)


def aligned_html(al: d.Alignment) -> str:
    head = ['<th>Step</th>']
    for col in al.columns:
        kind = _KIND_WORDS.get(col.kind, col.kind)
        says = f'<div class="dn-quiet">{_esc(col.says)}{_src(col.sources)}</div>' if col.says else ""
        verdict = f'<div class="dn-quiet">{_esc(col.verdict)}</div>' if col.verdict else ""
        head.append(f'<th class="dn-col {col.kind}"><div class="dn-col-name">{_esc(col.name)}</div>'
                    f'<div class="dn-col-kind">{_esc(kind)}</div>{verdict}{says}</th>')
    rows = []
    for i, (rk, label) in enumerate(al.rows):
        cells = [f'<td class="dn-rowlbl">{_esc(label)}</td>']
        for col in al.columns:
            if col.key is None:
                if i == 0:
                    cells.append(f'<td class="dn-text" rowspan="{len(al.rows)}">'
                                 f'<span class="dn-none">not recorded step by step</span></td>')
                continue
            sv = col.cells.get(rk)
            cells.append(f"<td>{_cell(sv)}</td>" if sv else
                         '<td class="dn-absent"><span class="dn-none">none</span></td>')
        rows.append("<tr>" + "".join(cells) + "</tr>")
    return (f'<div class="dn-aligned"><table class="table dn-table"><thead><tr>{"".join(head)}'
            f'</tr></thead><tbody>{"".join(rows)}</tbody></table></div>'
            f'<div class="hint">{_esc(al.conflicts_note)}</div>')


# ---- 5. start from ---------------------------------------------------------------

def start_from_html(sf: d.StartFrom) -> str:
    out = [f'<div class="card dn-start"><div class="card-kicker">You have</div>'
           f'<div class="card-head"><span class="card-tech">{_esc(sf.name)}</span></div>']
    if sf.not_ready_to_eat:
        out.append('<div class="dn-warn">Not ready to eat: where the routes record it, this '
                   'is a readiness state, ready for the next step.</div>')
    out.append(_line("Keeps", _list(sf.keeping) if sf.keeping else
                     '<span class="dn-none">not known</span>'))
    if sf.note:
        out.append(_line("Note", _esc(sf.note)))
    if any(h.by_state for h in sf.routes):
        out.append(f'<div class="dn-quiet">{_esc(d.HISTORY_NOT_CONSIDERED)}</div>')
    for p in sf.problems:
        out.append(_line("Problem", _esc(p), "dn-risk"))
    out.append("</div>")
    if not sf.routes:
        out.append('<div class="hint">No documented route passes through this state.</div>')
    return "".join(out)


def held_route_head_html(h: d.HeldRoute) -> str:
    state = ("not ready to eat here: ready for the next step" if h.readiness
             else "its endpoint is not recorded in this route")
    return (f'<div class="section-title">{_esc(h.name)}: {_esc(h.owner.replace("_", " "))} '
            f'is done to step {h.at} ({state}); what remains</div>')


# ---- 6. outcome table (the mindmap's default above about 20 edges) ----------------

def outcome_table_html(edges: list) -> str:
    rows = "".join(
        f"<tr><td>{_esc(_node_label(a))}</td><td>{_esc(lbl)}</td>"
        f"<td>{_esc(_node_label(b))}</td></tr>" for a, b, lbl in edges)
    return (f'<table class="table dn-outcome-table"><thead><tr><th>From</th><th>Link</th><th>To</th></tr>'
            f'</thead><tbody>{rows}</tbody></table>')


def _node_label(node: str) -> str:
    kind, _, rest = node.partition(":")
    if kind == "out":
        return d.route_label(rest)
    return rest.replace("_", " ")
