"""Documented constructions: real dishes from raw parts to their finished
structure (R3, docs/adr/0003-documented-constructions.md).

A dish in data/constructions.yaml has one or more routes. A route is:
- materials, each a part (or a fraction of another material) taken through R1
  operations from data/operations.yaml;
- assemblies, each an assembly operation (melanger, incorporer, farcir,
  envelopper, superposer, revetir) whose roles hold materials, other
  assemblies (nesting) or additions (ingredients used as they are), followed
  by further R1 steps on the assembled whole;
- a result, and the state documented practice says it ends in.

This module validates a route. It applies every step with
`operations.apply` and records whether the operation applies, checks every
role and every documented claim (`expects`, `final`) against the computed
states, derives the recombination links (a fraction of one material returned
into the same dish), and lists fractions nobody accounted for. It writes
nothing and generates nothing: there are no construction rules here, only
checks that recorded dishes are consistent with the operation model.

Quantities and conditions are `evidence` strings attached to the step or
relation they support. They are evidence for why the dish works, not a
recipe to follow.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

from foodprep import operations as o
from foodprep import pair_counts as pc

DATA = o.DATA
PATH = DATA / "constructions.yaml"
FREEZE_PATH = DATA / "construction_freeze.yaml"

# ---- the schema (frozen before the held-out dishes, see construction_freeze.yaml)

SCHEMA = {
    "dish": ["name", "tradition", "split", "routes", "note"],
    "route": ["recipes", "patterns", "holds_by", "water", "why", "materials", "assemblies",
              "result", "final", "gaps", "note"],
    "material": ["from", "steps", "recipes", "water", "note"],
    "source": ["material", "step", "output"],
    "step": ["op", "keep", "or", "discard", "recipes", "evidence", "expects", "optional", "note"],
    "assembly": ["op", "roles", "state", "because", "expects", "steps", "recipes", "holds_by",
                 "water", "evidence", "note"],
    "member": ["use", "recipes", "note", "water", "optional", "prep"],
    "expect": ["state", "member", "because", "recipes"],
    "final": ["state", "recipes", "evidence"],
    "gap": ["kind", "note"],
    "addition": ["catalogue", "shop", "props", "note"],
}
SPLITS = ("design", "held_out")
GAP_KINDS = ("model", "scope", "ingredient", "evidence")
RECIPE_ID = re.compile(r"^[EMA]\d+[a-z]$")
VERDICTS = ("fully", "partly", "not")


# ---- loading ---------------------------------------------------------------------

@lru_cache(maxsize=1)
def load() -> dict:
    return pc.load_yaml(PATH)


def dish_ids(split: str | None = None) -> list[str]:
    return [k for k, d in load()["dishes"].items() if split is None or d["split"] == split]


def assembly_ops(cat: o.Catalogue | None = None) -> dict:
    cat = cat or o.load()
    return {k: op for k, op in cat.operations.items() if op.get("assembly")}


def addition_material(aid: str, data: dict | None = None) -> o.Material:
    data = data or load()
    a = data["additions"][aid]
    return o.Material(aid, "addition", dict(a.get("props") or {}), kind="addition")


# ---- reports ---------------------------------------------------------------------

@dataclass
class StepCheck:
    owner: str            # material or assembly id
    index: int
    op: str
    status: str
    explain: str
    alternative: bool = False
    output: str = "main"


@dataclass
class RouteReport:
    dish: str
    route: str
    steps: list = field(default_factory=list)            # StepCheck
    errors: list = field(default_factory=list)           # the data is malformed
    failures: list = field(default_factory=list)         # the model disagrees
    unknowns: list = field(default_factory=list)         # a property is not stated
    claims: list = field(default_factory=list)           # (where, state, verdict) of expects/final
    recombinations: list = field(default_factory=list)   # (source, step, output, material)
    unaccounted: list = field(default_factory=list)      # fractions neither used nor discarded
    conventional: list = field(default_factory=list)     # usually_discarded fractions left unused
    model_gaps: list = field(default_factory=list)
    other_gaps: list = field(default_factory=list)
    result: o.Material | None = None
    states: dict = field(default_factory=dict)           # material/assembly id -> Material

    @property
    def verdict(self) -> str:
        if self.errors or self.result is None:
            return "not"
        if self.failures or self.unknowns or self.unaccounted or self.model_gaps:
            return "partly"
        return "fully"


# ---- validating -------------------------------------------------------------------

def _steps(raw) -> list[dict]:
    return [s if isinstance(s, dict) else {"op": s} for s in (raw or [])]


def _members(raw) -> list[dict]:
    if raw is None:
        return []
    raw = raw if isinstance(raw, list) else [raw]
    return [m if isinstance(m, dict) else {"use": m} for m in raw]


def _fields(rep: RouteReport, kind: str, where: str, obj) -> None:
    if not isinstance(obj, dict):
        return
    extra = set(obj) - set(SCHEMA[kind])
    if extra:
        rep.errors.append(f"{where}: unknown {kind} field(s) {sorted(extra)}")


def _recipes_ok(rep: RouteReport, where: str, ids, route_ids: set, required: bool) -> None:
    ids = ids or []
    if required and not ids:
        rep.errors.append(f"{where}: no recipe ids (every relationship must cite R2 recipes)")
    for r in ids:
        if not RECIPE_ID.match(str(r)):
            rep.errors.append(f"{where}: malformed recipe id {r!r}")
        elif route_ids and r not in route_ids:
            rep.errors.append(f"{where}: cites {r}, which the route does not list")


def _check_claims(rep: RouteReport, where: str, expects, before: dict, route_ids: set,
                  cat: o.Catalogue) -> None:
    """`expects` is a list of {state, member?, because, recipes}. `before` maps the
    ids a claim may name (`member`) to their states; key None is the step's input."""
    for i, e in enumerate(expects or []):
        _fields(rep, "expect", f"{where} expects[{i}]", e)
        if not e.get("because"):
            rep.errors.append(f"{where} expects[{i}]: no `because`")
        _recipes_ok(rep, f"{where} expects[{i}]", e.get("recipes"), route_ids, True)
        target = before.get(e.get("member"))
        if target is None:
            rep.errors.append(f"{where} expects[{i}]: unknown target {e.get('member')!r}")
            continue
        verdict = o.holds(target, e.get("state") or {}, cat)
        label = f"{where}" + (f" ({e['member']})" if e.get("member") else "")
        rep.claims.append((label, e.get("state"), verdict))
        if verdict is False:
            rep.failures.append(f"{label}: expected {e['state']} ({e['because']}), "
                                f"but the computed state disagrees")
        elif verdict is None:
            rep.unknowns.append(f"{label}: expected {e['state']}, a property is not stated")


def _run_steps(rep: RouteReport, owner: str, m: o.Material, steps: list[dict],
               route_ids: set, cat: o.Catalogue, outputs: dict) -> o.Material:
    """Apply R1 steps; record each output of each step in outputs[(owner, op)]."""
    for i, s in enumerate(steps):
        where = f"{owner} step {i + 1}"
        _fields(rep, "step", where, s)
        op = s.get("op")
        if op not in cat.operations:
            rep.errors.append(f"{where}: unknown operation {op!r}")
            return m
        if cat.operations[op].get("assembly"):
            rep.errors.append(f"{where}: {op} is an assembly operation; use an assembly")
            return m
        _recipes_ok(rep, where, s.get("recipes"), route_ids, False)
        _check_claims(rep, f"{where} ({op})", s.get("expects"), {None: m}, route_ids, cat)
        a = o.assess(op, m, cat)
        rep.steps.append(StepCheck(owner, i + 1, op, a.status, a.explain()))
        if a.status in ("inapplicable", "unsafe"):
            rep.failures.append(f"{where}: {op} is {a.status} ({a.explain()})")
        elif a.status == "unknown":
            rep.unknowns.append(f"{where}: {op} {a.explain()}")
        for alt in s.get("or") or []:
            if alt not in cat.operations:
                rep.errors.append(f"{where}: unknown alternative {alt!r}")
                continue
            b = o.assess(alt, m, cat)
            rep.steps.append(StepCheck(owner, i + 1, alt, b.status, b.explain(), True))
            if b.status in ("inapplicable", "unsafe"):
                rep.failures.append(f"{where}: alternative {alt} is {b.status} ({b.explain()})")
            elif b.status == "unknown":
                rep.unknowns.append(f"{where}: alternative {alt} {b.explain()}")
        outs = o.apply(op, m, cat)
        if not outs:
            rep.errors.append(f"{where}: {op} has no outputs")
            return m
        names = [x.path[-1].output for x in outs]
        keep = s.get("keep") or ("main" if "main" in names else names[0])
        if keep not in names:
            rep.errors.append(f"{where}: {op} has no output {keep!r} (has {names})")
            return m
        rep.steps[-1 - len(s.get("or") or [])].output = keep
        outputs.setdefault((owner, op), {}).update(dict(zip(names, outs)))
        for d in s.get("discard") or []:
            if d not in names:
                rep.errors.append(f"{where}: discards {d!r}, which {op} does not produce")
        outputs.setdefault(("_discarded", owner, op), set()).update(s.get("discard") or [])
        m = outs[names.index(keep)]
    return m


def validate_route(dish_id: str, route_id: str, cat: o.Catalogue | None = None,
                   data: dict | None = None) -> RouteReport:
    cat = cat or o.load()
    data = data or load()
    dish = data["dishes"][dish_id]
    route = dish["routes"][route_id]
    rep = RouteReport(dish_id, route_id)
    _fields(rep, "route", f"{dish_id}/{route_id}", route)
    route_ids = set(route.get("recipes") or [])
    _recipes_ok(rep, f"{dish_id}/{route_id}", route.get("recipes"), set(), True)
    for p in route.get("patterns") or []:
        if p not in data["patterns"]:
            rep.errors.append(f"unknown pattern {p!r}")
    for h in route.get("holds_by") or []:
        if h not in data["mechanisms"]:
            rep.errors.append(f"unknown mechanism {h!r}")
    for w in route.get("water") or []:
        if w not in data["water_routes"]:
            rep.errors.append(f"unknown water route {w!r}")
    for i, g in enumerate(route.get("gaps") or []):
        _fields(rep, "gap", f"gap {i}", g)
        if g.get("kind") not in GAP_KINDS:
            rep.errors.append(f"gap {i}: kind must be one of {GAP_KINDS}")
        (rep.model_gaps if g.get("kind") == "model" else rep.other_gaps).append(g.get("note"))
    if not route.get("why"):
        rep.errors.append("no `why`: say what holds the dish together")

    mats = route.get("materials") or {}
    asms = route.get("assemblies") or {}
    adds = data["additions"]
    clash = (set(mats) & set(asms)) | (set(mats) & set(adds)) | (set(asms) & set(adds))
    if clash:
        rep.errors.append(f"ids used twice: {sorted(clash)}")
    outputs: dict = {}
    computing: set = set()

    def material(mid: str) -> o.Material | None:
        if mid in rep.states:
            return rep.states[mid]
        if mid in computing:
            rep.errors.append(f"material {mid}: circular source")
            return None
        computing.add(mid)
        spec = mats[mid]
        _fields(rep, "material", f"material {mid}", spec)
        _recipes_ok(rep, f"material {mid}", spec.get("recipes"), route_ids, True)
        for w in spec.get("water") or []:
            if w not in data["water_routes"]:
                rep.errors.append(f"material {mid}: unknown water route {w!r}")
        src = spec.get("from")
        if isinstance(src, str):
            ing, _, part = src.partition(".")
            starts = o.start_materials(ing, part, cat) if ing in cat.parts else []
            if not starts:
                rep.errors.append(f"material {mid}: no part {src!r}")
                return None
            m = starts[0]
        elif isinstance(src, dict):
            _fields(rep, "source", f"material {mid} from", src)
            parent = src.get("material")
            if parent not in mats:
                rep.errors.append(f"material {mid}: unknown source material {parent!r}")
                return None
            if material(parent) is None:
                return None
            outs = outputs.get((parent, src.get("step"))) or {}
            if src.get("output") not in outs:
                rep.errors.append(f"material {mid}: {parent} has no output "
                                  f"{src.get('output')!r} at step {src.get('step')!r}")
                return None
            m = outs[src["output"]]
        else:
            rep.errors.append(f"material {mid}: `from` must be a part or a source")
            return None
        m = _run_steps(rep, mid, m, _steps(spec.get("steps")), route_ids, cat, outputs)
        rep.states[mid] = m
        computing.discard(mid)
        return m

    def resolve(ref: str) -> o.Material | None:
        if ref in mats:
            return material(ref)
        if ref in asms:
            return assembly(ref)
        if ref in adds:
            return addition_material(ref, data)
        rep.errors.append(f"unknown reference {ref!r}")
        return None

    def assembly(aid: str) -> o.Material | None:
        if aid in rep.states:
            return rep.states[aid]
        if aid in computing:
            rep.errors.append(f"assembly {aid}: circular nesting")
            return None
        computing.add(aid)
        spec = asms[aid]
        where = f"assembly {aid}"
        _fields(rep, "assembly", where, spec)
        _recipes_ok(rep, where, spec.get("recipes"), route_ids, True)
        op_id = spec.get("op")
        op = cat.operations.get(op_id) or {}
        block = op.get("assembly")
        if not block:
            rep.errors.append(f"{where}: {op_id!r} is not an assembly operation")
            return None
        roles = spec.get("roles") or {}
        members: dict = {}
        for role, raw in roles.items():
            rspec = block["roles"].get(role)
            if rspec is None:
                rep.errors.append(f"{where}: {op_id} has no role {role!r}")
                continue
            for mem in _members(raw):
                _fields(rep, "member", f"{where} {role}", mem)
                _recipes_ok(rep, f"{where} {role} {mem.get('use')}", mem.get("recipes"),
                            route_ids, False)
                m = resolve(mem.get("use"))
                if m is None:
                    continue
                members[mem["use"]] = m
                met, failed, unknown = o.check_requires(rspec.get("requires"), m, cat)
                for f in failed:
                    rep.failures.append(f"{where}: {mem['use']} as {role}: {f}")
                for k in unknown:
                    rep.unknowns.append(f"{where}: {mem['use']} as {role}: {k} unknown")
        for role, rspec in block["roles"].items():
            n = len(_members(roles.get(role)))
            if n < rspec.get("min", 0) or ("max" in rspec and n > rspec["max"]):
                rep.errors.append(f"{where}: role {role} has {n} member(s), "
                                  f"needs {rspec.get('min', 0)}..{rspec.get('max', 'n')}")
        carrier_ref = (_members(roles.get(block["carrier"])) or [{}])[0].get("use")
        carrier = members.get(carrier_ref)
        if carrier is None:
            rep.errors.append(f"{where}: no carrier ({block['carrier']})")
            return None
        _check_claims(rep, where, spec.get("expects"), members, route_ids, cat)
        props = dict(carrier.props)
        for out in op.get("outputs") or []:
            props.update(out.get("set") or {})
        if spec.get("state"):
            because = spec.get("because") or []
            if not because:
                rep.errors.append(f"{where}: `state` without `because`")
            for b in because:
                if b not in members:
                    rep.errors.append(f"{where}: because {b!r}, which is not a member")
            props.update(spec["state"])
        for w in spec.get("water") or []:
            if w not in data["water_routes"]:
                rep.errors.append(f"{where}: unknown water route {w!r}")
        for h in spec.get("holds_by") or []:
            if h not in data["mechanisms"]:
                rep.errors.append(f"{where}: unknown mechanism {h!r}")
        added = tuple(dict.fromkeys(a for mm in members.values() for a in
                                    ((mm.ingredient,) if mm.kind == "addition" else mm.adds)))
        m = o.Material(carrier.ingredient, carrier.part, props, carrier.fraction, "assembly",
                       carrier.edible, carrier.edible_reason, added, ())
        m = _run_steps(rep, aid, m, _steps(spec.get("steps")), route_ids, cat, outputs)
        rep.states[aid] = m
        computing.discard(aid)
        return m

    res = route.get("result")
    if res not in mats and res not in asms:
        rep.errors.append(f"result {res!r} is neither a material nor an assembly")
    else:
        rep.result = resolve(res)
    for mid in mats:          # materials the result does not reach still get checked
        material(mid)
    for aid in asms:
        assembly(aid)

    used = _reached(res, mats, asms)
    for mid in mats:
        if mid not in used:
            rep.errors.append(f"material {mid} does not reach the result")
    for aid in asms:
        if aid not in used:
            rep.errors.append(f"assembly {aid} does not reach the result")
    for mid, spec in mats.items():
        src = spec.get("from")
        if isinstance(src, dict) and src.get("material") in used and mid in used:
            rep.recombinations.append((src["material"], src.get("step"), src.get("output"), mid))
    taken = {(s["material"], s.get("step"), s.get("output")) for s in
             (spec.get("from") for spec in mats.values()) if isinstance(s, dict)}
    for (owner, *rest), outs in list(outputs.items()):
        if owner == "_discarded":
            continue
        op = rest[0]
        discarded = outputs.get(("_discarded", owner, op), set())
        kept = {sc.output for sc in rep.steps if sc.owner == owner and sc.op == op
                and not sc.alternative}
        for name in outs:
            if name in kept or name in discarded or (owner, op, name) in taken:
                continue
            if outs[name].props.get("usually_discarded"):
                rep.conventional.append(f"{owner}: {op} [{name}]")   # the model says cooks discard it
                continue
            rep.unaccounted.append(f"{owner}: {op} [{name}]")

    fin = route.get("final") or {}
    _fields(rep, "final", "final", fin)
    if not fin.get("state"):
        rep.errors.append("no `final` state: what does documented practice say it ends as?")
    _recipes_ok(rep, "final", fin.get("recipes"), route_ids, True)
    if rep.result is not None and fin.get("state"):
        v = o.holds(rep.result, fin["state"], cat)
        rep.claims.append(("final", fin["state"], v))
        if v is False:
            rep.failures.append(f"final: documented {fin['state']}, computed state disagrees")
        elif v is None:
            rep.unknowns.append(f"final: {fin['state']}, a property is not stated")
    return rep


def _reached(res: str, mats: dict, asms: dict) -> set:
    seen: set = set()
    todo = [res]
    while todo:
        x = todo.pop()
        if x in seen:
            continue
        seen.add(x)
        if x in asms:
            for raw in (asms[x].get("roles") or {}).values():
                todo += [m.get("use") for m in _members(raw)]
        elif x in mats and isinstance(mats[x].get("from"), dict):
            todo.append(mats[x]["from"].get("material"))
    return seen


@dataclass
class DishReport:
    dish: str
    routes: dict             # route id -> RouteReport

    @property
    def verdict(self) -> str:
        vs = [r.verdict for r in self.routes.values()]
        if all(v == "fully" for v in vs):
            return "fully"
        if all(v == "not" for v in vs):
            return "not"
        return "partly"


def validate(dish_id: str, cat: o.Catalogue | None = None) -> DishReport:
    cat = cat or o.load()
    data = load()
    dish = data["dishes"][dish_id]
    return DishReport(dish_id, {r: validate_route(dish_id, r, cat, data) for r in dish["routes"]})


def dish_errors(dish_id: str) -> list[str]:
    data = load()
    dish = data["dishes"][dish_id]
    out = [f"unknown dish field(s) {sorted(set(dish) - set(SCHEMA['dish']))}"] \
        if set(dish) - set(SCHEMA["dish"]) else []
    if dish.get("split") not in SPLITS:
        out.append(f"split must be one of {SPLITS}")
    if not dish.get("routes"):
        out.append("no routes")
    return out


def addition_errors() -> list[str]:
    data = load()
    cat_names = {i["canonical_name"] for i in pc.load_yaml(DATA / "tomato.yaml")["ingredients"]}
    out = []
    for aid, a in data["additions"].items():
        if set(a) - set(SCHEMA["addition"]):
            out.append(f"{aid}: unknown field(s) {sorted(set(a) - set(SCHEMA['addition']))}")
        c = a.get("catalogue")
        if c is not None and c not in cat_names:
            out.append(f"{aid}: catalogue ingredient {c!r} is not in tomato.yaml")
        if c is None and a.get("shop", True) and not a.get("note"):
            out.append(f"{aid}: not in the catalogue; say so in a note (a Lidl gap)")
    return out


# ---- what a dish uses (for the freeze) --------------------------------------------

def used_by(dish_id: str) -> dict:
    """Operations, parts, additions and property keys a dish relies on."""
    data = load()
    cat = o.load()
    ops, parts, adds = set(), set(), set()
    for route in data["dishes"][dish_id]["routes"].values():
        for spec in (route.get("materials") or {}).values():
            if isinstance(spec.get("from"), str):
                parts.add(spec["from"])
            for s in _steps(spec.get("steps")):
                ops.add(s.get("op"))
                ops.update(s.get("or") or [])
        for spec in (route.get("assemblies") or {}).values():
            ops.add(spec.get("op"))
            for s in _steps(spec.get("steps")):
                ops.add(s.get("op"))
                ops.update(s.get("or") or [])
            for raw in (spec.get("roles") or {}).values():
                adds.update(m["use"] for m in _members(raw) if m.get("use") in data["additions"])
    keys = set()
    for p in parts:
        ing, _, part = p.partition(".")
        props = (cat.parts.get(ing) or {}).get(part) or {}
        keys |= set(props)
        for layer in ("outer_layer", "seed_core"):
            keys |= set(props.get(layer) or {})
    for a in adds:
        keys |= set(data["additions"][a].get("props") or {})
    return {"operations": sorted(o_ for o_ in ops if o_), "parts": sorted(parts),
            "additions": sorted(adds), "property_keys": sorted(keys - {"edible",
                                                                        "not_food_reason"})}


def _sha(obj) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True, ensure_ascii=False,
                                     default=str).encode("utf-8")).hexdigest()[:16]


def _code_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()[:16]


def freeze_manifest() -> dict:
    """What the schema is: field lists, the vocabularies, every operation's
    definition, every property key, and the code that interprets them."""
    cat = o.load()
    data = load()
    keys = set(cat.default_false)
    for ps in cat.parts.values():
        for p in ps.values():
            keys |= set(p)
            for layer in ("outer_layer", "seed_core"):
                keys |= set(p.get(layer) or {})
    for a in data["additions"].values():
        keys |= set(a.get("props") or {})
    return {
        "schema": {k: list(v) for k, v in SCHEMA.items()},
        "vocabulary": {"patterns": sorted(data["patterns"]),
                       "mechanisms": sorted(data["mechanisms"]),
                       "water_routes": sorted(data["water_routes"]),
                       "gap_kinds": list(GAP_KINDS), "splits": list(SPLITS)},
        "operations": {k: _sha(v) for k, v in sorted(cat.operations.items())},
        "catalogue": _sha({"scales": cat.scales, "default_false": sorted(cat.default_false),
                           "functions": cat.functions}),
        "property_keys": sorted(keys - {"edible", "not_food_reason"}),
        "code": {"constructions.py": _code_sha(Path(__file__)),
                 "operations.py": _code_sha(Path(o.__file__))},
    }


# ---- rendering --------------------------------------------------------------------

def _en(op: str) -> str:
    return o.load().operations[op]["en"]


def render(dish_id: str) -> str:
    data = load()
    if dish_id not in data["dishes"]:
        return f"No construction {dish_id!r}. Known: {', '.join(sorted(data['dishes']))}.\n"
    dish = data["dishes"][dish_id]
    rep = validate(dish_id)
    out = [f"{dish['name']} ({dish['tradition']}): {rep.verdict} represented", ""]
    for rid, route in dish["routes"].items():
        r = rep.routes[rid]
        out.append(f"Route {rid} [{', '.join(route.get('patterns') or [])}] "
                   f"recipes {', '.join(route['recipes'])}: {r.verdict}")
        out.append(f"  why: {' '.join(str(route.get('why', '')).split())}")
        holds = [f"{h} {data['mechanisms'][h]}" for h in route.get("holds_by") or []
                 if h in data["mechanisms"]]
        if holds:
            out.append(f"  holds by: {'; '.join(holds)}")
        water = [f"{w} {data['water_routes'][w]}" for w in route.get("water") or []
                 if w in data["water_routes"]]
        if water:
            out.append(f"  water: {'; '.join(water)}")
        for mid, spec in (route.get("materials") or {}).items():
            src = spec["from"] if isinstance(spec["from"], str) else \
                f"{spec['from']['material']} [{spec['from']['output']}]"
            path = " -> ".join(_en(s["op"]) + (f" [{s['keep']}]" if s.get("keep") else "")
                               for s in _steps(spec.get("steps")) if s.get("op") in
                               o.load().operations)
            out.append(f"  material {mid}: {src}" + (f" -> {path}" if path else ""))
        for aid, spec in (route.get("assemblies") or {}).items():
            roles = "; ".join(f"{role}: {', '.join(m['use'] for m in _members(raw))}"
                              for role, raw in (spec.get("roles") or {}).items())
            then = " -> ".join(_en(s["op"]) for s in _steps(spec.get("steps"))
                               if s.get("op") in o.load().operations)
            out.append(f"  {aid} = {spec['op']} ({roles})" + (f" -> {then}" if then else ""))
        for src, step, output, mid in r.recombinations:
            out.append(f"  recombination: {src} -> {step} [{output}] -> {mid} returns to the dish")
        for problem in r.failures + r.unknowns + r.unaccounted + r.errors:
            out.append(f"  ! {problem}")
        for g in r.model_gaps:
            out.append(f"  gap (model): {g}")
        out.append("")
    return "\n".join(out)


def render_list() -> str:
    data = load()
    out = ["Documented constructions (R3): dish, split, routes, verdict", ""]
    for did, dish in data["dishes"].items():
        rep = validate(did)
        out.append(f"{did:26} {dish['split']:9} {len(dish['routes'])} route(s)  {rep.verdict}")
    return "\n".join(out) + "\n"
