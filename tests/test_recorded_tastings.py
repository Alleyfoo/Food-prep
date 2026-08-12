"""Recorded tastings must be durable.

A trial is the only thing in this system that can say food was good — it is
someone's actual kitchen result, and it cannot be regenerated. Trials used to
live only in the gitignored database, so the app (which builds in memory from
YAML) never showed them and a fresh clone lost them. They now load from
`data/tastings.yaml` like every other fact.
"""

import sqlite3

import pytest

from foodprep import query
from foodprep.loader import build


@pytest.fixture
def fresh():
    """A database built from scratch — the fresh-clone case."""
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    build(conn)
    return conn


def test_a_recorded_tasting_survives_a_fresh_build(fresh):
    n = fresh.execute("SELECT count(*) FROM tasting_trials").fetchone()[0]
    assert n >= 1, "tastings.yaml did not reach the database"


def test_rebuilding_does_not_duplicate_a_trial(fresh):
    before = fresh.execute("SELECT count(*) FROM tasting_trials").fetchone()[0]
    build(fresh)
    after = fresh.execute("SELECT count(*) FROM tasting_trials").fetchone()[0]
    assert after == before, "a rebuild duplicated the recorded trials"


def test_the_brown_butter_trial_reaches_its_hypothesis(fresh):
    hyps = query.generate_scout_hypotheses(fresh, "roasted_broccoli_component")
    brown = next(h for h in hyps if h["candidate"] == "brown_butter")
    assert brown["trials"], "the trial did not attach to its hypothesis"
    trial = brown["trials"][0]
    assert trial["verdict"] == "works"
    assert "garlic butter" in trial["observations"].lower()


def test_a_trial_records_what_was_not_measured(fresh):
    """Unmeasured is a legitimate value; inventing a ratio is not."""
    row = fresh.execute(
        "SELECT ratio, temperature, preparation FROM tasting_trials LIMIT 1"
    ).fetchone()
    assert row["ratio"], "ratio may be 'not measured' but never empty"
    assert row["temperature"]
    assert row["preparation"]


def test_every_trial_points_at_a_live_hypothesis(fresh):
    """A trial tests a Scout hypothesis — that is what makes it a trial."""
    orphans = fresh.execute(
        """SELECT tt.trial_id FROM tasting_trials tt
           LEFT JOIN analogy_rules ar ON ar.analogy_id = tt.analogy_id
           WHERE ar.analogy_id IS NULL"""
    ).fetchall()
    assert not orphans, "a trial references an analogy rule that no longer exists"
