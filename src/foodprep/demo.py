"""Five-flow demo of the food-prep engine.

Prints the five demo flows that give the concept in ~60 seconds — no browser
needed, just the query API. Run via ``foodprep demo`` or ``python scripts/demo.py``.

The flows:
  1. Tomato flow        — ingredient → technique → component → missing roles
  2. Stateful component  — start from an after-state, not raw ingredient
  3. Plate repair       — what a plate has, lacks, and what to add
  4. Cabbage guardrail  — sulfur is a risk/tag, never a missing role
  5. Scout              — experimental pairings only; taste before serving

This is the same data the Streamlit tabs render, in plain text.
"""

from __future__ import annotations

import sqlite3
import sys
from typing import Any, Callable

from . import query


def _ensure_utf8_stdout() -> None:
    """Force UTF-8 on stdout so box-drawing chars (═, →) don't crash on cp1252.

    The demo prints Unicode banners; on Windows the default stdout codec is
    cp1252, which can't encode them. Guarded so a non-reconfigurable stream
    (e.g. a test capture) is left untouched.
    """
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[union-attr]
    except Exception:  # noqa: BLE001 - reconfigure may be absent or refused
        pass


def _banner(out: Callable[[str], None], n: int, title: str, subtitle: str) -> None:
    out("")
    out(f"═══ Flow {n} — {title} ═══")
    out(f"    {subtitle}")
    out("")


def _card(out: Callable[[str], None], d: dict[str, Any]) -> None:
    """Print one branch card in the product shape (text mirror of the UI card)."""
    out(f"  {d['technique']}")
    out(f"    → {d.get('component') or ''}")
    if d.get("flavour_shift") or d.get("texture_shift"):
        out(f"    → {d.get('flavour_shift') or '—'} · {d.get('texture_shift') or '—'}")
    tags = ", ".join(t["value"] for t in d.get("tags") or [])
    if tags:
        out(f"    → tags: {tags}")
    if d.get("risks"):
        out(f"    → risks: {', '.join(d['risks'])}   ← a RISK, not a missing role")
    missing = [m["role_name"] for m in d.get("missing") or []]
    if missing:
        out(f"    → missing: {', '.join(missing)}")
    add_parts = []
    for role, fillers in (d.get("fillers_by_role") or {}).items():
        names = ", ".join(f["filler"] for f in fillers[:3]) or "(no curated filler)"
        add_parts.append(f"{role}: {names}")
    if add_parts:
        out(f"    → add: {' · '.join(add_parts)}")
    if d.get("uses"):
        out(f"    → use in: {', '.join(d['uses'])}")


def run_demo(conn: sqlite3.Connection, out: Callable[[str], None] = print) -> None:
    """Print the five demo flows to ``out`` (defaults to stdout)."""
    _ensure_utf8_stdout()
    out("Ingredient Foundry — demo")
    out("A local cooking map for turning ingredients into useful components,")
    out("seeing what taste roles are missing, and finding the next sensible move.")
    out("This does not generate recipes. It asks:")
    out("  - What can this ingredient become?")
    out("  - What does that component still need?")
    out("  - What fixes this plate?")
    out("  - What plausible weird pairing is worth tasting carefully?")

    # ---- Flow 1: tomato → roast ----
    _banner(out, 1, "Tomato → roast",
            "Ingredient Explorer: what does a tomato become, and what's missing?")
    card = query.branch_card(conn, "tomato", "roast")
    if card:
        _card(out, card)
    else:
        out("  (no tomato/roast transformation)")

    # ---- Flow 2: stateful component ----
    _banner(out, 2, "Component Explorer — roasted_tomato_component",
            "Start from an after-state. You are not always holding raw tomato.")
    d = query.component_card(conn, "roasted_tomato_component")
    if d:
        prod = ", ".join(f"{p['ingredient']} + {p['technique']}" for p in d["produced_by"])
        out(f"  {d['name']} (a reusable component)")
        out(f"    made by: {prod}")
        if d.get("uses"):
            out(f"    use it in: {', '.join(d['uses'])}")
        missing = [m["role_name"] for m in d.get("missing") or []]
        if missing:
            out(f"    if building a meal on it, still missing: {', '.join(missing)}")
        add_parts = []
        for role, fillers in (d.get("fillers_by_role") or {}).items():
            names = ", ".join(f["filler"] for f in fillers[:3]) or "(no curated filler)"
            add_parts.append(f"{role}: {names}")
        if add_parts:
            out(f"    add: {' · '.join(add_parts)}")
    else:
        out("  (no such component)")

    # ---- Flow 3: plate repair ----
    _banner(out, 3, "Plate repair — mashed potatoes + roasted chickpea patty",
            "Plate Balance (Cook mode): what does this plate have, lack, need?")
    r = query.plate_balance_detail(
        conn, "I have mashed potatoes and roasted chickpea patties. what is missing?")
    items = ", ".join(f"{it['name']} ({it['kind']})" for it in r["items"])
    out(f"  you have: {items}")
    out(f"  provided: {', '.join(r['provided']) or '(none)'}")
    if r["plate_heaviness"] is not None:
        out(f"  plate heaviness: {r['plate_heaviness']} ({r['heaviness_label']})")
    if r["target_gap"]:
        out(f"  missing for a balanced plate: {', '.join(r['target_gap'])}")
        for role in r["target_gap"]:
            fillers = r["suggested_fillers"].get(role, [])
            out(f"    - {role}: {', '.join(fillers) if fillers else '(no curated filler)'}")
    if r["flagged_more"]:
        out(f"  also flagged (may want more): {', '.join(r['flagged_more'])}")
    if r["leans_heavy"]:
        out("  leans heavy — favour acid/herb/crunch; avoid more fat/cream.")
    if r["leans_dry"]:
        out("  leans dry — favour sauce/hydration/cream.")

    # ---- Flow 4: cabbage guardrail ----
    _banner(out, 4, "Cabbage guardrail — roast / ferment / raw_slaw",
            "Sulfur/harshness is a RISK and a TAG, never a missing role.")
    for tech in ("roast", "ferment", "raw_slaw"):
        c = query.branch_card(conn, "cabbage", tech)
        if c:
            _card(out, c)
            out("")

    # ---- Flow 5: scout ----
    _banner(out, 5, "Scout — cabbage",
            "Experimental pairings only. NOT classics. Taste before serving.")
    rows = query.scout_rows(conn, ingredient="cabbage")
    if not rows:
        out("  (none curated yet)")
    for r in rows:
        subj = r["technique"] or r["target"] or "(general)"
        note = r["notes"] or f"{r['filler']} ({r['role']})"
        out(f"  - {r['filler']} + {subj}  [{r['role']}]")
        out(f"      {note}")
    out("")
    out("  Scout shows role-compatible but uncommon ideas. They are not classics.")
    out("  Taste a small amount before serving — a tiny spoon first.")
    out("")