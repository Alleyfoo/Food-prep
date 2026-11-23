"""Capture R4 and R4.1 side by side on identical URLs (desktop, 1440 x 900).

    py -3.11 -m streamlit run docs/research/ux-integrated-r4/prototype/app.py   --server.port 8541
    py -3.11 -m streamlit run docs/research/ux-integrated-r4-1/prototype/app.py --server.port 8542
    py -3.11 docs/research/ux-integrated-r4-1/evidence/capture_compare.py

Both prototypes read the same URL keys, so every state is opened with the same
query string in both. Fresh page per shot.

Writes
  screenshots/r4/<name>.png, screenshots/r41/<name>.png   first screen
  screenshots/side-by-side/<name>.png                     R4 left, R4.1 right
  screenshots/metrics.json                                mechanical counts only
  evidence/capture-output.txt

Metrics (no scores, no human judgement):
  coded_glyphs        occurrences of R4's legend-dependent marks ●◐○◇✓≠☐☑⇄ in the page text
  glyph_kinds         which of those marks occur
  broken_words        words (3+ letters) in table cells rendered across two lines
  overview_rows_visible  overview rows fully visible in the first screen (of total)
  pane_screens        right-pane content height in pane heights (1.0 = no scrolling)
  section_offsets     Detail: px from the pane top to each numbered section heading
  sections_first_screen  Detail: numbered sections whose heading is in the first pane screen
  scope_repeats       "scope: not recorded" occurrences (case-insensitive)
  trace_table_y       Trace: px from the pane top to the first relationship row (null: none)
  graph_drawn         a Graphviz chart is on the page
  markers             overview rows carrying a detail / compare / trace marker
"""
from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "screenshots"
VERSIONS = {"r4": "http://localhost:8541/", "r41": "http://localhost:8542/"}
W, H = 1440, 900

RB, SB = "roasted_broccoli_component", "steamed_broccoli_component"
BRO = "ingredient=broccoli&have=yogurt,lemon,garlic"
CAB = "ingredient=cabbage&have=lemon"
POT = "ingredient=potato"
STATES = {
    # the three datasets, each in detail, matrix, trace step 1 and 2
    "complete-detail": f"{BRO}&rec={RB}",
    "complete-matrix": f"{BRO}&rec={RB}&cols=matrix",
    "complete-trace1": f"{BRO}&rec={RB}&pane=trace&trace=state:{RB}",
    "complete-trace2": f"{BRO}&rec={RB}&pane=trace&depth=2&trace=state:{RB}",
    "incomplete-detail": f"{CAB}&rec=roasted_cabbage_component",
    "incomplete-matrix": f"{CAB}&rec=roasted_cabbage_component&cols=matrix",
    "incomplete-trace2": f"{CAB}&rec=roasted_cabbage_component&pane=trace&depth=2"
                         "&trace=state:roasted_cabbage_component",
    "sparse-detail": f"{POT}&rec=smashed_roasted_potato_component",
    "sparse-matrix": f"{POT}&rec=smashed_roasted_potato_component&cols=matrix",
    "sparse-trace2": f"{POT}&rec=smashed_roasted_potato_component&pane=trace&depth=2"
                     "&trace=state:smashed_roasted_potato_component",
    # tasks K1-K7 (same start states as R4's comparison.md)
    "K1-scan-has-route": f"{BRO}&has=route",
    "K2-compare-roasted-steamed": f"{BRO}&rec={RB}&cmp={RB},{SB}&pane=compare",
    "K2-compare-differences-only": f"{BRO}&rec={RB}&cmp={RB},{SB}&pane=compare&diff=1",
    "K3-trace-lemon": f"{BRO}&rec={RB}&trace=ingredient:lemon&pane=trace&depth=2",
    "K4-explain-lemon-detail": f"{BRO}&rec={RB}",
    "K4-explain-source-roast-culinary": f"{BRO}&rec={RB}&trace=source:10&pane=trace",
    "K5-brown-butter-trace": f"{BRO}&rec={RB}&trace=ingredient:brown_butter&pane=trace&depth=2",
    "K6-sparse-potato": f"{POT}&rec=smashed_roasted_potato_component",
    "K6-compare-complete-vs-sparse": (f"{POT}&rec=roasted_potato_component&cmp="
                                      "roasted_potato_component,smashed_roasted_potato_component"
                                      "&pane=compare"),
    "K7-cabbage-paired-with-lemon": f"{CAB}&paired=lemon",
    "K7-cabbage-paired-with-lemon-matrix": f"{CAB}&paired=lemon&cols=matrix",
    # shared selection: inspected + compare set + trace focus at once
    "S-all-selections": f"{BRO}&rec={RB}&cmp={RB},{SB}&trace=ingredient:lemon&pane=detail",
}
# Detail states where scrolling to a section is measured
DETAIL = {k for k in STATES if k.endswith("-detail") or k in ("K4-explain-lemon-detail",
                                                                "K6-sparse-potato",
                                                                "S-all-selections")}

MEASURE = r"""() => {
  const G = '●◐○◇✓≠☐☑⇄';
  const main = document.querySelector('[data-testid="stMain"]');
  const text = [...main.querySelectorAll('.r4')].map(e => e.innerText).join('\n');
  const glyphs = [...text].filter(c => G.includes(c));
  // scroll containers: the overview (left) and the right-hand pane
  const sc = [...main.querySelectorAll('div')].filter(d => !d.closest('.r4')).filter(d => {
      const s = getComputedStyle(d); return /(auto|scroll)/.test(s.overflowY) &&
        d.clientHeight > 300 && d.scrollHeight >= d.clientHeight; })
    .sort((a, b) => a.getBoundingClientRect().left - b.getBoundingClientRect().left);
  const left = sc[0], right = sc[sc.length - 1];
  // words broken across lines inside table cells
  let broken = 0;
  for (const td of main.querySelectorAll('.r4 td, .r4 th')) {
    const w = document.createTreeWalker(td, NodeFilter.SHOW_TEXT);
    let n; while ((n = w.nextNode())) {
      const re = /[A-Za-zÀ-ÿ]{3,}/g; let mm;
      while ((mm = re.exec(n.data))) {
        const r = document.createRange(); r.setStart(n, mm.index); r.setEnd(n, mm.index + mm[0].length);
        const tops = new Set([...r.getClientRects()].filter(x => x.width > 0).map(x => Math.round(x.top)));
        if (tops.size > 1) broken++;
      }
    }
  }
  // overview rows fully visible in the first screen
  let rows = [], vis = 0;
  if (left) {
    const lb = left.getBoundingClientRect();
    rows = [...left.querySelectorAll('table tbody tr, table tr')].filter(tr =>
      tr.querySelector('a[title="Open its fact sheet"]'));
    vis = rows.filter(tr => { const r = tr.getBoundingClientRect();
      return r.top >= lb.top - 1 && r.bottom <= Math.min(lb.bottom, innerHeight) + 1; }).length;
  }
  const out = {
    coded_glyphs: glyphs.length, glyph_kinds: [...new Set(glyphs)].join(''),
    broken_words: broken,
    overview_rows_visible: `${vis} of ${rows.length}`,
    pane_screens: right ? +(right.scrollHeight / right.clientHeight).toFixed(2) : null,
    scope_repeats: (text.match(/scope: not recorded/gi) || []).length,
    graph_drawn: !!main.querySelector('[data-testid="stGraphVizChart"]'),
    markers: left ? left.querySelectorAll('.tag.t-sel, .tag.t-cmp, .tag.t-trace').length : 0,
    errors: main.querySelectorAll('[data-testid="stException"]').length,
  };
  if (right) {
    const top = right.getBoundingClientRect().top + right.scrollTop;
    const hs = [...right.querySelectorAll('h4')].filter(h => /^\s*[1-8]/.test(h.innerText));
    out.section_offsets = hs.map(h => Math.round(h.getBoundingClientRect().top - top));
    out.sections_first_screen = out.section_offsets.filter(y => y < right.clientHeight).length;
    const edge = right.querySelector('table.trace tr.edge, table.trace tr:nth-child(2)');
    out.trace_table_y = edge ? Math.round(edge.getBoundingClientRect().top - top) : null;
    out.pane_height = right.clientHeight;
  }
  return out;
}"""


def shoot(b, base: str, query: str, path: Path) -> dict:
    page = b.new_page(viewport={"width": W, "height": H})
    page.goto(base + "?" + query)
    page.wait_for_selector('[data-testid="stMain"]')
    page.wait_for_timeout(4500)
    m = page.evaluate(MEASURE)
    path.parent.mkdir(parents=True, exist_ok=True)
    page.screenshot(path=str(path))
    page.close()
    return m


def side_by_side(name: str) -> None:
    a = Image.open(OUT / "r4" / f"{name}.png")
    b = Image.open(OUT / "r41" / f"{name}.png")
    gap, bar = 16, 36
    img = Image.new("RGB", (a.width + b.width + gap, max(a.height, b.height) + bar), "white")
    img.paste(a, (0, bar))
    img.paste(b, (a.width + gap, bar))
    d = ImageDraw.Draw(img)
    d.text((10, 10), f"R4 baseline  ·  {name}", fill="black")
    d.text((a.width + gap + 10, 10), f"R4.1  ·  {name}", fill="black")
    (OUT / "side-by-side").mkdir(parents=True, exist_ok=True)
    img.resize((img.width // 2, img.height // 2)).save(OUT / "side-by-side" / f"{name}.png",
                                                       optimize=True)


def main() -> None:
    metrics: dict = {}
    with sync_playwright() as p:
        b = p.chromium.launch()
        for name, q in STATES.items():
            for v, base in VERSIONS.items():
                metrics.setdefault(name, {})[v] = shoot(b, base, q, OUT / v / f"{name}.png")
            side_by_side(name)
        b.close()
    (OUT / "metrics.json").write_text(json.dumps(metrics, indent=1, ensure_ascii=False),
                                      encoding="utf-8")
    lines = []
    for name, vs in metrics.items():
        for v, m in vs.items():
            lines.append(f"{name:40s} {v:4s} {json.dumps(m, ensure_ascii=False)}")
    (ROOT / "evidence" / "capture-output.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
