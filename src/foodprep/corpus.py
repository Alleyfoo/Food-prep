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