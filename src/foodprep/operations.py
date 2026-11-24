"""Culinary operations: applicability, outputs and bounded operation sequences.

Culinary Operations R1 (docs/research/r1-culinary-operations/). Operations are
defined once, independent of ingredients, in data/operations.yaml. A material
is a part of an ingredient (data/part_properties.yaml) plus what has been done
to it. This module:

- assesses whether an operation applies to a material, and why
  (applicable / conditional / inapplicable / unknown / unsafe);
- applies an operation, producing one or more output materials with updated
  properties (peeling gives the peeled body AND the peel);
- explores bounded sequences of operations (depth 3), merging equivalent
  materials and keeping the reasons for every step;
- names the culinary functions of a material and ranks sequences by
  transparent criteria.

It reads the same YAML as the rest of the model and writes nothing. Generated
sequences are hypotheses: they are never added to the ontology. A sequence that
is tested and works can later be curated as transformations with
`input_component` (chains) and `byproducts` (several outputs).

Unknown is not false: a requirement on a property the material does not state
makes the result `unknown`, except for the flags operations.yaml lists under
`recorded_only_when_true`.
"""

from __future__ import annotations

from collections import Counter, deque
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

from foodprep import pair_counts as pc

DATA = Path(__file__).with_name("data")
STATUSES = ("applicable", "conditional", "inapplicable", "unknown", "unsafe")
TAKEN = ("applicable", "conditional")
MAX_DEPTH = 3
LAYER_KEYS = ("outer_layer", "seed_core")
# Processing states a fraction keeps from the material it was separated from.
STATE_FLAGS = ("cooked", "blanched", "browned", "salted", "smoked", "pickled", "fermented",
               "coated", "glazed", "concentrated", "cut")


# ---- loading ------------------------------------------------------------------

@dataclass(frozen=True)
class Catalogue:
    operations: dict
    scales: dict
    default_false: frozenset
    ordinary: frozenset
    functions: dict
    parts: dict          # ingredient -> part -> properties (+ edible, not_food_reason)


@lru_cache(maxsize=1)
def load() -> Catalogue:
    data = pc.load_yaml(DATA / "operations.yaml")
    props = pc.load_yaml(DATA / "part_properties.yaml")["parts"]
    edible = {(p["ingredient"], p["name"]): (str(p.get("edible", "yes")), p.get("not_food_reason"))
              for p in pc.load_yaml(DATA / "tomato.yaml").get("parts", [])}
    parts: dict = {}
    for ing, ps in props.items():
        for name, p in ps.items():
            e, why = edible.get((ing, name), ("yes", None))
            parts.setdefault(ing, {})[name] = {**(p or {}), "edible": e, "not_food_reason": why}
    return Catalogue(
        operations=data["operations"],
        scales=data["scales"],
        default_false=frozenset(data["recorded_only_when_true"]),
        ordinary=frozenset(data["ordinary_equipment"]),
        functions=data["functions"],
        parts=parts,
    )


# ---- materials ----------------------------------------------------------------

@dataclass(frozen=True)
class Step:
    operation: str
    output: str            # which output of the operation this path follows
    status: str            # applicable | conditional
    notes: tuple = ()
    siblings: tuple = ()   # the operation's other outputs (branches)
    terminal: bool = False # exhausted output; no sequence continues from it


@dataclass
class Material:
    ingredient: str
    part: str
    props: dict
    fraction: str | None = None
    kind: str = "part"     # part | fraction | geometry | state | composite
    edible: str = "yes"
    edible_reason: str | None = None
    adds: tuple = ()
    path: tuple = ()

    @property
    def name(self) -> str:
        base = f"{self.ingredient} {self.part}".replace("_", " ")
        if self.fraction:
            base += f" / {self.fraction.replace('_', ' ')}"
        return base

    def key(self) -> tuple:
        """Identity for merging: two paths that reach the same ingredient, part,
        fraction and properties (and added ingredients) made the same material.
        The cut's name (`form`) is left out: paysanne and thin slices that give
        the same piece, shape and thinness are the same material."""
        frozen = tuple(sorted((k, _freeze(v)) for k, v in self.props.items()
                              if k not in LAYER_KEYS and k not in ("note", "form")))
        return (self.ingredient, self.part, self.fraction, tuple(sorted(self.adds)), frozen)


def _freeze(v):
    if isinstance(v, list):
        return tuple(sorted(map(str, v)))   # flavour order does not make a new material
    if isinstance(v, dict):
        return tuple(sorted((k, _freeze(x)) for k, x in v.items()))
    return v


def start_materials(ingredient: str | None = None, part: str | None = None,
                    cat: Catalogue | None = None) -> list[Material]:
    cat = cat or load()
    out = []
    for ing, ps in cat.parts.items():
        if ingredient and ing != ingredient:
            continue
        for name, p in ps.items():
            if part and name != part:
                continue
            props = {k: v for k, v in p.items() if k not in ("edible", "not_food_reason")}
            out.append(Material(ing, name, props, edible=p["edible"],
                                edible_reason=p["not_food_reason"]))
    return out


# ---- property values and tests ---------------------------------------------------

def value(m: Material, key: str, cat: Catalogue | None = None):
    """(known, value) for a property, including derived ones."""
    cat = cat or load()
    p = m.props
    if key == "has_outer_layer":
        if key in p:
            return True, bool(p[key])
        return True, "outer_layer" in p
    if key == "outer_layer_toughness":
        if value(m, "has_outer_layer", cat)[1]:
            return ("toughness" in p["outer_layer"]), p["outer_layer"].get("toughness")
        return True, None
    if key == "has_seed_core":
        if key in p:
            return True, bool(p[key])
        return True, "seed_core" in p
    if key in p:
        return True, p[key]
    if key in cat.default_false:
        return True, False
    return False, None


def _scale(key: str, cat: Catalogue) -> list:
    return cat.scales["piece"] if key == "piece" else cat.scales["levels"]


def passes(key: str, have, want, cat: Catalogue | None = None) -> bool:
    cat = cat or load()
    if isinstance(want, bool):
        return bool(have) == want
    if isinstance(want, str):
        scale = _scale(key, cat)
        if want.startswith((">=", "<=")):
            if have not in scale:
                return False
            a, b = scale.index(have), scale.index(want[2:])
            return a >= b if want.startswith(">=") else a <= b
        if "|" in want:
            return have in want.split("|")
    return have == want


def holds(m: Material, cond: dict, cat: Catalogue | None = None) -> bool | None:
    """True / False, or None when a property it needs is unknown."""
    cat = cat or load()
    unknown = False
    for k, want in (cond or {}).items():
        known, have = value(m, k, cat)
        if not known:
            unknown = True
            continue
        if not passes(k, have, want, cat):
            return False
    return None if unknown else True


# ---- applicability ------------------------------------------------------------

@dataclass
class Assessment:
    operation: str
    status: str
    met: list = field(default_factory=list)       # why texts that hold
    failed: list = field(default_factory=list)    # why texts that do not
    unknown: list = field(default_factory=list)   # properties not stated
    notes: list = field(default_factory=list)     # conditions or safety

    def explain(self) -> str:
        if self.status == "applicable":
            return "; ".join(self.met) or "no requirements"
        if self.status == "conditional":
            return "; ".join(self.notes)
        if self.status == "unknown":
            return "unknown: " + ", ".join(self.unknown)
        if self.status == "unsafe":
            return "; ".join(self.notes)
        return "; ".join(self.failed)


def assess(op_id: str, m: Material, cat: Catalogue | None = None) -> Assessment:
    cat = cat or load()
    op = cat.operations[op_id]
    a = Assessment(op_id, "applicable")
    if m.edible == "no":
        reason = m.edible_reason or "not food"
        a.status = "unsafe" if "safe" in reason.lower() else "inapplicable"
        (a.notes if a.status == "unsafe" else a.failed).append(f"not food: {reason}")
        return a
    if f"{m.ingredient}.{m.part}" in (op.get("except") or []) and not m.fraction:
        a.status = "inapplicable"
        a.failed.append("a cook would not do this to this part (curated exception)")
        return a
    only = m.props.get("only_techniques")
    if only and not m.path:
        allowed = set(only) | set(m.props.get("only_operations") or [])
        if not ({op_id, op.get("generator_id"), op.get("technique")} & allowed):
            a.status = "inapplicable"
            a.failed.append("curated: this part is worth eating only as " + ", ".join(sorted(allowed)))
            return a
    for rule in op.get("unsafe_when") or []:
        if holds(m, rule["when"], cat):
            a.status = "unsafe"
            a.notes.append(rule["note"])
            return a
    for key, spec in (op.get("requires") or {}).items():
        test, why = (spec[0], spec[1]) if isinstance(spec, list) else (spec, key)
        waiver = spec[2] if isinstance(spec, list) and len(spec) > 2 else None
        waivers = waiver if isinstance(waiver, list) else [waiver] if waiver else []
        if any(holds(m, w, cat) for w in waivers):
            a.met.append(f"{why} (waived)")
            continue
        known, have = value(m, key, cat)
        if not known:
            a.unknown.append(key)
        elif passes(key, have, test, cat):
            if test is not False:      # a 'must not be X' rule explains failures only
                a.met.append(why)
        else:
            a.failed.append(why)
    if a.failed:
        a.status = "inapplicable"
        return a
    if a.unknown:
        a.status = "unknown"
        return a
    for rule in op.get("conditional") or []:
        if holds(m, rule["when"], cat):
            a.notes.append(rule["note"])
    for out in op.get("outputs") or []:
        layer = m.props.get(out.get("from", "self"))
        if isinstance(layer, dict) and layer.get("condition"):
            a.notes.append(layer["condition"])
    if a.notes:
        a.status = "conditional"
    return a


# ---- applying -----------------------------------------------------------------

def _shift(props: dict, key: str, by: int, cat: Catalogue) -> None:
    scale = _scale(key, cat)
    if props.get(key) in scale:
        i = max(0, min(len(scale) - 1, scale.index(props[key]) + by))
        props[key] = scale[i]


def apply(op_id: str, m: Material, cat: Catalogue | None = None) -> list[Material]:
    """The operation's output materials. Each records the step in its path."""
    cat = cat or load()
    op = cat.operations[op_id]
    a = assess(op_id, m, cat)
    outs = op.get("outputs") or []
    names = [o.get("name", "main") for o in outs]
    result = []
    for o, name in zip(outs, names):
        src = o.get("from", "self")
        fraction, edible, reason = m.fraction, m.edible, m.edible_reason
        if src == "self":
            props = {k: v for k, v in m.props.items()}
        else:
            layer = m.props.get(src)
            if not isinstance(layer, dict):
                continue
            props = {k: v for k, v in layer.items()
                     if k not in ("name", "edible", "inner_changes", "condition")}
            props.update({k: m.props[k] for k in STATE_FLAGS if m.props.get(k)})
            fraction = layer.get("name", src)
            edible = str(layer.get("edible", "yes"))
        if o.get("kind") == "fraction" and src == "self":
            fraction = name if not m.fraction else f"{m.fraction}_{name}"
        for k in LAYER_KEYS:
            if src != "self" or o.get("kind") == "fraction":
                props.pop(k, None)
        sets = dict(o.get("set") or {})
        if src == "self" and sets.get("has_outer_layer") is False and "outer_layer" in m.props:
            props.update(m.props["outer_layer"].get("inner_changes") or {})
            props.pop("outer_layer", None)
        if src == "self" and sets.get("has_seed_core") is False:
            props.pop("seed_core", None)
        props.update(sets)
        for k, n in (o.get("raise") or {}).items():
            _shift(props, k, n, cat)
        for k, n in (o.get("lower") or {}).items():
            _shift(props, k, -n, cat)
        if o.get("add_flavour"):
            props["flavour"] = list(dict.fromkeys(list(props.get("flavour") or [])
                                                  + o["add_flavour"]))
        if op.get("preparation") and o.get("kind") == "geometry":
            props["form"] = op["preparation"]
        probe = Material(m.ingredient, m.part, props, fraction)
        for ws in o.get("when_set") or []:
            if holds(probe, ws["when"], cat):
                props.update(ws["set"])
        adds = tuple(m.adds) + tuple(a for a in op.get("adds") or [] if a not in m.adds)
        kind = o.get("kind", "state")
        if adds and kind == "state":
            kind = "composite" if op.get("adds") else kind
        step = Step(op_id, name, a.status, tuple(a.notes),
                    tuple(n for n in names if n != name), bool(o.get("terminal")))
        result.append(Material(m.ingredient, m.part, props, fraction, kind, edible,
                               reason, adds, m.path + (step,)))
    return result


def changed(before: Material, after: Material) -> list[str]:
    keys = (set(before.props) | set(after.props)) - set(LAYER_KEYS) - {"note"}
    out = [k for k in sorted(keys) if before.props.get(k) != after.props.get(k)]
    if before.fraction != after.fraction:
        out.append("fraction")
    return out


# ---- functions ----------------------------------------------------------------

def functions(m: Material, cat: Catalogue | None = None) -> list[str]:
    cat = cat or load()
    if m.edible == "no":
        return []
    out = []
    for name, rule in cat.functions.items():
        if holds(m, rule.get("when", {}), cat) is not True:
            continue
        anyof = rule.get("when_any")
        if anyof and not any(holds(m, c, cat) is True for c in anyof):
            continue
        out.append(name)
    return out


def useful_functions(m: Material, cat: Catalogue | None = None) -> list[str]:
    """Functions that are a culinary use; waste reduction alone is not one."""
    return [f for f in functions(m, cat) if f != "waste_reduction"]


GROUP_WEIGHT = {"appearance": 0.5}


def usefulness(funcs: list[str], cat: Catalogue | None = None) -> float:
    """Distinct function groups, appearance at half weight, capped at 3, as 0..1.
    One liquid that is a broth base, an infusion and a colour scores two groups,
    not three functions."""
    cat = cat or load()
    groups = {cat.functions[f].get("group", f) for f in funcs}
    return min(sum(GROUP_WEIGHT.get(g, 1.0) for g in groups), 3) / 3


# ---- exploring ----------------------------------------------------------------

@dataclass
class Result:
    material: Material
    parent: Material | None = None                   # the material the last step started from
    alternates: list = field(default_factory=list)   # other paths to the same material

    @property
    def path(self) -> tuple:
        return self.material.path


@dataclass
class Exploration:
    starts: list
    results: list                 # Results, in discovery order
    stats: Counter                # generated, merged, pruned by reason
    unknown_props: Counter        # properties that blocked a step as unknown


def _cost(path: tuple, cat: Catalogue) -> tuple:
    """Which of two equivalent paths to show: fewer steps, less effort, fewer
    conditions."""
    return (len(path), sum(cat.operations[s.operation].get("effort", 1) for s in path),
            sum(1 for s in path if s.status == "conditional"))


def explore(ingredient: str | None = None, part: str | None = None,
            depth: int = MAX_DEPTH, cat: Catalogue | None = None) -> Exploration:
    """Breadth-first over operation sequences, deterministic, bounded by depth.

    A step is taken only when the operation is applicable or conditional, the
    operation is not already in the path, and the output differs from its input.
    Equivalent materials merge; the first (shortest) path is kept."""
    cat = cat or load()
    if depth < 1 or depth > MAX_DEPTH:
        raise ValueError(f"depth must be 1..{MAX_DEPTH}")
    ops = [k for k, op in cat.operations.items() if op.get("generator", True)]
    starts = start_materials(ingredient, part, cat)
    seen: dict[tuple, Result] = {}
    results: list[Result] = []
    stats: Counter = Counter()
    unknown: Counter = Counter()
    queue = deque((m, 0) for m in starts)
    for m in starts:
        seen[m.key()] = Result(m)
    while queue:
        m, d = queue.popleft()
        if d >= depth:
            continue
        used = {s.operation for s in m.path}
        for op_id in ops:
            if op_id in used:
                stats["pruned: operation already in path"] += 1
                continue
            a = assess(op_id, m, cat)
            if a.status not in TAKEN:
                stats[f"pruned: {a.status}"] += 1
                for k in a.unknown:
                    unknown[k] += 1
                continue
            for out in apply(op_id, m, cat):
                if not changed(m, out):
                    stats["pruned: no change"] += 1
                    continue
                stats["generated"] += 1
                k = out.key()
                if k in seen:
                    old = seen[k]
                    stats["merged: equivalent material"] += 1
                    if old.material.path and _cost(out.path, cat) < _cost(old.material.path, cat):
                        # keep the easiest path as the canonical one
                        old.alternates.append(old.material.path)
                        old.material.path = out.path
                        old.parent = m
                    else:
                        old.alternates.append(out.path)
                    continue
                r = Result(out, m)
                seen[k] = r
                results.append(r)
                if out.path[-1].terminal:
                    stats["ended: exhausted output"] += 1
                    continue
                queue.append((out, d + 1))
    return Exploration(starts, results, stats, unknown)


# ---- ranking -------------------------------------------------------------------

WEIGHTS = {"useful": 3.0, "difference": 1.0, "utilisation": 0.5, "experimental": 0.5,
           "effort": -1.0, "equipment": -0.5}


@dataclass
class Ranked:
    result: Result
    functions: list
    plausibility: float
    usefulness: float
    difference: float
    utilisation: float
    established: float
    experimental: float
    effort: float
    equipment: list
    score: float

    @property
    def evidence(self) -> str:
        return "established path" if self.established == 1.0 else "mechanistic inference"


def _origin(m: Material) -> str:
    return f"{m.ingredient}.{m.part}"


def rank(r: Result, start: Material, cat: Catalogue | None = None) -> Ranked | None:
    """Transparent scores. None (never ranked) when the material has no culinary
    function, when it is an exhausted output (spent solids), or when its last
    step adds no function its input did not already have: a longer path must
    earn its extra step."""
    cat = cat or load()
    m = r.material
    funcs = useful_functions(m, cat)
    if not funcs or r.path[-1].terminal:
        return None
    if r.parent is not None and r.parent.path and set(funcs) <= set(useful_functions(r.parent, cat)):
        return None
    ops = [cat.operations[s.operation] for s in r.path]
    plaus = 0.8 ** sum(1 for s in r.path if s.status == "conditional")
    useful = usefulness(funcs, cat)
    diff = min(len(changed(start, m)), 6) / 6
    discarded = bool(start.props.get("usually_discarded") or m.props.get("usually_discarded"))
    est = sum(1 for op in ops if _origin(m) in (op.get("established_on") or [])) / len(ops)
    experimental = useful * (1 - est)
    effort = sum(op.get("effort", 1) for op in ops) / 9
    equipment = sorted({e for op in ops for e in op.get("equipment") or []} - cat.ordinary)
    score = (WEIGHTS["useful"] * plaus * useful + WEIGHTS["difference"] * diff
             + WEIGHTS["utilisation"] * discarded + WEIGHTS["experimental"] * experimental
             + WEIGHTS["effort"] * effort + WEIGHTS["equipment"] * len(equipment))
    return Ranked(r, funcs, plaus, useful, diff, float(discarded), est, experimental,
                  effort, equipment, round(score, 3))


def ranked(ingredient: str, part: str | None = None, depth: int = MAX_DEPTH,
           cat: Catalogue | None = None) -> tuple[list[Ranked], Exploration]:
    cat = cat or load()
    ex = explore(ingredient, part, depth, cat)
    starts = {(s.ingredient, s.part): s for s in ex.starts}
    out = []
    for r in ex.results:
        rk = rank(r, starts[(r.material.ingredient, r.material.part)], cat)
        if rk:
            out.append(rk)
    out.sort(key=lambda x: (-x.score, len(x.result.path), describe_path(x.result.material)))
    return out, ex


def diverse(rs: list[Ranked], n: int) -> list[Ranked]:
    """The best n, at most one per (part, fraction, main function, last operation)
    and a fair share per starting part, so one part cannot fill the list."""
    parts = {x.result.material.part for x in rs}
    per_part = max(2, -(-n // max(len(parts), 1)))
    picked, keys, count = [], set(), Counter()
    for x in rs:
        m = x.result.material
        k = (m.part, m.fraction, x.functions[0], x.result.path[-1].operation)
        if k in keys or count[m.part] >= per_part:
            continue
        keys.add(k)
        count[m.part] += 1
        picked.append(x)
        if len(picked) == n:
            break
    return picked


# ---- rendering -----------------------------------------------------------------

def describe_path(m: Material) -> str:
    cat = load()
    bits = []
    for s in m.path:
        en = cat.operations[s.operation]["en"]
        bit = en if s.output in ("main", "inner", "flesh", "trimmed", "drained", "filtered",
                                 "fine", "passed", "coulis", "macerated", "clarified",
                                 "blades", "fronds", "shell") and not s.siblings else \
            f"{en} [{s.output}]"
        bits.append(bit)
    return " -> ".join(bits)


def render_applicability(ingredient: str, part: str | None = None) -> str:
    cat = load()
    starts = start_materials(ingredient, part, cat)
    if not starts:
        return f"No materials for {ingredient!r}. Known: {', '.join(sorted(cat.parts))}.\n"
    out = [f"Operations on {ingredient}: what applies, and why", ""]
    for m in starts:
        out.append(f"{m.part.replace('_', ' ').capitalize()}")
        by: dict[str, list] = {s: [] for s in STATUSES}
        for op_id, op in cat.operations.items():
            if op.get("generator", True) is False:
                continue
            a = assess(op_id, m, cat)
            by[a.status].append((op_id, op, a))
        for status in STATUSES:
            if not by[status]:
                continue
            out.append(f"  {status} ({len(by[status])})")
            for op_id, op, a in by[status]:
                out.append(f"    {op['fr']} ({op['en']}): {a.explain()}")
        out.append("")
    return "\n".join(out)


def render_explore(ingredient: str, part: str | None = None, top: int = 8) -> str:
    cat = load()
    if ingredient not in cat.parts:
        return f"No materials for {ingredient!r}. Known: {', '.join(sorted(cat.parts))}.\n"
    rs, ex = ranked(ingredient, part, cat=cat)
    s = ex.stats
    out = [f"Processing sequences for {ingredient} (depth {MAX_DEPTH}; hypotheses, not recipes)",
           f"{len(ex.results)} distinct materials from {s['generated']} generated steps; "
           f"{s['merged: equivalent material']} merged as equivalent; "
           f"{len(ex.results) - len(rs)} with no culinary function (noise).", ""]
    for x in diverse(rs, top):
        m = x.result.material
        out.append(f"{x.score:5.2f}  {m.name}: {describe_path(m)}")
        out.append(f"       functions: {', '.join(x.functions)}"
                   + ("; uses a usually discarded part" if x.utilisation else ""))
        out.append(f"       evidence: {x.evidence}; plausibility {x.plausibility:.2f}; "
                   f"effort {x.effort:.2f}"
                   + (f"; equipment: {', '.join(x.equipment)}" if x.equipment else ""))
        notes = [n for st in x.result.path for n in st.notes]
        if notes:
            out.append(f"       conditions: {'; '.join(dict.fromkeys(notes))}")
        safety = [cat.operations[st.operation].get("safety") for st in x.result.path]
        safety = [t for t in safety if t]
        if safety:
            out.append(f"       safety: {'; '.join(dict.fromkeys(safety))}")
        if x.result.alternates:
            out.append(f"       also reached by {len(x.result.alternates)} other path(s)")
    return "\n".join(out) + "\n"
