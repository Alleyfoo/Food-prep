from foodprep import query
from foodprep.cli import build_parser


def test_roasted_broccoli_generates_analogy_candidates(conn):
    hypotheses = query.generate_scout_hypotheses(
        conn, "roasted_broccoli_component"
    )

    # rye_crumbs joined via the toasted-grain reinforcement rule: roasted
    # broccoli carries both of its required dimensions (sweet, nutty_toasted).
    # tahini, rosemary, horseradish, and miso joined via new rules that also match
    # the sweet + nutty_toasted dimensions.
    # eggs, anchovy, and dill joined via potato rules that match umami + sweet or
    # nutty_toasted + sweet dimensions (Scout rules are generic, not ingredient-specific).
    # smoked_salt, chili_crisp, and pomegranate_molasses joined via tomato rules that
    # match sweet + nutty_toasted + umami dimensions.
    assert {h["candidate"] for h in hypotheses} == {
        "lingonberry_vinegar", "brown_butter", "rye_crumbs",
        "tahini", "rosemary", "horseradish", "miso",
        "eggs", "anchovy", "dill",
        "smoked_salt", "chili_crisp", "pomegranate_molasses"
    }
    for hypothesis in hypotheses:
        assert hypothesis["candidate_class"] == "scout_candidate"
        assert hypothesis["compatibility_score"] == 3
        assert hypothesis["compatibility_evidence"]
        assert hypothesis["risk"]
        assert hypothesis["novelty"] == {"class": "not_checked", "scope": None}


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
    assert "lingonberry_vinegar" in hypothesis["explanation"]


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
    assert all(h["rejection_reason"].startswith("State lacks") for h in rejected)
    assert all(h["compatibility_score"] == 0 for h in rejected)


def test_generated_output_keeps_novelty_honest(conn):
    output = query.render_generated_hypotheses(
        conn, "roasted_broccoli_component"
    )

    assert "Generated Scout hypotheses" in output
    assert "compatibility separate from novelty" in output
    assert "novelty: not checked — no corpus claim yet" in output
    assert "risk:" in output


def test_hypotheses_cli_parser():
    args = build_parser().parse_args(
        ["hypotheses", "roasted_broccoli_component"]
    )

    assert args.component == "roasted_broccoli_component"
