"""Write R3's generated tables under the current (amended) validator.

    py -3.11 docs/research/r3-construction-modelling/run.py            # *-a1.md tables
    py -3.11 docs/research/r3-construction-modelling/run.py --freeze   # refused: the freeze exists

The original R3 tables, `validation-tables.md` (written at e8a2e54) and
`generalisation-tables.md` (written at 6beda68), are historical evidence of
the experiment and are never regenerated: this script refuses to write them.
It writes the tables under the current validator, as amended by A1 (the PR #7
review), to `validation-tables-a1.md` and `generalisation-tables-a1.md`, and
compares every route with the original table.

--freeze was run once (commit e8a2e54), when the schema was frozen before the
held-out dishes were represented. It refuses to overwrite that manifest. A
later correction is a documented amendment in
src/foodprep/data/construction_freeze_amendments.yaml. A later round that
changes the schema on purpose writes a new freeze under a new name and says so.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))

import yaml  # noqa: E402

from foodprep import constructions as c  # noqa: E402

HERE = Path(__file__).resolve().parent
HELD_OUT = ["draniki", "kolokythokeftedes", "chawanmushi", "farcis_nicois",
            "pierogi_ruskie", "spanakopita", "zha_qie_he", "moi_moi"]
AMENDMENT = "A1"
AMENDMENT_DATE = "2026-11-24"
AMENDMENT_WHAT = ("recombination needs two materials of the same origin, each entering the "
                  "dish by its own route; edibility is checked at every join")
# split, original R3 table (never rewritten), title
TABLES = (("design", "validation-tables.md", "Design set"),
          ("held_out", "generalisation-tables.md", "Held-out set"))


def original_rows(name: str) -> dict:
    """(dish name, route) -> (verdict, recombination) read from an original R3 table."""
    out = {}
    for line in (HERE / name).read_text(encoding="utf-8").splitlines():
        cells = [x.strip() for x in line.strip().strip("|").split("|")]
        if len(cells) == 9 and cells[0] not in ("Dish", "---"):
            out[(cells[0], cells[1])] = (cells[7].strip("*"), cells[6])
    return out


def route_rows(split: str, original: dict) -> list[str]:
    data = c.load()
    rows = ["| Dish | Route | Patterns | Recipes | Steps (applicable / conditional / other) "
            "| Claims checked | Recombination | Verdict | What is missing "
            "| Original R3 verdict | Change from the original R3 table |",
            "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    for d in c.dish_ids(split):
        rep = c.validate(d)
        for rid, r in rep.routes.items():
            route = data["dishes"][d]["routes"][rid]
            name = data["dishes"][d]["name"]
            st = [s.status for s in r.steps]
            steps = f"{st.count('applicable')} / {st.count('conditional')} / " \
                    f"{len(st) - st.count('applicable') - st.count('conditional')}"
            rec = "; ".join(f"{s} [{o}] -> {m}" for s, _, o, m in r.recombinations) or "-"
            missing = [*(f"failure: {x}" for x in r.failures),
                       *(f"unknown: {x}" for x in r.unknowns),
                       *(f"unaccounted: {x}" for x in r.unaccounted),
                       *(f"model gap: {x}" for x in r.model_gaps),
                       *(f"error: {x}" for x in r.errors)]
            was = original.get((name, rid))
            if was is None:
                change = "not in the original table"
            else:
                diffs = ([f"verdict {was[0]} -> {r.verdict}"] if was[0] != r.verdict else []) + \
                        ([f"recombination {was[1]} -> {rec}"] if was[1] != rec else [])
                change = "; ".join(diffs) or "no change"
            rows.append(f"| {name} | {rid} | "
                        f"{', '.join(route.get('patterns') or []) or '-'} | "
                        f"{', '.join(route['recipes'])} | {steps} | {len(r.claims)} | {rec} | "
                        f"**{r.verdict}** | {'<br>'.join(missing).replace('|', '/') or '-'} | "
                        f"{was[0] if was else '-'} | {change} |")
    return rows


def summary(split: str) -> list[str]:
    reps = {d: c.validate(d) for d in c.dish_ids(split)}
    routes = [r for rep in reps.values() for r in rep.routes.values()]
    dv = [rep.verdict for rep in reps.values()]
    rv = [r.verdict for r in routes]
    steps = [s for r in routes for s in r.steps]
    return [f"- Dishes: {len(reps)} ({dv.count('fully')} fully, {dv.count('partly')} partly, "
            f"{dv.count('not')} not represented).",
            f"- Routes: {len(routes)} ({rv.count('fully')} fully, {rv.count('partly')} partly, "
            f"{rv.count('not')} not).",
            f"- Steps assessed: {len(steps)}; applicable {sum(s.status == 'applicable' for s in steps)}, "
            f"conditional {sum(s.status == 'conditional' for s in steps)}, "
            f"inapplicable {sum(s.status == 'inapplicable' for s in steps)}, "
            f"unknown {sum(s.status == 'unknown' for s in steps)}.",
            f"- Claims checked (expects + final): {sum(len(r.claims) for r in routes)}; "
            f"recombination links found: {sum(len(r.recombinations) for r in routes)}."]


def write_tables() -> None:
    for split, name, title in TABLES:
        out = name.replace(".md", f"-{AMENDMENT.lower()}.md")
        rows = route_rows(split, original_rows(name))
        changed = sum(1 for r in rows[2:] if not r.rstrip().endswith("| no change |"))
        text = [f"# {title}: after the post-freeze validator amendment {AMENDMENT}", "",
                f"Generated by `run.py` on the validator as amended by {AMENDMENT} "
                f"({AMENDMENT_DATE}, PR #7 review: {AMENDMENT_WHAT}). Do not edit by hand.", "",
                f"The original R3 table, `{name}`, is kept unchanged as the historical record. "
                "The last two columns compare every route with it: "
                f"{len(rows) - 2 - changed} of {len(rows) - 2} routes unchanged, {changed} changed.",
                "", *summary(split), "", *rows, ""]
        (HERE / out).write_text("\n".join(text), encoding="utf-8")
        print(f"wrote {out}")


def write_freeze() -> None:
    if c.FREEZE_PATH.exists():
        raise SystemExit(f"{c.FREEZE_PATH.name} exists and is the R3 record; record a documented "
                         "amendment in construction_freeze_amendments.yaml instead")
    m = c.freeze_manifest()
    m = {"note": "R3 schema freeze: written by docs/research/r3-construction-modelling/run.py "
                 "--freeze before any held-out dish was represented. tests/test_constructions.py "
                 "fails if a held-out dish relies on anything changed after it.",
         "held_out": HELD_OUT, **m}
    c.FREEZE_PATH.write_text(yaml.safe_dump(m, sort_keys=False, allow_unicode=True, width=100),
                             encoding="utf-8")
    print(f"wrote {c.FREEZE_PATH.name}")


if __name__ == "__main__":
    write_tables()
    if "--freeze" in sys.argv:
        write_freeze()
