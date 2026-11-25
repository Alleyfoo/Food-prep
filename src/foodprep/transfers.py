"""Controlled transfers: a documented construction carried over to another
ingredient (R4, docs/research/r4-transfers/).

A transfer in data/transfers.yaml starts from one documented route in
data/constructions.yaml (R3) and changes only what the transfer changes: a
material is swapped for another, steps are added or removed, an assembly is
rewritten. This module builds that derived route and runs it through R3's
validator (`constructions.validate_route`) unchanged, next to the base route,
so the two can be read side by side: which role requirements and claims still
hold, which fail, which are unknown.

The R3 validator only knows R2's recipe ids (E/M/A). A transfer cites R4
evidence ids (one letter and a number, listed in
docs/research/r4-transfers/sources.md); this module accepts those ids where
the R3 validator reports them as malformed, and nothing else. A citation that
is neither R2 nor R4 is still an error.

The validator says whether the transfer is *consistent* with the operation
model. Whether it is *good food* comes from the evidence each candidate cites
(`evidence_says`), and the report says whether the two agree. Nothing here
ranks or scores a transfer.
"""

from __future__ import annotations

import copy
import re
from dataclasses import dataclass, field
from functools import lru_cache

from foodprep import constructions as c
from foodprep import operations as o
from foodprep import pair_counts as pc

PATH = o.DATA / "transfers.yaml"

SCHEMA = {
    "candidate": ["name", "question", "base", "proposed", "replaced_by", "lidl", "status",
                  "evidence", "evidence_says", "verdict", "reasons", "transfer", "model",
                  "kitchen_test", "note"],
    "base": ["dish", "route"],
    "transfer": ["swap", "drop", "materials", "assemblies", "result", "final", "why",
                 "patterns", "holds_by", "water", "gaps"],
    "model": ["explains", "cannot", "agrees"],
    "kitchen_test": ["compare", "judge", "taste", "stop_if"],
}
STATUSES = ("documented", "inference")          # is the transfer found in practice?
EVIDENCE_SAYS = ("works", "works_with_conditions", "poor", "fails", "unknown")
VERDICTS = ("worth_cooking", "not_worth_it", "rejected")
EVIDENCE_ID = re.compile(r"^[A-Z]\d+$")         # R4 ids (sources.md); R2 ids end in a letter
_MALFORMED = re.compile(r"malformed recipe id '([^']+)'")


@lru_cache(maxsize=1)
def load() -> dict:
    return pc.load_yaml(PATH)


def candidate_ids() -> list[str]:
    return list(load()["candidates"])


# ---- the derived route -----------------------------------------------------------

def _rename(raw, swap: dict):
    """Members of a role with swapped ids renamed."""
    if raw is None:
        return None
    if isinstance(raw, list):
        return [_rename(x, swap) for x in raw]
    if isinstance(raw, dict):
        return {**raw, "use": swap.get(raw.get("use"), raw.get("use"))}
    return swap.get(raw, raw)


def _without(raw, drop: set):
    if raw is None:
        return None
    items = raw if isinstance(raw, list) else [raw]
    kept = [x for x in items if (x.get("use") if isinstance(x, dict) else x) not in drop]
    if not kept:
        return None
    return kept if isinstance(raw, list) else kept[0]


def derive(tid: str) -> tuple[dict, dict]:
    """(route, data): the base route with the transfer's changes applied, and the
    constructions data with this route as its only dish."""
    cand = load()["candidates"][tid]
    base = cand["base"]
    cdata = c.load()
    route = copy.deepcopy(cdata["dishes"][base["dish"]]["routes"][base["route"]])
    t = cand.get("transfer") or {}
    swap = dict(t.get("swap") or {})
    drop = set(t.get("drop") or [])
    mats = route.get("materials") or {}
    asms = route.get("assemblies") or {}
    for old in list(swap) + list(drop):
        mats.pop(old, None)
        asms.pop(old, None)
    for spec in mats.values():
        src = spec.get("from")
        if isinstance(src, dict) and src.get("material") in swap:
            spec["from"] = {**src, "material": swap[src["material"]]}
    for spec in asms.values():
        roles = {}
        for role, raw in (spec.get("roles") or {}).items():
            raw = _without(_rename(raw, swap), drop)
            if raw is not None:
                roles[role] = raw
        spec["roles"] = roles
        for e in spec.get("expects") or []:
            if e.get("member") in swap:
                e["member"] = swap[e["member"]]
    mats.update(copy.deepcopy(t.get("materials") or {}))
    asms.update(copy.deepcopy(t.get("assemblies") or {}))
    route["materials"], route["assemblies"] = mats, asms
    route["result"] = t.get("result") or swap.get(route.get("result"), route.get("result"))
    for k in ("final", "why", "patterns", "holds_by", "water", "gaps"):
        if k in t:
            route[k] = copy.deepcopy(t[k])
    route["recipes"] = list(route.get("recipes") or []) + list(cand.get("evidence") or [])
    data = {**cdata,
            "additions": {**cdata["additions"], **(load().get("additions") or {})},
            "dishes": {tid: {"name": cand["name"], "routes": {"transfer": route}}}}
    return route, data


# ---- reports -------------------------------------------------------------------------

@dataclass
class TransferReport:
    id: str
    base: c.RouteReport
    route: c.RouteReport | None                    # None: rejected before modelling
    evidence_ids: list = field(default_factory=list)  # R4 ids the route cites

    @property
    def model_holds(self) -> bool | None:
        """True: no step, role or claim fails; False: something fails; None: not modelled."""
        if self.route is None:
            return None
        return not (self.route.failures or self.route.errors)

    @property
    def agrees(self) -> bool | None:
        """Does the model's consistency check agree with what the evidence says?"""
        says = load()["candidates"][self.id].get("evidence_says")
        if self.model_holds is None or says == "unknown":
            return None
        works = says in ("works", "works_with_conditions")
        return works == self.model_holds


def validate(tid: str, cat: o.Catalogue | None = None) -> TransferReport:
    cat = cat or o.load()
    cand = load()["candidates"][tid]
    b = cand["base"]
    base = c.validate_route(b["dish"], b["route"], cat)
    if not cand.get("transfer"):
        return TransferReport(tid, base, None)
    _, data = derive(tid)
    rep = c.validate_route(tid, "transfer", cat, data)
    cited = []
    kept = []
    for e in rep.errors:
        m = _MALFORMED.search(e)
        if m and EVIDENCE_ID.match(m.group(1)):
            cited.append(m.group(1))       # an R4 evidence id, checked against sources.md
        else:
            kept.append(e)
    rep.errors = kept
    return TransferReport(tid, base, rep, sorted(set(cited)))


def candidate_errors(tid: str) -> list[str]:
    cand = load()["candidates"][tid]
    out = []
    extra = set(cand) - set(SCHEMA["candidate"])
    if extra:
        out.append(f"unknown candidate field(s) {sorted(extra)}")
    for key in ("base", "transfer", "model", "kitchen_test"):
        sub = cand.get(key)
        if isinstance(sub, dict) and set(sub) - set(SCHEMA[key]):
            out.append(f"unknown {key} field(s) {sorted(set(sub) - set(SCHEMA[key]))}")
    b = cand.get("base") or {}
    routes = (c.load()["dishes"].get(b.get("dish")) or {}).get("routes") or {}
    if b.get("route") not in routes:
        out.append(f"base {b} is not a documented route")
    if cand.get("status") not in STATUSES:
        out.append(f"status must be one of {STATUSES}")
    if cand.get("evidence_says") not in EVIDENCE_SAYS:
        out.append(f"evidence_says must be one of {EVIDENCE_SAYS}")
    if cand.get("verdict") not in VERDICTS:
        out.append(f"verdict must be one of {VERDICTS}")
    if not cand.get("reasons"):
        out.append("no reasons for the verdict")
    for e in cand.get("evidence") or []:
        if not EVIDENCE_ID.match(str(e)):
            out.append(f"malformed evidence id {e!r}")
    if cand.get("status") == "documented" and not cand.get("evidence"):
        out.append("documented, but no evidence cited")
    if cand.get("verdict") == "worth_cooking":
        kt = cand.get("kitchen_test") or {}
        for k in ("compare", "judge", "taste"):
            if not kt.get(k):
                out.append(f"worth cooking, but the kitchen test has no `{k}`")
        if not cand.get("transfer"):
            out.append("worth cooking, but not represented as a transfer")
    return out


# ---- rendering ---------------------------------------------------------------------

def _label(v: bool | None, yes: str, no: str) -> str:
    return "not modelled" if v is None else (yes if v else no)


def render(tid: str) -> str:
    data = load()
    if tid not in data["candidates"]:
        return f"No transfer {tid!r}. Known: {', '.join(data['candidates'])}.\n"
    cand = data["candidates"][tid]
    rep = validate(tid)
    b = cand["base"]
    out = [f"{cand['name']} [{cand['status']}; verdict: {cand['verdict'].replace('_', ' ')}]",
           f"  question: {' '.join(str(cand.get('question', '')).split())}",
           f"  from: {b['dish']}/{b['route']} ({rep.base.verdict} represented)",
           f"  evidence: {', '.join(cand.get('evidence') or []) or 'none'}; "
           f"says {cand['evidence_says'].replace('_', ' ')}"]
    if rep.route is not None:
        route, _ = derive(tid)
        r = rep.route
        out.append(f"  transfer route: {r.verdict} represented; model "
                   f"{_label(rep.model_holds, 'holds', 'fails')}; agrees with the evidence: "
                   f"{'not comparable' if rep.agrees is None else _label(rep.agrees, 'yes', 'no')}")
        for mid, spec in (route.get("materials") or {}).items():
            src = spec["from"] if isinstance(spec["from"], str) else \
                f"{spec['from']['material']} [{spec['from']['output']}]"
            path = " -> ".join(c._en(s["op"]) for s in c._steps(spec.get("steps"))
                               if s.get("op") in o.load().operations)
            out.append(f"    material {mid}: {src}" + (f" -> {path}" if path else ""))
        for aid, spec in (route.get("assemblies") or {}).items():
            roles = "; ".join(f"{role}: {', '.join(m['use'] for m in c._members(raw))}"
                              for role, raw in (spec.get("roles") or {}).items())
            out.append(f"    {aid} = {spec['op']} ({roles})")
        for src, step, output, mid in r.recombinations:
            out.append(f"    recombination: {src} -> {step} [{output}] -> {mid}")
        for problem in r.failures + r.unknowns + r.unaccounted + r.errors:
            out.append(f"    ! {problem}")
        for g in r.model_gaps:
            out.append(f"    gap (model): {g}")
    model = cand.get("model") or {}
    for x in model.get("explains") or []:
        out.append(f"  explains: {' '.join(x.split())}")
    for x in model.get("cannot") or []:
        out.append(f"  cannot: {' '.join(x.split())}")
    for x in cand.get("reasons") or []:
        out.append(f"  reason: {' '.join(x.split())}")
    kt = cand.get("kitchen_test") or {}
    if kt:
        out.append(f"  kitchen test: compare {' '.join(str(kt.get('compare', '')).split())}")
        out.append(f"    judge: {' '.join(str(kt.get('judge', '')).split())}")
        out.append(f"    taste: {' '.join(str(kt.get('taste', '')).split())}")
    return "\n".join(out) + "\n"


def render_list() -> str:
    out = ["Controlled transfers (R4): candidate, status, evidence, model, verdict", ""]
    for tid, cand in load()["candidates"].items():
        rep = validate(tid)
        model = "not modelled" if rep.route is None else rep.route.verdict
        out.append(f"{tid:22} {cand['status']:11} {cand['evidence_says']:22} "
                   f"{model:13} {cand['verdict']}")
    return "\n".join(out) + "\n"
