"""What the user actually cooked and saw: control records and shelf checks (R7).

Two append-only files, kept apart from every documented record:

- **Control records** (`records/control_records.yaml`): one cooking of one
  documented route, with the times it actually took, the endpoint each member
  reached, a verdict and notes. ISA-88 calls this the batch-level record of a
  control recipe (R6 Y602, Y604). It is shown *beside* the documented values of
  the route and never merged into them: a 62-minute bake in this oven does not
  change what the sources say.
- **Shelf checks** (`records/shelf_checks.yaml`): the user's own look at a shop
  shelf. Availability in the app comes only from here, never from lidl.fi,
  which lists offers only (R4 `catalogue.md`).

Both reuse the Scout tasting store's append-only writer
(`tasting.append_record_yaml`): the file is never rewritten, a new block must
parse strictly and round-trip, and a duplicate is refused. Nothing here reads
or writes `src/foodprep/data/`.

The paths can be moved with FOODPREP_CONTROL_RECORDS_PATH and
FOODPREP_SHELF_CHECKS_PATH (tests point them at a temporary folder).
"""

from __future__ import annotations

import os
import re
from datetime import date
from pathlib import Path
from typing import Any

from foodprep import conditions as cd
from foodprep.tasting import TastingError, append_record_yaml

ROOT = Path(__file__).resolve().parents[2]
RECORDS = ROOT / "records"
CONTROL_ENV = "FOODPREP_CONTROL_RECORDS_PATH"
SHELF_ENV = "FOODPREP_SHELF_CHECKS_PATH"
OPEN_QUESTIONS = ROOT / "docs" / "research" / "r6-academic-foundations" / "open-questions.md"

#: What a cooking came to. Words, not a scale: nothing here is a score.
VERDICTS = {
    "works": "worked as documented",
    "works_with_changes": "worked, with changes (say which in the notes)",
    "failed": "failed (say how in the notes)",
    "inconclusive": "inconclusive",
}
KT_ID = re.compile(r"^KT\d+$")

_CONTROL_HEADER = """\
# Control records (R7): what was actually cooked, one cooking per entry.
#
# Append-only. A record is an observation of one cooking in one kitchen
# (ISA-88's batch record): it never changes the documented values in
# src/foodprep/data/, and the app shows it beside them, never merged.
# If a second cooking disagrees, add a second record.
#
# Fields: route (dish/route or transfer:<id>), alternative (the documented R5
# alternative followed, if any), kitchen_test (KT id from
# docs/research/r6-academic-foundations/open-questions.md), cooked_on,
# step_times {step address: what it actually took}, endpoints {member: what it
# reached}, verdict (works | works_with_changes | failed | inconclusive), notes.

"""

_SHELF_HEADER = """\
# Shelf checks (R7): the user's own look at a shop shelf, append-only.
# The only source of availability in the app; lidl.fi is never used for it.
# Fields: ingredient, checked_on, shop, seen (true/false), note.

"""


class RecordError(TastingError):
    pass


def control_path() -> Path:
    override = os.environ.get(CONTROL_ENV)
    return Path(override) if override else RECORDS / "control_records.yaml"


def shelf_path() -> Path:
    override = os.environ.get(SHELF_ENV)
    return Path(override) if override else RECORDS / "shelf_checks.yaml"


def _read(path: Path, key: str) -> list[dict]:
    if not path.exists():
        return []
    from foodprep.loader import load_yaml
    return list((load_yaml(path) or {}).get(key) or [])


# ---- control records -------------------------------------------------------------

def control_records(route: str | None = None) -> list[dict]:
    """Every control record, or those of one route, in the order written."""
    out = _read(control_path(), "control_records")
    return [r for r in out if route is None or r.get("route") == route]


def _iso(day: str) -> str:
    try:
        return date.fromisoformat(str(day)).isoformat()
    except ValueError as exc:
        raise RecordError(f"cooked_on must be a date (YYYY-MM-DD), not {day!r}") from exc


def _clean(d: dict | None) -> dict:
    return {str(k): " ".join(str(v).split()) for k, v in (d or {}).items()
            if v is not None and str(v).strip()}


def build_control_record(route: str, *, cooked_on: str, verdict: str,
                         step_times: dict | None = None, endpoints: dict | None = None,
                         notes: str = "", kitchen_test: str | None = None,
                         alternative: str | None = None) -> dict[str, Any]:
    """Check one cooking against the route it was cooked from; return the record.

    Raises RecordError for an unknown route, step, verdict, kitchen test or
    alternative, or a record that says nothing beyond the verdict.
    """
    r = cd.routes().get(route)
    if r is None:
        raise RecordError(f"no documented route {route!r}")
    if verdict not in VERDICTS:
        raise RecordError(f"verdict must be one of {sorted(VERDICTS)}")
    if kitchen_test and not KT_ID.match(kitchen_test):
        raise RecordError(f"kitchen_test must look like KT1, not {kitchen_test!r}")
    alts = [a.get("name") for a in (cd.sequence(route) or {}).get("alternatives") or []]
    if alternative and alternative not in alts:
        raise RecordError(f"{alternative!r} is not a documented alternative of {route}")
    times = _clean(step_times)
    known = {p.address for p in r.points}
    unknown = sorted(set(times) - known)
    if unknown:
        raise RecordError(f"steps not in {route}: {unknown}")
    ends = _clean(endpoints)
    note = " ".join((notes or "").split())
    if not (times or ends or note):
        raise RecordError("say something about the cooking: a time, an endpoint or a note")
    rec: dict[str, Any] = {"route": route}
    if alternative:
        rec["alternative"] = alternative
    if kitchen_test:
        rec["kitchen_test"] = kitchen_test
    rec["cooked_on"] = _iso(cooked_on)
    if times:
        rec["step_times"] = times
    if ends:
        rec["endpoints"] = ends
    rec["verdict"] = verdict
    if note:
        rec["notes"] = note
    return rec


def record_cooking(route: str, **fields) -> dict[str, Any]:
    """Validate and append one control record; returns what was written."""
    rec = build_control_record(route, **fields)
    append_record_yaml(control_path(), "control_records", rec,
                       ("route", "alternative", "kitchen_test", "cooked_on"),
                       noun="control record", header=_CONTROL_HEADER)
    return rec


# ---- shelf checks ----------------------------------------------------------------

def shelf_checks(ingredient: str | None = None) -> list[dict]:
    out = _read(shelf_path(), "shelf_checks")
    return [r for r in out if ingredient is None or r.get("ingredient") == ingredient]


def record_shelf_check(ingredient: str, *, checked_on: str, seen: bool,
                       shop: str = "Lidl", note: str = "") -> dict[str, Any]:
    if not ingredient or not str(ingredient).strip():
        raise RecordError("which ingredient was looked for?")
    rec: dict[str, Any] = {"ingredient": str(ingredient).strip(),
                           "checked_on": _iso(checked_on),
                           "shop": " ".join(str(shop or "Lidl").split()),
                           "seen": bool(seen)}
    if note and note.strip():
        rec["note"] = " ".join(note.split())
    append_record_yaml(shelf_path(), "shelf_checks", rec,
                       ("ingredient", "checked_on", "shop"),
                       noun="shelf check", header=_SHELF_HEADER)
    return rec


# ---- the kitchen tests the form serves -------------------------------------------

def kitchen_tests() -> list[tuple[str, str]]:
    """(id, question) for KT1... from R6's open-question register, read-only.
    Empty when the research documents are not next to the package."""
    if not OPEN_QUESTIONS.exists():
        return []
    out = []
    for line in OPEN_QUESTIONS.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^\| (KT\d+) \| ([^|]+) \|", line)
        if m:
            out.append((m.group(1), " ".join(m.group(2).split())))
    return out
