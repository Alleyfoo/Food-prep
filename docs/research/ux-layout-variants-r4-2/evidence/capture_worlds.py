"""Capture the colour worlds on identical states (desktop, 1440 x 900).

    py -3.11 docs/research/ux-layout-variants-r4-2/prototype/run.py
    py -3.11 docs/research/ux-layout-variants-r4-2/evidence/capture_worlds.py

Only the URL key `pal` differs between shots: peach (the previous, food-
coloured palette), white, cool, pantry. Writes screenshots/worlds/<state>/<pal>.png
and screenshots/worlds/side-by-side/<state>.png (peach, white, cool,
pantry, left to right).
"""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "screenshots" / "worlds"
BASE = "http://localhost:8543/?"
WORLDS = ("peach", "white", "cool", "pantry")
CTX = ("ingredient=broccoli&have=yogurt,lemon,garlic&rec=roasted_broccoli_component"
       "&cmp=roasted_broccoli_component,steamed_broccoli_component&trace=ingredient:lemon&ov=c")
STATES = {
    "detail": f"{CTX}&pane=detail",
    "compare": f"{CTX}&pane=compare",
    "trace": f"{CTX}&pane=trace",
    "circle": f"{CTX}&pane=circle&tcb=roasted_broccoli_component&tc=sour:lemon&tcx=aromatic",
}


def main() -> None:
    (OUT / "side-by-side").mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch()
        page = b.new_page(viewport={"width": 1440, "height": 900})
        for state, q in STATES.items():
            (OUT / state).mkdir(exist_ok=True)
            shots = []
            for pal in WORLDS:
                page.goto(f"{BASE}{q}&pal={pal}")
                page.wait_for_selector("text=Prepared ingredient", timeout=30000)
                page.wait_for_timeout(3500)
                if state == "circle":
                    frame = page.locator("iframe[title*='taste_circle']")
                    if frame.count():
                        frame.first.scroll_into_view_if_needed()
                        page.wait_for_timeout(800)
                path = OUT / state / f"{pal}.png"
                page.screenshot(path=str(path))
                shots.append(path)
                print(state, pal, "ok")
            imgs = [Image.open(s) for s in shots]
            w, h = imgs[0].size
            sheet = Image.new("RGB", (w * len(imgs) + 20 * (len(imgs) - 1), h + 28), "white")
            d = ImageDraw.Draw(sheet)
            for i, (im, pal) in enumerate(zip(imgs, WORLDS)):
                x = i * (w + 20)
                sheet.paste(im, (x, 28))
                d.text((x + 6, 8), f"{state} · pal={pal}", fill=(20, 20, 20))
            sheet.save(OUT / "side-by-side" / f"{state}.png")
        b.close()


if __name__ == "__main__":
    main()
