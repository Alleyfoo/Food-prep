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


def test_butter_states_are_states_not_separate_ingredients(fresh):
    """Brown butter and ghee are things butter becomes, not things you buy.

    Both act on the milk proteins — browning cooks them, clarifying removes
    them — so they are opposite moves on one ingredient. Modelling them as
    unrelated ingredients was the same category error the whole project
    exists to avoid: it is why broccoli has states and butter did not.
    """
    techniques = {r[0] for r in fresh.execute(
        """SELECT tech.name FROM transformations t
           JOIN techniques tech ON tech.technique_id = t.technique_id
           JOIN ingredients i ON i.ingredient_id = t.ingredient_id
           WHERE i.canonical_name = 'butter'""")}
    assert techniques == {"brown", "clarify"}

    for component in ("brown_butter_component", "ghee_component"):
        row = fresh.execute(
            "SELECT component_id FROM components WHERE name = ?", (component,)
        ).fetchone()
        assert row, f"{component} is not a modelled state"


def test_ghee_keeps_longer_than_brown_butter(fresh):
    """Because the part that spoils — the milk proteins — has been removed."""
    keeps = dict(fresh.execute(
        "SELECT name, keeps_well FROM components "
        "WHERE name IN ('brown_butter_component', 'ghee_component')"))
    assert keeps["ghee_component"] == "long"
    assert keeps["brown_butter_component"] == "medium"


def test_the_users_garlic_fat_is_confit_not_garlic_butter(fresh):
    """It is cloves slow-roasted in ghee, which cannot brown — a different
    food from butter creamed with garlic, and the trial compared against it."""
    row = fresh.execute(
        "SELECT notes, aliases FROM ingredients WHERE canonical_name = 'garlic_confit'"
    ).fetchone()
    assert row, "garlic_confit is missing"
    assert "ghee" in row["notes"]
    # the old name still resolves, so nothing that referenced it is orphaned
    assert "garlic butter" in row["aliases"]
    assert not fresh.execute(
        "SELECT 1 FROM ingredients WHERE canonical_name = 'garlic_butter'").fetchone()


# ---- cached corpus measurements --------------------------------------------

def test_novelty_survives_a_build_with_no_corpus_present(fresh):
    """The corpus is ~46k recipes that do not ship with the app. Without the
    cache every hypothesis would read 'novelty not checked'."""
    n = fresh.execute("SELECT count(*) FROM novelty_observations").fetchone()[0]
    assert n > 0
    corpus_row = fresh.execute("SELECT name, recipe_count FROM corpora").fetchone()
    assert corpus_row["recipe_count"] > 1000, "provenance must travel with the claim"


def test_absence_is_the_claim_worth_trusting(fresh):
    """A zero, for two ingredients the corpus knows, is a real finding."""
    rows = fresh.execute(
        """SELECT target_covered, candidate_covered FROM novelty_observations
           WHERE result_class = 'not_observed'""").fetchall()
    assert rows, "expected some genuinely unobserved pairings"
    for r in rows:
        assert r["target_covered"] and r["candidate_covered"], (
            "'not observed' must never be claimed for something the corpus "
            "cannot see — that is what insufficient_coverage is for")


def test_unresolvable_pairings_make_no_claim(fresh):
    rows = fresh.execute(
        """SELECT observed_count FROM novelty_observations
           WHERE result_class = 'insufficient_coverage'""").fetchall()
    assert rows, "over half of ours do not resolve; that should be visible"


def test_absence_is_only_claimed_where_the_corpus_could_have_shown_it(fresh):
    """Two rare ingredients failing to meet is not a discovery.

    miso is in 0.23% of recipes and rutabaga in 0.14%, so 45k recipes expect
    them to co-occur 0.15 times. Finding none is exactly what chance predicts.
    Ten of the original eleven "not observed" findings were this.
    """
    from foodprep.corpus import MIN_EXPECTED_FOR_ABSENCE
    assert MIN_EXPECTED_FOR_ABSENCE >= 1
    classes = {r[0] for r in fresh.execute(
        "SELECT DISTINCT result_class FROM novelty_observations")}
    assert "underpowered" in classes, (
        "rare-versus-rare pairings must be separated from real absences")


def test_underpowered_is_not_reported_as_novel(fresh):
    from foodprep.ui.render import claim_cards_html
    html = claim_cards_html({"candidate_class": "scout_candidate",
                             "novelty": {"class": "underpowered",
                                         "observed_count": 0}})
    assert "Too rare to tell" in html
    assert "Not observed" not in html
