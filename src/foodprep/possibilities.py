"""Generate what each ingredient part could become, from techniques, not recipes.

The idea (ADR 0002 and the S2 note): recipes only tell us what cooks already
do. Possibilities come from three hand-curated tables instead:

- part_properties.yaml: what a part physically is (water, fibre, fat, ...);
- technique_rules.yaml: what a technique needs from a part and what it does;
- acid.yaml: acid sources with their own character, and the mechanisms by
  which acid changes a part in a given state.

part x technique gives a state; state x acid mechanism x acid source gives an
idea with its reason, risks and safety notes. Only then is RecipeNLG asked how
often the ingredient is cooked with that acid source (pair_counts.yaml). The
answer labels the idea and never removes it:

- common / seen:  recipes do this; a Cook suggestion.
- rare:           recipes do it far less than chance predicts.
- not_seen:       chance predicts it in some recipes, yet none have it.
- untested:       the corpus is too small to say either way.
- own_part:       the acid comes from the same ingredient (tomato gel on tomato
                  flesh); recipes do not record that, so it is the generator's
                  own idea.
- part_acid:      the acid is a part of another ingredient (tomato gel on
                  broccoli). Recipes list the whole tomato, never the gel used
                  as the acid, so the corpus cannot see this either.

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
WET_FORMS = {"juice", "vinegar", "liquid", "crushed_raw", "puree", "cooked_sauce",
             "jelly", "paste"}

# Labels, and the thresholds that set them.
MIN_EXPECTED = 5      # below this many expected (and seen) recipes the corpus cannot judge
RARE_RATIO = 0.3      # seen in under 30% of the recipes chance predicts is rare
COMMON_COUNT = 100    # not rare, and seen in 100+ recipes
SCOUT_LABELS = ("not_seen", "own_part", "part_acid", "rare", "untested")


@dataclass(frozen=True)
class Tables:
    parts: dict          # ingredient -> part -> properties (+ edible, not_food_reason)
    techniques: dict
    sources: dict
    mechanisms: dict
    notes: dict
    risks: dict
    counts: dict


def _edibility() -> dict[tuple[str, str], tuple[str, str | None]]:
    data = pc.load_yaml(DATA / "tomato.yaml")
    out = {}
    for p in data.get("parts", []):
        out[(p["ingredient"], p["name"])] = (str(p.get("edible", "yes")),
                                             p.get("not_food_reason"))
    return out


@lru_cache(maxsize=1)
def load_tables() -> Tables:
    props = pc.load_yaml(DATA / "part_properties.yaml")["parts"]
    edible = _edibility()
    parts: dict = {}
    for ing, ps in props.items():
        for name, p in ps.items():
            e, why = edible.get((ing, name), ("yes", None))
            parts.setdefault(ing, {})[name] = {**(p or {}), "edible": e, "not_food_reason": why}
    acid = pc.load_yaml(pc.ACID_PATH)
    return Tables(
        parts=parts,
        techniques=pc.load_yaml(DATA / "technique_rules.yaml")["techniques"],
        sources=acid["sources"],
        mechanisms=acid["mechanisms"],
        notes=acid.get("pairing_notes", {}),
        risks=acid.get("risks", {}),
        counts=pc.load_counts(),
    )


# ---- conditions --------------------------------------------------------------

def _level(v) -> int:
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
            if _level(have) < _level(want[2:]):
                return False
        elif isinstance(want, str) and want.startswith("<="):
            if _level(have) > _level(want[2:]):
                return False
        elif have != want:
            return False
    return True


def holds_any(props: dict, cond: dict) -> bool:
    return not cond or any(holds(props, {k: v}) for k, v in cond.items())


# ---- generating -------------------------------------------------------------

@dataclass
class Idea:
    ingredient: str
    part: str
    technique: str
    source: str | None = None
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


def source_form(source: dict, needs: dict) -> str | None:
    """The source's best form for a mechanism, or None if it cannot fill it."""
    if not holds(source, {k: v for k, v in needs.items() if k != "forms_any"}):
        return None
    allowed = needs.get("forms_any")
    for form in source["forms"]:
        if not allowed or form in allowed:
            return form
    return None


def acid_ideas(t: Tables, ingredient: str, part: str, technique: str) -> list[Idea]:
    p = t.parts[ingredient][part]
    if _level(p.get("acidity")) >= _level("high"):
        return []          # already acid: more acid adds nothing
    mechs = {name: m for name, m in t.mechanisms.items()
             if mechanism_applies(t, m, p, technique)}
    if not mechs:
        return []
    effects = set(t.techniques[technique].get("effects", []))
    hot = technique not in ("raw", "massage", "puree")
    ideas = []
    for sname, s in t.sources.items():
        if s.get("from_part") == f"{ingredient}.{part}":
            continue
        idea = Idea(ingredient, part, technique, source=sname)
        for mname, m in mechs.items():
            form = source_form(s, m.get("source_needs", {}))
            if form is None:
                continue
            idea.form = idea.form or form
            idea.mechanisms.append(mname)
            idea.reasons.append(m["does"])
            if m.get("safety"):
                idea.safety.append(m["safety"])
        if not idea.mechanisms:
            continue
        timings = {t.mechanisms[m].get("timing") for m in idea.mechanisms}
        if p.get("pigment") == "green" and (hot or timings & {"marinate", "dress"}):
            idea.risks.append(t.risks["green_turns_olive"])
        if _level(s.get("sweetness")) >= _level("medium"):
            idea.risks.append(t.risks["reads_as_dessert"])
        if _level(s.get("bitterness")) >= 2 and _level(p.get("bitterness")) >= 2:
            idea.risks.append(t.risks["bitter_on_bitter"])
        if hot and s.get("heat_risk"):
            idea.risks.append(s["heat_risk"])
        if s.get("astringent") and (_level(p.get("fat")) >= 3 or "browning" in effects):
            idea.reasons.append(t.notes["astringent_with_fat_or_browning"])
        if s.get("safety"):
            idea.safety.append(s["safety"])
        ideas.append(idea)
    return ideas


def label(t: Tables, idea: Idea) -> Idea:
    """Attach the corpus label. Ideas without an acid source are left unlabelled."""
    if idea.source is None:
        return idea
    src = t.sources[idea.source]
    if src.get("from_part"):
        same = str(src["from_part"]).startswith(idea.ingredient + ".")
        idea.label = "own_part" if same else "part_acid"
        return idea
    c = t.counts
    if not c:
        idea.label = "untested"
        return idea
    n_t = c["targets"].get(idea.ingredient, 0)
    n_s = c["sources"].get(idea.source, 0)
    obs = c["pairs"].get(idea.ingredient, {}).get(idea.source, 0)
    exp = n_t * n_s / c["recipes"] if c["recipes"] else 0.0
    key = t.techniques[idea.technique].get("corpus")
    idea.observed, idea.expected = obs, exp
    idea.with_technique = c["triples"].get(idea.ingredient, {}).get(key, {}).get(idea.source, 0)
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
             tables: Tables | None = None) -> list[Idea]:
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
                ideas.extend(label(t, i) for i in acid_ideas(t, ing, pname, tech))
    return ideas


def scout_rank(idea: Idea) -> tuple:
    """Strongest Scout ideas first: a loud absence (many expected, none seen),
    then the generator's own-part ideas, then rare, then untested; more
    mechanisms before fewer."""
    order = {"not_seen": 0, "own_part": 1, "part_acid": 1, "rare": 2, "untested": 3}
    exp = idea.expected or 0.0
    ratio = (idea.observed or 0) / exp if exp else 1.0
    return (order.get(idea.label, 9), ratio, -exp, -len(idea.mechanisms), idea.source or "")


def scout_ideas(ingredient: str | None = None, part: str | None = None) -> list[Idea]:
    return sorted((i for i in generate(ingredient, part) if i.scout), key=scout_rank)


# ---- rendering --------------------------------------------------------------

LABEL_WORDS = {
    "common": "Common",
    "seen": "Seen",
    "rare": "Rare",
    "not_seen": "Not seen",
    "own_part": "Own part",
    "part_acid": "Part as acid",
    "untested": "Untested",
}


@dataclass
class Pairing:
    """One acid source on one part, across every technique it fits."""
    ingredient: str
    part: str
    source: str
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
    groups: dict[tuple[str, str, str], list[Idea]] = {}
    for i in ideas:
        if i.source:
            groups.setdefault((i.ingredient, i.part, i.source), []).append(i)
    return [Pairing(*k, v) for k, v in groups.items()]


def _corpus_phrase(i: Idea) -> str:
    if i.label == "own_part":
        return "acid from the same ingredient; recipes do not record this"
    if i.label == "part_acid":
        return "acid from a part of another ingredient; recipes list only the whole one"
    if i.observed is None:
        return "no corpus counts yet"
    if i.label == "untested":
        return (f"corpus too small to judge: chance predicts {i.expected:.1f} "
                f"recipes, {i.observed} seen")
    return (f"RecipeNLG lists them together in {i.observed:,} recipes; "
            f"chance alone predicts {i.expected:,.0f}")


def render_pairing(pr: Pairing, t: Tables | None = None) -> str:
    t = t or load_tables()
    first = pr.ideas[0]
    src = t.sources[pr.source]
    techs = ", ".join(
        f"{i.technique.replace('_', ' ')}"
        + (f" ({i.with_technique})" if i.with_technique else "")
        for i in pr.ideas)
    form = first.form.replace("_", " ")
    lines = [f"[{LABEL_WORDS.get(pr.label, '')}] + {pr.source.replace('_', ' ')} ({form})",
             f"    {_corpus_phrase(first)}",
             f"    Techniques: {techs}"]
    by_mech: dict[str, list[str]] = {}
    for i in pr.ideas:
        for m in i.mechanisms:
            by_mech.setdefault(m, []).append(i.technique.replace("_", " "))
    does = {t.mechanisms[m]["does"] for m in by_mech}
    notes = dict.fromkeys(r for i in pr.ideas for r in i.reasons if r not in does)
    risks = dict.fromkeys(r for i in pr.ideas for r in i.risks)
    safety = dict.fromkeys(r for i in pr.ideas for r in i.safety)
    lines += [f"    Why ({', '.join(ts)}): {t.mechanisms[m]['does']}" for m, ts in by_mech.items()]
    lines += [f"    Why: {r}" for r in notes]
    lines += [f"    Risk: {r}" for r in risks]
    lines += [f"    Safety: {r}" for r in safety]
    if src.get("note"):
        lines.append(f"    Note: {src['note']}")
    if src.get("season"):
        lines.append(f"    Season: {src['season']}")
    return "\n".join(lines)


def render(ingredient: str, *, part: str | None = None, show_all: bool = False,
           limit: int = 8) -> str:
    t = load_tables()
    if ingredient not in t.parts:
        known = ", ".join(sorted(t.parts))
        return f"No part properties for {ingredient!r} yet. Known: {known}.\n"
    prs = pairings(generate(ingredient, part, t))
    out = [f"What {ingredient} could become with acid. The ideas come from part properties,",
           "techniques and acid mechanisms; RecipeNLG only labels them.", ""]
    for pname, p in t.parts[ingredient].items():
        if part and pname != part:
            continue
        techs = techniques_for(t, ingredient, pname)
        title = pname.replace("_", " ").capitalize()
        if not techs:
            out += [f"{title}: not food. {p.get('not_food_reason') or ''}".rstrip(), ""]
            continue
        out.append(f"{title}. Techniques: {', '.join(x.replace('_', ' ') for x in techs)}.")
        if p.get("note"):
            out.append(f"  {p['note']}")
        if _level(p.get("acidity")) >= _level("high"):
            out += ["  Already acid, so adding acid does nothing: it is an acid source itself.", ""]
            continue
        mine = [x for x in prs if x.part == pname]
        shown = sorted((x for x in mine if show_all or x.scout), key=Pairing.rank)
        for x in shown[:limit]:
            out.append("  " + render_pairing(x, t).replace("\n", "\n  "))
        if len(shown) > limit:
            out.append(f"  ... {len(shown) - limit} more (--limit)")
        cook = [x.source.replace("_", " ") for x in mine if not x.scout]
        if cook and not show_all:
            out.append(f"  Recipes already do: {', '.join(cook)} (--all shows them).")
        out.append("")
    return "\n".join(out).rstrip() + "\n"
