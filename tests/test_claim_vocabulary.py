"""Three different claims must not share one word.

`confidence` used to sit on routes, analogy rules and pairings alike, on the
same high/medium/low scale — but it meant something different each time:

  * a pairing's  confidence        — how sure we are people cook this
  * a route's    attestation       — how well attested the STRUCTURE is
  * an analogy's inference_strength — how sound the SUBSTITUTION reasoning is

None of them claims the food will taste good; only a recorded tasting can do
that. Collapsing them back into one word is how "compatible" quietly starts
reading as "good", so the separation is pinned here.
"""

import pytest

from foodprep import query
from foodprep.ui.render import conf_pill


def _columns(conn, table):
    return {r[1] for r in conn.execute(f"PRAGMA table_info({table})")}


def test_a_route_claims_attestation_not_confidence(conn):
    cols = _columns(conn, "flavour_routes")
    assert "attestation" in cols
    assert "confidence" not in cols, (
        "a route claims its structure is attested, not that the food is good")


def test_an_analogy_claims_inference_strength(conn):
    cols = _columns(conn, "analogy_rules")
    assert "inference_strength" in cols
    assert "confidence" not in cols, (
        "an analogy rule claims its reasoning is sound, not that the result is")


def test_pairings_keep_confidence(conn):
    # Pairings are the one place the plain word still fits.
    assert "confidence" in _columns(conn, "pairings")


def test_every_route_carries_an_attestation(conn):
    rows = conn.execute("SELECT name, attestation FROM flavour_routes").fetchall()
    assert rows
    for row in rows:
        assert row["attestation"], f"{row['name']} has no attestation"


def test_routes_reach_the_ui_as_attestation(conn):
    routes = query.flavour_routes_for_component(conn, "massaged_kale_component")
    assert routes
    for r in routes:
        assert r.get("attestation")
        assert "confidence" not in r


def test_hypotheses_carry_inference_strength(conn):
    hyps = query.generate_scout_hypotheses(conn, "roasted_broccoli_component")
    assert hyps
    for h in hyps:
        assert h.get("inference_strength")


@pytest.mark.parametrize("claim,expected", [
    ("attested", "attested high"),
    ("", "high"),
])
def test_the_pill_names_the_claim(claim, expected):
    # "high" on its own reads as "this tastes good"; the word prevents that.
    assert expected in conf_pill("high", claim)
