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
    # ---- potato techniques ----
    (r"\bboil(?:ed|ing)?\b", "boil"),
    (r"\bmash(?:ed|ing|ed potato(?:es)?)?\b|\bmashed potato\b", "mash"),
    (r"\bfri(?:ed|es|ing)\b|\bfry\b|\bhash brown\b", "fry"),
    (r"\bgratin\b|\bdauphinois\b", "gratin"),
    (r"\bbak(?:ed|ing|e)\b", "bake"),
    (r"\bhash(?:ed|ing)?\b", "hash"),
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
# Profile missing_risks use cook language as well as role names. Map those cook
# terms to real roles so a profiled gap can still be filled. (sauce -> hydration,
# fresh_side / freshness -> herb.) Unmapped terms pass through unchanged.
MISSING_TERM_TO_ROLE = {"sauce": "hydration", "fresh_side": "herb", "freshness": "herb"}

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


def _plate_phrases(text: str) -> list[str]:
    """Best-effort: pull the plate-item noun phrases the user names.
    Supports 'I have X and Y', 'balance X and Y', 'plate of X and Y'.
    'I have mashed potatoes and roasted chickpea patties. What is missing?'
    -> ['mashed potatoes', 'roasted chickpea patties']"""
    low = text.lower()
    m = re.search(
        r"(?:i have|i've got|i got|balance|plate of|plate|with)\b\s*"
        r"(.*?)(?:\.|\?|!|what|how|which|$)",
        low,
    )
    if m:
        clause = m.group(1)
    else:
        # bare item list with no prefix (e.g. the `foodprep plate` CLI args):
        # treat the whole text as the item clause.
        clause = re.split(r"\bwhat\b|\bhow\b|\bwhich\b|[.?!]", low)[0]
    parts = re.split(r"\band\b|\balso\b|,", clause)
    out = []
    for p in parts:
        p = p.strip(" .,;:'\"")
        if 2 < len(p) <= 40 and not p.isdigit():
            out.append(p)
    return out


def _match_profile(conn: sqlite3.Connection, phrase: str) -> str | None:
    """Return the most specific component_profile name matching a phrase
    (via name or alias, longest match wins), or None if no profile fits.

    Also maps transformation-output component names (roasted_tomato_component,
    tomato_sauce_base) to profiles by stripping the _component / _base suffix."""
    p = phrase.lower()
    # normalise component-style names: roasted_tomato_component -> roasted tomato
    cleaned = (p.replace("_component", " ").replace("_base", " ")
               .replace("_", " "))
    cleaned = " ".join(cleaned.split())
    candidates = [p] if p != cleaned else [p]
    if p != cleaned:
        candidates = [cleaned, p]
    best, best_len = None, 0
    for r in conn.execute("SELECT name, aliases FROM component_profiles").fetchall():
        terms = [r["name"].replace("_", " ")] + _split_list(r["aliases"])
        for t in terms:
            t = t.lower()
            if not t:
                continue
            for cand in candidates:
                if t == cand or t in cand or cand in t:
                    if len(t) > best_len:
                        best, best_len = r["name"], len(t)
    return best


def _match_ingredient(conn: sqlite3.Connection, phrase: str) -> str | None:
    """Return the canonical ingredient name matching a phrase (name/alias,
    longest match wins), or None. Used so raw ingredients on a plate (garlic,
    onion, butter) contribute their base_roles even without a plate profile."""
    p = phrase.lower()
    best, best_len = None, 0
    for r in conn.execute(
        "SELECT canonical_name, aliases FROM ingredients"
    ).fetchall():
        terms = [r["canonical_name"]] + _split_list(r["aliases"])
        for t in terms:
            t = t.lower()
            if t and (t == p or t in p or p in t) and len(t) > best_len:
                best, best_len = r["canonical_name"], len(t)
    return best


def _canon_role(role: str) -> str:
    """Canonicalise a role/cook-term to a real role name."""
    return ROLE_CANON.get(role) or MISSING_TERM_TO_ROLE.get(role, role)


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
                      limit: int = 4, include_experimental: bool = False) -> list[str]:
    """Best fillers for a role across all pairings (any transformation).
    Ties on confidence are broken by versatility (how many pairings that filler
    has for the role) so olive_oil ranks above mozzarella for fat.

    Cook mode (default) excludes `experimental` pairings — those belong to Scout
    mode, surfaced via `scout()`. This keeps Cook and Scout answers separate."""
    rows = conn.execute(
        """
        SELECT ing.canonical_name AS filler,
               MAX(CASE p.confidence WHEN 'high' THEN 4 WHEN 'medium_high' THEN 3
                   WHEN 'medium' THEN 2 WHEN 'low' THEN 1 ELSE 0 END) AS rnk,
               COUNT(*) AS n
        FROM pairings p JOIN ingredients ing ON ing.ingredient_id = p.ingredient_id
        JOIN roles r ON r.role_id = p.role_id
        WHERE r.role_name = :role
          AND (:incl_exp = 1 OR p.confidence != 'experimental')
        GROUP BY ing.ingredient_id
        ORDER BY rnk DESC, COUNT(*) DESC
        LIMIT :limit
        """,
        {"role": role, "limit": limit, "incl_exp": 1 if include_experimental else 0},
    ).fetchall()
    return [r["filler"] for r in rows]


def _recognise_plate_item(conn: sqlite3.Connection, phrase: str) -> dict[str, Any]:
    """Recognise one plate-item phrase as a profile, an ingredient, or unknown.

    Returns {kind, name, provides, missing_risks, heaviness, dryness}:
      kind 'profile'    — a component_profile match (full balance data)
      kind 'ingredient' — a raw ingredient (base_roles as provides; no scores)
      kind 'unknown'    — neither, matched nothing
    """
    prof = _match_profile(conn, phrase)
    if prof:
        row = conn.execute(
            "SELECT provides_roles, missing_risks, heaviness_score, dryness_score "
            "FROM component_profiles WHERE name = ?", (prof,)
        ).fetchone()
        return {
            "kind": "profile", "name": prof,
            "provides": _split_list(row["provides_roles"]),
            "missing_risks": _split_list(row["missing_risks"]),
            "heaviness": row["heaviness_score"],
            "dryness": row["dryness_score"],
        }
    ing = _match_ingredient(conn, phrase)
    if ing:
        row = conn.execute(
            "SELECT base_roles FROM ingredients WHERE canonical_name = ?", (ing,)
        ).fetchone()
        return {
            "kind": "ingredient", "name": ing,
            "provides": _split_list(row["base_roles"]),
            "missing_risks": [], "heaviness": None, "dryness": None,
        }
    return {"kind": "unknown", "name": phrase, "provides": [],
            "missing_risks": [], "heaviness": None, "dryness": None}


def _heaviness_label(avg: float) -> str:
    if avg >= 4:
        return "heavy"
    if avg >= 3:
        return "rich"
    if avg >= 2:
        return "balanced"
    return "light"


def _dryness_label(avg: float) -> str:
    if avg >= 3.5:
        return "dry"
    if avg >= 2:
        return "medium"
    return "moist"


def plate_balance(conn: sqlite3.Connection, text: str) -> str:
    """Plate Balance Engine (Cook mode).

    Evaluates a set of known component profiles / ingredients on a plate:
      - aggregates provided roles (from profiles + ingredient base_roles)
      - aggregates missing_risks from profiles (cook terms canonicalised)
      - computes plate-level heaviness and dryness with a plain-English read
      - suggests missing roles (balanced-target gap ∪ item missing_risks)
      - suggests fillers grouped by role (Cook mode: no experimental pairings)
      - warns about items with no component profile (incl. known ingredients
        that lack balance data, and fully unknown items)

    Honest about its limits — it never invents roles or fillers it doesn't have.
    """
    phrases = _plate_phrases(text)
    items = [_recognise_plate_item(conn, ph) for ph in phrases]

    profiles = [it for it in items if it["kind"] == "profile"]
    no_profile = [it for it in items if it["kind"] != "profile"]  # ingredient or unknown

    # ---- aggregate provided roles (canonicalised) ----
    provided: set[str] = set()
    for it in items:
        for role in it["provides"]:
            provided.add(_canon_role(role))

    # ---- aggregate missing_risks from profiles (canonicalised) ----
    risk_roles: set[str] = set()
    for it in profiles:
        for role in it["missing_risks"]:
            risk_roles.add(_canon_role(role))

    # ---- plate-level heaviness / dryness (from profiled items only) ----
    h_vals = [it["heaviness"] for it in profiles if it["heaviness"] is not None]
    d_vals = [it["dryness"] for it in profiles if it["dryness"] is not None]
    plate_h = sum(h_vals) if h_vals else None
    plate_d = sum(d_vals) if d_vals else None
    h_avg = plate_h / len(h_vals) if h_vals else None
    d_avg = plate_d / len(d_vals) if d_vals else None

    # ---- suggested missing roles ----
    # Hard gaps = target roles no item provides. These definitely need filling.
    target_gap = [r for r in TARGET_ROLES if r not in provided]
    # "may want more" = roles flagged by a profile's missing_risks even though
    # some item provides them (e.g. roasted tomato provides acid but may want
    # more if too sweet). These are soft suggestions, not hard gaps.
    flagged_more = sorted(r for r in risk_roles if r not in set(target_gap))

    # ---- render (Cook mode) ----
    if not items:
        return ("Plate balance — Cook mode\n"
                "Name the plate items, e.g. 'balance mashed potatoes and "
                "chickpea patties' or 'I have X and Y, what is missing?'")
    have_parts = []
    for it in items:
        tag = {"profile": "profile", "ingredient": "ingredient",
               "unknown": "unknown"}[it["kind"]]
        have_parts.append(f"{it['name']} ({tag})")
    lines = ["Plate balance — Cook mode",
            f"You have: {', '.join(have_parts)}"]

    if no_profile:
        names = []
        for it in no_profile:
            label = "unknown item" if it["kind"] == "unknown" else "known ingredient, no balance data"
            names.append(f"{it['name']} ({label})")
        lines.append(
            "  no profile for: " + ", ".join(names)
            + " — add component_profiles entries for heaviness/dryness/missing-risk data."
        )

    prov_disp = sorted(provided)
    lines.append("  provided roles: " + (", ".join(prov_disp) if prov_disp else "(none)"))

    if plate_h is not None:
        lines.append(f"  plate heaviness: {plate_h}  ({_heaviness_label(h_avg)})")
    else:
        lines.append("  plate heaviness: unknown (no profiled items)")
    if plate_d is not None:
        lines.append(f"  plate dryness: {plate_d}  ({_dryness_label(d_avg)})")
    else:
        lines.append("  plate dryness: unknown (no profiled items)")

    if h_avg is not None and h_avg >= 4:
        lines.append("  leans heavy — favor acid/herb/crunch; avoid more fat/cream.")
    if d_avg is not None and d_avg >= 3.5:
        lines.append("  leans dry — favor sauce/hydration/cream.")

    if not target_gap and not flagged_more:
        lines.append("  balanced — nothing essential missing.")
        return "\n".join(lines)

    if target_gap:
        lines.append("  missing for a balanced plate: " + ", ".join(target_gap))
        lines.append("  add:")
        for role in target_gap:
            fillers = _fillers_for_role(conn, role)
            lines.append(f"    - {role}: " + (", ".join(fillers) if fillers else "(no curated filler)"))
    else:
        lines.append("  no hard gaps — all target roles are covered.")

    if flagged_more:
        lines.append("  also flagged by item profiles (may want more): " + ", ".join(flagged_more))
        for role in flagged_more:
            fillers = _fillers_for_role(conn, role)
            lines.append(f"    - {role}: " + (", ".join(fillers) if fillers else "(no curated filler)"))
    return "\n".join(lines)


def meal_repair(conn: sqlite3.Connection, text: str) -> str:
    """Backward-compat wrapper — the plate balance engine (Cook mode)."""
    return plate_balance(conn, text)


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


def _has_transformations(conn: sqlite3.Connection, ingredient: str) -> bool:
    """True if this ingredient has a technique tree (full or both)."""
    row = conn.execute(
        """SELECT COUNT(*) FROM transformations t
           JOIN ingredients i ON i.ingredient_id = t.ingredient_id
           WHERE i.canonical_name = ?""",
        (ingredient,),
    ).fetchone()
    return row[0] > 0


def _detect_subject(text: str, conn: sqlite3.Connection) -> str | None:
    """Detect ANY ingredient named in the prompt (including fillers), longest
    name wins. Unlike _detect_ingredient, this also matches fillers that have no
    transformation tree — so 'what can I do with lemon' can route to a filler
    profile instead of falling through to tomato branches."""
    low = text.lower()
    best, best_len = None, 0
    for r in conn.execute("SELECT canonical_name, aliases FROM ingredients").fetchall():
        for n in [r["canonical_name"]] + _split_list(r["aliases"]):
            nl = n.lower()
            if nl and nl in low and len(nl) > best_len:
                best, best_len = r["canonical_name"], len(nl)
    return best


def filler_profile(conn: sqlite3.Connection, name: str) -> str:
    """Answer the five filler questions for one ingredient:
      1. what roles does this fill?      (base_roles)
      2. what kinds of plates does it repair?  (repairs)
      3. what should it not be used for? (avoid_when)
      4. is it common in Finnish supermarket reality? (availability)
      5. is it Cook or Scout?             (derived from its pairings:
         any non-experimental -> Cook; experimental-only -> Scout)

    repairs / avoid_when are per-filler profile data — they are NOT a
    plate-condition matcher inside plate_balance (that would flatten the model;
    see docs/ARCHITECTURE_CHECKPOINT_ROUND_4.md). They are surfaced here so a
    human (or agent) can read a filler's culinary contract at a glance.
    """
    row = conn.execute(
        "SELECT canonical_name, aliases, base_roles, default_availability_class, "
        "kind, repairs, avoid_when FROM ingredients WHERE canonical_name = ?",
        (name,),
    ).fetchone()
    if row is None:
        canon = _match_ingredient(conn, name)
        if canon:
            return filler_profile(conn, canon)
        return f"No ingredient named {name!r}."
    roles = _split_list(row["base_roles"])
    repairs = _split_list(row["repairs"])
    avoid = _split_list(row["avoid_when"])
    avail = row["default_availability_class"] or "(unspecified)"

    prs = conn.execute(
        """SELECT r.role_name AS role, p.confidence AS conf,
                  ti.canonical_name AS target, tech.name AS technique
           FROM pairings p
           JOIN roles r ON r.role_id = p.role_id
           JOIN ingredients i ON i.ingredient_id = p.ingredient_id
           LEFT JOIN transformations t ON t.transformation_id = p.works_best_with_transformation_id
           LEFT JOIN ingredients ti ON ti.ingredient_id = t.ingredient_id
           LEFT JOIN techniques tech ON tech.technique_id = t.technique_id
           WHERE i.canonical_name = ?
           ORDER BY CASE p.confidence WHEN 'high' THEN 4 WHEN 'medium_high' THEN 3
                     WHEN 'medium' THEN 2 WHEN 'low' THEN 1 ELSE 0 END DESC""",
        (name,),
    ).fetchall()
    n_cook = sum(1 for p in prs if p["conf"] != "experimental")
    n_exp = sum(1 for p in prs if p["conf"] == "experimental")
    if n_cook and n_exp:
        mode = f"Cook (also has {n_exp} Scout/experimental pairing{'s' if n_exp != 1 else ''})"
    elif n_cook:
        mode = f"Cook ({n_cook} non-experimental pairing{'s' if n_cook != 1 else ''})"
    elif n_exp:
        mode = (f"Scout / experimental ({n_exp} experimental pairing"
                f"{'s' if n_exp != 1 else ''}; no classic pairings yet)")
    else:
        mode = "no pairings yet — not suggested by the plate engine"

    kind = row["kind"]
    if kind == "full":
        header = (f"{row['canonical_name']} — full ingredient (has a technique tree; "
                  f"ask 'what can I do with {row['canonical_name']}')")
    elif kind == "both":
        header = f"{row['canonical_name']} — both (technique tree + filler) profile"
    else:
        header = f"{row['canonical_name']} — filler profile"
    lines = [header]
    lines.append("  roles filled: " + (", ".join(roles) if roles else "(none)"))
    lines.append("  repairs plates that are: " + (", ".join(repairs) if repairs else "(unspecified)"))
    lines.append("  avoid when: " + (", ".join(avoid) if avoid else "(unspecified)"))
    lines.append(f"  Finnish supermarket: {avail}")
    lines.append(f"  mode: {mode}")
    seen = []
    for p in prs[:6]:
        tgt = f"{p['target']} {p['technique']}" if p["target"] else "(general)"
        seen.append(f"{p['role']} for {tgt}")
    if seen:
        lines.append("  paired with: " + "; ".join(seen))
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

    # ---- plate balance (Cook mode): "balance / plate of / what is missing" + items ----
    phrases = _plate_phrases(prompt)
    wants_balance = (
        "balance" in low or "plate of" in low or "plate balance" in low
        or (("missing" in low or "what should i add" in low or "what taste" in low)
            and len(phrases) >= 2)
    )
    if wants_balance:
        return plate_balance(conn, prompt)

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

    # ---- filler profile: subject is a filler (no technique tree) ----
    # "what can I do with lemon", "what does mustard repair", "tell me about
    # sauerkraut" — a filler has no branches, so it routes to its profile
    # (roles / repairs / avoid_when / availability / Cook-or-Scout) instead of
    # falling through to tomato branches. Full/both ingredients (tomato, onion,
    # potato) have transformations, so they skip this and keep their branch view.
    subject = _detect_subject(prompt, conn)
    if subject and not _has_transformations(conn, subject):
        return filler_profile(conn, subject)

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