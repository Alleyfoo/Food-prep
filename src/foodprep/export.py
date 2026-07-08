"""Markdown export — a third surface over the same computed dicts.

query computes → ui renders HTML/cards → cli renders text → export renders
Markdown. Same truth, different surface. No new ontology and no engine logic
live here: these functions only serialize the dicts returned by
query.branch_card, query.component_card, query.plate_balance_detail,
query.scout_rows, and the available-filter partition
(query.available_filter / _partition_by_available). They never re-derive an
answer from strings.

Two layers:
  * render_*_markdown(d, ...) — pure: take an already-computed dict, return a
    Markdown string. No connection, no queries. Used by the UI (the dicts are
    already in scope) and by the tests.
  * branch/component/plate/scout_markdown(conn, ...) — high-level: call the
    matching query.* function then the matching renderer. Used by the CLI.
    Return None when the lookup misses (branch / component) so the CLI can
    print a clean "not found" message.
"""

from __future__ import annotations

from typing import Any

from . import query

# Verbatim Scout disclaimer (matches the UI wording, streamlit_app.py Scout tab)
SCOUT_DISCLAIMER = (
    "> Scout mode: these are role-compatible but uncommon or experimental. "
    "Taste a small amount before serving."
)

# Appended to every export as a closing "decision receipt" note.
FOOTER_LINES = [
    "## Notes",
    "",
    "Generated from local Ingredient Foundry data. Taste before serving, "
    "especially for Scout or experimental ideas.",
    "",
]


# ---------------------------------------------------------------------------
# small shared render helpers
# ---------------------------------------------------------------------------

def _add_section(parts: list[str], title: str, lines: list[str]) -> None:
    """Append a '## title' section (header, blank, bullet lines, blank) to parts."""
    parts.append(f"## {title}")
    parts.append("")
    parts.extend(lines)
    parts.append("")


def _partition_blocks(part: dict[str, Any]) -> list[tuple[str, list[str]]]:
    """The available-filter partition as (title, bullet-lines) blocks.

    Shared by branch and plate renderers — both consume the same partition
    shape (available_now / missing_but_useful / unknown_items /
    no_match_known). Empty buckets are omitted."""
    blocks: list[tuple[str, list[str]]] = []
    avail = part.get("available_now") or []
    if avail:
        blocks.append(("Available now", [
            f"- {g['filler']} → {', '.join(g['roles'])}" for g in avail
        ]))
    missing = part.get("missing_but_useful") or []
    if missing:
        lines = []
        for m in missing:
            fillers = ", ".join(m["fillers"]) if m["fillers"] else "(no curated filler)"
            lines.append(f"- {m['role']}: {fillers}")
        blocks.append(("Missing but useful", lines))
    no_match = list(part.get("unknown_items") or []) + list(part.get("no_match_known") or [])
    if no_match:
        blocks.append(("No match from selected items", [f"- {n}" for n in no_match]))
    return blocks


def _add_tags(parts: list[str], d: dict[str, Any]) -> None:
    tags = d.get("tags") or []
    if not tags:
        return
    _add_section(parts, "Tags",
                 [f"- {t.get('family', '?')}: {t.get('value', '')}" for t in tags])


def _add_risks(parts: list[str], d: dict[str, Any]) -> None:
    risks = d.get("risks") or []
    if not risks:
        return
    _add_section(parts, "Risks", [f"- {r}" for r in risks])


def _add_missing(parts: list[str], d: dict[str, Any]) -> None:
    missing = d.get("missing") or []
    if not missing:
        return
    _add_section(parts, "Missing roles",
                 [f"- {m['role_name']} ({m.get('priority', '?')})" for m in missing])


def _add_uses(parts: list[str], d: dict[str, Any]) -> None:
    uses = d.get("uses") or []
    if not uses:
        return
    _add_section(parts, "Uses", [f"- {u}" for u in uses])


def _add_next_moves(parts: list[str], d: dict[str, Any],
                    partition: dict[str, Any] | None) -> None:
    """'Next moves' = the branch/component fillers grouped by role, OR — when an
    available-filter partition is supplied — the Available now / Missing but
    useful / No match buckets that replace it."""
    if partition is not None:
        for title, lines in _partition_blocks(partition):
            _add_section(parts, title, lines)
        return
    fbr = d.get("fillers_by_role") or {}
    if not fbr:
        return
    lines = []
    for role, fillers in fbr.items():
        names = ", ".join(f["filler"] for f in fillers) if fillers else "(no curated filler)"
        lines.append(f"- {role}: {names}")
    _add_section(parts, "Next moves", lines)


# ---------------------------------------------------------------------------
# pure renderers
# ---------------------------------------------------------------------------

def render_branch_markdown(card: dict[str, Any],
                           partition: dict[str, Any] | None = None) -> str:
    """Render a query.branch_card dict to Markdown. `partition` (from
    query.available_filter) replaces the plain 'Next moves' section when given."""
    ing = card.get("ingredient", "")
    tech = card.get("technique", "")
    parts = [f"# {ing} · {tech}", ""]
    parts.append(f"→ {card.get('component', '')}")
    fs, ts = card.get("flavour_shift"), card.get("texture_shift")
    if fs or ts:
        parts.append(f"→ {fs or '—'} · {ts or '—'}")
    parts.append("")
    _add_tags(parts, card)
    _add_risks(parts, card)
    _add_missing(parts, card)
    _add_uses(parts, card)
    _add_next_moves(parts, card, partition)
    parts.extend(FOOTER_LINES)
    return "\n".join(parts)


def render_component_markdown(d: dict[str, Any],
                              partition: dict[str, Any] | None = None) -> str:
    """Render a query.component_card dict to Markdown. `partition` (from
    query.available_filter on the first producing transformation) replaces
    'Next moves' when given."""
    parts = [f"# {d.get('name', '')}", ""]
    producers = d.get("produced_by") or []
    if producers:
        prod_str = ", ".join(f"{p['ingredient']} + {p['technique']}" for p in producers)
    else:
        prod_str = "(no producing transformation)"
    parts.append(f"came from: {prod_str}")
    keeps = d.get("keeps_well") or "—"
    freezes = "yes" if d.get("freezes_well") else "no"
    batch = d.get("batch_prep_value") or "—"
    parts.append(f"Storage: keeps {keeps} · freezes: {freezes} · batch: {batch}")
    parts.append("")
    _add_tags(parts, d)
    _add_risks(parts, d)
    _add_missing(parts, d)
    _add_uses(parts, d)
    _add_next_moves(parts, d, partition)
    parts.extend(FOOTER_LINES)
    return "\n".join(parts)


def _suggested_next_move(r: dict[str, Any]) -> str:
    """A single mechanical line read only from the computed dicts — no
    synthesis, no invented pairings. Reads available_now + covered_roles +
    the gap roles."""
    gaps = list(r.get("target_gap") or []) + list(r.get("flagged_more") or [])
    if "available_now" in r:
        avail = r.get("available_now") or []
        covered = list(r.get("covered_roles") or [])
        if avail:
            fillers = ", ".join(g["filler"] for g in avail)
            remaining = [g for g in gaps if g not in covered]
            if remaining:
                return (f"Add {fillers} for {', '.join(covered)}; "
                        f"still missing {', '.join(remaining)}.")
            return f"Add {fillers} for {', '.join(covered)}."
        if gaps:
            return f"Add fillers for {', '.join(gaps)} — see Missing but useful."
        return "Plate is balanced — no hard gaps."
    if gaps:
        return f"Add fillers for {', '.join(gaps)}."
    return "Plate is balanced — no hard gaps."


def render_plate_markdown(r: dict[str, Any]) -> str:
    """Render a query.plate_balance_detail dict to Markdown. When the partition
    keys are present (available_items was passed), the Available now / Missing
    but useful / No match sections are rendered alongside the gap lists."""
    parts = ["# Plate Balance", ""]

    items = [it["name"] for it in r.get("items", [])]
    _add_section(parts, "Plate items", [f"- {n}" for n in items] or ["- _(none)_"])

    provided = r.get("provided") or []
    _add_section(parts, "Already provides",
                 [f"- {p}" for p in provided] or ["- _(none)_"])

    # hard gaps + soft flags are always shown (the brief lists "Missing hard
    # gaps" then the partition); the partition adds the on-hand view.
    gap = r.get("target_gap") or []
    if gap:
        _add_section(parts, "Missing — hard gaps", [f"- {g}" for g in gap])
    else:
        _add_section(parts, "Missing — hard gaps", ["- none — all target roles covered"])
    more = r.get("flagged_more") or []
    if more:
        _add_section(parts, "May want more", [f"- {m}" for m in more])

    if "available_now" in r:
        for title, lines in _partition_blocks(r):
            _add_section(parts, title, lines)

    # risks / avoid (mirror the UI: leans heavy / leans dry)
    risk_lines: list[str] = []
    if r.get("leans_heavy"):
        risk_lines.append("- leans heavy — favour acid / herb / crunch.")
    if r.get("leans_dry"):
        risk_lines.append("- leans dry — favour sauce / hydration / cream.")
    if risk_lines:
        _add_section(parts, "Risks", risk_lines)
    avoid: list[str] = []
    if r.get("leans_heavy"):
        avoid.append("more fat / cream")
    if r.get("leans_dry"):
        avoid.append("more dry items")
    if avoid:
        _add_section(parts, "Avoid adding more of", [f"- {a}" for a in avoid])

    no_profile = [it["name"] for it in (r.get("no_profile") or [])]
    if no_profile:
        _add_section(parts, "No balance profile for", [f"- {n}" for n in no_profile])

    parts.append("## Suggested next move")
    parts.append("")
    parts.append(_suggested_next_move(r))
    parts.append("")
    parts.extend(FOOTER_LINES)
    return "\n".join(parts)


def render_scout_markdown(rows: list[dict[str, Any]]) -> str:
    """Render query.scout_rows to Markdown, with the Scout disclaimer up front.
    Every row is experimental by construction (scout_rows filters on it)."""
    parts = ["# Scout — experimental pairings", "", SCOUT_DISCLAIMER, ""]
    if not rows:
        parts.append("No experimental pairings curated yet for this filter.")
        parts.append("")
        parts.extend(FOOTER_LINES)
        return "\n".join(parts)
    for r in rows:
        parts.append(f"## {r['filler']}")
        parts.append("")
        parts.append(f"- role: {r['role']}")
        subj = r.get("technique") or r.get("target") or "(general)"
        parts.append(f"- pairs with: {subj}")
        parts.append(f"- note: {r.get('notes') or '(none)'}")
        parts.append(f"- FI shop: {r.get('availability_class') or '—'}")
        parts.append("")
    parts.extend(FOOTER_LINES)
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# high-level helpers (take a connection; used by the CLI)
# ---------------------------------------------------------------------------

def branch_markdown(conn, ingredient: str, technique: str,
                    available_items: list[str] | None = None) -> str | None:
    """query.branch_card + (optionally) query.available_filter → Markdown.
    None if no such transformation. Empty/None available_items = plain view."""
    card = query.branch_card(conn, ingredient, technique)
    if not card:
        return None
    avail = available_items or None
    part = (query.available_filter(conn, card["transformation_id"], avail)
            if avail else None)
    return render_branch_markdown(card, part)


def component_markdown(conn, name: str,
                       available_items: list[str] | None = None) -> str | None:
    """query.component_card + (optionally) query.available_filter on the first
    producer → Markdown. None if no such component."""
    d = query.component_card(conn, name)
    if not d:
        return None
    avail = available_items or None
    part = None
    producers = d.get("produced_by") or []
    if avail and producers:
        part = query.available_filter(conn, producers[0]["transformation_id"], avail)
    return render_component_markdown(d, part)


def plate_markdown(conn, text: str,
                   available_items: list[str] | None = None) -> str:
    """query.plate_balance_detail → Markdown. Empty/None available_items takes
    the current (unfiltered) path — no partition keys in the result."""
    avail = available_items or None
    r = query.plate_balance_detail(conn, text, available_items=avail)
    return render_plate_markdown(r)


def scout_markdown(conn, ingredient: str | None = None,
                   technique: str | None = None) -> str:
    """query.scout_rows → Markdown with the Scout disclaimer."""
    rows = query.scout_rows(conn, technique=technique, ingredient=ingredient)
    return render_scout_markdown(rows)