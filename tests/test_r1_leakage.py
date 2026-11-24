"""R1 model selection: no feature may read the answers it is scored on.

docs/research/r1-model-selection/ builds candidate tables for two tasks.
These tests change the curated answers and check that every feature column
stays identical: only `label` may move. A fake corpus keeps them independent
of CulinaryDB.
"""
from __future__ import annotations

import dataclasses
import sys
from pathlib import Path

import numpy as np
import pytest

R1 = Path(__file__).resolve().parents[1] / "docs/research/r1-model-selection"
if str(R1) not in sys.path:
    sys.path.insert(0, str(R1))

from r1.data import CorpusStats, load_ontology  # noqa: E402
from r1.evaluate import query_metrics, strict_filter  # noqa: E402
from r1.features import SETS, columns, pairing_table, scout_table  # noqa: E402


@pytest.fixture(scope="module")
def onto():
    return load_ontology()


@pytest.fixture(scope="module")
def fake_corpus(onto):
    names = sorted(onto.ingredients)
    rng = np.random.default_rng(0)
    counts = {n: int(rng.integers(0, 500)) for n in names}
    pair = {(a, b): int(rng.integers(0, 20)) for i, a in enumerate(names) for b in names[i + 1:]}
    vectors = {n: rng.normal(size=8) for n in names}
    return CorpusStats(10000, counts, pair, vectors, set(names), {})


def _features(df):
    cols = sorted(set().union(*[columns(df, f) for f in SETS]))
    return df.sort_values(["query", "candidate"]).reset_index(drop=True)[["query", "candidate", *cols]]


def test_pairing_features_ignore_the_curated_pairings(onto, fake_corpus):
    real = pairing_table(onto, fake_corpus)
    blind = pairing_table(dataclasses.replace(onto, _pairings=[]), fake_corpus)
    assert real["label"].sum() > 200 and blind["label"].sum() == 0
    assert _features(real).equals(_features(blind))


def test_scout_features_ignore_which_substitute_the_rule_names(onto, fake_corpus):
    real = scout_table(onto, fake_corpus)
    names = sorted(onto.ingredients)
    moved = [(s, src, next(n for n in names if n not in (src, sub, onto.states[s].base)))
             for s, src, sub in onto.answers_scout()]
    other = scout_table(dataclasses.replace(onto, _scout=moved), fake_corpus)
    assert not real["label"].equals(other.sort_index()["label"])
    assert _features(real).equals(_features(other))


def test_no_feature_set_uses_the_probe_except_the_probe(onto, fake_corpus):
    df = pairing_table(onto, fake_corpus)
    for f in "ABCD":
        assert not any(c.startswith("L_") for c in columns(df, f)), f
    assert any(c.startswith("L_") for c in columns(df, "L"))


def test_strict_mode_drops_every_training_row_of_a_test_substitution():
    import pandas as pd
    train = pd.DataFrame({"source": ["olive_oil", "olive_oil", "lemon"],
                          "candidate": ["brown_butter", "tahini", "brown_butter"], "label": [1, 0, 0]})
    test = pd.DataFrame({"source": ["olive_oil"], "candidate": ["brown_butter"], "label": [1]})
    kept = strict_filter(train, test)
    assert list(zip(kept.source, kept.candidate)) == [("olive_oil", "tahini"), ("lemon", "brown_butter")]


def test_ties_earn_nothing():
    labels = np.array([1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    flat = np.mean([query_metrics(np.zeros(12), labels, seed)["ndcg@5"] for seed in range(400)])
    best = query_metrics(np.array([1.0] + [0.0] * 11), labels, 0)["ndcg@5"]
    assert best == 1.0 and flat < 0.5
