"""CulinaryDB corpus backfill — attach co-occurrence *evidence* to pairings.

This module NEVER invents roles or overwrites curated confidence. It reads the
CulinaryDB CSVs, computes how often a pairing's filler and target ingredient
appear in the same recipe, and writes that count + a few recipe titles into the
pairings table's corpus columns. The curated `confidence` and `curated_role_fit`
stay hand-authored truth.

Design note (the user's guardrail): co-occurrence is not role-fit. Garlic and
onion co-occur in thousands of recipes, but that does not mean garlic fixes
every onion state — garlic fills `aromatic`, not `acid`. So corpus evidence is
stored next to, not in place of, the curated role. `curated_role_fit` is the
hand field that says whether the corpus signal actually supports THIS pairing's
role.

CulinaryDB keys ingredients by Entity ID (file 02 uses Title Case names, file 04
uses lowercase with trailing spaces — so Entity ID is the only stable key).

CulinaryDB files expected in the given directory:
    01_Recipe_Details.csv          Recipe ID,Title,Source,Cuisine
    02_Ingredients.csv             Aliased Ingredient Name,Ingredient Synonyms,Entity ID,Category
    04_Recipe-Ingredients_Aliases.csv  Recipe ID,Original Ingredient,Aliased Ingredient,Entity ID
"""

from __future__ import annotations

import csv
import sqlite3
from datetime import date
from pathlib import Path

# Our canonical ingredient name -> CulinaryDB ingredient name(s) to look up.
# Only the tricky ones need listing; the rest resolve by normalised name lookup.
CANONICAL_TO_CORPUS: dict[str, list[str]] = {
    "olive_oil": ["olive oil"],
    "sea_salt": ["salt"],
    "black_pepper": ["pepper"],
    "white_beans": ["white beans", "cannellini beans", "navy beans", "beans"],
    "chile_flakes": ["chili flakes", "red pepper flakes", "cayenne", "chili powder"],
    "jalapeno": ["jalapeno", "green chili", "green chilli"],
    "soft_cheese": ["ricotta cheese", "feta cheese", "cottage cheese", "cream cheese"],
    "mozzarella": ["mozzarella cheese"],
    "parmesan": ["parmesan cheese"],
    "gruyere": ["gruyere cheese", "gruyère cheese"],
    "cilantro": ["cilantro", "coriander"],
    "greens": ["lettuce", "spinach"],
    "stock": ["stock", "broth", "vegetable stock"],
    "grilled_fish": ["fish", "fatty fish", "codfish"],
    "soy_sauce": ["soy sauce", "soya sauce"],
    "brown_butter": ["butter"],
    "smoked_yogurt": ["yogurt"],
    "rye_crumbs": ["rye bread"],
    "lingonberry_vinegar": ["vinegar"],
    "fennel_pollen": ["fennel"],
    "orange_zest": ["orange"],
    "hard_cheese": ["parmesan cheese", "gruyere cheese", "cheddar cheese"],
    "pickles": ["pickle", "pickled cucumber", "cucumber"],
}


def _norm(name: str) -> str:
    return " ".join(name.lower().split())


def load_corpus(dir_path: Path | str) -> tuple[dict[int, set[int]], dict[int, str], dict[str, int]]:
    """Read CulinaryDB into:
      entity_recipes: entity id -> set of recipe ids containing it
      recipe_titles:  recipe id -> title
      name_index:      normalised ingredient name -> entity id
    """
    dir_path = Path(dir_path)
    recipe_titles: dict[int, str] = {}
    with open(dir_path / "01_Recipe_Details.csv", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            try:
                rid = int(r["Recipe ID"])
            except (ValueError, KeyError):
                continue
            recipe_titles[rid] = r.get("Title", "").strip()

    name_index: dict[str, int] = {}
    with open(dir_path / "02_Ingredients.csv", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            try:
                eid = int(r["Entity ID"])
            except (ValueError, KeyError):
                continue
            for field in ("Aliased Ingredient Name", "Ingredient Synonyms"):
                for raw in (r.get(field) or "").split(","):
                    raw = raw.strip()
                    if raw:
                        name_index.setdefault(_norm(raw), eid)

    entity_recipes: dict[int, set[int]] = {}
    with open(dir_path / "04_Recipe-Ingredients_Aliases.csv", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            try:
                rid = int(r["Recipe ID"])
                eid = int(r["Entity ID"])
            except (ValueError, KeyError):
                continue
            entity_recipes.setdefault(eid, set()).add(rid)
            # file 04 names are lowercase aliases — index them too for coverage
            raw = (r.get("Aliased Ingredient Name") or "").strip()
            if raw and _norm(raw) not in name_index:
                name_index[_norm(raw)] = eid

    return entity_recipes, recipe_titles, name_index


def resolve_entities(canonical: str, name_index: dict[str, int]) -> list[int]:
    """Map one of our canonical ingredient names to CulinaryDB entity ids."""
    out: list[int] = []
    seen: set[int] = set()
    for corpus_name in CANONICAL_TO_CORPUS.get(canonical, []):
        eid = name_index.get(_norm(corpus_name))
        if eid is not None and eid not in seen:
            out.append(eid)
            seen.add(eid)
    if out:
        return out
    # fall back to normalised exact lookup of our own name
    eid = name_index.get(_norm(canonical.replace("_", " ")))
    if eid is not None:
        out.append(eid)
    return out


def resolve_novelty_entities(canonical: str,
                             name_index: dict[str, int]) -> list[int]:
    """Strict resolution for novelty claims.

    Broad functional aliases used by legacy pairing backfill (for example
    brown_butter -> butter) must not establish corpus coverage for a more
    specific Scout candidate.
    """
    entity = name_index.get(_norm(canonical.replace("_", " ")))
    return [entity] if entity is not None else []


def cooccurrence(entity_recipes: dict[int, set[int]],
                 recipe_titles: dict[int, str],
                 filler_entities: list[int],
                 target_entities: list[int],
                 max_contexts: int = 3) -> tuple[int, str]:
    """Count recipes where any filler entity and any target entity co-occur.
    Returns (count, newline-joined example recipe titles)."""
    filler_recipes: set[int] = set()
    for e in filler_entities:
        filler_recipes |= entity_recipes.get(e, set())
    target_recipes: set[int] = set()
    for e in target_entities:
        target_recipes |= entity_recipes.get(e, set())
    shared = filler_recipes & target_recipes
    if not shared:
        return 0, ""
    contexts = []
    for rid in list(shared)[:max_contexts]:
        title = recipe_titles.get(rid, "").strip()
        if title:
            contexts.append(title)
    return len(shared), "\n".join(contexts)


def novelty_class(observed_count: int, covered: bool) -> str:
    """Transparent provisional classes based on distinct recipe occurrence."""
    if not covered:
        return "insufficient_coverage"
    if observed_count == 0:
        return "not_observed"
    if observed_count == 1:
        return "rare"
    if observed_count < 5:
        return "uncommon"
    if observed_count < 20:
        return "established"
    return "common"


def observe_hypotheses(
    conn: sqlite3.Connection,
    component_name: str,
    dir_path: Path | str,
    corpus_id: str = "culinarydb",
    corpus_name: str = "CulinaryDB",
    scope: str | None = None,
    search_date: str | None = None,
) -> dict[str, int]:
    """Measure generated candidates in one named corpus without rescoring them."""
    # Local import avoids a query -> corpus -> query module cycle at import time.
    from .query import generate_scout_hypotheses

    entity_recipes, recipe_titles, name_index = load_corpus(dir_path)
    component = conn.execute(
        """SELECT c.component_id, i.canonical_name AS target
           FROM components c
           JOIN transformations t ON t.output_component_id = c.component_id
           JOIN ingredients i ON i.ingredient_id = t.ingredient_id
           WHERE c.name = ?""",
        (component_name,),
    ).fetchone()
    if component is None:
        raise ValueError(f"unknown transformed component: {component_name!r}")

    observed_at = search_date or date.today().isoformat()
    scope_text = scope or f"{len(recipe_titles)} recipes in supplied CulinaryDB files"
    conn.execute(
        """INSERT INTO corpora(corpus_id, name, scope, source_path, recipe_count, search_date)
           VALUES (?,?,?,?,?,?)
           ON CONFLICT(corpus_id) DO UPDATE SET name=excluded.name, scope=excluded.scope,
             source_path=excluded.source_path, recipe_count=excluded.recipe_count,
             search_date=excluded.search_date""",
        (corpus_id, corpus_name, scope_text, str(Path(dir_path)),
         len(recipe_titles), observed_at),
    )

    target_entities = resolve_entities(component["target"], name_index)
    target_covered = bool(target_entities) and any(
        entity_recipes.get(entity) for entity in target_entities
    )
    summary = {"observed": 0, "not_observed": 0, "insufficient_coverage": 0}
    for hypothesis in generate_scout_hypotheses(conn, component_name):
        candidate_entities = resolve_novelty_entities(
            hypothesis["candidate"], name_index
        )
        candidate_covered = bool(candidate_entities) and any(
            entity_recipes.get(entity) for entity in candidate_entities
        )
        covered = target_covered and candidate_covered
        count, contexts = (0, "")
        if covered:
            count, contexts = cooccurrence(
                entity_recipes, recipe_titles, candidate_entities, target_entities
            )
        result = novelty_class(count, covered)
        context_count = count  # every CulinaryDB recipe id is one distinct context
        candidate_id = conn.execute(
            "SELECT ingredient_id FROM ingredients WHERE canonical_name = ?",
            (hypothesis["candidate"],),
        ).fetchone()[0]
        conn.execute(
            """INSERT INTO novelty_observations(
                 analogy_id, component_id, candidate_ingredient_id, corpus_id,
                 observed_count, context_count, contexts, target_covered,
                 candidate_covered, result_class, observed_at)
               VALUES (?,?,?,?,?,?,?,?,?,?,?)
               ON CONFLICT(analogy_id, component_id, corpus_id) DO UPDATE SET
                 candidate_ingredient_id=excluded.candidate_ingredient_id,
                 observed_count=excluded.observed_count,
                 context_count=excluded.context_count, contexts=excluded.contexts,
                 target_covered=excluded.target_covered,
                 candidate_covered=excluded.candidate_covered,
                 result_class=excluded.result_class, observed_at=excluded.observed_at""",
            (
                hypothesis["analogy_id"], component["component_id"], candidate_id,
                corpus_id, count, context_count, contexts or None,
                int(target_covered), int(candidate_covered), result, observed_at,
            ),
        )
        if result == "insufficient_coverage":
            summary["insufficient_coverage"] += 1
        elif result == "not_observed":
            summary["not_observed"] += 1
        else:
            summary["observed"] += 1
    conn.commit()
    return summary


def backfill(conn: sqlite3.Connection, dir_path: Path | str,
             verbose: bool = False) -> dict[str, int]:
    """Attach corpus co-occurrence evidence to every pairing that has a target
    transformation. Leaves `confidence` and `curated_role_fit` untouched.
    Returns a small summary {updated, skipped, zero}."""
    entity_recipes, recipe_titles, name_index = load_corpus(dir_path)

    rows = conn.execute(
        """
        SELECT p.pairing_id,
               i.canonical_name AS filler_name,
               ti.canonical_name AS target_name,
               p.confidence, p.curated_role_fit
        FROM pairings p
        JOIN ingredients i ON i.ingredient_id = p.ingredient_id
        LEFT JOIN transformations t
            ON t.transformation_id = p.works_best_with_transformation_id
        LEFT JOIN ingredients ti ON ti.ingredient_id = t.ingredient_id
        """
    ).fetchall()

    summary = {"updated": 0, "skipped": 0, "zero": 0}
    for r in rows:
        filler_name = r["filler_name"]
        target_name = r["target_name"]
        if not target_name:
            summary["skipped"] += 1
            continue
        filler_entities = resolve_entities(filler_name, name_index)
        target_entities = resolve_entities(target_name, name_index)
        if not filler_entities or not target_entities:
            summary["zero"] += 1
            continue
        count, contexts = cooccurrence(entity_recipes, recipe_titles,
                                        filler_entities, target_entities)
        conn.execute(
            "UPDATE pairings SET corpus_cooccurrence_count = ?, corpus_contexts = ? "
            "WHERE pairing_id = ?",
            (count, contexts or None, r["pairing_id"]),
        )
        if count:
            summary["updated"] += 1
        else:
            summary["zero"] += 1
        if verbose:
            print(f"  {filler_name} + {target_name}: {count} recipes")
    conn.commit()
    return summary
