import sqlite3

from foodprep import corpus, query
from foodprep.cli import build_parser
from foodprep.loader import build
from test_corpus import _write_corpus


def test_observation_records_corpus_scope_and_occurrence(conn, tmp_path):
    _write_corpus(
        tmp_path,
        recipes=[(1, "Broccoli Brown Butter"), (2, "Plain Broccoli"),
                 (3, "Vinegar Dressing")],
        ingredients=[("Broccoli", 100), ("Brown Butter", 101),
                     ("Lingonberry Vinegar", 102)],
        links=[(1, "broccoli", 100), (1, "brown butter", 101),
               (2, "broccoli", 100), (3, "lingonberry vinegar", 102)],
    )

    before = query.generate_scout_hypotheses(conn, "roasted_broccoli_component")
    compatibility = {h["analogy_id"]: h["compatibility_score"] for h in before}
    summary = corpus.observe_hypotheses(
        conn, "roasted_broccoli_component", tmp_path,
        scope="3 synthetic savoury recipes", search_date="2026-07-12",
    )
    after = query.generate_scout_hypotheses(conn, "roasted_broccoli_component")

    # rye_crumbs, tahini, rosemary, horseradish, miso, eggs, anchovy, dill, and other
    # candidates have no entity in the synthetic corpus, so they land honestly in
    # insufficient_coverage, not zero.
    # A three-recipe corpus cannot support a novelty claim: the pairing would
    # not be expected to appear even if everyone cooked it. That is what
    # `underpowered` says, and saying it is the point.
    assert summary == {"observed": 1, "not_observed": 0, "underpowered": 1,
                       "insufficient_coverage": 15}
    by_candidate = {h["candidate"]: h for h in after}
    assert by_candidate["brown_butter"]["novelty"]["class"] == "rare"
    assert by_candidate["brown_butter"]["novelty"]["observed_count"] == 1
    # Underpowered rather than not_observed: with this corpus the absence
    # carries no information (see corpus.MIN_EXPECTED_FOR_ABSENCE).
    assert by_candidate["lingonberry_vinegar"]["novelty"]["class"] == "underpowered"
    assert by_candidate["brown_butter"]["novelty"]["scope"] == "3 synthetic savoury recipes"
    assert {h["analogy_id"]: h["compatibility_score"] for h in after} == compatibility


def test_absent_alias_is_insufficient_coverage_not_zero(tmp_path):
    # Its own database: this measures a deliberately sparse corpus, and the
    # cached real measurements would otherwise answer for it.
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    build(conn, novelty_path=None)
    _write_corpus(
        tmp_path,
        recipes=[(1, "Plain Broccoli")],
        ingredients=[("Broccoli", 100)],
        links=[(1, "broccoli", 100)],
    )

    summary = corpus.observe_hypotheses(
        conn, "roasted_broccoli_component", tmp_path,
        corpus_id="sparse", search_date="2026-07-12",
    )
    hypotheses = query.generate_scout_hypotheses(conn, "roasted_broccoli_component")

    assert summary["insufficient_coverage"] == 17
    assert all(h["novelty"]["class"] == "insufficient_coverage" for h in hypotheses)
    assert all(h["novelty"]["candidate_covered"] is False for h in hypotheses)


def test_novelty_observations_survive_ontology_rebuild(conn, tmp_path):
    _write_corpus(
        tmp_path,
        recipes=[(1, "Broccoli Brown Butter"), (2, "Plain Broccoli"),
                 (3, "Vinegar Dressing")],
        ingredients=[("Broccoli", 100), ("Brown Butter", 101),
                     ("Lingonberry Vinegar", 102)],
        links=[(1, "broccoli", 100), (1, "brown butter", 101),
               (2, "broccoli", 100), (3, "lingonberry vinegar", 102)],
    )
    corpus.observe_hypotheses(
        conn, "roasted_broccoli_component", tmp_path,
        scope="3 synthetic savoury recipes", search_date="2026-07-12",
    )

    build(conn)

    by_candidate = {
        h["candidate"]: h
        for h in query.generate_scout_hypotheses(conn, "roasted_broccoli_component")
    }
    assert by_candidate["brown_butter"]["novelty"]["class"] == "rare"
    assert by_candidate["brown_butter"]["novelty"]["scope"] == "3 synthetic savoury recipes"
    assert by_candidate["brown_butter"]["novelty"]["search_date"] == "2026-07-12"
    # Underpowered rather than not_observed: with this corpus the absence
    # carries no information (see corpus.MIN_EXPECTED_FOR_ABSENCE).
    assert by_candidate["lingonberry_vinegar"]["novelty"]["class"] == "underpowered"
    stored_corpus = conn.execute(
        "SELECT name, recipe_count FROM corpora WHERE corpus_id = 'culinarydb'"
    ).fetchone()
    assert stored_corpus["recipe_count"] == 3


def test_orphaned_novelty_observations_are_dropped_not_restored(tmp_path):
    # Its own database, built without recorded tastings: this test strips the
    # ontology down to nothing, and the loader deliberately refuses to drop a
    # real kitchen result on the floor when its hypothesis disappears.
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    build(conn, tastings_path=None)
    _write_corpus(
        tmp_path,
        recipes=[(1, "Broccoli Brown Butter")],
        ingredients=[("Broccoli", 100), ("Brown Butter", 101)],
        links=[(1, "broccoli", 100), (1, "brown butter", 101)],
    )
    corpus.observe_hypotheses(
        conn, "roasted_broccoli_component", tmp_path, search_date="2026-07-12",
    )
    assert conn.execute(
        "SELECT count(*) FROM novelty_observations"
    ).fetchone()[0] > 0

    # Rebuild without any Scout rules: every observation loses its analogy.
    # Recorded tastings are excluded too — they reference a rule by design,
    # and the loader rightly refuses to drop one silently.
    build(conn, scout_rules_path=tmp_path / "no_scout_rules.yaml",
          tastings_path=None)

    assert conn.execute(
        "SELECT count(*) FROM novelty_observations"
    ).fetchone()[0] == 0
    # Corpus metadata is still kept: it describes the search, not the ontology.
    assert conn.execute(
        "SELECT count(*) FROM corpora WHERE corpus_id = 'culinarydb'"
    ).fetchone()[0] == 1


def test_novelty_thresholds_are_explicit():
    assert corpus.novelty_class(0, False) == "insufficient_coverage"
    assert corpus.novelty_class(0, True) == "not_observed"
    assert corpus.novelty_class(1, True) == "rare"
    assert corpus.novelty_class(2, True) == "uncommon"
    assert corpus.novelty_class(5, True) == "established"
    assert corpus.novelty_class(20, True) == "common"


def test_novelty_resolution_does_not_use_broad_functional_aliases():
    index = {"butter": 1, "vinegar": 2, "brown butter": 3}

    assert corpus.resolve_entities("lingonberry_vinegar", index) == [2]
    assert corpus.resolve_novelty_entities("lingonberry_vinegar", index) == []
    assert corpus.resolve_novelty_entities("brown_butter", index) == [3]


def test_novelty_cli_parser():
    args = build_parser().parse_args([
        "novelty", "roasted_broccoli_component", "C:/corpus",
        "--corpus-id", "test", "--scope", "test recipes",
    ])
    assert args.component == "roasted_broccoli_component"
    assert args.corpus_id == "test"
    assert args.scope == "test recipes"


def test_a_big_enough_corpus_can_still_claim_absence(tmp_path):
    """The power gate must not make novelty unclaimable — only unclaimable
    when the corpus had no real chance of showing the pairing."""
    from foodprep.corpus import MIN_EXPECTED_FOR_ABSENCE, novelty_class
    # plenty of expected co-occurrences, none observed -> a real finding
    assert novelty_class(0, True, expected_count=MIN_EXPECTED_FOR_ABSENCE * 3) == "not_observed"
    # too rare for the absence to mean anything
    assert novelty_class(0, True, expected_count=0.15) == "underpowered"
    # unchanged when nothing is known about the base rate
    assert novelty_class(0, True) == "not_observed"
    assert novelty_class(0, False, expected_count=99) == "insufficient_coverage"
