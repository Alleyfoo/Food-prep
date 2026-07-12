import pytest

from foodprep import query, tasting
from foodprep.cli import build_parser


STATE = "roasted_broccoli_component"
CANDIDATE = "lingonberry_vinegar"


def test_generated_hypotheses_include_controlled_protocol(conn):
    hypothesis = next(
        h for h in query.generate_scout_hypotheses(conn, STATE)
        if h["candidate"] == CANDIDATE
    )

    assert hypothesis["protocol"]["starting_ratio"]
    assert "one warm roasted floret" in hypothesis["protocol"]["smallest_test"].lower()
    assert "not preservation guidance" in hypothesis["protocol"]["safety_note"]


def test_protocol_renderer_contains_success_failure_and_safety(conn):
    output = tasting.render_protocol(tasting.protocol(conn, STATE, CANDIDATE))

    assert "Starting ratio:" in output
    assert "Smallest test:" in output
    assert "Success condition:" in output
    assert "Likely failure:" in output
    assert "Corrections:" in output
    assert "Safety:" in output


def test_record_trial_is_append_only_and_complete(conn):
    compatibility_before = {
        h["candidate"]: h["compatibility_score"]
        for h in query.generate_scout_hypotheses(conn, STATE)
    }
    first = tasting.record_trial(
        conn, STATE, CANDIDATE,
        verdict="promising",
        preparation="Roasted floret, vinegar added warm",
        ratio="1 floret : 3 drops",
        temperature="warm",
        supporting_ingredients="sea_salt",
        observations="Acid sharpened the browned edge; fruit was noticeable.",
        failure_mode="Slightly too fruity",
        successful_correction="One extra pinch of salt",
        safety_confirmed=True,
        tested_at="2026-07-12T12:00:00+00:00",
    )
    second = tasting.record_trial(
        conn, STATE, CANDIDATE,
        verdict="works_only_in_this_form",
        preparation="Roasted floret, diluted vinegar",
        ratio="1 floret : 1 drop",
        temperature="room temperature",
        observations="Balanced only at the lower dose.",
        safety_confirmed=True,
        tested_at="2026-07-12T12:30:00+00:00",
    )

    trials = tasting.trials_for_hypothesis(conn, STATE, CANDIDATE)
    assert [trial["trial_id"] for trial in trials] == [first["trial_id"], second["trial_id"]]
    assert first["successful_correction"] == "One extra pinch of salt"
    assert first["safety_confirmed"] is True
    assert {h["candidate"]: h["compatibility_score"]
            for h in query.generate_scout_hypotheses(conn, STATE)} == compatibility_before


def test_trial_requires_safety_confirmation(conn):
    with pytest.raises(tasting.TastingError, match="safety_confirmed"):
        tasting.record_trial(
            conn, STATE, CANDIDATE,
            verdict="inconclusive", preparation="roasted", ratio="one drop",
            temperature="warm", observations="not tested safely",
            safety_confirmed=False,
        )
    assert conn.execute("SELECT count(*) FROM tasting_trials").fetchone()[0] == 0


def test_trial_rejects_unknown_verdict(conn):
    with pytest.raises(tasting.TastingError, match="unknown tasting verdict"):
        tasting.record_trial(
            conn, STATE, CANDIDATE,
            verdict="delicious", preparation="roasted", ratio="one drop",
            temperature="warm", observations="subjective",
            safety_confirmed=True,
        )


def test_trial_rejects_non_generated_candidate(conn):
    with pytest.raises(tasting.TastingError, match="no accepted generated hypothesis"):
        tasting.protocol(conn, STATE, "mustard")


def test_tasting_cli_parsers_require_explicit_fields():
    parser = build_parser()
    protocol_args = parser.parse_args(["protocol", STATE, CANDIDATE])
    record_args = parser.parse_args([
        "record-tasting", STATE, CANDIDATE,
        "--verdict", "promising",
        "--preparation", "roasted",
        "--ratio", "one drop",
        "--temperature", "warm",
        "--observations", "worked",
        "--safety-confirmed",
    ])

    assert protocol_args.candidate == CANDIDATE
    assert record_args.verdict == "promising"
    assert record_args.safety_confirmed is True
