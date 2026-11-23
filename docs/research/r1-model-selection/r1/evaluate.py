"""Nested leave-one-ingredient-out evaluation and ranking metrics.

Outer loop: each base ingredient in turn is held out; its prepared states
(pairing) or substitution contexts (Scout) are the test queries. This copies
the real use: adding an ingredient the model has never seen.

Inner loop: hyperparameters are chosen by grouped cross-validation over the
remaining ingredients only (GroupKFold by base ingredient). The held-out
ingredient is never used for tuning.

Scout, strict mode ("new substitution"): training rows whose
(source, candidate) pair is a right answer in the test fold are removed,
positive or negative. The same Scout rule is scoped to several ingredients'
states (brown butter for olive oil fits potato, broccoli, cabbage...), so
without this a learner could pass by memorising the rule from another
ingredient. Strict mode measures whether a model can propose a substitution
nobody has written down yet. "transfer" mode keeps those rows and measures
reuse of known rules on a new ingredient.
"""
from __future__ import annotations

import math

import numpy as np
import pandas as pd
from sklearn.model_selection import GroupKFold

KS = (5, 10)


def query_metrics(scores: np.ndarray, labels: np.ndarray, seed: int) -> dict[str, float]:
    """Binary-relevance ranking metrics for one query. Ties are broken by a
    fixed random order, so a model gains nothing from tied scores."""
    rng = np.random.default_rng(seed)
    order = np.lexsort((rng.random(len(scores)), -scores))
    rel = labels[order]
    n_pos = int(rel.sum())
    out: dict[str, float] = {}
    gains = 1.0 / np.log2(np.arange(2, len(rel) + 2))
    for k in KS:
        dcg = float((rel[:k] * gains[:k]).sum())
        idcg = float(gains[:min(k, n_pos)].sum())
        out[f"ndcg@{k}"] = dcg / idcg if idcg else 0.0
        out[f"recall@{k}"] = float(rel[:k].sum()) / n_pos
    hits = np.flatnonzero(rel)
    out["map"] = float(np.mean([(i + 1) / (r + 1) for i, r in enumerate(hits)]))
    out["mrr"] = 1.0 / (hits[0] + 1)
    out["covered"] = float(len(np.unique(np.round(scores, 12))) > 1)
    return out


def evaluate_queries(df: pd.DataFrame, scores: np.ndarray) -> pd.DataFrame:
    d = df[["query", "fold", "label"]].copy()
    d["score"] = scores
    rows = []
    for q, g in d.groupby("query", sort=False):
        if g["label"].sum() == 0:
            continue
        m = query_metrics(g["score"].to_numpy(), g["label"].to_numpy(),
                          seed=abs(hash(q)) % (2**32))
        rows.append({"query": q, "fold": g["fold"].iloc[0], **m})
    return pd.DataFrame(rows)


def strict_filter(train: pd.DataFrame, test: pd.DataFrame) -> pd.DataFrame:
    if "source" not in test.columns:
        return train
    banned = set(map(tuple, test.loc[test.label == 1, ["source", "candidate"]].to_numpy()))
    keys = list(zip(train["source"], train["candidate"]))
    return train[[k not in banned for k in keys]]


def _fit_score(factory, params, train, test, cols):
    m = factory(**params)
    m.fit(train, cols)
    return m.score(test)


def tune(factory, grid, train, cols, strict, n_inner=3):
    configs = [dict(zip(grid, v)) for v in __import__("itertools").product(*grid.values())] or [{}]
    if len(configs) == 1:
        return configs[0]
    groups = train["fold"].to_numpy()
    k = min(n_inner, len(np.unique(groups)))
    best, best_s = configs[0], -1.0
    for p in configs:
        vals = []
        for tr, te in GroupKFold(n_splits=k).split(train, groups=groups):
            a, b = train.iloc[tr], train.iloc[te]
            if strict:
                a = strict_filter(a, b)
            if b["label"].sum() == 0:
                continue
            s = _fit_score(factory, p, a, b.reset_index(drop=True), cols)
            vals.append(evaluate_queries(b.reset_index(drop=True), s)["ndcg@10"].mean())
        score = float(np.nanmean(vals)) if vals else -1.0
        if score > best_s:
            best, best_s = p, score
    return best


def cross_validate(df: pd.DataFrame, factory, grid, cols, strict=False):
    """Returns (per-query metrics, out-of-fold scores, chosen params per fold)."""
    per_q, oof, chosen = [], np.full(len(df), np.nan), {}
    for fold in sorted(df["fold"].unique()):
        test_mask = (df["fold"] == fold).to_numpy()
        test = df[test_mask].reset_index(drop=True)
        if test["label"].sum() == 0:
            continue
        train = df[~test_mask].reset_index(drop=True)
        if strict:
            train = strict_filter(train, test).reset_index(drop=True)
        params = tune(factory, grid, train, cols, strict)
        chosen[fold] = params
        s = _fit_score(factory, params, train, test, cols)
        oof[np.flatnonzero(test_mask)] = s
        per_q.append(evaluate_queries(test, s))
    return pd.concat(per_q, ignore_index=True), oof, chosen


def summarise(q: pd.DataFrame) -> dict[str, float]:
    by_fold = q.groupby("fold")["ndcg@10"].mean()
    out = {m: q[m].mean() for m in ["ndcg@5", "ndcg@10", "recall@5", "recall@10", "map", "mrr",
                                    "covered"]}
    out["fold_sd"] = by_fold.std()
    out["worst_fold"] = by_fold.min()
    out["worst_fold_name"] = by_fold.idxmin()
    return out


def paired_bootstrap(a: pd.DataFrame, b: pd.DataFrame, metric="ndcg@10", n=4000, seed=0):
    """Mean difference a - b over shared queries, with a 95% interval from a
    bootstrap that resamples whole held-out ingredients (queries of one
    ingredient are not independent)."""
    m = a[["query", "fold", metric]].merge(b[["query", metric]], on="query", suffixes=("_a", "_b"))
    m["d"] = m[f"{metric}_a"] - m[f"{metric}_b"]
    folds = m["fold"].unique()
    per = {f: m.loc[m.fold == f, "d"].to_numpy() for f in folds}
    rng = np.random.default_rng(seed)
    boots = []
    for _ in range(n):
        pick = rng.choice(folds, size=len(folds), replace=True)
        boots.append(np.concatenate([per[f] for f in pick]).mean())
    lo, hi = np.percentile(boots, [2.5, 97.5])
    wins = sum(per[f].mean() > 0 for f in folds)
    return float(m["d"].mean()), float(lo), float(hi), f"{wins}/{len(folds)}"
