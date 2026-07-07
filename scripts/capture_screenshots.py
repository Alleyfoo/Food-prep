"""Capture screenshots of each Streamlit tab for the README.

Boots `streamlit run app.py` headless, opens it in a headless browser via
Playwright, clicks through the five tabs, and saves a full-page PNG of each
into docs/screenshots/. Reproducible:  python scripts/capture_screenshots.py

Requires Playwright + a Chromium or system Google Chrome. Falls back to the
system Chrome (channel="chrome") if a Playwright-managed chromium is missing.
"""

from __future__ import annotations

import os
import socket
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "screenshots"
PORT = 8521
URL = f"http://localhost:{PORT}"

TABS = [
    ("Ingredient Explorer", "tab1_ingredient_explorer.png"),
    ("Component Explorer", "tab2_component_explorer.png"),
    ("Plate Balance", "tab3_plate_balance.png"),
    ("Filler Profiles", "tab4_filler_profiles.png"),
    ("Scout", "tab5_scout.png"),
]


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
                                    device_scale_factor=2)
            page.goto(URL, wait_until="networkidle", timeout=30000)
            # wait for the topbar to render
            page.wait_for_selector("text=Ingredient Foundry", timeout=20000)
            time.sleep(1.5)

            for title, fname in TABS:
                page.get_by_role("tab", name=title).click()
                # wait for that tab's section title to appear, then settle
                try:
                    page.wait_for_selector(f"text={title}", timeout=10000)
                except Exception:
                    pass
                time.sleep(2.0)
                out_path = OUT / fname
                page.screenshot(path=str(out_path), full_page=True)
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