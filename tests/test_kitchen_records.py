"""R7: control records and shelf checks (foodprep.kitchen_records).

The user's own records: append-only, in their own files, never merged into the
documented data, and shown beside it.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from foodprep import dinner as d
from foodprep import kitchen_records as kr
from foodprep.loader import load_yaml
from foodprep.ui import dinner_render as dnr

GRATIN = "transfer:rutabaga_gratin"
BLANCH = f"{GRATIN}/rutabaga/3"
BAKE = f"{GRATIN}/gratin/1"


@pytest.fixture(autouse=True)
def _paths(tmp_path, monkeypatch):
    monkeypatch.setenv(kr.CONTROL_ENV, str(tmp_path / "control.yaml"))
    monkeypatch.setenv(kr.SHELF_ENV, str(tmp_path / "shelf.yaml"))
    return tmp_path


def _kt1(**over):
    fields = dict(cooked_on="2026-11-26", verdict="works", kitchen_test="KT1",
                  step_times={BLANCH: "4 min", BAKE: "62 min, covered then uncovered"},
                  endpoints={"rutabaga": "some give", "potato": "no resistance"},
                  notes="good with rye bread")
    fields.update(over)
    return kr.record_cooking(GRATIN, **fields)


def test_records_live_outside_the_documented_data():
    data = Path(d.cd.PATH).parent
    assert data not in kr.control_path().parents
    assert kr.RECORDS.parent == Path(d.cd.__file__).resolve().parents[2]
    assert "data" not in kr.RECORDS.parts[-1]


def test_a_kt1_record_round_trips(_paths):
    rec = _kt1()
    assert kr.control_records(GRATIN) == [rec]
    text = kr.control_path().read_text(encoding="utf-8")
    assert text.startswith("# Control records (R7)")
    assert load_yaml(kr.control_path())["control_records"] == [rec]


def test_the_file_is_appended_never_rewritten():
    _kt1()
    first = kr.control_path().read_text(encoding="utf-8")
    _kt1(alternative="raw slices and a long covered bake", kitchen_test="KT8",
         step_times={BAKE: "95 min"}, endpoints={}, notes="")
    assert kr.control_path().read_text(encoding="utf-8").startswith(first)
    assert len(kr.control_records(GRATIN)) == 2


def test_a_duplicate_is_refused():
    _kt1()
    with pytest.raises(kr.TastingError, match="already recorded"):
        _kt1(notes="again")


@pytest.mark.parametrize("bad, match", [
    (dict(verdict="great"), "verdict"),
    (dict(kitchen_test="test one"), "KT1"),
    (dict(alternative="a combination nobody documented"), "not a documented alternative"),
    (dict(step_times={"falafel/raw_soaked/paste/3": "3 min"}), "steps not in"),
    (dict(cooked_on="yesterday"), "date"),
    (dict(step_times={}, endpoints={}, notes=" "), "say something"),
])
def test_invalid_records_are_refused(bad, match):
    with pytest.raises(kr.RecordError, match=match):
        _kt1(**bad)
    assert kr.control_records() == []


def test_unknown_route_is_refused():
    with pytest.raises(kr.RecordError, match="no documented route"):
        kr.record_cooking("transfer:nope", cooked_on="2026-11-26", verdict="works", notes="x")


def test_control_record_is_shown_beside_never_merged():
    before = d.overview(GRATIN)
    blanch_times = [x.text for x in before.branches[1].steps[2].times]
    _kt1()
    ov = d.overview(GRATIN)
    blanch = ov.branches[1].steps[2]
    assert [x.text for x in blanch.times] == blanch_times     # documented values unchanged
    assert blanch.recorded == [("2026-11-26", "4 min")]
    html = dnr.overview_html(ov)
    assert "Your record" in html and "Kept apart from the documented values" in html
    oc = next(o for o in d.outcomes("rutabaga").less_usual if o.key == GRATIN)
    assert oc.cooked and "KT1, 2026-11-26" in dnr.outcome_card_html(oc)


def test_shelf_checks_round_trip_and_refuse_duplicates():
    rec = kr.record_shelf_check("dried_peas", checked_on="2026-11-25", seen=False,
                                note="split peas not on the shelf")
    assert kr.shelf_checks("dried_peas") == [rec]
    with pytest.raises(kr.TastingError, match="already recorded"):
        kr.record_shelf_check("dried_peas", checked_on="2026-11-25", seen=True)


def test_kitchen_tests_come_from_the_open_question_register():
    ids = [k for k, _ in kr.kitchen_tests()]
    assert ids[:6] == ["KT1", "KT2", "KT3", "KT4", "KT5", "KT6"]
