"""UX experiment E3: the answer-first Ingredient Explorer (variant B).

The summary must be derived from the same data as the detailed cards, follow
the investigated prepared ingredient, and say so honestly when little is
known. Tests use the real catalogue and never touch tastings.yaml.
"""
from __future__ import annotations

import re
import sqlite3

import pytest

from foodprep import loader, query
from foodprep.ui.answer import answer_html, card_anchor, explorer_answer

HAVE = ["yogurt", "lemon", "garlic"]


@pytest.fixture(scope="module")
def conn():
    c = sqlite3.connect(":memory:")
    c.row_factory = sqlite3.Row
    loader.build(c)
    return c


def _answer(conn, ingredient, state, have):
    cards = query.all_branch_cards(conn, ingredient)
    chosen = next((c for c in cards if c["component"] == state), None)
    data = {}
    for c in cards:
        part = (query.available_filter(conn, c["transformation_id"], have)
                if have else None)
        routes = query.flavour_routes_for_component(
            conn, c["component"], available_items=have or None)
        data[c["component"]] = (part, routes)
    part, routes = data[state] if chosen else (None, None)
    others = [(c, data[c["component"]][1]) for c in cards if c is not chosen]
    return explorer_answer(ingredient, chosen, routes, part, have, others), data


# ---- answer follows the investigated subject --------------------------------

def test_broccoli_scenario_answers_about_roasted_broccoli(conn):
    a, data = _answer(conn, "broccoli", "roasted_broccoli_component", HAVE)
    assert a["state"] == "roasted_broccoli_component"
    assert a["kind"] == "route"
    assert a["route_id"] == "creamy_and_acidic"
    assert a["have"] == ["yogurt", "lemon"]
    assert a["need"] == []                     # both required elements on hand
    assert a["optional"] == ["dill"]           # finish, not required
    assert "raw" not in a["headline"].lower()


def test_answer_never_names_another_preparation_as_the_subject(conn):
    for state in ("raw_broccoli_component", "steamed_broccoli_component",
                  "stir_fried_broccoli_component"):
        a, _ = _answer(conn, "broccoli", state, HAVE)
        assert a["state"] == state
        assert state.replace("_component", "").replace("_", " ") in a["headline"].lower()


def test_subject_change_to_cabbage_leaves_no_broccoli(conn):
    a, _ = _answer(conn, "cabbage", "roasted_cabbage_component", HAVE)
    html = answer_html(a).lower()
    assert "broccoli" not in html
    assert a["state"] == "roasted_cabbage_component"


# ---- summary and card agree --------------------------------------------------

def test_route_answer_matches_the_cards_route_row(conn):
    a, data = _answer(conn, "broccoli", "roasted_broccoli_component", HAVE)
    _, routes = data["roasted_broccoli_component"]
    card_route_names = [r["name"] for r in routes if r["available_elements"]]
    route = next(r for r in routes if r["route_id"] == a["route_id"])
    assert route["name"] == card_route_names[0]          # first on the card too
    assert set(a["have"]) == {e["ingredient"] for e in route["available_elements"]}


def test_pairing_answer_matches_available_now(conn):
    a, data = _answer(conn, "cabbage", "roasted_cabbage_component", HAVE)
    part, routes = data["roasted_cabbage_component"]
    assert not any(r["available_elements"] for r in routes)
    assert a["kind"] == "pairings"
    assert a["have"] == [g["filler"] for g in part["available_now"]]


def test_card_anchor_links_resolve_to_rendered_cards(conn):
    from foodprep.ui.render import branch_card_html
    a, _ = _answer(conn, "broccoli", "roasted_broccoli_component", HAVE)
    html = answer_html(a)
    targets = re.findall(r'href="#([^"]+)"', html)
    assert card_anchor("roasted_broccoli_component") in targets
    cards = {c["component"]: c for c in query.all_branch_cards(conn, "broccoli")}
    for t in targets:
        comp = next(k for k in cards if card_anchor(k) == t)
        assert f'id="{t}"' in branch_card_html(cards[comp], anchor=t)


# ---- available-ingredient filtering -----------------------------------------

def test_other_preparations_use_what_you_have(conn):
    a, data = _answer(conn, "broccoli", "roasted_broccoli_component", HAVE)
    others = dict(a["others"])
    assert "stir_fried_broccoli_component" in others      # soy and garlic: garlic
    assert "roasted_broccoli_component" not in others
    for comp in others:
        _, routes = data[comp]
        assert any(r["available_elements"] for r in routes)


def test_nothing_matching_is_said_honestly(conn):
    a, _ = _answer(conn, "broccoli", "roasted_broccoli_component", ["tortilla"])
    assert a["kind"] == "no_match"
    assert "not that it clashes" in answer_html(a)


def test_no_items_on_hand_asks_for_them(conn):
    a, _ = _answer(conn, "broccoli", "roasted_broccoli_component", [])
    assert a["kind"] == "recorded_route"
    assert "Enter what you have" in answer_html(a)
    assert a["others"] == []


# ---- missing data -----------------------------------------------------------

def test_limited_knowledge_makes_no_recommendation(conn):
    a, _ = _answer(conn, "potato", "smashed_roasted_potato_component", [])
    assert a["kind"] == "limited"
    html = answer_html(a)
    assert "Nothing here is a recommendation" in html
    assert "Try " not in a["headline"]


def test_state_without_routes_lists_single_pairings(conn):
    a, _ = _answer(conn, "tomato", "roasted_tomato_component", [])
    assert a["kind"] == "needs"
    assert "No flavour route is written" in answer_html(a)


def test_no_state_chosen_does_not_pick_one(conn):
    a, _ = _answer(conn, "broccoli", None, HAVE)
    assert a["kind"] == "no_state"
    assert a["state"] is None
    assert "href" not in answer_html(a)


def test_risks_are_always_shown(conn):
    a, _ = _answer(conn, "broccoli", "roasted_broccoli_component", HAVE)
    assert "sulfurous if overcooked" in a["watch"]
    assert "Watch for" in answer_html(a)
    assert "_" not in " ".join(a["watch"][:1])       # readable, not an id


def test_answer_is_escaped(conn):
    a = {"headline": "<b>x</b>", "lines": [("Why", "<script>")], "watch": [],
         "state": None, "others": []}
    html = answer_html(a)
    assert "<script>" not in html and "&lt;b&gt;" in html


# ---- the app (AppTest) ------------------------------------------------------

from pathlib import Path  # noqa: E402

from streamlit.testing.v1 import AppTest  # noqa: E402

APP = str(Path(__file__).resolve().parents[1] / "app.py")


def _app(**params) -> AppTest:
    at = AppTest.from_file(APP, default_timeout=60)
    for key, value in params.items():
        at.query_params[key] = value
    at.run()
    assert not at.exception, at.exception
    return at


def _md(at) -> str:
    return "\n".join(m.value for m in at.markdown if "<style>" not in m.value)


def _answer_block(at) -> str:
    return next(m.value for m in at.markdown
                if 'class="answer-first"' in m.value)


def test_app_answer_and_lead_card_name_the_same_preparation():
    at = _app(state="roasted_broccoli_component", have="yogurt,lemon,garlic")
    answer = _answer_block(at)
    assert "Try roasted broccoli: creamy and acidic" in answer
    lead = next(m.value for m in at.markdown if 'class="card lead' in m.value)
    assert "roasted broccoli" in lead and "raw broccoli" not in lead


def test_app_answer_follows_a_subject_picked_in_the_explorer():
    at = _app(state="roasted_broccoli_component", have="yogurt,lemon,garlic")
    picker = next(s for s in at.selectbox if s.key == "explorer_state")
    picker.set_value("steamed_broccoli_component").run()
    assert "Try steamed broccoli" in _answer_block(at)
    assert at.session_state.ctx_state == "steamed_broccoli_component"


def test_app_subject_change_elsewhere_updates_the_answer():
    at = _app(state="roasted_broccoli_component", have="yogurt,lemon,garlic")
    next(r for r in at.radio if r.key == "active_tab").set_value("Component Explorer").run()
    next(s for s in at.selectbox if s.key == "component_explorer_comp") \
        .set_value("roasted_cabbage_component").run()
    next(r for r in at.radio if r.key == "active_tab").set_value("Ingredient Explorer").run()
    answer = _answer_block(at)
    assert "roasted cabbage" in answer and "broccoli" not in answer.lower()


def test_app_state_beyond_the_top_five_is_still_shown():
    # smashed roasted potato ranked below the first five: variant A only
    # pointed at it; B shows its card first.
    at = _app(state="smashed_roasted_potato_component")
    page = _md(at)
    assert 'id="card-smashed-roasted-potato-component"' in page
    assert "Little is recorded for smashed roasted potato" in page


def test_app_ingredient_without_state_asks_for_one():
    at = _app(ingredient="cabbage")
    assert "Choose how the cabbage is prepared" in _answer_block(at)
    assert 'class="card lead' not in _md(at)


def test_variant_a_is_unchanged(monkeypatch):
    at = AppTest.from_file(APP, default_timeout=60)
    at.query_params["have"] = "yogurt,lemon,garlic"
    monkeypatch.setenv("FOODPREP_EXPLORER_VARIANT", "A")
    at.run()
    assert not at.exception, at.exception
    assert not any('class="answer-first"' in m.value for m in at.markdown)
    lead = next(m.value for m in at.markdown if 'class="card lead' in m.value)
    assert "raw broccoli" in lead          # the old emphasis, for comparison
