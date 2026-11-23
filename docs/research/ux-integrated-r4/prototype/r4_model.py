"""R4 presentation model: one ingredient's knowledge as records with
independent dimensions.

R3 gave every relation ONE `status` (curated / on hand / source / idea /
tested / not recorded). That mixed independent questions: brown butter on
roasted broccoli is an experimental pairing AND a Scout idea AND tested once,
and it may or may not be on hand. R4 keeps those as separate fields:

    knowledge     what kind of statement: "curated" | "experimental" | "generated"
                  (curated relationship, experimental pairing, Scout hypothesis)
    confidence    {"field", "value"}: the field's own name is kept, because
                  `confidence` (editor's judgement), `attestation` (how common a
                  route is) and `inference_strength` (how sound an analogy's
                  reasoning is) are different scales and must not be merged
    availability  "on hand" | "not on hand" | None (not applicable)
    evidence      {"coverage", "sources": [...], "corpus"}: sources with their
                  recorded claim scope (None = not recorded, shown as such)
    testing       None (not applicable) | {"status": "untested"|"tested", "trials"}
    coverage      "recorded" | "not recorded" | "not applicable"
    optionality   "required" | "supporting" | "finish" | None

Every record has a stable id built from database keys (pairing_id,
transformation_id, route_id, analogy_id, component_id, ingredient_id,
trial_id). Records that describe the same (prepared ingredient, ingredient)
pair are LINKED by those ids, never merged and never matched by text; the
link says what each record contributes.

Nothing here ranks, scores or infers. It reads the existing query layer and
tables. Missing information is "not recorded", never "no".
"""
from __future__ import annotations

import sqlite3
from typing import Any

from foodprep import query

KNOWLEDGE = ("curated", "experimental", "generated")
KNOWLEDGE_LABEL = {"curated": "curated", "experimental": "experimental pairing",
                   "generated": "Scout idea (generated)"}
CONFIDENCE_FIELD_LABEL = {"confidence": "confidence",
                          "attestation": "attestation",
                          "inference_strength": "inference strength"}


def pretty(name: str | None) -> str:
    return (name or "").replace("_component", "").replace("_base", " base") \
        .replace("_", " ").strip()


def _ids(conn) -> tuple[dict, dict]:
    comp = {r[0]: r[1] for r in conn.execute("SELECT name, component_id FROM components")}
    ing = {r[0]: r[1] for r in conn.execute(
        "SELECT canonical_name, ingredient_id FROM ingredients")}
    return comp, ing


def _source_rows(conn, sql: str, key: int) -> list[dict]:
    return [{"source_id": r["source_id"], "title": r["title"],
             "type": r["source_type"], "citation": r["citation_text"],
             "license": r["license"], "claim_scope": r["claim_scope"]}
            for r in conn.execute(sql, (key,))]


_STEP_SOURCES = """SELECT s.source_id, s.title, s.source_type, s.citation_text,
                          s.license, e.claim_scope
                   FROM transformation_evidence e JOIN evidence_sources s USING (source_id)
                   WHERE e.transformation_id = ? ORDER BY s.title"""
_PAIR_SOURCES = """SELECT s.source_id, s.title, s.source_type, s.citation_text,
                          s.license, e.claim_scope
                   FROM pairing_evidence e JOIN evidence_sources s USING (source_id)
                   WHERE e.pairing_id = ? ORDER BY s.title"""


def _evidence(sources: list[dict], corpus: int | None = None,
              applicable: bool = True) -> dict:
    if not applicable:
        return {"coverage": "not applicable", "sources": [], "corpus": None}
    ev = {"coverage": "sourced" if sources else "no source recorded",
          "sources": sources, "corpus": None}
    if corpus is not None:
        ev["corpus"] = {"count": corpus}
    return ev


def _pairings(conn, tid: int) -> list[sqlite3.Row]:
    return list(conn.execute(
        """SELECT p.pairing_id, p.ingredient_id, i.canonical_name AS filler,
                  r.role_name AS role, p.confidence, p.application,
                  p.availability_class, p.common_context, p.notes,
                  p.curated_role_fit, p.corpus_cooccurrence_count AS corpus
           FROM pairings p JOIN ingredients i USING (ingredient_id)
           JOIN roles r USING (role_id)
           WHERE p.works_best_with_transformation_id = ?
           ORDER BY r.role_name, i.canonical_name""", (tid,)))


def _trials(conn, analogy_id: str, component_id: int, ingredient_id: int) -> list[dict]:
    return [dict(r) for r in conn.execute(
        """SELECT trial_id, tested_at, verdict, preparation, ratio, temperature,
                  supporting_ingredients, observations, failure_mode,
                  successful_correction, safety_confirmed
           FROM tasting_trials
           WHERE analogy_id = ? AND component_id = ? AND candidate_ingredient_id = ?
           ORDER BY tested_at, trial_id""", (analogy_id, component_id, ingredient_id))]


def build(conn: sqlite3.Connection, ingredient: str,
          have: list[str] | None = None) -> dict[str, Any]:
    """{'ingredient', 'have', 'states', 'records', 'links', 'roles', 'sources'}.

    states   one dict per prepared ingredient, in the query layer's order
    records  every relationship as a record with independent dimensions
    links    groups of records about the same (component_id, ingredient_id)
    roles    role names in first-seen order (matrix columns)
    sources  source_id -> source dict, every source any record cites
    """
    have_set = {h for h in (have or []) if h}
    comp_id, ing_id = _ids(conn)
    states: list[dict] = []
    records: list[dict] = []
    roles_order: list[str] = []
    sources: dict[int, dict] = {}

    def avail(name: str | None) -> str | None:
        if not name:
            return None
        return "on hand" if name in have_set else "not on hand"

    def add(rec: dict) -> dict:
        base = {"role": None, "ingredient": None, "ingredient_id": None,
                "route_id": None, "confidence": None, "availability": None,
                "evidence": _evidence([], applicable=False), "testing": None,
                "coverage": "recorded", "optionality": None, "attrs": {}}
        base.update(rec)
        for s in base["evidence"]["sources"]:
            sources.setdefault(s["source_id"], {k: v for k, v in s.items()
                                                if k != "claim_scope"})
        records.append(base)
        return base

    for rank, card in enumerate(query.all_branch_cards(conn, ingredient), 1):
        comp = card["component"]
        cid = card["component_id"]
        tid = card["transformation_id"]
        inp = conn.execute(
            """SELECT c.name FROM transformations t
               LEFT JOIN components c ON c.component_id = t.input_component_id
               WHERE t.transformation_id = ?""", (tid,)).fetchone()[0]
        step_sources = _source_rows(conn, _STEP_SOURCES, tid)
        profile = query.component_state_profile(conn, comp)
        state = {
            "rank": rank, "component": comp, "component_id": cid,
            "label": pretty(comp), "transformation_id": tid,
            "technique": card["technique"],
            "from": inp, "from_label": pretty(inp) if inp else f"raw {pretty(ingredient)}",
            "confidence": card["confidence"],
            "flavour_shift": card["flavour_shift"],
            "texture_shift": card["texture_shift"],
            "keeps_well": card["keeps_well"],
            "freezes_well": bool(card["freezes_well"]),
            "batch_prep_value": card["batch_prep_value"],
            "risks": [pretty(r) for r in card["risks"]],
            "profile": profile,
            "uses": query.dish_contexts_for_component(conn, comp),
        }
        states.append(state)

        add({"id": f"transformation:{tid}", "kind": "transformation",
             "state": comp, "component_id": cid, "knowledge": "curated",
             "ingredient": inp or ingredient,
             "confidence": {"field": "confidence", "value": card["confidence"]},
             "evidence": _evidence(step_sources),
             "attrs": {"technique": card["technique"],
                       "from": inp or ingredient, "chained": bool(inp)}})

        pairs = _pairings(conn, tid)
        for m in card["missing"]:
            role = m["role_name"]
            if role not in roles_order:
                roles_order.append(role)
            cook = [p for p in pairs if p["role"] == role and p["confidence"] != "experimental"]
            exp = [p for p in pairs if p["role"] == role and p["confidence"] == "experimental"]
            add({"id": f"need:{tid}:{role}", "kind": "need", "state": comp,
                 "component_id": cid, "role": role, "knowledge": "curated",
                 "coverage": "recorded" if cook else "not recorded",
                 "attrs": {"priority": m["priority"], "note": m["note"],
                           "curated_pairings": len(cook),
                           "experimental_pairings": len(exp)}})
        needed = {m["role_name"] for m in card["missing"]}
        for p in pairs:
            psrc = _source_rows(conn, _PAIR_SOURCES, p["pairing_id"])
            add({"id": f"pairing:{p['pairing_id']}", "kind": "pairing",
                 "state": comp, "component_id": cid, "role": p["role"],
                 "ingredient": p["filler"], "ingredient_id": p["ingredient_id"],
                 "knowledge": ("experimental" if p["confidence"] == "experimental"
                               else "curated"),
                 "confidence": {"field": "confidence", "value": p["confidence"]},
                 "availability": avail(p["filler"]),
                 "evidence": _evidence(psrc, corpus=p["corpus"]),
                 "attrs": {"application": p["application"],
                           "availability_class": p["availability_class"],
                           "context": p["common_context"], "notes": p["notes"],
                           "role_fit": p["curated_role_fit"],
                           "role_is_needed": p["role"] in needed}})

        for rt in query.flavour_routes_for_component(conn, comp, sorted(have_set)):
            rid = rt["route_id"]
            add({"id": f"route:{rid}:{cid}", "kind": "route_fit", "state": comp,
                 "component_id": cid, "route_id": rid, "knowledge": "curated",
                 "confidence": {"field": "attestation", "value": rt["attestation"]},
                 "evidence": {"coverage": "no source table for routes",
                              "sources": [], "corpus": None},
                 "attrs": {"name": rt["name"], "fit_reason": rt.get("fit_reason"),
                           "description": rt["description"], "risks": rt["risks"],
                           "dimensions": rt["flavour_dimensions"],
                           "context": rt.get("cultural_context"),
                           "required_on_hand": list(rt["required_coverage"])}})
            for e in rt["elements"]:
                add({"id": f"element:{rid}:{ing_id.get(e['ingredient'])}:{cid}",
                     "kind": "route_element", "state": comp, "component_id": cid,
                     "route_id": rid, "ingredient": e["ingredient"],
                     "ingredient_id": ing_id.get(e["ingredient"]),
                     "knowledge": "curated", "availability": avail(e["ingredient"]),
                     "optionality": e["optionality"],
                     "attrs": {"contribution": e["contribution"], "route": rt["name"]}})

        for h in query.generate_scout_hypotheses(conn, comp):
            cand_id = h["substitute_ingredient_id"]
            trials = _trials(conn, h["analogy_id"], cid, cand_id)
            nov = h.get("novelty") or {}
            add({"id": f"idea:{h['analogy_id']}:{cid}:{cand_id}", "kind": "idea",
                 "state": comp, "component_id": cid, "ingredient": h["candidate"],
                 "ingredient_id": cand_id, "knowledge": "generated",
                 "confidence": {"field": "inference_strength",
                                "value": h["inference_strength"]},
                 "availability": avail(h["candidate"]),
                 "testing": {"status": "tested" if trials else "untested",
                             "trials": trials},
                 "attrs": {"analogy_id": h["analogy_id"], "replaces": h["source"],
                           "mechanism": h["mechanism"],
                           "shared_function": h["shared_function"],
                           "difference": h["meaningful_difference"],
                           "risk": h["expected_risk"],
                           "novelty": nov.get("class"),
                           "novelty_corpus": nov.get("corpus_name"),
                           "novelty_count": nov.get("observed_count"),
                           "protocol": h.get("protocol")}})

    # Matrix columns: needed roles first (query order), then roles that only
    # appear on pairings (a pairing may fill a role the state doesn't list).
    for r in records:
        if r["kind"] == "pairing" and r["role"] not in roles_order:
            roles_order.append(r["role"])
    links = _links(records)
    return {"ingredient": ingredient, "have": sorted(have_set), "states": states,
            "records": records, "links": links, "roles": roles_order,
            "sources": sources,
            "corpus_populated": bool(conn.execute(
                "SELECT MAX(corpus_cooccurrence_count) FROM pairings").fetchone()[0])}


def _links(records: list[dict]) -> list[dict]:
    """Group pairing and idea records that share (component_id, ingredient_id).

    The basis is the two database ids, never names. The records stay separate;
    the link only says they concern the same prepared ingredient and the same
    ingredient. Route elements are NOT linked: a route element is about a
    route, not about a pairing, even when the ingredient is the same.
    """
    groups: dict[tuple, list[dict]] = {}
    for r in records:
        if r["kind"] in ("pairing", "idea") and r["ingredient_id"]:
            groups.setdefault((r["component_id"], r["ingredient_id"]), []).append(r)
    out = []
    for (cid, iid), recs in groups.items():
        kinds = {r["kind"] for r in recs}
        if len(kinds) < 2:
            continue
        out.append({"component_id": cid, "ingredient_id": iid,
                    "state": recs[0]["state"], "ingredient": recs[0]["ingredient"],
                    "records": [r["id"] for r in recs],
                    "basis": "same component_id and ingredient_id"})
    return out


# ---------------------------------------------------------------------------
# helpers the views share
# ---------------------------------------------------------------------------

def of(m: dict, state: str | None = None, kind: str | tuple | None = None) -> list[dict]:
    kinds = (kind,) if isinstance(kind, str) else kind
    return [r for r in m["records"]
            if (state is None or r["state"] == state)
            and (kinds is None or r["kind"] in kinds)]


def state_by(m: dict, comp: str) -> dict | None:
    return next((s for s in m["states"] if s["component"] == comp), None)


def linked(m: dict, rec: dict) -> list[dict]:
    """Other records linked to *rec* by ids (see `_links`)."""
    for g in m["links"]:
        if rec["id"] in g["records"]:
            return [r for r in m["records"] if r["id"] in g["records"] and r is not rec]
    return []


def route_ids(m: dict, comp: str) -> list[str]:
    return [r["route_id"] for r in of(m, comp, "route_fit")]


def gaps(m: dict, comp: str) -> list[str]:
    """What is NOT recorded for a state, said plainly (never 'not needed')."""
    s = state_by(m, comp)
    out = []
    unpaired = [r["role"] for r in of(m, comp, "need") if r["coverage"] == "not recorded"]
    if unpaired:
        out.append("no curated pairing for " + ", ".join(unpaired))
    if not of(m, comp, "route_fit"):
        out.append("no flavour route")
    if not of(m, comp, "transformation")[0]["evidence"]["sources"]:
        out.append("no source for the step")
    pairs = [r for r in of(m, comp, "pairing") if r["knowledge"] == "curated"]
    if pairs and not any(r["evidence"]["sources"] for r in pairs):
        out.append("no source for any pairing")
    if not s["profile"]:
        out.append("no sensory profile")
    if not of(m, comp, "need"):
        out.append("no needed roles")
    return out


def shared_gaps(m: dict) -> list[str]:
    """Gaps every state of the ingredient has: stated once, not per row."""
    if len(m["states"]) < 2:
        return []
    sets = [set(gaps(m, s["component"])) for s in m["states"]]
    common = set.intersection(*sets)
    return [g for g in gaps(m, m["states"][0]["component"]) if g in common]


def corpus_populated(m: dict) -> bool:
    """False when every pairing in the database has a corpus count of 0: the
    column was not backfilled, so 0 must not be read as 'never seen together'."""
    return m["corpus_populated"]
