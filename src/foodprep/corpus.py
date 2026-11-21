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
import re
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


def _synonym_variants(raw: str) -> list[str]:
    """Readable names for one CulinaryDB synonym.

    Synonyms are ``;``-separated and written head-first: ``cheese-gruyere`` is
    gruyere cheese, ``vinegar-cider`` cider vinegar, and ``=`` joins one word
    (``hazel=nut``). Splitting on ``,`` alone indexed "bread; bun" as a single
    unusable key, so every entity with two synonyms was half invisible.
    """
    raw = raw.strip().strip("#").strip()
    if not raw:
        return []
    joined = raw.replace("=", " ")
    variants = [_norm(joined.replace("-", " "))]
    if "-" in joined:
        head, _, rest = joined.partition("-")
        variants.append(_norm(f"{rest.replace('-', ' ')} {head}"))
    return variants


def _singular_forms(name: str) -> list[str]:
    """``eggs`` -> ``egg``, ``juniper berries`` -> ``juniper berry``."""
    words = name.split()
    last = words[-1] if words else ""
    forms = []
    if last.endswith("ies") and len(last) > 4:
        forms.append(last[:-3] + "y")
    if last.endswith("es") and len(last) > 3:
        forms.append(last[:-2])
    if last.endswith("s") and not last.endswith("ss") and len(last) > 2:
        forms.append(last[:-1])
    return [" ".join(words[:-1] + [f]) for f in forms]


ORIGINAL_PREFIX = "original:"


def _original_name(raw: str) -> str:
    """A recipe's own ingredient wording, reduced to lowercase words."""
    return " ".join(re.sub(r"[^a-z]+", " ", raw.lower()).split())


#: The same food under the corpus's name — identity, never a broader family.
#: brown_butter is NOT butter and smoked_salt is NOT salt: mapping them would
#: let butter's 12,000 recipes vouch for a pairing nobody has measured.
#: Add an entry only when a cook would buy the corpus item to make ours.
NOVELTY_IDENTITY: dict[str, str] = {
    "caraway_seeds": "caraway",         # the spice is the seed
    "pomegranate_seeds": "pomegranate", # recipes say pomegranate, mean arils
    "gruyere": "gruyere cheese",
    "rye_crumbs": "rye bread",          # crumbs are toasted rye bread
}


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
                for raw in re.split(r"[;,]", r.get(field) or ""):
                    for variant in _synonym_variants(raw):
                        name_index.setdefault(variant, eid)

    entity_recipes: dict[int, set[int]] = {}
    used_as: dict[str, dict[int, int]] = {}  # recipe-file name -> entity -> uses
    originals: dict[str, int] = {}             # cook's wording -> pseudo-entity
    with open(dir_path / "04_Recipe-Ingredients_Aliases.csv", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            try:
                rid = int(r["Recipe ID"])
                eid = int(r["Entity ID"])
            except (ValueError, KeyError):
                continue
            entity_recipes.setdefault(eid, set()).add(rid)
            # The cook's own wording survives in "Original Ingredient Name"
            # even when CulinaryDB files it under a general entity (balsamic
            # vinegar -> vinegar). Keep it as its own pseudo-entity, with a
            # negative id, so a specific candidate can be measured by what
            # recipes actually said instead of by its broad family.
            original = _original_name(r.get("Original Ingredient Name") or "")
            if original:
                if original not in originals:
                    originals[original] = -(len(originals) + 1)
                entity_recipes.setdefault(originals[original], set()).add(rid)
            # file 04 names are lowercase aliases — index them too for coverage
            raw = (r.get("Aliased Ingredient Name") or "").strip()
            if raw:
                counts = used_as.setdefault(_norm(raw), {})
                counts[eid] = counts.get(eid, 0) + 1
                if _norm(raw) not in name_index:
                    name_index[_norm(raw)] = eid

    # The ingredient list and the recipe links sometimes disagree: "anchovy"
    # is entity 720 in 02_Ingredients, but all 241 recipes link it as 2073,
    # so 720 has no recipes and anchovy looked absent from the corpus. When
    # an indexed entity is never used and the recipes use the same name for
    # another entity, follow the recipes.
    for name, eid in list(name_index.items()):
        if entity_recipes.get(eid) or name not in used_as:
            continue
        used = max(used_as[name].items(), key=lambda item: item[1])[0]
        if entity_recipes.get(used):
            name_index[name] = used

    # Original wordings go in under a prefix: they are only for the strict
    # novelty fallback, never for the broad lookups pairings use.
    for original, pseudo in originals.items():
        name_index[ORIGINAL_PREFIX + original] = pseudo

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
    name = _norm(canonical.replace("_", " "))
    candidates = [name, *_singular_forms(name)]
    if canonical in NOVELTY_IDENTITY:
        candidates.append(_norm(NOVELTY_IDENTITY[canonical]))
    for candidate in candidates:
        entity = name_index.get(candidate)
        if entity is not None:
            return [entity]
    # Fall back to what cooks wrote: every original wording that contains the
    # name as whole words ("aged balsamic vinegar" counts for balsamic
    # vinegar; "vinegar" alone does not).
    phrases = [f" {c} " for c in candidates]
    found = [
        entity for key, entity in name_index.items()
        if key.startswith(ORIGINAL_PREFIX)
        and any(p in f" {key[len(ORIGINAL_PREFIX):]} " for p in phrases)
    ]
    return sorted(set(found))


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


#: Below this many expected co-occurrences, a zero is indistinguishable from
#: chance. miso appears in 0.23% of recipes and rutabaga in 0.14%, so the two
#: are expected to meet 0.15 times in 45k recipes — finding none is not a
#: discovery. Absence is only evidence where the corpus had a real chance to
#: show the pairing.
MIN_EXPECTED_FOR_ABSENCE = 3.0


def novelty_class(observed_count: int, covered: bool,
                  expected_count: float | None = None) -> str:
    """Transparent provisional classes based on distinct recipe occurrence.

    *expected_count* is N x p(target) x p(candidate) — how often the pairing
    would turn up by chance if the two were independent. Without enough of it
    a zero cannot be called novel, only unmeasurable.
    """
    if not covered:
        return "insufficient_coverage"
    if observed_count == 0:
        if expected_count is not None and expected_count < MIN_EXPECTED_FOR_ABSENCE:
            return "underpowered"
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
    summary = {"observed": 0, "not_observed": 0, "insufficient_coverage": 0,
               "underpowered": 0}
    for hypothesis in generate_scout_hypotheses(conn, component_name):
        candidate_entities = resolve_novelty_entities(
            hypothesis["candidate"], name_index
        )
        candidate_covered = bool(candidate_entities) and any(
            entity_recipes.get(entity) for entity in candidate_entities
        )
        covered = target_covered and candidate_covered
        count, contexts = (0, "")
        expected = None
        if covered:
            count, contexts = cooccurrence(
                entity_recipes, recipe_titles, candidate_entities, target_entities
            )
            # How often the two would meet by chance, so a zero can be judged.
            target_recipes: set[int] = set()
            for e in target_entities:
                target_recipes |= entity_recipes.get(e, set())
            candidate_recipes: set[int] = set()
            for e in candidate_entities:
                candidate_recipes |= entity_recipes.get(e, set())
            n_recipes = len(recipe_titles) or 1
            expected = len(target_recipes) * len(candidate_recipes) / n_recipes
        result = novelty_class(count, covered, expected)
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
        elif result == "underpowered":
            summary["underpowered"] += 1
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
