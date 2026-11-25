"""Documented processing conditions (R5, docs/research/r5-processing-conditions/).

R1-R4 record what a step does: ingredient -> operation -> state. This module
records what documented practice says you have to *do* for the step to work,
read from data/processing_conditions.yaml:

- the conditions (medium, heat, starting state);
- how long, kept apart as elapsed time and the kind of active work;
- what shifts the time;
- how you know it is done (observable, primary; time is a guide);
- how you know it failed, with the stated cause;
- how long the resulting intermediate keeps, and how.

A condition belongs to a step in a documented dish (an R3 route or an R4
transfer), because the same part and operation can have a different endpoint
in another role. A pair's `default` holds only what its sources agree on.
Conflicting instructions stay as separate versions with their sources;
nothing is averaged, derived, predicted or simulated, and nothing is ranked.

Two queries:
- `for_step(address)` / `for_pair(id)`: the conditions of one step or pair;
- `from_state(part, tokens)`: given a state you already have, the documented
  routes and transfers that pass through an equivalent state, and the
  remaining steps from there. Equivalence is R1's `Material.key()`; the state
  is built by applying the named R1 operations to the part with
  `operations.apply`, exactly as the R3 validator walks a route.

constructions.py, operations.py and their data are read, never changed.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

from foodprep import constructions as c
from foodprep import operations as o
from foodprep import pair_counts as pc
from foodprep import transfers as t

PATH = o.DATA / "processing_conditions.yaml"
RESEARCH = Path(__file__).resolve().parents[2] / "docs" / "research"
R5_DOCS = RESEARCH / "r5-processing-conditions"

SCHEMA = {
    "top": ["vocabulary", "pairs", "sequences", "intermediates"],
    "pair": ["name", "part", "op", "steps", "default", "at", "conflicts", "confidence",
             "gaps", "note"],
    "fields": ["start", "medium", "elapsed", "active", "shifts", "completion", "failure",
               "role", "note"],
    "start": ["particle", "moisture", "sources", "note"],
    "medium": ["medium", "temp_c", "cover", "sources", "note"],
    "elapsed": ["min", "max", "unit", "label", "sources", "note"],
    "active": ["kind", "sources", "note"],
    "shift": ["factor", "effect", "sources"],
    "check": ["check", "cause", "sources"],
    "conflict": ["topic", "versions", "note"],
    "version": ["says", "sources"],
    "intermediate": ["name", "part", "after", "at", "keeps", "note"],
    "sequence": ["name", "steps", "members", "depends", "misses", "alternatives", "finish",
                 "gaps", "note"],
    "seqstep": ["endpoint", "start", "medium", "elapsed", "active", "shifts", "completion",
                "failure", "role", "note"],
    "endpoint": ["kind", "sources", "by", "note"],
    "member": ["completion", "failure", "note"],
    "depend": ["step", "because", "says", "sources"],
    "miss": ["step", "when", "failure", "sources"],
    "alternative": ["name", "route", "says", "sources"],
    "finish": ["stage", "elapsed", "active", "completion", "failure", "note"],
    "keep": ["where", "how", "min", "max", "unit", "basis", "sources", "note"],
}
UNITS = ("s", "min", "h", "days", "months")
# where a keeping time comes from: a public food-safety body, a home-economics
# association (Martat), or a cook, recipe or packet
BASES = ("food_safety", "home_economics", "cooking")
FORBIDDEN = {"score", "rank", "rating", "priority", "weight", "predicted", "estimate"}

R2_ID = re.compile(r"^[EMA]\d+[a-z]$")      # docs/research/r2-construction-patterns/recipes.md
R4_ID = re.compile(r"^[A-PR-Z]\d+$")        # docs/research/r4-transfers/sources.md
R5_ID = re.compile(r"^Q\d+$")               # docs/research/r5-processing-conditions/evidence-*.md
STEP = re.compile(r"^(?:transfer:(?P<tid>[a-z0-9_]+)|(?P<dish>[a-z0-9_]+)/(?P<route>[a-z0-9_]+))"
                  r"/(?P<owner>[a-z0-9_]+)/(?P<index>\d+)$")


@lru_cache(maxsize=1)
def load() -> dict:
    return pc.load_yaml(PATH)


def pair_ids() -> list[str]:
    return list(load()["pairs"])


def _ops(pair: dict) -> list[str]:
    op = pair.get("op")
    return list(op) if isinstance(op, list) else [op]


# ---- documented routes as step sequences ---------------------------------------------

@dataclass
class Point:
    """One step of a documented route, with the material state before and after it
    (materials only; an assembly's state is the R3 validator's business)."""
    address: str
    owner: str
    index: int
    op: str
    kind: str                         # material | assembly
    evidence: str = ""
    before: o.Material | None = None
    after: o.Material | None = None


@dataclass
class Route:
    key: str                          # dish/route or transfer:<id>
    name: str
    spec: dict
    points: list = field(default_factory=list)

    def point(self, owner: str, index: int) -> Point | None:
        return next((p for p in self.points if p.owner == owner and p.index == index), None)


def _walk(key: str, name: str, route: dict, cat: o.Catalogue) -> Route:
    """Every step of a route, in the order the R3 validator applies them: each
    material from its part (or another material's output) through its steps with
    `operations.apply`, keeping the output the route keeps."""
    r = Route(key, name, route)
    mats = route.get("materials") or {}
    outputs: dict = {}
    done: dict = {}

    def material(mid: str, seen: frozenset = frozenset()) -> None:
        if mid in done or mid in seen or mid not in mats:
            return
        spec = mats[mid]
        src = spec.get("from")
        m = None
        if isinstance(src, str):
            ing, _, part = src.partition(".")
            starts = o.start_materials(ing, part, cat) if ing in cat.parts else []
            m = starts[0] if starts else None
        elif isinstance(src, dict):
            material(src.get("material"), seen | {mid})
            m = (outputs.get((src.get("material"), src.get("step"))) or {}).get(src.get("output"))
        for i, s in enumerate(c._steps(spec.get("steps")), 1):
            op = s.get("op")
            p = Point(f"{key}/{mid}/{i}", mid, i, op, "material", s.get("evidence") or "", m)
            if m is not None and op in cat.operations and not cat.operations[op].get("assembly"):
                outs = o.apply(op, m, cat)
                names = [x.path[-1].output for x in outs]
                keep = s.get("keep") or ("main" if "main" in names else (names or [None])[0])
                outputs.setdefault((mid, op), {}).update(dict(zip(names, outs)))
                m = outs[names.index(keep)] if keep in names else None
            else:
                m = None
            p.after = m
            r.points.append(p)
        done[mid] = m

    for mid in mats:
        material(mid)
    for aid, spec in (route.get("assemblies") or {}).items():
        for i, s in enumerate(c._steps(spec.get("steps")), 1):
            r.points.append(Point(f"{key}/{aid}/{i}", aid, i, s.get("op"), "assembly",
                                  s.get("evidence") or ""))
    return r


@lru_cache(maxsize=1)
def routes() -> dict:
    """Every documented R3 route and every modelled R4 transfer, as step sequences."""
    cat = o.load()
    out = {}
    for did, dish in c.load()["dishes"].items():
        for rid, route in dish["routes"].items():
            out[f"{did}/{rid}"] = _walk(f"{did}/{rid}", dish["name"], route, cat)
    for tid in t.candidate_ids():
        cand = t.load()["candidates"][tid]
        if not cand.get("transfer"):
            continue
        route, _ = t.derive(tid)
        out[f"transfer:{tid}"] = _walk(f"transfer:{tid}", cand["name"], route, cat)
    return out


def resolve_step(address: str) -> Point | None:
    m = STEP.match(address)
    if not m:
        return None
    key = f"transfer:{m['tid']}" if m["tid"] else f"{m['dish']}/{m['route']}"
    r = routes().get(key)
    return r.point(m["owner"], int(m["index"])) if r else None


# ---- evidence ids ------------------------------------------------------------------------

@lru_cache(maxsize=1)
def evidence_index() -> dict | None:
    """id -> URL for every id this module can resolve, or None when the research
    documents are not next to the package (an installed copy)."""
    r2 = RESEARCH / "r2-construction-patterns" / "recipes.md"
    r4 = RESEARCH / "r4-transfers" / "sources.md"
    if not (r2.exists() and r4.exists() and R5_DOCS.exists()):
        return None
    out = {}
    for m in re.finditer(r"^### ([EMA]\d+[a-z])\.", r2.read_text(encoding="utf-8"), re.M):
        out[m.group(1)] = "r2-construction-patterns/recipes.md"
    for line in r4.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^\| ([A-Z]\d+) \|.*?(https?://\S+)", line)
        if m:
            out[m.group(1)] = m.group(2)
    for path in sorted(R5_DOCS.glob("evidence-*.md")):
        for m in re.finditer(r"^### (Q\d+)\s*[—-]+\s*(https?://\S+)",
                             path.read_text(encoding="utf-8"), re.M):
            out.setdefault(m.group(1), m.group(2))
    return out


def _source_ids(obj) -> set:
    found = set()
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == "sources" and isinstance(v, list):
                found |= {str(x) for x in v}
            else:
                found |= _source_ids(v)
    elif isinstance(obj, list):
        for x in obj:
            found |= _source_ids(x)
    return found


# ---- validation --------------------------------------------------------------------------

def _keys(errs: list, where: str, obj, kind: str) -> None:
    if not isinstance(obj, dict):
        errs.append(f"{where}: must be a mapping")
        return
    extra = set(obj) - set(SCHEMA[kind])
    if extra:
        errs.append(f"{where}: unknown field(s) {sorted(extra)}")
    bad = FORBIDDEN & {str(k) for k in obj}
    if bad:
        errs.append(f"{where}: no scoring or prediction fields ({sorted(bad)})")


def _cited(errs: list, where: str, obj: dict) -> None:
    if not obj.get("sources"):
        errs.append(f"{where}: no sources")


def _in(errs: list, where: str, value, vocab: list) -> None:
    for v in (value if isinstance(value, list) else [value]):
        if v not in vocab:
            errs.append(f"{where}: {v!r} is not in the vocabulary {vocab}")


def _fields_errors(errs: list, where: str, f: dict, voc: dict, kind: str = "fields") -> None:
    _keys(errs, where, f, kind)
    if not isinstance(f, dict):
        return
    if f.get("role") is not None and not isinstance(f["role"], str):
        errs.append(f"{where}: role must be text")
    s = f.get("start")
    if s is not None:
        _keys(errs, f"{where} start", s, "start")
        if "particle" in s:
            _in(errs, f"{where} start particle", s["particle"], voc["particle"])
        if "moisture" in s:
            _in(errs, f"{where} start moisture", s["moisture"], voc["moisture"])
    for i, m in enumerate(f.get("medium") or []):
        w = f"{where} medium {i + 1}"
        _keys(errs, w, m, "medium")
        _cited(errs, w, m)
        _in(errs, w, m.get("medium"), voc["medium"])
        if "cover" in m:
            _in(errs, w, m["cover"], voc["cover"])
        tc = m.get("temp_c")
        if tc is not None and not (isinstance(tc, list) and len(tc) == 2
                                   and all(isinstance(x, (int, float)) for x in tc)
                                   and tc[0] <= tc[1]):
            errs.append(f"{w}: temp_c must be [low, high]")
    for i, e in enumerate(f.get("elapsed") or []):
        w = f"{where} elapsed {i + 1}"
        _keys(errs, w, e, "elapsed")
        _cited(errs, w, e)
        if e.get("min") is None and e.get("max") is None and not e.get("label"):
            errs.append(f"{w}: needs min/max or a label")
        if (e.get("min") is not None or e.get("max") is not None) and e.get("unit") not in UNITS:
            errs.append(f"{w}: unit must be one of {UNITS}")
        if e.get("min") is not None and e.get("max") is not None and e["min"] > e["max"]:
            errs.append(f"{w}: min > max")
    a = f.get("active")
    if a is not None:
        _keys(errs, f"{where} active", a, "active")
        _cited(errs, f"{where} active", a)
        _in(errs, f"{where} active", a.get("kind"), voc["active"])
    for i, s in enumerate(f.get("shifts") or []):
        _keys(errs, f"{where} shift {i + 1}", s, "shift")
        _cited(errs, f"{where} shift {i + 1}", s)
    for kind in ("completion", "failure"):
        for i, ch in enumerate(f.get(kind) or []):
            w = f"{where} {kind} {i + 1}"
            _keys(errs, w, ch, "check")
            _cited(errs, w, ch)
            if not ch.get("check"):
                errs.append(f"{w}: no observable check")
            if kind == "completion" and "cause" in ch:
                errs.append(f"{w}: a completion check has no cause")


def errors() -> list[str]:
    """Everything wrong with the data: unknown fields, words outside the
    vocabulary, operations or parts that do not exist, steps that are not in a
    documented route (or whose operation is not the pair's), uncited claims,
    and evidence ids that do not resolve to a page that was read."""
    data = load()
    errs: list[str] = []
    _keys(errs, "top", data, "top")
    voc = data.get("vocabulary") or {}
    for k in ("particle", "moisture", "medium", "cover", "active", "confidence"):
        if not voc.get(k):
            errs.append(f"vocabulary: {k} missing")
    cat = o.load()
    for pid, p in (data.get("pairs") or {}).items():
        where = f"pair {pid}"
        _keys(errs, where, p, "pair")
        for op in _ops(p):
            if op not in cat.operations:
                errs.append(f"{where}: unknown operation {op!r}")
        part = p.get("part") or ""
        ing, _, name = part.partition(".")
        if "." in part and not o.start_materials(ing, name, cat):
            errs.append(f"{where}: no part {part!r}")
        if p.get("confidence") not in voc.get("confidence", []):
            errs.append(f"{where}: confidence must be one of {voc.get('confidence')}")
        if not p.get("steps"):
            errs.append(f"{where}: attached to no documented step")
        for addr in p.get("steps") or []:
            pt = resolve_step(addr)
            if pt is None:
                errs.append(f"{where}: step {addr!r} is not in a documented route or transfer")
            elif pt.op not in _ops(p):
                errs.append(f"{where}: step {addr} is {pt.op}, not {p.get('op')}")
        if p.get("default") is not None:
            _fields_errors(errs, f"{where} default", p["default"], voc)
        for addr, f in (p.get("at") or {}).items():
            if addr not in (p.get("steps") or []):
                errs.append(f"{where}: `at` names {addr!r}, which is not one of its steps")
            _fields_errors(errs, f"{where} at {addr}", f, voc)
        for i, cf in enumerate(p.get("conflicts") or []):
            w = f"{where} conflict {i + 1}"
            _keys(errs, w, cf, "conflict")
            vs = cf.get("versions") or []
            if len(vs) < 2:
                errs.append(f"{w}: a conflict has at least two versions")
            for j, v in enumerate(vs):
                _keys(errs, f"{w} version {j + 1}", v, "version")
                _cited(errs, f"{w} version {j + 1}", v)
    for iid, it in (data.get("intermediates") or {}).items():
        where = f"intermediate {iid}"
        _keys(errs, where, it, "intermediate")
        if it.get("at"):
            if resolve_step(it["at"]) is None:
                errs.append(f"{where}: step {it['at']!r} is not in a documented route")
            if it.get("part") or it.get("after"):
                errs.append(f"{where}: give either `at` (a step) or `part` + `after`")
        else:
            part = it.get("part") or ""
            ing, _, name = part.partition(".")
            if not o.start_materials(ing, name, cat):
                errs.append(f"{where}: no part {part!r}")
        for op in it.get("after") or []:
            if op not in cat.operations:
                errs.append(f"{where}: unknown operation {op!r}")
        for i, k in enumerate(it.get("keeps") or []):
            w = f"{where} keeps {i + 1}"
            _keys(errs, w, k, "keep")
            _cited(errs, w, k)
            if k.get("basis") not in BASES:
                errs.append(f"{w}: basis must be one of {BASES}")
            if (k.get("min") is not None or k.get("max") is not None) and k.get("unit") not in UNITS:
                errs.append(f"{w}: unit must be one of {UNITS}")
        if not it.get("at") and not from_state(it.get("part") or "",
                                                it.get("after") or []).matches:
            errs.append(f"{where}: no documented route passes through this state")
    for key, seq in (data.get("sequences") or {}).items():
        errs += sequence_errors(key, seq, voc, cat)
    idx = evidence_index()
    if idx is not None:
        for sid in sorted(_source_ids(data)):
            if not (R2_ID.match(sid) or R4_ID.match(sid) or R5_ID.match(sid)):
                errs.append(f"malformed evidence id {sid!r}")
            elif sid not in idx:
                errs.append(f"evidence id {sid!r} does not resolve to a page that was read")
    return errs


# ---- sequences: a whole route, raw to plate -------------------------------------------

def _is_heat(op: str, cat: o.Catalogue) -> bool:
    return "thermal" in (cat.operations.get(op, {}).get("categories") or [])


def subtree(r: Route, aid: str) -> list[str]:
    """Every material, assembly and addition an assembly joins, nested ones included."""
    asms = r.spec.get("assemblies") or {}
    out: list[str] = []
    todo = list(_members(asms.get(aid) or {}))
    while todo:
        x = todo.pop(0)
        if x in out:
            continue
        out.append(x)
        if x in asms:
            todo += _members(asms[x])
    return out


def _split(address: str) -> tuple[str, int]:
    owner, index = address.rsplit("/", 2)[-2:]
    return owner, int(index)


def _feeds(r: Route, a: str, b: str) -> bool:
    """Is step `a` upstream of step `b` in the route (walk order aside)?"""
    owner, idx = _split(a)
    todo, _ = _downstream(r, owner, idx - 1)
    return any(p.address == b for p in todo)


def sequence_errors(key: str, seq: dict, voc: dict, cat: o.Catalogue) -> list[str]:
    """A sequence is a whole documented route: every step has an endpoint that
    says readiness or doneness (with sources, or `by: route_order` when only the
    route's own order says so), every heat step after a join names an endpoint for
    each material it holds, and every link points at steps of this route."""
    errs: list[str] = []
    where = f"sequence {key}"
    _keys(errs, where, seq, "sequence")
    r = routes().get(key)
    if r is None:
        return errs + [f"{where}: not a documented route or modelled transfer"]
    steps = seq.get("steps") or {}
    addrs = [p.address for p in r.points]
    for a in steps:
        if a not in addrs:
            errs.append(f"{where}: step {a!r} is not in the route")
    kinds = []
    for p in r.points:
        st = steps.get(p.address)
        if st is None:
            errs.append(f"{where}: step {p.address} ({p.op}) is missing: a sequence is the "
                        f"whole route")
            continue
        _fields_errors(errs, f"{where} {p.address}", st, voc, "seqstep")
        ep = st.get("endpoint") or {}
        _keys(errs, f"{where} {p.address} endpoint", ep, "endpoint")
        _in(errs, f"{where} {p.address} endpoint", ep.get("kind"), voc.get("endpoint", []))
        kinds.append(ep.get("kind"))
        if not ep.get("sources") and ep.get("by") != "route_order":
            errs.append(f"{where} {p.address}: endpoint kind needs sources or by: route_order")
    if "doneness" not in kinds:
        errs.append(f"{where}: no step ends in doneness (nothing reaches the plate)")
    members = seq.get("members") or {}
    mats = r.spec.get("materials") or {}
    for p in r.points:
        if p.kind != "assembly" or not _is_heat(p.op, cat):
            continue
        inside = subtree(r, p.owner)
        got = members.get(p.address)
        if got is None:
            errs.append(f"{where}: heat after the join at {p.address} has no member endpoints")
            continue
        for m in inside:
            if m in mats and m not in got:
                errs.append(f"{where}: {p.address} names no endpoint for member {m}")
        for m, spec in got.items():
            if m not in inside:
                errs.append(f"{where}: {p.address}: {m!r} is not inside {p.owner}")
            _keys(errs, f"{where} {p.address} member {m}", spec or {}, "member")
            for kind in ("completion", "failure"):
                for i, ch in enumerate((spec or {}).get(kind) or []):
                    _keys(errs, f"{where} {p.address} member {m} {kind} {i + 1}", ch, "check")
                    _cited(errs, f"{where} {p.address} member {m} {kind} {i + 1}", ch)
    for a in members:
        pt = r.point(*_split(a)) if a in addrs else None
        if pt is None or pt.kind != "assembly":
            errs.append(f"{where}: members given for {a!r}, which is not a join step here")
    for i, d in enumerate(seq.get("depends") or []):
        w = f"{where} depends {i + 1}"
        _keys(errs, w, d, "depend")
        _cited(errs, w, d)
        for k in ("step", "because"):
            if d.get(k) not in addrs:
                errs.append(f"{w}: {k} {d.get(k)!r} is not a step of this route")
        if d.get("step") in addrs and d.get("because") in addrs and \
                not _feeds(r, d["step"], d["because"]):
            errs.append(f"{w}: {d['because']} does not follow {d['step']} in the route")
    for i, m in enumerate(seq.get("misses") or []):
        w = f"{where} misses {i + 1}"
        _keys(errs, w, m, "miss")
        _cited(errs, w, m)
        _in(errs, w, m.get("when"), voc.get("miss", []))
        if m.get("step") not in addrs:
            errs.append(f"{w}: step {m.get('step')!r} is not a step of this route")
    for i, a in enumerate(seq.get("alternatives") or []):
        w = f"{where} alternative {i + 1}"
        _keys(errs, w, a, "alternative")
        _cited(errs, w, a)
        if a.get("route") is not None and a["route"] not in routes():
            errs.append(f"{w}: route {a['route']!r} is not documented")
    for i, f in enumerate(seq.get("finish") or []):
        w = f"{where} finish {i + 1}"
        _keys(errs, w, f, "finish")
        sub = {k: f[k] for k in ("elapsed", "active", "completion", "failure") if k in f}
        _fields_errors(errs, w, sub, voc)
    return errs


def sequence(key: str) -> dict | None:
    return (load().get("sequences") or {}).get(key)


def _route_key(address: str) -> str:
    m = STEP.match(address)
    if not m:
        return ""
    return f"transfer:{m['tid']}" if m["tid"] else f"{m['dish']}/{m['route']}"


def endpoint_kind(address: str) -> str | None:
    """readiness | doneness for a step of a recorded sequence, else None."""
    st = ((sequence(_route_key(address)) or {}).get("steps") or {}).get(address) or {}
    return (st.get("endpoint") or {}).get("kind")


@dataclass
class History:
    member: str
    lines: list               # (point, step fields, endpoint kind, member endpoint or None)


def step_fields(address: str) -> dict:
    """Everything recorded for one step: each attached pair's default and its
    `at` entry, then the sequence's own fields for the step on top."""
    out: dict = {}
    for x in for_step(address):
        out.update(x["fields"])
    st = ((sequence(_route_key(address)) or {}).get("steps") or {}).get(address) or {}
    out.update({k: v for k, v in st.items() if k != "endpoint"})
    return out


def histories(key: str) -> list[History]:
    """Each material of the route from raw to plate: its own steps, then every
    join it enters and the heat after it, with this member's endpoint there."""
    r = routes()[key]
    seq = sequence(key) or {}
    steps = seq.get("steps") or {}
    members = seq.get("members") or {}
    out = []
    for mid in (r.spec.get("materials") or {}):
        lines = []
        todo, _ = _downstream(r, mid, 0)
        for p in todo:
            st = steps.get(p.address) or {}
            mine = (members.get(p.address) or {}).get(mid) if p.kind == "assembly" else None
            lines.append((p, step_fields(p.address), (st.get("endpoint") or {}).get("kind"),
                          mine))
        out.append(History(mid, lines))
    return out


# ---- query 1: the conditions of a step ---------------------------------------------------

def pairs_for_step(address: str) -> list[str]:
    return [pid for pid, p in load()["pairs"].items() if address in (p.get("steps") or [])]


def for_step(address: str) -> list[dict]:
    """For each pair attached to this step: the pair's default fields with the
    step's own fields on top (a field the step states replaces the default's)."""
    out = []
    for pid in pairs_for_step(address):
        p = load()["pairs"][pid]
        merged = dict(p.get("default") or {})
        merged.update((p.get("at") or {}).get(address) or {})
        st = ((sequence(_route_key(address)) or {}).get("steps") or {}).get(address) or {}
        merged.update({k: v for k, v in st.items() if k != "endpoint"})
        out.append({"pair": pid, "name": p.get("name"), "op": p.get("op"),
                    "part": p.get("part"), "confidence": p.get("confidence"),
                    "fields": merged, "conflicts": p.get("conflicts") or [],
                    "gaps": p.get("gaps") or []})
    return out


def for_pair(pid: str) -> dict | None:
    return load()["pairs"].get(pid)


def pairs_for_part(query: str) -> list[str]:
    """Pairs whose part is this ingredient or ingredient.part."""
    out = []
    for pid, p in load()["pairs"].items():
        part = p.get("part") or ""
        if part == query or part.partition(".")[0] == query:
            out.append(pid)
    return out


# ---- query 2: from a state you already have ----------------------------------------------

@dataclass
class Match:
    route: str
    name: str
    owner: str
    at: int                     # steps of `owner` already done (0: the raw part)
    remaining: list             # Points still to do, in order
    needs: list                 # (assembly, other members it joins)
    kind: str | None = None     # readiness | doneness of the last step done, if recorded


@dataclass
class FromState:
    part: str
    tokens: list
    state: o.Material | None
    problems: list = field(default_factory=list)
    matches: list = field(default_factory=list)
    keeps: list = field(default_factory=list)     # (intermediate id, keep entries)


def _members(spec: dict) -> list[str]:
    out = []
    for raw in (spec.get("roles") or {}).values():
        out += [m["use"] for m in c._members(raw)]
    return out


def _downstream(r: Route, owner: str, after: int) -> tuple[list, list]:
    """Remaining steps once `owner` has done `after` of its own steps: the rest of
    its steps, then each assembly it feeds (with that assembly's steps), up to the
    route's result. Also the other members each of those assemblies joins."""
    mats = r.spec.get("materials") or {}
    asms = r.spec.get("assemblies") or {}
    todo = [p for p in r.points if p.owner == owner and p.index > after]
    needs = []
    cur, seen = owner, {owner}
    while True:
        users = [aid for aid, spec in asms.items() if cur in _members(spec)]
        users += [mid for mid, spec in mats.items()
                  if isinstance(spec.get("from"), dict) and spec["from"].get("material") == cur
                  and mid not in seen and any(mid in _members(s) for s in asms.values())]
        users = [u for u in users if u not in seen]
        if not users:
            break
        cur = users[0]
        seen.add(cur)
        if cur in asms:
            needs.append((cur, [m for m in _members(asms[cur]) if m not in seen]))
        todo += [p for p in r.points if p.owner == cur]
    return todo, needs


def _state(part: str, tokens: list, cat: o.Catalogue) -> tuple[o.Material | None, list, list]:
    """The material you have: the part with the named R1 operations applied in
    order (the main output, as a route keeps it). Tokens that are not operations
    are state flags (`soaked`, `blanched`, `key=value`) checked on the match."""
    problems, flags = [], []
    ing, _, name = part.partition(".")
    starts = o.start_materials(ing, name, cat) if ing in cat.parts else []
    if not starts:
        return None, [f"no part {part!r}"], []
    m = starts[0]
    by_en = {spec["en"].split(",")[0].strip(): op for op, spec in cat.operations.items()}
    for tok in tokens:
        op = tok if tok in cat.operations else by_en.get(tok.replace("_", " "))
        if op is None:
            key, _, val = tok.partition("=")
            flags.append((key, val if val else True))
            continue
        outs = o.apply(op, m, cat)
        names = [x.path[-1].output for x in outs]
        if not outs:
            problems.append(f"{op} has no output")
            return None, problems, flags
        m = outs[names.index("main")] if "main" in names else outs[0]
    return m, problems, flags


def _flag_ok(m: o.Material, flags: list) -> bool:
    for key, want in flags:
        have = m.props.get(key)
        if want is True:
            if not have:
                return False
        elif str(have) != str(want):
            return False
    return True


def from_state(part: str, tokens: list | tuple = ()) -> FromState:
    """Documented routes and transfers that pass through a state equivalent to
    the one you have (R1 `Material.key()`), and what remains from there."""
    cat = o.load()
    if STEP.match(part):
        return _from_step(part)
    m, problems, flags = _state(part, list(tokens), cat)
    res = FromState(part, list(tokens), m, problems)
    if m is None:
        return res
    has_ops = len(flags) < len(tokens)
    for key, r in routes().items():
        found: dict = {}                  # owner -> the furthest step at an equivalent state
        for p in r.points:
            if p.kind != "material":
                continue
            for at, state in ((p.index - 1, p.before), (p.index, p.after)):
                if state is None or (state.ingredient, state.part) != (m.ingredient, m.part):
                    continue
                if (has_ops or not flags) and state.key() != m.key():
                    continue
                if flags and not _flag_ok(state, flags):
                    continue
                # the same state sits after step i and before step i + 1: with
                # operations named, take the furthest; with flags only, the first
                # step at which the flags hold (a flag such as `soaked` persists)
                prev = found.get(p.owner)
                found[p.owner] = at if prev is None else (max(prev, at) if has_ops
                                                          else min(prev, at))
        for owner, at in found.items():
            todo, needs = _downstream(r, owner, at)
            kind = endpoint_kind(f"{key}/{owner}/{at}") if at else None
            res.matches.append(Match(key, r.name, owner, at, todo, needs, kind))
    for iid, it in (load().get("intermediates") or {}).items():
        if it.get("at") or it.get("part") != part:
            continue
        im, _, _ = _state(part, list(it.get("after") or []), cat)
        if im is not None and im.key() == m.key() and _flag_ok(im, flags):
            res.keeps.append((iid, it))
    return res


def _from_step(address: str) -> FromState:
    """From the state a documented step leaves (an assembly such as a rested paste,
    or any material step): the rest of that route."""
    pt = resolve_step(address)
    res = FromState(address, [], pt.after if pt else None)
    if pt is None:
        res.problems.append(f"no step {address!r}")
        return res
    key = _route_key(address)
    r = routes()[key]
    todo, needs = _downstream(r, pt.owner, pt.index)
    res.matches.append(Match(key, r.name, pt.owner, pt.index, todo, needs,
                             endpoint_kind(address)))
    for iid, it in (load().get("intermediates") or {}).items():
        if it.get("at") == address:
            res.keeps.append((iid, it))
    return res


# ---- rendering ---------------------------------------------------------------------------

def _src(obj: dict) -> str:
    return f" [{', '.join(obj.get('sources') or [])}]" if obj.get("sources") else ""


def _time(e: dict) -> str:
    lo, hi, unit = e.get("min"), e.get("max"), e.get("unit", "")
    if unit in ("days", "months") and (hi if hi is not None else lo) == 1:
        unit = unit[:-1]
    if lo is not None and hi is not None:
        span = f"{lo}-{hi} {unit}" if lo != hi else f"{lo} {unit}"
    elif lo is not None:
        span = f"at least {lo} {unit}"
    elif hi is not None:
        span = f"at most {hi} {unit}"
    else:
        span = ""
    label = e.get("label") or ""
    if span and label and set(re.findall(r"\d+(?:\.\d+)?", span)) <= \
            set(re.findall(r"\d+(?:\.\d+)?", label)):
        return label                 # the label already says it ("at least 15 min")
    return ", ".join(x for x in (span, label) if x)


def _fields_lines(f: dict, indent: str = "    ") -> list[str]:
    out = []
    if f.get("role"):
        out.append(f"{indent}role: {f['role']}")
    s = f.get("start")
    if s:
        bits = [f"{k} {', '.join(v) if isinstance(v, list) else v}"
                for k, v in s.items() if k in ("particle", "moisture")]
        out.append(f"{indent}start: {'; '.join(bits)}{_src(s)}")
    for m in f.get("medium") or []:
        bits = [m["medium"].replace("_", " ")]
        if m.get("temp_c"):
            lo, hi = m["temp_c"]
            bits.append(f"{lo}-{hi} C" if lo != hi else f"{lo} C")
        if m.get("cover"):
            bits.append(m["cover"].replace("_", " "))
        if m.get("note"):
            bits.append(" ".join(str(m["note"]).split()))
        out.append(f"{indent}medium: {'; '.join(bits)}{_src(m)}")
    for e in f.get("elapsed") or []:
        out.append(f"{indent}elapsed: {_time(e)}{_src(e)}"
                   + (f" ({' '.join(str(e['note']).split())})" if e.get("note") else ""))
    a = f.get("active")
    out.append(f"{indent}active work: "
               + (f"{a['kind']}{_src(a)}" + (f" ({' '.join(str(a['note']).split())})"
                                             if a.get("note") else "") if a else "unknown"))
    for s in f.get("shifts") or []:
        out.append(f"{indent}time shifts with {s['factor']}: {s.get('effect', '')}{_src(s)}")
    done = f.get("completion") or []
    out.append(f"{indent}done when:" + ("" if done else " unknown"))
    out += [f"{indent}  - {' '.join(ch['check'].split())}{_src(ch)}" for ch in done]
    bad = f.get("failure") or []
    out.append(f"{indent}failed if:" + ("" if bad else " unknown"))
    for ch in bad:
        cause = f" <- {' '.join(ch['cause'].split())}" if ch.get("cause") else ""
        out.append(f"{indent}  - {' '.join(ch['check'].split())}{cause}{_src(ch)}")
    if f.get("note"):
        out.append(f"{indent}note: {' '.join(str(f['note']).split())}")
    return out


def render_pair(pid: str) -> str:
    p = for_pair(pid)
    if p is None:
        return f"No pair {pid!r}. Known: {', '.join(pair_ids())}.\n"
    ops = " / ".join(_ops(p))
    out = [f"{p.get('name', pid)}: {p.get('part')} -> {ops} [{p.get('confidence')}]"]
    out.append("  default (where the sources agree):")
    out += _fields_lines(p.get("default") or {})
    for addr in p.get("steps") or []:
        pt = resolve_step(addr)
        out.append(f"  at {addr}" + (f": {' '.join(pt.evidence.split())}" if pt and pt.evidence else ""))
        here = (p.get("at") or {}).get(addr)
        if here:
            out += _fields_lines(here, "      ")
    for cf in p.get("conflicts") or []:
        out.append(f"  conflict: {cf['topic']}")
        for v in cf.get("versions") or []:
            out.append(f"    - {' '.join(v['says'].split())}{_src(v)}")
    for g in p.get("gaps") or []:
        out.append(f"  not found: {' '.join(str(g).split())}")
    return "\n".join(out) + "\n"


def render_step(address: str) -> str:
    pt = resolve_step(address)
    if pt is None:
        return f"No step {address!r}.\n"
    out = [f"{address}: {c._en(pt.op) if pt.op in o.load().operations else pt.op}"
           + (f" ({' '.join(pt.evidence.split())})" if pt.evidence else "")]
    found = for_step(address)
    if not found:
        out.append("  no documented conditions recorded for this step")
    for x in found:
        out.append(f"  pair {x['pair']} [{x['confidence']}]")
        out += _fields_lines(x["fields"])
        for cf in x["conflicts"]:
            out.append(f"    conflict: {cf['topic']}")
            for v in cf.get("versions") or []:
                out.append(f"      - {' '.join(v['says'].split())}{_src(v)}")
    return "\n".join(out) + "\n"


def render_route(key: str) -> str:
    r = routes().get(key)
    if r is None:
        keys = [k for k in routes() if k.split("/")[0] == key]
        if not keys:
            return f"No route {key!r}.\n"
        return "".join(render_route(k) + "\n" for k in keys)
    if sequence(key) is not None:
        return render_sequence(key)
    out = [f"{r.name} ({key}): steps with documented conditions"]
    for p in r.points:
        pids = pairs_for_step(p.address)
        if pids:
            out.append(f"  {p.owner} {p.index} {p.op}: {', '.join(pids)}")
            for x in for_step(p.address):
                f = x["fields"]
                done = "; ".join(" ".join(ch["check"].split()) for ch in f.get("completion") or [])
                bad = "; ".join(" ".join(ch["check"].split()) for ch in f.get("failure") or [])
                times = "; ".join(_time(e) for e in f.get("elapsed") or [])
                act = (f.get("active") or {}).get("kind", "unknown")
                out.append(f"      time: {times or 'unknown'}; active: {act}")
                out.append(f"      done when: {done or 'unknown'}")
                out.append(f"      failed if: {bad or 'unknown'}")
    if len(out) == 1:
        out.append("  none recorded")
    return "\n".join(out) + "\n"


def _checks(chs: list) -> str:
    out = []
    for ch in chs or []:
        cause = f" <- {' '.join(ch['cause'].split())}" if ch.get("cause") else ""
        out.append(f"{' '.join(ch['check'].split())}{cause}{_src(ch)}")
    return "; ".join(out)


def render_sequence(key: str) -> str:
    """A whole route, member by member, raw to plate: every step with its endpoint
    kind and checks, the heat after each join with this member's endpoint, then the
    documented dependencies, failures of skipped or overdone stages, finishing
    stages and alternative sequences."""
    r = routes().get(key)
    seq = sequence(key)
    if r is None or seq is None:
        return f"No sequence {key!r}.\n"
    out = [f"{seq.get('name') or r.name} ({key}): the whole sequence, raw to plate"]
    for h in histories(key):
        out.append(f"  {h.member}:")
        for p, st, kind, mine in h.lines:
            name = c._en(p.op) if p.op in o.load().operations else p.op
            times = "; ".join(_time(e) + _src(e) for e in st.get("elapsed") or [])
            act = (st.get("active") or {}).get("kind")
            head = f"    {p.owner} {p.index} {name} -> {kind or 'endpoint unknown'}"
            extra = ", ".join(x for x in (times, f"active {act}" if act else "") if x)
            out.append(head + (f" ({extra})" if extra else ""))
            if p.owner == h.member or mine is None:
                done, bad = _checks(st.get("completion")), _checks(st.get("failure"))
            else:
                done, bad = _checks(mine.get("completion")), _checks(mine.get("failure"))
                out.append(f"      {h.member} inside {p.owner}:")
            if done:
                out.append(f"      done when: {done}")
            if bad:
                out.append(f"      failed if: {bad}")
            if p.owner != h.member and mine is not None and not (done or bad):
                out.append(f"      not found: {' '.join(str(mine.get('note', '')).split())}")
    for d in seq.get("depends") or []:
        out.append(f"  depends: {d['step']} exists because of {d['because']}: "
                   f"{' '.join(d['says'].split())}{_src(d)}")
    for m in seq.get("misses") or []:
        out.append(f"  if {m['step']} is {m['when']}: {' '.join(m['failure'].split())}{_src(m)}")
    for f in seq.get("finish") or []:
        times = "; ".join(_time(e) + _src(e) for e in f.get("elapsed") or [])
        out.append(f"  then {f['stage']}" + (f" ({times})" if times else "")
                   + (f": done when {_checks(f.get('completion'))}" if f.get("completion") else ""))
    for a in seq.get("alternatives") or []:
        out.append(f"  alternative sequence {a.get('name', '')}"
                   + (f" ({a['route']})" if a.get("route") else "")
                   + f": {' '.join(a['says'].split())}{_src(a)}")
    for g in seq.get("gaps") or []:
        out.append(f"  evidence stops: {' '.join(str(g).split())}")
    return "\n".join(out) + "\n"


def render(query: str | None = None) -> str:
    """`foodprep conditions [pair | ingredient[.part] | dish[/route] | transfer:<id> | step]`."""
    if not query:
        out = ["Documented processing conditions (R5): pair, part, operation, steps, "
               "completion/failure checks, confidence", ""]
        for pid, p in load()["pairs"].items():
            fs = [p.get("default") or {}] + list((p.get("at") or {}).values())
            nc = sum(len(f.get("completion") or []) for f in fs)
            nf = sum(len(f.get("failure") or []) for f in fs)
            out.append(f"{pid:26} {p.get('part', ''):28} {' / '.join(_ops(p)):22} "
                       f"{len(p.get('steps') or []):2} step(s)  done {nc:2}  failed {nf:2}  "
                       f"{p.get('confidence')}")
        return "\n".join(out) + "\n"
    if query in load()["pairs"]:
        return render_pair(query)
    if STEP.match(query):
        return render_step(query)
    pids = pairs_for_part(query)
    if pids:
        return "\n".join(render_pair(pid) for pid in pids)
    return render_route(query)


def render_from(part: str, tokens: list | tuple = ()) -> str:
    res = from_state(part, tokens)
    if STEP.match(part):
        if res.problems:
            return f"No state: {'; '.join(res.problems)}.\n"
        pt = resolve_step(part)
        return _render_matches(res, [f"From {part} ({c._en(pt.op) if pt.op in o.load().operations else pt.op} done):"])
    if res.state is None:
        return f"No state: {'; '.join(res.problems)}.\n"
    have = " -> ".join([c._en(s.operation) for s in res.state.path]
                       + [k if v is True else f"{k}={v}" for k, v in _state(part, res.tokens,
                                                                             o.load())[2]])
    have = have or "as bought"
    out = [f"From {part} ({have}): {len(res.matches)} documented route(s) pass through "
           f"an equivalent state"]
    return _render_matches(res, out)


def _render_matches(res: FromState, out: list) -> str:
    for iid, it in res.keeps:
        for k in it.get("keeps") or []:
            span = _time(k)
            out.append(f"  keeps: {k.get('where', '')}"
                       + (f", {' '.join(k['how'].split())}" if k.get("how") else "")
                       + (f", {span}" if span else "") + f" ({k['basis'].replace('_', ' ')})"
                       + _src(k))
    for mt in res.matches:
        out.append(f"  {mt.name} ({mt.route}): {mt.owner} after {mt.at} step(s); remaining:")
        if mt.kind == "readiness":
            out.append("    ! what you have is a readiness state: ready for the next "
                       "operation, not ready to eat")
        seq = sequence(mt.route) or {}
        for p in mt.remaining:
            pids = pairs_for_step(p.address)
            name = c._en(p.op) if p.op in o.load().operations else p.op
            kind = endpoint_kind(p.address)
            out.append(f"    {p.owner} {p.index} {name}"
                       + (f" -> {kind}" if kind else "")
                       + (f"  [conditions: {', '.join(pids)}]" if pids else ""))
            f = step_fields(p.address)
            times = "; ".join(_time(e) for e in f.get("elapsed") or [])
            act = (f.get("active") or {}).get("kind")
            if times or act:
                out.append(f"      time: {times or 'unknown'}; active work: {act or 'unknown'}")
            if f.get("completion") and p.owner == mt.owner:
                out.append(f"      done when: {_checks(f['completion'])}")
            mine = ((seq.get("members") or {}).get(p.address) or {}).get(mt.owner)
            if mine and (mine.get("completion") or mine.get("failure")):
                out.append(f"      {mt.owner} inside: done when {_checks(mine.get('completion')) or 'unknown'}"
                           + (f"; failed if {_checks(mine.get('failure'))}"
                              if mine.get("failure") else ""))
        later = {p.address for p in mt.remaining}
        for d in seq.get("depends") or []:
            if d["because"] in later:
                out.append(f"    why: {d['step']} -> {d['because']}: "
                           f"{' '.join(d['says'].split())}{_src(d)}")
        for f in seq.get("finish") or []:
            times = "; ".join(_time(e) for e in f.get("elapsed") or [])
            out.append(f"    then {f['stage']}" + (f" ({times})" if times else ""))
        for aid, others in mt.needs:
            if others:
                out.append(f"    {aid} also joins: {', '.join(others)}")
    if not res.matches:
        out.append("  no documented route passes through this state")
    return "\n".join(out) + "\n"
