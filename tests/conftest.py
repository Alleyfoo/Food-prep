"""Shared pytest fixture: an in-memory built db."""

import sqlite3
import pytest

from foodprep.loader import build


@pytest.fixture()
def conn():
    c = sqlite3.connect(":memory:")
    c.row_factory = sqlite3.Row
    c.execute("PRAGMA foreign_keys = ON")
    build(c)
    yield c
    c.close()