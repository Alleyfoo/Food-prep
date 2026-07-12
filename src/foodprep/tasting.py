"""Controlled Scout tasting protocols and append-only trial records."""

from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from typing import Any

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
) -> dict[str, Any]:
    """Append one kitchen observation without modifying hypothesis evidence."""
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
