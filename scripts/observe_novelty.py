"""Measure every Scout hypothesis against a recipe corpus, and cache the result.

The corpus is ~46k recipes that do not ship with the app, so the app can only
show a novelty claim if the answer travels with it. This writes
`src/foodprep/data/novelty.yaml`, which the loader reads like any other fact.

What the numbers can and cannot say:

  * **Absence is evidence.** Zero co-occurrences across the whole corpus, for
    two ingredients the corpus *does* know, is a real finding.
  * **Presence is not.** A high count often just means both ingredients are
    popular — the corpus has "mango lassi + capers" once, in a crab parfait.
    Raw counts cannot separate that from a real affinity; that needs lift over
    base rate, which this does not compute.
  * **`insufficient_coverage` is honest.** If either side does not resolve
    strictly, no claim is made rather than a false "never seen".

Run:  py -3.11 scripts/observe_novelty.py <path-to-CulinaryDB>
"""

from __future__ import annotations

import sqlite3
import sys
from datetime import date
from pathlib import Path

import yaml

from foodprep import corpus, query
from foodprep.loader import NOVELTY_PATH, build


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    corpus_dir = Path(sys.argv[1])
    if not corpus_dir.exists():
        print(f"no such corpus directory: {corpus_dir}")
        return 1

    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    # Build without the cached file so a stale cache cannot seed a new run.
    build(conn, novelty_path=None)

    states = [n for n in query.components_list(conn)
              if query.component_state_profile(conn, n) is not None
              and query.generate_scout_hypotheses(conn, n)]
    print(f"observing {len(states)} transformed states against {corpus_dir}...")
    for state in states:
        corpus.observe_hypotheses(conn, state, corpus_dir,
                                  search_date=date.today().isoformat())

    corpora = [dict(r) for r in conn.execute("SELECT * FROM corpora")]
    observations = [
        {
            "analogy_id": r["analogy_id"],
            "component": r["component"],
            "candidate": r["candidate"],
            "corpus_id": r["corpus_id"],
            "observed_count": r["observed_count"],
            "context_count": r["context_count"],
            "contexts": r["contexts"] or None,
            "target_covered": bool(r["target_covered"]),
            "candidate_covered": bool(r["candidate_covered"]),
            "result_class": r["result_class"],
            "observed_at": r["observed_at"],
        }
        for r in conn.execute(
            """SELECT o.*, c.name AS component, i.canonical_name AS candidate
               FROM novelty_observations o
               JOIN components c ON c.component_id = o.component_id
               JOIN ingredients i ON i.ingredient_id = o.candidate_ingredient_id
               ORDER BY c.name, i.canonical_name, o.analogy_id""")
    ]

    header = (
        "# Cached corpus measurements — GENERATED, do not hand-edit.\n"
        "#\n"
        "# Regenerate: py -3.11 scripts/observe_novelty.py <CulinaryDB dir>\n"
        "#\n"
        "# These are derived, unlike data/tastings.yaml: anyone with the corpus\n"
        "# can reproduce them. They are committed only because the corpus does\n"
        "# not ship with the app, so without this file every hypothesis reads\n"
        "# 'novelty not checked'.\n"
        "#\n"
        "# Absence is the claim worth trusting. A zero here means two ingredients\n"
        "# the corpus knows never appear in one recipe. A high count means little:\n"
        "# popular ingredients co-occur with everything.\n"
    )
    NOVELTY_PATH.write_text(
        header + yaml.safe_dump({"corpora": corpora, "observations": observations},
                                sort_keys=False, allow_unicode=True),
        encoding="utf-8")

    counts: dict[str, int] = {}
    for o in observations:
        counts[o["result_class"]] = counts.get(o["result_class"], 0) + 1
    print(f"wrote {len(observations)} observations to {NOVELTY_PATH}")
    for k in sorted(counts, key=lambda k: -counts[k]):
        print(f"   {k:22} {counts[k]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
