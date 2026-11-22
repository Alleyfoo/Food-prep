"""Research probe (not part of the app or its test suite).

Test C: an unrecorded pairing (roasted broccoli + mango) and how each view
classifies it, next to a recorded one (lemon), an experimental one (miso) and
a rejected one. Run from the repo root:

    py -3.11 docs/research/ux-qlik-celonis-r1/screenshots/evidence/testC-uncertain-relationships-probe.py
"""
import re

from streamlit.testing.v1 import AppTest

at = AppTest.from_file("app.py", default_timeout=60)
at.run()


def radio(key):
    return next(r for r in at.radio if r.key == key)


def select(key):
    return next(s for s in at.selectbox if s.key == key)


def text():
    return re.sub(r"<[^>]+>", " ", "\n".join(m.value for m in at.markdown))


def roast_card():
    for card in "\n".join(m.value for m in at.markdown).split('<div class="card ')[1:]:
        if 'card-tech">roast<' in card:
            return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", card))
    return ""


next(m for m in at.multiselect if m.key == "available_items").set_value(
    ["mango", "lemon", "miso"]).run()

print("== Ingredient Explorer, broccoli, Roast card, with mango/lemon/miso on hand")
card = roast_card()
for label in ("Available now", "Missing but useful", "Not paired here yet",
              "Routes with what you have"):
    i = card.find(label)
    print(f"  {label:26s}:", card[i:i + 110] if i >= 0 else "(absent)")

radio("active_tab").set_value("Plate Balance").run()
print("\n== Plate Balance: does it show destination-unsuitable roles?")
print("  'unsuitable' on screen   :", "unsuitable" in text().lower())

radio("active_section").set_value("Explore").run()
radio("active_tab").set_value("Filler Profiles").run()
select("filler_profile_name").set_value("mango").run()
t = text()
print("\n== Filler Profiles, mango")
print("  mentions broccoli        :", "broccoli" in t.lower())
i = t.find("Avoid when")
print("  Avoid when               :", re.sub(r"\s+", " ", t[i:i + 80]))

radio("active_section").set_value("Experiment").run()
t = text()
print("\n== Scout, roasted broccoli")
print("  mango anywhere on screen :", "mango" in t.lower())
others = [b.label for b in at.button if b.key.startswith("scout_jump_")]
print("  candidates               :", others)
exp = [e for e in at.expander if "rejected" in e.label]
print("  rejected expander        :", exp[0].label if exp else "(none)")
reasons = re.findall(r"Rule does not apply here: [^<]+", "\n".join(m.value for m in at.markdown))
print("  sample rejection reasons :")
for r in reasons[:3]:
    print("    -", r)
print("\nExceptions:", list(at.exception))
