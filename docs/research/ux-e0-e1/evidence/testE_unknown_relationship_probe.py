"""Test E: an unrecorded pairing (roasted cabbage + mango) across views.

Records what each view says about mango while roasted cabbage is the subject
and mango is on hand, so the wording can be compared screen by screen.

    py -3.11 docs/research/ux-e0-e1/evidence/testE_unknown_relationship_probe.py
"""
import re

from streamlit.testing.v1 import AppTest

at = AppTest.from_file("app.py", default_timeout=60)
at.query_params["state"] = "roasted_cabbage_component"
at.query_params["have"] = "mango,lemon"
at.run()


def text(include_chrome=False):
    """Page text without the stylesheet and, by default, without the context
    strip and availability hint, which name the on-hand items themselves."""
    skip = ("<style>",) if include_chrome else ("<style>", "ctx-strip", "avail-head")
    html = "\n".join(m.value for m in at.markdown
                     if not any(s in m.value for s in skip))
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html))


def around(t, word, n=90):
    hits = [m.start() for m in re.finditer(word, t, re.I)]
    return [t[max(0, h - n): h + n].strip() for h in hits[:2]] or ["(not mentioned)"]


def radio(key):
    return next(r for r in at.radio if r.key == key)


def card_for(technique):
    for card in "\n".join(m.value for m in at.markdown).split('<div class="card ')[1:]:
        if f'card-tech">{technique}<' in card:
            return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", card))
    return ""


print("Context strip:", around(text(include_chrome=True), "Investigating", 60)[0])

print("\n== Ingredient Explorer (cabbage), Roast card")
roast = card_for("roast")
for label in ("Available now", "Not paired here yet", "Routes with what you have"):
    i = roast.find(label)
    print(f"  {label:26s}:", roast[i:i + 70] if i >= 0 else "(absent)")

radio("active_tab").set_value("Component Explorer").run()
print("\n== Component Explorer (roasted cabbage)")
print("  mango:", around(text(), "mango")[0])

radio("active_section").set_value("Experiment").run()
print("\n== Scout (roasted cabbage)")
print("  mango mentioned:", "mango" in text().lower())

radio("active_section").set_value("Explore").run()
radio("active_tab").set_value("Filler Profiles").run()
next(s for s in at.selectbox if s.key == "filler_profile_name").set_value("mango").run()
print("\n== Filler Profiles (mango)")
print("  ", around(text(), "No pairings")[0])
print("  cabbage mentioned:", "cabbage" in text().lower())

words = ["incompatible", "doesn't go", "does not go", "bad pairing", "avoid mango"]
print("\nNegative claims anywhere:", [w for w in words if w in text().lower()] or "none")
print("Exceptions:", list(at.exception))
