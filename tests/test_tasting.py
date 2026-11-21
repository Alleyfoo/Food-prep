import pytest

from foodprep import query, tasting
from foodprep.cli import build_parser
from foodprep.loader import build


STATE = "roasted_broccoli_component"
CANDIDATE = "lingonberry_vinegar"


def test_generated_hypotheses_include_controlled_protocol(conn):
    hypothesis = next(
        h for h in query.generate_scout_hypotheses(conn, STATE)
        if h["candidate"] == CANDIDATE
    )

    assert hypothesis["protocol"]["starting_ratio"]
    # The rule now travels across browned brassicas and roots, so its test
    # says "one warm piece" rather than naming a floret.
    assert "one warm piece" in hypothesis["protocol"]["smallest_test"].lower()
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
    before = conn.execute("SELECT count(*) FROM tasting_trials").fetchone()[0]
    with pytest.raises(tasting.TastingError, match="safety_confirmed"):
        tasting.record_trial(
            conn, STATE, CANDIDATE,
            verdict="inconclusive", preparation="roasted", ratio="one drop",
            temperature="warm", observations="not tested safely",
            safety_confirmed=False,
        )
    # The table is not empty any more — data/tastings.yaml seeds the real
    # recorded trials — so assert the failed attempt added nothing.
    assert conn.execute(
        "SELECT count(*) FROM tasting_trials").fetchone()[0] == before


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


def test_scout_output_shows_read_only_trial_history(conn):
    tasting.record_trial(
        conn, STATE, CANDIDATE,
        verdict="promising",
        preparation="Roasted floret, vinegar added warm",
        ratio="1 floret : 3 drops", temperature="warm",
        observations="Acid sharpened the browned edge.",
        failure_mode="Slightly too fruity",
        successful_correction="One extra pinch of salt",
        safety_confirmed=True, tested_at="2026-07-12T12:00:00+00:00",
    )

    hypotheses = {h["candidate"]: h
                  for h in query.generate_scout_hypotheses(conn, STATE)}
    output = query.render_generated_hypotheses(conn, STATE)

    tested = hypotheses[CANDIDATE]["trials"]
    assert [t["verdict"] for t in tested] == ["promising"]
    # brown_butter now carries a real recorded trial, so an untested
    # candidate is the one that must show an empty history.
    untested = next(name for name, h in hypotheses.items() if name != "brown_butter"
                    and not h["trials"])
    assert hypotheses[untested]["trials"] == []
    assert "trials: 1 recorded" in output
    assert "[2026-07-12] promising — 1 floret : 3 drops, warm: " \
           "Acid sharpened the browned edge." in output
    assert "correction: One extra pinch of salt" in output
    assert "trials: none recorded" in output  # the untested candidates


def test_trials_survive_ontology_rebuild(conn):
    recorded = tasting.record_trial(
        conn, STATE, CANDIDATE,
        verdict="promising", preparation="roasted floret",
        ratio="1 floret : 2 drops", temperature="warm",
        observations="Worth another test.", safety_confirmed=True,
        tested_at="2026-07-12T13:00:00+00:00",
    )

    build(conn)

    restored = tasting.trial(conn, recorded["trial_id"])
    assert restored["verdict"] == "promising"
    assert restored["observations"] == "Worth another test."
    assert restored["state"] == STATE
    assert restored["candidate"] == CANDIDATE


# ---- the durable record: tastings.yaml, appended, never rewritten ----------

def _copy_of_tastings(tmp_path):
    import shutil
    from foodprep.loader import TASTINGS_PATH
    copy = tmp_path / "tastings.yaml"
    shutil.copy(TASTINGS_PATH, copy)
    return copy


def _record(conn, path, **overrides):
    fields = dict(verdict="promising", preparation="one warm piece",
                  ratio="3 drops", temperature="warm",
                  observations="sharp: 'bright' # still text",
                  safety_confirmed=True, yaml_path=path)
    fields.update(overrides)
    return tasting.record_trial(conn, STATE, CANDIDATE, **fields)


def test_yaml_append_keeps_every_existing_byte(conn, tmp_path):
    path = _copy_of_tastings(tmp_path)
    before = path.read_bytes()
    _record(conn, path)
    after = path.read_bytes()
    assert after.startswith(before) and len(after) > len(before)


def test_yaml_append_round_trips_through_a_rebuild(conn, tmp_path):
    import sqlite3
    path = _copy_of_tastings(tmp_path)
    trial = _record(conn, path)
    rebuilt = sqlite3.connect(":memory:")
    rebuilt.row_factory = sqlite3.Row
    build(rebuilt, tastings_path=path)
    obs = [r[0] for r in rebuilt.execute(
        "SELECT observations FROM tasting_trials WHERE tested_at = ?",
        (trial["tested_at"],))]
    assert obs == ["sharp: 'bright' # still text"]


def test_duplicate_trial_is_refused_and_nothing_is_written(conn, tmp_path):
    path = _copy_of_tastings(tmp_path)
    first = _record(conn, path, tested_at="2026-11-21")
    size = path.stat().st_size
    with pytest.raises(tasting.TastingError, match="already recorded"):
        _record(conn, path, tested_at=first["tested_at"])
    assert path.stat().st_size == size


def test_invalid_trial_writes_nothing(conn, tmp_path):
    path = _copy_of_tastings(tmp_path)
    before = path.read_bytes()
    with pytest.raises(tasting.TastingError):
        _record(conn, path, safety_confirmed=False)
    assert path.read_bytes() == before


def test_cli_records_into_tastings_yaml_by_default(conn, tmp_path, monkeypatch):
    from foodprep import cli
    path = _copy_of_tastings(tmp_path)
    db = tmp_path / "fp.sqlite"
    monkeypatch.setenv(tasting.TASTINGS_ENV, str(path))
    assert cli.main(["--db", str(db), "build"]) == 0
    before = path.read_bytes()
    args = ["--db", str(db), "record-tasting", STATE, CANDIDATE,
            "--verdict", "works", "--preparation", "p", "--ratio", "r",
            "--temperature", "t", "--observations", "o", "--safety-confirmed"]
    assert cli.main(args) == 0
    assert len(path.read_bytes()) > len(before)
    grown = path.read_bytes()
    assert cli.main(args + ["--db-only"]) == 0
    assert path.read_bytes() == grown


def test_build_reads_the_file_the_app_appends_to(tmp_path, monkeypatch):
    import sqlite3
    path = _copy_of_tastings(tmp_path)
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    build(conn)
    _record(conn, path, tested_at="2026-11-22")
    monkeypatch.setenv(tasting.TASTINGS_ENV, str(path))
    fresh = sqlite3.connect(":memory:")
    fresh.row_factory = sqlite3.Row
    build(fresh)                      # default path -> follows the override
    dates = {r[0] for r in fresh.execute("SELECT tested_at FROM tasting_trials")}
    assert "2026-11-22" in dates
