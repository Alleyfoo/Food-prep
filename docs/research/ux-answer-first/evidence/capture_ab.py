"""Capture and measure Ingredient Explorer scenarios for E3 (A/B).

    py -3.11 docs/research/ux-answer-first/evidence/capture_ab.py <label> [A|B]

<label> names the output folder (baseline, A, B). The second argument sets
FOODPREP_EXPLORER_VARIANT for the server; the baseline build ignores it.

Each scenario runs in a fresh server and a fresh page, so nothing carries
over. The page is rendered in a tall viewport (nothing scrolls), and a
first-screen crop is saved alongside the full capture:
  desktop first screen 1400x900, phone first screen 390x844.

Measurements are mechanical, not usability scores:
  target_y        px from the top of the page to the first element whose own
                  text contains the scenario's target phrase
  screens         target_y / first-screen height (1.0 = just below the fold)
  chips_above     .chip elements drawn above the target (things to scan past)
  lead            the prepared ingredient on the accent-bordered card
  stale           occurrences of the previous subject in the main area (T4)
  (target search covers .card and .answer-first only: strip and hints excluded)
Results: <label>/metrics.json, screenshots <label>/<scenario>-<width>[-full].png
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "scripts"))
import capture_screenshots as cs  # noqa: E402

PORT = 8531
SHOTS = Path(__file__).resolve().parents[1] / "screenshots"
WIDTHS = {"desktop": (1400, 900), "phone": (390, 844)}
TALL = 5200

MEASURE = """(target) => {
  const main = document.querySelector('[data-testid="stMain"]') || document.body;
  const top0 = main.getBoundingClientRect().top;
  let y = null;
  // Only content counts: cards and the answer panel, never the context
  // strip, pickers or hints, which merely name the subject.
  if (target) {
    for (const box of main.querySelectorAll('.card, .answer-first')) {
      const walker = document.createTreeWalker(box, NodeFilter.SHOW_TEXT);
      let hit = null;
      while (walker.nextNode()) {
        const n = walker.currentNode;
        if (n.textContent.toLowerCase().includes(target.toLowerCase())) {
          const r = n.parentElement.getBoundingClientRect();
          if (r.height > 0) { hit = Math.round(r.top - top0); break; }
        }
      }
      if (hit !== null && (y === null || hit < y)) y = hit;
    }
  }
  const chips = [...main.querySelectorAll('.chip')].filter(c => {
    const r = c.getBoundingClientRect();
    return r.height > 0 && (y === null || r.top - top0 < y);
  }).length;
  const lead = main.querySelector('.card.lead .card-comp');
  return {target_y: y, chips_above: y === null ? null : chips,
          lead: lead ? lead.textContent.trim() : null};
}"""


def boot(variant: str | None):
    env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1")
    if variant:
        env["FOODPREP_EXPLORER_VARIANT"] = variant
    proc = subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", "app.py", "--server.headless=true",
         f"--server.port={PORT}", "--browser.gatherUsageStats=false"],
        cwd=str(ROOT), env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if not cs._wait_for_port("localhost", PORT, timeout=40):
        proc.terminate()
        raise SystemExit("server did not start")
    time.sleep(3)
    return proc


def open_page(browser, width: int, query: str = ""):
    page = browser.new_page(viewport={"width": width, "height": TALL})
    page.goto(f"http://localhost:{PORT}/{query}", wait_until="networkidle")
    page.wait_for_selector("text=Ingredient Foundry", timeout=20000)
    time.sleep(4)
    return page


def pick(page, key: str, text: str) -> None:
    box = page.locator(f".st-key-{key} input").first
    box.click()
    box.fill(text)
    time.sleep(0.6)
    box.press("Enter")
    time.sleep(3)


def have(page, items) -> None:
    for item in items:
        pick(page, "available_items", item)
    page.keyboard.press("Tab")      # Escape would clear the list
    time.sleep(3)


def shoot(page, out: Path, name: str, first_h: int) -> None:
    page.screenshot(path=str(out / f"{name}-full.png"), full_page=False,
                    clip={"x": 0, "y": 0, "width": page.viewport_size["width"],
                          "height": min(TALL, 3600)})
    page.screenshot(path=str(out / f"{name}.png"), full_page=False,
                    clip={"x": 0, "y": 0, "width": page.viewport_size["width"],
                          "height": first_h})


def measure(page, target: str | None, first_h: int, stale: str | None = None) -> dict:
    m = page.evaluate(MEASURE, target)
    m["screens"] = (round(m["target_y"] / first_h, 2)
                    if m["target_y"] is not None else None)
    if stale:
        text = page.locator('[data-testid="stMain"]').inner_text().lower()
        # The strip and pickers are not the answer; count the whole main area
        # and report it, the reader can check the screenshot.
        m["stale"] = text.count(stale.lower())
    return m


# scenario -> (url query, on-hand items, target phrase, setup)
def t1(page):  have(page, ["yogurt", "lemon", "garlic"])


def t4(page):
    have(page, ["yogurt", "lemon", "garlic"])
    cs._pill(page, "tab_rail_pills", "Component Explorer").click()
    time.sleep(3)
    pick(page, "component_explorer_comp", "roasted cabbage")
    cs._pill(page, "tab_rail_pills", "Ingredient Explorer").click()
    time.sleep(4)


SCENARIOS = {
    "default": ("", None, None, None),
    "T1-broccoli-on-hand": ("", t1, "creamy and acidic", None),
    "T2-roasted-tomato": ("?tab=ingredient-explorer&state=roasted_tomato_component",
                          None, "basil", None),
    "T3-smashed-potato": ("?tab=ingredient-explorer&state=smashed_roasted_potato_component",
                          None, "smashed roasted potato", None),
    "T4-switch-to-roasted-cabbage": ("", t4, "roasted cabbage", "broccoli"),
}


def main() -> int:
    from playwright.sync_api import sync_playwright
    label = sys.argv[1]
    variant = sys.argv[2] if len(sys.argv) > 2 else None
    only = set(sys.argv[3:])
    out = SHOTS / label
    out.mkdir(parents=True, exist_ok=True)
    metrics_path = out / "metrics.json"
    metrics = json.loads(metrics_path.read_text()) if metrics_path.exists() else {}
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        for name, (query, setup, target, stale) in SCENARIOS.items():
            if only and name not in only:
                continue
            for wname, (w, first_h) in WIDTHS.items():
                proc = boot(variant)
                try:
                    page = open_page(browser, w, query)
                    if setup:
                        setup(page)
                    shoot(page, out, f"{name}-{wname}", first_h)
                    metrics[f"{name}-{wname}"] = measure(page, target, first_h, stale)
                    print(label, name, wname, metrics[f"{name}-{wname}"])
                    page.close()
                finally:
                    proc.terminate()
                    proc.wait(timeout=20)
        browser.close()
    metrics_path.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
