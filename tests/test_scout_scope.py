"""Scout rules only speak where their wording holds.

Rules used to fire wherever a state's flavour tags lined up, so the
potato-soup anchovy rule told cooks to put "1 cup soup : 1 anchovy fillet"
on roasted broccoli. Scope (serving form, ingredient family, or exact
states) keeps rules in place; the wording guard guarantees a mis-scoped rule
never reaches the UI; these tests keep the guard's catch empty so that a
scoping mistake is fixed in the data rather than silently hidden.
"""

import sqlite3

import pytest

from foodprep import loader, query

PLACEHOLDER = "{state}"


def _states(conn):
    return [r[0] for r in conn.execute(
        "SELECT c.name FROM component_state_profiles sp "
        "JOIN components c USING (component_id) ORDER BY c.name")]


def _all(conn, include_rejected=False):
    for state in _states(conn):
        for h in query.generate_scout_hypotheses(conn, state, include_rejected):
            yield state, h


def test_every_state_has_a_serving_form(conn):
    missing = conn.execute(
        "SELECT COUNT(*) FROM component_state_profiles WHERE serving_form IS NULL"
    ).fetchone()[0]
    assert missing == 0


def test_soup_rule_does_not_reach_roasted_broccoli(conn):
    hypotheses = query.generate_scout_hypotheses(
        conn, "roasted_broccoli_component", include_rejected=True)
    anchovy = next(h for h in hypotheses
                   if h["analogy_id"] == "anchovy_for_bacon_on_potato_soup")
    assert anchovy["candidate_class"] == "rejected"
    assert "soup" in anchovy["rejection_reason"]
    assert "cooked pieces" in anchovy["rejection_reason"]


def test_travelling_rule_names_the_state_it_lands_on(conn):
    soup = next(h for h in query.generate_scout_hypotheses(conn, "tomato_soup_base")
                if h["candidate"] == "anchovy")
    assert "warm tomato soup" in soup["protocol"]["smallest_test"]
    assert "potato" not in soup["protocol"]["smallest_test"]


def test_no_live_hypothesis_leaks_another_food_or_a_placeholder(conn):
    for state, h in _all(conn):
        texts = [h["shared_function"], h["meaningful_difference"],
                 h["expected_risk"], h["explanation"]]
        texts += list((h["protocol"] or {}).values())
        for text in texts:
            assert PLACEHOLDER not in text, (state, h["analogy_id"], text)


def test_wording_guard_catches_nothing_in_shipped_rules(conn):
    """A wording rejection means a rule is scoped wider than its text.

    Fix the rule's `forms` / `families` / `states` or rewrite it with
    {state}; do not loosen this test.
    """
    caught = [
        (state, h["analogy_id"], h["scope_reason"])
        for state, h in _all(conn, include_rejected=True)
        if h["scope_reason"] and h["scope_reason"].startswith("its ")
    ]
    assert caught == []


def test_rule_never_replaces_the_state_itself(conn):
    tomato = query.generate_scout_hypotheses(
        conn, "fresh_tomato_component", include_rejected=True)
    peach = [h for h in tomato
             if h["analogy_id"] == "stone_fruit_for_tomato_in_cool_salad"]
    assert all(h["candidate_class"] == "rejected" for h in peach)


def test_one_card_per_candidate_per_state(conn):
    for state in _states(conn):
        live = [h["candidate"] for h in query.generate_scout_hypotheses(conn, state)]
        assert len(live) == len(set(live)), state


def test_recorded_tasting_keeps_its_hypothesis(conn):
    brown_butter = next(
        h for h in query.generate_scout_hypotheses(conn, "roasted_broccoli_component")
        if h["candidate"] == "brown_butter")
    assert brown_butter["trials"]


def test_restored_rule_is_its_own_rule(conn):
    ids = {r[0] for r in conn.execute("SELECT analogy_id FROM analogy_rules")}
    assert {"soft_egg_for_butter_on_mashed_potato",
            "tahini_for_cheese_on_caramelized_onion"} <= ids
    tahini = conn.execute(
        "SELECT i.canonical_name FROM analogy_rules ar "
        "JOIN ingredients i ON i.ingredient_id = ar.substitute_ingredient_id "
        "WHERE analogy_id = 'tahini_for_cheese_on_caramelized_onion'").fetchone()[0]
    assert tahini == "tahini"


def test_duplicate_yaml_keys_are_refused(tmp_path):
    path = tmp_path / "dup.yaml"
    path.write_text("a:\n  id: one\n  id: two\n", encoding="utf-8")
    with pytest.raises(loader.LoadError, match="duplicate key 'id'"):
        loader.load_yaml(path)


def _build_with_rules(tmp_path, rules_text):
    path = tmp_path / "rules.yaml"
    path.write_text(rules_text, encoding="utf-8")
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    loader.build(conn, scout_rules_path=path, tastings_path=None, novelty_path=None)


_RULE = """analogy_rules:
  - id: test_rule
    known_pairing: "x"
    source_ingredient: lemon
    substitute_ingredient: sumac
    mechanism: aroma_bridge
    shared_function: "x."
    meaningful_difference: "x"
    expected_risk: "x"
    required_dimensions: "sour"
    explanation_template: "{candidate}"
    inference_strength: low
"""


def test_unscoped_rule_is_refused(tmp_path):
    with pytest.raises(loader.LoadError, match="needs `forms` or `states`"):
        _build_with_rules(tmp_path, _RULE)


def test_unknown_serving_form_is_refused(tmp_path):
    from foodprep.vocabulary import VocabularyError
    with pytest.raises(VocabularyError, match="serving_forms"):
        _build_with_rules(tmp_path, _RULE + "    forms: [casserole]\n")
