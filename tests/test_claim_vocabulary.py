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


# ---- when a filler meets the food ------------------------------------------

def test_a_pairing_records_when_the_filler_meets_the_food(conn):
    """The fat you roast in and the confit you dress with are not the same
    kind of claim. Stored in one bucket they looked interchangeable."""
    cols = {r[1] for r in conn.execute("PRAGMA table_info(pairings)")}
    assert "application" in cols


def test_unclassified_pairings_say_so_rather_than_guessing(conn):
    """`unspecified` is honest. Inferring from heat_type is not: you do not
    steam broccoli in butter or boil a potato in it, yet both are heat."""
    values = {r[0] for r in conn.execute("SELECT DISTINCT application FROM pairings")}
    assert values <= {"medium", "dressing", "finish", "unspecified"}
    assert "unspecified" in values, "the honest default should still be in use"


def test_butter_on_steamed_broccoli_is_a_dressing_not_a_medium(conn):
    row = conn.execute(
        """SELECT p.application FROM pairings p
           JOIN ingredients i ON i.ingredient_id = p.ingredient_id
           JOIN transformations t ON t.transformation_id = p.works_best_with_transformation_id
           JOIN techniques tech ON tech.technique_id = t.technique_id
           JOIN ingredients ing ON ing.ingredient_id = t.ingredient_id
           WHERE i.canonical_name = 'butter' AND ing.canonical_name = 'broccoli'
             AND tech.name = 'steam'"""
    ).fetchone()
    assert row and row[0] == "dressing"


def test_a_dressing_outranks_a_cooking_medium(conn):
    """What you dress the finished state with is the dish; what you cooked it
    in usually cannot be tasted, so it must not lead the list."""
    from foodprep import query
    card = next(b for b in query.all_branch_cards(conn, "broccoli")
                if b["technique"] == "roast")
    apps = [f["application"] for f in card["fillers_by_role"]["fat"]]
    assert apps[0] == "dressing"
    assert apps[-1] == "medium"


# ---- the novelty card must say what the corpus actually found --------------

@pytest.mark.parametrize("nclass,expected", [
    ("not_observed", "Not observed"),
    ("rare", "Almost unheard of"),
    ("uncommon", "Uncommon"),
    ("established", "Seen before"),
    ("common", "Seen before"),
    ("insufficient_coverage", "Cannot tell"),
    ("not_checked", "Not checked"),
])
def test_every_corpus_class_gets_its_own_wording(nclass, expected):
    """The card once tested for a class called "novel", which
    corpus.novelty_class() never returns — so a genuinely unobserved pairing
    fell through to the catch-all and rendered as
    "Seen before — 0 co-occurrences"."""
    from foodprep.ui.render import claim_cards_html
    html = claim_cards_html({"candidate_class": "scout_candidate",
                             "novelty": {"class": nclass, "observed_count": 0}})
    assert expected in html


def test_no_class_renders_as_seen_before_with_zero_occurrences():
    """The specific contradiction that slipped through."""
    from foodprep.ui.render import claim_cards_html
    for nclass in ("not_observed", "rare", "uncommon", "established",
                   "common", "insufficient_coverage", "not_checked"):
        html = claim_cards_html({"candidate_class": "scout_candidate",
                                 "novelty": {"class": nclass, "observed_count": 0}})
        assert not ("Seen before" in html and "0 co-occurrences" in html)
