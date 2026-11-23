"""R1: statistical and machine-learning model selection. Reruns the study.

    py -3.11 docs/research/r1-model-selection/run.py [--quick]

Needs the CulinaryDB corpus (foodprep.corpus.resolve_corpus_dir). Writes
results/ next to this file: per-model summaries, per-query metrics, the
paired comparisons and the novel-candidate review sheets.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE.parents[2] / "src"), str(HERE)]

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

from r1.data import corpus_stats, load_ontology  # noqa: E402
from r1.evaluate import cross_validate, paired_bootstrap, summarise  # noqa: E402
from r1.features import columns, pairing_table, scout_table  # noqa: E402
from r1.models import LGBMClf, LGBMRank, LogReg, pairing_models, scout_models  # noqa: E402

OUT = HERE / "results"


def run_task(name, df, models, strict, quick):
    rows, perq, oofs = [], {}, {}
    for mname, factory, grid, sets in models:
        for fs in sets:
            if quick and mname not in ("Popularity", "Hybrid statistical", "Logistic regression",
                                       "LightGBM LambdaRank"):
                continue
            t = time.time()
            q, oof, chosen = cross_validate(df, factory, grid, columns(df, fs), strict=strict)
            key = f"{mname} [{fs}]"
            s = summarise(q)
            rows.append({"task": name, "model": mname, "features": fs, **s,
                         "seconds": round(time.time() - t, 1),
                         "params": json.dumps(chosen, default=str)})
            perq[key], oofs[key] = q.assign(model=key), oof
            print(f"{name:14} {key:46} ndcg@10 {s['ndcg@10']:.3f}  worst {s['worst_fold']:.3f}"
                  f"  ({rows[-1]['seconds']}s)", flush=True)
    return pd.DataFrame(rows), perq, oofs


def leakage_probe(name, df, strict):
    rows = []
    for mname, cls in (("Logistic regression", LogReg), ("LightGBM classifier", LGBMClf),
                       ("LightGBM LambdaRank", LGBMRank)):
        for fs in ("D", "L"):
            q, _oof, _c = cross_validate(df, cls, cls.grid, columns(df, fs), strict=strict)
            rows.append({"task": name, "model": mname, "features": fs, **summarise(q)})
            print(f"probe {name:8} {mname:22} [{fs}] ndcg@10 {rows[-1]['ndcg@10']:.3f}", flush=True)
    return pd.DataFrame(rows)


def comparisons(summary, perq):
    """Each model against the best non-learned model of the same task."""
    out = []
    stat = summary[summary.model.isin(STATISTICAL)]
    ref = stat.sort_values("ndcg@10", ascending=False).iloc[0]
    ref_key = f"{ref.model} [{ref.features}]"
    for _, r in summary.iterrows():
        key = f"{r.model} [{r.features}]"
        if key == ref_key:
            continue
        d, lo, hi, wins = paired_bootstrap(perq[key], perq[ref_key])
        out.append({"model": key, "vs": ref_key, "diff_ndcg@10": d, "ci_low": lo, "ci_high": hi,
                    "folds_better": wins})
    return pd.DataFrame(out).sort_values("diff_ndcg@10", ascending=False)


STATISTICAL = {"Popularity", "Curated frequency", "Co-occurrence", "Smoothed lift / PPMI", "SVD embeddings",
               "Flavour compatibility", "Hybrid statistical", "Bayesian scoring",
               "K-nearest neighbours (states)", "Co-occurrence with the state",
               "Smoothed lift / PPMI with the state", "Rarely with the source (-PPMI)",
               "SVD cosine to the source", "Functional similarity", "Context nearest neighbour"}


def novel_sheet(df, oof, k=5):
    d = df[["query", "fold", "candidate", "label"]].copy()
    d["score"] = oof
    d = d.dropna(subset=["score"])
    rows = []
    for q, g in d.groupby("query"):
        if g.label.sum() == 0:
            continue
        g = g.sort_values("score", ascending=False)
        for rank, (_, r) in enumerate(g.iterrows(), 1):
            if r.label == 0 and len([x for x in rows if x["query"] == q]) < k:
                rows.append({"query": q, "held_out": r.fold, "rank": rank, "candidate": r.candidate,
                             "verdict": "", "note": ""})
    return pd.DataFrame(rows)


def main():
    quick = "--quick" in sys.argv
    OUT.mkdir(exist_ok=True)
    o = load_ontology()
    cs = corpus_stats(sorted(o.ingredients))
    P, S = pairing_table(o, cs), scout_table(o, cs)
    meta = {"pairing_rows": len(P), "pairing_queries": int(P["query"].nunique()),
            "pairing_positives": int(P.label.sum()), "scout_rows": len(S),
            "scout_queries": int(S["query"].nunique()), "scout_positives": int(S.label.sum()),
            "ingredients_without_vector": sorted(set(o.ingredients) - set(cs.vectors)),
            "corpus_recipes": cs.n_recipes,
            "feature_counts": {t: {f: len(columns(d, f)) for f in "ABCDL"}
                               for t, d in (("pairing", P), ("scout", S))}}
    (OUT / "meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")

    tasks = [("pairing", P, pairing_models(), False),
             ("scout_strict", S, scout_models(), True),
             ("scout_transfer", S, scout_models(), False)]
    all_rows = []
    for name, df, models, strict in tasks:
        summary, perq, oofs = run_task(name, df, models, strict, quick)
        all_rows.append(summary)
        pd.concat(perq.values()).to_csv(OUT / f"{name}_per_query.csv", index=False)
        comparisons(summary, perq).to_csv(OUT / f"{name}_vs_best_statistical.csv", index=False)
        best = summary.sort_values("ndcg@10", ascending=False).iloc[0]
        stat = summary[summary.model.isin(STATISTICAL)].sort_values("ndcg@10", ascending=False).iloc[0]
        for tag, r in (("best", best), ("best_statistical", stat)):
            key = f"{r.model} [{r.features}]"
            novel_sheet(df, oofs[key]).assign(model=key).to_csv(
                OUT / f"{name}_novel_review_{tag}.csv", index=False)
    pd.concat(all_rows).to_csv(OUT / "summary.csv", index=False)
    if not quick:
        pd.concat([leakage_probe("pairing", P, False), leakage_probe("scout_strict", S, True)]
                  ).to_csv(OUT / "leakage_probe.csv", index=False)


if __name__ == "__main__":
    main()
