"""SQLite connection and schema bootstrap."""

from __future__ import annotations

import sqlite3
from pathlib import Path

SCHEMA_PATH = Path(__file__).with_name("schema.sql")
DEFAULT_DB_PATH = Path("foodprep.sqlite")


def connect(db_path: Path | str = DEFAULT_DB_PATH) -> sqlite3.Connection:
    """Open a SQLite connection with foreign keys on and a dict-ish row factory."""
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def apply_schema(conn: sqlite3.Connection) -> None:
    """Create all tables/views from schema.sql. Idempotent-ish: drops nothing,
    relies on CREATE TABLE without IF NOT EXISTS failing only if already present.
    Use rebuild() to reset."""
    conn.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))


def rebuild(conn: sqlite3.Connection) -> None:
    """Drop everything and re-apply schema from scratch."""
    conn.executescript(
        "PRAGMA writable_schema = 1;"
        "DELETE FROM sqlite_master WHERE type IN ('table','view','index','trigger');"
        "PRAGMA writable_schema = 0;"
        "VACUUM;"
    )
    apply_schema(conn)