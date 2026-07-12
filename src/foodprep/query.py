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
    conn: sqlite3.Connection, transformation_id: int,
    include_experimental: bool = False,
) -> list[dict[str, Any]]:
    """Answer 'What can I add after making X?' — fillers ranked to fill the gaps.

    Cook mode by default (excludes `experimental` pairings — those belong to
    Scout mode, surfaced via `scout()`). Pass include_experimental=True to also
    list speculative pairings (used nowhere in the Cook UI; available for a
    future 'show me everything' view)."""
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
    out = [dict(r) for r in rows if include_experimental or r["confidence"] != "experimental"]
    out.sort(key=lambda d: (-_rank(d["confidence"]), d["filler"]))
    return out


def fillers_by_role(
    conn: sqlite3.Connection, transformation_id: int,
    include_experimental: bool = False,
) -> dict[str, list[dict[str, Any]]]:
    """Group fillers by the missing role they satisfy — the briefing's core view.

    Cook mode by default (experimental pairings excluded); the Scout tab reaches
    experimental pairings via `scout_rows`, not here, so the branch/component
    Cook views stay clean of Scout-only suggestions."""
    gaps = {g["role_name"] for g in missing_roles(conn, transformation_id)}
    fillers = fillers_for_transformation(conn, transformation_id, include_experimental)
    by_role: dict[str, list[dict[str, Any]]] = {gap: [] for gap in gaps}
    for f in fillers:
        by_role.setdefault(f["role"], []).append(f)
    # only keep roles that are actually missing (the briefing's logic)
    return {r: v for r, v in by_role.items() if r in gaps}


def _partition_by_available(by_role_names: dict[str, list[str]],
                            available: set[str],
                            known: set[str]) -> dict[str, Any]:
    """Split a {role: [filler_name]} map (Cook mode — no experimental) against
    the ingredients the user has on hand.

    Returns:
      available_now      — [{filler, roles}] fillers the user has that fill
                            >=1 role, with the roles they cover.
      missing_but_useful — [{role, fillers}] roles not covered by any available
                            filler; fillers = the unavailable curated fillers
                            that WOULD fill it ([] if none curated).
      unknown_items      — [item] selected items not recognised as ingredients.
      no_match_known     — [item] recognised selected items that fill no missing
                            role for this branch/plate (available but useless
                            here).
      covered_roles      — [role] roles with >=1 available filler.

    Honest: never invents fillers; unknown selections are reported, not
    silently dropped. Scout/experimental never leaks in — callers feed it
    Cook-only filler lists (fillers_by_role / _fillers_for_role).
    """
    filler_roles: dict[str, list[str]] = {}
    for role, names in by_role_names.items():
        for f in names:
            if f in available:
                filler_roles.setdefault(f, []).append(role)
    available_now = [
        {"filler": f, "roles": sorted(rs)} for f, rs in sorted(filler_roles.items())
    ]
    covered = {r for grp in available_now for r in grp["roles"]}
    missing_but_useful = [
        {"role": role, "fillers": [n for n in names if n not in available]}
        for role, names in by_role_names.items() if role not in covered
    ]
    used = {grp["filler"] for grp in available_now}
    unknown_items = sorted(a for a in available if a not in known)
    no_match_known = sorted(a for a in available if a in known and a not in used)
    return {
        "available_now": available_now,
        "missing_but_useful": missing_but_useful,
        "unknown_items": unknown_items,
        "no_match_known": no_match_known,
        "covered_roles": sorted(covered),
    }


def available_filter(conn: sqlite3.Connection, transformation_id: int,
                      available_items: list[str] | None) -> dict[str, Any]:
    """Round 11 — 'What do I have right now?' for a single transformation branch.

    Partitions the branch's Cook fillers against the ingredients on hand into
    Available now / Missing but useful / No match. None or [] available_items
    behaves like the current system: available_now empty, missing_but_useful
    = every role with all its curated fillers (the existing Try view), and the
    UI falls back to the plain role->fillers render.

    Cook-only — Scout/experimental pairings (lingonberry_vinegar, walnut, ...)
    never appear here even if selected; they stay in scout_rows.
    """
    available = {a.strip() for a in (available_items or []) if a and a.strip()}
    missing = missing_roles(conn, transformation_id)            # priority-ordered
    by_role = fillers_by_role(conn, transformation_id)        # Cook, no experimental
    by_role_names = {
        m["role_name"]: [f["filler"] for f in by_role.get(m["role_name"], [])]
        for m in missing
    }
    known = set(ingredients_list(conn))
    return _partition_by_available(by_role_names, available, known)


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
    # ---- cabbage techniques (stir_fry must precede fry; slaw precedes salad) ----
    (r"\bslaw\b|\bcoleslaw\b", "raw_slaw"),
    (r"\bstir[- ]?fr(?:y|ied|ying)\b", "stir_fry"),
    (r"\bbrais(?:e|ed|ing)\b", "braise"),
    (r"\bferment(?:ed|ing|ation)?\b", "ferment"),
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


def component_state_profile(conn: sqlite3.Connection,
                            component_name: str) -> dict[str, Any] | None:
    """Profile owned by a transformed component, without a shadow name."""
    row = conn.execute(
        """
        SELECT c.name, sp.*
        FROM component_state_profiles sp
        JOIN components c ON c.component_id = sp.component_id
        WHERE c.name = ?
        """,
        (component_name,),
    ).fetchone()
    if row is None:
        return None
    profile = dict(row)
    for field in ("provides_roles", "flavour_tags", "texture_tags", "missing_risks"):
        profile[field] = _split_list(profile[field])
    return profile


def flavour_routes_for_component(
    conn: sqlite3.Connection,
    component_name: str,
    available_items: list[str] | None = None,
) -> list[dict[str, Any]]:
    """Routes fitting a transformed state, optionally matched to inventory."""
    rows = conn.execute(
        """
        SELECT fr.*, frs.fit_reason
        FROM flavour_routes fr
        JOIN flavour_route_states frs ON frs.route_id = fr.route_id
        JOIN components c ON c.component_id = frs.component_id
        WHERE c.name = ?
        ORDER BY CASE fr.confidence WHEN 'high' THEN 3 WHEN 'medium_high' THEN 2
                                    WHEN 'medium' THEN 1 ELSE 0 END DESC,
                 fr.name
        """,
        (component_name,),
    ).fetchall()
    available = {item.strip() for item in (available_items or []) if item.strip()}
    result = []
    for row in rows:
        route = dict(row)
        route["flavour_dimensions"] = _split_list(route["flavour_dimensions"])
        route["destinations"] = [r[0] for r in conn.execute(
            "SELECT destination_id FROM flavour_route_destinations "
            "WHERE route_id = ? ORDER BY rowid", (route["route_id"],)
        ).fetchall()]
        route["elements"] = [dict(r) for r in conn.execute(
            """SELECT i.canonical_name AS ingredient, fre.contribution, fre.optionality
               FROM flavour_route_elements fre
               JOIN ingredients i ON i.ingredient_id = fre.ingredient_id
               WHERE fre.route_id = ? ORDER BY fre.rowid""",
            (route["route_id"],),
        ).fetchall()]
        route["available_elements"] = [
            element for element in route["elements"]
            if element["ingredient"] in available
        ]
        route["missing_required"] = [
            element for element in route["elements"]
            if element["optionality"] == "required"
            and element["ingredient"] not in available
        ]
        route["required_coverage"] = (
            sum(e["optionality"] == "required" and e["ingredient"] in available
                for e in route["elements"]),
            sum(e["optionality"] == "required" for e in route["elements"]),
        )
        result.append(route)
    if available_items is not None:
        result.sort(key=lambda r: (-r["required_coverage"][0], r["route_id"]))
    return result


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


def _transformation_tags(conn: sqlite3.Connection,
                         transformation_id: int) -> list[dict[str, Any]]:
    """Tags produced by a transformation (flavour/texture/state), with polarity.
    Sorted flavour → texture → state for stable card rendering."""
    rows = conn.execute(
        """
        SELECT tg.family, tg.tag_value AS value, tt.polarity
        FROM transformation_tags tt
        JOIN tags tg ON tg.tag_id = tt.tag_id
        WHERE tt.transformation_id = ?
        ORDER BY CASE tg.family WHEN 'flavour' THEN 0 WHEN 'texture' THEN 1 ELSE 2 END,
                 tg.tag_value
        """,
        (transformation_id,),
    ).fetchall()
    return [dict(r) for r in rows]


def branch_detail(conn: sqlite3.Connection, transformation_id: int) -> dict[str, Any]:
    """The product-shape primitive: technique → component → flavour/texture
    → missing roles (priority-ordered) → fillers grouped by gap → uses."""
    row = conn.execute(
        """
        SELECT t.transformation_id, tech.name AS technique, c.name AS component,
               c.component_id, t.flavour_shift, t.texture_shift, t.confidence,
               t.risks, c.batch_prep_value, c.freezes_well, c.keeps_well
        FROM transformations t
        JOIN techniques tech ON tech.technique_id = t.technique_id
        JOIN components c     ON c.component_id = t.output_component_id
        WHERE t.transformation_id = ?
        """,
        (transformation_id,),
    ).fetchone()
    d = dict(row)
    d["risks"] = _split_list(d.get("risks"))
    d["tags"] = _transformation_tags(conn, transformation_id)
    d["missing"] = missing_roles(conn, transformation_id)
    d["fillers_by_role"] = fillers_by_role(conn, transformation_id)
    d["uses"] = component_uses(conn, d["component_id"])
    return d


def render_branch(d: dict[str, Any]) -> str:
    """One transformation in the product shape."""
    lines = [f"{d['technique']}", f"  → {d['component']}"]
    if d.get("flavour_shift") or d.get("texture_shift"):
        lines.append(f"  → {d['flavour_shift']} · {d['texture_shift']}")
    if d.get("risks"):
        lines.append("  → risks: " + ", ".join(d["risks"]))
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
        if d.get("risks"):
            lines.append("  risks: " + ", ".join(d["risks"]))
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


def scout_rows(conn: sqlite3.Connection, technique: str | None = None,
               ingredient: str | None = None) -> list[dict[str, Any]]:
    """Structured Scout mode — the experimental pairings as rows (for the UI).

    If `ingredient` is given, restrict to that ingredient's transformations
    (e.g. scout_rows(conn, ingredient='cabbage') -> cabbage's experimental
    pairings). Cook mode (plate_balance) never surfaces these — the two paths
    are separate."""
    where = ["p.confidence = 'experimental'"]
    params: list[Any] = []
    if technique:
        where.append("tech.name = ?")
        params.append(technique)
    if ingredient:
        where.append("ti.canonical_name = ?")
        params.append(ingredient)
    rows = conn.execute(
        """
        SELECT ing.canonical_name AS filler, r.role_name AS role,
               p.notes, p.availability_class,
               ti.canonical_name AS target, tech.name AS technique
        FROM pairings p
        JOIN ingredients ing ON ing.ingredient_id = p.ingredient_id
        JOIN roles r         ON r.role_id = p.role_id
        LEFT JOIN transformations t ON t.transformation_id = p.works_best_with_transformation_id
        LEFT JOIN ingredients ti ON ti.ingredient_id = t.ingredient_id
        LEFT JOIN techniques tech ON tech.technique_id = t.technique_id
        WHERE """ + " AND ".join(where),
        params,
    ).fetchall()
    return [dict(r) for r in rows]


def scout(conn: sqlite3.Connection, technique: str | None = None,
          ingredient: str | None = None) -> str:
    """Scout mode — experimental pairings, explicitly labelled, never as classic.

    If `ingredient` is given, restrict to that ingredient's transformations
    (e.g. scout(conn, ingredient='cabbage') -> cabbage's experimental pairings),
    so 'scout cabbage' surfaces cabbage-specific ideas rather than every
    experimental pairing in the ontology. Cook mode (plate_balance) never
    surfaces these — the two paths are separate."""
    rows = scout_rows(conn, technique, ingredient)
    subject = ingredient or technique or "all"
    if not rows:
        return f"Scout / experimental: none curated yet for {subject!r}."
    lines = ["Scout / experimental (plausible but uncommon — NOT classic):"]
    for r in rows:
        note = r["notes"] or f"{r['filler']} ({r['role']})"
        subj = r["technique"] or r["target"] or technique or "tomato"
        lines.append(f"  - {r['filler']} + {subj}: {note}")
    lines.append("  (These are speculative — labelled so no one pretends they're tradition.)")
    return "\n".join(lines)


def classify_scout_candidate(compatibility_evidence: list[str],
                             novelty_class: str = "not_checked") -> str:
    """Classify from compatibility only; novelty cannot rescue weak evidence."""
    if not compatibility_evidence:
        return "rejected"
    if len(compatibility_evidence) >= 3:
        return "scout_candidate"
    return "weak_hypothesis"


def generate_scout_hypotheses(
    conn: sqlite3.Connection,
    component_name: str,
    include_rejected: bool = False,
) -> list[dict[str, Any]]:
    """Generate hypotheses by applying reusable analogy rules to one state.

    Compatibility is derived from state dimensions and the rule's functional
    analogy. Novelty is deliberately left unchecked and never enters ranking.
    """
    state = component_state_profile(conn, component_name)
    if state is None:
        return []
    state_dimensions = set(state["flavour_tags"])
    rows = conn.execute(
        """
        SELECT ar.*, src.canonical_name AS source,
               candidate.canonical_name AS candidate
        FROM analogy_rules ar
        JOIN ingredients src ON src.ingredient_id = ar.source_ingredient_id
        JOIN ingredients candidate
          ON candidate.ingredient_id = ar.substitute_ingredient_id
        ORDER BY CASE ar.confidence WHEN 'high' THEN 4 WHEN 'medium_high' THEN 3
                                    WHEN 'medium' THEN 2 WHEN 'low' THEN 1 ELSE 0 END DESC,
                 ar.analogy_id
        """
    ).fetchall()
    hypotheses = []
    for row in rows:
        hypothesis = dict(row)
        required = _split_list(hypothesis["required_dimensions"])
        matched = [dimension for dimension in required if dimension in state_dimensions]
        evidence = []
        if matched:
            evidence.append("state fit: " + ", ".join(matched))
            evidence.append("mechanism: " + hypothesis["mechanism"].replace("_", " "))
            evidence.append("analogy: " + hypothesis["shared_function"])
        hypothesis.update({
            "state": component_name,
            "required_dimensions": required,
            "matched_dimensions": matched,
            "compatibility_evidence": evidence,
            "compatibility_score": len(evidence),
            "novelty": {"class": "not_checked", "scope": None},
            "risk": hypothesis["expected_risk"],
        })
        observation = conn.execute(
            """
            SELECT no.observed_count, no.context_count, no.contexts,
                   no.target_covered, no.candidate_covered, no.result_class,
                   no.observed_at, c.corpus_id, c.name AS corpus_name,
                   c.scope, c.recipe_count, c.search_date
            FROM novelty_observations no
            JOIN corpora c ON c.corpus_id = no.corpus_id
            JOIN components component ON component.component_id = no.component_id
            WHERE no.analogy_id = ? AND component.name = ?
            ORDER BY no.observed_at DESC, no.observation_id DESC LIMIT 1
            """,
            (hypothesis["analogy_id"], component_name),
        ).fetchone()
        if observation:
            novelty = dict(observation)
            novelty["class"] = novelty.pop("result_class")
            novelty["contexts"] = _split_list(novelty["contexts"])
            novelty["target_covered"] = bool(novelty["target_covered"])
            novelty["candidate_covered"] = bool(novelty["candidate_covered"])
            hypothesis["novelty"] = novelty
        protocol = conn.execute(
            "SELECT starting_ratio, smallest_test, success_condition, "
            "likely_failure, corrections, safety_note "
            "FROM tasting_protocol_templates WHERE analogy_id = ?",
            (hypothesis["analogy_id"],),
        ).fetchone()
        hypothesis["protocol"] = dict(protocol) if protocol else None
        hypothesis["candidate_class"] = classify_scout_candidate(
            evidence, hypothesis["novelty"]["class"]
        )
        if hypothesis["candidate_class"] == "rejected":
            hypothesis["rejection_reason"] = (
                "State lacks required dimensions: " + ", ".join(required)
            )
        else:
            hypothesis["rejection_reason"] = None
            hypothesis["explanation"] = hypothesis["explanation_template"].format(
                candidate=hypothesis["candidate"], source=hypothesis["source"],
                shared_function=hypothesis["shared_function"],
                matched_dimensions=", ".join(matched),
            )
        if include_rejected or hypothesis["candidate_class"] != "rejected":
            hypotheses.append(hypothesis)
    hypotheses.sort(key=lambda h: (-h["compatibility_score"], h["candidate"]))
    return hypotheses


def render_generated_hypotheses(conn: sqlite3.Connection,
                                component_name: str) -> str:
    hypotheses = generate_scout_hypotheses(conn, component_name)
    if not hypotheses:
        return f"No generated Scout hypotheses for {component_name!r}."
    lines = ["Generated Scout hypotheses (compatibility separate from novelty):"]
    for hypothesis in hypotheses:
        lines.extend([
            f"  - {component_name} + {hypothesis['candidate']}",
            f"    class: {hypothesis['candidate_class']}",
            f"    why: {hypothesis['explanation']}",
            f"    analogy: {hypothesis['known_pairing']}",
            f"    difference: {hypothesis['meaningful_difference']}",
            f"    risk: {hypothesis['risk']}",
            (
                "    novelty: not checked — no corpus claim yet"
                if hypothesis["novelty"]["class"] == "not_checked"
                else "    novelty: {class_} ({count} occurrence(s), {scope}; "
                     "searched {date})".format(
                         class_=hypothesis["novelty"]["class"],
                         count=hypothesis["novelty"]["observed_count"],
                         scope=hypothesis["novelty"]["scope"],
                         date=hypothesis["novelty"]["search_date"],
                     )
            ),
        ])
        if hypothesis.get("protocol"):
            protocol = hypothesis["protocol"]
            lines.extend([
                f"    smallest test: {protocol['smallest_test']}",
                f"    starting ratio: {protocol['starting_ratio']}",
                f"    success: {protocol['success_condition']}",
                f"    likely failure: {protocol['likely_failure']}",
                f"    corrections: {protocol['corrections']}",
                f"    safety: {protocol['safety_note']}",
            ])
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
    component_name = phrase.strip().lower()
    state_profile = component_state_profile(conn, component_name)
    if state_profile:
        return {
            "kind": "profile", "name": component_name,
            "provides": state_profile["provides_roles"],
            "missing_risks": state_profile["missing_risks"],
            "heaviness": state_profile["heaviness_score"],
            "dryness": state_profile["dryness_score"],
            "profile_source": "component_state",
        }

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


def destination_profile(conn: sqlite3.Connection,
                        destination_id: str) -> dict[str, Any] | None:
    """Return one destination's contextual functional targets and reasons."""
    row = conn.execute(
        "SELECT * FROM destination_profiles WHERE destination_id = ?",
        (destination_id,),
    ).fetchone()
    if row is None:
        return None
    profile = dict(row)
    functions = conn.execute(
        """
        SELECT r.role_name AS role, df.importance, df.reason
        FROM destination_functions df
        JOIN roles r ON r.role_id = df.role_id
        WHERE df.destination_id = ?
        ORDER BY df.rowid
        """,
        (destination_id,),
    ).fetchall()
    profile["functions"] = [dict(function) for function in functions]
    for importance in ("required", "useful", "optional", "unsuitable"):
        profile[importance] = [
            function["role"] for function in profile["functions"]
            if function["importance"] == importance
        ]
    return profile


def plate_balance_detail(conn: sqlite3.Connection, text: str,
                           available_items: list[str] | None = None,
                           destination_id: str = "complete_savoury_plate") -> dict[str, Any]:
    """Plate Balance Engine (Cook mode) — structured result for the UI.

    Returns:
      items            — [{name, kind, provides, missing_risks, heaviness, dryness}]
      provided         — sorted canonical roles the plate already has
      target_gap       — hard gaps: TARGET_ROLES no item provides
      flagged_more     — soft gaps: a profile flags a role even though covered
      plate_heaviness  — sum of profiled heaviness (None if no profiled items)
      plate_dryness    — sum of profiled dryness (None if no profiled items)
      heaviness_label  — plain-English read of avg heaviness
      dryness_label    — plain-English read of avg dryness
      leans_heavy      — True if avg heaviness >= 4
      leans_dry        — True if avg dryness >= 3.5
      suggested_fillers — {role: [filler names]} for target_gap + flagged_more
      no_profile       — items with no balance profile (ingredient or unknown)
      unknown          — items that matched nothing at all
      balanced         — True if no target_gap and no flagged_more
    Round 11 — when available_items is provided, ALSO returns:
      available_now      — [{filler, roles}] on-hand fillers covering a gap
      missing_but_useful — [{role, fillers}] uncovered gaps + the unavailable
                           curated fillers that would help
      unknown_items      — [item] selected items not recognised as ingredients
      no_match_known     — [item] recognised on-hand items that fill no gap here
    Cook-only; Scout never leaks in. None/[] available_items = current behaviour.
    Honest about its limits — it never invents roles or fillers it doesn't have.
    """
    destination = destination_profile(conn, destination_id)
    if destination is None:
        raise ValueError(f"unknown or unmodelled destination: {destination_id!r}")

    phrases = _plate_phrases(text)
    items = [_recognise_plate_item(conn, ph) for ph in phrases]

    profiles = [it for it in items if it["kind"] == "profile"]
    no_profile = [it for it in items if it["kind"] != "profile"]
    unknown = [it for it in items if it["kind"] == "unknown"]

    provided: set[str] = set()
    for it in items:
        for role in it["provides"]:
            provided.add(_canon_role(role))

    risk_roles: set[str] = set()
    for it in profiles:
        for role in it["missing_risks"]:
            risk_roles.add(_canon_role(role))

    h_vals = [it["heaviness"] for it in profiles if it["heaviness"] is not None]
    d_vals = [it["dryness"] for it in profiles if it["dryness"] is not None]
    plate_h = sum(h_vals) if h_vals else None
    plate_d = sum(d_vals) if d_vals else None
    h_avg = plate_h / len(h_vals) if h_vals else None
    d_avg = plate_d / len(d_vals) if d_vals else None

    target_gap = [r for r in destination["required"] if r not in provided]
    useful_gap = [r for r in destination["useful"] if r not in provided]
    unsuitable_provided = [r for r in destination["unsuitable"] if r in provided]
    flagged_more = sorted(r for r in risk_roles if r not in set(target_gap))

    suggested: dict[str, list[str]] = {}
    for role in target_gap + flagged_more:
        suggested[role] = _fillers_for_role(conn, role)

    result = {
        "items": items,
        "destination": destination,
        "destination_id": destination_id,
        "provided": sorted(provided),
        "target_gap": target_gap,
        "useful_gap": useful_gap,
        "unsuitable_provided": unsuitable_provided,
        "flagged_more": flagged_more,
        "plate_heaviness": plate_h,
        "plate_dryness": plate_d,
        "heaviness_label": _heaviness_label(h_avg) if h_avg is not None else None,
        "dryness_label": _dryness_label(d_avg) if d_avg is not None else None,
        "leans_heavy": bool(h_avg is not None and h_avg >= 4),
        "leans_dry": bool(d_avg is not None and d_avg >= 3.5),
        "suggested_fillers": suggested,
        "no_profile": no_profile,
        "unknown": unknown,
        "balanced": not target_gap and not flagged_more,
    }

    if available_items is not None:
        available = {a.strip() for a in available_items if a and a.strip()}
        # Cook-only filler names per gap role, in gap order (target then flagged)
        by_role_names = {role: suggested.get(role, [])
                         for role in target_gap + flagged_more}
        part = _partition_by_available(by_role_names, available,
                                        set(ingredients_list(conn)))
        result["available_now"] = part["available_now"]
        result["missing_but_useful"] = part["missing_but_useful"]
        result["unknown_items"] = part["unknown_items"]
        result["no_match_known"] = part["no_match_known"]
        result["covered_roles"] = part["covered_roles"]
    return result


def plate_balance(conn: sqlite3.Connection, text: str,
                  destination_id: str = "complete_savoury_plate") -> str:
    """Plate Balance Engine (Cook mode) — human-readable render.

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
    try:
        r = plate_balance_detail(conn, text, destination_id=destination_id)
    except ValueError as exc:
        return str(exc)
    if not r["items"]:
        return ("Plate balance — Cook mode\n"
                "Name the plate items, e.g. 'balance mashed potatoes and "
                "chickpea patties' or 'I have X and Y, what is missing?'")
    have_parts = []
    for it in r["items"]:
        tag = {"profile": "profile", "ingredient": "ingredient",
               "unknown": "unknown"}[it["kind"]]
        have_parts.append(f"{it['name']} ({tag})")
    lines = ["Plate balance — Cook mode",
             f"Destination: {r['destination']['name']}",
             f"You have: {', '.join(have_parts)}"]

    if r["no_profile"]:
        names = []
        for it in r["no_profile"]:
            label = "unknown item" if it["kind"] == "unknown" else "known ingredient, no balance data"
            names.append(f"{it['name']} ({label})")
        lines.append(
            "  no profile for: " + ", ".join(names)
            + " — add component_profiles entries for heaviness/dryness/missing-risk data."
        )

    prov_disp = r["provided"]
    lines.append("  provided roles: " + (", ".join(prov_disp) if prov_disp else "(none)"))

    if r["plate_heaviness"] is not None:
        lines.append(f"  plate heaviness: {r['plate_heaviness']}  ({r['heaviness_label']})")
    else:
        lines.append("  plate heaviness: unknown (no profiled items)")
    if r["plate_dryness"] is not None:
        lines.append(f"  plate dryness: {r['plate_dryness']}  ({r['dryness_label']})")
    else:
        lines.append("  plate dryness: unknown (no profiled items)")

    if r["leans_heavy"]:
        lines.append("  leans heavy — favor acid/herb/crunch; avoid more fat/cream.")
    if r["leans_dry"]:
        lines.append("  leans dry — favor sauce/hydration/cream.")

    if r["balanced"]:
        lines.append("  balanced — nothing essential missing.")
        return "\n".join(lines)

    if r["target_gap"]:
        gap_label = (
            "missing for a balanced plate"
            if r["destination_id"] == "complete_savoury_plate"
            else "required for this destination"
        )
        lines.append(f"  {gap_label}: " + ", ".join(r["target_gap"]))
        lines.append("  add:")
        for role in r["target_gap"]:
            fillers = r["suggested_fillers"].get(role, [])
            lines.append(f"    - {role}: " + (", ".join(fillers) if fillers else "(no curated filler)"))
    else:
        lines.append("  no hard gaps — all required destination functions are covered.")

    if r["useful_gap"]:
        lines.append("  useful but not required here: " + ", ".join(r["useful_gap"]))
        by_role = {f["role"]: f["reason"] for f in r["destination"]["functions"]}
        for role in r["useful_gap"]:
            lines.append(f"    - {role}: {by_role[role]}")

    if r["unsuitable_provided"]:
        lines.append(
            "  not required for this destination (already present): "
            + ", ".join(r["unsuitable_provided"])
        )

    if r["flagged_more"]:
        lines.append("  also flagged by item profiles (may want more): " + ", ".join(r["flagged_more"]))
        for role in r["flagged_more"]:
            fillers = r["suggested_fillers"].get(role, [])
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


def filler_profile_detail(conn: sqlite3.Connection, name: str) -> dict[str, Any]:
    """Structured filler profile — the five questions as a dict (for the UI).

    Returns:
      name, aliases, kind, roles, repairs, avoid_when, availability,
      mode       — human-readable Cook/Scout label
      mode_kind  — 'cook' | 'scout' | 'both' | 'none'
      n_cook, n_exp — pairing counts
      pairings   — [{role, conf, target, technique}]
      found      — False if no ingredient matched (name unchanged)
    """
    row = conn.execute(
        "SELECT canonical_name, aliases, base_roles, default_availability_class, "
        "kind, repairs, avoid_when FROM ingredients WHERE canonical_name = ?",
        (name,),
    ).fetchone()
    if row is None:
        canon = _match_ingredient(conn, name)
        if canon:
            return filler_profile_detail(conn, canon)
        return {"found": False, "name": name, "kind": None, "aliases": [],
                "roles": [], "repairs": [], "avoid_when": [], "availability": None,
                "mode": f"No ingredient named {name!r}.", "mode_kind": "none",
                "n_cook": 0, "n_exp": 0, "pairings": []}
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
        mode_kind = "both"
        mode = f"Cook (also has {n_exp} Scout/experimental pairing{'s' if n_exp != 1 else ''})"
    elif n_cook:
        mode_kind = "cook"
        mode = f"Cook ({n_cook} non-experimental pairing{'s' if n_cook != 1 else ''})"
    elif n_exp:
        mode_kind = "scout"
        mode = (f"Scout / experimental ({n_exp} experimental pairing"
                f"{'s' if n_exp != 1 else ''}; no classic pairings yet)")
    else:
        mode_kind = "none"
        mode = "no pairings yet — not suggested by the plate engine"
    return {
        "found": True,
        "name": row["canonical_name"],
        "aliases": _split_list(row["aliases"]),
        "kind": row["kind"],
        "roles": roles,
        "repairs": repairs,
        "avoid_when": avoid,
        "availability": avail,
        "mode": mode,
        "mode_kind": mode_kind,
        "n_cook": n_cook,
        "n_exp": n_exp,
        "pairings": [dict(p) for p in prs],
    }


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
    d = filler_profile_detail(conn, name)
    if not d["found"]:
        return d["mode"]
    kind = d["kind"]
    if kind == "full":
        header = (f"{d['name']} — full ingredient (has a technique tree; "
                  f"ask 'what can I do with {d['name']}')")
    elif kind == "both":
        header = f"{d['name']} — both (technique tree + filler) profile"
    else:
        header = f"{d['name']} — filler profile"
    lines = [header]
    lines.append("  roles filled: " + (", ".join(d["roles"]) if d["roles"] else "(none)"))
    lines.append("  repairs plates that are: " + (", ".join(d["repairs"]) if d["repairs"] else "(unspecified)"))
    lines.append("  avoid when: " + (", ".join(d["avoid_when"]) if d["avoid_when"] else "(unspecified)"))
    lines.append(f"  Finnish supermarket: {d['availability']}")
    lines.append(f"  mode: {d['mode']}")
    seen = []
    for p in d["pairings"][:6]:
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
        return scout(conn, tech, _detect_subject(prompt, conn))

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


# ---- UI handles (read-only structured views for the Streamlit slice) ------
# These return dicts/lists so the UI can render cards/chips instead of parsing
# the string renders above. They add NO ontology — just handles on the engine.

def tree_ingredients(conn: sqlite3.Connection) -> list[str]:
    """Ingredients that own a technique tree (kind full or both, >=1
    transformation) — the Tab-1 selectbox population: tomato/onion/potato/cabbage."""
    rows = conn.execute(
        """
        SELECT DISTINCT i.canonical_name
        FROM ingredients i
        JOIN transformations t ON t.ingredient_id = i.ingredient_id
        WHERE i.kind IN ('full', 'both')
        ORDER BY i.canonical_name
        """
    ).fetchall()
    return [r[0] for r in rows]


def techniques_for_ingredient(conn: sqlite3.Connection,
                              ingredient: str) -> list[str]:
    """Valid technique names for an ingredient, ranked like the branch view
    (cooking moves before preservation, then confidence) — Tab-1 technique
    selectbox and acceptance test target."""
    rows = transformations_for_ingredient(conn, ingredient)
    KIND_RANK = {"fresh": 0, "cooked": 0, "concentrated": 0,
                 "preserved": 1, "storage": 2}
    rows.sort(key=lambda d: (
        KIND_RANK.get(d.get("component_kind", "cooked"), 0),
        d.get("preservation_flag", 0),
        -_rank(d["confidence"]),
        d["technique"],
    ))
    return [r["technique"] for r in rows]


def branch_card(conn: sqlite3.Connection, ingredient: str,
                 technique: str) -> dict[str, Any] | None:
    """A single transformation card for (ingredient, technique): the branch_detail
    dict plus the ingredient name. None if no such transformation."""
    tr = transformation_by_technique(conn, technique, ingredient)
    if not tr:
        return None
    d = branch_detail(conn, tr["transformation_id"])
    d["ingredient"] = ingredient
    return d


def all_branch_cards(conn: sqlite3.Connection, ingredient: str) -> list[dict[str, Any]]:
    """Every transformation branch for an ingredient as a card dict (with
    ingredient + tags). Ranked cooking-before-preservation."""
    out = []
    for tech in techniques_for_ingredient(conn, ingredient):
        card = branch_card(conn, ingredient, tech)
        if card:
            out.append(card)
    return out


def component_card(conn: sqlite3.Connection, component_name: str) -> dict[str, Any] | None:
    """Tab-2 component view: what produced it, its tags/risks, what it still
    needs, and useful next moves. None if no such component.

    A component is an after-state; 'provides' is its flavour/texture tags +
    kind, and 'may need' is the producing transformation's missing_roles +
    risks — the same read component_first gives, but structured."""
    comp = conn.execute("SELECT * FROM components WHERE name = ?",
                        (component_name,)).fetchone()
    if comp is None:
        return None
    uses = component_uses(conn, comp["component_id"])
    prod = conn.execute(
        """
        SELECT t.transformation_id, i.canonical_name AS ingredient,
               tech.name AS technique, t.confidence,
               t.flavour_shift, t.texture_shift
        FROM transformations t
        JOIN ingredients i ON i.ingredient_id = t.ingredient_id
        JOIN techniques tech ON tech.technique_id = t.technique_id
        WHERE t.output_component_id = ?
        """,
        (comp["component_id"],),
    ).fetchall()
    producers = [dict(p) for p in prod]
    detail = branch_detail(conn, producers[0]["transformation_id"]) if producers else None
    return {
        "name": component_name,
        "kind": comp["component_kind"],
        "keeps_well": comp["keeps_well"],
        "freezes_well": bool(comp["freezes_well"]),
        "batch_prep_value": comp["batch_prep_value"],
        "produced_by": producers,
        "flavour_shift": detail["flavour_shift"] if detail else None,
        "texture_shift": detail["texture_shift"] if detail else None,
        "tags": detail["tags"] if detail else [],
        "risks": detail["risks"] if detail else [],
        "missing": detail["missing"] if detail else [],
        "fillers_by_role": detail["fillers_by_role"] if detail else {},
        "uses": uses,
        "plate_profile": component_state_profile(conn, component_name),
    }


def components_list(conn: sqlite3.Connection) -> list[str]:
    rows = conn.execute("SELECT name FROM components ORDER BY name").fetchall()
    return [r[0] for r in rows]


def profiles_list(conn: sqlite3.Connection) -> list[str]:
    """Component-profile names (Tab-3 multiselect population)."""
    rows = conn.execute("SELECT name FROM component_profiles ORDER BY name").fetchall()
    return [r[0] for r in rows]


def ingredients_list(conn: sqlite3.Connection) -> list[str]:
    """All ingredient canonical names (Tab-4 selectbox population)."""
    rows = conn.execute(
        "SELECT canonical_name FROM ingredients ORDER BY canonical_name"
    ).fetchall()
    return [r[0] for r in rows]


# ---- Ingredient journeys ---------------------------------------------------

def ingredient_journeys(conn: sqlite3.Connection,
                        ingredient: str) -> list[dict[str, Any]]:
    """Return complete, ordered product-facing paths for an ingredient.

    Journeys reference the existing primary transformation record and add the
    preparation, causal explanation, destinations, and secondary transitions
    needed by Cook. They do not replace branch cards or plate profiles.
    """
    rows = conn.execute(
        """
        SELECT j.*, i.canonical_name AS ingredient, tech.name AS primary_transformation,
               c.name AS primary_component
        FROM journeys j
        JOIN ingredients i ON i.ingredient_id = j.ingredient_id
        JOIN transformations tr
          ON tr.transformation_id = j.primary_transformation_id
        JOIN techniques tech ON tech.technique_id = tr.technique_id
        JOIN components c ON c.component_id = tr.output_component_id
        WHERE i.canonical_name = ?
        ORDER BY j.journey_id
        """,
        (ingredient,),
    ).fetchall()
    result: list[dict[str, Any]] = []
    for row in rows:
        journey = dict(row)
        journey["useful_additions"] = _split_list(journey.get("useful_additions"))
        journey["destinations"] = [
            r[0] for r in conn.execute(
                "SELECT destination_id FROM journey_destinations "
                "WHERE journey_id = ? ORDER BY rowid",
                (journey["journey_id"],),
            ).fetchall()
        ]
        journey["transitions"] = [
            dict(r) for r in conn.execute(
                "SELECT sequence_no, from_state, move, to_state, reason "
                "FROM journey_transitions WHERE journey_id = ? ORDER BY sequence_no",
                (journey["journey_id"],),
            ).fetchall()
        ]
        result.append(journey)
    return result


def ingredient_journey(conn: sqlite3.Connection, ingredient: str,
                       slug: str) -> dict[str, Any] | None:
    """Return one named journey, or ``None`` when it is not modelled."""
    return next(
        (journey for journey in ingredient_journeys(conn, ingredient)
         if journey["slug"] == slug),
        None,
    )


def render_journey(journey: dict[str, Any]) -> str:
    """Render one journey as a causal, text-first Cook explanation."""
    lines = [journey["title"], f"Why choose it: {journey['why_choose']}"]
    lines.append(f"Prepare: {journey['preparation_id'].replace('_', ' ')}")
    lines.append(f"Transform: {journey['primary_transformation'].replace('_', ' ')}")
    lines.append(f"What changes: {journey['sensory_change']}")
    lines.append(f"Flavour direction: {journey['flavour_direction']}")
    additions = journey.get("useful_additions") or []
    if additions:
        lines.append("Useful additions: " + ", ".join(a.replace("_", " ") for a in additions))
    lines.append(f"What becomes possible: {journey['becomes_possible']}")
    lines.append("Destinations: " + ", ".join(
        d.replace("_", " ") for d in journey["destinations"]
    ))
    lines.append(f"Watch for: {journey['risks']}")
    lines.append(f"Correction: {journey['correction'].replace('_', ' ')}")
    lines.append("Path:")
    for transition in journey["transitions"]:
        lines.append(
            f"  {transition['sequence_no']}. {transition['from_state']} -> "
            f"{transition['move']} -> {transition['to_state']} — {transition['reason']}"
        )
    return "\n".join(lines)


def render_ingredient_journeys(conn: sqlite3.Connection, ingredient: str,
                               slug: str | None = None) -> str:
    """Text-first CLI surface for all journeys or one selected journey."""
    if slug:
        journey = ingredient_journey(conn, ingredient, slug)
        return render_journey(journey) if journey else (
            f"No journey named {slug!r} for {ingredient!r}."
        )
    journeys = ingredient_journeys(conn, ingredient)
    if not journeys:
        return f"No complete journeys modelled for {ingredient!r}."
    return (f"Complete Cook journeys for {ingredient}:\n\n" +
            "\n\n---\n\n".join(render_journey(j) for j in journeys))
