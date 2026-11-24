"""Generate what each ingredient part could become, from techniques, not recipes.

The idea (ADR 0002, S2 and S3 notes): recipes only tell us what cooks already
do. Possibilities come from three hand-curated tables instead:

- part_properties.yaml: what a part physically is (water, fibre, fat, ...);
- technique_rules.yaml: what a technique needs from a part and what it does;
- families.yaml: families of what an ingredient brings (acid, fat, salt,
  umami, sweet, protein, carb), their members, and the mechanisms by which a
  member changes or completes a part in a given state.

part x technique gives a state; state x family mechanism x member gives an
idea with its reason, risks and safety notes. Ideas are grouped by family.
Only then is RecipeNLG asked how often the ingredient is cooked with that
member (pair_counts.yaml). The answer labels the idea and never removes it:

- common / seen:  recipes do this; a Cook suggestion.
- rare:           recipes do it far less than chance predicts.
- not_seen:       chance predicts it in some recipes, yet none have it.
- untested:       the corpus is too small to say either way.
- own_part:       the member is a part of the same ingredient (tomato gel on
                  tomato flesh); recipes do not record that.
- part_acid:      the member is a part of another ingredient (tomato gel on
                  broccoli). Recipes list only the whole tomato, so the corpus
                  cannot see this either. (The name stays from the acid-only
                  first version; it covers every family.)

Everything but common and seen is a Scout idea: possible by mechanism, and
something recipes cannot tell us.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

from foodprep import pair_counts as pc

DATA = Path(__file__).with_name("data")
LEVELS = ("none", "low", "medium", "high", "very_high")
MEMBER_MIN = "medium"   # a member counts in a family from this level up
COLD = ("raw", "massage", "puree")

# Labels, and the thresholds that set them.
MIN_EXPECTED = 5      # below this many expected (and seen) recipes the corpus cannot judge
RARE_RATIO = 0.3      # seen in under 30% of the recipes chance predicts is rare
COMMON_COUNT = 100    # not rare, and seen in 100+ recipes
SCOUT_LABELS = ("not_seen", "own_part", "part_acid", "rare", "untested")

# What the corpus label is evidence of. Stated wherever a label is shown.
LABEL_SCOPE = ("Labels count recipes that list the ingredient and the member together, "
               "whatever the technique. Technique counts in brackets are recipes whose "
               "directions mention that technique anywhere, not necessarily for the "
               "ingredient.")


@dataclass(frozen=True)
class Tables:
    parts: dict          # ingredient -> part -> properties (+ edible, not_food_reason)
    techniques: dict
    families: dict
    members: dict
    notes: list
    risks: list
    counts: dict


def _edibility() -> dict[tuple[str, str], tuple[str, str | None]]:
    data = pc.load_yaml(DATA / "tomato.yaml")
    return {(p["ingredient"], p["name"]): (str(p.get("edible", "yes")), p.get("not_food_reason"))
            for p in data.get("parts", [])}


@lru_cache(maxsize=1)
def load_tables() -> Tables:
    props = pc.load_yaml(DATA / "part_properties.yaml")["parts"]
    edible = _edibility()
    parts: dict = {}
    for ing, ps in props.items():
        for name, p in ps.items():
            e, why = edible.get((ing, name), ("yes", None))
            parts.setdefault(ing, {})[name] = {**(p or {}), "edible": e, "not_food_reason": why}
    fam = pc.load_yaml(pc.FAMILIES_PATH)
    return Tables(
        parts=parts,
        techniques=pc.load_yaml(DATA / "technique_rules.yaml")["techniques"],
        families=fam["families"],
        members=fam["members"],
        notes=fam.get("pairing_notes", []),
        risks=fam.get("risks", []),
        counts=pc.load_counts(),
    )


# ---- conditions --------------------------------------------------------------

def level(v) -> int:
    return LEVELS.index(v) if v in LEVELS else 0


def holds(props: dict, cond: dict) -> bool:
    """All conditions hold. Levels take "x", ">=x" or "<=x"; flags take
    true/false, and a missing flag is false."""
    for key, want in cond.items():
        have = props.get(key)
        if isinstance(want, bool):
            if bool(have) != want:
                return False
        elif isinstance(want, str) and want.startswith(">="):
            if level(have) < level(want[2:]):
                return False
        elif isinstance(want, str) and want.startswith("<="):
            if level(have) > level(want[2:]):
                return False
        elif have != want:
            return False
    return True


def holds_any(props: dict, cond: dict) -> bool:
    return not cond or any(holds(props, {k: v}) for k, v in cond.items())


def members_of(t: Tables, family: str) -> dict[str, dict]:
    """Members that count in a family (level medium or above)."""
    return {n: m for n, m in t.members.items()
            if level(m["families"].get(family)) >= level(MEMBER_MIN)}


def families_of(t: Tables, member: str) -> list[str]:
    m = t.members[member]
    return [f for f, lv in m["families"].items() if level(lv) >= level(MEMBER_MIN)]


def already_has(t: Tables, part_props: dict, family: str) -> bool:
    """The part already supplies this family, so adding more does nothing."""
    prop = t.families[family].get("part_property")
    return bool(prop) and level(part_props.get(prop)) >= level("high")


# ---- generating -------------------------------------------------------------

@dataclass
class Idea:
    ingredient: str
    part: str
    technique: str
    family: str | None = None
    member: str | None = None
    form: str | None = None
    mechanisms: list[str] = field(default_factory=list)
    reasons: list[str] = field(default_factory=list)
    risks: list[str] = field(default_factory=list)
    safety: list[str] = field(default_factory=list)
    label: str | None = None
    observed: int | None = None
    expected: float | None = None
    with_technique: int | None = None

    @property
    def scout(self) -> bool:
        return self.label in SCOUT_LABELS


def techniques_for(t: Tables, ingredient: str, part: str) -> list[str]:
    p = t.parts[ingredient][part]
    if p["edible"] == "no":
        return []
    only = p.get("only_techniques")
    out = []
    for name, rule in t.techniques.items():
        if only and name not in only:
            continue
        if f"{ingredient}.{part}" in rule.get("except", []):
            continue
        if holds(p, rule.get("requires", {})):
            out.append(name)
    return out


def mechanism_applies(t: Tables, mech: dict, part_props: dict, technique: str) -> bool:
    when = mech.get("when", {})
    effects = set(t.techniques[technique].get("effects", []))
    if "techniques" in when and technique not in when["techniques"]:
        return False
    if "effects_any" in when and not effects & set(when["effects_any"]):
        return False
    if not holds(part_props, when.get("part", {})):
        return False
    if not holds_any(part_props, when.get("part_any", {})):
        return False
    flav = when.get("part_flavour_any")
    if flav and not set(part_props.get("flavour", [])) & set(flav):
        return False
    return True


def member_form(member: dict, family: str, needs: dict) -> str | None:
    """The member's best form for a mechanism, or None if it cannot fill it."""
    plain = {k: v for k, v in needs.items() if k not in ("forms_any", "strength")}
    if not holds(member, plain):
        return None
    if "strength" in needs and not holds({"s": member["families"].get(family)},
                                         {"s": needs["strength"]}):
        return None
    allowed = needs.get("forms_any")
    for form in member["forms"]:
        if not allowed or form in allowed:
            return form
    return None


def _risk_applies(rule: dict, family: str, member: dict, part_props: dict,
                  hot: bool, contact: bool) -> bool:
    w = rule["when"]
    if "family" in w and w["family"] != family:
        return False
    if "family_not" in w and w["family_not"] == family:
        return False
    if not holds(part_props, w.get("part", {})):
        return False
    if not holds(member, w.get("member", {})):
        return False
    if not holds(member["families"], w.get("member_family", {})):
        return False
    if w.get("hot_or_contact") and not (hot or contact):
        return False
    return True


def family_ideas(t: Tables, family: str, ingredient: str, part: str,
                 technique: str) -> list[Idea]:
    p = t.parts[ingredient][part]
    if already_has(t, p, family):
        return []
    mechs = {name: m for name, m in t.families[family]["mechanisms"].items()
             if mechanism_applies(t, m, p, technique)}
    if not mechs:
        return []
    effects = set(t.techniques[technique].get("effects", []))
    hot = technique not in COLD
    ideas = []
    for mname, member in members_of(t, family).items():
        if member.get("from_part") == f"{ingredient}.{part}":
            continue
        idea = Idea(ingredient, part, technique, family=family, member=mname)
        for name, m in mechs.items():
            form = member_form(member, family, m.get("member_needs", {}))
            if form is None:
                continue
            idea.form = idea.form or form
            idea.mechanisms.append(name)
            idea.reasons.append(m["does"])
            if m.get("safety"):
                idea.safety.append(m["safety"])
        if not idea.mechanisms:
            continue
        contact = bool({t.families[family]["mechanisms"][n].get("timing") for n in idea.mechanisms}
                       & {"marinate", "dress"})
        for rule in t.risks:
            if _risk_applies(rule, family, member, p, hot, contact):
                idea.risks.append(rule["text"])
        if hot and member.get("heat_risk"):
            idea.risks.append(member["heat_risk"])
        for note in t.notes:
            w = note["when"]
            if holds(member, w.get("member", {})) and (
                    holds(p, w.get("part_or_browning", {})) or "browning" in effects):
                idea.reasons.append(note["text"])
        if member.get("safety"):
            idea.safety.append(member["safety"])
        ideas.append(idea)
    return ideas


def label(t: Tables, idea: Idea) -> Idea:
    """Attach the corpus label. Ideas without a member are left unlabelled.

    Scope (LABEL_SCOPE): the label is set by the ingredient-member pair over all
    recipes, never by the technique. A pair common in soups is labelled common
    for roasting too. `with_technique` is recorded for display only, and its
    technique is detected anywhere in the directions, not tied to the target.
    """
    if idea.member is None:
        return idea
    m = t.members[idea.member]
    if m.get("from_part"):
        same = str(m["from_part"]).startswith(idea.ingredient + ".")
        idea.label = "own_part" if same else "part_acid"
        return idea
    c = t.counts
    if not c:
        idea.label = "untested"
        return idea
    n_t = c["targets"].get(idea.ingredient, 0)
    n_s = c["sources"].get(idea.member, 0)
    obs = c["pairs"].get(idea.ingredient, {}).get(idea.member, 0)
    exp = n_t * n_s / c["recipes"] if c["recipes"] else 0.0
    key = t.techniques[idea.technique].get("corpus")
    idea.observed, idea.expected = obs, exp
    idea.with_technique = c["triples"].get(idea.ingredient, {}).get(key, {}).get(idea.member, 0)
    if exp < MIN_EXPECTED and obs < MIN_EXPECTED:
        idea.label = "untested"
    elif obs == 0:
        idea.label = "not_seen"
    elif obs < RARE_RATIO * exp:
        idea.label = "rare"
    elif obs >= COMMON_COUNT:
        idea.label = "common"
    else:
        idea.label = "seen"
    return idea


def generate(ingredient: str | None = None, part: str | None = None,
             family: str | None = None, tables: Tables | None = None) -> list[Idea]:
    t = tables or load_tables()
    ideas = []
    for ing, ps in t.parts.items():
        if ingredient and ing != ingredient:
            continue
        for pname in ps:
            if part and pname != part:
                continue
            for tech in techniques_for(t, ing, pname):
                ideas.append(Idea(ing, pname, tech))
                for fam in t.families:
                    if family and fam != family:
                        continue
                    ideas.extend(label(t, i) for i in family_ideas(t, fam, ing, pname, tech))
    return ideas


def scout_rank(idea: Idea) -> tuple:
    """Strongest Scout ideas first: a loud absence (many expected, none seen),
    then part-as-member ideas, then rare, then untested; more mechanisms first."""
    order = {"not_seen": 0, "own_part": 1, "part_acid": 1, "rare": 2, "untested": 3}
    exp = idea.expected or 0.0
    ratio = (idea.observed or 0) / exp if exp else 1.0
    return (order.get(idea.label, 9), ratio, -exp, -len(idea.mechanisms), idea.member or "")


def scout_ideas(ingredient: str | None = None, part: str | None = None,
                family: str | None = None) -> list[Idea]:
    return sorted((i for i in generate(ingredient, part, family) if i.scout), key=scout_rank)


# ---- grouping and rendering ----------------------------------------------------

LABEL_WORDS = {
    "common": "Common",
    "seen": "Seen",
    "rare": "Rare",
    "not_seen": "Not seen",
    "own_part": "Own part",
    "part_acid": "Part as member",
    "untested": "Untested",
}


@dataclass
class Pairing:
    """One member on one part within one family, across every technique it fits."""
    ingredient: str
    part: str
    family: str
    member: str
    ideas: list[Idea]

    @property
    def label(self) -> str | None:
        return self.ideas[0].label

    @property
    def scout(self) -> bool:
        return self.ideas[0].scout

    def rank(self) -> tuple:
        best = min(scout_rank(i) for i in self.ideas)
        return best[:3] + (-len({m for i in self.ideas for m in i.mechanisms}),) + best[4:]


def pairings(ideas: list[Idea]) -> list[Pairing]:
    groups: dict[tuple[str, str, str, str], list[Idea]] = {}
    for i in ideas:
        if i.member:
            groups.setdefault((i.ingredient, i.part, i.family, i.member), []).append(i)
    return [Pairing(*k, v) for k, v in groups.items()]


def _corpus_phrase(i: Idea) -> str:
    if i.label == "own_part":
        return "a part of the same ingredient; recipes do not record this"
    if i.label == "part_acid":
        return "a part of another ingredient; recipes list only the whole one"
    if i.observed is None:
        return "no corpus counts yet"
    if i.label == "untested":
        return (f"corpus too small to judge: chance predicts {i.expected:.1f} "
                f"recipes, {i.observed} seen")
    return (f"RecipeNLG lists them together in {i.observed:,} recipes (any technique); "
            f"chance alone predicts {i.expected:,.0f}")


def _name(x: str) -> str:
    return x.replace("_", " ")


def render_pairing(pr: Pairing, t: Tables | None = None) -> str:
    t = t or load_tables()
    first = pr.ideas[0]
    member = t.members[pr.member]
    mechs = t.families[pr.family]["mechanisms"]
    techs = ", ".join(_name(i.technique) + (f" ({i.with_technique})" if i.with_technique else "")
                      for i in pr.ideas)
    also = [f for f in families_of(t, pr.member) if f != pr.family]
    head = f"[{LABEL_WORDS.get(pr.label, '')}] + {_name(pr.member)} ({_name(first.form)})"
    if also:
        head += f", also {', '.join(also)}"
    lines = [head, f"    {_corpus_phrase(first)}",
             f"    Techniques (recipes also mentioning it anywhere): {techs}"]
    by_mech: dict[str, list[str]] = {}
    for i in pr.ideas:
        for m in i.mechanisms:
            by_mech.setdefault(m, []).append(_name(i.technique))
    does = {mechs[m]["does"] for m in by_mech}
    notes = dict.fromkeys(r for i in pr.ideas for r in i.reasons if r not in does)
    lines += [f"    Why ({', '.join(ts)}): {mechs[m]['does']}" for m, ts in by_mech.items()]
    lines += [f"    Why: {r}" for r in notes]
    lines += [f"    Risk: {r}" for r in dict.fromkeys(r for i in pr.ideas for r in i.risks)]
    lines += [f"    Safety: {r}" for r in dict.fromkeys(r for i in pr.ideas for r in i.safety)]
    if member.get("note"):
        lines.append(f"    Note: {member['note']}")
    if member.get("season"):
        lines.append(f"    Season: {member['season']}")
    return "\n".join(lines)


def render(ingredient: str, *, part: str | None = None, family: str | None = None,
           show_all: bool = False, limit: int = 3) -> str:
    t = load_tables()
    if ingredient not in t.parts:
        return f"No part properties for {ingredient!r} yet. Known: {', '.join(sorted(t.parts))}.\n"
    if family and family not in t.families:
        return f"No family {family!r}. Families: {', '.join(t.families)}.\n"
    prs = pairings(generate(ingredient, part, family, t))
    out = [f"What {ingredient} could become, by family. The ideas come from part properties,",
           "techniques and family mechanisms; RecipeNLG only labels them.",
           LABEL_SCOPE]
    if (warn := pc.stale_warning(t.counts)):
        out.append(warn)
    out.append("")
    for pname, p in t.parts[ingredient].items():
        if part and pname != part:
            continue
        techs = techniques_for(t, ingredient, pname)
        title = _name(pname).capitalize()
        if not techs:
            out += [f"{title}: not food. {p.get('not_food_reason') or ''}".rstrip(), ""]
            continue
        out.append(f"{title}. Techniques: {', '.join(_name(x) for x in techs)}.")
        if p.get("note"):
            out.append(f"  {p['note']}")
        for fam, spec in t.families.items():
            if family and fam != family:
                continue
            if already_has(t, p, fam):
                out.append(f"  {fam.capitalize()}: already has it, so adding {fam} does nothing.")
                continue
            mine = [x for x in prs if x.part == pname and x.family == fam]
            if not mine:
                continue
            shown = sorted((x for x in mine if show_all or x.scout), key=Pairing.rank)
            cook = [_name(x.member) for x in mine if not x.scout]
            out.append(f"  {fam.capitalize()} ({spec['says']}): {len(shown)} "
                       f"{'ideas' if show_all else 'Scout ideas'}")
            for x in shown[:limit]:
                out.append("    " + render_pairing(x, t).replace("\n", "\n    "))
            if len(shown) > limit:
                rest = ", ".join(_name(x.member) for x in shown[limit:])
                out.append(f"    More: {rest}")
            if cook and not show_all:
                out.append(f"    Recipes already do: {', '.join(cook)}")
        out.append("")
    return "\n".join(out).rstrip() + "\n"


def render_families(family: str | None = None) -> str:
    """Each family with its members, strongest first, and the other families
    each member also belongs to."""
    t = load_tables()
    if family and family not in t.families:
        return f"No family {family!r}. Families: {', '.join(t.families)}.\n"
    out = []
    for fam, spec in t.families.items():
        if family and fam != family:
            continue
        ms = sorted(members_of(t, fam).items(),
                    key=lambda kv: (-level(kv[1]["families"][fam]), kv[0]))
        out.append(f"{fam.capitalize()} ({spec['kind']}: {spec['says']}), "
                   f"{len(ms)} members, {len(spec['mechanisms'])} mechanisms")
        for name, m in ms:
            also = [f for f in families_of(t, name) if f != fam]
            extra = f"  also {', '.join(also)}" if also else ""
            src = "  (a part of ours)" if m.get("from_part") else ""
            out.append(f"  {_name(name):22} {m['families'][fam]:10}{extra}{src}")
        out.append(f"  Mechanisms: {', '.join(_name(x) for x in spec['mechanisms'])}")
        out.append("")
    return "\n".join(out).rstrip() + "\n"
