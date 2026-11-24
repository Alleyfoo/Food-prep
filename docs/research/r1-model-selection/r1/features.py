"""Candidate tables and the feature sets A-D (plus a leakage probe, L).

  A  culinary only      CulinaryDB statistics and embeddings
  B  functional only    flavour profiles, ingredient roles, families
  C  combined           A + B
  D  full context       C + independently defined preparation characteristics
                        (technique, heat, moisture, serving form, keeping,
                        transformation tags)
  L  leakage probe      D + transformation_missing_roles. Those roles are
                        written per state and their notes name the curated
                        fillers ("olive oil or cheese"), so they are NOT an
                        independent characteristic. L exists only to measure
                        how much such a feature would inflate the scores.

Every row is one (query, candidate). For pairing, the query is a prepared
state; for Scout it is (state, source filler). Labels come from
Ontology.answers_*; no feature reads them.
"""
from __future__ import annotations

import math

import numpy as np
import pandas as pd

from .data import FLAVOURS, ROLES, CorpusStats, Ontology

AVAIL = ["very_common", "common", "occasional", "specialty", "unknown"]
SETS = ("A", "B", "C", "D", "L")


def _onehot(prefix: str, value: str, vocab: list[str]) -> dict[str, float]:
    return {f"{prefix}{v}": float(value == v) for v in vocab}


def _multihot(prefix: str, values: list[str], vocab: list[str]) -> dict[str, float]:
    s = set(values)
    return {f"{prefix}{v}": float(v in s) for v in vocab}


class Vocab:
    """Category vocabularies fixed from the ontology's descriptions, never from labels."""

    def __init__(self, o: Ontology):
        st = list(o.states.values())
        ing = list(o.ingredients.values())
        self.families = sorted({i.family for i in ing})
        self.kinds = sorted({i.kind for i in ing})
        self.textures = sorted({t for s in st for t in s.texture_tags})
        self.forms = sorted({s.serving_form for s in st})
        self.heat = sorted({s.heat_type for s in st})
        self.moisture = sorted({s.moisture_change for s in st})
        self.keeps = sorted({s.keeps_well for s in st})
        self.ttags = sorted({t for s in st for t in s.transformation_tags})
        self.state_flav = sorted({t for s in st for t in s.flavour_tags} | set(FLAVOURS))


# ---------------------------------------------------------------- shared parts

def corpus_feats(cs: CorpusStats, a: str, b: str, tag: str) -> dict[str, float]:
    return {
        f"A_cooc_{tag}": math.log1p(cs.cooc(a, b)),
        f"A_lift_{tag}": math.log(cs.lift(a, b, alpha=5.0)),
        f"A_ppmi_{tag}": cs.ppmi(a, b, alpha=5.0),
        f"A_cos_{tag}": cs.cos(a, b),
    }


def filler_desc(o: Ontology, v: Vocab, f: str, prefix: str = "B_f_") -> dict[str, float]:
    i = o.ingredients[f]
    d = _multihot(prefix + "role_", i.roles, ROLES)
    d.update(_onehot(prefix + "fam_", i.family, v.families))
    d.update(_onehot(prefix + "avail_", i.availability, AVAIL))
    d.update(_onehot(prefix + "kind_", i.kind, v.kinds))
    d[prefix + "n_roles"] = float(len(i.roles))
    return d


def state_desc(o: Ontology, v: Vocab, s: str) -> dict[str, float]:
    st = o.states[s]
    d = _multihot("B_s_flav_", st.flavour_tags, v.state_flav)
    d.update(_multihot("B_s_tex_", st.texture_tags, v.textures))
    d.update(_multihot("B_s_prov_", st.provides_roles, ROLES))
    d.update(_multihot("B_s_risk_", st.missing_risks, ROLES))
    d["B_s_heavy"] = st.heaviness
    d["B_s_dry"] = st.dryness
    return d


def compat(o: Ontology, s: str, f: str) -> dict[str, float]:
    """Functional complementarity of a filler for a state, from descriptions
    only: does the filler bring a role the state's sensory profile says it
    risks missing, and does it duplicate a role the state already provides?
    A filler whose `repairs` names one of the state's flavour tags, or whose
    `avoid_when` does, counts too."""
    st, i = o.states[s], o.ingredients[f]
    fills = len(set(i.roles) & set(st.missing_risks))
    dup = len(set(i.roles) & set(st.provides_roles))
    rep = len(set(i.repairs) & (set(st.flavour_tags) | set(st.texture_tags)))
    avoid = len(set(i.avoid_when) & (set(st.flavour_tags) | set(st.texture_tags)))
    return {"B_x_fills_risk": float(fills), "B_x_dup_provided": float(dup),
            "B_x_repairs": float(rep), "B_x_avoid": float(avoid),
            "B_x_compat": fills - 0.5 * dup + 0.5 * rep - avoid}


def context_desc(o: Ontology, v: Vocab, s: str) -> dict[str, float]:
    st = o.states[s]
    d = _onehot("D_form_", st.serving_form, v.forms)
    d.update(_onehot("D_heat_", st.heat_type, v.heat))
    d.update(_onehot("D_moist_", st.moisture_change, v.moisture))
    d.update(_onehot("D_keeps_", st.keeps_well, v.keeps))
    d.update(_multihot("D_tt_", st.transformation_tags, v.ttags))
    return d


def probe_desc(o: Ontology, s: str, f: str) -> dict[str, float]:
    st, i = o.states[s], o.ingredients[f]
    d = _multihot("L_miss_", st.curated_missing_roles, ROLES)
    d["L_fills_curated_missing"] = float(len(set(i.roles) & set(st.curated_missing_roles)))
    return d


# ---------------------------------------------------------------- tables

def pairing_table(o: Ontology, cs: CorpusStats) -> pd.DataFrame:
    """One row per (prepared state, candidate filler). Candidates: every
    ingredient except the state's own base."""
    v = Vocab(o)
    answers = o.answers_pairings()
    rows = []
    for s, st in o.states.items():
        sd, cd = state_desc(o, v, s), context_desc(o, v, s)
        for f in o.ingredients:
            if f == st.base:
                continue
            r = {"query": s, "fold": st.base, "candidate": f,
                 "label": int((s, f) in answers),
                 "A_pop": math.log1p(cs.count(f)), "A_covered": float(f in cs.covered),
                 **corpus_feats(cs, f, st.base, "base")}
            r.update(filler_desc(o, v, f))
            r.update(sd)
            r.update(compat(o, s, f))
            r.update(cd)
            r.update(probe_desc(o, s, f))
            rows.append(r)
    return pd.DataFrame(rows)


def scout_table(o: Ontology, cs: CorpusStats) -> pd.DataFrame:
    """One row per (state, source, candidate substitute). Queries are the
    (state, source) pairs the Scout rules start from; candidates are every
    ingredient except the source and the state's base."""
    v = Vocab(o)
    answers = o.answers_scout()
    queries = sorted({(s, src) for s, src, _sub in answers})
    rows = []
    for s, src in queries:
        st = o.states[s]
        sd, cd = state_desc(o, v, s), context_desc(o, v, s)
        si = o.ingredients[src]
        for f in o.ingredients:
            if f in (src, st.base):
                continue
            fi = o.ingredients[f]
            inter = set(fi.roles) & set(si.roles)
            union = set(fi.roles) | set(si.roles)
            r = {"query": f"{s}|{src}", "fold": st.base, "candidate": f, "source": src,
                 "label": int((s, src, f) in answers),
                 "A_pop": math.log1p(cs.count(f)), "A_covered": float(f in cs.covered),
                 "A_pop_ratio": math.log1p(cs.count(f)) - math.log1p(cs.count(src)),
                 **corpus_feats(cs, f, st.base, "base"),
                 **corpus_feats(cs, f, src, "src")}
            r.update(filler_desc(o, v, f))
            r.update(filler_desc(o, v, src, prefix="B_src_"))
            r.update({
                "B_role_jaccard": len(inter) / len(union) if union else 0.0,
                "B_same_family": float(fi.family == si.family and fi.family != "none"),
                "B_avail_gap": abs(AVAIL.index(fi.availability if fi.availability in AVAIL else "unknown")
                                   - AVAIL.index(si.availability if si.availability in AVAIL else "unknown")),
            })
            r.update(sd)
            r.update(compat(o, s, f))
            r.update(cd)
            r.update(probe_desc(o, s, f))
            rows.append(r)
    return pd.DataFrame(rows)


def columns(df: pd.DataFrame, fset: str) -> list[str]:
    if fset == "-":                      # models that use no features
        return []
    pref = {"A": ("A_",), "B": ("B_",), "C": ("A_", "B_"), "D": ("A_", "B_", "D_"),
            "L": ("A_", "B_", "D_", "L_")}[fset]
    return [c for c in df.columns if c.startswith(pref)]
