"""Capture the seven main views at desktop and narrow widths (research only).

Reuses scripts/capture_screenshots.py's pill helper and server boot, but sets
the viewport and uses a fresh browser page per view, so each capture starts
from the app's documented default state (broccoli / roasted broccoli, nothing
on hand). Run from the repo root:

    py -3.11 docs/research/ux-clarity-r2/evidence/capture_views.py
"""
from __future__ import annotations

import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "scripts"))
import capture_screenshots as cs  # noqa: E402

OUT = Path(__file__).resolve().parents[1] / "screenshots"
PORT = 8522
VIEWS = [
    ("Cook", "Ingredient Explorer", "1-ingredient-explorer"),
    ("Cook", "Component Explorer", "2-component-explorer"),
    ("Cook", "Plate Balance", "3-plate-balance"),
    ("Cook", "Taste Circle", "4-taste-circle"),
    ("Explore", "Map", "5-map"),
    ("Explore", "Journeys", "6-journeys"),
    ("Experiment", "Scout", "7-scout"),
]
# Optional: capture only some views, with a longer settle time, e.g.
#   capture_views.py 4-taste-circle   (WAIT=10). The 4 s default caught a
#   stale, faded frame of the previous view for Taste Circle.
ONLY = set(sys.argv[1:])
WAIT = 10 if ONLY else 4
SIZES = {"desktop": (1400, 2200), "narrow": (390, 2600)}


def main() -> int:
    from playwright.sync_api import sync_playwright
    env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1")
    proc = subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", "app.py", "--server.headless=true",
         f"--server.port={PORT}", "--browser.gatherUsageStats=false"],
        cwd=str(ROOT), env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        if not cs._wait_for_port("localhost", PORT, timeout=40):
            return 1
        time.sleep(3)
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)
            for size, (w, h) in SIZES.items():
                (OUT / size).mkdir(parents=True, exist_ok=True)
                for section, tab, name in VIEWS:
                    if ONLY and name not in ONLY:
                        continue
                    page = browser.new_page(viewport={"width": w, "height": h})
                    page.goto(f"http://localhost:{PORT}/", wait_until="networkidle")
                    page.wait_for_selector("text=Ingredient Foundry", timeout=20000)
                    time.sleep(1.5)
                    cs._pill(page, "section_rail_pills", section).click()
                    time.sleep(2)
                    pill = cs._pill(page, "tab_rail_pills", tab)
                    if pill.count():
                        pill.click()
                    time.sleep(WAIT)
                    page.screenshot(path=str(OUT / size / f"{name}.png"))
                    print("saved", size, name)
                    page.close()
            browser.close()
    finally:
        proc.terminate()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
