"""Text counts for R4 and R4.1, rendered from the same model (no browser).

    PYTHONIOENCODING=utf-8 py -3.11 docs/research/ux-integrated-r4-1/evidence/text_counts.py

Prints, per dataset: legend-dependent glyphs and words in each overview
column set; fact-sheet words and repetition counts; compare glyphs; trace
sizes and where R4.1 puts the graph. Mechanical counts only.
"""
from __future__ import annotations

import re
import sqlite3
import sys
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path[:0] = [str(ROOT / "docs/research/ux-integrated-r4-1/prototype"),
                str(ROOT / "docs/research/ux-integrated-r4/prototype"), str(ROOT / "src")]

from foodprep import loader, query  # noqa: E402
import r4_model as M  # noqa: E402
import r4_state as S4  # noqa: E402
import r4_views as V4  # noqa: E402
import r41_state as S  # noqa: E402
import r41_views as V  # noqa: E402

G = "●◐○◇✓≠☐☑⇄"
DATA = [("broccoli", ["yogurt", "lemon", "garlic"], "roasted_broccoli_component",
         "steamed_broccoli_component"),
        ("cabbage", ["lemon"], "roasted_cabbage_component", "braised_cabbage_component"),
        ("potato", [], "smashed_roasted_potato_component", "roasted_potato_component")]


def text(h: str) -> str:
    return re.sub(r"\s+", " ", unescape(re.sub(r"<[^>]+>", " ", h)))


def st(mod, ing, have, **kw):
    s = mod.parse({"ingredient": ing, "have": ",".join(have)})
    s.update(kw)
    return s


def glyphs(t: str) -> int:
    return sum(t.count(g) for g in G)


def main() -> None:
    c = sqlite3.connect(":memory:")
    c.row_factory = sqlite3.Row
    loader.build(c)
    for ing, have, rec, other in DATA:
        m = M.build(c, ing, have)
        print(f"== {ing} (on hand: {', '.join(have) or 'nothing'}) · record {rec}")
        for cols in ("summary", "matrix", "evidence"):
            a = text(V4.overview_html(m, st(S4, ing, have, cols=cols)))
            b = text(V.overview_html(m, st(S, ing, have, cols=cols)))
            print(f"  overview {cols:9s} glyphs {glyphs(a):3d} -> {glyphs(b):3d} · "
                  f"words {len(a.split()):4d} -> {len(b.split()):4d}")
        a = text(V4.detail_html(m, st(S4, ing, have, rec=rec), rec))
        b = text(V.detail_html(m, st(S, ing, have, rec=rec), rec))
        titles = {x["title"] for r in M.of(m, rec, ("pairing", "transformation"))
                  for x in r["evidence"]["sources"]}
        for label, f in (("words", lambda t: len(t.split())),
                         ("'scope: not recorded'", lambda t: t.lower().count("scope: not recorded")),
                         ("'not on hand'", lambda t: t.count("not on hand")),
                         ("source-title mentions", lambda t: sum(t.count(x) for x in titles)),
                         ("glyphs", glyphs)):
            print(f"  sheet {label:24s} {f(a):4d} -> {f(b):4d}")
        cm = [other, rec]
        a = text(V4.compare_html(m, st(S4, ing, have, cmp=cm)))
        b = text(V.compare_html(m, st(S, ing, have, cmp=cm)))
        print(f"  compare glyphs {glyphs(a)} -> {glyphs(b)} · rows "
              f"{len(V4.compare_rows(m, st(S4, ing, have, cmp=cm), cm))} -> "
              f"{len(V.compare_rows(m, st(S, ing, have, cmp=cm), cm))}")
        for d in (1, 2, 3):
            s = st(S, ing, have, trace=f"state:{rec}", depth=d)
            e, n = V.trace_edges(m, s)
            print(f"  trace step {d}: {len(e)} relationships / {len(n)} entities · "
                  f"graph {V.graph_placement(m, s)}")
    tot = over = 0
    for ing in query.tree_ingredients(c):
        m = M.build(c, ing, [])
        for s_ in m["states"]:
            for d in (1, 2, 3):
                s = st(S, ing, [], trace=f"state:{s_['component']}", depth=d)
                tot += 1
                over += len(V.trace_edges(m, s)[0]) > V.GRAPH_LIMIT
    print(f"== preparation traces above {V.GRAPH_LIMIT} relationships: {over} of {tot}")
    print(f"== matrix legend words: R4 {len(text(V4.LEGEND).split())} · "
          f"R4.1 {len(text(V._legend('matrix')).split())}")


if __name__ == "__main__":
    main()
