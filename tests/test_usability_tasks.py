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


def test_t5_record_command_survives_powershell():
    at = _app()
    _radio(at, "active_section").set_value("Experiment").run()
    at.button(key="scout_record").click().run()
    command = at.code[0].value
    # Finding 3: one line, no bash-only "\" continuations.
    assert "\n" not in command and "\\" not in command
    assert command.startswith("foodprep record-tasting roasted_broccoli_component ")
    assert at.button(key="scout_record").label == "How to record a tasting"


def test_scores_outside_zero_to_five_are_refused():
    """Smashed potato once scored 6 on a 0-5 heaviness scale (finding 9)."""
    import pytest
    from foodprep.loader import LoadError, _score
    assert _score({"heaviness_score": 5}, "heaviness_score", "x") == 5
    assert _score({}, "heaviness_score", "x") is None
    with pytest.raises(LoadError, match="0-5"):
        _score({"heaviness_score": 6}, "heaviness_score", "smashed potato")
