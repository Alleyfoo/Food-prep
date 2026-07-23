"""Pure HTML builders for the food-prep Streamlit UI.

No Streamlit imports here — these functions return HTML strings that the
Streamlit app renders via ``st.markdown(..., unsafe_allow_html=True)``.
"""

from __future__ import annotations

import html
import json
from typing import Any


def _esc(s) -> str:
    return html.escape(str(s) if s is not None else "")


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


def available_partition_html(part: dict) -> str:
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
    try_groups = []
    for role, fillers in (d.get("fillers_by_role") or {}).items():
        names = [f["filler"] for f in fillers[:3]] or ["(no curated filler)"]
        try_groups.append(
            f'<div class="chip-group"><span class="gl">{_esc(role)}</span>'
            + " ".join(chip(n, "filler") for n in names) + "</div>"
        )
    try_html = "".join(try_groups) or '<span class="chip" style="color:var(--ink-5)">—</span>'
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


def hypothesis_card_html(h: dict, with_debug: bool = False) -> str:
    """Render one generated Scout hypothesis as a card."""
    candidate_class = h.get("candidate_class", "weak_hypothesis")
    novelty = h.get("novelty") or {}
    novelty_class = novelty.get("class", "not_checked")

    novelty_badge = ""
    if novelty_class == "not_checked":
        novelty_badge = '<span class="novelty-badge not_checked">novelty not checked</span>'
    elif novelty_class == "novel":
        count = novelty.get("observed_count", 0)
        scope = novelty.get("scope", "")
        novelty_badge = f'<span class="novelty-badge novel">novel ({count} occurrences, {_esc(scope)})</span>'
    else:
        count = novelty.get("observed_count", 0)
        scope = novelty.get("scope", "")
        novelty_badge = f'<span class="novelty-badge seen">seen ({count}×, {_esc(scope)})</span>'

    explanation = h.get("explanation") or ""
    analogy = h.get("known_pairing") or ""
    difference = h.get("meaningful_difference") or ""
    risk = h.get("risk") or ""
    mechanism = (h.get("mechanism") or "").replace("_", " ")
    shared_function = h.get("shared_function") or ""

    parts = ['<div class="card hypothesis">']
    parts.append(
        f'<div class="hyp-header">'
        f'<span class="hyp-candidate">{_esc(h.get("candidate", ""))}</span>'
        f'<span class="hyp-class {candidate_class}">{_esc(candidate_class.replace("_", " "))}</span>'
        f'{novelty_badge}'
        f'</div>'
    )
    if explanation:
        parts.append(f'<div class="hyp-explanation">{_esc(explanation)}</div>')
    parts.append(
        f'<div class="hyp-meta">'
        f'<div><span class="lbl">Analogy</span><div class="val">{_esc(analogy)}</div></div>'
        f'<div><span class="lbl">Shared function</span><div class="val">{_esc(shared_function)}</div></div>'
        f'<div><span class="lbl">Mechanism</span><div class="val">{_esc(mechanism)}</div></div>'
        f'<div><span class="lbl">Difference</span><div class="val">{_esc(difference)}</div></div>'
        f'<div><span class="lbl">Risk</span><div class="val">{_esc(risk)}</div></div>'
        f'</div>'
    )

    protocol = h.get("protocol")
    if protocol:
        parts.append('<div class="protocol-block">')
        parts.append('<h5>Smallest test protocol</h5>')
        for key, label in [
            ("smallest_test", "Smallest test"),
            ("starting_ratio", "Starting ratio"),
            ("success_condition", "Success if"),
            ("likely_failure", "Likely failure"),
            ("corrections", "Corrections"),
            ("safety_note", "Safety"),
        ]:
            val = protocol.get(key) or ""
            if val:
                parts.append(
                    f'<div class="protocol-row"><span class="lbl">{_esc(label)}</span>'
                    f'<span class="val">{_esc(val)}</span></div>'
                )
        parts.append('</div>')

    trials = h.get("trials") or []
    if trials:
        parts.append('<div class="trial-block">')
        parts.append(f'<h5>Trial history ({len(trials)} recorded)</h5>')
        for trial in trials:
            verdict = trial.get("verdict", "")
            verdict_cls = verdict if verdict in ("accept", "reject", "partial", "mixed") else "mixed"
            parts.append(f'<div class="trial-row">')
            parts.append(
                f'<span class="lbl">{_esc(trial.get("tested_at", ""))}</span>'
                f'<span class="val"><span class="trial-verdict {verdict_cls}">{_esc(verdict)}</span></span>'
            )
            parts.append('</div>')
            for tkey, tlabel in [
                ("preparation", "Prep"), ("ratio", "Ratio"),
                ("temperature", "Temp"), ("observations", "Notes"),
                ("failure_mode", "Failure"), ("successful_correction", "Fix"),
            ]:
                tval = trial.get(tkey)
                if tval:
                    parts.append(
                        f'<div class="trial-row"><span class="lbl">{_esc(tlabel)}</span>'
                        f'<span class="val">{_esc(tval)}</span></div>'
                    )
        parts.append('</div>')
    else:
        parts.append(
            '<div class="trial-block"><h5>Trial history</h5>'
            '<div class="trial-row"><span class="val" style="color:var(--ink-5);font-style:italic">'
            'no tastings recorded yet</span></div></div>'
        )

    if with_debug:
        parts.append(debug_block("Show hypothesis data", h))
    parts.append('</div>')
    return "".join(parts)


def journey_card_html(j: dict, with_debug: bool = False) -> str:
    """Render one ingredient journey as a card."""
    transitions = j.get("transitions") or []
    destinations = j.get("destinations") or []
    additions = j.get("useful_additions") or []

    path_parts = []
    for i, t in enumerate(transitions):
        if i > 0:
            path_parts.append(f'<span class="journey-move">{_esc(t["move"].replace("_", " "))}</span>')
        path_parts.append(f'<span class="journey-state">{_esc(t["to_state"].replace("_", " "))}</span>')
    path_html = "".join(path_parts) if path_parts else (
        f'<span class="journey-state">{_esc(j.get("output_state", "").replace("_", " "))}</span>'
    )

    parts = ['<div class="card journey">']
    parts.append(
        f'<div class="journey-title">{_esc(j.get("title", ""))}</div>'
    )
    parts.append(
        f'<div class="journey-why">{_esc(j.get("why_choose", ""))}</div>'
    )
    parts.append(
        f'<div class="row"><span class="lbl">Transform</span>'
        f'<div class="val">{_esc((j.get("primary_transformation") or "").replace("_", " "))}</div></div>'
    )
    parts.append(
        f'<div class="row"><span class="lbl">Change</span>'
        f'<div class="val">{_esc(j.get("sensory_change", ""))}</div></div>'
    )
    parts.append(
        f'<div class="row"><span class="lbl">Direction</span>'
        f'<div class="val">{_esc(j.get("flavour_direction", ""))}</div></div>'
    )
    if additions:
        parts.append(
            f'<div class="row"><span class="lbl">Additions</span>'
            f'<div class="chips">{chips([a.replace("_", " ") for a in additions])}</div></div>'
        )
    parts.append(
        f'<div class="row"><span class="lbl">Unlocks</span>'
        f'<div class="val">{_esc(j.get("becomes_possible", ""))}</div></div>'
    )
    if destinations:
        parts.append(
            f'<div class="row"><span class="lbl">Destinations</span>'
            f'<div class="chips">{chips([d.replace("_", " ") for d in destinations])}</div></div>'
        )
    parts.append(
        f'<div class="row"><span class="lbl">Watch for</span>'
        f'<div class="val">{_esc(j.get("risks", ""))}</div></div>'
    )
    parts.append(
        f'<div class="row"><span class="lbl">Correction</span>'
        f'<div class="val">{_esc((j.get("correction") or "").replace("_", " "))}</div></div>'
    )
    if transitions:
        parts.append('<div class="journey-path">' + path_html + '</div>')
    if with_debug:
        parts.append(debug_block("Show journey data", j))
    parts.append('</div>')
    return "".join(parts)


def route_card_html(r: dict, with_debug: bool = False) -> str:
    """Render one flavour route as a card."""
    elements = r.get("elements") or []
    available_elements = {e["ingredient"] for e in (r.get("available_elements") or [])}
    destinations = r.get("destinations") or []
    dimensions = r.get("flavour_dimensions") or []
    conf = r.get("confidence") or ""

    element_chips = []
    for e in elements:
        name = e.get("ingredient", "")
        contribution = e.get("contribution", "")
        optionality = e.get("optionality", "")
        is_available = name in available_elements
        cls = "available" if is_available else ("required" if optionality == "required" else "")
        element_chips.append(
            f'<span class="route-element {cls}">'
            f'<span class="name">{_esc(name)}</span>'
            f'<span class="contribution">{_esc(contribution)}</span>'
            f'</span>'
        )

    parts = [f'<div class="card route">']
    parts.append(
        f'<div class="card-head"><span class="card-tech">{_esc(r.get("name", ""))}</span>'
        f'<span class="card-comp">{_esc(r.get("description", ""))}</span>'
        f'{conf_pill(conf)}</div>'
    )
    if dimensions:
        parts.append(
            f'<div class="row"><span class="lbl">Dimensions</span>'
            f'<div class="chips">{chips(dimensions, "flavour")}</div></div>'
        )
    if destinations:
        parts.append(
            f'<div class="row"><span class="lbl">Destinations</span>'
            f'<div class="chips">{chips([d.replace("_", " ") for d in destinations])}</div></div>'
        )
    if r.get("cultural_context"):
        parts.append(
            f'<div class="row"><span class="lbl">Culture</span>'
            f'<div class="val">{_esc(r["cultural_context"])}</div></div>'
        )
    if r.get("risks"):
        parts.append(
            f'<div class="row"><span class="lbl">Risks</span>'
            f'<div class="val">{_esc(r["risks"])}</div></div>'
        )
    if element_chips:
        parts.append(
            f'<div class="row"><span class="lbl">Elements</span>'
            f'<div class="route-elements">{"".join(element_chips)}</div></div>'
        )
    if r.get("fit_reason"):
        parts.append(
            f'<div class="row"><span class="lbl">Fit</span>'
            f'<div class="val">{_esc(r["fit_reason"])}</div></div>'
        )
    if with_debug:
        parts.append(debug_block("Show route data", r))
    parts.append('</div>')
    return "".join(parts)
