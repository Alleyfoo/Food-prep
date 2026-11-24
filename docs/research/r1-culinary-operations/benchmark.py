"""Benchmark: can the generator recover established preparations it was not
told about, and which way of presenting results finds them best?

Run from the repository root:

    py -3.11 docs/research/r1-culinary-operations/benchmark.py

Writes benchmark-results.md next to this file. About two minutes.

Variants (all over the same exploration, depth 3):

A  global ranking, as shipped (uses `established_on`)
B  global ranking without `established_on` (no answers in the score)
C  purpose-specific: per part and function, the k best (B's scores)
D  global ranking + sensory term from the curated transformations
E  purpose-specific + sensory term
F  purpose-specific, simplest first (fewest steps, least effort and equipment)
G  purpose-specific, simplest first, with the sensory term (flavour_shift)
H  global ranking B cut to F's length, and I global D cut to G's length: the
   fair controls for F and G, whose lists come out longer than C's

A list is only as useful as it is short, so every variant is compared at the
same budget: the number of distinct sequences the purpose-specific lists
show for that ingredient. Global variants are cut to that many.
"""

from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parents[2] / "src"))

from foodprep import operations as o  # noqa: E402
from foodprep import pair_counts as pc  # noqa: E402

K = 3   # sequences per (part, function) in purpose-specific lists


def final_material(item: dict, cat: o.Catalogue):
    """Apply the item's sequence; (material, None) or (None, reason)."""
    [m] = o.start_materials(item["ingredient"], item["part"], cat)
    for step in item["sequence"]:
        op, _, want = step.partition(":")
        a = o.assess(op, m, cat)
        if a.status not in o.TAKEN:
            return None, f"{op}: {a.status} ({a.explain()})"
        outs = o.apply(op, m, cat)
        m = next((x for x in outs if not want or x.path[-1].output == want), None)
        if m is None:
            return None, f"{op} has no output {want!r}"
    return m, None


def shown_global(rs: list, n: int) -> list:
    return rs[:n]


def shown_purpose(rs: list, order: str = "score") -> list:
    lists = o.by_function(rs, K, order)
    seen, out = set(), []
    for key in sorted(lists):
        for x in lists[key]:
            if id(x) not in seen:
                seen.add(id(x))
                out.append(x)
    return out


def main() -> int:
    cat = o.load()
    items = pc.load_yaml(HERE / "benchmark.yaml")["items"]
    ingredients = list(dict.fromkeys(i["ingredient"] for i in items))
    rows, summary = [], []
    totals = {v: 0 for v in "ABCDEFGHI"}
    fair = 0
    for ing in ingredients:
        ex = o.explore(ing, cat=cat)
        by_key = {r.material.key(): r for r in ex.results}
        lists = {
            "A": o.ranked(ing, cat=cat, exploration=ex)[0],
            "B": o.ranked(ing, cat=cat, exploration=ex, use_established=False)[0],
            "D": o.ranked(ing, cat=cat, exploration=ex, use_established=False, sensory=True)[0],
        }
        purpose_b = shown_purpose(lists["B"])
        purpose_d = shown_purpose(lists["D"])
        budget = len(purpose_b)
        shown = {
            "A": shown_global(lists["A"], budget),
            "B": shown_global(lists["B"], budget),
            "C": purpose_b,
            "D": shown_global(lists["D"], len(purpose_d)),
            "E": purpose_d,
            "F": shown_purpose(lists["B"], "simple"),
            "G": shown_purpose(lists["D"], "simple"),
        }
        shown["H"] = shown_global(lists["B"], len(shown["F"]))
        shown["I"] = shown_global(lists["D"], len(shown["G"]))
        shown_ids = {v: {id(x.result) for x in xs} for v, xs in shown.items()}
        pos = {v: {id(x.result): i for i, x in enumerate(lists[v])} for v in "ABD"}
        summary.append((ing, len(ex.results), {v: len(lists[v]) for v in "ABD"},
                        budget, len(purpose_d), len(shown["F"]), len(shown["G"])))
        for item in (i for i in items if i["ingredient"] == ing):
            m, why = final_material(item, cat)
            expected_block = item.get("expect") == "blocked"
            if m is None:
                rows.append((item, "blocked", why, {}, expected_block))
                continue
            r = by_key.get(m.key())
            if r is None:
                rows.append((item, "not reached", "", {}, expected_block))
                continue
            if not expected_block:
                fair += 1
            hits = {}
            for v in "ABCDEFGHI":
                base = {"C": "B", "E": "D", "F": "B", "G": "D", "H": "B", "I": "D"}.get(v, v)
                rank = pos[base].get(id(r))
                hits[v] = (rank, id(r) in shown_ids[v])
                if id(r) in shown_ids[v] and not expected_block:
                    totals[v] += 1
            rows.append((item, "generated", "", hits, expected_block))

    out = ["# Benchmark results",
           "",
           "Generated by `benchmark.py` from `benchmark.yaml`. Do not edit by hand.",
           "",
           "Variants:",
           "",
           "- **A:** global ranking as shipped",
           "- **B:** global without `established_on`",
           "- **C:** purpose-specific lists (B's scores, "
           f"{K} per part and function)",
           "- **D:** global + sensory term",
           "- **E:** purpose-specific + sensory",
           "- **F:** purpose-specific, simplest first",
           "- **G:** purpose-specific, simplest first, + sensory",
           "- **H:** global B cut to F's length; **I:** global D cut to G's length "
           "(fair controls)",
           "",
           "F and G show the same number of lists as C and E (one per part and function, "
           f"{K} each), so their budgets are close to C's and E's and are listed below.",
           "",
           "Each variant shows as many sequences as its purpose-specific counterpart (the "
           "budget). An item is **found** when it is among the sequences shown.",
           "",
           "## Summary",
           "",
           f"{fair} benchmark items reachable by the generator (blocked or expected-blocked "
           "items excluded).",
           "",
           "| Variant | found within budget | share |",
           "| --- | ---: | ---: |"]
    for v, label in (("A", "global, as shipped"), ("B", "global, no established_on"),
                     ("C", "purpose-specific"), ("D", "global + sensory"),
                     ("E", "purpose-specific + sensory"),
                     ("F", "purpose-specific, simplest first"),
                     ("G", "purpose-specific, simplest first, + sensory"),
                     ("H", "global B at F's length (control)"),
                     ("I", "global D at G's length (control)")):
        out.append(f"| {v} {label} | {totals[v]} | {totals[v] / fair:.0%} |")
    out += ["", "| Ingredient | distinct materials | ranked A / B / D | budget A,B,C | budget D,E | shown F | shown G |",
            "| --- | ---: | --- | ---: | ---: | ---: | ---: |"]
    for ing, n, ranked, b, bd, nf, ng in summary:
        out.append(f"| {ing} | {n} | {ranked['A']} / {ranked['B']} / {ranked['D']} | {b} | {bd} | {nf} | {ng} |")
    out += ["", "## Items", "",
            "Rank is the position in the full global list (0 = first; - = generated but not "
            "ranked). Found: ✓ within the budget, · not.",
            "",
            "| Item | Source | Status | A rank | B rank | D rank | A | B | C | D | E | F | G |",
            "| --- | --- | --- | ---: | ---: | ---: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |"]
    for item, status, why, hits, expected in rows:
        name = f"{item['id']} ({item['ingredient']} {item['part']})"
        if status != "generated":
            note = why or ""
            if expected:
                note = f"expected: {item['why']}"
            out.append(f"| {name} | {item['source']} | {status}: {note} | | | | | | | | | | |")
            continue

        def rk(v):
            r = hits[v][0]
            return "-" if r is None else str(r)

        def ok(v):
            return "✓" if hits[v][1] else "·"
        out.append(f"| {name} | {item['source']} | generated | {rk('A')} | {rk('B')} | {rk('D')} | "
                   + " | ".join(ok(v) for v in "ABCDEFG") + " |")
    (HERE / "benchmark-results.md").write_text("\n".join(out) + "\n", encoding="utf-8")
    print("\n".join(out[:30]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
