"""Count what RecipeNLG does with each ingredient part, and cache the counts.

Writes `src/foodprep/data/part_evidence.yaml` (counts only) and a hand-check
sheet of sampled sentences next to the corpus, in the gitignored
data/corpus/recipenlg/ folder, because it holds recipe text.

Run:  py -3.11 scripts/count_part_evidence.py [path-to-full_dataset.csv] [--sample N]

Without a path it uses $FOODPREP_RECIPENLG, then
data/corpus/recipenlg/full_dataset.csv (see foodprep.part_evidence.resolve_csv).
"""

from __future__ import annotations

import argparse
import re
import sys
import time
from datetime import date
from pathlib import Path

from foodprep import part_evidence as pe


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("csv", nargs="?")
    ap.add_argument("--sample", type=int, default=15,
                    help="sentences per part and class for the hand check (0 = none)")
    args = ap.parse_args()
    try:
        path = pe.resolve_csv(args.csv)
    except pe.RecipeNLGNotFound as err:
        print(err, file=sys.stderr)
        return 1

    t0 = time.time()
    print(f"Counting recipes in {path} ...", flush=True)
    totals = pe.count_rows(path)
    keep = re.compile("|".join(i.listed.pattern for i in pe.INGREDIENTS.values()), re.I)
    tallies, baselines, samples = pe.tally(pe.read_recipes(path, keep),
                                           sample_per_class=args.sample)
    evidence = pe.build_evidence(path, totals, tallies, baselines,
                                 search_date=date.today().isoformat())
    pe.write_evidence(evidence)
    sheet = Path(path).parent / "hand_check.tsv"
    if samples:
        pe.write_samples(samples, sheet)

    print(f"{sum(totals.values())} recipes; baselines {dict(baselines)}")
    for p in evidence["parts"]:
        r = p["recipes"]
        print(f"  {p['ingredient']:8} {p['part']:14} {p['evidence_level']:12} "
              f"mentioning {p['recipes_mentioning']:6}  "
              + "  ".join(f"{c} {r[c]}" for c in pe.CLASSES))
    print(f"Wrote {pe.EVIDENCE_PATH}")
    if samples:
        print(f"Hand-check sheet ({len(samples)} sentences): {sheet}")
    print(f"{time.time() - t0:.0f} s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
