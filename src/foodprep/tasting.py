"""Controlled Scout tasting protocols and append-only trial records."""

from __future__ import annotations

import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from .query import generate_scout_hypotheses


VERDICTS = {
    "works",
    "promising",
    "works_only_in_this_form",
    "needs_adjustment",
    "dominated",
    "texturally_wrong",
    "clashes",
    "inconclusive",
}


class TastingError(ValueError):
    pass


#: Overrides where trials are appended. Tests point it at a temporary copy;
#: a hosted app can point it somewhere durable, because an installed package
#: directory is not.
TASTINGS_ENV = "FOODPREP_TASTINGS_PATH"


def tastings_path() -> Path:
    """The append-only tastings file: $FOODPREP_TASTINGS_PATH, else the repo's."""
    from .loader import TASTINGS_PATH
    override = os.environ.get(TASTINGS_ENV)
    return Path(override) if override else Path(TASTINGS_PATH)


def append_record_yaml(path: Path | str, list_key: str, record: dict[str, Any],
                       key_fields: tuple[str, ...], noun: str = "record",
                       header: str = "") -> None:
    """Append one record to the `list_key:` list of an append-only YAML file.

    Never rewrites what is there. The new block is checked first: the whole
    file plus the block must parse with the loader's strict YAML (no duplicate
    keys), the block must come back as exactly this record, and a record with
    the same `key_fields` must not already exist. Only then is the file opened,
    in append mode. The list must be the file's last top-level key. A missing
    file is started with `header` (comments) and the list key.

    Shared by the Scout tastings (tastings.yaml) and the R7 kitchen records
    (foodprep.kitchen_records), so both stores keep one set of guarantees.
    """
    from .loader import load_yaml  # strict loader; local import avoids a cycle

    path = Path(path)
    existing = (path.read_text(encoding="utf-8") if path.exists()
                else header + f"{list_key}:\n")
    if f"{list_key}:" not in existing:
        raise TastingError(f"{path} has no `{list_key}:` list to append to")
    body = yaml.safe_dump([record], sort_keys=False, allow_unicode=True, width=78)
    block = "\n" + "".join("  " + line if line.strip() else line
                           for line in body.splitlines(keepends=True))
    prefix = "" if existing.endswith("\n") else "\n"

    path.parent.mkdir(parents=True, exist_ok=True)
    probe = path.with_name(path.name + ".probe")
    try:
        probe.write_text(existing + prefix + block, encoding="utf-8")
        parsed = (load_yaml(probe) or {}).get(list_key) or []
    except Exception as exc:  # noqa: BLE001 - any parse failure blocks the write
        raise TastingError(f"the new {noun} would not parse cleanly: {exc}") from exc
    finally:
        probe.unlink(missing_ok=True)
    if not parsed or parsed[-1] != record:
        raise TastingError(f"the new {noun} did not round-trip; nothing was written")
    key = tuple(record.get(k) for k in key_fields)
    if any(tuple(t.get(k) for k in key_fields) == key for t in parsed[:-1]):
        raise TastingError(f"this {noun} is already recorded")

    if not path.exists():
        path.write_text(existing, encoding="utf-8", newline="\n")
    with open(path, "a", encoding="utf-8", newline="\n") as fh:
        fh.write(prefix + block)


def append_trial_yaml(path: Path | str, trial: dict[str, Any]) -> None:
    """Append one trial to tastings.yaml. Never rewrites what is there.

    The new block is checked first: the whole file plus the block must parse
    with the loader's strict YAML (no duplicate keys), the block must come back
    as exactly this trial, and an identical (hypothesis, state, time) trial
    must not already exist. Only then is the file opened, in append mode.
    """
    append_record_yaml(path, "tastings", trial,
                       ("analogy_id", "component", "tested_at"), noun="trial")


def _hypothesis(conn: sqlite3.Connection, component_name: str,
                candidate: str) -> dict[str, Any]:
    hypothesis = next(
        (item for item in generate_scout_hypotheses(conn, component_name)
         if item["candidate"] == candidate),
        None,
    )
    if hypothesis is None:
        raise TastingError(
            f"no accepted generated hypothesis for {component_name!r} + {candidate!r}"
        )
    return hypothesis


def protocol(conn: sqlite3.Connection, component_name: str,
             candidate: str) -> dict[str, Any]:
    hypothesis = _hypothesis(conn, component_name, candidate)
    if not hypothesis.get("protocol"):
        raise TastingError(f"no tasting protocol for {hypothesis['analogy_id']!r}")
    return {
        "state": component_name,
        "candidate": candidate,
        "analogy_id": hypothesis["analogy_id"],
        **hypothesis["protocol"],
    }


def record_trial(
    conn: sqlite3.Connection,
    component_name: str,
    candidate: str,
    *,
    verdict: str,
    preparation: str,
    ratio: str,
    temperature: str,
    observations: str,
    supporting_ingredients: str | None = None,
    failure_mode: str | None = None,
    successful_correction: str | None = None,
    safety_confirmed: bool = False,
    tested_at: str | None = None,
    yaml_path: Path | str | None = None,
) -> dict[str, Any]:
    """Append one kitchen observation without modifying hypothesis evidence.

    With *yaml_path*, the trial is also appended to that tastings file — the
    durable record the app builds from. Without it, it lives only in *conn*.
    The file is written first: the database is rebuilt from it, never the
    other way round.
    """
    if verdict not in VERDICTS:
        raise TastingError(f"unknown tasting verdict: {verdict!r}")
    if not safety_confirmed:
        raise TastingError("safety_confirmed is required before recording a trial")
    for name, value in {
        "preparation": preparation,
        "ratio": ratio,
        "temperature": temperature,
        "observations": observations,
    }.items():
        if not value or not value.strip():
            raise TastingError(f"{name} is required")

    hypothesis = _hypothesis(conn, component_name, candidate)
    component_id = conn.execute(
        "SELECT component_id FROM components WHERE name = ?", (component_name,)
    ).fetchone()[0]
    candidate_id = conn.execute(
        "SELECT ingredient_id FROM ingredients WHERE canonical_name = ?", (candidate,)
    ).fetchone()[0]
    timestamp = tested_at or datetime.now(timezone.utc).isoformat()
    if yaml_path is not None:
        record = {
            "analogy_id": hypothesis["analogy_id"],
            "component": component_name,
            "candidate": candidate,
            "tested_at": timestamp,
            "preparation": preparation.strip(),
            "ratio": ratio.strip(),
            "temperature": temperature.strip(),
            "supporting_ingredients": (supporting_ingredients.strip()
                                       if supporting_ingredients else None),
            "verdict": verdict,
            "observations": observations.strip(),
            "failure_mode": failure_mode.strip() if failure_mode else None,
            "successful_correction": (successful_correction.strip()
                                      if successful_correction else None),
            "safety_confirmed": True,
        }
        append_trial_yaml(yaml_path, {k: v for k, v in record.items()
                                      if v is not None})
    conn.execute(
        """INSERT INTO tasting_trials(
             analogy_id, component_id, candidate_ingredient_id, tested_at,
             preparation, ratio, temperature, supporting_ingredients, verdict,
             observations, failure_mode, successful_correction, safety_confirmed)
           VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        (
            hypothesis["analogy_id"], component_id, candidate_id, timestamp,
            preparation.strip(), ratio.strip(), temperature.strip(),
            supporting_ingredients.strip() if supporting_ingredients else None,
            verdict, observations.strip(),
            failure_mode.strip() if failure_mode else None,
            successful_correction.strip() if successful_correction else None, 1,
        ),
    )
    trial_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    conn.commit()
    return trial(conn, trial_id)


def trial(conn: sqlite3.Connection, trial_id: int) -> dict[str, Any]:
    row = conn.execute(
        """SELECT tt.*, c.name AS state, i.canonical_name AS candidate
           FROM tasting_trials tt
           JOIN components c ON c.component_id = tt.component_id
           JOIN ingredients i ON i.ingredient_id = tt.candidate_ingredient_id
           WHERE tt.trial_id = ?""",
        (trial_id,),
    ).fetchone()
    if row is None:
        raise TastingError(f"unknown tasting trial: {trial_id}")
    result = dict(row)
    result["safety_confirmed"] = bool(result["safety_confirmed"])
    return result


def trials_for_hypothesis(conn: sqlite3.Connection, component_name: str,
                          candidate: str) -> list[dict[str, Any]]:
    rows = conn.execute(
        """SELECT tt.trial_id FROM tasting_trials tt
           JOIN components c ON c.component_id = tt.component_id
           JOIN ingredients i ON i.ingredient_id = tt.candidate_ingredient_id
           WHERE c.name = ? AND i.canonical_name = ?
           ORDER BY tt.tested_at, tt.trial_id""",
        (component_name, candidate),
    ).fetchall()
    return [trial(conn, row[0]) for row in rows]


def render_protocol(data: dict[str, Any]) -> str:
    return "\n".join([
        f"Tasting protocol: {data['state']} + {data['candidate']}",
        f"Starting ratio: {data['starting_ratio']}",
        f"Smallest test: {data['smallest_test']}",
        f"Success condition: {data['success_condition']}",
        f"Likely failure: {data['likely_failure']}",
        f"Corrections: {data['corrections']}",
        f"Safety: {data['safety_note']}",
    ])
