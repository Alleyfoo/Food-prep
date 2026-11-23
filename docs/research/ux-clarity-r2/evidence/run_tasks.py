"""Scripted walkthrough of task scripts T1-T5 on the E1 interface (research only).

Every task starts from a fresh browser page on a freshly started server: the
documented default state (Cook > Ingredient Explorer, broccoli / roasted
broccoli, nothing on hand, example plate in Plate Balance). Each step saves a
screenshot to ../screenshots/tasks/ and the visible main text to
task-logs/<task>-<step>.txt.

This follows the path an expert reviewer judges most likely for a first-time
cook. It is NOT a user test: it proves a path exists and records what is shown
along it, not whether a person would find it.

T5 writes a tasting. The server is started with FOODPREP_TASTINGS_PATH pointing
at a scratch copy, and the real tastings.yaml checksum is compared before and
after. Run from the repo root:

    py -3.11 docs/research/ux-clarity-r2/evidence/run_tasks.py
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

HERE = Path(__file__).resolve().parent
SHOTS = HERE.parent / "screenshots" / "tasks"
LOGS = HERE / "task-logs"
PORT = 8523
REAL = ROOT / "src" / "foodprep" / "data" / "tastings.yaml"


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


class Run:
    def __init__(self, page, task: str):
        self.page, self.task, self.n = page, task, 0

    def snap(self, label: str, wait: float = 3.0) -> None:
        time.sleep(wait)
        self.n += 1
        name = f"{self.task}-{self.n}-{label}"
        self.page.screenshot(path=str(SHOTS / f"{name}.png"), full_page=False)
        text = self.page.locator("section.main, [data-testid='stMain']").first.inner_text()
        (LOGS / f"{name}.txt").write_text(text, encoding="utf-8")
        print("  step", name)

    def pick(self, key: str, text: str) -> None:
        box = self.page.locator(f".st-key-{key} input").first
        box.click()
        box.fill(text)
        time.sleep(0.6)
        box.press("Enter")
        time.sleep(2.5)

    def pill(self, rail: str, label: str) -> None:
        cs._pill(self.page, rail, label).click()
        time.sleep(2.5)

    def click_text(self, text: str) -> None:
        self.page.get_by_text(text, exact=True).first.click()
        time.sleep(2.5)


def fresh(browser):
    page = browser.new_page(viewport={"width": 1400, "height": 1700})
    page.goto(f"http://localhost:{PORT}/", wait_until="networkidle")
    page.wait_for_selector("text=Ingredient Foundry", timeout=20000)
    time.sleep(3)
    return page


def t1(r: Run):
    r.snap("arrival")
    for item in ("yogurt", "lemon", "garlic"):  # click the box before each item
        r.pick("available_items", item)
    r.page.keyboard.press("Tab")  # close the menu without Escape (Escape clears)
    r.snap("after-on-hand", 4)
    r.page.mouse.wheel(0, 900)
    r.snap("scrolled")


def t2(r: Run):
    r.pill("tab_rail_pills", "Plate Balance")
    r.snap("plate-balance", 4)


def t3(r: Run):
    r.pill("tab_rail_pills", "Component Explorer")
    r.snap("component-explorer")
    r.pick("component_explorer_comp", "roasted tomato")
    r.snap("roasted-tomato", 4)
    r.page.mouse.wheel(0, 900)
    r.snap("roasted-tomato-routes")


def t4(r: Run):
    r.pill("section_rail_pills", "Experiment")
    r.snap("scout-arrival", 4)
    r.pick("tab_scout_component_select", "roasted cabbage")
    r.snap("roasted-cabbage", 4)


def t5(r: Run):
    r.pill("section_rail_pills", "Experiment")
    r.snap("scout-arrival", 4)
    r.click_text("Record a tasting")
    r.snap("form-open")
    p = r.page
    p.locator(".st-key-tasting_preparation input").fill("tossed one warm floret in brown butter")
    p.locator(".st-key-tasting_ratio input").fill("1 piece : 1/4 tsp")
    p.locator(".st-key-tasting_temperature input").fill("warm")
    p.locator(".st-key-tasting_observations textarea").fill(
        "Research walkthrough entry: nutty, still tasted of broccoli.")
    p.locator(".st-key-tasting_safety label").first.click()
    r.snap("form-filled", 1)
    p.get_by_role("button", name="Review tasting").click()
    r.snap("review", 4)
    p.get_by_role("button", name="Save permanently").click()
    r.snap("saved", 4)


TASKS = {"T1": t1, "T2": t2, "T3": t3, "T4": t4, "T5": t5}


def main() -> int:
    from playwright.sync_api import sync_playwright
    SHOTS.mkdir(parents=True, exist_ok=True)
    LOGS.mkdir(parents=True, exist_ok=True)
    scratch = Path(tempfile.mkdtemp(prefix="foodprep-r2-")) / "tastings.yaml"
    shutil.copy(REAL, scratch)
    before = sha(REAL)
    env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1",
               FOODPREP_TASTINGS_PATH=str(scratch))
    only = set(sys.argv[1:]) or set(TASKS)
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        for task, fn in TASKS.items():
            if task not in only:
                continue
            # A fresh server per task: no session state carries over.
            proc = subprocess.Popen(
                [sys.executable, "-m", "streamlit", "run", "app.py",
                 "--server.headless=true", f"--server.port={PORT}",
                 "--browser.gatherUsageStats=false"],
                cwd=str(ROOT), env=env,
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            try:
                if not cs._wait_for_port("localhost", PORT, timeout=40):
                    print("server did not start")
                    return 1
                time.sleep(3)
                print(task)
                page = fresh(browser)
                try:
                    fn(Run(page, task))
                except Exception as exc:  # record, keep going
                    print(f"  {task} stopped: {exc!r}")
                    page.screenshot(path=str(SHOTS / f"{task}-error.png"))
                page.close()
            finally:
                proc.terminate()
                proc.wait(timeout=20)
        browser.close()
    after = sha(REAL)
    added = scratch.read_text(encoding="utf-8")[len(REAL.read_text(encoding="utf-8")):]
    (LOGS / "T5-scratch-diff.txt").write_text(
        f"real tastings.yaml sha256 before {before}\n"
        f"real tastings.yaml sha256 after  {after}\n"
        f"unchanged: {before == after}\n\nappended to scratch copy:\n{added}",
        encoding="utf-8")
    print("real tastings.yaml unchanged:", before == after)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
