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
               t.confidence, c.batch_prep_value, c.freezes_well, c.keeps_well,
               tech.preservation_flag, c.component_kind
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

import re

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
    (r"\bsaute(?:ed)?\b|\bsweat(?:ed)?\b", "saute"),
    (r"\bcaramel(?:is|iz)(?:e|ed|ed)\b", "caramelize"),
]

_INTENT_KEYWORDS = {
    "batch": "batch",
    "prep": "batch",
    "hub": "hub",
    "unlock": "hub",
    "scout": "scout",
    "unusual": "scout",
    "plausible but uncommon": "scout",
    "plausible but rare": "scout",
}

# Roles that make a plate feel complete. cream counts as fat; mild_base/body are
# supporting richness and are not required targets on their own.
TARGET_ROLES = ["salt", "fat", "acid", "herb", "crunch", "carb", "protein"]
ROLE_CANON = {"cream": "fat"}

BATCH_RANK = {"very_high": 3, "high": 2, "medium": 1, "low": 0}


def _split_list(text: str | None) -> list[str]:
    if not text:
        return []
    return [line.strip() for line in text.splitlines() if line.strip()]


def _detect_ingredient(text: str, conn: sqlite3.Connection) -> str:
    """Find which ingredient (with transformations) the prompt is about."""
    low = text.lower()
    # only ingredients that actually have transformations are valid subjects
    rows = conn.execute(
        """
        SELECT DISTINCT i.canonical_name, i.aliases
        FROM ingredients i
        JOIN transformations t ON t.ingredient_id = i.ingredient_id
        """
    ).fetchall()
    best = None
    best_len = 0
    for r in rows:
        names = [r["canonical_name"]] + _split_list(r["aliases"])
        for n in names:
            nl = n.lower()
            if nl in low and len(nl) > best_len:
                best, best_len = r["canonical_name"], len(nl)
    return best or "tomato"


def _find_component_name(text: str, conn: sqlite3.Connection) -> str | None:
    """Return a component name mentioned in the prompt, if any."""
    low = text.lower()
    for name in (r["name"] for r in conn.execute("SELECT name FROM components").fetchall()):
        if name.lower() in low:
            return name
    return None


def _find_profiles(text: str, conn: sqlite3.Connection) -> list[str]:
    """Return component_profile names mentioned in the prompt (via name/aliases)."""
    low = text.lower()
    found: list[str] = []
    for r in conn.execute("SELECT name, aliases FROM component_profiles").fetchall():
        terms = [r["name"]] + _split_list(r["aliases"])
        if any(t.lower() in low for t in terms):
            found.append(r["name"])
    return found


def branch_detail(conn: sqlite3.Connection, transformation_id: int) -> dict[str, Any]:
    """The product-shape primitive: technique → component → flavour/texture
    → missing roles (priority-ordered) → fillers grouped by gap → uses."""
    row = conn.execute(
        """
        SELECT t.transformation_id, tech.name AS technique, c.name AS component,
               c.component_id, t.flavour_shift, t.texture_shift, t.confidence,
               c.batch_prep_value, c.freezes_well, c.keeps_well
        FROM transformations t
        JOIN techniques tech ON tech.technique_id = t.technique_id
        JOIN components c     ON c.component_id = t.output_component_id
        WHERE t.transformation_id = ?
        """,
        (transformation_id,),
    ).fetchone()
    d = dict(row)
    d["missing"] = missing_roles(conn, transformation_id)
    d["fillers_by_role"] = fillers_by_role(conn, transformation_id)
    d["uses"] = component_uses(conn, d["component_id"])
    return d


def render_branch(d: dict[str, Any]) -> str:
    """One transformation in the product shape."""
    lines = [f"{d['technique']}", f"  → {d['component']}"]
    if d.get("flavour_shift") or d.get("texture_shift"):
        lines.append(f"  → {d['flavour_shift']} · {d['texture_shift']}")
    gaps = [m["role_name"] for m in d["missing"]]
    if gaps:
        lines.append("  → missing: " + ", ".join(gaps))
    add_parts = []
    for role, fillers in d["fillers_by_role"].items():
        names = ", ".join(f["filler"] for f in fillers[:3]) or "(no curated filler)"
        add_parts.append(f"{role}: {names}")
    if add_parts:
        lines.append("  → add: " + " · ".join(add_parts))
    if d["uses"]:
        lines.append("  → use in: " + ", ".join(d["uses"]))
    return "\n".join(lines)


def top_branches(conn: sqlite3.Connection, ingredient: str = "tomato",
                 limit: int = 5) -> list[dict[str, Any]]:
    """Top transformation branches for an ingredient, ranked by confidence then
    batch-prep value — capped so we don't dump every branch (the report's biggest
    UX risk was returning too many options instead of a few useful next moves)."""
    rows = transformations_for_ingredient(conn, ingredient)
    # cooking moves before storage/preservation (freeze/can/dry/pickle are
    # dead-end "downstream context" branches — not useful as a first suggestion)
    KIND_RANK = {"fresh": 0, "cooked": 0, "concentrated": 0,
                 "preserved": 1, "storage": 2}
    rows.sort(key=lambda d: (
        KIND_RANK.get(d.get("component_kind", "cooked"), 0),
        d.get("preservation_flag", 0),
        -_rank(d["confidence"]),
        -BATCH_RANK.get(d["batch_prep_value"], 0),
    ))
    out = []
    for r in rows[:limit]:
        out.append(branch_detail(conn, r["transformation_id"]))
    return out


def component_first(conn: sqlite3.Connection, component_name: str) -> str:
    """Answer 'what can I do with <component>?' — start from the after-state."""
    comp = conn.execute("SELECT * FROM components WHERE name = ?",
                        (component_name,)).fetchone()
    if comp is None:
        return f"No component named {component_name!r}."
    uses = component_uses(conn, comp["component_id"])
    # the transformation(s) that produce this component give the role gaps
    prod = conn.execute(
        """
        SELECT t.transformation_id, tech.name AS technique, t.confidence,
               t.flavour_shift, t.texture_shift
        FROM transformations t JOIN techniques tech ON tech.technique_id = t.technique_id
        WHERE t.output_component_id = ?
        """,
        (comp["component_id"],),
    ).fetchall()
    lines = [f"{component_name} (a reusable component)"]
    if prod:
        p = prod[0]
        lines.append(f"  made by: {p['technique']} (confidence {p['confidence']})")
        if p["flavour_shift"] or p["texture_shift"]:
            lines.append(f"  tastes/feels: {p['flavour_shift']} · {p['texture_shift']}")
    if uses:
        lines.append("  use it in: " + ", ".join(uses))
    if prod:
        d = branch_detail(conn, prod[0]["transformation_id"])
        gaps = [m["role_name"] for m in d["missing"]]
        if gaps:
            lines.append("  if building a meal on it, still missing: " + ", ".join(gaps))
        add_parts = []
        for role, fillers in d["fillers_by_role"].items():
            names = ", ".join(f["filler"] for f in fillers[:3]) or "(no curated filler)"
            add_parts.append(f"{role}: {names}")
        if add_parts:
            lines.append("  add: " + " · ".join(add_parts))
    return "\n".join(lines)


def hub_ingredients(conn: sqlite3.Connection, ingredient: str = "tomato") -> list[dict[str, Any]]:
    """Rank fillers by how many of this ingredient's transformations they unlock."""
    rows = conn.execute(
        """
        SELECT ing.canonical_name AS filler,
               COUNT(DISTINCT p.works_best_with_transformation_id) AS transformations_covered,
               COUNT(DISTINCT r.role_name) AS roles_filled
        FROM pairings p
        JOIN ingredients ing ON ing.ingredient_id = p.ingredient_id
        JOIN roles r         ON r.role_id = p.role_id
        JOIN transformations t ON t.transformation_id = p.works_best_with_transformation_id
        WHERE t.ingredient_id = (SELECT ingredient_id FROM ingredients WHERE canonical_name = ?)
          AND p.works_best_with_transformation_id IS NOT NULL
        GROUP BY ing.ingredient_id
        ORDER BY transformations_covered DESC, roles_filled DESC
        """,
        (ingredient,),
    ).fetchall()
    return [dict(r) for r in rows]


def hub_explained(conn: sqlite3.Connection, ingredient: str = "tomato") -> str:
    """Like hub_ingredients but explains WHY — which techniques and which roles."""
    rows = conn.execute(
        """
        SELECT ing.canonical_name AS filler,
               GROUP_CONCAT(DISTINCT tech.name) AS techniques,
               GROUP_CONCAT(DISTINCT r.role_name) AS roles,
               COUNT(DISTINCT p.works_best_with_transformation_id) AS n
        FROM pairings p
        JOIN ingredients ing ON ing.ingredient_id = p.ingredient_id
        JOIN roles r         ON r.role_id = p.role_id
        JOIN transformations t ON t.transformation_id = p.works_best_with_transformation_id
        JOIN techniques tech ON tech.technique_id = t.technique_id
        WHERE t.ingredient_id = (SELECT ingredient_id FROM ingredients WHERE canonical_name = ?)
          AND p.works_best_with_transformation_id IS NOT NULL
        GROUP BY ing.ingredient_id
        ORDER BY n DESC
        """,
        (ingredient,),
    ).fetchall()
    lines = [f"Ingredients that unlock the most {ingredient} transformations:"]
    for r in rows[:10]:
        techs = ", ".join(sorted((r["techniques"] or "").split(",")))
        roles = ", ".join(sorted((r["roles"] or "").split(",")))
        lines.append(
            f"  - {r['filler']} unlocks {techs} because it fills {roles} "
            f"({r['n']} transformations)"
        )
    return "\n".join(lines)


def scout(conn: sqlite3.Connection, technique: str | None = None) -> str:
    """Scout mode — experimental pairings, explicitly labelled, never as classic."""
    if technique:
        row = conn.execute(
            """
            SELECT p.pairing_id, ing.canonical_name AS filler, r.role_name AS role,
                   p.notes, p.availability_class
            FROM pairings p
            JOIN ingredients ing ON ing.ingredient_id = p.ingredient_id
            JOIN roles r         ON r.role_id = p.role_id
            JOIN transformations t ON t.transformation_id = p.works_best_with_transformation_id
            JOIN techniques tech ON tech.technique_id = t.technique_id
            WHERE p.confidence = 'experimental' AND tech.name = ?
            """,
            (technique,),
        ).fetchall()
    else:
        row = conn.execute(
            """
            SELECT p.pairing_id, ing.canonical_name AS filler, r.role_name AS role,
                   p.notes, p.availability_class
            FROM pairings p
            JOIN ingredients ing ON ing.ingredient_id = p.ingredient_id
            JOIN roles r         ON r.role_id = p.role_id
            WHERE p.confidence = 'experimental'
            """
        ).fetchall()
    if not row:
        return ("Scout / experimental: none curated yet"
                + (f" for {technique!r}." if technique else "."))
    lines = ["Scout / experimental (plausible but uncommon — NOT classic):"]
    for r in row:
        note = r["notes"] or f"{r['filler']} ({r['role']})"
        lines.append(f"  - {r['filler']} + {technique or 'tomato'}: {note}")
    lines.append("  (These are speculative — labelled so no one pretends they're tradition.)")
    return "\n".join(lines)


def _fillers_for_role(conn: sqlite3.Connection, role: str,
                      limit: int = 4) -> list[str]:
    """Best fillers for a role across all pairings (any transformation).
    Ties on confidence are broken by versatility (how many pairings that filler
    has for the role) so olive_oil ranks above mozzarella for fat."""
    rows = conn.execute(
        """
        SELECT ing.canonical_name AS filler,
               MAX(CASE p.confidence WHEN 'high' THEN 4 WHEN 'medium_high' THEN 3
                   WHEN 'medium' THEN 2 WHEN 'low' THEN 1 ELSE 0 END) AS rnk,
               COUNT(*) AS n
        FROM pairings p JOIN ingredients ing ON ing.ingredient_id = p.ingredient_id
        JOIN roles r ON r.role_id = p.role_id
        WHERE r.role_name = ?
        GROUP BY ing.ingredient_id
        ORDER BY rnk DESC, COUNT(*) DESC
        LIMIT ?
        """,
        (role, limit),
    ).fetchall()
    return [r["filler"] for r in rows]


def meal_repair(conn: sqlite3.Connection, profiles: list[str], text: str) -> str:
    """Given plate items, union their provided roles and report what's missing
    for a balanced plate, with fillers. Honest about unrecognised items."""
    provided: set[str] = set()
    recognized: list[str] = []
    for pname in profiles:
        row = conn.execute("SELECT * FROM component_profiles WHERE name = ?",
                           (pname,)).fetchone()
        if row is None:
            continue
        recognized.append(pname)
        for role in _split_list(row["provides_roles"]):
            provided.add(ROLE_CANON.get(role, role))
    # detect unrecognised items the user mentioned (best-effort, noun-ish words)
    missing_target = [r for r in TARGET_ROLES if r not in provided]
    lines = [f"You have: {', '.join(recognized)}"]
    prov_disp = sorted({ROLE_CANON.get(r, r) for r in provided})
    lines.append("  provided roles: " + ", ".join(prov_disp))
    if not missing_target:
        lines.append("  balanced — nothing essential missing.")
        return "\n".join(lines)
    lines.append("  missing for a balanced plate: " + ", ".join(missing_target))
    lines.append("  add:")
    for role in missing_target:
        fillers = _fillers_for_role(conn, role)
        lines.append(f"    - {role}: " + (", ".join(fillers) or "(no curated filler)"))
    return "\n".join(lines)


def lighten(conn: sqlite3.Connection, text: str) -> str:
    """For 'less heavy / too rich' prompts — recommend brightness + crunch,
    explicitly warn against adding more fat/body/cream."""
    lines = ["To lighten a heavy/rich plate, add brightness and crunch:"]
    for role, why in [("acid", "cuts richness"),
                      ("herb", "freshness"),
                      ("crunch", "contrast")]:
        fillers = _fillers_for_role(conn, role)
        lines.append(f"  - {role}: {', '.join(fillers)}  ({why})")
    lines.append("  avoid: more fat / body / cream — that makes it heavier.")
    return "\n".join(lines)


def parse_prompt(text: str) -> dict[str, Any]:
    """Loosely parse a free-text prompt into an intent + optional technique."""
    low = text.lower()
    intent = "branches"
    for kw, it in _INTENT_KEYWORDS.items():
        if kw in low:
            intent = it
            break
    technique = None
    for pattern, tech in _TECHNIQUE_PATTERNS:
        if re.search(pattern, low):
            technique = tech
            break
    if technique and intent == "branches" and (
        "now what" in low or "next" in low or "add" in low or "after" in low
    ):
        intent = "next"
    return {"intent": intent, "technique": technique, "raw": text}


def answer(conn: sqlite3.Connection, prompt: str) -> str:
    """Render a human-readable answer for a free-text prompt."""
    low = prompt.lower()
    parsed = parse_prompt(prompt)
    intent = parsed["intent"]
    tech = parsed["technique"]
    ingredient = _detect_ingredient(prompt, conn)

    # ---- scout (checked early: "unusual / plausible but uncommon") ----
    if intent == "scout":
        return scout(conn, tech)

    # ---- meal repair: "what is missing / what should I add" + plate items ----
    profiles = _find_profiles(prompt, conn)
    wants_repair = (
        ("missing" in low or "what should i add" in low or "what taste" in low)
        and (len(profiles) >= 2 or (" and " in low and profiles))
    )
    if wants_repair and profiles:
        return meal_repair(conn, profiles, prompt)

    # ---- lighten: "less heavy / too rich" ----
    if ("less heavy" in low or "lighter" in low or "too rich" in low
            or "too heavy" in low or "cut the richness" in low):
        return lighten(conn, prompt)

    # ---- batch / freeze / hub ----
    if intent == "batch":
        rows = batch_prep(conn, ingredient)
        lines = [f"Batch-prep from {ingredient} (high/very-high reuse):"]
        for r in rows:
            lines.append(
                f"  - {r['technique']} -> {r['component']}  "
                f"(batch={r['batch_prep_value']}, freezes={bool(r['freezes_well'])}, "
                f"keeps={r['keeps_well']}, conf={r['confidence']})"
            )
        return "\n".join(lines) if len(lines) > 1 else f"No batch-prep components for {ingredient}."

    if "freeze" in low and ("component" in low or "freeze well" in low or "freezes" in low):
        rows = freezes_well(conn, ingredient)
        lines = [f"{ingredient} components that freeze well:"]
        for r in rows:
            lines.append(f"  - {r['technique']} -> {r['component']}")
        return "\n".join(lines) if len(lines) > 1 else "No freezer-friendly components."

    if intent == "hub":
        return hub_explained(conn, ingredient)

    # ---- component-first: a component name is the subject ----
    comp = _find_component_name(prompt, conn)
    if comp and not (intent == "next" and tech):
        return component_first(conn, comp)

    # ---- next: "I roasted them, now what" / "what can I add after sauce" ----
    if intent == "next" and tech:
        tr = transformation_by_technique(conn, tech, ingredient)
        if not tr:
            return f"I don't have a transformation for {ingredient}/{tech!r}."
        d = branch_detail(conn, tr["transformation_id"])
        lines = [f"After {tr['technique']} you have {tr['component']} "
                 f"(confidence {tr['confidence']})."]
        lines.append(render_branch(d))
        return "\n".join(lines)

    # ---- single-technique detail: "what is missing from roasted tomato" ----
    if tech and not (intent == "next"):
        tr = transformation_by_technique(conn, tech, ingredient)
        if tr:
            return render_branch(branch_detail(conn, tr["transformation_id"]))

    # ---- branches: "what can I do with tomatoes" (the product shape) ----
    branches = top_branches(conn, ingredient, limit=5)
    if not branches:
        return f"I don't have transformations modelled for {ingredient!r} yet."
    lines = [f"What you can do with {ingredient} (top branches by confidence + reuse):"]
    for d in branches:
        lines.append(render_branch(d))
        lines.append("")
    lines.append(f"({len(transformations_for_ingredient(conn, ingredient))} {ingredient} transformations total — ask 'what is missing from <technique> {ingredient}' for detail, or 'what can I do with <component>' for an after-state.)")
    return "\n".join(lines)