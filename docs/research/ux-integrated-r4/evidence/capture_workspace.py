"""Capture the R4 workspace on the same data as R3 (desktop only, 1440 x 900).

    py -3.11 -m streamlit run docs/research/ux-integrated-r4/prototype/app.py --server.port 8541
    py -3.11 docs/research/ux-integrated-r4/evidence/capture_workspace.py

Fresh page per shot; all state comes from the URL.
  <name>.png       the first screen as a person sees it (panes scroll inside)
  <name>-full.png  the same state with `full=1` (no inner scrolling), to read
                   the whole content and its order
metrics.json holds mechanical counts only, never scores:
  first_screen_panes   which panes have content visible in the first screen
  gap_markers          elements that say plainly that something is not recorded
  links                navigable entity links in the page (one click each)
  full_height_screens  length of the full=1 page in 900 px screens
"""
from __future__ import annotations

import json
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = "http://localhost:8541/"
OUT = Path(__file__).resolve().parents[1] / "screenshots"
W, H, TALL = 1440, 900, 7000

RB, SB = "roasted_broccoli_component", "steamed_broccoli_component"
DATASETS = {
    "complete-roasted-broccoli": "ingredient=broccoli&have=yogurt,lemon,garlic&rec=" + RB,
    "incomplete-roasted-cabbage": "ingredient=cabbage&have=lemon&rec=roasted_cabbage_component",
    "sparse-smashed-roasted-potato": "ingredient=potato&rec=smashed_roasted_potato_component",
}
VIEWS = {
    "detail": "",
    "matrix": "&cols=matrix",
    "evidence": "&cols=evidence",
    "trace": "&pane=trace&trace=state:{rec}",
    "trace-depth2": "&pane=trace&depth=2&trace=state:{rec}",
}
BRO = "ingredient=broccoli&have=yogurt,lemon,garlic"
TASKS = {
    "K1-scan-has-route": f"{BRO}&has=route",
    "K2-compare-roasted-steamed": f"{BRO}&rec={RB}&cmp={RB},{SB}&pane=compare",
    "K2-compare-differences-only": f"{BRO}&rec={RB}&cmp={RB},{SB}&pane=compare&diff=1",
    "K3-trace-lemon": f"{BRO}&rec={RB}&trace=ingredient:lemon&pane=trace&depth=2",
    "K4-explain-source-roast-culinary": f"{BRO}&rec={RB}&trace=source:10&pane=trace",
    "K5-brown-butter-trace": f"{BRO}&rec={RB}&trace=ingredient:brown_butter&pane=trace&depth=2",
    "K6-sparse-potato": "ingredient=potato&rec=smashed_roasted_potato_component",
    "K6-compare-complete-vs-sparse": ("ingredient=potato&rec=roasted_potato_component&cmp="
                                      "roasted_potato_component,smashed_roasted_potato_component"
                                      "&pane=compare"),
    "K7-cabbage-paired-with-lemon": "ingredient=cabbage&have=lemon&paired=lemon",
    "K7-cabbage-paired-with-lemon-matrix": "ingredient=cabbage&have=lemon&paired=lemon&cols=matrix",
    "E3-answer-summary-on": f"{BRO}&rec={RB}&answer=1",
}

MEASURE = """() => {
  const main = document.querySelector('[data-testid="stMain"]') || document.body;
  const vis = (sel) => [...main.querySelectorAll(sel)].some(e => {
      const r = e.getBoundingClientRect(); return r.height > 0 && r.top < %d && r.bottom > 0; });
  return {
    gap_markers: main.querySelectorAll('.nr, .gapbox').length,
    links: main.querySelectorAll('.r4 a[href^="?"]').length,
    first_screen_panes: {
      overview: vis('.r4 table tr td a[title="Open its fact sheet"]'),
      detail: vis('.r4 h4'), compare: vis('.r4 td.diff, .r4 tr.same'),
      trace: vis('[data-testid="stGraphVizChart"]') ||
             [...main.querySelectorAll('.r4 h3')].some(h => h.textContent.startsWith('Trace:'))},
    errors: main.querySelectorAll('[data-testid="stException"]').length
  };
}""" % H


def shoot(b, query: str, path: Path) -> dict:
    page = b.new_page(viewport={"width": W, "height": H})
    page.goto(BASE + "?" + query)
    page.wait_for_selector('[data-testid="stMain"]')
    page.wait_for_timeout(4500)
    m = page.evaluate(MEASURE)
    page.screenshot(path=str(path) + ".png")
    page.close()
    page = b.new_page(viewport={"width": W, "height": TALL})
    page.goto(BASE + "?" + query + "&full=1")
    page.wait_for_selector('[data-testid="stMain"]')
    page.wait_for_timeout(4500)
    h = page.evaluate("""() => Math.ceil(document.querySelector('[data-testid="stMainBlockContainer"]')
                                 .getBoundingClientRect().bottom) + 40""")
    m["full_height_screens"] = round(h / H, 2)
    page.screenshot(path=str(path) + "-full.png", clip={"x": 0, "y": 0, "width": W,
                                                        "height": min(h, TALL)})
    page.close()
    return m


def main():
    metrics = {}
    with sync_playwright() as p:
        b = p.chromium.launch()
        for ds, q in DATASETS.items():
            (OUT / ds).mkdir(parents=True, exist_ok=True)
            rec = q.split("rec=")[1]
            for view, extra in VIEWS.items():
                metrics[f"{ds}/{view}"] = shoot(b, q + extra.format(rec=rec), OUT / ds / view)
        (OUT / "tasks").mkdir(parents=True, exist_ok=True)
        for name, q in TASKS.items():
            metrics[f"tasks/{name}"] = shoot(b, q, OUT / "tasks" / name)
        b.close()
    (OUT / "metrics.json").write_text(json.dumps(metrics, indent=1))
    for k, v in metrics.items():
        print(k, v)


if __name__ == "__main__":
    main()
