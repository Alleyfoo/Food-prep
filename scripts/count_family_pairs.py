"""Count how often RecipeNLG cooks each ingredient with each family member.

Writes src/foodprep/data/pair_counts.yaml (counts only, no recipe text).

Run:  py -3.11 scripts/count_family_pairs.py [path-to-full_dataset.csv]

Without a path it uses $FOODPREP_RECIPENLG, then
data/corpus/recipenlg/full_dataset.csv (see foodprep.part_evidence.resolve_csv).
"""

from __future__ import annotations

import argparse
import sys
import time
from datetime import date

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
    counts = pc.count_csv(path)
    record = {
        "corpus": {
            "corpus_id": "recipenlg",
            "name": "RecipeNLG",
            "source_path": portable_source(path.parent),
            "terms": "non-commercial research and educational use only; counts only",
            "search_date": date.today().isoformat(),
        },
        **counts.to_record(),
    }
    pc.write_counts(record)
    print(f"{record['recipes']} recipes; targets {record['targets']}")
    for t, row in record["pairs"].items():
        print(f"  {t:8} " + "  ".join(f"{s} {n}" for s, n in row.items()))
    print(f"sources {record['sources']}")
    print(f"Wrote {pc.PAIR_COUNTS_PATH} in {time.time() - t0:.0f} s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
