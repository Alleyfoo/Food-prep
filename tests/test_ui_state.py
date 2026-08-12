"""Only the active tab renders, so selector state needs explicit care.

Since the tab rail replaced ``st.tabs``, Streamlit garbage-collects the state
of any widget it did not draw on a given run. Two rules keep that from
quietly eating the user's selections:

  1. Every selector widget carries an explicit ``key`` — an auto-keyed widget
     cannot be reached from ``st.session_state`` and so cannot be preserved.
  2. Every such key is listed in ``_STICKY_WIDGETS``.

This test reads the app's source rather than running it, so a newly added
selectbox fails here immediately instead of on someone's third tab switch.
"""

import ast
from pathlib import Path

import pytest

from foodprep.ui.streamlit_app import _STICKY_PREFIXES, _STICKY_WIDGETS

APP = Path(__file__).resolve().parents[1] / "src" / "foodprep" / "ui" / "streamlit_app.py"

#: Widgets that hold a user selection worth keeping. Buttons are deliberately
#: absent: they are transient, and re-assigning their key breaks them.
SELECTORS = {
    "selectbox", "multiselect", "radio", "checkbox", "toggle",
    "text_input", "text_area", "number_input", "slider", "select_slider",
    "date_input", "time_input", "pills", "segmented_control",
}


#: Our own helpers that wrap a selector widget. The wrapper's own st.* call
#: takes a variable key, so it is skipped; its call sites supply the literal.
WRAPPERS = {"pill_radio": 2}   # name -> positional index of the key argument


def _wrapper_body_lines(tree):
    """Line numbers inside a wrapper's definition, whose st.* call we skip."""
    lines = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name in WRAPPERS:
            for inner in ast.walk(node):
                if hasattr(inner, "lineno"):
                    lines.add(inner.lineno)
    return lines


def _selector_calls():
    tree = ast.parse(APP.read_text(encoding="utf-8"))
    skip = _wrapper_body_lines(tree)
    # call sites of our wrappers count as keyed selectors
    for node in ast.walk(tree):
        if (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                and node.func.id in WRAPPERS):
            idx = WRAPPERS[node.func.id]
            key = None
            if len(node.args) > idx and isinstance(node.args[idx], ast.Constant):
                key = node.args[idx].value
            else:
                kw = next((k for k in node.keywords if k.arg == "key"), None)
                if kw is not None and isinstance(kw.value, ast.Constant):
                    key = kw.value.value
            yield node.func.id, key, node.lineno
    for node in ast.walk(tree):
        if getattr(node, "lineno", None) in skip:
            continue
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if (isinstance(func, ast.Attribute) and func.attr in SELECTORS
                and isinstance(func.value, ast.Name) and func.value.id == "st"):
            kw = next((k for k in node.keywords if k.arg == "key"), None)
            if kw is None:
                key = None
            elif isinstance(kw.value, ast.Constant):
                key = kw.value.value
            elif isinstance(kw.value, ast.JoinedStr):
                # f"taste_circle_{dim}" -> the literal prefix, marked dynamic
                head = kw.value.values[0]
                key = ("dynamic", head.value if isinstance(head, ast.Constant) else "")
            else:
                key = ("dynamic", "")
            yield func.attr, key, node.lineno


def test_every_selector_widget_has_an_explicit_key():
    unkeyed = [(w, line) for w, key, line in _selector_calls() if key is None]
    assert not unkeyed, (
        "auto-keyed selector(s) will reset on tab switch; add key=: "
        + ", ".join(f"st.{w} at line {line}" for w, line in unkeyed))


def test_every_selector_key_is_sticky():
    keys = {key for _w, key, _l in _selector_calls()
            if isinstance(key, str)}
    missing = keys - set(_STICKY_WIDGETS)
    assert not missing, (
        f"add to _STICKY_WIDGETS or they reset on tab switch: {sorted(missing)}")


def test_dynamically_keyed_selectors_are_covered_by_a_prefix():
    dynamic = [(k[1], line) for _w, k, line in _selector_calls()
               if isinstance(k, tuple)]
    assert dynamic, "expected the per-dimension Taste Circle selectboxes"
    for prefix, line in dynamic:
        assert prefix and prefix.startswith(_STICKY_PREFIXES), (
            f"dynamic key at line {line} ({prefix!r}) is not covered by "
            f"_STICKY_PREFIXES {_STICKY_PREFIXES}")


def test_sticky_list_has_no_dead_entries():
    keys = {key for _w, key, _l in _selector_calls() if isinstance(key, str)}
    stale = {k for k in _STICKY_WIDGETS
             if k not in keys and not k.startswith(_STICKY_PREFIXES)}
    assert not stale, f"_STICKY_WIDGETS names widgets that no longer exist: {sorted(stale)}"


@pytest.mark.parametrize("button_key", ["tcm_prev", "tcm_next", "tcm_random", "tcm_reset"])
def test_button_keys_are_never_sticky(button_key):
    # Streamlit refuses to build a button whose key was set via session_state.
    assert button_key not in _STICKY_WIDGETS
    assert not button_key.startswith(_STICKY_PREFIXES)


def test_no_button_key_collides_with_a_sticky_prefix():
    tree = ast.parse(APP.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                and node.func.attr in {"button", "download_button"}):
            for kw in node.keywords:
                if kw.arg != "key":
                    continue
                if isinstance(kw.value, ast.Constant):
                    head = kw.value.value
                elif isinstance(kw.value, ast.JoinedStr):
                    first = kw.value.values[0]
                    head = first.value if isinstance(first, ast.Constant) else ""
                else:
                    continue
                assert not head.startswith(_STICKY_PREFIXES), (
                    f"button key {head!r} at line {node.lineno} would be "
                    "persisted, and Streamlit then refuses to build it")
