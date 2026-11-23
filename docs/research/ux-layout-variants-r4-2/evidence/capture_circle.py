"""Capture the embedded Taste Circle pane (desktop, 1440 x 900).

    py -3.11 -m streamlit run docs/research/ux-layout-variants-r4-2/prototype/app.py --server.port 8543
    py -3.11 docs/research/ux-layout-variants-r4-2/evidence/capture_circle.py

Every state is a URL; the circle's dish is held in tc / tcx (see r42_state).
Writes screenshots/circle/<state>.png: the first screen and, with the right
pane scrolled to the circle, <state>-circle.png.
"""
from __future__ import annotations

from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "screenshots" / "circle"
BASE = "http://localhost:8543/?"
BRO = "ingredient=broccoli&have=yogurt,lemon,garlic&ov=c&pane=circle"
REC = "roasted_broccoli_component"
STATES = {
    "empty": f"{BRO}&rec={REC}",
    "sour-open": f"{BRO}&rec={REC}&tcb={REC}&tcx=sour",
    "dish": f"{BRO}&rec={REC}&tcb={REC}&tc=sour:lemon,pungent:garlic,rich_fatty:yogurt",
    "no-profile": f"{BRO}&rec=raw_broccoli_component",
    "cabbage": "ingredient=cabbage&have=lemon&ov=c&pane=circle&rec=roasted_cabbage_component",
}


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch()
        page = b.new_page(viewport={"width": 1440, "height": 900})
        for name, q in STATES.items():
            page.goto(BASE + q)
            page.wait_for_selector("text=Taste circle", timeout=30000)
            page.wait_for_timeout(3500)          # the circle's iframe draws after the page
            page.screenshot(path=str(OUT / f"{name}.png"))
            frame = page.locator("iframe[title*='taste_circle']")
            if frame.count():
                frame.first.scroll_into_view_if_needed()
                page.wait_for_timeout(800)
                page.screenshot(path=str(OUT / f"{name}-circle.png"))
            print(name, "ok", "circle" if frame.count() else "no circle")
        b.close()


if __name__ == "__main__":
    main()
