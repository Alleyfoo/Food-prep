"""Streamlit wrapper for the Taste Circle Map custom component.

The frontend (``taste_circle_component/index.html``) is a static, no-build
component: it renders the circle with a vendored vis-network build and posts
node clicks back via the component v1 postMessage protocol. No CDN or npm
build step required, so it deploys to Streamlit Cloud as plain package data.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import streamlit.components.v1 as components

_FRONTEND_DIR = Path(__file__).parent / "taste_circle_component"

_taste_circle = components.declare_component(
    "taste_circle_map",
    path=str(_FRONTEND_DIR),
)


def taste_circle_map(
    nodes: list[dict[str, Any]],
    edges: list[dict[str, Any]],
    *,
    height: int = 640,
    key: str,
) -> dict[str, Any] | None:
    """Render the taste circle and return the latest click event.

    Returns ``{"id": <node id or None>, "t": <js timestamp>}`` after each
    click on a clickable node (or on blank canvas, where ``id`` is None),
    and ``None`` before the first click. Every click carries a unique
    timestamp, so repeated clicks on the same node are all delivered.
    """
    return _taste_circle(
        nodes=nodes,
        edges=edges,
        height=height,
        key=key,
        default=None,
    )
