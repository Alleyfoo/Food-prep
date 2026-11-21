"""Capture screenshots of each Streamlit tab for the README.

Boots `streamlit run app.py` headless, opens it in a headless browser via
Playwright, picks each section and tab from the pill rails, and saves a PNG of
each into docs/screenshots/. Reproducible:  python scripts/capture_screenshots.py

The rails are styled radios, not ``role="tab"`` elements (they stopped being
tabs when the pill rail replaced ``st.tabs``), so they are clicked by label.

Requires Playwright + a Chromium or system Google Chrome. Falls back to the
system Chrome (channel="chrome") if a Playwright-managed chromium is missing.
"""

from __future__ import annotations

import os
import re
import socket
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "screenshots"
PORT = 8521
URL = f"http://localhost:{PORT}"

#: (section, tab, file). A single-tab section has no tab rail to click.
SHOTS = [
    ("Cook", "Ingredient Explorer", "cook_ingredient_explorer.png"),
    ("Cook", "Component Explorer", "cook_component_explorer.png"),
    ("Cook", "Plate Balance", "cook_plate_balance.png"),
    ("Cook", "Taste Circle", "cook_taste_circle.png"),
    ("Explore", "Map", "explore_map.png"),
    ("Explore", "Journeys", "explore_journeys.png"),
    ("Experiment", "Scout", "experiment_scout.png"),
]


def _pill(page, rail: str, label: str):
    """The pill with exactly this label in one rail (Explorer != Ingredient Explorer)."""
    return page.locator(f".st-key-{rail} label").filter(
        has_text=re.compile(rf"^\s*{re.escape(label)}\s*$"))


def _wait_for_port(host: str, port: int, timeout: float = 30.0) -> bool:
    end = time.time() + timeout
    while time.time() < end:
        try:
            with socket.create_connection((host, port), timeout=1):
                return True
        except OSError:
            time.sleep(0.4)
    return False


def main() -> int:
    from playwright.sync_api import sync_playwright

    OUT.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1")
    proc = subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", "app.py",
         "--server.headless=true", f"--server.port={PORT}",
         "--browser.gatherUsageStats=false"],
        cwd=str(ROOT), env=env,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    try:
        if not _wait_for_port("localhost", PORT, timeout=40):
            print("streamlit did not come up on port", PORT, file=sys.stderr)
            return 1
        time.sleep(3)  # let the app finish its first render

        with sync_playwright() as pw:
            browser = None
            for channel in (None, "chrome"):
                try:
                    browser = pw.chromium.launch(headless=True, channel=channel) \
                        if channel else pw.chromium.launch(headless=True)
                    print(f"launched chromium (channel={channel or 'default'})")
                    break
                except Exception as e:  # noqa: BLE001
                    print(f"channel={channel or 'default'} failed: {e}", file=sys.stderr)
            if browser is None:
                return 2
            page = browser.new_page(viewport={"width": 1320, "height": 1000},
                                    device_scale_factor=1.5)
            page.goto(URL, wait_until="networkidle", timeout=30000)
            # wait for the topbar to render
            page.wait_for_selector("text=Ingredient Foundry", timeout=20000)
            time.sleep(1.5)

            for section, tab, fname in SHOTS:
                _pill(page, "section_rail_pills", section).click()
                time.sleep(2.0)
                tab_pill = _pill(page, "tab_rail_pills", tab)
                if tab_pill.count():
                    tab_pill.click()
                # graphs and the taste circle draw after the script finishes
                time.sleep(4.0)
                out_path = OUT / fname
                page.screenshot(path=str(out_path))
                print(f"  saved {out_path.relative_to(ROOT)}")
            browser.close()
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            proc.kill()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())