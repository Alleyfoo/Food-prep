"""After-captures of the two E3 repairs (Taste Circle arrows, tasting form).

    py -3.11 docs/research/ux-answer-first/evidence/capture_repairs.py

The tasting is saved to a temporary copy via FOODPREP_TASTINGS_PATH; the real
tastings.yaml checksum is printed before and after.
"""
from __future__ import annotations

import hashlib
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "scripts"))
import capture_screenshots as cs  # noqa: E402

PORT = 8532
OUT = Path(__file__).resolve().parents[1] / "screenshots" / "repairs"
REAL = ROOT / "src" / "foodprep" / "data" / "tastings.yaml"


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> int:
    from playwright.sync_api import sync_playwright
    OUT.mkdir(parents=True, exist_ok=True)
    scratch = Path(tempfile.mkdtemp(prefix="foodprep-e3-")) / "tastings.yaml"
    shutil.copy(REAL, scratch)
    before = sha(REAL)
    env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1",
               FOODPREP_TASTINGS_PATH=str(scratch))
    proc = subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", "app.py", "--server.headless=true",
         f"--server.port={PORT}", "--browser.gatherUsageStats=false"],
        cwd=str(ROOT), env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        if not cs._wait_for_port("localhost", PORT, timeout=40):
            return 1
        time.sleep(3)
        with sync_playwright() as pw:
            b = pw.chromium.launch(headless=True)
            page = b.new_page(viewport={"width": 1400, "height": 900})
            page.goto(f"http://localhost:{PORT}/?tab=taste-circle&state=roasted_broccoli_component",
                      wait_until="networkidle")
            time.sleep(8)
            page.screenshot(path=str(OUT / "taste-circle-arrows.png"))
            page.get_by_role("button", name="roasted cabbage ▶").click()
            time.sleep(8)
            page.screenshot(path=str(OUT / "taste-circle-after-step.png"))
            page.close()

            page = b.new_page(viewport={"width": 1400, "height": 1700})
            page.goto(f"http://localhost:{PORT}/?tab=scout&state=roasted_broccoli_component",
                      wait_until="networkidle")
            time.sleep(6)
            page.get_by_text("Record a tasting", exact=True).first.click()
            time.sleep(3)
            page.locator(".st-key-tasting_preparation input").fill("one warm floret")
            page.locator(".st-key-tasting_temperature input").fill("warm")
            page.locator(".st-key-tasting_observations textarea").fill("E3 capture entry.")
            page.locator(".st-key-tasting_safety label").first.click()
            page.get_by_role("button", name="Review tasting").click()
            time.sleep(4)
            page.screenshot(path=str(OUT / "tasting-no-verdict.png"))
            box = page.locator(".st-key-tasting_verdict input").first
            box.click()
            box.fill("Promising")
            time.sleep(0.6)
            box.press("Enter")
            time.sleep(1)
            page.get_by_role("button", name="Review tasting").click()
            time.sleep(4)
            page.get_by_role("button", name="Save permanently").click()
            time.sleep(5)
            page.screenshot(path=str(OUT / "tasting-saved.png"))
            page.close()
            b.close()
    finally:
        proc.terminate()
    print("real tastings.yaml unchanged:", sha(REAL) == before)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
