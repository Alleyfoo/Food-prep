-- food-prep SQLite schema
-- The core object is the TRANSFORMATION RECORD, not the recipe.
-- Centre of gravity: transformations + transformation_missing_roles.
--
-- Conventions:
--   - integer primary keys are surrogate ids
--   - text *_name columns are the human labels
--   - confidence / evidence_level use a controlled vocabulary:
--       high | medium_high | medium | low | experimental
--   - availability_class: very_common | common | occasional | rare | n/a

PRAGMA foreign_keys = ON;

-- ---------------------------------------------------------------------------
-- Identity & vocabulary
-- ---------------------------------------------------------------------------

CREATE TABLE ingredients (
    ingredient_id            INTEGER PRIMARY KEY AUTOINCREMENT,
    canonical_name           TEXT NOT NULL UNIQUE,
    aliases                  TEXT,            -- newline-separated
    base_roles               TEXT,            -- newline-separated role names
    default_availability_class TEXT,          -- very_common | common | ...
    kind                     TEXT NOT NULL DEFAULT 'filler',  -- full | filler | both
    repairs                  TEXT,            -- newline-separated plate conditions this filler repairs (heavy, fatty, roasted, ...)
    avoid_when               TEXT,            -- newline-separated plate conditions where this filler is wrong (already_high_acid, delicate, ...)
    notes                    TEXT
);

CREATE TABLE techniques (
    technique_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    name            TEXT NOT NULL UNIQUE,
    is_modifier     INTEGER NOT NULL DEFAULT 0,  -- 1 = prep modifier, 0 = state-changing
    heat_type       TEXT,    -- none | dry | wet | ambient
    moisture_change TEXT,    -- none | lose | gain
    preservation_flag INTEGER NOT NULL DEFAULT 0,
    notes           TEXT
);

CREATE TABLE components (
    component_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    name              TEXT NOT NULL UNIQUE,
    component_kind    TEXT,          -- fresh | cooked | concentrated | preserved | storage
    keeps_well        TEXT,          -- short | medium | long
    freezes_well      INTEGER NOT NULL DEFAULT 0,
    batch_prep_value  TEXT,          -- low | medium | high | very_high
    notes             TEXT
);

CREATE TABLE tags (
    tag_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    family     TEXT NOT NULL,        -- flavour | texture | state
    tag_value  TEXT NOT NULL,
    UNIQUE (family, tag_value)
);

CREATE TABLE roles (
    role_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    role_name   TEXT NOT NULL UNIQUE,
    role_family TEXT                 -- seasoning | structure | richness | lift | balance
);

CREATE TABLE dish_contexts (
    dish_context_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name            TEXT NOT NULL UNIQUE
);

CREATE TABLE evidence_sources (
    source_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    source_type   TEXT,              -- dataset | official | culinary | paper | tool
    title         TEXT,
    license       TEXT,
    citation_text TEXT
);

CREATE TABLE users (
    user_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    name       TEXT
);

-- ---------------------------------------------------------------------------
-- The transformation record
-- ---------------------------------------------------------------------------

CREATE TABLE transformations (
    transformation_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    ingredient_id         INTEGER NOT NULL REFERENCES ingredients(ingredient_id),
    technique_id          INTEGER NOT NULL REFERENCES techniques(technique_id),
    output_component_id   INTEGER NOT NULL REFERENCES components(component_id),
    flavour_shift         TEXT,
    texture_shift         TEXT,
    confidence            TEXT NOT NULL,    -- high | medium_high | medium | low | experimental
    risks                 TEXT,             -- newline-separated caveats (harsh_when_raw, sulfurous_if_overcooked, ...) — a RISK, not a missing role
    notes                 TEXT,
    UNIQUE (ingredient_id, technique_id)
);

CREATE TABLE transformation_tags (
    transformation_id INTEGER NOT NULL REFERENCES transformations(transformation_id),
    tag_id            INTEGER NOT NULL REFERENCES tags(tag_id),
    polarity          TEXT,            -- gain | loss
    evidence_level    TEXT,
    PRIMARY KEY (transformation_id, tag_id)
);

CREATE TABLE transformation_missing_roles (
    transformation_id INTEGER NOT NULL REFERENCES transformations(transformation_id),
    role_id           INTEGER NOT NULL REFERENCES roles(role_id),
    priority          TEXT,            -- high | medium | low
    note              TEXT,
    PRIMARY KEY (transformation_id, role_id)
);

-- ---------------------------------------------------------------------------
-- Pairings: "what should I add next?"
-- ---------------------------------------------------------------------------

CREATE TABLE pairings (
    pairing_id                       INTEGER PRIMARY KEY AUTOINCREMENT,
    ingredient_id                    INTEGER NOT NULL REFERENCES ingredients(ingredient_id),  -- filler
    role_id                          INTEGER NOT NULL REFERENCES roles(role_id),
    works_best_with_transformation_id INTEGER REFERENCES transformations(transformation_id),
    common_context                   TEXT,
    availability_class               TEXT,
    confidence                       TEXT,        -- curated final truth (high/medium/...) — the engine's truth
    curated_role_fit                 TEXT,        -- hand judgement of whether corpus co-occurrence actually supports
                                                   -- THIS role (e.g. "garlic+onion co-occur hugely but garlic fills
                                                   -- aromatic, not acid"). Guardrail against seen_together = good.
    notes                            TEXT,
    -- corpus evidence (populated by `foodprep backfill`); evidence, NOT role-invention
    corpus_cooccurrence_count        INTEGER NOT NULL DEFAULT 0,
    corpus_contexts                  TEXT
);

CREATE TABLE component_uses (
    component_id    INTEGER NOT NULL REFERENCES components(component_id),
    dish_context_id INTEGER NOT NULL REFERENCES dish_contexts(dish_context_id),
    strength        TEXT,            -- primary | secondary
    PRIMARY KEY (component_id, dish_context_id)
);

CREATE TABLE transformation_evidence (
    transformation_id INTEGER NOT NULL REFERENCES transformations(transformation_id),
    source_id         INTEGER NOT NULL REFERENCES evidence_sources(source_id),
    claim_scope       TEXT,
    PRIMARY KEY (transformation_id, source_id)
);

-- ---------------------------------------------------------------------------
-- Ingredient journeys: product-facing paths across existing transformations
-- ---------------------------------------------------------------------------

CREATE TABLE journeys (
    journey_id              INTEGER PRIMARY KEY AUTOINCREMENT,
    slug                    TEXT NOT NULL,
    ingredient_id           INTEGER NOT NULL REFERENCES ingredients(ingredient_id),
    title                   TEXT NOT NULL,
    preparation_id          TEXT NOT NULL, -- controlled by vocabularies.yaml
    primary_transformation_id INTEGER NOT NULL REFERENCES transformations(transformation_id),
    starting_state          TEXT NOT NULL,
    output_state            TEXT NOT NULL,
    why_choose              TEXT NOT NULL,
    sensory_change          TEXT NOT NULL,
    flavour_direction       TEXT NOT NULL,
    useful_additions        TEXT,
    correction              TEXT NOT NULL, -- controlled correction id
    becomes_possible        TEXT NOT NULL,
    risks                   TEXT NOT NULL,
    confidence              TEXT NOT NULL,
    UNIQUE (ingredient_id, slug)
);

CREATE TABLE journey_destinations (
    journey_id    INTEGER NOT NULL REFERENCES journeys(journey_id),
    destination_id TEXT NOT NULL, -- controlled by vocabularies.yaml
    PRIMARY KEY (journey_id, destination_id)
);

CREATE TABLE journey_transitions (
    transition_id INTEGER PRIMARY KEY AUTOINCREMENT,
    journey_id    INTEGER NOT NULL REFERENCES journeys(journey_id),
    sequence_no   INTEGER NOT NULL,
    from_state    TEXT NOT NULL,
    move          TEXT NOT NULL,
    to_state      TEXT NOT NULL,
    reason        TEXT NOT NULL,
    UNIQUE (journey_id, sequence_no)
);

-- ---------------------------------------------------------------------------
-- Destination-aware functional targets
-- ---------------------------------------------------------------------------

CREATE TABLE destination_profiles (
    destination_id TEXT PRIMARY KEY, -- controlled by vocabularies.yaml
    name            TEXT NOT NULL,
    texture_needs   TEXT,
    moisture_needs  TEXT,
    notes           TEXT
);

CREATE TABLE destination_functions (
    destination_id TEXT NOT NULL REFERENCES destination_profiles(destination_id),
    role_id        INTEGER NOT NULL REFERENCES roles(role_id),
    importance     TEXT NOT NULL, -- required | useful | optional | unsuitable
    reason         TEXT NOT NULL,
    PRIMARY KEY (destination_id, role_id)
);

CREATE TABLE flavour_routes (
    route_id         TEXT PRIMARY KEY,
    name             TEXT NOT NULL,
    description      TEXT NOT NULL,
    flavour_dimensions TEXT NOT NULL,
    risks            TEXT NOT NULL,
    cultural_context TEXT,
    confidence       TEXT NOT NULL
);

CREATE TABLE flavour_route_states (
    route_id     TEXT NOT NULL REFERENCES flavour_routes(route_id),
    component_id INTEGER NOT NULL REFERENCES components(component_id),
    fit_reason   TEXT NOT NULL,
    PRIMARY KEY (route_id, component_id)
);

CREATE TABLE flavour_route_destinations (
    route_id       TEXT NOT NULL REFERENCES flavour_routes(route_id),
    destination_id TEXT NOT NULL,
    PRIMARY KEY (route_id, destination_id)
);

CREATE TABLE flavour_route_elements (
    route_id      TEXT NOT NULL REFERENCES flavour_routes(route_id),
    ingredient_id INTEGER NOT NULL REFERENCES ingredients(ingredient_id),
    contribution  TEXT NOT NULL,
    optionality   TEXT NOT NULL, -- required | supporting | finish
    PRIMARY KEY (route_id, ingredient_id)
);

-- Scout generator inputs. These are reusable analogy/substitution rules, not
-- manually authored final candidate pairings.
CREATE TABLE analogy_rules (
    analogy_id            TEXT PRIMARY KEY,
    known_pairing         TEXT NOT NULL,
    source_ingredient_id  INTEGER NOT NULL REFERENCES ingredients(ingredient_id),
    substitute_ingredient_id INTEGER NOT NULL REFERENCES ingredients(ingredient_id),
    mechanism             TEXT NOT NULL,
    shared_function       TEXT NOT NULL,
    meaningful_difference TEXT NOT NULL,
    expected_risk         TEXT NOT NULL,
    required_dimensions   TEXT NOT NULL,
    explanation_template  TEXT NOT NULL,
    confidence            TEXT NOT NULL
);

CREATE TABLE corpora (
    corpus_id      TEXT PRIMARY KEY,
    name           TEXT NOT NULL,
    scope          TEXT NOT NULL,
    source_path    TEXT,
    recipe_count   INTEGER NOT NULL,
    search_date    TEXT NOT NULL
);

CREATE TABLE novelty_observations (
    observation_id       INTEGER PRIMARY KEY AUTOINCREMENT,
    analogy_id           TEXT NOT NULL REFERENCES analogy_rules(analogy_id),
    component_id         INTEGER NOT NULL REFERENCES components(component_id),
    candidate_ingredient_id INTEGER NOT NULL REFERENCES ingredients(ingredient_id),
    corpus_id            TEXT NOT NULL REFERENCES corpora(corpus_id),
    observed_count       INTEGER NOT NULL,
    context_count        INTEGER NOT NULL,
    contexts             TEXT,
    target_covered       INTEGER NOT NULL,
    candidate_covered    INTEGER NOT NULL,
    result_class         TEXT NOT NULL,
    observed_at          TEXT NOT NULL,
    UNIQUE (analogy_id, component_id, corpus_id)
);

CREATE TABLE tasting_protocol_templates (
    analogy_id        TEXT PRIMARY KEY REFERENCES analogy_rules(analogy_id),
    starting_ratio    TEXT NOT NULL,
    smallest_test     TEXT NOT NULL,
    success_condition TEXT NOT NULL,
    likely_failure    TEXT NOT NULL,
    corrections       TEXT NOT NULL,
    safety_note       TEXT NOT NULL
);

CREATE TABLE tasting_trials (
    trial_id               INTEGER PRIMARY KEY AUTOINCREMENT,
    analogy_id             TEXT NOT NULL REFERENCES analogy_rules(analogy_id),
    component_id           INTEGER NOT NULL REFERENCES components(component_id),
    candidate_ingredient_id INTEGER NOT NULL REFERENCES ingredients(ingredient_id),
    tested_at              TEXT NOT NULL,
    preparation            TEXT NOT NULL,
    ratio                  TEXT NOT NULL,
    temperature            TEXT NOT NULL,
    supporting_ingredients TEXT,
    verdict                TEXT NOT NULL,
    observations           TEXT NOT NULL,
    failure_mode           TEXT,
    successful_correction  TEXT,
    safety_confirmed       INTEGER NOT NULL
);

CREATE TABLE pairing_evidence (
    pairing_id  INTEGER NOT NULL REFERENCES pairings(pairing_id),
    source_id   INTEGER NOT NULL REFERENCES evidence_sources(source_id),
    claim_scope TEXT,
    PRIMARY KEY (pairing_id, source_id)
);

CREATE TABLE availability (
    ingredient_id      INTEGER NOT NULL REFERENCES ingredients(ingredient_id),
    region_code        TEXT NOT NULL,           -- e.g. FI
    availability_class TEXT NOT NULL,
    seasonality_note   TEXT,
    PRIMARY KEY (ingredient_id, region_code)
);

CREATE TABLE user_preferences (
    user_id          INTEGER NOT NULL REFERENCES users(user_id),
    vegetarian       INTEGER,
    allergens        TEXT,            -- newline-separated
    avoid_ingredients TEXT,           -- newline-separated canonical names
    max_complexity   TEXT,            -- low | medium | high
    PRIMARY KEY (user_id)
);

-- ---------------------------------------------------------------------------
-- Component profiles: non-transformation plate items (mash, beans, bread, ...)
-- Used by meal-repair logic: union of provides_roles vs a balanced target.
-- This is the table that lets the engine reason about meals, not just tomato.
-- ---------------------------------------------------------------------------

CREATE TABLE component_profiles (
    profile_id        INTEGER PRIMARY KEY AUTOINCREMENT,
    name              TEXT NOT NULL UNIQUE,   -- e.g. mashed_potatoes, chickpea_patty
    aliases           TEXT,                   -- newline-separated
    provides_roles    TEXT,                   -- newline-separated role names present
    flavour_tags      TEXT,                    -- newline-separated
    texture_tags      TEXT,                    -- newline-separated
    missing_risks     TEXT,                    -- newline-separated roles this plate item tends to lack
    heaviness_score   INTEGER,                -- 0-5 subjective richness
    dryness_score     INTEGER,                -- 0-5 subjective dryness
    notes             TEXT
);

-- Sensory/plate profile owned directly by a transformed component. This lets a
-- journey state enter destination reasoning without an independently named
-- shadow row in component_profiles.
CREATE TABLE component_state_profiles (
    component_id      INTEGER PRIMARY KEY REFERENCES components(component_id),
    provides_roles    TEXT,
    flavour_tags      TEXT,
    texture_tags      TEXT,
    missing_risks     TEXT,
    heaviness_score   INTEGER,
    dryness_score     INTEGER,
    notes             TEXT
);

-- ---------------------------------------------------------------------------
-- Query helpers
-- ---------------------------------------------------------------------------

CREATE VIEW v_transformations_full AS
SELECT
    t.transformation_id,
    i.canonical_name   AS ingredient,
    tech.name          AS technique,
    c.name             AS output_component,
    t.flavour_shift,
    t.texture_shift,
    t.confidence
FROM transformations t
JOIN ingredients i  ON i.ingredient_id = t.ingredient_id
JOIN techniques tech ON tech.technique_id = t.technique_id
JOIN components c   ON c.component_id = t.output_component_id;
