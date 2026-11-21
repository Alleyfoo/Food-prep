"""Drive the real app: every section and tab renders, and navigation holds.

Runs app.py headlessly through Streamlit's AppTest. Slow-ish (a few seconds
per tab) but it is the only test that would notice a tab throwing.
"""

from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

from foodprep.ui.streamlit_app import SECTIONS, TABS

APP = str(Path(__file__).resolve().parents[1] / "app.py")


def _app() -> AppTest:
    at = AppTest.from_file(APP, default_timeout=60)
    at.run()
    assert not at.exception, at.exception
    return at


def _radio(at: AppTest, key: str):
    return next(r for r in at.radio if r.key == key)


def test_every_tab_is_in_exactly_one_section():
    placed = [tab for tabs in SECTIONS.values() for tab in tabs]
    assert sorted(placed) == sorted(TABS)
    assert len(placed) == len(set(placed))


def test_opens_on_cook_with_broccoli():
    at = _app()
    assert _radio(at, "active_section").value == "Cook"
    assert _radio(at, "active_tab").value == "Ingredient Explorer"
    assert next(s for s in at.selectbox if s.key == "explorer_ing").value == "broccoli"


@pytest.mark.parametrize("section", list(SECTIONS))
def test_every_tab_renders_without_error(section):
    at = _app()
    _radio(at, "active_section").set_value(section).run()
    assert not at.exception, at.exception
    for tab in SECTIONS[section][1:]:
        _radio(at, "active_tab").set_value(tab).run()
        assert not at.exception, (tab, at.exception)


def test_switching_section_lands_on_its_first_tab():
    at = _app()
    _radio(at, "active_tab").set_value("Plate Balance").run()
    _radio(at, "active_section").set_value("Explore").run()
    assert _radio(at, "active_tab").value == "Map"


def test_single_tab_section_has_no_tab_rail():
    at = _app()
    _radio(at, "active_section").set_value("Experiment").run()
    assert not at.exception, at.exception
    assert all(r.key != "active_tab" for r in at.radio)


def test_map_views_share_one_ingredient_picker():
    at = _app()
    _radio(at, "active_section").set_value("Explore").run()
    next(s for s in at.selectbox if s.key == "map_ing").set_value("kale").run()
    _radio(at, "map_view").set_value("Scout ideas").run()
    assert not at.exception, at.exception
    assert next(s for s in at.selectbox if s.key == "map_ing").value == "kale"


def test_taste_circle_views_build_one_dish():
    at = _app()
    _radio(at, "active_tab").set_value("Taste Circle").run()
    _radio(at, "tc_view").set_value("Cards").run()
    assert not at.exception, at.exception
    at.button(key="tc_random").click().run()
    picked = dict(at.session_state["tcm_selections"])
    assert picked, "Surprise me should fill at least one dimension"
    _radio(at, "tc_view").set_value("Circle").run()
    assert not at.exception, at.exception
    assert dict(at.session_state["tcm_selections"]) == picked


def test_selectors_show_readable_names():
    at = _app()
    _radio(at, "active_section").set_value("Experiment").run()
    state = next(s for s in at.selectbox if s.key == "tab_scout_component_select")
    assert state.value == "roasted_broccoli_component"
    assert "roasted broccoli" in state.options
    assert not any("_component" in option for option in state.options)


def test_availability_strip_hides_on_reference_tabs_and_keeps_its_picks():
    at = _app()
    next(m for m in at.multiselect if m.key == "available_items").set_value(["lemon"]).run()
    _radio(at, "active_section").set_value("Explore").run()
    assert all(m.key != "available_items" for m in at.multiselect)
    _radio(at, "active_section").set_value("Cook").run()
    assert next(m for m in at.multiselect if m.key == "available_items").value == ["lemon"]


def test_record_tasting_hint_is_a_complete_command():
    at = _app()
    _radio(at, "active_section").set_value("Experiment").run()
    at.button(key="scout_record").click().run()
    assert not at.exception, at.exception
    command = at.code[0].value
    for flag in ("--verdict", "--preparation", "--ratio", "--temperature",
                 "--observations", "--safety-confirmed"):
        assert flag in command, flag
