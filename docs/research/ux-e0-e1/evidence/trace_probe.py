"""Interaction trace for Tests A and B, runnable on any version of the app.

Drives app.py through Streamlit's AppTest. It never writes tastings. It uses
only widget keys that exist both before and after the experiment, so the same
script produces the "before" and "after" traces.

    py -3.11 docs/research/ux-e0-e1/evidence/trace_probe.py

Counts are of programmatic interactions: a lower bound on what a person does,
not a usability measurement.
"""
from __future__ import annotations

from streamlit.testing.v1 import AppTest

APP = "app.py"
#: (section, tab, picker key, kind). kind says what the picker holds.
VIEWS = [
    ("Cook", "Component Explorer", "component_explorer_comp", "state"),
    ("Cook", "Taste Circle", None, "state"),          # tcm_component, no selectbox in Circle view
    ("Explore", "Map", "map_ing", "ingredient"),
    ("Explore", "Journeys", "journey_ing", "ingredient"),
    ("Experiment", "Scout", "tab_scout_component_select", "state"),
    ("Cook", "Ingredient Explorer", "explorer_ing", "ingredient"),
]
STATE_ING = {"roasted_cabbage_component": "cabbage",
             "roasted_tomato_component": "tomato"}

actions = 0


def act(widget_call):
    """Count one user-equivalent interaction."""
    global actions
    actions += 1
    widget_call.run()


def radio(at, key):
    return next(r for r in at.radio if r.key == key)


def select(at, key):
    return next((s for s in at.selectbox if s.key == key), None)


def go(at, section, tab):
    if radio(at, "active_section").value != section:
        act(radio(at, "active_section").set_value(section))
    if tab != "Scout" and radio(at, "active_tab").value != tab:
        act(radio(at, "active_tab").set_value(tab))


def shown_subject(at, key):
    if key is None:
        return at.session_state["tcm_component"] if "tcm_component" in at.session_state else None
    widget = select(at, key)
    return widget.value if widget else None


def visit_all(at, target_state, label):
    """Visit every view; re-pick wherever it does not show the target."""
    repicks = 0
    print(f"\n-- {label}: visiting every view, target {target_state}")
    for section, tab, key, kind in VIEWS:
        go(at, section, tab)
        want = target_state if kind == "state" else STATE_ING[target_state]
        got = shown_subject(at, key)
        status = "ok" if got == want else "WRONG"
        line = f"  {section:10s} > {tab:20s} shows {got!s:30s} {status}"
        if got != want and key is not None:
            act(select(at, key).set_value(want))
            repicks += 1
            line += "  -> re-picked"
        elif got != want:
            # Taste Circle Circle view: switch to Cards and pick there.
            act(radio(at, "tc_view").set_value("Cards"))
            act(select(at, "taste_circle_component").set_value(want))
            act(radio(at, "tc_view").set_value("Circle"))
            repicks += 1
            line += "  -> re-picked via Cards"
        print(line)
    return repicks


def available(at):
    m = next((m for m in at.multiselect if m.key == "available_items"), None)
    return m.value if m else "(strip not shown)"


at = AppTest.from_file(APP, default_timeout=60)
at.run()
print("Version under test: subject on first load")
for section, tab, key, kind in VIEWS:
    go(at, section, tab)
    print(f"  {tab:20s}: {shown_subject(at, key)}")
actions = 0

# ---- Test A: roasted cabbage --------------------------------------------
print("\n==== Test A: roasted cabbage, lemon + garlic")
go(at, "Cook", "Component Explorer")
act(select(at, "component_explorer_comp").set_value("roasted_cabbage_component"))
act(next(m for m in at.multiselect if m.key == "available_items").set_value(["lemon", "garlic"]))
start_actions = actions
repicks_a = visit_all(at, "roasted_cabbage_component", "Test A")
go(at, "Cook", "Component Explorer")
print(f"  back at start: Component Explorer shows "
      f"{shown_subject(at, 'component_explorer_comp')}; available = {available(at)}")
print(f"  Test A: {repicks_a} re-picks, {actions - start_actions} interactions after the first selection")

# ---- Reload ---------------------------------------------------------------
print("\n==== Reload (new session; URL query parameters carried over if any)")
params = dict(at.query_params) if hasattr(at, "query_params") else {}
print("  URL query parameters:", params or "(none)")
fresh = AppTest.from_file(APP, default_timeout=60)
for k, v in params.items():
    fresh.query_params[k] = v
fresh.run()
go(fresh, "Cook", "Component Explorer")
print(f"  after reload: section={radio(fresh, 'active_section').value}, "
      f"Component Explorer shows {shown_subject(fresh, 'component_explorer_comp')}, "
      f"available = {available(fresh)}")

# ---- Test B: change subject -----------------------------------------------
print("\n==== Test B: switch to roasted tomato")
actions = 0
go(at, "Cook", "Component Explorer")
act(select(at, "component_explorer_comp").set_value("roasted_tomato_component"))
repicks_b = visit_all(at, "roasted_tomato_component", "Test B")
print(f"  Test B: {repicks_b} re-picks, {actions} interactions in total")
print("\nExceptions:", list(at.exception) + list(fresh.exception))
