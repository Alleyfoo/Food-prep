"""The product's Taste Circle component, served with a transparent page.

The product's component (src/foodprep/ui/taste_circle_component/) paints its
iframe a fixed page colour (#F5F5EB, oat, since the pantry port), which would carry the food tint into
every colour world. Rather than change src/, the prototype builds its own
copy at start-up: the product's index.html with only the background made
transparent, and the product's vendored vis-network, in a temp folder. The
copy is generated, never committed, so it cannot drift from the product.
"""
from __future__ import annotations

import shutil
import tempfile
from pathlib import Path
from typing import Any

import streamlit.components.v1 as components

import foodprep.ui

SRC = Path(foodprep.ui.__file__).resolve().parent / "taste_circle_component"
PRODUCT_BG = "background: #F5F5EB;"


def frontend_dir() -> Path:
    out = Path(tempfile.gettempdir()) / "r42_taste_circle_frontend"
    out.mkdir(exist_ok=True)
    html = (SRC / "index.html").read_text(encoding="utf-8")
    if PRODUCT_BG in html:                      # otherwise serve the product page as it is
        html = html.replace(PRODUCT_BG, "background: transparent;", 1)
    target = out / "index.html"
    if not target.exists() or target.read_text(encoding="utf-8") != html:
        target.write_text(html, encoding="utf-8")
    js_src, js_out = SRC / "vis-network.min.js", out / "vis-network.min.js"
    if not js_out.exists() or js_out.stat().st_size != js_src.stat().st_size:
        shutil.copyfile(js_src, js_out)
    return out


_component = components.declare_component("r42_taste_circle", path=str(frontend_dir()))


def taste_circle_map(nodes: list[dict[str, Any]], edges: list[dict[str, Any]], *,
                     height: int = 640, key: str) -> dict[str, Any] | None:
    """Same contract as foodprep.ui.taste_circle.taste_circle_map."""
    return _component(nodes=nodes, edges=edges, height=height, key=key, default=None)
