"""Tests for the CulinaryDB corpus backfill (evidence, not truth).

Uses a tiny synthetic corpus so the test is self-contained and does not depend
on the F:\\download\\google\\CulinaryDB dataset being present.
"""

import csv
import sqlite3

import pytest

from foodprep.loader import build
from foodprep import corpus


@pytest.fixture()
def conn():
    c = sqlite3.connect(":memory:")
    c.row_factory = sqlite3.Row
    build(c)
    yield c
    c.close()


def _write_corpus(tmp_path, recipes, ingredients, links):
    """Write the three CSVs CulinaryDB-style."""
    with open(tmp_path / "01_Recipe_Details.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["Recipe ID", "Title", "Source", "Cuisine"])
        for rid, title in recipes:
            w.writerow([rid, title, "test", "test"])
    with open(tmp_path / "02_Ingredients.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["Aliased Ingredient Name", "Ingredient Synonyms", "Entity ID", "Category"])
        for name, eid in ingredients:
            w.writerow([name, name.lower(), eid, "misc"])
    with open(tmp_path / "04_Recipe-Ingredients_Aliases.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["Recipe ID", "Original Ingredient Name", "Aliased Ingredient Name", "Entity ID"])
        for rid, name, eid in links:
            w.writerow([rid, name, name, eid])


def test_backfill_populates_counts_and_contexts(conn, tmp_path):
    """garlic + tomato co-occur in 3 recipes -> count 3, contexts from titles."""
    _write_corpus(
        tmp_path,
        recipes=[(1, "Garlic Tomato Pasta"), (2, "Tomato Garlic Soup"),
                 (3, "Salsa With Garlic"), (4, "Plain Rice")],
        ingredients=[("Tomato", 100), ("Garlic", 101), ("Rice", 102)],
        links=[(1, "tomato", 100), (1, "garlic", 101),
               (2, "tomato", 100), (2, "garlic", 101),
               (3, "tomato", 100), (3, "garlic", 101),
               (4, "rice", 102)],
    )
    summary = corpus.backfill(conn, tmp_path)
    assert summary["updated"] >= 1
    row = conn.execute(
        """
        SELECT p.corpus_cooccurrence_count, p.corpus_contexts, p.confidence
        FROM pairings p
        JOIN ingredients i ON i.ingredient_id = p.ingredient_id
        LEFT JOIN transformations t ON t.transformation_id = p.works_best_with_transformation_id
        LEFT JOIN ingredients ti ON ti.ingredient_id = t.ingredient_id
        WHERE i.canonical_name = 'garlic' AND ti.canonical_name = 'tomato'
        ORDER BY p.corpus_cooccurrence_count DESC LIMIT 1
        """
    ).fetchone()
    assert row is not None
    assert row["corpus_cooccurrence_count"] == 3
    assert row["corpus_contexts"] is not None
    assert "Garlic Tomato Pasta" in row["corpus_contexts"]
    # confidence is curated truth — backfill must not touch it
    assert row["confidence"] in ("high", "medium", "medium_high", "low", "experimental")


def test_backfill_leaves_confidence_untouched(conn, tmp_path):
    """Counts change, curated confidence does not."""
    before = {r[0]: r[1] for r in conn.execute(
        "SELECT pairing_id, confidence FROM pairings").fetchall()}
    _write_corpus(
        tmp_path, recipes=[(1, "Tomato Garlic")],
        ingredients=[("Tomato", 100), ("Garlic", 101)],
        links=[(1, "tomato", 100), (1, "garlic", 101)],
    )
    corpus.backfill(conn, tmp_path)
    after = {r[0]: r[1] for r in conn.execute(
        "SELECT pairing_id, confidence FROM pairings").fetchall()}
    assert before == after


def test_resolve_entities_fallback():
    """A canonical name not in the override map resolves via normalised lookup;
    an absent name returns [] (honest, not an error)."""
    idx = {"tomato": 100, "garlic": 101}
    assert corpus.resolve_entities("tomato", idx) == [100]
    assert corpus.resolve_entities("olive_oil", idx) == []


def test_backfill_corpus_columns_default_zero(conn):
    """Before any backfill, corpus columns are honest zeros/nulls."""
    row = conn.execute(
        "SELECT count(*) AS n FROM pairings WHERE corpus_cooccurrence_count != 0"
    ).fetchone()
    assert row["n"] == 0