"""How often RecipeNLG cooks each ingredient with each acid source.

The possibility generator (foodprep.possibilities) builds its ideas from part
properties, technique rules and acid mechanisms, never from recipes. These
counts only label each idea afterwards: common, rare, or never seen although
chance alone would put it in some recipes.

One pass over the corpus counts, per recipe:
- which target ingredients it lists (part_evidence.INGREDIENTS),
- which acid sources it lists (acid.yaml `corpus` regexes),
- which techniques its directions use (part_evidence.TECHNIQUES).

Only counts are written (src/foodprep/data/pair_counts.yaml), never recipe
text: RecipeNLG's terms allow non-commercial research use only.
"""

from __future__ import annotations

import csv
import re
from collections import Counter
from pathlib import Path
from typing import Iterable

from foodprep import part_evidence as pe

DATA = Path(__file__).with_name("data")
ACID_PATH = DATA / "acid.yaml"
PAIR_COUNTS_PATH = DATA / "pair_counts.yaml"


def load_yaml(path: Path) -> dict:
    import yaml
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def source_patterns(acid: dict | None = None) -> dict[str, re.Pattern[str]]:
    acid = acid if acid is not None else load_yaml(ACID_PATH)
    return {name: re.compile(s["corpus"], re.I) for name, s in acid["sources"].items()}


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
              any_source: re.Pattern[str]) -> None:
    """Count one recipe from its raw ingredient and direction fields."""
    found_t = {t for t, rx in targets.items() if rx.search(ingredients)}
    found_s = ({s for s, rx in sources.items() if rx.search(ingredients)}
               if any_source.search(ingredients) else set())
    techs = {k for k, rx in pe.TECHNIQUES if rx.search(directions)} if found_t else set()
    counts.add(found_t, found_s, techs)


def count_csv(path: Path | str, acid: dict | None = None) -> Counts:
    sources = source_patterns(acid)
    targets = {name: ing.listed for name, ing in pe.INGREDIENTS.items()}
    any_source = re.compile("|".join(f"(?:{rx.pattern})" for rx in sources.values()), re.I)
    counts = Counts(targets, sources)
    csv.field_size_limit(2**31 - 1)
    with open(path, encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        header = next(reader)
        i_ing, i_dir = header.index("ingredients"), header.index("directions")
        for row in reader:
            count_row(counts, row[i_ing], row[i_dir], targets, sources, any_source)
    return counts


HEADER = """\
# How often RecipeNLG lists each target ingredient with each acid source:
# GENERATED, do not hand-edit.
#
# Regenerate: py -3.11 scripts/count_acid_pairs.py [path-to-full_dataset.csv]
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
