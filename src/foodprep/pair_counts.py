"""How often RecipeNLG cooks each ingredient with each family member.

The possibility generator (foodprep.possibilities) builds its ideas from part
properties, technique rules and family mechanisms, never from recipes. These
counts only label each idea afterwards: common, rare, or never seen although
chance alone would put it in some recipes.

One pass over the corpus counts, per recipe:
- which target ingredients it lists (part_evidence.INGREDIENTS),
- which family members it lists (families.yaml `corpus` regexes),
- which techniques its directions use (part_evidence.TECHNIQUES).

Only counts are written (src/foodprep/data/pair_counts.yaml), never recipe
text: RecipeNLG's terms allow non-commercial research use only.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import Iterable

from foodprep import part_evidence as pe

DATA = Path(__file__).with_name("data")
FAMILIES_PATH = DATA / "families.yaml"
PAIR_COUNTS_PATH = DATA / "pair_counts.yaml"


def load_yaml(path: Path) -> dict:
    import yaml
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def families_checksum(path: Path = FAMILIES_PATH) -> str:
    """SHA-256 of the family definitions' content (not their formatting), so
    generated counts can say which ontology they were made from."""
    data = load_yaml(path)
    canon = json.dumps(data, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(canon.encode("utf-8")).hexdigest()


def stale_warning(record: dict, path: Path = FAMILIES_PATH) -> str | None:
    """A warning when counts were made from other family definitions than the
    current families.yaml (or carry no checksum), else None."""
    if not record:
        return None
    made_from = (record.get("corpus") or {}).get("families_sha256")
    if made_from == families_checksum(path):
        return None
    why = ("carry no checksum of the family definitions they were made from"
           if not made_from else "were made from different family definitions than "
           "the current families.yaml")
    return (f"Warning: the corpus counts {why}; "
            f"rerun scripts/count_family_pairs.py before trusting the labels.")


def source_patterns(families: dict | None = None) -> dict[str, re.Pattern[str]]:
    families = families if families is not None else load_yaml(FAMILIES_PATH)
    return {name: re.compile(m["corpus"], re.I) for name, m in families["members"].items()}


class Counts:
    """Recipe counts for targets, sources, their pairs, and the technique splits."""

    def __init__(self, targets: Iterable[str], sources: Iterable[str]):
        self.recipes = 0
        self.target: Counter[str] = Counter()
        self.source: Counter[str] = Counter()
        self.pair: Counter[tuple[str, str]] = Counter()
        self.target_technique: Counter[tuple[str, str]] = Counter()
        self.triple: Counter[tuple[str, str, str]] = Counter()
        self.targets = list(targets)
        self.sources = list(sources)

    def add(self, targets: set[str], sources: set[str], techniques: set[str]) -> None:
        self.recipes += 1
        self.source.update(sources)
        for t in targets:
            self.target[t] += 1
            for s in sources:
                self.pair[(t, s)] += 1
            for k in techniques:
                self.target_technique[(t, k)] += 1
                for s in sources:
                    self.triple[(t, k, s)] += 1

    def to_record(self) -> dict:
        return {
            "recipes": self.recipes,
            "targets": {t: self.target[t] for t in self.targets},
            "sources": {s: self.source[s] for s in self.sources},
            "pairs": {t: {s: self.pair[(t, s)] for s in self.sources} for t in self.targets},
            "techniques": {t: {k: self.target_technique[(t, k)] for k, _ in pe.TECHNIQUES}
                           for t in self.targets},
            "triples": {t: {k: {s: n for s in self.sources
                                if (n := self.triple[(t, k, s)])}
                            for k, _ in pe.TECHNIQUES}
                        for t in self.targets},
        }


def count_row(counts: Counts, ingredients: str, directions: str,
              targets: dict[str, re.Pattern[str]],
              sources: dict[str, re.Pattern[str]],
              any_source: re.Pattern[str]) -> tuple[set[str], set[str], set[str]]:
    """Count one recipe from its raw ingredient and direction fields, and return
    what was found (targets, members, techniques) for other tallies."""
    found_t = {t for t, rx in targets.items() if rx.search(ingredients)}
    found_s = ({s for s, rx in sources.items() if rx.search(ingredients)}
               if any_source.search(ingredients) else set())
    techs = {k for k, rx in pe.TECHNIQUES if rx.search(directions)} if found_t else set()
    counts.add(found_t, found_s, techs)
    return found_t, found_s, techs


def count_csv(path: Path | str, families: dict | None = None,
              also: Iterable = ()) -> Counts:
    """One pass over the corpus. Each object in `also` gets
    add(targets, members, techniques) for every recipe (family_profiles)."""
    sources = source_patterns(families)
    targets = {name: ing.listed for name, ing in pe.INGREDIENTS.items()}
    any_source = re.compile("|".join(f"(?:{rx.pattern})" for rx in sources.values()), re.I)
    counts = Counts(targets, sources)
    csv.field_size_limit(2**31 - 1)
    with open(path, encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        header = next(reader)
        i_ing, i_dir = header.index("ingredients"), header.index("directions")
        for row in reader:
            found = count_row(counts, row[i_ing], row[i_dir], targets, sources, any_source)
            for other in also:
                other.add(*found)
    return counts


HEADER = """\
# How often RecipeNLG lists each target ingredient with each family member
# GENERATED, do not hand-edit.
#
# Regenerate: py -3.11 scripts/count_family_pairs.py [path-to-full_dataset.csv]
#
# Counts recipes, from the ingredient list (targets, sources) and the
# directions (techniques, as in part_evidence.TECHNIQUES). foodprep.possibilities
# uses them only to label generated ideas as common, rare or not seen.
# Mostly American home cooking: absence means not done here, never not good.
#
# RecipeNLG's terms allow non-commercial research and educational use only.
# Only counts are kept here, never recipe text.
"""


def write_counts(record: dict, path: Path = PAIR_COUNTS_PATH) -> None:
    import yaml
    path.write_text(HEADER + yaml.safe_dump(record, sort_keys=False, allow_unicode=True),
                    encoding="utf-8")


def load_counts(path: Path = PAIR_COUNTS_PATH) -> dict:
    """The committed counts, or {} when they have not been generated."""
    return load_yaml(path) if path.is_file() else {}
