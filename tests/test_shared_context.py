"""UX experiment E0 + E1: shared investigation context and its repairs.

The headline regression: before E1, choosing roasted cabbage in one view left
five other views on broccoli. Every test here uses a non-default subject
(cabbage or tomato) so a broccoli default cannot hide a missing sync.
"""

import shutil
from pathlib import Path

import pytest
import streamlit as st
from streamlit.testing.v1 import AppTest

from foodprep import loader, query, tasting

APP = str(Path(__file__).resolve().parents[1] / "app.py")


# ---- deterministic mapping (query layer) ---------------------------------

def test_every_component_maps_to_exactly_its_ingredient(conn):
    for comp in query.components_list(conn):
        ing = query.ingredient_for_component(conn, comp)
        assert ing, comp
        assert comp in query.states_for_ingredient(conn, ing) or comp == "tomato_water_component"


def test_by_product_maps_to_the_ingredient_that_yields_it(conn):
    assert query.ingredient_for_component(conn, "tomato_water_component") == "tomato"


def test_unknown_or_plate_item_has_no_ingredient(conn):
    assert query.ingredient_for_component(conn, "mashed_potatoes") is None
    assert query.ingredient_for_component(conn, "nonsense") is None


def test_profiled_states_are_a_subset(conn):
    every = query.states_for_ingredient(conn, "broccoli")
    profiled = query.states_for_ingredient(conn, "broccoli", profiled_only=True)
    assert set(profiled) < set(every)
    assert "raw_broccoli_component" in every and "raw_broccoli_component" not in profiled


# ---- the app ---------------------------------------------------------------

def _app(**params) -> AppTest:
    at = AppTest.from_file(APP, default_timeout=60)
    for key, value in params.items():
        at.query_params[key] = value
    at.run()
    assert not at.exception, at.exception
    return at


def _radio(at, key):
    return next(r for r in at.radio if r.key == key)


def _select(at, key):
    return next((s for s in at.selectbox if s.key == key), None)


def _page(at) -> str:
    return "\n".join(m.value for m in at.markdown if "<style>" not in m.value)


def _go(at, section, tab=None):
    _radio(at, "active_section").set_value(section).run()
    if tab:
        _radio(at, "active_tab").set_value(tab).run()
    assert not at.exception, at.exception


def _pick_roasted_cabbage(at):
    _go(at, "Cook", "Component Explorer")
    _select(at, "component_explorer_comp").set_value("roasted_cabbage_component").run()


def test_a_subject_chosen_once_is_the_subject_everywhere():
    at = _app()
    _pick_roasted_cabbage(at)
    _go(at, "Cook", "Taste Circle")
    assert at.session_state["tcm_component"] == "roasted_cabbage_component"
    _go(at, "Explore", "Map")
    assert _select(at, "map_ing").value == "cabbage"
    _go(at, "Explore", "Journeys")
    assert _select(at, "journey_ing").value == "cabbage"
    _go(at, "Experiment")
    assert _select(at, "tab_scout_component_select").value == "roasted_cabbage_component"
    _go(at, "Cook", "Ingredient Explorer")
    assert _select(at, "explorer_ing").value == "cabbage"


def test_changing_the_subject_anywhere_moves_it_everywhere():
    at = _app()
    _pick_roasted_cabbage(at)
    _go(at, "Experiment")
    _select(at, "tab_scout_component_select").set_value("roasted_tomato_component").run()
    _go(at, "Cook", "Component Explorer")
    assert _select(at, "component_explorer_comp").value == "roasted_tomato_component"
    _go(at, "Explore", "Map")
    assert _select(at, "map_ing").value == "tomato"


def test_no_view_falls_back_to_broccoli():
    at = _app()
    _pick_roasted_cabbage(at)
    for section, tab in [("Cook", "Taste Circle"), ("Explore", "Map"),
                         ("Explore", "Journeys"), ("Experiment", None),
                         ("Cook", "Ingredient Explorer")]:
        _go(at, section, tab)
        widgets = [s.value for s in at.selectbox] + [
            at.session_state["tcm_component"] if tab == "Taste Circle" else ""]
        assert not any("broccoli" in str(v) for v in widgets), (tab, widgets)


def test_changing_ingredient_drops_a_state_of_another_ingredient():
    at = _app()
    _pick_roasted_cabbage(at)
    _go(at, "Explore", "Map")
    _select(at, "map_ing").set_value("tomato").run()
    assert at.session_state["ctx_ingredient"] == "tomato"
    assert at.session_state["ctx_state"] is None
    assert "no prepared ingredient chosen" in _page(at)


def test_a_view_that_cannot_show_the_state_explains_instead_of_substituting():
    at = _app()
    _go(at, "Cook", "Component Explorer")
    # raw broccoli exists but has no flavour profile, so Taste Circle and
    # Scout cannot use it; they must say so and change nothing.
    _select(at, "component_explorer_comp").set_value("raw_broccoli_component").run()
    _go(at, "Cook", "Taste Circle")
    assert "has no flavour profile" in _page(at)
    assert at.session_state["ctx_state"] == "raw_broccoli_component"
    _go(at, "Experiment")
    assert _select(at, "tab_scout_component_select").value is None
    assert "has no flavour profile" in _page(at)


def test_view_specific_state_is_kept_while_the_subject_holds():
    at = _app()
    _pick_roasted_cabbage(at)
    _go(at, "Cook", "Taste Circle")
    _radio(at, "tc_view").set_value("Cards").run()
    at.button(key="tc_random").click().run()
    dish = dict(at.session_state["tcm_selections"])
    assert dish
    _go(at, "Explore", "Map")
    _go(at, "Cook", "Taste Circle")
    assert dict(at.session_state["tcm_selections"]) == dish


def test_available_ingredients_persist_and_show_on_explore():
    at = _app()
    next(m for m in at.multiselect if m.key == "available_items").set_value(
        ["lemon", "garlic"]).run()
    _go(at, "Explore", "Map")
    assert all(m.key != "available_items" for m in at.multiselect)   # box hidden
    assert "Available" in _page(at) and "lemon, garlic" in _page(at)  # strip shows it
    _go(at, "Cook", "Component Explorer")
    assert next(m for m in at.multiselect if m.key == "available_items").value == ["lemon", "garlic"]


def test_context_strip_names_subject_and_availability():
    at = _app()
    _pick_roasted_cabbage(at)
    page = _page(at)
    assert "Investigating" in page and "Roasted cabbage" in page and "from cabbage" in page


# ---- URL and reload ----------------------------------------------------------

def test_context_is_written_to_the_url():
    at = _app()
    _pick_roasted_cabbage(at)
    next(m for m in at.multiselect if m.key == "available_items").set_value(
        ["lemon", "garlic"]).run()
    qp = {k: v[0] if isinstance(v, list) else v for k, v in at.query_params.items()}
    assert qp["state"] == "roasted_cabbage_component"
    assert qp["ingredient"] == "cabbage"
    assert qp["have"] == "lemon,garlic"
    assert qp["tab"] == "component-explorer"


def test_reload_restores_subject_availability_and_tab():
    at = _app(state="roasted_cabbage_component", have="lemon,garlic",
              tab="taste-circle")
    assert _radio(at, "active_tab").value == "Taste Circle"
    assert at.session_state["tcm_component"] == "roasted_cabbage_component"
    assert at.session_state["available_items"] == ["lemon", "garlic"]


def test_ingredient_only_link_has_no_state():
    at = _app(ingredient="tomato")
    assert at.session_state["ctx_ingredient"] == "tomato"
    assert at.session_state["ctx_state"] is None


def test_unknown_ids_in_the_url_are_ignored_not_guessed():
    at = _app(state="no_such_state", ingredient="kryptonite",
              have="lemon,unicorn", tab="nowhere")
    assert at.session_state["ctx_ingredient"] == "broccoli"   # app default
    assert at.session_state["available_items"] == ["lemon"]
    assert _radio(at, "active_section").value == "Cook"


# ---- tasting review and duplicate protection (E0) ----------------------------

@pytest.fixture()
def tastings_copy(tmp_path, monkeypatch):
    copy = tmp_path / "tastings.yaml"
    shutil.copy(loader.TASTINGS_PATH, copy)
    monkeypatch.setenv(tasting.TASTINGS_ENV, str(copy))
    real = Path(loader.TASTINGS_PATH).read_bytes()
    yield copy
    st.cache_resource.clear()
    assert Path(loader.TASTINGS_PATH).read_bytes() == real   # never touched


def _fill_tasting(at, observation="nutty, not greasy"):
    text = {t.key: t for t in at.text_input}
    text["tasting_preparation"].input("tossed one warm piece")
    text["tasting_temperature"].input("warm")
    next(a for a in at.text_area if a.key == "tasting_observations").input(observation)
    next(c for c in at.checkbox if c.key == "tasting_safety").check()
    at.button(key="FormSubmitter:tasting_form-Review tasting").click().run()


def test_review_shows_the_entry_and_writes_nothing(tastings_copy):
    before = tastings_copy.read_bytes()
    at = _app(state="roasted_cabbage_component", tab="scout")
    _fill_tasting(at)
    page = _page(at)
    assert "cannot be changed afterwards" in page
    assert "nutty, not greasy" in page and "Works" in page
    assert tastings_copy.read_bytes() == before


def test_back_to_edit_keeps_the_text_and_writes_nothing(tastings_copy):
    before = tastings_copy.read_bytes()
    at = _app(state="roasted_cabbage_component", tab="scout")
    _fill_tasting(at)
    at.button(key="tasting_edit").click().run()
    assert {t.key: t for t in at.text_input}["tasting_preparation"].value == "tossed one warm piece"
    assert tastings_copy.read_bytes() == before
    # Found in the browser: the panel used to collapse here, hiding the form.
    panel = next(e for e in at.expander if e.label == "Record a tasting")
    assert panel.proto.expanded


def test_confirm_writes_exactly_once(tastings_copy):
    before = tastings_copy.read_text(encoding="utf-8")
    at = _app(state="roasted_cabbage_component", tab="scout")
    _fill_tasting(at, observation="once only")
    reviewed = dict(at.session_state["tasting_pending"])
    at.button(key="tasting_confirm").click().run()
    assert any("Saved to" in s.value for s in at.success)
    after_first = tastings_copy.read_text(encoding="utf-8")
    assert after_first.count("once only") == 1
    assert len(after_first) > len(before)
    # Replay the very entry that was just saved (a stale tab, a double click
    # delivered late): the review shows again, but confirming writes nothing.
    at.session_state["tasting_pending"] = reviewed
    at.run()
    at.button(key="tasting_confirm").click().run()
    assert tastings_copy.read_text(encoding="utf-8") == after_first


def test_navigating_away_from_review_writes_nothing(tastings_copy):
    before = tastings_copy.read_bytes()
    at = _app(state="roasted_cabbage_component", tab="scout")
    _fill_tasting(at)
    _go(at, "Cook", "Component Explorer")
    _go(at, "Experiment")
    assert tastings_copy.read_bytes() == before


# ---- E0 copy -----------------------------------------------------------------

def test_header_counts_are_gone_and_hint_matches_cards():
    page = _page(_app())
    assert "plate profiles" not in page and "62 components" not in page
    assert "not paired here yet" in page and "no match" not in page


def test_empty_states_explain_and_offer_a_next_step():
    at = _app(ingredient="butter", tab="journeys")
    page = _page(at)
    assert "gap in the catalogue" in page
    assert at.button(key="journeys_to_explorer")
    at = _app(state="ghee_component", tab="scout")
    page = _page(at)
    assert "analogy rules fits" in page and "limit of the rule set" in page
