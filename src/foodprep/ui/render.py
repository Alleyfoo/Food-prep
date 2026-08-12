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


def _initials(name: str) -> str:
    """"roasted_broccoli_component" -> "RB"; "lemon" -> "L"."""
    words = [w for w in name.replace("_component", "").replace("-", "_").split("_") if w]
    if not words:
        return "?"
    if len(words) == 1:
        return words[0][0]
    return words[0][0] + words[1][0]


def subject_disc_html(name: str, kind: str = "ingredient") -> str:
    """The 200px disc at the head of a subject column.

    No photography exists yet and the design must stand up without it, so
    this is the typographic fallback: the subject's initials on its own
    kind's hue. A photograph drops into the same slot later without the
    layout moving.
    """
    return (f'<div class="subject-disc {_esc(kind)}">'
            f'{_esc(_initials(name).upper())}</div>')


def subject_column_html(name: str, kind: str = "ingredient",
                        label: str = "", note: str = "") -> str:
    """Label, disc, name and a line of context — the left rail of a screen."""
    parts = []
    if label:
        parts.append(f'<div class="eyebrow">{_esc(label)}</div>')
    parts.append(subject_disc_html(name, kind))
    parts.append(f'<div class="subject-name">'
                 f'{_esc(name.replace("_component", "").replace("_", " "))}</div>')
    if note:
        parts.append(f'<div class="subject-note">{_esc(note)}</div>')
    return "".join(parts)


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
                f'<div class="chip-group"><span class="gl have">'
                f'{_esc(g["filler"].replace("_", " "))} — have it</span>{roles}</div>'
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


def branch_card_html(d: dict, with_debug: bool = False,
                     available: dict | None = None,
                     lead: bool = False) -> str:
    """*lead* marks the top-ranked branch, which takes the accent border."""
    conf = d.get("confidence") or ""
    card_cls = "scout" if conf == "experimental" else ""
    if lead:
        card_cls = (card_cls + " lead").strip()
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


def hypothesis_card_html(h: dict, with_debug: bool = False,
                         lead: bool = True) -> str:
    """The hypothesis itself: what it is and why, and nothing else.

    Compatibility and novelty deliberately live in their own cards — they
    are two separate claims and must never read as one score.
    """
    rules = []
    mech = (h.get("mechanism") or "").replace("_", " ")
    if mech:
        rules.append(f'<span class="tag tag-neutral">{_esc(mech)}</span>')
    if h.get("known_pairing"):
        rules.append('<span class="tag tag-neutral">analogy substitution</span>')
    if h.get("on_hand"):
        rules.append(f'<span class="tag tag-accent-2">'
                     f'{_esc(str(h["on_hand"]).replace("_", " "))} — have it</span>')

    parts = [f'<div class="card hypothesis{" lead elev-md" if lead else ""}">']
    parts.append('<div class="card-kicker">Hypothesis</div>')
    parts.append(f'<div class="hyp-candidate">'
                 f'{_esc(h.get("pairing_title") or h.get("candidate", ""))}</div>')
    if h.get("explanation"):
        parts.append(f'<div class="hyp-explanation">{_esc(h["explanation"])}</div>')
    if h.get("known_pairing"):
        parts.append(f'<div class="hyp-explanation">The analogy is '
                     f'{_esc(str(h["known_pairing"]).replace("_", " "))}.</div>')
    if rules:
        parts.append(f'<div class="journey-chain">{"".join(rules)}</div>')
    if with_debug:
        parts.append(debug_block("Show hypothesis data", h))
    parts.append('</div>')
    return "".join(parts)


def claim_cards_html(h: dict) -> str:
    """Compatibility and novelty, side by side, as two separate claims."""
    novelty = h.get("novelty") or {}
    nclass = novelty.get("class", "not_checked")
    count = novelty.get("observed_count", 0)
    scope = novelty.get("scope", "the local corpus")
    if nclass == "not_checked":
        n_title, n_body = "Not checked", "Novelty has not been evaluated for this pairing."
    elif nclass == "novel":
        n_title = "Not observed"
        n_body = (f"Zero co-occurrences in {scope}. "
                  f"Absent evidence, not proof.")
    else:
        n_title = "Seen before"
        n_body = f"{count} co-occurrence{'s' if count != 1 else ''} in {scope}."

    compat = {"scout_candidate": "Plausible",
              "weak_hypothesis": "Thin",
              "rejected": "Rejected"}.get(h.get("candidate_class"), "Thin")
    c_body = h.get("shared_function") or h.get("meaningful_difference") or ""

    return (
        '<div class="claim-pair">'
        f'<div class="card"><div class="card-kicker">Compatibility</div>'
        f'<div class="claim-title">{_esc(compat)}</div>'
        f'<div class="card-body">{_esc(c_body)}</div></div>'
        f'<div class="card"><div class="card-kicker">Novelty</div>'
        f'<div class="claim-title">{_esc(n_title)}</div>'
        f'<div class="card-body">{_esc(n_body)}</div></div>'
        '</div>'
    )


def smallest_test_html(h: dict) -> str:
    """The protocol as a label grid. Buttons are rendered by the caller."""
    protocol = h.get("protocol") or {}
    rows = []
    for key, label in [
        ("starting_ratio", "Ratio"),
        ("success_condition", "Success"),
        ("likely_failure", "Likely failure"),
        ("corrections", "Correction"),
        ("safety_note", "Safety"),
    ]:
        val = protocol.get(key)
        if val:
            rows.append(f'<div class="row"><span class="lbl">{_esc(label)}</span>'
                        f'<div class="val">{_esc(val)}</div></div>')
    if not rows:
        rows.append('<div class="row"><span class="lbl">Protocol</span>'
                    '<div class="val">No test protocol written for this rule '
                    'yet.</div></div>')
    return ('<div class="card smallest-test">'
            '<div class="card-kicker">Smallest test</div>'
            + "".join(rows) + '</div>')


def trial_history_html(h: dict) -> str:
    """Recorded tastings, read-only — the append-only record, never edited."""
    trials = h.get("trials") or []
    if not trials:
        return ('<div class="card muted"><div class="card-kicker">Trial history</div>'
                '<div class="card-body">No tastings recorded yet.</div></div>')
    parts = ['<div class="card"><div class="card-kicker">'
             f'Trial history · {len(trials)} recorded</div>']
    for t in trials:
        verdict = t.get("verdict", "")
        vcls = verdict if verdict in ("accept", "reject", "partial", "mixed") else "mixed"
        parts.append(f'<div class="row"><span class="lbl">'
                     f'{_esc(t.get("tested_at", ""))}</span><div class="val">'
                     f'<span class="trial-verdict {vcls}">{_esc(verdict)}</span> '
                     f'{_esc(t.get("observations") or "")}</div></div>')
    parts.append('</div>')
    return "".join(parts)


def journey_card_html(j: dict, with_debug: bool = False,
                      index: int | None = None) -> str:
    """One journey as its causal chain.

    The chain is the point of the screen: ingredient → preparation →
    transformation → sensory change → flavour route → correction →
    destination. It reads as a row of tags rather than a label grid, so the
    causality is visible at a glance instead of being reconstructed from
    rows. Colour marks the kind of step: what you do (neutral), what it
    becomes (accent), which direction it takes (sage).
    """
    transitions = j.get("transitions") or []
    destinations = j.get("destinations") or []

    def step(text: str, cls: str) -> str:
        return f'<span class="tag {cls}">{_esc(text.replace("_", " "))}</span>'

    chain: list[str] = []
    prep = transitions[0]["move"] if transitions else ""
    if prep:
        chain.append(step(prep, "tag-neutral"))
    if j.get("primary_transformation"):
        chain.append(step(j["primary_transformation"], "tag-accent"))
    if j.get("sensory_change"):
        chain.append(step(j["sensory_change"], "tag-neutral"))
    if j.get("flavour_direction"):
        chain.append(step(j["flavour_direction"], "tag-accent-2"))
    if j.get("correction"):
        chain.append(step(j["correction"], "tag-neutral"))
    for d in destinations[:2]:
        chain.append(step(d, "tag-accent"))

    arrow = '<span class="chain-arrow">&rarr;</span>'
    chain_html = arrow.join(chain) if chain else ""

    kicker = "Journey"
    if index is not None:
        kicker = f"Journey {index}"
    if destinations:
        kicker += f" · {destinations[0].replace('_', ' ')}"

    body_bits = [j.get("why_choose") or "", j.get("becomes_possible") or ""]
    body = " ".join(b for b in body_bits if b)

    parts = ['<div class="card journey">']
    parts.append(f'<div class="card-kicker">{_esc(kicker)}</div>')
    parts.append(f'<div class="journey-title">{_esc(j.get("title", ""))}</div>')
    if chain_html:
        parts.append(f'<div class="journey-chain">{chain_html}</div>')
    if body:
        parts.append(f'<div class="card-body">{_esc(body)}</div>')
    if j.get("useful_additions"):
        parts.append(
            f'<div class="row"><span class="lbl">Additions</span>'
            f'<div class="chips">'
            f'{chips([a.replace("_", " ") for a in j["useful_additions"]])}'
            f'</div></div>')
    if j.get("risks"):
        parts.append(f'<div class="row"><span class="lbl">Watch for</span>'
                     f'<div class="val">{_esc(j["risks"])}</div></div>')
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
