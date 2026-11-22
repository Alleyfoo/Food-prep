"""The usability task scripts (docs/usability/task-scripts.md), automated.

Each test drives the real app the way the task's cook would and asserts the
task's success condition is on screen. They prove the answer is REACHABLE;
whether a person can FIND it still needs a person — see the findings in
docs/usability/.
"""

from pathlib import Path

from streamlit.testing.v1 import AppTest

APP = str(Path(__file__).resolve().parents[1] / "app.py")


def _app() -> AppTest:
    at = AppTest.from_file(APP, default_timeout=60)
    at.run()
    assert not at.exception, at.exception
    return at


def _radio(at, key):
    return next(r for r in at.radio if r.key == key)


def _select(at, key):
    return next(s for s in at.selectbox if s.key == key)


def _page(at) -> str:
    return "\n".join(m.value for m in at.markdown)


def test_t1_dinner_from_what_i_have():
    """Broccoli, yogurt, lemon, garlic: the app must use all of them."""
    at = _app()
    next(m for m in at.multiselect if m.key == "available_items").set_value(
        ["yogurt", "lemon", "garlic"]).run()
    assert not at.exception, at.exception
    page = _page(at)
    assert "lemon — have it" in page
    # Finding 1: garlic and yogurt reach the cook through broccoli's routes,
    # instead of being dismissed on every card.
    assert "Routes with what you have" in page
    assert "Creamy and acidic" in page and "Soy and garlic" in page
    # Finding 4: absence of a recorded pairing is not "no match".
    assert "No match here" not in page
    # ...and nothing a route uses is called unpaired on the same card.
    import re
    for card in page.split('<div class="card ')[1:]:
        if "Routes with what you have" not in card:
            continue
        unpaired = re.search(r"Not paired here yet</span><div class=\"chips\">(.*?)</div>", card)
        routes = card.split("Routes with what you have", 1)[1]
        for name in re.findall(r'chip have">([^<]+)<', routes):
            assert not unpaired or name not in unpaired.group(1), name


def test_t2_heavy_plate_says_what_not_to_add():
    at = _app()
    _radio(at, "active_tab").set_value("Plate Balance").run()
    page = _page(at)
    assert "acid" in page and "herb" in page and "crunch" in page
    # Finding 2: a "rich" plate already gets the avoid list.
    assert "Avoid adding more of" in page and "more fat / cream" in page
    # Finding 5: the number has a scale.
    assert "/ 5" in page


def test_t3_leftover_roasted_tomatoes():
    at = _app()
    _radio(at, "active_tab").set_value("Component Explorer").run()
    _select(at, "component_explorer_comp").set_value("roasted_tomato_component").run()
    page = _page(at)
    assert "Something you already cooked" in page          # finding 10
    for use in ("pasta", "toast"):
        assert use in page


def test_t4_something_new_for_roasted_cabbage():
    at = _app()
    _radio(at, "active_section").set_value("Experiment").run()
    _select(at, "tab_scout_component_select").set_value("roasted_cabbage_component").run()
    page = _page(at)
    assert "1 small piece of roasted cabbage" in page
    assert "Both sides are uncommon" not in page             # finding 6
    # Finding 7: another candidate is one click away.
    jump = next(b for b in at.button if b.key.startswith("scout_jump_"))
    target = jump.label
    jump.click().run()
    assert not at.exception, at.exception
    assert f"Roasted cabbage + {target}" in _page(at)


def test_t5_record_a_tasting_from_the_app(tmp_path, monkeypatch):
    """T5 used to need a terminal; now the form appends to tastings.yaml."""
    import shutil
    import streamlit as st
    from foodprep import loader, tasting

    real = Path(loader.TASTINGS_PATH)
    before_real = real.read_bytes()
    copy = tmp_path / "tastings.yaml"
    shutil.copy(real, copy)
    monkeypatch.setenv(tasting.TASTINGS_ENV, str(copy))
    try:
        at = _app()
        _radio(at, "active_section").set_value("Experiment").run()
        _select(at, "tab_scout_component_select").set_value(
            "roasted_cabbage_component").run()
        text = {t.key: t for t in at.text_input}
        # The protocol's starting ratio is prefilled.
        assert text["tasting_ratio"].value.startswith("1 small piece of roasted cabbage")
        text["tasting_preparation"].input("tossed one warm piece")
        text["tasting_temperature"].input("warm")
        next(a for a in at.text_area if a.key == "tasting_observations").input(
            "nutty, not greasy")
        next(c for c in at.checkbox if c.key == "tasting_safety").check()
        at.button(key="FormSubmitter:tasting_form-Review tasting").click().run()
        assert not at.exception, at.exception
        # Reviewing writes nothing (E0: review before a permanent save).
        assert copy.read_bytes() == before_real
        at.button(key="tasting_confirm").click().run()
        assert not at.exception, at.exception

        assert any("Saved to" in s.value for s in at.success)
        added = copy.read_text(encoding="utf-8")[len(before_real.decode("utf-8")):]
        assert "component: roasted_cabbage_component" in added
        assert "observations: nutty, not greasy" in added
        # The trial shows on the card straight away...
        assert "nutty, not greasy" in _page(at)
        # ...the form is cleared for the next one...
        assert {t.key: t for t in at.text_input}["tasting_preparation"].value == ""
        # ...and the real record was never touched.
        assert real.read_bytes() == before_real
    finally:
        st.cache_resource.clear()   # the trial went into the cached database


def test_t5_refused_tasting_keeps_what_was_typed(tmp_path, monkeypatch):
    import shutil
    import streamlit as st
    from foodprep import loader, tasting

    copy = tmp_path / "tastings.yaml"
    shutil.copy(loader.TASTINGS_PATH, copy)
    monkeypatch.setenv(tasting.TASTINGS_ENV, str(copy))
    try:
        at = _app()
        _radio(at, "active_section").set_value("Experiment").run()
        text = {t.key: t for t in at.text_input}
        text["tasting_preparation"].input("tossed warm")
        at.button(key="FormSubmitter:tasting_form-Review tasting").click().run()
        errors = " ".join(e.value for e in at.error)
        # Plain words, no raw field names (Dembrandt audit D9).
        assert "safely prepared" in errors and "safety_confirmed" not in errors
        assert "“What you tasted”" in errors
        assert {t.key: t for t in at.text_input}["tasting_preparation"].value == "tossed warm"
        assert copy.read_bytes() == Path(loader.TASTINGS_PATH).read_bytes()
    finally:
        st.cache_resource.clear()


def test_scores_outside_zero_to_five_are_refused():
    """Smashed potato once scored 6 on a 0-5 heaviness scale (finding 9)."""
    import pytest
    from foodprep.loader import LoadError, _score
    assert _score({"heaviness_score": 5}, "heaviness_score", "x") == 5
    assert _score({}, "heaviness_score", "x") is None
    with pytest.raises(LoadError, match="0-5"):
        _score({"heaviness_score": 6}, "heaviness_score", "smashed potato")
