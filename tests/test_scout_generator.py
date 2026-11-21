from foodprep import query
from foodprep.cli import build_parser


def test_roasted_broccoli_generates_analogy_candidates(conn):
    hypotheses = query.generate_scout_hypotheses(
        conn, "roasted_broccoli_component"
    )

    # Only rules whose wording holds for browned brassica pieces. Flavour tags
    # alone used to admit thirteen, including anchovy from the potato-soup
    # rule ("1 cup soup : 1 anchovy fillet") and rosemary from roasted
    # apricots. Rules are now scoped by serving form and ingredient family.
    assert {h["candidate"] for h in hypotheses} == {
        "lingonberry_vinegar", "brown_butter", "rye_crumbs",
        "tahini", "miso", "eggs",
    }
    for hypothesis in hypotheses:
        assert hypothesis["candidate_class"] == "scout_candidate"
        assert hypothesis["compatibility_score"] == 3
        assert hypothesis["compatibility_evidence"]
        assert hypothesis["risk"]
        # Novelty is measured against CulinaryDB and cached in
        # data/novelty.yaml, so it is a real claim now rather than absent.
        # What must hold: it stays SEPARATE from compatibility, and absence
        # is never claimed for a pairing the corpus cannot see.
        novelty = hypothesis["novelty"]
        assert novelty["class"] in {
            "not_observed", "rare", "uncommon", "established", "common",
            "insufficient_coverage", "underpowered",
        }
        if novelty["class"] == "not_observed":
            assert novelty["target_covered"] and novelty["candidate_covered"]


def test_candidate_is_generated_not_stored_as_final_pairing(conn):
    hypothesis = next(
        h for h in query.generate_scout_hypotheses(
            conn, "roasted_broccoli_component"
        )
        if h["candidate"] == "lingonberry_vinegar"
    )

    assert hypothesis["analogy_id"] == "tart_fruit_for_citrus_on_browned_vegetable"
    assert hypothesis["source"] == "lemon"
    assert "analogue substitution" in hypothesis["compatibility_evidence"][1]
    assert "lingonberry vinegar" in hypothesis["explanation"].lower()


def test_rarity_alone_cannot_create_candidate():
    assert query.classify_scout_candidate([], "not_observed") == "rejected"
    assert query.classify_scout_candidate([], "rare") == "rejected"
    assert query.classify_scout_candidate(["state fit"], "common") == "weak_hypothesis"


def test_rejected_rules_keep_reasons(conn):
    hypotheses = query.generate_scout_hypotheses(
        conn, "steamed_broccoli_component", include_rejected=True
    )
    rejected = [h for h in hypotheses if h["candidate_class"] == "rejected"]

    assert rejected
    assert all(h["rejection_reason"].startswith(("State lacks", "Rule does not apply"))
               for h in rejected)
    assert all(h["compatibility_score"] == 0 for h in rejected)


def test_generated_output_keeps_novelty_honest(conn):
    output = query.render_generated_hypotheses(
        conn, "roasted_broccoli_component"
    )

    assert "Generated Scout hypotheses" in output
    assert "compatibility separate from novelty" in output
    # The corpus has been run, so the output carries a real novelty line.
    # The claim that matters is that it is reported apart from compatibility.
    assert "novelty:" in output
    assert "risk:" in output


def test_hypotheses_cli_parser():
    args = build_parser().parse_args(
        ["hypotheses", "roasted_broccoli_component"]
    )

    assert args.component == "roasted_broccoli_component"
