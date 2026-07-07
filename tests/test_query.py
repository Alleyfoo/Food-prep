"""End-to-end tests for the tomato transformation engine."""

from foodprep import query


def test_schema_populated(conn):
    assert conn.execute("SELECT count(*) FROM ingredients").fetchone()[0] >= 30
    assert conn.execute("SELECT count(*) FROM transformations").fetchone()[0] == 12
    assert conn.execute("SELECT count(*) FROM roles").fetchone()[0] >= 12
    assert conn.execute("SELECT count(*) FROM pairings").fetchone()[0] >= 30


def test_what_can_i_do_with_tomatoes(conn):
    rows = query.transformations_for_ingredient(conn)
    names = {r["technique"] for r in rows}
    assert {"raw_assemble", "roast", "simmer", "dry", "pickle", "freeze", "can"} <= names
    # high-confidence branches rank first
    assert rows[0]["confidence"] == "high"


def test_roast_now_what(conn):
    tr = query.transformation_by_technique(conn, "roast")
    assert tr is not None
    gaps = query.fillers_by_role(conn, tr["transformation_id"])
    # roasted tomato still needs salt + lift + acid/carb per the ontology
    assert "salt" in gaps
    assert "herb" in gaps
    # fillers are curated for each gap
    assert any(f["filler"] == "sea_salt" for f in gaps["salt"])
    assert any(f["filler"] == "basil" for f in gaps["herb"])


def test_sauce_missing_roles(conn):
    tr = query.transformation_by_technique(conn, "simmer")
    gaps = {g["role_name"] for g in query.missing_roles(conn, tr["transformation_id"])}
    assert {"fat", "aromatic", "carb"} <= gaps


def test_batch_prep(conn):
    rows = query.batch_prep(conn)
    techniques = {r["technique"] for r in rows}
    # sauce, reduce, frozen, canned are the very-high batch-prep winners
    assert {"simmer", "reduce", "freeze", "can"} <= techniques
    assert all(r["batch_prep_value"] in ("high", "very_high") for r in rows)


def test_freezes_well(conn):
    rows = query.freezes_well(conn)
    comps = {r["component"] for r in rows}
    assert "frozen_tomato_base" in comps
    assert "fresh_tomato_component" not in comps


def test_hub_ingredient(conn):
    rows = query.hub_ingredients(conn)
    assert rows, "expected hub ranking"
    # olive oil should be near the top: it appears across many transformations
    top = {r["filler"] for r in rows[:3]}
    assert "olive_oil" in top
    assert rows[0]["transformations_covered"] >= 3


def test_parse_prompt_intents():
    assert query.parse_prompt("what can I do with tomatoes")["intent"] == "branches"
    assert query.parse_prompt("I roasted them now what")["intent"] == "next"
    assert query.parse_prompt("I roasted them now what")["technique"] == "roast"
    assert query.parse_prompt("what can I batch prep")["intent"] == "batch"
    assert query.parse_prompt("what unlocks the most")["intent"] == "hub"


def test_answer_renders(conn):
    out = query.answer(conn, "what can I do with tomatoes")
    assert "roast" in out and "simmer" in out
    out2 = query.answer(conn, "I roasted them now what")
    assert "roasted_tomato_component" in out2
    assert "Still missing" in out2
    out3 = query.answer(conn, "what can I batch prep")
    assert "batch_prep_value" not in out3  # human label, not raw key
    assert "simmer" in out3


def test_evidence_traceability(conn):
    # every transformation has at least one evidence source
    n = conn.execute(
        "SELECT count(*) FROM transformations t "
        "WHERE NOT EXISTS (SELECT 1 FROM transformation_evidence e "
        "WHERE e.transformation_id = t.transformation_id)"
    ).fetchone()[0]
    assert n == 0