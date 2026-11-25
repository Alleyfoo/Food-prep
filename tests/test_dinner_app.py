"""R7: the Dinner section in the running app (Streamlit AppTest)."""

from __future__ import annotations

from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

from foodprep import kitchen_records as kr

APP = str(Path(__file__).resolve().parents[1] / "app.py")


@pytest.fixture(autouse=True)
def _private_records(tmp_path, monkeypatch):
    monkeypatch.setenv(kr.CONTROL_ENV, str(tmp_path / "control.yaml"))
    monkeypatch.setenv(kr.SHELF_ENV, str(tmp_path / "shelf.yaml"))


def _app() -> AppTest:
    at = AppTest.from_file(APP, default_timeout=60)
    at.run()
    assert not at.exception, at.exception
    return at


def _radio(at, key):
    return next(r for r in at.radio if r.key == key)


def _text(at) -> str:
    return "\n".join(m.value for m in at.markdown)


def test_outcome_list_opens_a_dish():
    at = _app()
    _radio(at, "active_section").set_value("Dinner").run()
    next(s for s in at.selectbox if s.key == "dinner_ing").set_value("dried_peas").run()
    assert not at.exception, at.exception
    assert "Falafel from Finnish dried peas" in _text(at)
    at.button(key="dn_open_less_usual_0").click().run()
    assert not at.exception, at.exception
    assert _radio(at, "active_tab").value == "Dish"
    assert at.session_state["dinner_dish"] == "transfer:pea_falafel"


def test_dish_defaults_to_the_gratin_and_shows_aligned_routes():
    at = _app()
    _radio(at, "active_section").set_value("Dinner").run()
    _radio(at, "active_tab").set_value("Dish").run()
    assert at.session_state["dinner_dish"] == "transfer:rutabaga_gratin"
    _radio(at, "dish_view").set_value("Routes side by side").run()
    assert not at.exception, at.exception
    assert "documented to fail" in _text(at)


def test_map_outcomes_is_the_default_view_and_a_table_for_potato():
    at = _app()
    _radio(at, "active_section").set_value("Explore").run()
    next(s for s in at.selectbox if s.key == "map_ing").set_value("potato").run()
    assert not at.exception, at.exception
    assert _radio(at, "map_view").value == "Outcomes"
    assert "dn-outcome-table" in _text(at)


def test_taste_circle_says_documented_pairings_not_predicted_taste():
    at = _app()
    _radio(at, "active_tab").set_value("Taste Circle").run()
    assert not at.exception, at.exception
    assert "Documented pairings, not predicted taste" in _text(at)


def test_an_ingredient_only_dinner_knows_does_not_break_the_other_views():
    """Dried peas are in the R3-R5 records but not in the older catalogue the Cook
    and Explore views draw from: picking them in Dinner keeps the pick there and
    leaves the shared context alone, so every other tab still renders."""
    from foodprep.ui.streamlit_app import SECTIONS
    at = _app()
    _radio(at, "active_section").set_value("Dinner").run()
    next(s for s in at.selectbox if s.key == "dinner_ing").set_value("dried_peas").run()
    assert at.session_state["ctx_ingredient"] == "broccoli"
    for section, tabs in SECTIONS.items():
        _radio(at, "active_section").set_value(section).run()
        assert not at.exception, (section, at.exception)
        for tab in tabs[1:]:
            _radio(at, "active_tab").set_value(tab).run()
            assert not at.exception, (tab, at.exception)
    _radio(at, "active_section").set_value("Dinner").run()
    _radio(at, "active_tab").set_value("What can I make").run()
    assert next(s for s in at.selectbox if s.key == "dinner_ing").value == "dried_peas"
