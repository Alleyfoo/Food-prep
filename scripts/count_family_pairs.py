"""Count how often RecipeNLG cooks each ingredient with each family member,
and which families each ingredient's recipes contain, in one pass.

Writes, counts only (no recipe text):
- src/foodprep/data/pair_counts.yaml       member pairs (labels for possibilities)
- src/foodprep/data/family_profiles.yaml   family shares, by technique, and sets

Run:  py -3.11 scripts/count_family_pairs.py [path-to-full_dataset.csv]

Without a path it uses $FOODPREP_RECIPENLG, then
data/corpus/recipenlg/full_dataset.csv (see foodprep.part_evidence.resolve_csv).
"""

from __future__ import annotations

import argparse
import sys
import time
from datetime import date

from foodprep import family_profiles as fp
from foodprep import pair_counts as pc
from foodprep import part_evidence as pe
from foodprep.corpus import portable_source


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("csv", nargs="?")
    args = ap.parse_args()
    try:
        path = pe.resolve_csv(args.csv)
    except pe.RecipeNLGNotFound as err:
        print(err, file=sys.stderr)
        return 1
    t0 = time.time()
    print(f"Counting {path} ...", flush=True)
    fams = fp.FamilyCounts()
    counts = pc.count_csv(path, also=[fams])
    corpus = {
        "corpus_id": "recipenlg",
        "name": "RecipeNLG",
        "source_path": portable_source(path.parent),
        "terms": "non-commercial research and educational use only; counts only",
        "search_date": date.today().isoformat(),
    }
    record = {"corpus": corpus, **counts.to_record()}
    pc.write_counts(record)
    profiles = {"corpus": corpus, **fams.to_record()}
    fp.write_profiles(profiles)
    print(f"{record['recipes']} recipes; targets {record['targets']}")
    print(f"families in any recipe {profiles['all_recipes']}")
    for t, row in profiles["targets"].items():
        print(f"  {t:8} {row['recipes']:7} {row['families']}")
    print(f"Wrote {pc.PAIR_COUNTS_PATH} and {fp.PROFILES_PATH} in {time.time() - t0:.0f} s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
