from foodprep import corpus, query
from foodprep.cli import build_parser
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

    assert summary == {"observed": 1, "not_observed": 1, "insufficient_coverage": 0}
    by_candidate = {h["candidate"]: h for h in after}
    assert by_candidate["brown_butter"]["novelty"]["class"] == "rare"
    assert by_candidate["brown_butter"]["novelty"]["observed_count"] == 1
    assert by_candidate["lingonberry_vinegar"]["novelty"]["class"] == "not_observed"
    assert by_candidate["brown_butter"]["novelty"]["scope"] == "3 synthetic savoury recipes"
    assert {h["analogy_id"]: h["compatibility_score"] for h in after} == compatibility


def test_absent_alias_is_insufficient_coverage_not_zero(conn, tmp_path):
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

    assert summary["insufficient_coverage"] == 2
    assert all(h["novelty"]["class"] == "insufficient_coverage" for h in hypotheses)
    assert all(h["novelty"]["candidate_covered"] is False for h in hypotheses)


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
