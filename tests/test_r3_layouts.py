"""R3 research prototype: the three layouts show the same facts, and status
labels are read from the data, not invented. Desktop prototype only."""
from __future__ import annotations

import re
import sqlite3
import sys
from html import unescape
from pathlib import Path

import pytest

PROTO = Path(__file__).resolve().parents[1] / "docs/research/ux-data-layouts-r3/prototype"
sys.path.insert(0, str(PROTO))

from foodprep import loader  # noqa: E402
import layouts as L  # noqa: E402
from model import build_model, pretty, state_gaps  # noqa: E402


@pytest.fixture(scope="module")
def conn():
    c = sqlite3.connect(":memory:")
    c.row_factory = sqlite3.Row
    loader.build(c)
    return c


def _text(html: str) -> str:
    return unescape(re.sub(r"<[^>]+>", " ", html))


@pytest.mark.parametrize("ing,have", [("broccoli", ["yogurt", "lemon", "garlic"]),
                                      ("cabbage", ["lemon"]), ("potato", []),
                                      ("tomato", [])])
def test_every_layout_shows_every_recorded_pairing(conn, ing, have):
    m = build_model(conn, ing, have)
    table = _text(L.associative_html(m, {}))
    for s in m["states"]:
        sheet = _text(L.fact_sheet_html(m, s["component"]))
        dot = L.explorer_dot(m, s["component"], 3)
        for role, r in s["roles"].items():
            for p in r["fillers"]:
                name = pretty(p["filler"])
                assert name in table, (s["component"], name)
                assert name in sheet, (s["component"], name)
                assert f'label="{name}"' in dot, (s["component"], name)


def test_filters_grey_out_rather_than_remove(conn):
    m = build_model(conn, "broccoli", [])
    full = L.associative_html(m, {})
    filt = L.associative_html(m, {"has": ["flavour route"]})
    assert full.count("<tr") == filt.count("<tr")
    assert 'class="excluded"' in filt and "excluded: no flavour route" in filt


def test_brown_butter_is_shown_as_idea_and_tested_never_as_curated(conn):
    m = build_model(conn, "broccoli", [])
    rels = [r for r in m["relations"] if r["target"] == "brown_butter"
            and (r.get("state") == "roasted_broccoli_component"
                 or r["source"] == "roasted_broccoli_component")]
    assert {r["status"] for r in rels} == {"hypothesis", "tested"}
    sheet = L.fact_sheet_html(m, "roasted_broccoli_component")
    assert "st-test" in sheet and "works (2026-08-12)" in sheet


def test_sparse_record_states_its_gaps(conn):
    m = build_model(conn, "potato", [])
    s = next(x for x in m["states"] if x["component"] == "smashed_roasted_potato_component")
    assert "no flavour route" in state_gaps(s)
    assert all(r["status"] == "not_recorded" for r in s["roles"].values())
    sheet = _text(L.fact_sheet_html(m, s["component"]))
    assert "needed · nothing recorded" in sheet and "no flavour route written" in sheet


def test_on_hand_comes_only_from_what_the_user_typed(conn):
    none = build_model(conn, "broccoli", [])
    assert not any(r["status"] == "on_hand" for r in none["relations"])
    some = build_model(conn, "broccoli", ["lemon"])
    assert {r["target"] for r in some["relations"] if r["status"] == "on_hand"} == {"lemon"}


def test_filler_focus_lists_every_preparation_it_is_paired_with(conn):
    m = build_model(conn, "broccoli", ["lemon"])
    dot = L.explorer_dot(m, "lemon", 2)
    paired = {r["state"] for r in m["relations"]
              if r["kind"] == "filled by" and r["target"] == "lemon"}
    assert paired
    for comp in paired:
        assert f'"{comp}"' in dot
