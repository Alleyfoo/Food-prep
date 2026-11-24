"""R1 data layer: the curated ontology and CulinaryDB statistics.

Everything here is read-only. The ontology comes from the shipped YAML
(foodprep.loader.build); the corpus from foodprep.corpus.resolve_corpus_dir.

Leakage rule for the whole study: nothing in this module that is used as a
feature may read the curated answers. The answers are
  * pairings (which filler is curated for which prepared state), and
  * Scout hypotheses (which substitute a rule proposes for which source).
`Ontology.answers_*` expose them for labels only; feature code never calls them.
Columns that exist only for curated rows (pairings.corpus_cooccurrence_count,
a hypothesis's compatibility_score) are never read.
"""
from __future__ import annotations

import math
import pickle
import sqlite3
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
from scipy import sparse
from scipy.sparse.linalg import svds

from foodprep import corpus, query
from foodprep.loader import build

ROLES = ["salt", "fat", "acid", "herb", "aromatic", "crunch", "body", "carb", "protein",
         "heat", "umami", "cream", "carrier", "hydration", "mild_base"]
FLAVOURS = ["salty", "sour", "sweet", "bitter", "umami", "pungent", "aromatic",
            "nutty_toasted", "fresh_green", "fermented_funky", "rich_fatty"]


def _split(v) -> list[str]:
    if v is None:
        return []
    if isinstance(v, list):
        return [x for x in v if x]
    return [x.strip() for x in str(v).replace(",", "\n").split("\n") if x.strip()]


@dataclass
class State:
    name: str
    component_id: int
    base: str                 # the base ingredient (broccoli for roasted broccoli)
    technique: str
    heat_type: str
    moisture_change: str
    serving_form: str
    flavour_tags: list[str]
    texture_tags: list[str]
    provides_roles: list[str]
    missing_risks: list[str]
    heaviness: float
    dryness: float
    transformation_tags: list[str]       # "polarity:family:value"
    keeps_well: str
    freezes_well: str
    curated_missing_roles: list[str]     # transformation_missing_roles: LEAKAGE PROBE ONLY


@dataclass
class Ingredient:
    name: str
    kind: str
    family: str
    roles: list[str]
    availability: str
    repairs: list[str]
    avoid_when: list[str]


@dataclass
class Ontology:
    states: dict[str, State]
    ingredients: dict[str, Ingredient]
    _pairings: list[tuple[str, str]] = field(repr=False, default_factory=list)
    _scout: list[tuple[str, str, str]] = field(repr=False, default_factory=list)

    def answers_pairings(self) -> set[tuple[str, str]]:
        """(state, filler) pairs curated in the ontology. LABELS ONLY."""
        return set(self._pairings)

    def answers_scout(self) -> set[tuple[str, str, str]]:
        """(state, source, substitute) from the Scout rules. LABELS ONLY."""
        return set(self._scout)


def load_ontology() -> Ontology:
    c = sqlite3.connect(":memory:")
    c.row_factory = sqlite3.Row
    build(c)
    ingredients: dict[str, Ingredient] = {}
    for r in c.execute("SELECT * FROM ingredients"):
        ingredients[r["canonical_name"]] = Ingredient(
            r["canonical_name"], r["kind"] or "", r["family"] or "none",
            _split(r["base_roles"]), r["default_availability_class"] or "unknown",
            _split(r["repairs"]), _split(r["avoid_when"]))

    states: dict[str, State] = {}
    rows = c.execute("""
        SELECT t.transformation_id, i.canonical_name AS base, te.name AS technique,
               te.heat_type, te.moisture_change, comp.name AS state, comp.component_id,
               comp.keeps_well, comp.freezes_well
        FROM transformations t
        JOIN ingredients i ON i.ingredient_id = t.ingredient_id
        JOIN techniques te ON te.technique_id = t.technique_id
        JOIN components comp ON comp.component_id = t.output_component_id""").fetchall()
    for r in rows:
        prof = query.component_state_profile(c, r["state"])
        if prof is None or r["state"] in states:
            continue
        tid = r["transformation_id"]
        tags = [f"{x['polarity'] or 'pos'}:{x['family']}:{x['tag_value']}" for x in c.execute(
            """SELECT tt.polarity, tg.family, tg.tag_value FROM transformation_tags tt
               JOIN tags tg ON tg.tag_id = tt.tag_id WHERE tt.transformation_id = ?""", (tid,))]
        missing = [x[0] for x in c.execute(
            """SELECT ro.role_name FROM transformation_missing_roles m
               JOIN roles ro ON ro.role_id = m.role_id WHERE m.transformation_id = ?""", (tid,))]
        states[r["state"]] = State(
            r["state"], r["component_id"], r["base"], r["technique"], r["heat_type"] or "none",
            r["moisture_change"] or "none", prof.get("serving_form") or "none",
            _split(prof.get("flavour_tags")), _split(prof.get("texture_tags")),
            _split(prof.get("provides_roles")), _split(prof.get("missing_risks")),
            float(prof.get("heaviness_score") or 0), float(prof.get("dryness_score") or 0),
            tags, str(r["keeps_well"] or "none"), str(r["freezes_well"] or "none"), missing)

    pairings = [(r["state"], r["filler"]) for r in c.execute("""
        SELECT comp.name AS state, i.canonical_name AS filler FROM pairings p
        JOIN transformations t ON t.transformation_id = p.works_best_with_transformation_id
        JOIN components comp ON comp.component_id = t.output_component_id
        JOIN ingredients i ON i.ingredient_id = p.ingredient_id""") if r["state"] in states]
    scout = []
    for s in states:
        for h in query.generate_scout_hypotheses(c, s):
            scout.append((s, h["source"], h["candidate"]))
    return Ontology(states, ingredients, pairings, scout)


# --------------------------------------------------------------------------
# CulinaryDB statistics
# --------------------------------------------------------------------------

@dataclass
class CorpusStats:
    n_recipes: int
    counts: dict[str, int]                     # ingredient -> recipes containing it
    pair: dict[tuple[str, str], int]           # sorted pair -> recipes with both
    vectors: dict[str, np.ndarray]             # SVD embedding of the PPMI matrix
    covered: set[str]
    resolution: dict[str, list[int]]

    def count(self, a: str) -> int:
        return self.counts.get(a, 0)

    def cooc(self, a: str, b: str) -> int:
        return self.pair.get(tuple(sorted((a, b))), 0)

    def lift(self, a: str, b: str, alpha: float = 1.0) -> float:
        """Smoothed lift: (n_ab + a) / (expected + a)."""
        exp = self.count(a) * self.count(b) / max(self.n_recipes, 1)
        return (self.cooc(a, b) + alpha) / (exp + alpha)

    def ppmi(self, a: str, b: str, alpha: float = 1.0) -> float:
        return max(0.0, math.log(self.lift(a, b, alpha)))

    def cos(self, a: str, b: str) -> float:
        va, vb = self.vectors.get(a), self.vectors.get(b)
        if va is None or vb is None:
            return 0.0
        d = float(np.linalg.norm(va) * np.linalg.norm(vb))
        return float(va @ vb / d) if d else 0.0


def _resolve(name: str, idx: dict[str, int]) -> list[int]:
    return corpus.resolve_entities(name, idx) or corpus.resolve_novelty_entities(name, idx)


def corpus_stats(names: list[str], dim: int = 48, cache: Path | None = None) -> CorpusStats:
    corpus_dir = corpus.resolve_corpus_dir()
    cache = cache or corpus_dir.parent / ".r1_stats.pkl"
    key = (tuple(sorted(names)), dim)
    if cache.exists():
        with open(cache, "rb") as fh:
            stored = pickle.load(fh)
        if stored[0] == key:
            return stored[1]
    entity_recipes, titles, idx = corpus.load_corpus(corpus_dir)
    n = len(titles)
    resolution = {nm: _resolve(nm, idx) for nm in names}
    recipes = {nm: set().union(*[entity_recipes.get(e, set()) for e in ents]) if ents else set()
               for nm, ents in resolution.items()}
    counts = {nm: len(r) for nm, r in recipes.items()}
    pair = {}
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            k = len(recipes[a] & recipes[b])
            if k:
                pair[tuple(sorted((a, b)))] = k

    # Embeddings: PPMI over every corpus entity with >= 20 recipes (the
    # corpus's own vocabulary, not only ours), including the cooks' original
    # wordings (negative ids: "olive oil" exists only as wording), then
    # truncated SVD. Our ingredients get the recipe-weighted mean vector of
    # the entities they resolve to.
    ents = sorted(e for e, r in entity_recipes.items() if len(r) >= 20)
    col = {e: j for j, e in enumerate(ents)}
    rid = {r: i for i, r in enumerate(titles)}
    rows, cols = [], []
    for e in ents:
        for r in entity_recipes[e]:
            if r in rid:
                rows.append(rid[r]); cols.append(col[e])
    R = sparse.csr_matrix((np.ones(len(rows)), (rows, cols)), shape=(len(rid), len(ents)))
    C = (R.T @ R).toarray().astype(float)
    np.fill_diagonal(C, 0)
    tot = C.sum()
    pr = C.sum(1, keepdims=True) / tot
    pc = (C.sum(0, keepdims=True) / tot) ** 0.75          # context smoothing
    pc = pc / pc.sum()
    with np.errstate(divide="ignore", invalid="ignore"):
        pmi = np.log((C / tot) / (pr @ pc))
    pmi[~np.isfinite(pmi)] = 0
    P = np.maximum(pmi, 0)
    U, S, _ = svds(sparse.csr_matrix(P), k=dim)
    E = U * np.sqrt(S)
    vectors = {}
    for nm, es in resolution.items():
        ws = [(E[col[e]], len(entity_recipes[e])) for e in es if e in col]
        if ws:
            vectors[nm] = sum(v * w for v, w in ws) / sum(w for _v, w in ws)
    stats = CorpusStats(n, counts, pair, vectors, {nm for nm, c in counts.items() if c > 0},
                        resolution)
    with open(cache, "wb") as fh:
        pickle.dump((key, stats), fh)
    return stats
