"""Load curated YAML ontology into SQLite.

The YAML is the human-editable source of truth; this module is the compiler that
turns it into queryable rows. Names in the YAML (role names, technique names,
ingredient names, source ids) are resolved to surrogate ids here.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

import yaml

from .db import rebuild
from .vocabulary import VOCABULARY_PATH, load_vocabulary

DATA_PATH = Path(__file__).with_name("data") / "tomato.yaml"
PROFILES_PATH = Path(__file__).with_name("data") / "component_profiles.yaml"
DESTINATIONS_PATH = Path(__file__).with_name("data") / "destination_profiles.yaml"
ROUTES_PATH = Path(__file__).with_name("data") / "flavour_routes.yaml"

CONFIDENCE_OK = {"high", "medium_high", "medium", "low", "experimental"}


class LoadError(ValueError):
    pass


def _split_list(text: str | None) -> list[str]:
    if not text:
        return []
    return [line.strip() for line in text.splitlines() if line.strip()]


def _ingredient_id(conn: sqlite3.Connection, canonical: str) -> int:
    row = conn.execute(
        "SELECT ingredient_id FROM ingredients WHERE canonical_name = ?", (canonical,)
    ).fetchone()
    if row is None:
        raise LoadError(f"ingredient not found: {canonical!r}")
    return row[0]


def _technique_id(conn: sqlite3.Connection, name: str) -> int:
    row = conn.execute(
        "SELECT technique_id FROM techniques WHERE name = ?", (name,)
    ).fetchone()
    if row is None:
        raise LoadError(f"technique not found: {name!r}")
    return row[0]


def _component_id(conn: sqlite3.Connection, name: str) -> int:
    row = conn.execute(
        "SELECT component_id FROM components WHERE name = ?", (name,)
    ).fetchone()
    if row is None:
        raise LoadError(f"component not found: {name!r}")
    return row[0]


def _role_id(conn: sqlite3.Connection, name: str) -> int:
    row = conn.execute(
        "SELECT role_id FROM roles WHERE role_name = ?", (name,)
    ).fetchone()
    if row is None:
        raise LoadError(f"role not found: {name!r}")
    return row[0]


def _tag_id(conn: sqlite3.Connection, family: str, value: str) -> int:
    row = conn.execute(
        "SELECT tag_id FROM tags WHERE family = ? AND tag_value = ?", (family, value)
    ).fetchone()
    if row is None:
        raise LoadError(f"tag not found: {family}:{value!r}")
    return row[0]


def _dish_id(conn: sqlite3.Connection, name: str) -> int:
    row = conn.execute(
        "SELECT dish_context_id FROM dish_contexts WHERE name = ?", (name,)
    ).fetchone()
    if row is None:
        raise LoadError(f"dish_context not found: {name!r}")
    return row[0]


def _source_id(conn: sqlite3.Connection, sid: str) -> int:
    row = conn.execute(
        "SELECT source_id FROM evidence_sources WHERE title = ?", (sid,)
    ).fetchone()
    if row is None:
        raise LoadError(f"evidence_source not found: {sid!r}")
    return row[0]


def load_yaml(path: Path | str = DATA_PATH) -> dict:
    with open(path, "r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def _deep_merge(base: dict, extra: dict) -> dict:
    """Merge two ontology dicts: list-valued keys are extended, scalars overwritten.
    component_profiles from the profiles file join tomato.yaml's (if any)."""
    for key, val in (extra or {}).items():
        if key in base and isinstance(base[key], list) and isinstance(val, list):
            base[key] = base[key] + val
        else:
            base[key] = val
    return base


def populate(conn: sqlite3.Connection, data: dict, vocabulary=None) -> None:
    """Insert a parsed ontology dict into a freshly-schemed database."""
    # ---- vocabulary ----
    for r in data.get("roles", []):
        conn.execute(
            "INSERT INTO roles(role_name, role_family) VALUES (?,?)",
            (r["name"], r.get("family")),
        )
    for t in data.get("tags", []):
        conn.execute(
            "INSERT INTO tags(family, tag_value) VALUES (?,?)",
            (t["family"], t["value"]),
        )
    for d in data.get("dish_contexts", []):
        conn.execute("INSERT INTO dish_contexts(name) VALUES (?)", (d,))
    for s in data.get("evidence_sources", []):
        conn.execute(
            "INSERT INTO evidence_sources(source_type, title, license, citation_text) "
            "VALUES (?,?,?,?)",
            (s.get("source_type"), s["id"], s.get("license"), s.get("citation_text")),
        )
    for tech in data.get("techniques", []):
        conn.execute(
            "INSERT INTO techniques(name, is_modifier, heat_type, moisture_change, "
            "preservation_flag, notes) VALUES (?,?,?,?,?,?)",
            (
                tech["name"],
                int(tech.get("is_modifier", 0)),
                tech.get("heat_type"),
                tech.get("moisture_change"),
                int(tech.get("preservation_flag", 0)),
                tech.get("notes"),
            ),
        )

    # ---- ingredients (tomato + fillers) ----
    for ing in data.get("ingredients", []):
        conn.execute(
            "INSERT INTO ingredients(canonical_name, aliases, base_roles, "
            "default_availability_class, kind, repairs, avoid_when, notes) "
            "VALUES (?,?,?,?,?,?,?,?)",
            (
                ing["canonical_name"],
                ing.get("aliases"),
                ing.get("base_roles"),
                ing.get("default_availability_class"),
                ing.get("kind", "filler"),
                ing.get("repairs"),
                ing.get("avoid_when"),
                ing.get("notes"),
            ),
        )
        ing_id = conn.execute(
            "SELECT ingredient_id FROM ingredients WHERE canonical_name = ?",
            (ing["canonical_name"],),
        ).fetchone()[0]
        for avail in ing.get("availability", [
            {"region_code": "FI",
             "availability_class": ing.get("default_availability_class"),
             "seasonality_note": ing.get("seasonality_note")}
        ]):
            if not avail or not avail.get("availability_class"):
                continue
            conn.execute(
                "INSERT INTO availability(ingredient_id, region_code, "
                "availability_class, seasonality_note) VALUES (?,?,?,?)",
                (ing_id, avail["region_code"], avail["availability_class"],
                 avail.get("seasonality_note")),
            )

    # ---- components ----
    for c in data.get("components", []):
        conn.execute(
            "INSERT INTO components(name, component_kind, keeps_well, freezes_well, "
            "batch_prep_value, notes) VALUES (?,?,?,?,?,?)",
            (
                c["name"],
                c.get("kind"),
                c.get("keeps_well"),
                int(c.get("freezes_well", 0)),
                c.get("batch_prep_value"),
                c.get("notes"),
            ),
        )

    # ---- component profiles (meal-repair plate items) ----
    for cp in data.get("component_profiles", []):
        conn.execute(
            "INSERT INTO component_profiles(name, aliases, provides_roles, "
            "flavour_tags, texture_tags, missing_risks, heaviness_score, "
            "dryness_score, notes) VALUES (?,?,?,?,?,?,?,?,?)",
            (cp["name"], cp.get("aliases"), cp.get("provides", cp.get("provides_roles")),
             cp.get("flavour", cp.get("flavour_tags")),
             cp.get("texture", cp.get("texture_tags")),
             cp.get("missing_risks"),
             cp.get("heaviness_score"), cp.get("dryness_score"), cp.get("notes")),
        )

    default_ing = data.get("default_ingredient", "tomato")

    # ---- transformations (the core record) ----
    # Each entry may name its own ingredient; default is default_ing.
    for tr in data.get("transformations", []):
        ing_name = tr.get("ingredient", default_ing)
        ing_id = _ingredient_id(conn, ing_name)
        tech_id = _technique_id(conn, tr["technique"])
        comp_id = _component_id(conn, tr["output_component"])
        conf = tr["confidence"]
        if conf not in CONFIDENCE_OK:
            raise LoadError(f"bad confidence {conf!r} in {tr['technique']}")
        conn.execute(
            "INSERT INTO transformations(ingredient_id, technique_id, "
            "output_component_id, flavour_shift, texture_shift, confidence, "
            "risks, notes) VALUES (?,?,?,?,?,?,?,?)",
            (ing_id, tech_id, comp_id, tr.get("flavour_shift"),
             tr.get("texture_shift"), conf, tr.get("risks"), tr.get("notes")),
        )
        tr_id = conn.execute(
            "SELECT transformation_id FROM transformations "
            "WHERE ingredient_id = ? AND technique_id = ?",
            (ing_id, tech_id),
        ).fetchone()[0]

        state_profile = tr.get("state_profile")
        if state_profile:
            for role in _split_list(state_profile.get("provides")):
                _role_id(conn, role)  # validate authored functional claims
            conn.execute(
                "INSERT INTO component_state_profiles(component_id, provides_roles, "
                "flavour_tags, texture_tags, missing_risks, heaviness_score, "
                "dryness_score, notes) VALUES (?,?,?,?,?,?,?,?)",
                (
                    comp_id, state_profile.get("provides"),
                    state_profile.get("flavour"), state_profile.get("texture"),
                    state_profile.get("missing_risks"),
                    state_profile.get("heaviness_score"),
                    state_profile.get("dryness_score"), state_profile.get("notes"),
                ),
            )

        for tg in tr.get("tags_after", []):
            conn.execute(
                "INSERT INTO transformation_tags(transformation_id, tag_id, "
                "polarity, evidence_level) VALUES (?,?,?,?)",
                (tr_id, _tag_id(conn, tg["family"], tg["value"]),
                 tg.get("polarity"), tg.get("evidence_level")),
            )
        for mr in tr.get("missing_roles", []):
            conn.execute(
                "INSERT INTO transformation_missing_roles(transformation_id, "
                "role_id, priority, note) VALUES (?,?,?,?)",
                (tr_id, _role_id(conn, mr["role"]),
                 mr.get("priority"), mr.get("note")),
            )
        for use in tr.get("uses", []):
            conn.execute(
                "INSERT INTO component_uses(component_id, dish_context_id, strength) "
                "VALUES (?,?,?)",
                (comp_id, _dish_id(conn, use), "primary"),
            )
        for ev in tr.get("evidence", []):
            conn.execute(
                "INSERT INTO transformation_evidence(transformation_id, source_id, "
                "claim_scope) VALUES (?,?,?)",
                (tr_id, _source_id(conn, ev["source"]), ev.get("scope")),
            )

    # ---- pairings ----
    # for_ingredient names which ingredient's transformation the pairing targets;
    # default is default_ing. works_best_with is a technique name on that ingredient.
    for p in data.get("pairings", []):
        filler_id = _ingredient_id(conn, p["filler"])
        role_id = _role_id(conn, p["role"])
        wbtr_id = None
        if p.get("works_best_with"):
            target_ing = _ingredient_id(conn, p.get("for_ingredient", default_ing))
            row = conn.execute(
                "SELECT transformation_id FROM transformations "
                "WHERE ingredient_id = ? AND technique_id = ?",
                (target_ing, _technique_id(conn, p["works_best_with"])),
            ).fetchone()
            if row is not None:
                wbtr_id = row[0]
        conn.execute(
            "INSERT INTO pairings(ingredient_id, role_id, "
            "works_best_with_transformation_id, common_context, "
            "availability_class, confidence, curated_role_fit, notes) "
            "VALUES (?,?,?,?,?,?,?,?)",
            (filler_id, role_id, wbtr_id, p.get("context"),
             p.get("availability"), p.get("confidence"),
             p.get("curated_role_fit"), p.get("notes")),
        )
        pair_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
        for sid in p.get("evidence", []):
            conn.execute(
                "INSERT INTO pairing_evidence(pairing_id, source_id, claim_scope) "
                "VALUES (?,?,?)",
                (pair_id, _source_id(conn, sid), None),
            )

    # ---- product-facing journeys over existing transformations ----
    vocabulary = vocabulary or load_vocabulary()
    for journey in data.get("journeys", []):
        ingredient_id = _ingredient_id(conn, journey["ingredient"])
        preparation = vocabulary.require("preparations", journey["preparation"]).id
        correction = vocabulary.require("corrections", journey["correction"]).id
        confidence = vocabulary.require("confidence", journey["confidence"]).id
        transformation = conn.execute(
            "SELECT t.transformation_id FROM transformations t "
            "JOIN techniques tech ON tech.technique_id = t.technique_id "
            "WHERE t.ingredient_id = ? AND tech.name = ?",
            (ingredient_id, journey["primary_transformation"]),
        ).fetchone()
        if transformation is None:
            raise LoadError(
                "journey primary transformation not found: "
                f"{journey['ingredient']}/{journey['primary_transformation']}"
            )
        conn.execute(
            "INSERT INTO journeys(slug, ingredient_id, title, preparation_id, "
            "primary_transformation_id, starting_state, output_state, why_choose, "
            "sensory_change, flavour_direction, useful_additions, correction, "
            "becomes_possible, risks, confidence) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (
                journey["slug"], ingredient_id, journey["title"], preparation,
                transformation[0], journey["starting_state"], journey["output_state"],
                journey["why_choose"], journey["sensory_change"],
                journey["flavour_direction"], journey.get("useful_additions"),
                correction, journey["becomes_possible"], journey["risks"], confidence,
            ),
        )
        journey_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
        for destination in journey["destinations"]:
            destination_id = vocabulary.require("destinations", destination).id
            conn.execute(
                "INSERT INTO journey_destinations(journey_id, destination_id) VALUES (?,?)",
                (journey_id, destination_id),
            )
        for sequence_no, transition in enumerate(journey["transitions"], start=1):
            conn.execute(
                "INSERT INTO journey_transitions(journey_id, sequence_no, from_state, "
                "move, to_state, reason) VALUES (?,?,?,?,?,?)",
                (
                    journey_id, sequence_no, transition["from"], transition["move"],
                    transition["to"], transition["reason"],
                ),
            )

    # ---- destination profiles ----
    for profile in data.get("destination_profiles", []):
        destination = vocabulary.require("destinations", profile["destination"])
        conn.execute(
            "INSERT INTO destination_profiles(destination_id, name, texture_needs, "
            "moisture_needs, notes) VALUES (?,?,?,?,?)",
            (
                destination.id, destination.name, profile.get("texture_needs"),
                profile.get("moisture_needs"), profile.get("notes"),
            ),
        )
        seen_roles: set[str] = set()
        for function in profile.get("functions", []):
            role = function["role"]
            if role in seen_roles:
                raise LoadError(
                    f"duplicate destination function: {destination.id}/{role}"
                )
            seen_roles.add(role)
            importance = function["importance"]
            if importance not in {"required", "useful", "optional", "unsuitable"}:
                raise LoadError(
                    f"bad destination importance {importance!r} for {destination.id}/{role}"
                )
            conn.execute(
                "INSERT INTO destination_functions(destination_id, role_id, "
                "importance, reason) VALUES (?,?,?,?)",
                (destination.id, _role_id(conn, role), importance, function["reason"]),
            )

    # ---- reusable flavour routes ----
    for route in data.get("flavour_routes", []):
        confidence = vocabulary.require("confidence", route["confidence"]).id
        for dimension in _split_list(route["dimensions"]):
            vocabulary.require("flavours", dimension)
        conn.execute(
            "INSERT INTO flavour_routes(route_id, name, description, "
            "flavour_dimensions, risks, cultural_context, confidence) "
            "VALUES (?,?,?,?,?,?,?)",
            (
                route["id"], route["name"], route["description"],
                route["dimensions"], route["risks"], route.get("cultural_context"),
                confidence,
            ),
        )
        for state in route["states"]:
            conn.execute(
                "INSERT INTO flavour_route_states(route_id, component_id, fit_reason) "
                "VALUES (?,?,?)",
                (route["id"], _component_id(conn, state["component"]), state["reason"]),
            )
        for destination in route["destinations"]:
            destination_id = vocabulary.require("destinations", destination).id
            conn.execute(
                "INSERT INTO flavour_route_destinations(route_id, destination_id) "
                "VALUES (?,?)", (route["id"], destination_id),
            )
        for element in route["elements"]:
            optionality = element["optionality"]
            if optionality not in {"required", "supporting", "finish"}:
                raise LoadError(f"bad route optionality: {optionality!r}")
            conn.execute(
                "INSERT INTO flavour_route_elements(route_id, ingredient_id, "
                "contribution, optionality) VALUES (?,?,?,?)",
                (
                    route["id"], _ingredient_id(conn, element["ingredient"]),
                    element["contribution"], optionality,
                ),
            )


def build(conn: sqlite3.Connection, data_path: Path | str = DATA_PATH,
          profiles_path: Path | str | None = PROFILES_PATH,
          destinations_path: Path | str | None = DESTINATIONS_PATH,
          routes_path: Path | str | None = ROUTES_PATH,
          vocabulary_path: Path | str = VOCABULARY_PATH) -> None:
    """Rebuild schema and load the YAML ontology from scratch.

    The ingredient ontology (tomato/onion/potato, techniques, transformations,
    pairings) comes from data_path. Plate-item component profiles come from a
    separate profiles_path so they can grow independently of ingredient trees."""
    # Validate the shared Cook/Scout language before making destructive schema
    # changes, so a bad vocabulary cannot wipe an existing local database.
    vocabulary = load_vocabulary(vocabulary_path)
    rebuild(conn)
    data = load_yaml(data_path) or {}
    if profiles_path and Path(profiles_path).exists():
        data = _deep_merge(data, load_yaml(profiles_path) or {})
    if destinations_path and Path(destinations_path).exists():
        data = _deep_merge(data, load_yaml(destinations_path) or {})
    if routes_path and Path(routes_path).exists():
        data = _deep_merge(data, load_yaml(routes_path) or {})
    populate(conn, data, vocabulary)
    conn.commit()
