"""Family-level analysis: which families (acid, fat, salt, umami, sweet,
protein, carb) cooks put with each ingredient, by technique, and how that
compares with what the model says each state is missing.

Families are big enough to count reliably where single members are not:
lingonberry is in 222 of 2.2 million recipes, some acid in hundreds of
thousands. A recipe has a family when it lists any member of it at level
medium or above (families.yaml). A member that is a part of the target itself
(tomato gel for tomato) is not counted for that target.

Three questions:

1. Profile: what share of, say, roasted broccoli recipes has any acid?
2. Check: each curated state lists `missing_roles` in tomato.yaml (roasted
   broccoli florets miss salt, fat, acid, herb, protein, carb). Do cooks add
   those families? A curated gap that cooks rarely fill is a family-level
   Scout idea; a family cooks nearly always add but the model does not list
   is a curation hint.
3. Combinations: which sets of families appear together, e.g. fat + salt
   only versus fat + salt + acid.

Counts come from the same corpus pass as pair_counts.yaml
(scripts/count_family_pairs.py) and are written to family_profiles.yaml.
"""

from __future__ import annotations

from collections import Counter
from pathlib import Path

from foodprep import pair_counts as pc
from foodprep import part_evidence as pe

DATA = Path(__file__).with_name("data")
PROFILES_PATH = DATA / "family_profiles.yaml"
LEVELS = ("none", "low", "medium", "high", "very_high")
TOP_COMBOS = 12

# Shares, and what they are called.
USUAL = 0.5     # half the recipes or more add the family
RARELY = 0.2    # fewer than one in five

# Curated state techniques -> the RecipeNLG technique word that stands for them.
STATE_TECHNIQUE = {
    "raw_assemble": "raw", "raw_slaw": "raw", "salsa": "raw", "salt_and_drain": "raw",
    "steam": "steam", "roast": "roast", "char": "grill", "stir_fry": "stir_fry",
    "saute": "saute", "simmer": "boil", "reduce": "boil", "soup": "soup", "dry": "dry",
    "fry": "fry", "bake": "bake", "boil": "boil",
}


def member_families(families: dict) -> dict[str, list[str]]:
    out = {}
    for name, m in families["members"].items():
        out[name] = [f for f, lv in m["families"].items()
                     if LEVELS.index(lv) >= LEVELS.index("medium")]
    return out


class FamilyCounts:
    """Recipes per family, per target ingredient and technique, and combinations."""

    def __init__(self, families: dict | None = None):
        families = families if families is not None else pc.load_yaml(pc.FAMILIES_PATH)
        self.family_names = list(families["families"])
        self.of = member_families(families)
        self.own = {name: str(m["from_part"]).split(".")[0]
                    for name, m in families["members"].items() if m.get("from_part")}
        self.recipes = 0
        self.all: Counter[str] = Counter()
        self.target: Counter[str] = Counter()
        self.target_family: Counter[tuple[str, str]] = Counter()
        self.tech: Counter[tuple[str, str]] = Counter()
        self.tech_family: Counter[tuple[str, str, str]] = Counter()
        self.combos: Counter[tuple[str, str, str]] = Counter()

    def families_for(self, members: set[str], target: str | None = None) -> set[str]:
        """Families of the members, leaving out parts of `target` itself."""
        return {f for m in members
                if target is None or self.own.get(m) != target for f in self.of[m]}

    def add(self, targets: set[str], members: set[str], techniques: set[str]) -> None:
        self.recipes += 1
        self.all.update(self.families_for(members))
        for t in targets:
            fams = self.families_for(members, t)
            key = "+".join(f for f in self.family_names if f in fams) or "none"
            self.target[t] += 1
            self.combos[(t, "all", key)] += 1
            for f in fams:
                self.target_family[(t, f)] += 1
            for k in techniques:
                self.tech[(t, k)] += 1
                self.combos[(t, k, key)] += 1
                for f in fams:
                    self.tech_family[(t, k, f)] += 1

    def to_record(self) -> dict:
        targets = list(pe.INGREDIENTS)
        techs = [k for k, _ in pe.TECHNIQUES]

        def combos(t, k):
            row = [(key, n) for (tt, kk, key), n in self.combos.items() if tt == t and kk == k]
            return dict(sorted(row, key=lambda kv: -kv[1])[:TOP_COMBOS])

        return {
            "recipes": self.recipes,
            "all_recipes": {f: self.all[f] for f in self.family_names},
            "targets": {
                t: {
                    "recipes": self.target[t],
                    "families": {f: self.target_family[(t, f)] for f in self.family_names},
                    "combos": combos(t, "all"),
                    "techniques": {
                        k: {"recipes": self.tech[(t, k)],
                            "families": {f: self.tech_family[(t, k, f)] for f in self.family_names},
                            "combos": combos(t, k)}
                        for k in techs if self.tech[(t, k)]
                    },
                }
                for t in targets
            },
        }


HEADER = """\
# Which families RecipeNLG cooks put with each ingredient, by technique:
# GENERATED, do not hand-edit.
#
# Regenerate: py -3.11 scripts/count_family_pairs.py [path-to-full_dataset.csv]
#
# A recipe has a family when its ingredient list names any member of it at
# level medium or above (families.yaml). `combos` are the most frequent exact
# sets of families. Read by foodprep.family_profiles. Counts only.
# RecipeNLG's terms allow non-commercial research and educational use only.
"""


def write_profiles(record: dict, path: Path = PROFILES_PATH) -> None:
    import yaml
    path.write_text(HEADER + yaml.safe_dump(record, sort_keys=False, allow_unicode=True),
                    encoding="utf-8")


def load_profiles(path: Path = PROFILES_PATH) -> dict:
    return pc.load_yaml(path) if path.is_file() else {}


# ---- analysis -----------------------------------------------------------------

def share(n: int, total: int) -> float:
    return n / total if total else 0.0


def word(s: float) -> str:
    if s >= USUAL:
        return "usual"
    if s < RARELY:
        return "rare"
    return "common"


def curated_states(ingredient: str) -> list[dict]:
    """Curated states of an ingredient with their missing roles (tomato.yaml)."""
    data = pc.load_yaml(DATA / "tomato.yaml")
    default = data.get("default_ingredient", "tomato")
    out = []
    for tr in data["transformations"]:
        if tr.get("ingredient", default) != ingredient:
            continue
        missing = {}
        for m in tr.get("missing_roles") or []:
            if isinstance(m, dict):
                missing[m["role"]] = m.get("priority", "")
            else:
                missing[str(m)] = ""
        out.append({"technique": tr["technique"], "part": tr.get("part"),
                    "component": tr.get("output_component"), "missing": missing})
    return out


def verdict(curated: str | None, s: float) -> str:
    if curated is not None:
        if s >= USUAL:
            return "agrees"
        if s < RARELY:
            return "gap"          # the model says it needs it; cooks rarely add it
        return "partly"
    if s >= USUAL:
        return "unlisted"         # cooks usually add it; the model does not list it
    return ""


def check(ingredient: str, profiles: dict | None = None,
          family_names: list[str] | None = None) -> list[dict]:
    """One row per curated state and family: the curated claim against practice."""
    prof = profiles if profiles is not None else load_profiles()
    if not prof:
        return []
    fams = family_names or list(pc.load_yaml(pc.FAMILIES_PATH)["families"])
    target = prof["targets"].get(ingredient)
    if not target:
        return []
    rows = []
    for st in curated_states(ingredient):
        key = STATE_TECHNIQUE.get(st["technique"])
        tech = target["techniques"].get(key) if key else None
        if not tech:
            continue
        for f in fams:
            s = share(tech["families"][f], tech["recipes"])
            curated = st["missing"].get(f)
            rows.append({
                "technique": st["technique"], "part": st["part"], "corpus": key,
                "recipes": tech["recipes"], "family": f, "curated": curated,
                "share": s, "ingredient_share": share(target["families"][f], target["recipes"]),
                "verdict": verdict(curated, s),
            })
    return rows


def _pct(x: float) -> str:
    return f"{100 * x:.0f}%"


def render_profile(ingredient: str, profiles: dict | None = None) -> str:
    prof = profiles if profiles is not None else load_profiles()
    if not prof:
        return "No family profiles yet. Run scripts/count_family_pairs.py.\n"
    target = prof["targets"].get(ingredient)
    if not target:
        return f"No family profile for {ingredient!r}. Known: {', '.join(prof['targets'])}.\n"
    fams = list(target["families"])
    out = [f"Families cooks put with {ingredient} (RecipeNLG, {target['recipes']:,} recipes)", ""]
    head = f"  {'technique':10} {'recipes':>8} " + " ".join(f"{f:>7}" for f in fams)
    out.append(head)
    allr = prof["all_recipes"]
    out.append(f"  {'any recipe':10} {prof['recipes']:>8,} "
               + " ".join(f"{_pct(share(allr[f], prof['recipes'])):>7}" for f in fams))
    out.append(f"  {'all ' + ingredient:10} {target['recipes']:>8,} "
               + " ".join(f"{_pct(share(target['families'][f], target['recipes'])):>7}" for f in fams))
    for k, tech in sorted(target["techniques"].items(), key=lambda kv: -kv[1]["recipes"]):
        out.append(f"  {k:10} {tech['recipes']:>8,} "
                   + " ".join(f"{_pct(share(tech['families'][f], tech['recipes'])):>7}" for f in fams))

    rows = check(ingredient, prof, fams)
    if rows:
        out += ["", "Curated missing roles against practice (share of recipes with that technique):"]
        by_state: dict[tuple, list[dict]] = {}
        for r in rows:
            by_state.setdefault((r["technique"], r["part"], r["corpus"], r["recipes"]), []).append(r)
        for (tech, part, key, n), rs in by_state.items():
            name = tech.replace("_", " ") + (f" ({part})" if part else "")
            out.append(f"  {name}, counted as '{key}' in {n:,} recipes:")
            for label, test in (("Agrees, cooks add it", "agrees"),
                                ("Partly", "partly"),
                                ("Gap: listed as missing, cooks rarely add it", "gap"),
                                ("Cooks usually add it, not listed as missing", "unlisted")):
                hit = [f"{r['family']} {_pct(r['share'])}" for r in rs if r["verdict"] == test]
                if hit:
                    out.append(f"    {label}: {', '.join(hit)}")

    combos = target["combos"]
    out += ["", "Most frequent family sets (all recipes with the ingredient):"]
    for key, n in list(combos.items())[:8]:
        out.append(f"  {key.replace('+', ' + '):45} {_pct(share(n, target['recipes'])):>5}")
    return "\n".join(out) + "\n"
