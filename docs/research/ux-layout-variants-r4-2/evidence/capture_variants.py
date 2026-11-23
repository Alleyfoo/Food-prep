"""Capture the R4.2 layout variants on identical states (desktop, 1440 x 900).

    py -3.11 -m streamlit run docs/research/ux-layout-variants-r4-2/prototype/app.py --server.port 8543
    py -3.11 docs/research/ux-layout-variants-r4-2/evidence/capture_variants.py

One prototype, one URL per state; only the condition keys differ:
  overview  ov=a | ov=b | ov=c      (sheet=full)
  sheet     sheet=full | sheet=dense (ov=b)

Writes
  screenshots/<state>/<condition>.png         first screen
  screenshots/side-by-side/<state>.png        conditions left to right
  screenshots/metrics.json, evidence/capture-output.txt

Metrics (mechanical, no scores):
  coded_glyphs        legend-dependent marks ●◐○◇✓≠☐☑⇄ in the page text
  legend_words        words in the overview legend row (0 = none)
  overview_rows_visible  overview rows fully visible in the first screen
  row_height_median   median overview row height, px
  overview_words      words in the overview table
  tooltip_only        overview cells whose names appear only in a tooltip
  pane_screens        right-pane content height in pane heights
  section_offsets     Detail: px from pane top to each numbered section
  sections_first_screen  Detail: section headings in the first pane screen
"""
from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "screenshots"
BASE = "http://localhost:8543/"
W, H = 1440, 900

BRO = "ingredient=broccoli&have=yogurt,lemon,garlic&rec=roasted_broccoli_component"
CAB = "ingredient=cabbage&have=lemon&rec=roasted_cabbage_component"
POT = "ingredient=potato&rec=smashed_roasted_potato_component"
OVERVIEW = {  # state -> query; conditions ov=a/b/c
    "complete-overview": BRO,
    "incomplete-overview": CAB,
    "sparse-overview": POT,
    "scan-cabbage-paired-lemon": "ingredient=cabbage&have=lemon&paired=lemon",
    "scan-potato-uncovered-roles": "ingredient=potato&gap=unpaired",
}
SHEET = {  # state -> query; conditions sheet=full/dense
    "complete-sheet": BRO,
    "incomplete-sheet": CAB,
    "sparse-sheet": POT,
}

MEASURE = r"""() => {
  const G = '●◐○◇✓≠☐☑⇄';
  const main = document.querySelector('[data-testid="stMain"]');
  const text = [...main.querySelectorAll('.r4')].map(e => e.innerText).join('\n');
  const sc = [...main.querySelectorAll('div')].filter(d => !d.closest('.r4')).filter(d => {
      const s = getComputedStyle(d); return /(auto|scroll)/.test(s.overflowY) &&
        d.clientHeight > 300 && d.scrollHeight >= d.clientHeight; })
    .sort((a, b) => a.getBoundingClientRect().left - b.getBoundingClientRect().left);
  const left = sc[0], right = sc[sc.length - 1];
  const out = {coded_glyphs: [...text].filter(c => G.includes(c)).length};
  if (left) {
    const lb = left.getBoundingClientRect();
    const table = left.querySelector('table.ov');
    const rows = table ? [...table.querySelectorAll('tbody tr')] : [];
    const vis = rows.filter(tr => { const r = tr.getBoundingClientRect();
      return r.top >= lb.top - 1 && r.bottom <= Math.min(lb.bottom, innerHeight) + 1; }).length;
    const hs = rows.map(r => r.getBoundingClientRect().height).sort((a, b) => a - b);
    const leg = table && table.querySelector('tr.legendrow');
    out.overview_rows_visible = `${vis} of ${rows.length}`;
    out.row_height_median = hs.length ? Math.round(hs[Math.floor(hs.length / 2)]) : null;
    out.overview_words = table ? table.querySelector('tbody').innerText.split(/\s+/).filter(Boolean).length : 0;
    out.legend_words = leg ? leg.innerText.split(/\s+/).filter(Boolean).length : 0;
    out.tooltip_only = table ? [...table.querySelectorAll('tbody [title]')].filter(e =>
        !e.closest('a') && e.getAttribute('title').length > 0).length : 0;
  }
  if (right) {
    const top = right.getBoundingClientRect().top + right.scrollTop;
    const hs = [...right.querySelectorAll('h4')].filter(h => /^\s*[1-8]/.test(h.innerText));
    out.pane_screens = +(right.scrollHeight / right.clientHeight).toFixed(2);
    out.section_offsets = hs.map(h => Math.round(h.getBoundingClientRect().top - top));
    out.sections_first_screen = out.section_offsets.filter(y => y < right.clientHeight).length;
  }
  out.errors = main.querySelectorAll('[data-testid="stException"]').length;
  return out;
}"""


def shoot(b, query: str, path: Path) -> dict:
    page = b.new_page(viewport={"width": W, "height": H})
    page.goto(BASE + "?" + query)
    page.wait_for_selector('[data-testid="stMain"]')
    page.wait_for_timeout(4500)
    m = page.evaluate(MEASURE)
    path.parent.mkdir(parents=True, exist_ok=True)
    page.screenshot(path=str(path))
    page.close()
    return m


def side_by_side(state: str, conds: list[str]) -> None:
    imgs = [Image.open(OUT / state / f"{c}.png") for c in conds]
    gap, bar = 16, 36
    img = Image.new("RGB", (sum(i.width for i in imgs) + gap * (len(imgs) - 1),
                            max(i.height for i in imgs) + bar), "white")
    d = ImageDraw.Draw(img)
    x = 0
    for c, i in zip(conds, imgs):
        img.paste(i, (x, bar))
        d.text((x + 10, 10), f"{state}  ·  {c}", fill="black")
        x += i.width + gap
    (OUT / "side-by-side").mkdir(parents=True, exist_ok=True)
    img.resize((img.width // 2, img.height // 2)).save(OUT / "side-by-side" / f"{state}.png",
                                                       optimize=True)


def main() -> None:
    metrics: dict = {}
    with sync_playwright() as p:
        b = p.chromium.launch()
        for state, q in OVERVIEW.items():
            conds = [f"ov-{x}" for x in "abc"]
            for c, x in zip(conds, "abc"):
                metrics.setdefault(state, {})[c] = shoot(b, f"{q}&ov={x}", OUT / state / f"{c}.png")
            side_by_side(state, conds)
        for state, q in SHEET.items():
            conds = ["sheet-full", "sheet-dense"]
            for c, x in zip(conds, ("full", "dense")):
                metrics.setdefault(state, {})[c] = shoot(b, f"{q}&sheet={x}", OUT / state / f"{c}.png")
            side_by_side(state, conds)
        b.close()
    (OUT / "metrics.json").write_text(json.dumps(metrics, indent=1, ensure_ascii=False),
                                      encoding="utf-8")
    lines = [f"{s:30s} {c:12s} {json.dumps(m, ensure_ascii=False)}"
             for s, cs in metrics.items() for c, m in cs.items()]
    (ROOT / "evidence" / "capture-output.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
