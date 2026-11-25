"""Views over the documented records for a cook deciding and making dinner (R7).

Read-only. Everything here is a projection of data that already exists:
- R3 documented dishes (`constructions`),
- R4 controlled transfers (`transfers`),
- R5 processing conditions, whole sequences and intermediates (`conditions`),
- the user's own kitchen records (`kitchen_records`), shown beside the
  documented values and never merged into them.

It follows docs/research/r6-academic-foundations/r7-recommendation.md:
1. `outcomes`: what an ingredient can become, familiar uses then less usual ones;
2. `overview`: a dish as one branch per independently prepared member, joining
   at the assembly, each member keeping its own line after the join;
3. `aligned`: a dish's documented routes as aligned columns, rejected ones too;
4. a swap (an R4 transfer) is an `overview` with the changed branch marked;
5. `start_from`: the routes through a state you already have, the held branch
   marked done;
6. `outcome_edges` / `map_default_view`: the mindmap's outcome ring.

What it never does: compose a route from the steps of several routes, rank or
score anything, average conflicting values, present a done-when check as a
safety limit, or read availability from anywhere but the user's shelf checks.
"Not found" stays "not found".
"""

from __future__ import annotations

from dataclasses import dataclass, field

from foodprep import conditions as cd
from foodprep import constructions as c
from foodprep import kitchen_records as kr
from foodprep import operations as o
from foodprep import transfers as t

# ---- words -----------------------------------------------------------------------

ENDPOINT_WORDS = {
    "readiness": "ready for the next step",
    "doneness": "ready to eat",
    None: "endpoint not recorded",
}
TRANSFER_VERDICTS = {
    "worth_cooking": "worth cooking",
    "not_worth_it": "not worth it",
    "rejected": "rejected: documented to fail",
}
EVIDENCE_WORDS = {
    "works": "the evidence says it works",
    "works_with_conditions": "the evidence says it works, with conditions",
    "poor": "the evidence says it is poor",
    "fails": "the evidence says it fails",
    "unknown": "the evidence does not say",
}
STATUS_WORDS = {
    "documented": "made this way in practice",
    "inference": "not found in practice: an inference",
}
BASIS_WORDS = {
    "food_safety": "a food-safety body",
    "home_economics": "a home-economics association",
    "cooking": "cooks",
}
ACTIVE_WORDS = {
    "continuous": "continuous: stay with it",
    "regular": "regular: come back every few minutes",
    "occasional": "occasional: once or twice",
    "none": "waiting: nothing to do",
}
MISS_WORDS = {
    "skipped": "Do not skip",
    "underdone": "Do not stop short at",
    "overdone": "Do not overdo",
}
NOT_A_SAFETY_LIMIT = ("Done-when checks are cooks' signs that a step has worked. "
                      "They are not food-safety limits.")
NO_COMBINATIONS = ("Each column is one documented route or one documented "
                   "alternative. Taking a step from one column and a step from "
                   "another makes a combination nobody documented: each part has a "
                   "source, the whole does not.")
HISTORY_NOT_CONSIDERED = ("History not considered: this matched by the state the "
                          "food is in (R1), not by how it got there.")


def op_name(op: str | None) -> str:
    cat = o.load()
    if op in cat.operations:
        first = str(cat.operations[op].get("en") or op).split(",")[0].strip()
        if first.count("(") > first.count(")"):        # "wrap or roll a filling (leaf"
            first = first.split(" (")[0].strip()
        return first
    return str(op or "?").replace("_", " ")


def _words(text) -> str:
    return " ".join(str(text or "").split())


def _readable(x: str) -> str:
    return str(x).replace("_", " ")


# ---- small value types -----------------------------------------------------------

@dataclass
class Cited:
    """One statement with the sources that make it."""
    text: str
    sources: list = field(default_factory=list)
    cause: str = ""


@dataclass
class Conflict:
    topic: str
    versions: list            # Cited: choices, never merged
    note: str = ""


@dataclass
class MemberLine:
    """One member's own endpoint at a step after a join."""
    member: str
    done_when: list           # Cited
    failed_if: list           # Cited
    note: str = ""

    @property
    def found(self) -> bool:
        return bool(self.done_when or self.failed_if)


@dataclass
class StepView:
    address: str
    owner: str
    index: int
    op: str
    name: str
    says: str = ""                                    # the route's own evidence text
    or_ops: list = field(default_factory=list)        # documented alternative operations
    optional: bool = False
    endpoint: str | None = None                       # readiness | doneness | None
    endpoint_sources: list = field(default_factory=list)
    done_when: list = field(default_factory=list)     # Cited
    failed_if: list = field(default_factory=list)     # Cited (with cause)
    times: list = field(default_factory=list)         # Cited: versions, never merged
    active: Cited | None = None
    medium: list = field(default_factory=list)        # Cited
    conflicts: list = field(default_factory=list)     # Conflict
    because: list = field(default_factory=list)       # Cited: why this step exists
    misses: list = field(default_factory=list)        # Cited: what fails if skipped/...
    note: str = ""
    members: list = field(default_factory=list)       # MemberLine, steps after a join
    heat: bool = False
    done: bool = False                                # held: you already have this
    recorded: list = field(default_factory=list)      # (cooked_on, what it took): control

    @property
    def endpoint_words(self) -> str:
        return ENDPOINT_WORDS.get(self.endpoint, ENDPOINT_WORDS[None])


@dataclass
class Branch:
    member: str
    source: str                                       # ingredient.part, or a fraction
    steps: list                                       # StepView
    changed: bool = False                             # changed by a swap
    replaces: str = ""                                # the base member it replaces
    held_upto: int = 0                                # steps already done (start from)

    @property
    def remaining(self) -> list:
        return [s for s in self.steps if not s.done]


@dataclass
class Join:
    aid: str
    op: str
    name: str
    members: list                                     # (member, role, kind)
    steps: list                                       # StepView
    changed: bool = False
    says: str = ""


@dataclass
class Overview:
    key: str
    name: str
    kind: str                                         # dish | transfer
    branches: list
    joins: list
    result: str = ""
    finish: list = field(default_factory=list)        # (stage, [Cited times], [Cited done])
    gaps: list = field(default_factory=list)          # str: where the evidence stops
    keeping: list = field(default_factory=list)       # (intermediate name, [Cited], note)
    alternatives: list = field(default_factory=list)  # Cited "name: says": R5, as recorded
    has_sequence: bool = False
    # a swap
    base: str = ""                                    # base route key
    swaps: dict = field(default_factory=dict)         # old -> new
    dropped: list = field(default_factory=list)
    added: list = field(default_factory=list)          # members the swap adds
    reworked: list = field(default_factory=list)       # base members it re-specifies
    verdict: str = ""
    evidence: str = ""
    status: str = ""
    refused: bool = False
    reasons: list = field(default_factory=list)
    replaced_by: str = ""
    records: list = field(default_factory=list)       # control records for this route


# ---- the routes ------------------------------------------------------------------

def route_keys() -> list[str]:
    return list(cd.routes())


def route_label(key: str) -> str:
    r = cd.routes().get(key)
    if r is None:
        return key
    if key.startswith("transfer:"):
        return r.name
    dish, _, route = key.partition("/")
    n = len(c.load()["dishes"][dish]["routes"])
    return r.name if n == 1 else f"{r.name} ({_readable(route)})"


def dish_choices() -> list[tuple[str, str]]:
    """(route key, label) for the dish picker: the controlled transfers first (the
    dishes R4/R5 prepared for cooking), then every documented route, in the order
    recorded. Not a ranking."""
    keys = route_keys()
    tr = [k for k in keys if k.startswith("transfer:")]
    return [(k, route_label(k)) for k in tr + [k for k in keys if k not in tr]]


def _ingredient_of(src) -> str | None:
    if isinstance(src, str):
        return src.partition(".")[0]
    return None


def _source_label(spec: dict) -> str:
    src = spec.get("from")
    if isinstance(src, str):
        ing, _, part = src.partition(".")
        return f"{_readable(ing)} ({_readable(part)})" if part else _readable(ing)
    if isinstance(src, dict):
        return (f"the {_readable(src.get('output') or 'part')} of "
                f"{_readable(src.get('material'))}, kept from its "
                f"{op_name(src.get('step'))}")
    return "?"


def raw_ingredients(key: str) -> list[str]:
    """The raw ingredients a route's materials start from, in route order."""
    out = []
    for spec in (cd.routes()[key].spec.get("materials") or {}).values():
        ing = _ingredient_of(spec.get("from"))
        if ing and ing not in out:
            out.append(ing)
    return out


def _cited(items, text="check") -> list[Cited]:
    return [Cited(_words(x.get(text)), list(x.get("sources") or []), _words(x.get("cause")))
            for x in items or [] if x.get(text)]


def _time_cited(e: dict) -> Cited:
    return Cited(cd._time(e) + (f" ({_words(e['note'])})" if e.get("note") else ""),
                 list(e.get("sources") or []))


def _medium_cited(m: dict) -> Cited:
    bits = [_readable(m.get("medium", ""))]
    if m.get("temp_c"):
        lo, hi = m["temp_c"]
        bits.append(f"{lo}-{hi} C" if lo != hi else f"{lo} C")
    if m.get("cover"):
        bits.append(_readable(m["cover"]))
    if m.get("note"):
        bits.append(_words(m["note"]))
    return Cited("; ".join(bits), list(m.get("sources") or []))


def _step_view(r: cd.Route, owner: str, index: int, op: str, raw: dict, seq: dict,
               cat: o.Catalogue) -> StepView:
    addr = f"{r.key}/{owner}/{index}"
    sv = StepView(addr, owner, index, op, op_name(op), _words(raw.get("evidence")),
                  [op_name(x) for x in raw.get("or") or []], bool(raw.get("optional")))
    st = (seq.get("steps") or {}).get(addr) or {}
    ep = st.get("endpoint") or {}
    sv.endpoint = ep.get("kind")
    sv.endpoint_sources = list(ep.get("sources") or [])
    f = cd.step_fields(addr)
    sv.done_when = _cited(f.get("completion"))
    sv.failed_if = _cited(f.get("failure"))
    sv.times = [_time_cited(e) for e in f.get("elapsed") or []]
    a = f.get("active")
    if a:
        sv.active = Cited(ACTIVE_WORDS.get(a.get("kind"), _readable(a.get("kind")))
                          + (f" ({_words(a['note'])})" if a.get("note") else ""),
                          list(a.get("sources") or []))
    sv.medium = [_medium_cited(m) for m in f.get("medium") or []]
    for x in cd.for_step(addr):
        for cf in x["conflicts"]:
            sv.conflicts.append(Conflict(_words(cf.get("topic")),
                                         _cited(cf.get("versions"), "says"),
                                         _words(cf.get("note"))))
    sv.because = [Cited(_words(d["says"]), list(d.get("sources") or []))
                  for d in seq.get("depends") or [] if d.get("step") == addr]
    sv.misses = [Cited(f"{MISS_WORDS.get(m['when'], m['when'])}: {_words(m['failure'])}",
                       list(m.get("sources") or []))
                 for m in seq.get("misses") or [] if m.get("step") == addr]
    sv.note = _words(f.get("note") or st.get("note"))
    sv.heat = cd._is_heat(op, cat) if op else False
    return sv


def _member_lines(r: cd.Route, aid: str, addr: str, seq: dict) -> list[MemberLine]:
    """Each material the join holds, with its own endpoint at this step: the
    recorded one, or "not found" (with the sequence's note when it gives one)."""
    recorded = (seq.get("members") or {}).get(addr) or {}
    mats = r.spec.get("materials") or {}
    out = []
    for m in cd.subtree(r, aid):
        if m not in mats:
            continue
        x = recorded.get(m) or {}
        out.append(MemberLine(m, _cited(x.get("completion")), _cited(x.get("failure")),
                              _words(x.get("note"))))
    return out


def _join_order(asms: dict) -> list[str]:
    """Assemblies with any nested assembly before the one that holds it."""
    order: list[str] = []

    def visit(aid: str, seen: frozenset = frozenset()) -> None:
        if aid in order or aid in seen:
            return
        for m in cd._members(asms[aid]):
            if m in asms:
                visit(m, seen | {aid})
        order.append(aid)

    for aid in asms:
        visit(aid)
    return order


def _roles(spec: dict, mats: dict, asms: dict) -> list[tuple[str, str, str]]:
    out = []
    for role, raw in (spec.get("roles") or {}).items():
        for m in c._members(raw):
            use = m["use"]
            kind = "material" if use in mats else "assembly" if use in asms else "added as is"
            out.append((use, _readable(role), kind))
    return out


def intermediates_on(key: str) -> list[tuple[str, dict]]:
    """Recorded intermediate states this route passes through: a part after the
    first operations of one of its materials, or the state after one of its steps."""
    r = cd.routes()[key]
    addrs = {p.address for p in r.points}
    out = []
    for iid, it in (cd.load().get("intermediates") or {}).items():
        if it.get("at"):
            if it["at"] in addrs:
                out.append((iid, it))
            continue
        after = list(it.get("after") or [])
        for spec in (r.spec.get("materials") or {}).values():
            ops = [s.get("op") for s in c._steps(spec.get("steps"))]
            if spec.get("from") == it.get("part") and ops[:len(after)] == after:
                out.append((iid, it))
                break
    return out


def keeping_lines(it: dict) -> list[Cited]:
    """How long a state keeps, each statement with its authority and sources."""
    out = []
    for k in it.get("keeps") or []:
        bits = [_words(k.get("where")) if k.get("where") not in (None, "-") else ""]
        if k.get("how"):
            bits.append(_words(k["how"]))
        span = cd._time(k)
        if span:
            bits.append(span)
        bits.append(f"says {BASIS_WORDS.get(k.get('basis'), _readable(k.get('basis')))}")
        out.append(Cited(", ".join(b for b in bits if b), list(k.get("sources") or [])))
    return out


def overview(key: str, held: tuple[str, int] | None = None) -> Overview | None:
    """A route as one branch per independently prepared member, joining at the
    assemblies; every step with what R5 holds for it. `held=(member, n)` marks the
    first n steps of that member done (start from a state you have)."""
    r = cd.routes().get(key)
    if r is None:
        return None
    cat = o.load()
    seq = cd.sequence(key) or {}
    mats = r.spec.get("materials") or {}
    asms = r.spec.get("assemblies") or {}
    ov = Overview(key, route_label(key), "transfer" if key.startswith("transfer:") else "dish",
                  [], [], result=_readable(r.spec.get("result") or ""),
                  has_sequence=bool(seq))
    changed_m, changed_a = set(), set()
    if ov.kind == "transfer":
        tid = key.split(":", 1)[1]
        cand = t.load()["candidates"][tid]
        tr = cand.get("transfer") or {}
        b = cand["base"]
        ov.base = f"{b['dish']}/{b['route']}"
        ov.swaps = dict(tr.get("swap") or {})
        ov.dropped = list(tr.get("drop") or [])
        changed_m = set(tr.get("materials") or {})
        changed_a = set(tr.get("assemblies") or {})
        ov.verdict = TRANSFER_VERDICTS.get(cand.get("verdict"), _readable(cand.get("verdict")))
        ov.evidence = EVIDENCE_WORDS.get(cand.get("evidence_says"), "")
        ov.status = STATUS_WORDS.get(cand.get("status"), "")
        ov.refused = cand.get("verdict") in ("not_worth_it", "rejected")
        ov.reasons = [_words(x) for x in cand.get("reasons") or []]
        ov.replaced_by = cand.get("replaced_by") or ""
        base_mats = set(c.load()["dishes"][b["dish"]]["routes"][b["route"]].get("materials") or {})
        new = set(ov.swaps.values())
        ov.added = [m for m in mats if m in changed_m and m not in base_mats and m not in new]
        ov.reworked = [m for m in mats if m in changed_m and m in base_mats]
    replaced = {new: old for old, new in ov.swaps.items()}
    records = kr.control_records(key)
    ov.records = records

    def steps_of(owner: str, raw_steps) -> list[StepView]:
        out = []
        for i, s in enumerate(c._steps(raw_steps), 1):
            sv = _step_view(r, owner, i, s.get("op"), s, seq, cat)
            for rec in records:
                took = (rec.get("step_times") or {}).get(sv.address)
                if took:
                    sv.recorded.append((rec.get("cooked_on"), took))
            if held and owner == held[0] and i <= held[1]:
                sv.done = True
            out.append(sv)
        return out

    for mid, spec in mats.items():
        br = Branch(mid, _source_label(spec), steps_of(mid, spec.get("steps")),
                    changed=mid in changed_m, replaces=replaced.get(mid, ""))
        if held and held[0] == mid:
            br.held_upto = held[1]
        ov.branches.append(br)
    for aid in _join_order(asms):
        spec = asms[aid]
        j = Join(aid, spec.get("op", ""), op_name(spec.get("op")), _roles(spec, mats, asms),
                 steps_of(aid, spec.get("steps")), changed=aid in changed_a,
                 says=_words(spec.get("evidence")))
        for sv in j.steps:
            if sv.heat or (seq.get("members") or {}).get(sv.address):
                sv.members = _member_lines(r, aid, sv.address, seq)
        ov.joins.append(j)
    for f in seq.get("finish") or []:
        ov.finish.append((_words(f.get("stage")),
                          [_time_cited(e) for e in f.get("elapsed") or []],
                          _cited(f.get("completion")), _words(f.get("note"))))
    ov.gaps = [_words(g) for g in seq.get("gaps") or []]
    ov.alternatives = [Cited(f"{_words(a.get('name'))}: {_words(a.get('says'))}",
                             list(a.get("sources") or []))
                       for a in seq.get("alternatives") or []]
    for _, it in intermediates_on(key):
        ov.keeping.append((it.get("name"), keeping_lines(it), _words(it.get("note"))))
    return ov


# ---- 1. what can I make with this ------------------------------------------------

@dataclass
class Outcome:
    key: str                     # the route to open
    name: str
    kind: str                    # dish | transfer
    group: str                   # familiar | less_usual
    verdict: str
    condition: Cited | None
    availability: list           # (ingredient, words)
    cooked: list                 # control records of this route
    risks: list                  # Cited: recorded quality risks
    gaps: list                   # str: where the evidence stops (safety included)
    keeping: list                # (intermediate name, note) with a safety or keeping gap
    swapped: str = ""            # "pea instead of chickpea"
    refused: bool = False
    reasons: list = field(default_factory=list)
    replaced_by: str = ""
    other_routes: int = 0


@dataclass
class PartRecord:
    """An R5 processing record on the part: its conflicts kept as versions. This is
    where uses that are not modelled as dishes appear (pea soup, in the soak)."""
    name: str
    conflicts: list              # Conflict
    gaps: list                   # str


@dataclass
class Outcomes:
    ingredient: str
    familiar: list
    less_usual: list
    part_records: list

    @property
    def empty(self) -> bool:
        return not (self.familiar or self.less_usual)


def ingredient_choices() -> list[str]:
    """Every ingredient a documented dish or a transfer starts from."""
    out: set = set()
    for key in route_keys():
        out.update(raw_ingredients(key))
    return sorted(out)


def one_condition(key: str) -> Cited | None:
    """The one thing documented practice says breaks this route: the stage whose
    skipping fails it, else the first recorded failure of a stage (R5 `misses`)."""
    misses = (cd.sequence(key) or {}).get("misses") or []
    if not misses:
        return None
    m = next((x for x in misses if x.get("when") == "skipped"), misses[0])
    r = cd.routes()[key]
    owner, idx = cd._split(m["step"])
    pt = r.point(owner, idx)
    what = f"{op_name(pt.op) if pt else m['step']} ({_readable(owner)})"
    return Cited(f"{MISS_WORDS.get(m['when'], m['when'])}: {what}. Otherwise "
                 f"{_words(m['failure'])}", list(m.get("sources") or []))


def quality_risks(key: str) -> list[Cited]:
    """Recorded failures at the step that makes the dish ready to eat, and each
    member's own recorded failures there."""
    seq = cd.sequence(key) or {}
    out = []
    for addr, st in (seq.get("steps") or {}).items():
        if (st.get("endpoint") or {}).get("kind") == "doneness":
            out += _cited(st.get("failure"))
    for addr, members in (seq.get("members") or {}).items():
        for m, x in members.items():
            for ch in _cited(x.get("failure")):
                ch.text = f"{_readable(m)}: {ch.text}"
                out.append(ch)
    return out


def availability(key: str) -> list[tuple[str, str]]:
    """Each raw ingredient with the user's latest shelf check, or that there is
    none. Never from lidl.fi."""
    out = []
    for ing in raw_ingredients(key):
        checks = kr.shelf_checks(ing)
        if not checks:
            out.append((ing, "no shelf check of yours recorded"))
            continue
        last = checks[-1]
        seen = "seen" if last.get("seen") else "not seen"
        out.append((ing, f"{seen} at {last.get('shop', 'the shop')} on {last.get('checked_on')}"
                         + (f" ({last['note']})" if last.get("note") else "")))
    return out


def _uses(key: str, ingredient: str) -> bool:
    return ingredient in raw_ingredients(key)


def _outcome(key: str, group: str, others: int = 0) -> Outcome:
    r = cd.routes()[key]
    oc = Outcome(key, route_label(key), "transfer" if key.startswith("transfer:") else "dish",
                 group, "", one_condition(key), availability(key), kr.control_records(key),
                 quality_risks(key), [_words(g) for g in (cd.sequence(key) or {}).get("gaps") or []],
                 [(it.get("name"), _words(it.get("note"))) for _, it in intermediates_on(key)
                  if it.get("note")], other_routes=others)
    if oc.kind == "transfer":
        cand = t.load()["candidates"][key.split(":", 1)[1]]
        oc.verdict = "; ".join(x for x in (
            TRANSFER_VERDICTS.get(cand.get("verdict"), _readable(cand.get("verdict"))),
            STATUS_WORDS.get(cand.get("status"), ""),
            EVIDENCE_WORDS.get(cand.get("evidence_says"), "")) if x)
        swap = (cand.get("transfer") or {}).get("swap") or {}
        oc.swapped = ", ".join(f"{_readable(new)} instead of {_readable(old)}"
                               for old, new in swap.items())
        oc.refused = cand.get("verdict") in ("not_worth_it", "rejected")
        oc.reasons = [_words(x) for x in cand.get("reasons") or []]
        oc.replaced_by = cand.get("replaced_by") or ""
    else:
        dish = c.load()["dishes"][key.split("/")[0]]
        oc.verdict = f"a documented dish ({_words(dish.get('tradition')) or 'tradition not recorded'})"
    del r
    return oc


def outcomes(ingredient: str) -> Outcomes:
    """The documented dishes (familiar uses) and controlled transfers (less usual
    uses) whose route starts from this ingredient, in the order recorded."""
    ingredient = ingredient.partition(".")[0]
    familiar, less = [], []
    for did, dish in c.load()["dishes"].items():
        keys = [f"{did}/{rid}" for rid in dish["routes"] if _uses(f"{did}/{rid}", ingredient)]
        if keys:
            # open the route R5 holds a whole sequence for, if there is one
            key = next((k for k in keys if cd.sequence(k)), keys[0])
            familiar.append(_outcome(key, "familiar", len(keys) - 1))
    for tid in t.candidate_ids():
        key = f"transfer:{tid}"
        if key in cd.routes() and _uses(key, ingredient):
            less.append(_outcome(key, "less_usual"))
    recs = []
    for pid in cd.pairs_for_part(ingredient):
        p = cd.for_pair(pid)
        cfs = [Conflict(_words(cf.get("topic")), _cited(cf.get("versions"), "says"),
                        _words(cf.get("note"))) for cf in p.get("conflicts") or []]
        recs.append(PartRecord(_words(p.get("name")), cfs, [_words(g) for g in p.get("gaps") or []]))
    return Outcomes(ingredient, familiar, less, recs)


# ---- 3. alternative routes as aligned columns ------------------------------------

@dataclass
class Column:
    key: str | None              # a whole route, or None for cited text
    name: str
    kind: str                    # route | alternative | rejected
    says: str = ""
    sources: list = field(default_factory=list)
    verdict: str = ""
    cells: dict = field(default_factory=dict)        # row -> StepView


@dataclass
class Alignment:
    key: str
    name: str
    rows: list                   # (row key, label)
    columns: list
    conflicts_note: str = NO_COMBINATIONS


def _row(sv: StepView) -> tuple[str, str]:
    return (f"{sv.owner}:{sv.op}", f"{op_name(sv.op)} ({_readable(sv.owner)})")


def _route_column(key: str, kind: str = "route", says: str = "", sources=None) -> Column:
    ov = overview(key)
    col = Column(key, route_label(key), kind, says, list(sources or []))
    if key.startswith("transfer:"):
        col.verdict = ov.verdict
    for sv in [s for b in ov.branches for s in b.steps] + [s for j in ov.joins for s in j.steps]:
        col.cells[_row(sv)[0]] = sv
    return col


def aligned(key: str) -> Alignment | None:
    """The documented ways to this dish, side by side. Corresponding steps share a
    row: the same member through the same operation. A route without the step
    shows "none". Alternatives that are only cited text are columns of text. A
    rejected route is a column. Nothing is combined, merged or ordered by merit."""
    if key not in cd.routes():
        return None
    cols = [_route_column(key)]
    seen = {key}
    sibling_keys = []
    if not key.startswith("transfer:"):
        dish = key.split("/")[0]
        sibling_keys = [f"{dish}/{rid}" for rid in c.load()["dishes"][dish]["routes"]]
    for k in sibling_keys:
        if k not in seen:
            cols.append(_route_column(k))
            seen.add(k)
    for k in [key] + sibling_keys:
        for a in (cd.sequence(k) or {}).get("alternatives") or []:
            says, srcs, name = _words(a.get("says")), list(a.get("sources") or []), _words(a.get("name"))
            target = a.get("route")
            if target and target in cd.routes():
                if target in seen:
                    continue
                tid = target.split(":", 1)[1] if target.startswith("transfer:") else ""
                rejected = bool(tid) and t.load()["candidates"][tid].get("verdict") == "rejected"
                cols.append(_route_column(target, "rejected" if rejected else "route", says, srcs))
                seen.add(target)
            elif says.lower().startswith("this route"):
                cols[0].says = "; ".join(x for x in (cols[0].says, f"{name}: {says}") if x)
                cols[0].sources += [s for s in srcs if s not in cols[0].sources]
            else:
                rejected = "rejected" in name.lower()
                cols.append(Column(None, name, "rejected" if rejected else "alternative",
                                   says, srcs))
    rows: list = []
    for col in cols:
        for sv in col.cells.values():
            r = _row(sv)
            if r not in rows:
                rows.append(r)
    return Alignment(key, route_label(key), rows, cols)


# ---- 5. start from what I have ---------------------------------------------------

@dataclass
class HeldRoute:
    route: str
    name: str
    owner: str
    at: int
    readiness: bool              # what you hold is ready for the next step, not to eat
    overview: Overview
    by_state: bool               # matched by R1 key(): history not considered


@dataclass
class StartFrom:
    iid: str
    name: str
    note: str
    keeping: list                # Cited
    routes: list                 # HeldRoute
    problems: list = field(default_factory=list)
    not_ready_to_eat: bool = False


def held_states() -> list[tuple[str, str]]:
    """(intermediate id, name): the recorded states a cook may already have."""
    return [(iid, _words(it.get("name")) or iid)
            for iid, it in (cd.load().get("intermediates") or {}).items()]


def start_from(iid: str) -> StartFrom | None:
    it = (cd.load().get("intermediates") or {}).get(iid)
    if it is None:
        return None
    if it.get("at"):
        res = cd.from_state(it["at"])
        by_state = False
    else:
        res = cd.from_state(it["part"], list(it.get("after") or []))
        by_state = True
    sf = StartFrom(iid, _words(it.get("name")), _words(it.get("note")), keeping_lines(it),
                   [], list(res.problems))
    for mt in res.matches:
        ov = overview(mt.route, held=(mt.owner, mt.at))
        sf.routes.append(HeldRoute(mt.route, route_label(mt.route), mt.owner, mt.at,
                                   mt.kind == "readiness", ov, by_state))
    sf.not_ready_to_eat = any(h.readiness for h in sf.routes) or \
        "not ready to eat" in sf.note.lower()
    return sf


# ---- 6. the mindmap's outcome ring -----------------------------------------------

MAP_TABLE_ABOVE = 20       # R4.1: above about 20 edges a graph is illegible


def outcome_edges(ingredient: str) -> list[tuple[str, str, str]]:
    """(from, to, label): the ingredient to each outcome (the second ring), then each
    outcome to the other raw ingredients it needs (the third)."""
    res = outcomes(ingredient)
    edges = []
    for oc in res.familiar + res.less_usual:
        label = "familiar use" if oc.group == "familiar" else "less usual use"
        edges.append((f"ing:{res.ingredient}", f"out:{oc.key}", label))
        for other in raw_ingredients(oc.key):
            if other != res.ingredient:
                edges.append((f"out:{oc.key}", f"ing:{other}", "also needs"))
    return edges


def map_default_view(n_edges: int) -> str:
    return "table" if n_edges > MAP_TABLE_ABOVE else "graph"
