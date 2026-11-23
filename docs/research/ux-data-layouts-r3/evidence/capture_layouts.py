"""Capture the R3 layouts on identical data (desktop only).

    py -3.11 -m streamlit run docs/research/ux-data-layouts-r3/prototype/app.py --server.port 8540
    py -3.11 docs/research/ux-data-layouts-r3/evidence/capture_layouts.py

Fresh page per shot; all state comes from the URL. Saves
screenshots/<dataset>/<layout>.png (first screen, 1440x900) and
<layout>-full.png, plus metrics.json with mechanical counts only:

  height_screens   full page height / 900
  gap_markers      elements that say plainly that something is not recorded
  status_badges    elements carrying an explicit epistemic status
  records_visible  prepared ingredients named in the first screen
"""
from __future__ import annotations

import json
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = "http://localhost:8540/"
OUT = Path(__file__).resolve().parents[1] / "screenshots"
W, H = 1440, 900

DATASETS = {
    "complete-roasted-broccoli": ("broccoli", "yogurt,lemon,garlic", "roasted_broccoli_component"),
    "incomplete-roasted-cabbage": ("cabbage", "lemon", "roasted_cabbage_component"),
    "sparse-smashed-roasted-potato": ("potato", "", "smashed_roasted_potato_component"),
}
LAYOUTS = {"table": "", "explorer": "&level=2", "workspace": "", "cards": ""}
TASKS = {  # extra task shots: (dataset, layout, extra query)
    "trace-lemon-across-broccoli": ("broccoli", "yogurt,lemon,garlic", "explorer", "&focus=lemon&level=2"),
    "compare-roasted-vs-steamed": ("broccoli", "yogurt,lemon,garlic", "workspace",
                                   "&compare=roasted_broccoli_component,steamed_broccoli_component"),
    "filter-has-route": ("broccoli", "yogurt,lemon,garlic", "table", "&has=flavour route"),
    "filter-paired-with-lemon-cabbage": ("cabbage", "lemon", "table", "&filler=lemon"),
}

MEASURE = """(names) => {
  const main = document.querySelector('[data-testid="stMain"]') || document.body;
  const txt = (el) => (el.innerText || '').toLowerCase();
  const gaps = [...main.querySelectorAll('.cell-nr, .st-nr, .gaps')].length
             + [...main.querySelectorAll('text')].filter(t => /nothing recorded|not recorded/.test(t.textContent)).length;
  const badges = main.querySelectorAll('.badge').length;
  const first = [...main.querySelectorAll('*')].filter(e => {
      const r = e.getBoundingClientRect(); return r.height > 0 && r.top >= 0 && r.bottom <= %d && e.children.length === 0; })
      .map(txt).join(' | ');
  const seen = names.filter(n => first.includes(n)).length;
  return {gap_markers: gaps, status_badges: badges, records_visible: seen};
}""" % H


TALL = 6000


def shoot(page, url, path, names):
    """Render in a tall viewport (Streamlit scrolls an inner container, so a
    normal full-page shot would clip), then crop the first screen."""
    page.goto(url)
    page.wait_for_selector('[data-testid="stMain"]')
    page.wait_for_timeout(5000)
    m = page.evaluate(MEASURE, names)
    h = page.evaluate("""() => { const b = document.querySelector('[data-testid="stMainBlockContainer"]')
                                   || document.querySelector('[data-testid="stMain"]');
                                 return Math.ceil(b.getBoundingClientRect().bottom) + 40; }""")
    m["height_screens"] = round(h / H, 2)
    page.screenshot(path=str(path) + ".png", clip={"x": 0, "y": 0, "width": W, "height": H})
    page.screenshot(path=str(path) + "-full.png",
                    clip={"x": 0, "y": 0, "width": W, "height": min(h, TALL)})
    return m


def main():
    import sqlite3, sys
    root = Path(__file__).resolve().parents[4]
    sys.path[:0] = [str(root / "src")]
    from foodprep import loader, query
    c = sqlite3.connect(":memory:"); c.row_factory = sqlite3.Row; loader.build(c)
    names = {ing: [x["component"].replace("_component", "").replace("_base", " base")
                   .replace("_", " ") for x in query.all_branch_cards(c, ing)]
             for ing in ("broccoli", "cabbage", "potato")}
    metrics = {}
    with sync_playwright() as p:
        b = p.chromium.launch()
        for ds, (ing, have, focus) in DATASETS.items():
            (OUT / ds).mkdir(parents=True, exist_ok=True)
            for lay, extra in LAYOUTS.items():
                page = b.new_page(viewport={"width": W, "height": TALL})
                url = f"{BASE}?ingredient={ing}&have={have}&layout={lay}&focus={focus}{extra}"
                metrics[f"{ds}/{lay}"] = shoot(page, url, OUT / ds / lay, names[ing])
                page.close()
        (OUT / "tasks").mkdir(parents=True, exist_ok=True)
        for name, (ing, have, lay, extra) in TASKS.items():
            page = b.new_page(viewport={"width": W, "height": TALL})
            url = f"{BASE}?ingredient={ing}&have={have}&layout={lay}{extra}"
            metrics[f"tasks/{name}"] = shoot(page, url, OUT / "tasks" / name, names[ing])
            page.close()
        b.close()
    (OUT / "metrics.json").write_text(json.dumps(metrics, indent=1))
    for k, v in metrics.items():
        print(k, v)


if __name__ == "__main__":
    main()
