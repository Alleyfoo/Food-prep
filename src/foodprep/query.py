"""Query engine — answers the brief's prompts against the SQLite db.

All queries are read-only and parameterised. The brief's target prompts:
  * "What can I do with tomatoes?"
  * "I roasted them — now what?"        (component-first)
  * "What can I add after making tomato sauce?"  (missing-role fillers)
  * "What can I batch-prep?"             (storage flags)
  * "What unlocks the most transformations?" (hub ingredient)
"""

from __future__ import annotations

import sqlite3
from typing import Any

CONFIDENCE_RANK = {"high": 4, "medium_high": 3, "medium": 2, "low": 1, "experimental": 0}


def _rank(conf: str | None) -> int:
    return CONFIDENCE_RANK.get(conf or "", 0)


def transformations_for_ingredient(
    conn: sqlite3.Connection, ingredient: str = "tomato"
) -> list[dict[str, Any]]:
    """Answer 'What can I do with tomatoes?' — every transformation branch."""
    rows = conn.execute(
        """
        SELECT t.transformation_id, tech.name AS technique,
               c.name AS component, t.flavour_shift, t.texture_shift,
               t.confidence, c.batch_prep_value, c.freezes_well, c.keeps_well
        FROM transformations t
        JOIN ingredients i  ON i.ingredient_id = t.ingredient_id
        JOIN techniques tech ON tech.technique_id = t.technique_id
        JOIN components c   ON c.component_id = t.output_component_id
        WHERE i.canonical_name = ?
        """,
        (ingredient,),
    ).fetchall()
    out = [dict(r) for r in rows]
    out.sort(key=lambda d: (-_rank(d["confidence"]), d["technique"]))
    return out


def transformation_by_technique(
    conn: sqlite3.Connection, technique: str, ingredient: str = "tomato"
) -> dict[str, Any] | None:
    """Resolve a single transformation record by technique name."""
    row = conn.execute(
        """
        SELECT t.transformation_id, tech.name AS technique,
               c.name AS component, t.flavour_shift, t.texture_shift,
               t.confidence, c.component_id
        FROM transformations t
        JOIN ingredients i  ON i.ingredient_id = t.ingredient_id
        JOIN techniques tech ON tech.technique_id = t.technique_id
        JOIN components c   ON c.component_id = t.output_component_id
        WHERE i.canonical_name = ? AND tech.name = ?
        """,
        (ingredient, technique),
    ).fetchone()
    return dict(row) if row else None


def missing_roles(conn: sqlite3.Connection, transformation_id: int) -> list[dict[str, Any]]:
    rows = conn.execute(
        """
        SELECT r.role_name, mr.priority, mr.note
        FROM transformation_missing_roles mr
        JOIN roles r ON r.role_id = mr.role_id
        WHERE mr.transformation_id = ?
        ORDER BY CASE mr.priority
                   WHEN 'high' THEN 0 WHEN 'medium' THEN 1 ELSE 2 END
        """,
        (transformation_id,),
    ).fetchall()
    return [dict(r) for r in rows]


def fillers_for_transformation(
    conn: sqlite3.Connection, transformation_id: int
) -> list[dict[str, Any]]:
    """Answer 'What can I add after making X?' — fillers ranked to fill the gaps."""
    rows = conn.execute(
        """
        SELECT p.pairing_id, ing.canonical_name AS filler, r.role_name AS role,
               p.common_context, p.availability_class, p.confidence
        FROM pairings p
        JOIN ingredients ing ON ing.ingredient_id = p.ingredient_id
        JOIN roles r         ON r.role_id = p.role_id
        WHERE p.works_best_with_transformation_id = ?
        """,
        (transformation_id,),
    ).fetchall()
    out = [dict(r) for r in rows]
    out.sort(key=lambda d: (-_rank(d["confidence"]), d["filler"]))
    return out


def fillers_by_role(
    conn: sqlite3.Connection, transformation_id: int
) -> dict[str, list[dict[str, Any]]]:
    """Group fillers by the missing role they satisfy — the briefing's core view."""
    gaps = {g["role_name"] for g in missing_roles(conn, transformation_id)}
    fillers = fillers_for_transformation(conn, transformation_id)
    by_role: dict[str, list[dict[str, Any]]] = {gap: [] for gap in gaps}
    for f in fillers:
        by_role.setdefault(f["role"], []).append(f)
    # only keep roles that are actually missing (the briefing's logic)
    return {r: v for r, v in by_role.items() if r in gaps}


def component_uses(conn: sqlite3.Connection, component_id: int) -> list[str]:
    rows = conn.execute(
        """
        SELECT d.name FROM component_uses cu
        JOIN dish_contexts d ON d.dish_context_id = cu.dish_context_id
        WHERE cu.component_id = ? ORDER BY d.name
        """,
        (component_id,),
    ).fetchall()
    return [r["name"] for r in rows]


def batch_prep(conn: sqlite3.Connection, ingredient: str = "tomato") -> list[dict[str, Any]]:
    """Answer 'What can I batch-prep from tomatoes for future meals?'."""
    rows = conn.execute(
        """
        SELECT tech.name AS technique, c.name AS component,
               c.batch_prep_value, c.freezes_well, c.keeps_well, t.confidence
        FROM transformations t
        JOIN ingredients i  ON i.ingredient_id = t.ingredient_id
        JOIN techniques tech ON tech.technique_id = t.technique_id
        JOIN components c   ON c.component_id = t.output_component_id
        WHERE i.canonical_name = ?
          AND c.batch_prep_value IN ('high','very_high')
        """,
        (ingredient,),
    ).fetchall()
    out = [dict(r) for r in rows]
    out.sort(key=lambda d: (-{"very_high": 2, "high": 1}.get(d["batch_prep_value"], 0),
                            -_rank(d["confidence"])))
    return out


def freezes_well(conn: sqlite3.Connection, ingredient: str = "tomato") -> list[dict[str, Any]]:
    rows = conn.execute(
        """
        SELECT tech.name AS technique, c.name AS component
        FROM transformations t
        JOIN ingredients i  ON i.ingredient_id = t.ingredient_id
        JOIN techniques tech ON tech.technique_id = t.technique_id
        JOIN components c   ON c.component_id = t.output_component_id
        WHERE i.canonical_name = ? AND c.freezes_well = 1
        """,
        (ingredient,),
    ).fetchall()
    return [dict(r) for r in rows]


def hub_ingredients(conn: sqlite3.Connection) -> list[dict[str, Any]]:
    """Answer 'What common ingredient unlocks the most tomato transformations?'."""
    rows = conn.execute(
        """
        SELECT ing.canonical_name AS filler,
               COUNT(DISTINCT p.works_best_with_transformation_id) AS transformations_covered,
               COUNT(DISTINCT r.role_name) AS roles_filled
        FROM pairings p
        JOIN ingredients ing ON ing.ingredient_id = p.ingredient_id
        JOIN roles r         ON r.role_id = p.role_id
        WHERE p.works_best_with_transformation_id IS NOT NULL
        GROUP BY ing.ingredient_id
        ORDER BY transformations_covered DESC, roles_filled DESC
        """,
    ).fetchall()
    return [dict(r) for r in rows]


# ---- prompt parsing --------------------------------------------------------

# (regex, technique). Order matters: first match wins. "can" is matched with a
# negative lookahead so the English modal in "what can I do" does not collide.
_TECHNIQUE_PATTERNS = [
    (r"\broast(?:ed)?\b", "roast"),
    (r"\bchar(?:red)?\b|\bgrill(?:ed)?\b|\bbroil(?:ed)?\b|\bsmok(?:e|ed|y)\b", "char"),
    (r"\bsimmer\b|\bsauce\b", "simmer"),
    (r"\breduc(?:e|ed)\b|\bpaste\b|\bconcentrat(?:e|ed)\b", "reduce"),
    (r"\bsalsa\b|\bpico\b", "salsa"),
    (r"\bsalt(?:ed)?\b.*\bdrain(?:ed)?\b|\bdrain(?:ed)?\b.*\bsalt(?:ed)?\b", "salt_and_drain"),
    (r"\bsoup\b", "soup"),
    (r"\bdri(?:ed|y)\b|\bdehydrat(?:e|ed)\b", "dry"),
    (r"\bpickle(?:d)?\b|\bchutney\b", "pickle"),
    (r"\bfrozen\b|\bfreeze\b", "freeze"),
    (r"\bcanned\b|\bcanning\b|\bcan\b(?!\s+(?:i|you|we|do))|\bpreserv(?:e|ed)\b", "can"),
    (r"\bsalt(?:ed)?\b", "salt_and_drain"),
    (r"\braw\b|\bfresh\b|\bsalad\b", "raw_assemble"),
]

_INTENT_KEYWORDS = {
    "batch": "batch",
    "prep": "batch",
    "freeze": "freeze_list",
    "hub": "hub",
    "unlock": "hub",
}


def parse_prompt(text: str) -> dict[str, Any]:
    """Loosely parse a free-text prompt into an intent + optional technique."""
    import re

    low = text.lower()
    intent = "branches"  # default: what can I do with tomatoes
    for kw, it in _INTENT_KEYWORDS.items():
        if kw in low:
            intent = it
            break
    technique = None
    for pattern, tech in _TECHNIQUE_PATTERNS:
        if re.search(pattern, low):
            technique = tech
            break
    # "I roasted them, now what" -> component-first intent
    if technique and intent == "branches" and (
        "now what" in low or "next" in low or "add" in low or "after" in low
    ):
        intent = "next"
    return {"intent": intent, "technique": technique, "raw": text}


def answer(conn: sqlite3.Connection, prompt: str) -> str:
    """Render a human-readable answer for a free-text prompt."""
    parsed = parse_prompt(prompt)
    intent = parsed["intent"]

    if intent == "batch":
        rows = batch_prep(conn)
        lines = ["Batch-prep from tomatoes (high/very-high reuse, future-meal friendly):"]
        for r in rows:
            lines.append(
                f"  - {r['technique']} -> {r['component']}  "
                f"(batch={r['batch_prep_value']}, freezes={bool(r['freezes_well'])}, "
                f"keeps={r['keeps_well']}, conf={r['confidence']})"
            )
        return "\n".join(lines) if len(lines) > 1 else "No batch-prep components found."

    if intent == "freeze_list":
        rows = freezes_well(conn)
        lines = ["Tomato components that freeze well:"]
        for r in rows:
            lines.append(f"  - {r['technique']} -> {r['component']}")
        return "\n".join(lines) if len(lines) > 1 else "No freezer-friendly components."

    if intent == "hub":
        rows = hub_ingredients(conn)
        lines = ["Ingredients that unlock the most tomato transformations:"]
        for r in rows[:10]:
            lines.append(
                f"  - {r['filler']}: covers {r['transformations_covered']} transformations, "
                f"{r['roles_filled']} roles"
            )
        return "\n".join(lines)

    # default / next
    tech = parsed["technique"]
    if intent == "next" and tech:
        tr = transformation_by_technique(conn, tech)
        if not tr:
            return f"I don't have a transformation for {tech!r}."
        gaps = fillers_by_role(conn, tr["transformation_id"])
        uses = component_uses(conn, tr["component_id"])
        lines = [f"After {tr['technique']} you have {tr['component']} "
                 f"(confidence {tr['confidence']})."]
        if gaps:
            lines.append("Still missing, and what fills it:")
            for role, fillers in gaps.items():
                names = ", ".join(f["filler"] for f in fillers[:4]) or "(no curated filler)"
                lines.append(f"  - {role}: {names}")
        else:
            lines.append("No curated missing roles for this branch.")
        if uses:
            lines.append("Use it in: " + ", ".join(uses))
        return "\n".join(lines)

    # branches: "what can I do with tomatoes"
    if tech:
        tr = transformation_by_technique(conn, tech)
        if tr:
            gaps = missing_roles(conn, tr["transformation_id"])
            uses = component_uses(conn, tr["component_id"])
            lines = [f"{tr['technique']} -> {tr['component']} (confidence {tr['confidence']})",
                     f"  flavour: {tr['flavour_shift']}",
                     f"  texture: {tr['texture_shift']}"]
            if gaps:
                lines.append("  still needs: " + ", ".join(g["role_name"] for g in gaps))
            if uses:
                lines.append("  use in: " + ", ".join(uses))
            return "\n".join(lines)
    rows = transformations_for_ingredient(conn)
    lines = ["What you can do with tomatoes:"]
    for r in rows:
        lines.append(
            f"  - {r['technique']} -> {r['component']}  "
            f"(conf={r['confidence']}, batch={r['batch_prep_value']}, "
            f"freezes={'Y' if r['freezes_well'] else 'N'})"
        )
    return "\n".join(lines)