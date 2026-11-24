"""The R1 models: statistical scorers, knowledge-based scorers and learners.

Every model has the same interface:
    m = Model(**params); m.fit(train_df, cols); scores = m.score(test_df)
`grid` lists the hyperparameters tuned inside the training folds only.
Scorers that take no parameters have an empty grid and ignore `fit`.
"""
from __future__ import annotations

import itertools
import warnings

import numpy as np
import pandas as pd
from sklearn.ensemble import ExtraTreesClassifier, HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

import lightgbm as lgb

warnings.filterwarnings("ignore", category=UserWarning)


def _z(x: pd.Series | np.ndarray) -> np.ndarray:
    x = np.asarray(x, dtype=float)
    sd = x.std()
    return (x - x.mean()) / sd if sd > 0 else np.zeros_like(x)


class Model:
    grid: dict[str, list] = {}
    learned = True

    def __init__(self, **params):
        self.params = params

    def fit(self, df: pd.DataFrame, cols: list[str]) -> "Model":
        self.cols = cols
        return self

    def score(self, df: pd.DataFrame) -> np.ndarray:
        raise NotImplementedError

    @classmethod
    def configs(cls):
        keys = list(cls.grid)
        for vals in itertools.product(*[cls.grid[k] for k in keys]):
            yield dict(zip(keys, vals))


# ------------------------------------------------------------------ scorers

class Column(Model):
    """Rank by one column (or a fixed linear combination). No learning."""
    learned = False

    def __init__(self, expr, **params):
        super().__init__(**params)
        self.expr = expr

    def score(self, df):
        return np.asarray(self.expr(df), dtype=float)


class Hybrid(Model):
    """Statistical hybrid: a weighted sum of standardised evidence columns.
    Weights are chosen inside the training folds (grid)."""
    learned = False

    def __init__(self, terms, **params):
        super().__init__(**params)
        self.terms = terms                      # [(column, sign, param name or None)]

    def score(self, df):
        out = np.zeros(len(df))
        for col, sign, w in self.terms:
            out += sign * (self.params.get(w, 1.0) if w else 1.0) * _z(df[col])
        return out


class NaiveBayesBeta(Model):
    """Bayesian scoring with uncertainty. Each feature is binned into
    quantiles on the training rows; the per-bin likelihood of a positive and
    of a negative carries a Beta(a, a) prior, so sparse bins shrink toward
    no evidence instead of swinging the score. An empirical-Bayes candidate
    prior (how often this candidate was a right answer in training queries,
    shrunk toward the base rate) gives general usefulness."""
    grid = {"a": [0.5, 2.0], "bins": [4, 8]}

    def __init__(self, feats, use_prior=True, **params):
        super().__init__(**params)
        self.feats, self.use_prior = feats, use_prior

    def fit(self, df, cols):
        a, nb = self.params["a"], self.params["bins"]
        y = df["label"].to_numpy()
        self.base = (y.sum() + 1) / (len(y) + 2)
        self.edges, self.llr = {}, {}
        for f in self.feats:
            x = df[f].to_numpy(dtype=float)
            e = np.unique(np.quantile(x, np.linspace(0, 1, nb + 1)[1:-1]))
            b = np.searchsorted(e, x, side="right")
            k = len(e) + 1
            pos = np.bincount(b[y == 1], minlength=k) + a
            neg = np.bincount(b[y == 0], minlength=k) + a
            self.edges[f] = e
            self.llr[f] = np.log(pos / pos.sum()) - np.log(neg / neg.sum())
        if self.use_prior:
            g = df.groupby("candidate")["label"].agg(["sum", "count"])
            m = 5.0                                         # prior strength, in queries
            rate = (g["sum"] + m * self.base) / (g["count"] + m)
            self.prior = np.log(rate / (1 - rate)) - np.log(self.base / (1 - self.base))
        return self

    def score(self, df):
        s = np.zeros(len(df))
        for f in self.feats:
            b = np.searchsorted(self.edges[f], df[f].to_numpy(dtype=float), side="right")
            s += self.llr[f][b]
        if self.use_prior:
            s += df["candidate"].map(self.prior).fillna(0.0).to_numpy()
        return s


class CuratedFrequency(Model):
    """How often this candidate is a right answer in the training queries,
    shrunk toward the base rate (empirical Bayes, 5 pseudo-queries). The
    simplest use of the curated labels: "olive oil is usually curated". Any
    learner can pick this up through the candidate's own features, so it is
    the fair baseline for learners, next to corpus popularity."""
    learned = False

    def fit(self, df, cols):
        base = (df["label"].sum() + 1) / (len(df) + 2)
        g = df.groupby("candidate")["label"].agg(["sum", "count"])
        self.rate = (g["sum"] + 5 * base) / (g["count"] + 5)
        return self

    def score(self, df):
        return df["candidate"].map(self.rate).fillna(0.0).to_numpy()


class KnnStates(Model):
    """Pairing only: score a filler by how often it is curated for the k
    training states most similar to this one (cosine over state features)."""
    grid = {"k": [3, 5, 10]}

    def fit(self, df, cols):
        self.cols = [c for c in cols if c.startswith(("B_s_", "D_"))]
        st = df.drop_duplicates("query").set_index("query")[self.cols].astype(float)
        self.S = st
        self.pos = df[df.label == 1].groupby("query")["candidate"].apply(set).to_dict()
        return self

    def score(self, df):
        out = np.zeros(len(df))
        k = self.params["k"]
        A = self.S.to_numpy()
        An = A / (np.linalg.norm(A, axis=1, keepdims=True) + 1e-9)
        for q, idx in df.groupby("query").groups.items():
            v = df.loc[idx[0], self.cols].to_numpy(dtype=float)
            sims = An @ (v / (np.linalg.norm(v) + 1e-9))
            top = np.argsort(-sims)[:k]
            votes: dict[str, float] = {}
            for t in top:
                for f in self.pos.get(self.S.index[t], ()):
                    votes[f] = votes.get(f, 0.0) + max(sims[t], 0.0)
            out[df.index.get_indexer(idx)] = df.loc[idx, "candidate"].map(votes).fillna(0.0)
        return out


# ------------------------------------------------------------------ learners

class SkModel(Model):
    def make(self):
        raise NotImplementedError

    def fit(self, df, cols):
        self.cols = cols
        self.m = self.make()
        self.m.fit(df[cols].to_numpy(dtype=float), df["label"].to_numpy())
        return self

    def score(self, df):
        return self.m.predict_proba(df[self.cols].to_numpy(dtype=float))[:, 1]


class LogReg(SkModel):
    grid = {"C": [0.01, 0.1, 1.0]}

    def make(self):
        return make_pipeline(StandardScaler(), LogisticRegression(
            C=self.params["C"], class_weight="balanced", max_iter=2000))


class Knn(SkModel):
    grid = {"k": [10, 30]}

    def make(self):
        return make_pipeline(StandardScaler(), KNeighborsClassifier(
            n_neighbors=self.params["k"], weights="distance"))


class Forest(SkModel):
    grid = {"max_depth": [6, None], "min_samples_leaf": [1, 5]}
    cls = RandomForestClassifier

    def make(self):
        return self.cls(n_estimators=200, class_weight="balanced_subsample", n_jobs=-1,
                        random_state=0, **self.params)


class Extra(Forest):
    cls = ExtraTreesClassifier


class HGB(SkModel):
    grid = {"learning_rate": [0.05, 0.1], "max_depth": [3, None]}

    def make(self):
        return HistGradientBoostingClassifier(class_weight="balanced", random_state=0,
                                              max_iter=200, **self.params)


class LGBMClf(SkModel):
    grid = {"num_leaves": [7, 15], "n_estimators": [100, 300], "min_child_samples": [10, 30]}

    def make(self):
        return lgb.LGBMClassifier(learning_rate=0.05, is_unbalance=True, subsample=0.8,
                                  subsample_freq=1, colsample_bytree=0.8, random_state=0,
                                  verbose=-1, **self.params)


class LGBMRank(Model):
    """LambdaRank, grouped by query (a prepared state for pairing, a
    (state, source) substitution context for Scout)."""
    grid = {"num_leaves": [7, 15], "n_estimators": [100, 300], "min_child_samples": [10, 30]}

    def fit(self, df, cols):
        self.cols = cols
        d = df.sort_values("query", kind="stable")
        groups = d.groupby("query", sort=False).size().to_numpy()
        self.m = lgb.LGBMRanker(objective="lambdarank", learning_rate=0.05, subsample=0.8,
                                subsample_freq=1, colsample_bytree=0.8, random_state=0,
                                verbose=-1, lambdarank_truncation_level=10, **self.params)
        self.m.fit(d[cols].to_numpy(dtype=float), d["label"].to_numpy(), group=groups)
        return self

    def score(self, df):
        return self.m.predict(df[self.cols].to_numpy(dtype=float))


LEARNERS = {
    "Logistic regression": LogReg,
    "K-nearest neighbours (rows)": Knn,
    "Random forest": Forest,
    "Extra trees": Extra,
    "Histogram gradient boosting": HGB,
    "LightGBM classifier": LGBMClf,
    "LightGBM LambdaRank": LGBMRank,
}


def _hybrid(terms, ws):
    cls = type("HybridT", (Hybrid,), {"grid": {w: ws for _c, _s, w in terms if w}})
    return lambda **p: cls(terms, **p)


def _nb(feats, prior=True):
    cls = type("NBT", (NaiveBayesBeta,), {})
    return lambda **p: cls(feats, prior, **p)


def pairing_models():
    """(name, factory, grid, feature sets it runs on)."""
    col = lambda f: (lambda **p: Column(f, **p))  # noqa: E731
    W = [0.0, 0.5, 1.0, 2.0]
    out = [
        ("Popularity", col(lambda d: d["A_pop"]), {}, ["A"]),
        ("Curated frequency", CuratedFrequency, {}, ["-"]),
        ("Co-occurrence", col(lambda d: d["A_cooc_base"]), {}, ["A"]),
        ("Smoothed lift / PPMI", col(lambda d: d["A_ppmi_base"]), {}, ["A"]),
        ("SVD embeddings", col(lambda d: d["A_cos_base"]), {}, ["A"]),
        ("Flavour compatibility", col(lambda d: d["B_x_compat"] + 1e-3 * d["B_f_n_roles"]), {}, ["B"]),
        ("Hybrid statistical", _hybrid([("A_ppmi_base", 1, None), ("A_cos_base", 1, "w_cos"),
                                        ("B_x_compat", 1, "w_compat")], W),
         {"w_cos": W, "w_compat": W}, ["C"]),
    ]
    nbA = ["A_ppmi_base", "A_cos_base", "A_pop"]
    nbB = ["B_x_fills_risk", "B_x_dup_provided", "B_x_repairs", "B_x_avoid"]
    out += [("Bayesian scoring", _nb(nbA), NaiveBayesBeta.grid, ["A"]),
            ("Bayesian scoring", _nb(nbB), NaiveBayesBeta.grid, ["B"]),
            ("Bayesian scoring", _nb(nbA + nbB), NaiveBayesBeta.grid, ["C"]),
            ("K-nearest neighbours (states)", KnnStates, KnnStates.grid, ["B", "D"])]
    out += [(n, c, c.grid, ["A", "B", "C", "D"]) for n, c in LEARNERS.items()]
    return out


def scout_models():
    col = lambda f: (lambda **p: Column(f, **p))  # noqa: E731
    W = [0.0, 1.0, 2.0]
    out = [
        ("Popularity", col(lambda d: d["A_pop"]), {}, ["A"]),
        ("Curated frequency", CuratedFrequency, {}, ["-"]),
        ("Co-occurrence with the state", col(lambda d: d["A_cooc_base"]), {}, ["A"]),
        ("Smoothed lift / PPMI with the state", col(lambda d: d["A_ppmi_base"]), {}, ["A"]),
        ("Rarely with the source (-PPMI)", col(lambda d: -d["A_ppmi_src"]), {}, ["A"]),
        ("SVD cosine to the source", col(lambda d: d["A_cos_src"]), {}, ["A"]),
        ("Functional similarity", col(lambda d: d["B_role_jaccard"] + 0.5 * d["B_same_family"]
                                      - 0.1 * d["B_avail_gap"]), {}, ["B"]),
        ("Context nearest neighbour", _hybrid([("A_cos_src", 1, None), ("B_role_jaccard", 1, "w_role"),
                                               ("A_ppmi_base", 1, "w_ctx")], W),
         {"w_role": W, "w_ctx": W}, ["C"]),
        ("Hybrid statistical", _hybrid([("A_cos_src", 1, None), ("B_role_jaccard", 1, "w_role"),
                                        ("A_ppmi_base", 1, "w_ctx"), ("A_ppmi_src", -1, "w_alt"),
                                        ("B_x_compat", 1, "w_compat")], W),
         {"w_role": W, "w_ctx": W, "w_alt": W, "w_compat": W}, ["C"]),
    ]
    nbA = ["A_cos_src", "A_ppmi_base", "A_ppmi_src", "A_pop"]
    nbB = ["B_role_jaccard", "B_same_family", "B_avail_gap", "B_x_fills_risk"]
    out += [("Bayesian scoring", _nb(nbA), NaiveBayesBeta.grid, ["A"]),
            ("Bayesian scoring", _nb(nbB), NaiveBayesBeta.grid, ["B"]),
            ("Bayesian scoring", _nb(nbA + nbB), NaiveBayesBeta.grid, ["C"])]
    out += [(n, c, c.grid, ["A", "B", "C", "D"]) for n, c in LEARNERS.items()]
    return out
