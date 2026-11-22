"""Research probe (not part of the app or its test suite).

Test A control: does choosing a subject in one view carry into the others?
Picks roasted tomato in Component Explorer and tomato in Ingredient Explorer,
then reads which subject every other view shows. Run from the repo root:

    py -3.11 docs/research/ux-qlik-celonis-r1/screenshots/evidence/testA-subject-continuity-probe.py
"""
from streamlit.testing.v1 import AppTest

at = AppTest.from_file("app.py", default_timeout=60)
at.run()


def radio(key):
    return next(r for r in at.radio if r.key == key)


def select(key):
    return next(s for s in at.selectbox if s.key == key)


radio("active_tab").set_value("Component Explorer").run()
select("component_explorer_comp").set_value("roasted_tomato_component").run()
radio("active_tab").set_value("Ingredient Explorer").run()
select("explorer_ing").set_value("tomato").run()
print("Chosen: Component Explorer = roasted_tomato_component, "
      "Ingredient Explorer = tomato\n")

radio("active_tab").set_value("Taste Circle").run()
print("Taste Circle shows      :", at.session_state["tcm_component"])

radio("active_section").set_value("Explore").run()
print("Map shows               :", select("map_ing").value)
radio("active_tab").set_value("Journeys").run()
print("Journeys shows          :", select("journey_ing").value)

radio("active_section").set_value("Experiment").run()
print("Scout shows             :", select("tab_scout_component_select").value)

radio("active_section").set_value("Cook").run()
print("Back in Cook, tab       :", radio("active_tab").value)
radio("active_tab").set_value("Component Explorer").run()
print("Component Explorer kept :", select("component_explorer_comp").value)
print("Exceptions              :", list(at.exception))
