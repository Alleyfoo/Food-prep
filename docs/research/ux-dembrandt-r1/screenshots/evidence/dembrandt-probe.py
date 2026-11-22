"""Research probe for the Dembrandt audit (not part of the app or its tests).

Drives app.py through Streamlit's AppTest and records facts the Dembrandt
skills ask about: nested pill levels per screen (tab-navigation), coined
terms on screen (information-architecture), error-message wording and empty
states (nielsen 2, 9, 10). Run from the repo root:

    py -3.11 docs/research/ux-dembrandt-r1/screenshots/evidence/dembrandt-probe.py
"""
import re

from streamlit.testing.v1 import AppTest

SCREENS = [
    ("Cook", "Ingredient Explorer"), ("Cook", "Component Explorer"),
    ("Cook", "Plate Balance"), ("Cook", "Taste Circle"),
    ("Explore", "Map"), ("Explore", "Journeys"), ("Explore", "Filler Profiles"),
    ("Experiment", "Scout"),
]
#: Words the app coins or uses in a domain-specific sense. A cook would not
#: bring these to the app (information-architecture: ~10 invented terms max).
TERMS = ["component", "after-state", "state", "filler", "route", "destination",
         "journey", "role", "hypothes", "scout", "cook mode", "branch",
         "plate profile", "hard gap", "target role", "attested", "novelty",
         "compatibility", "corpus", "analogy", "mechanism", "dimension",
         "medium", "taste circle", "preparation"]

at = AppTest.from_file("app.py", default_timeout=60)
at.run()


def radio(key):
    return next(r for r in at.radio if r.key == key)


def page_text():
    # The app injects design.css as a markdown element; its class names are
    # not visible text, so skip it.
    html = "\n".join(m.value for m in at.markdown
                     if "<style>" not in m.value)
    text = re.sub(r"<[^>]+>", " ", html)
    labels = [w.label for w in list(at.radio) + list(at.selectbox) + list(at.button)]
    options = [str(o) for r in at.radio for o in r.options]
    return (text + " " + " ".join(labels + options)).lower()


seen = {t: [] for t in TERMS}
print("== Pill levels stacked per screen (section > tab > view/mode)")
for section, tab in SCREENS:
    radio("active_section").set_value(section).run()
    if tab != "Scout":
        radio("active_tab").set_value(tab).run()
    keys = [r.key for r in at.radio]
    print(f"  {section:10s} > {tab:20s}: {len(keys)} levels {keys}")
    text = page_text()
    for t in TERMS:
        if re.search(rf"\b{re.escape(t)}", text):
            seen[t].append(tab)

print("\n== Coined or domain terms visible, and on how many of 8 screens")
used = {t: s for t, s in seen.items() if s}
for t, s in sorted(used.items(), key=lambda kv: -len(kv[1])):
    print(f"  {t:15s} {len(s)}  {', '.join(s)}")
print(f"  total distinct: {len(used)}")

print("\n== Error message when a tasting is saved without the safety tick")
radio("active_section").set_value("Experiment").run()
next(t for t in at.text_input if t.key == "tasting_preparation").input("x")
at.button(key="FormSubmitter:tasting_form-Save tasting").click().run()
print("  ", [e.value for e in at.error])

print("\n== Empty states")
radio("active_section").set_value("Cook").run()
radio("active_tab").set_value("Plate Balance").run()
next(m for m in at.multiselect if m.key == "plate_items").set_value([]).run()
print("  Plate Balance, no items :", re.sub(r"<[^>]+>", "", at.markdown[-1].value)[:120])
radio("active_section").set_value("Explore").run()
radio("active_tab").set_value("Journeys").run()
next(s for s in at.selectbox if s.key == "journey_ing").set_value("butter").run()
print("  Journeys, butter        :", re.sub(r"<[^>]+>", " ", " ".join(m.value for m in at.markdown[-2:]))[:140])
radio("active_section").set_value("Experiment").run()
next(s for s in at.selectbox if s.key == "tab_scout_component_select").set_value("ghee_component").run()
print("  Scout, ghee             :", re.sub(r"<[^>]+>", " ", " ".join(m.value for m in at.markdown[-2:]))[:160])
print("\nExceptions:", list(at.exception))
